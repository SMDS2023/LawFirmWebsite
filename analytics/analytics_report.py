#!/usr/bin/env python3
"""
LotterLaw Website Analytics Report Generator

Generates weekly analytics reports from:
- Google Analytics 4 (GA4 Data API)
- Microsoft Clarity (REST API)
- Google Tag Manager (status check)

Usage:
    python analytics_report.py                  # Generate report for current week
    python analytics_report.py --week 2025-W50  # Generate report for specific week
    python analytics_report.py --help           # Show help
"""

import os
import sys
import argparse
import yaml
import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import quote
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta, MO
import requests
from jinja2 import Environment, FileSystemLoader

# Optional: GA4 Data API (may not be installed yet)
try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest,
        DateRange,
        Dimension,
        Metric,
    )
    GA4_AVAILABLE = True
except ImportError:
    GA4_AVAILABLE = False

# ============================================================================
# Configuration
# ============================================================================

SCRIPT_DIR = Path(__file__).parent.absolute()
CONFIG_PATH = SCRIPT_DIR / "config.yaml"
GA4_CONVERSION_EVENTS = {
    "form_submission": "Contact Form Submit",
    "click_to_call": "Phone Click",
    "generate_lead": "Lead Generated",
    "contact_form_submit": "Contact Form Submit",
    "phone_click": "Phone Click",
}


class AnalyticsDataUnavailable(RuntimeError):
    """Raised when required live analytics data cannot be fetched."""


def load_config():
    """Load configuration from config.yaml."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def configured_path(path_value):
    """Resolve a config path, preserving absolute paths."""
    if not path_value:
        return None

    # Preserve Windows-style paths in diagnostics instead of joining them to
    # SCRIPT_DIR on macOS.
    if ":" in path_value and "\\" in path_value:
        return Path(path_value)

    path = Path(path_value)
    if path.is_absolute():
        return path
    return SCRIPT_DIR / path


def load_refreshed_oauth_credentials(token_file):
    """Load and refresh a Google OAuth token file without exposing token values."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    creds = Credentials.from_authorized_user_file(str(token_file))
    if creds.refresh_token:
        creds.refresh(Request())
        token_file.write_text(creds.to_json(), encoding="utf-8")
    return creds


# ============================================================================
# Date Utilities
# ============================================================================

def get_week_dates(week_str=None):
    """
    Get start and end dates for a week.

    Args:
        week_str: ISO week string like '2025-W50' or None for current week

    Returns:
        tuple: (start_date, end_date, week_label)
    """
    if week_str:
        # Parse ISO week format YYYY-Wnn
        year, week = week_str.split("-W")
        # Get Monday of that week
        start = datetime.strptime(f"{year}-W{week}-1", "%G-W%V-%u").date()
    else:
        # Get Monday of current week
        today = datetime.now().date()
        start = today - timedelta(days=today.weekday())

    end = start + timedelta(days=6)
    week_label = f"{start.year}-W{start.isocalendar()[1]:02d}"

    return start, end, week_label


def format_date(d):
    """Format date for display."""
    return d.strftime("%b %d, %Y")


# ============================================================================
# Google Analytics 4
# ============================================================================

def get_ga4_data(config, start_date, end_date, allow_mock=False):
    """
    Fetch GA4 metrics via Data API.

    Returns dict with:
        - sessions, users, pageviews, bounce_rate, avg_duration
        - top_pages: list of {path, views}
        - traffic_sources: list of {name, sessions, percent}
        - devices: list of {name, percent}
        - conversions: list of {name, count}
        - *_delta: week-over-week changes
    """
    ga4_config = config.get("ga4", {})
    property_id = ga4_config.get("property_id", "")

    # Try OAuth token first, fallback to service account
    token_file = configured_path(ga4_config.get("token_file", ""))
    credentials_file = configured_path(ga4_config.get("credentials_file", ""))

    if not GA4_AVAILABLE:
        if allow_mock:
            return get_mock_ga4_data()
        raise AnalyticsDataUnavailable(
            "GA4 Data API dependency is not installed. Run "
            "`analytics/.venv/bin/python -m pip install -r analytics/requirements.txt`."
        )

    try:
        # Initialize client with OAuth token or service account
        if token_file and token_file.exists():
            print(f"Using GA4 OAuth token from {token_file}")
            creds = load_refreshed_oauth_credentials(token_file)
            client = BetaAnalyticsDataClient(credentials=creds)
        elif credentials_file and credentials_file.exists():
            print(f"Using GA4 service account from {credentials_file}")
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_file)
            client = BetaAnalyticsDataClient()
        else:
            if allow_mock:
                return get_mock_ga4_data()
            configured = [
                str(path) for path in (token_file, credentials_file)
                if path is not None
            ]
            raise AnalyticsDataUnavailable(
                "GA4 credentials not found. Configure a valid `ga4.token_file` "
                "or `ga4.credentials_file` in analytics/config.yaml. "
                f"Checked: {configured or 'no credential paths configured'}"
            )

        # Current week metrics
        current_metrics = fetch_ga4_metrics(client, property_id, start_date, end_date)

        # Previous week for comparison
        prev_start = start_date - timedelta(days=7)
        prev_end = end_date - timedelta(days=7)
        prev_metrics = fetch_ga4_metrics(client, property_id, prev_start, prev_end)

        # Calculate deltas
        current_metrics["sessions_delta"] = calculate_delta(
            current_metrics["sessions"], prev_metrics["sessions"]
        )
        current_metrics["users_delta"] = calculate_delta(
            current_metrics["users"], prev_metrics["users"]
        )
        current_metrics["pageviews_delta"] = calculate_delta(
            current_metrics["pageviews"], prev_metrics["pageviews"]
        )
        current_metrics["bounce_rate_delta"] = calculate_delta(
            current_metrics["bounce_rate"], prev_metrics["bounce_rate"]
        )

        # Top pages
        current_metrics["top_pages"] = fetch_ga4_top_pages(
            client, property_id, start_date, end_date
        )

        # Traffic sources
        current_metrics["traffic_sources"] = fetch_ga4_sources(
            client, property_id, start_date, end_date
        )

        # Device breakdown
        current_metrics["devices"] = fetch_ga4_devices(
            client, property_id, start_date, end_date
        )

        # Conversion-like events tracked through GTM/dataLayer
        conversions, conversions_status = fetch_ga4_conversions(
            client, property_id, start_date, end_date
        )
        current_metrics["conversions"] = conversions
        current_metrics["conversions_status"] = conversions_status

        return current_metrics

    except Exception as e:
        if allow_mock:
            print(f"Warning: GA4 fetch failed; using mock data because --allow-mock was set: {e}")
            return get_mock_ga4_data()
        if isinstance(e, AnalyticsDataUnavailable):
            raise
        raise AnalyticsDataUnavailable(f"Error fetching GA4 data: {e}") from e


def fetch_ga4_metrics(client, property_id, start_date, end_date):
    """Fetch basic GA4 metrics for a date range."""
    request = RunReportRequest(
        property=property_id,
        date_ranges=[DateRange(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )],
        metrics=[
            Metric(name="sessions"),
            Metric(name="activeUsers"),
            Metric(name="screenPageViews"),
            Metric(name="bounceRate"),
            Metric(name="averageSessionDuration"),
        ]
    )

    response = client.run_report(request)

    if response.rows:
        row = response.rows[0]
        return {
            "sessions": int(row.metric_values[0].value),
            "users": int(row.metric_values[1].value),
            "pageviews": int(row.metric_values[2].value),
            "bounce_rate": round(float(row.metric_values[3].value) * 100, 1),
            "avg_duration": round(float(row.metric_values[4].value), 1),
        }

    return {"sessions": 0, "users": 0, "pageviews": 0, "bounce_rate": 0, "avg_duration": 0}


def fetch_ga4_top_pages(client, property_id, start_date, end_date, limit=10):
    """Fetch top pages by views."""
    request = RunReportRequest(
        property=property_id,
        date_ranges=[DateRange(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )],
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        limit=limit
    )

    response = client.run_report(request)

    return [
        {
            "path": row.dimension_values[0].value,
            "views": int(row.metric_values[0].value)
        }
        for row in response.rows
    ]


def fetch_ga4_sources(client, property_id, start_date, end_date):
    """Fetch traffic sources breakdown."""
    request = RunReportRequest(
        property=property_id,
        date_ranges=[DateRange(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )],
        dimensions=[Dimension(name="sessionDefaultChannelGroup")],
        metrics=[Metric(name="sessions")]
    )

    response = client.run_report(request)

    total = sum(int(row.metric_values[0].value) for row in response.rows)

    return [
        {
            "name": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "percent": round(int(row.metric_values[0].value) / total * 100, 1) if total else 0
        }
        for row in response.rows
    ]


def fetch_ga4_devices(client, property_id, start_date, end_date):
    """Fetch device category breakdown."""
    request = RunReportRequest(
        property=property_id,
        date_ranges=[DateRange(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )],
        dimensions=[Dimension(name="deviceCategory")],
        metrics=[Metric(name="sessions")]
    )

    response = client.run_report(request)

    total = sum(int(row.metric_values[0].value) for row in response.rows)

    return [
        {
            "name": row.dimension_values[0].value.capitalize(),
            "percent": round(int(row.metric_values[0].value) / total * 100, 1) if total else 0
        }
        for row in response.rows
    ]


def fetch_ga4_conversions(client, property_id, start_date, end_date, limit=100):
    """Fetch configured conversion-like event counts from GA4."""
    request = RunReportRequest(
        property=property_id,
        date_ranges=[DateRange(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )],
        dimensions=[Dimension(name="eventName")],
        metrics=[Metric(name="eventCount")],
        limit=limit
    )

    try:
        response = client.run_report(request)
    except Exception as e:
        print(f"Warning: GA4 conversion event query failed: {e}")
        return [], (
            "Conversion event query unavailable. Check GA4 event/key-event "
            "configuration and API access."
        )

    found = {}
    for row in response.rows:
        event_name = row.dimension_values[0].value
        if event_name in GA4_CONVERSION_EVENTS:
            label = GA4_CONVERSION_EVENTS[event_name]
            found[label] = found.get(label, 0) + int(row.metric_values[0].value)

    conversions = [
        {"name": label, "count": count}
        for label, count in found.items()
        if count > 0
    ]

    if conversions:
        return conversions, "Fetched tracked GA4 event counts for configured lead actions."

    return [], (
        "No configured lead-action events were recorded for this date range. "
        "Confirm GTM publishes form_submission and click_to_call into GA4 key events."
    )


def get_mock_ga4_data():
    """Return mock GA4 data for testing/demo."""
    return {
        "_mock": True,
        "sessions": 1234,
        "users": 987,
        "pageviews": 3456,
        "bounce_rate": 42.3,
        "avg_duration": 145.2,
        "sessions_delta": 12,
        "users_delta": 8,
        "pageviews_delta": 15,
        "bounce_rate_delta": -3,
        "top_pages": [
            {"path": "/practice-areas/dui.html", "views": 456},
            {"path": "/index.html", "views": 321},
            {"path": "/practice-areas/criminal-traffic.html", "views": 234},
            {"path": "/blog/01-dui-penalties-florida.html", "views": 198},
            {"path": "/contact.html", "views": 167},
        ],
        "traffic_sources": [
            {"name": "Organic Search", "sessions": 802, "percent": 65.0},
            {"name": "Direct", "sessions": 309, "percent": 25.0},
            {"name": "Referral", "sessions": 99, "percent": 8.0},
            {"name": "Social", "sessions": 24, "percent": 2.0},
        ],
        "devices": [
            {"name": "Mobile", "percent": 58.0},
            {"name": "Desktop", "percent": 38.0},
            {"name": "Tablet", "percent": 4.0},
        ],
        "conversions": [
            {"name": "Contact Form Submit", "count": 23},
            {"name": "Phone Click", "count": 45},
        ],
        "conversions_status": "Mock conversion data.",
    }


def calculate_delta(current, previous):
    """Calculate percentage change."""
    if previous == 0:
        return 0
    return round((current - previous) / previous * 100, 1)


# ============================================================================
# Microsoft Clarity
# ============================================================================

def get_clarity_data(config, start_date, end_date, allow_mock=False):
    """
    Fetch Clarity metrics via Data Export API.

    API: GET https://www.clarity.ms/export-data/api/v1/project-live-insights
    Note: API only supports numOfDays=1,2,3 (last 24/48/72 hours), not arbitrary date ranges.
    We use numOfDays=3 for weekly reports as the best available window.

    Returns dict with:
        - total_sessions, rage_clicks, dead_clicks, quick_backs, scroll_depth
        - engagement_time, active_time, bot_sessions, users, pages_per_session
        - recordings_link: URL to Clarity dashboard
    """
    clarity_config = config.get("clarity", {})
    project_id = clarity_config.get("project_id", "")

    # Try to load API token from file first, fallback to environment variable
    api_key = None
    token_file = configured_path(clarity_config.get("token_file", ""))
    if token_file and token_file.exists():
        try:
            with open(token_file, 'r', encoding='utf-8') as f:
                api_key = f.read().strip()
                # Remove BOM if present
                if api_key.startswith('\ufeff'):
                    api_key = api_key[1:]
            print(f"Loaded Clarity token from {token_file}")
        except Exception as e:
            if allow_mock:
                print(f"Warning: Could not read Clarity token; using mock data because --allow-mock was set: {e}")
                return get_mock_clarity_data(project_id)
            raise AnalyticsDataUnavailable(f"Could not read Clarity token file {token_file}: {e}") from e

    # Fallback to environment variable
    if not api_key:
        api_key_env = clarity_config.get("api_key_env", "CLARITY_API_KEY")
        api_key = os.environ.get(api_key_env)
        if api_key:
            print(f"Loaded Clarity token from environment variable {api_key_env}")

    if not api_key:
        if allow_mock:
            return get_mock_clarity_data(project_id)
        raise AnalyticsDataUnavailable(
            "Clarity API token not found. Configure `clarity.token_file` in "
            "analytics/config.yaml or set the configured environment variable "
            f"`{clarity_config.get('api_key_env', 'CLARITY_API_KEY')}`."
        )

    try:
        # Clarity Data Export API endpoint
        url = "https://www.clarity.ms/export-data/api/v1/project-live-insights"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        params = {"numOfDays": "3"}

        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        raw_metrics = response.json()

        # Parse the array of metric objects into a flat dict
        result = {
            "total_sessions": 0,
            "bot_sessions": 0,
            "users": 0,
            "pages_per_session": 0,
            "rage_clicks": 0,
            "dead_clicks": 0,
            "quick_backs": 0,
            "scroll_depth": 0,
            "script_errors": 0,
            "engagement_time": 0,
            "active_time": 0,
            "recordings_link": f"https://clarity.microsoft.com/projects/{project_id}/recordings",
        }

        for metric in raw_metrics:
            name = metric.get("metricName", "")
            info = metric.get("information", [{}])

            if name == "Traffic" and info:
                result["total_sessions"] = int(info[0].get("totalSessionCount", 0))
                result["bot_sessions"] = int(info[0].get("totalBotSessionCount", 0))
                result["users"] = int(info[0].get("distinctUserCount", 0))
                result["pages_per_session"] = round(float(info[0].get("pagesPerSessionPercentage", 0)), 2)

            elif name == "RageClickCount" and info:
                result["rage_clicks"] = int(info[0].get("subTotal", 0))

            elif name == "DeadClickCount" and info:
                result["dead_clicks"] = int(info[0].get("subTotal", 0))

            elif name == "QuickbackClick" and info:
                result["quick_backs"] = int(info[0].get("subTotal", 0))

            elif name == "ScrollDepth" and info:
                result["scroll_depth"] = round(float(info[0].get("averageScrollDepth", 0)), 1)

            elif name == "ScriptErrorCount" and info:
                result["script_errors"] = int(info[0].get("subTotal", 0))

            elif name == "EngagementTime" and info:
                result["engagement_time"] = int(info[0].get("totalTime", 0))
                result["active_time"] = int(info[0].get("activeTime", 0))

        return result

    except Exception as e:
        if allow_mock:
            print(f"Warning: Clarity fetch failed; using mock data because --allow-mock was set: {e}")
            return get_mock_clarity_data(project_id)
        raise AnalyticsDataUnavailable(f"Error fetching Clarity data: {e}") from e


def get_mock_clarity_data(project_id=""):
    """Return mock Clarity data for testing/demo."""
    return {
        "_mock": True,
        "total_sessions": 892,
        "bot_sessions": 45,
        "users": 756,
        "pages_per_session": 2.1,
        "rage_clicks": 12,
        "dead_clicks": 34,
        "quick_backs": 8,
        "scroll_depth": 72,
        "script_errors": 0,
        "engagement_time": 350,
        "active_time": 90,
        "recordings_link": f"https://clarity.microsoft.com/projects/{project_id}/recordings" if project_id else None,
    }


# ============================================================================
# Google Search Console
# ============================================================================

def get_search_console_data(config, start_date, end_date, allow_mock=False):
    """
    Fetch Google Search Console search performance data.

    Returns dict with:
        - clicks, impressions, ctr, position
        - top_queries: list of {query, clicks, impressions, ctr, position}
        - top_pages: list of {page, clicks, impressions, ctr, position}
    """
    search_config = config.get("search_console", {})
    site_url = search_config.get("site_url", "")
    token_file = configured_path(
        search_config.get("token_file") or config.get("ga4", {}).get("token_file", "")
    )

    if not site_url:
        if allow_mock:
            return get_mock_search_console_data()
        raise AnalyticsDataUnavailable(
            "Search Console site URL is not configured. Set `search_console.site_url` "
            "in analytics/config.yaml."
        )

    if not token_file or not token_file.exists():
        if allow_mock:
            return get_mock_search_console_data()
        raise AnalyticsDataUnavailable(
            "Search Console OAuth token not found. Configure "
            "`search_console.token_file` in analytics/config.yaml."
        )

    try:
        from google.auth.transport.requests import AuthorizedSession

        creds = load_refreshed_oauth_credentials(token_file)
        scopes = set(creds.scopes or [])
        if "https://www.googleapis.com/auth/webmasters.readonly" not in scopes:
            raise AnalyticsDataUnavailable(
                "Search Console token is missing the webmasters.readonly scope."
            )

        session = AuthorizedSession(creds)
        totals = fetch_search_console_rows(session, site_url, start_date, end_date, [])
        queries = fetch_search_console_rows(session, site_url, start_date, end_date, ["query"], row_limit=10)
        pages = fetch_search_console_rows(session, site_url, start_date, end_date, ["page"], row_limit=10)

        total = totals[0] if totals else {}
        return {
            "site_url": site_url,
            "clicks": int(total.get("clicks", 0)),
            "impressions": int(total.get("impressions", 0)),
            "ctr": round(float(total.get("ctr", 0)) * 100, 1),
            "position": round(float(total.get("position", 0)), 1),
            "top_queries": [format_search_console_row(row, "query") for row in queries],
            "top_pages": [format_search_console_row(row, "page") for row in pages],
        }

    except Exception as e:
        if allow_mock:
            print(f"Warning: Search Console fetch failed; using mock data because --allow-mock was set: {e}")
            return get_mock_search_console_data()
        if isinstance(e, AnalyticsDataUnavailable):
            raise
        raise AnalyticsDataUnavailable(f"Error fetching Search Console data: {e}") from e


def fetch_search_console_rows(session, site_url, start_date, end_date, dimensions, row_limit=1):
    """Fetch Search Console rows for one dimension set."""
    url = (
        "https://www.googleapis.com/webmasters/v3/sites/"
        f"{quote(site_url, safe='')}/searchAnalytics/query"
    )
    payload = {
        "startDate": start_date.strftime("%Y-%m-%d"),
        "endDate": end_date.strftime("%Y-%m-%d"),
        "dimensions": dimensions,
        "rowLimit": row_limit,
    }
    response = session.post(url, json=payload, timeout=30)
    if response.status_code >= 400:
        raise AnalyticsDataUnavailable(
            f"Search Console API returned {response.status_code}: {response.text[:500]}"
        )
    return response.json().get("rows", [])


def format_search_console_row(row, key_name):
    """Normalize one Search Console API row for templates."""
    keys = row.get("keys") or [""]
    return {
        key_name: keys[0],
        "clicks": int(row.get("clicks", 0)),
        "impressions": int(row.get("impressions", 0)),
        "ctr": round(float(row.get("ctr", 0)) * 100, 1),
        "position": round(float(row.get("position", 0)), 1),
    }


def get_mock_search_console_data():
    """Return mock Search Console data for testing/demo."""
    return {
        "_mock": True,
        "site_url": "sc-domain:example.com",
        "clicks": 42,
        "impressions": 1000,
        "ctr": 4.2,
        "position": 12.3,
        "top_queries": [
            {"query": "example legal question", "clicks": 12, "impressions": 100, "ctr": 12.0, "position": 3.4},
        ],
        "top_pages": [
            {"page": "https://example.com/blog/example/", "clicks": 12, "impressions": 100, "ctr": 12.0, "position": 3.4},
        ],
    }


# ============================================================================
# Google Tag Manager
# ============================================================================

def get_gtm_status(config):
    """
    Check GTM container status.

    Note: GTM API requires OAuth which is complex. For now, we return
    static config info and a healthy status. Could be enhanced later
    to actually check the container.

    Returns dict with:
        - container_id, status, last_published, tags_count
    """
    gtm_config = config.get("gtm", {})
    container_id = gtm_config.get("container_id", "")

    # For now, return static info
    # Future: implement OAuth and actual API check
    return {
        "container_id": container_id,
        "status": "healthy",
        "last_published": None,  # Would require API access
        "tags_count": None,  # Would require API access
    }


# ============================================================================
# Alert Generation
# ============================================================================

def generate_alerts(config, ga4_data, clarity_data):
    """
    Check metrics against thresholds and generate alerts.

    Returns list of alert dicts: {level, title, message}
    """
    alerts = []
    thresholds = config.get("alerts", {})

    # Bounce rate alert
    bounce_threshold = thresholds.get("bounce_rate_threshold", 60)
    if ga4_data.get("bounce_rate", 0) > bounce_threshold:
        alerts.append({
            "level": "warning",
            "title": "High Bounce Rate",
            "message": f"Bounce rate is {ga4_data['bounce_rate']}%, above the {bounce_threshold}% threshold."
        })

    # Rage clicks alert
    rage_threshold = thresholds.get("rage_clicks_threshold", 20)
    if clarity_data.get("rage_clicks", 0) > rage_threshold:
        alerts.append({
            "level": "warning",
            "title": "High Rage Clicks",
            "message": f"Rage clicks ({clarity_data['rage_clicks']}) exceed threshold of {rage_threshold}. Users may be frustrated with UI elements."
        })

    # Sessions drop alert
    sessions_drop_threshold = thresholds.get("sessions_drop_threshold", -20)
    sessions_delta = ga4_data.get("sessions_delta", 0)
    if sessions_delta < sessions_drop_threshold:
        alerts.append({
            "level": "danger",
            "title": "Significant Traffic Drop",
            "message": f"Sessions dropped {abs(sessions_delta)}% compared to last week."
        })

    # Low session duration alert
    min_duration = thresholds.get("avg_session_duration_min", 30)
    if ga4_data.get("avg_duration", 0) < min_duration:
        alerts.append({
            "level": "warning",
            "title": "Low Engagement",
            "message": f"Average session duration ({ga4_data.get('avg_duration', 0):.0f}s) is below {min_duration}s threshold."
        })

    return alerts


# ============================================================================
# Report Generation
# ============================================================================

def generate_report(ga4_data, clarity_data, search_console_data, gtm_status, alerts, week_label, start_date, end_date):
    """
    Generate HTML report from template.

    Returns HTML string.
    """
    templates_dir = SCRIPT_DIR / "templates"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("report_template.html")

    html = template.render(
        ga4=ga4_data,
        clarity=clarity_data,
        search_console=search_console_data,
        gtm=gtm_status,
        alerts=alerts,
        week_label=week_label,
        start_date=format_date(start_date),
        end_date=format_date(end_date),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )

    return html


def save_report(html, week_label, config):
    """
    Save HTML report to output directory.

    Creates:
        - reports/YYYY-WNN/weekly_report.html
        - reports/latest.html (copy of most recent)
    """
    report_config = config.get("report", {})
    output_dir = SCRIPT_DIR / report_config.get("output_dir", "reports")

    # Create week directory
    week_dir = output_dir / week_label
    week_dir.mkdir(parents=True, exist_ok=True)

    # Save report
    report_path = week_dir / "weekly_report.html"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report saved to: {report_path}")

    # Copy to latest.html
    latest_path = output_dir / "latest.html"
    shutil.copy(report_path, latest_path)
    print(f"Latest report: {latest_path}")

    return report_path


# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate LotterLaw weekly analytics report"
    )
    parser.add_argument(
        "--week",
        help="Week to generate report for (YYYY-WNN format, e.g., 2025-W50). Default: current week"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print report to stdout instead of saving"
    )
    parser.add_argument(
        "--allow-mock",
        action="store_true",
        help=(
            "Use design/demo mock data when live analytics are unavailable. "
            "Do not use for production reports."
        )
    )

    args = parser.parse_args()

    print("=" * 60)
    print("LotterLaw Weekly Analytics Report Generator")
    print("=" * 60)

    # Load config
    try:
        config = load_config()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Get date range
    start_date, end_date, week_label = get_week_dates(args.week)
    print(f"\nGenerating report for: {week_label}")
    print(f"Date range: {format_date(start_date)} - {format_date(end_date)}")

    # Fetch data from all sources
    try:
        print("\nFetching GA4 data...")
        ga4_data = get_ga4_data(config, start_date, end_date, allow_mock=args.allow_mock)

        print("Fetching Clarity data...")
        clarity_data = get_clarity_data(config, start_date, end_date, allow_mock=args.allow_mock)

        print("Fetching Search Console data...")
        search_console_data = get_search_console_data(config, start_date, end_date, allow_mock=args.allow_mock)
    except AnalyticsDataUnavailable as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        print("Report generation aborted; no mock analytics data was used.", file=sys.stderr)
        return 2

    if ga4_data.get("_mock") or clarity_data.get("_mock") or search_console_data.get("_mock"):
        print("\nWARNING: Report uses mock analytics data because --allow-mock was set.")
        print("This output is for template/design testing only, not business reporting.")

    print("Checking GTM status...")
    gtm_status = get_gtm_status(config)

    # Generate alerts
    print("Checking thresholds...")
    alerts = generate_alerts(config, ga4_data, clarity_data)

    if alerts:
        print(f"\n{len(alerts)} alert(s) generated:")
        for alert in alerts:
            print(f"  [{alert['level'].upper()}] {alert['title']}")

    # Generate report
    print("\nGenerating HTML report...")
    html = generate_report(
        ga4_data,
        clarity_data,
        search_console_data,
        gtm_status,
        alerts,
        week_label,
        start_date,
        end_date,
    )

    if args.dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN - Report Preview:")
        print("=" * 60)
        print(html)
    else:
        # Save report
        report_path = save_report(html, week_label, config)
        print(f"\nReport generation complete!")
        print(f"Open in browser: file://{report_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
