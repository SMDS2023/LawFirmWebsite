#!/usr/bin/env python3
"""
List available Google Calendars.

Run this to see which calendar IDs to add to calendar_config.json
"""

import json
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent
CONFIG_DIR = Path(__file__).parent / "config"
CALENDAR_CLIENT_SECRET = BASE_DIR / "LotterLaw" / "Admin" / "Calendar" / "client_secret_1095806145319-lkef8fm7b3gdks3rshn44ne6h5v1idh8.apps.googleusercontent.com.json"
CALENDAR_TOKEN_FILE = CONFIG_DIR / "calendar_token.json"
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    print("=" * 60)
    print("Google Calendar - List Available Calendars")
    print("=" * 60)
    print()

    # Load credentials
    creds = None
    if CALENDAR_TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(CALENDAR_TOKEN_FILE), CALENDAR_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CALENDAR_CLIENT_SECRET), CALENDAR_SCOPES
            )
            creds = flow.run_local_server(port=0)
        CALENDAR_TOKEN_FILE.write_text(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # List all calendars
    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get('items', [])

    print(f"Found {len(calendars)} calendars:\n")
    print("-" * 60)

    for cal in calendars:
        cal_id = cal.get('id', '')
        summary = cal.get('summary', 'Untitled')
        primary = cal.get('primary', False)
        access_role = cal.get('accessRole', '')

        print(f"  Name: {summary}")
        print(f"  ID:   {cal_id}")
        print(f"  Role: {access_role}")
        if primary:
            print(f"  [PRIMARY CALENDAR]")
        print("-" * 60)

    print()
    print("To scan specific calendars, edit:")
    print(f"  {CONFIG_DIR / 'calendar_config.json'}")
    print()
    print("Add the calendar IDs to the 'calendar_ids' array.")


if __name__ == "__main__":
    main()
