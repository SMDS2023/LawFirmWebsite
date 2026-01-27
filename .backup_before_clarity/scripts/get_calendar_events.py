#!/usr/bin/env python3
"""
Pull calendar events for next 30 days and identify court dates/conflicts.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Configuration
CONFIG_DIR = Path(__file__).parent / "config"
BASE_DIR = Path(__file__).parent.parent.parent.parent
CALENDAR_CLIENT_SECRET = BASE_DIR / "LotterLaw" / "Admin" / "Calendar" / "client_secret_1095806145319-lkef8fm7b3gdks3rshn44ne6h5v1idh8.apps.googleusercontent.com.json"
CALENDAR_TOKEN_FILE = CONFIG_DIR / "calendar_token.json"
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_credentials():
    """Get valid credentials, refreshing if needed."""
    creds = None
    if CALENDAR_TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(CALENDAR_TOKEN_FILE), CALENDAR_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
            CALENDAR_TOKEN_FILE.write_text(creds.to_json())
        else:
            print("ERROR: No valid credentials. Run list_calendars.py first to authenticate.")
            return None

    return creds


def main():
    print("=" * 70)
    print("Calendar Events - Next 30 Days")
    print("=" * 70)
    print()

    creds = get_credentials()
    if not creds:
        return

    service = build('calendar', 'v3', credentials=creds)

    # Time range: now to 30 days from now
    now = datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    time_max = (now + timedelta(days=30)).isoformat() + 'Z'

    print(f"Date range: {now.strftime('%Y-%m-%d')} to {(now + timedelta(days=30)).strftime('%Y-%m-%d')}")
    print()

    # Get all calendars
    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get('items', [])

    all_events = []
    court_events = []

    for cal in calendars:
        cal_id = cal.get('id', '')
        cal_name = cal.get('summary', 'Untitled')

        try:
            events_result = service.events().list(
                calendarId=cal_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            events = events_result.get('items', [])

            for event in events:
                start = event.get('start', {})
                end = event.get('end', {})
                summary = event.get('summary', 'No Title')
                location = event.get('location', '')

                # Get date/time
                start_dt = start.get('dateTime', start.get('date', ''))
                end_dt = end.get('dateTime', end.get('date', ''))

                event_data = {
                    'calendar': cal_name,
                    'summary': summary,
                    'start': start_dt,
                    'end': end_dt,
                    'location': location,
                    'all_day': 'date' in start
                }

                all_events.append(event_data)

                # Check if it's a court date
                court_keywords = ['court', 'hearing', 'trial', 'arraignment', 'motion',
                                  'pretrial', 'deposition', 'docket', 'sentencing',
                                  'probation', 'jail', 'prison', 'judge']
                summary_lower = summary.lower()
                location_lower = location.lower()

                is_court = any(kw in summary_lower or kw in location_lower for kw in court_keywords)
                if is_court:
                    court_events.append(event_data)

        except Exception as e:
            print(f"  Error reading {cal_name}: {e}")

    # Sort all events by start time
    all_events.sort(key=lambda x: x['start'])
    court_events.sort(key=lambda x: x['start'])

    # Print court dates first
    print("=" * 70)
    print("COURT DATES")
    print("=" * 70)
    if court_events:
        for event in court_events:
            start = event['start'][:16].replace('T', ' ') if 'T' in event['start'] else event['start']
            print(f"\n  {start}")
            print(f"  {event['summary']}")
            if event['location']:
                print(f"  Location: {event['location']}")
    else:
        print("  No court dates found in the next 30 days.")

    # Print all events
    print()
    print("=" * 70)
    print("ALL EVENTS")
    print("=" * 70)

    # Group by date
    events_by_date = {}
    for event in all_events:
        date_str = event['start'][:10]
        if date_str not in events_by_date:
            events_by_date[date_str] = []
        events_by_date[date_str].append(event)

    for date_str in sorted(events_by_date.keys()):
        events = events_by_date[date_str]
        # Parse date for display
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            date_display = date_obj.strftime('%A, %B %d, %Y')
        except:
            date_display = date_str

        print(f"\n{date_display}")
        print("-" * 40)

        for event in events:
            if event['all_day']:
                time_str = "All Day"
            else:
                time_str = event['start'][11:16] if 'T' in event['start'] else ""

            print(f"  {time_str:>8}  {event['summary']}")
            if event['location']:
                print(f"            {event['location']}")

    # Check for conflicts (overlapping events on same day)
    print()
    print("=" * 70)
    print("POTENTIAL CONFLICTS")
    print("=" * 70)

    conflicts_found = False
    for date_str, events in events_by_date.items():
        if len(events) > 1:
            # Check for time overlaps (non-all-day events)
            timed_events = [e for e in events if not e['all_day']]
            if len(timed_events) > 1:
                for i, e1 in enumerate(timed_events):
                    for e2 in timed_events[i+1:]:
                        # Simple overlap check
                        if e1['start'] < e2['end'] and e2['start'] < e1['end']:
                            conflicts_found = True
                            print(f"\n  {date_str}: OVERLAP DETECTED")
                            print(f"    - {e1['summary']} ({e1['start'][11:16]}-{e1['end'][11:16]})")
                            print(f"    - {e2['summary']} ({e2['start'][11:16]}-{e2['end'][11:16]})")

    if not conflicts_found:
        print("  No scheduling conflicts detected.")

    print()
    print(f"Total events: {len(all_events)}")
    print(f"Court dates: {len(court_events)}")


if __name__ == "__main__":
    main()
