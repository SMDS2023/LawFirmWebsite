# Website Analytics

> **Last Updated:** 2025-12-12
> **Parent Project:** LotterLaw Website
> **Purpose:** Weekly analytics reporting from GA4, Clarity, Search Console, and GTM

## Project Overview

Automated weekly analytics report generator that pulls data from:
- **Google Analytics 4** - Traffic, sessions, pageviews, conversions
- **Microsoft Clarity** - User behavior, rage clicks, scroll depth
- **Google Search Console** - Search clicks, impressions, CTR, position, top queries/pages
- **Google Tag Manager** - Container status and tag health

## Folder Structure

```
analytics/
├── analytics_report.py     # Main report generator script
├── config.yaml             # API credentials paths, thresholds
├── requirements.txt        # Python dependencies
├── credentials/            # Service account keys (gitignored)
├── reports/                # Generated HTML reports by week
│   ├── 2025-W50/
│   │   └── weekly_report.html
│   └── latest.html         # Copy of most recent report
└── templates/
    └── report_template.html  # Jinja2 HTML template
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_APPLICATION_CREDENTIALS="credentials/ga4_service_account.json"
export CLARITY_API_KEY="your-api-key"

# Generate weekly report (current week)
python analytics_report.py

# Generate report for specific week
python analytics_report.py --week 2025-W50

# Dry run (preview without saving)
python analytics_report.py --dry-run
```

## Data Integrity Rule

Production analytics reports must use live data or fail. Missing credentials,
API errors, unavailable libraries, or empty upstream responses should produce a
nonzero exit code rather than substitute fake numbers.

Mock data is only allowed for original report/template design work and must be
requested explicitly:

```bash
python analytics_report.py --dry-run --allow-mock
```

Do not use `--allow-mock` for business reporting, SEO decisions, weekly reports,
or client-facing analysis.

As of 2026-05-24, live Lotter Law reports are expected to fetch GA4, Microsoft
Clarity, and Google Search Console. If any configured live source fails, the
report should exit nonzero rather than omit that source silently.

## Configuration

Edit `config.yaml` to set:
- GA4 property ID and credentials path
- Clarity project ID
- Search Console domain property and OAuth token path
- GTM container ID
- Alert thresholds (bounce rate, rage clicks, etc.)

## Credentials Setup

### GA4 Service Account
1. Go to Google Cloud Console
2. Create service account with Analytics Data API access
3. Download JSON key to `credentials/ga4_service_account.json`
4. Add service account email as viewer in GA4 admin

### Clarity API Key
1. Go to Clarity project settings
2. Generate API key
3. Set `CLARITY_API_KEY` environment variable

## Report Metrics

### GA4 Metrics
| Metric | Description |
|--------|-------------|
| Sessions | Total visits |
| Users | Unique visitors |
| Pageviews | Total pages viewed |
| Bounce Rate | Single-page sessions % |
| Avg Duration | Time on site |
| Top Pages | Most visited pages |
| Traffic Sources | Organic, direct, referral |
| Devices | Desktop, mobile, tablet |

### Clarity Metrics
| Metric | Description |
|--------|-------------|
| Rage Clicks | Frustrated repeated clicking |
| Dead Clicks | Clicks with no response |
| Quick Backs | Fast back-button presses |
| Scroll Depth | % of page scrolled |

## Alert Thresholds

Configured in `config.yaml`:
- Bounce rate > 60%
- Rage clicks > 20
- Sessions drop > 20% week-over-week
- Avg session duration < 30 seconds

## Playbook

| Strategy | Source |
|----------|--------|
| Always check credentials exist before API calls | Initial |
| Use mock data as fallback when APIs unavailable | Initial |
| Calculate week-over-week deltas for context | Initial |
| Save reports with ISO week labels (YYYY-WNN) | Initial |
