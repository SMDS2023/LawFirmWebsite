#!/usr/bin/env python3
"""
Add events to Google Calendar.
"""

import json
from datetime import datetime
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configuration
CONFIG_DIR = Path(__file__).parent / "config"
BASE_DIR = Path(__file__).parent.parent.parent.parent
CALENDAR_CLIENT_SECRET = BASE_DIR / "LotterLaw" / "Admin" / "Calendar" / "client_secret_1095806145319-lkef8fm7b3gdks3rshn44ne6h5v1idh8.apps.googleusercontent.com.json"
CALENDAR_TOKEN_FILE = CONFIG_DIR / "calendar_token_write.json"
# Need write scope to add events
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_credentials():
    """Get valid credentials with write access, authenticating if needed."""
    creds = None
    if CALENDAR_TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(CALENDAR_TOKEN_FILE), CALENDAR_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
            CALENDAR_TOKEN_FILE.write_text(creds.to_json())
        else:
            print("Need to authenticate for calendar write access...")
            if not CALENDAR_CLIENT_SECRET.exists():
                print(f"ERROR: Client secret not found at {CALENDAR_CLIENT_SECRET}")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CALENDAR_CLIENT_SECRET), CALENDAR_SCOPES
            )
            creds = flow.run_local_server(port=0)
            CALENDAR_TOKEN_FILE.write_text(creds.to_json())
            print("Authentication successful!")

    return creds


def add_event(service, calendar_id, summary, start_datetime, end_datetime, description=None, location=None):
    """Add a single event to the calendar."""
    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'America/New_York',
        },
    }

    if description:
        event['description'] = description
    if location:
        event['location'] = location

    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return created_event


def main():
    print("=" * 70)
    print("Add BLE 26-01 Teaching Events to Calendar")
    print("=" * 70)
    print()

    creds = get_credentials()
    if not creds:
        return

    service = build('calendar', 'v3', credentials=creds)

    # Use primary calendar (jeff@jlotterlaw.com)
    calendar_id = 'jeff@jlotterlaw.com'

    # BLE 26-01 Teaching Events for Jeff Lotter
    events_to_add = [
        {
            'summary': 'BLE 26-01 Teaching: Classification of Offenses / Understanding Statutes',
            'start': '2026-01-22T06:00:00',
            'end': '2026-01-22T10:00:00',
            'description': 'Legal - Intro to Law - Classification of Offenses / Understanding Statutes\nCourse: CJK 0018\nPages: 64-69',
            'location': 'Valencia College Criminal Justice Institute'
        },
        {
            'summary': 'BLE 26-01 Teaching: Categories of Criminal Intent',
            'start': '2026-01-22T11:00:00',
            'end': '2026-01-22T14:00:00',
            'description': 'Legal - Legal Concepts - Categories of Criminal Intent\nCourse: CJK 0018\nPages: 70-73',
            'location': 'Valencia College Criminal Justice Institute'
        },
        {
            'summary': 'BLE 26-01 Teaching: Standards of Legal Justification (AM)',
            'start': '2026-01-23T06:00:00',
            'end': '2026-01-23T10:00:00',
            'description': 'Legal - Legal Concepts - Standards of Legal Justification\nCourse: CJK 0018\nPages: 74-81',
            'location': 'Valencia College Criminal Justice Institute'
        },
        {
            'summary': 'BLE 26-01 Teaching: Standards of Legal Justification (PM)',
            'start': '2026-01-23T11:00:00',
            'end': '2026-01-23T14:00:00',
            'description': 'Legal - Legal Concepts - Standards of Legal Justification\nCourse: CJK 0018\nPages: 74-81',
            'location': 'Valencia College Criminal Justice Institute'
        },
        {
            'summary': 'BLE 26-01 Teaching: Search & Seizure (AM)',
            'start': '2026-01-26T06:00:00',
            'end': '2026-01-26T10:00:00',
            'description': 'Legal - Legal Concepts - Search & Seizure\nCourse: CJK 0018\nPages: 82-90',
            'location': 'Valencia College Criminal Justice Institute'
        },
        {
            'summary': 'BLE 26-01 Teaching: Search & Seizure (PM)',
            'start': '2026-01-26T11:00:00',
            'end': '2026-01-26T14:00:00',
            'description': 'Legal - Legal Concepts - Search & Seizure\nCourse: CJK 0018\nPages: 82-90',
            'location': 'Valencia College Criminal Justice Institute'
        },
    ]

    print(f"Adding {len(events_to_add)} events to calendar: {calendar_id}")
    print()

    for event_data in events_to_add:
        try:
            created = add_event(
                service,
                calendar_id,
                event_data['summary'],
                event_data['start'],
                event_data['end'],
                event_data.get('description'),
                event_data.get('location')
            )
            print(f"  [OK] {event_data['summary']}")
            print(f"       {event_data['start'][:10]} {event_data['start'][11:16]}-{event_data['end'][11:16]}")
        except Exception as e:
            print(f"  [ERROR] {event_data['summary']}: {e}")

    print()
    print("Done!")


if __name__ == "__main__":
    main()
