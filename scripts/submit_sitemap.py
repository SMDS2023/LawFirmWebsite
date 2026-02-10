#!/usr/bin/env python3
"""
Submit sitemap to Google Search Console

Requires: google-api-python-client, google-auth-oauthlib, google-auth-httplib2
Install: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
"""

import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes needed (full webmasters access, not readonly)
SCOPES = ['https://www.googleapis.com/auth/webmasters']

# Paths
CONFIG_DIR = Path.home() / '.config' / 'google-auth'
TOKEN_FILE = CONFIG_DIR / 'search_console_token_write.json'
CLIENT_SECRET = CONFIG_DIR / 'client_secret.json'

# Site and sitemap URLs
SITE_URL = 'sc-domain:lotterlaw.com'
SITEMAP_URL = 'https://lotterlaw.com/sitemap.xml'


def get_credentials():
    """Get or create credentials with write access."""
    creds = None

    # Load existing token if available
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'r') as f:
            token_data = json.load(f)

        creds = Credentials(
            token=token_data['token'],
            refresh_token=token_data.get('refresh_token'),
            token_uri=token_data.get('token_uri'),
            client_id=token_data.get('client_id'),
            client_secret=token_data.get('client_secret'),
            scopes=token_data.get('scopes')
        )

    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Need new authorization...")
            print("Opening browser for Google OAuth consent...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        token_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        with open(TOKEN_FILE, 'w') as f:
            json.dump(token_data, f, indent=2)
        print(f"Credentials saved to: {TOKEN_FILE}")

    return creds


def submit_sitemap():
    """Submit sitemap to Google Search Console."""
    print("="*70)
    print("GOOGLE SEARCH CONSOLE - SITEMAP SUBMISSION")
    print("="*70)

    # Get credentials
    creds = get_credentials()

    # Build service
    service = build('searchconsole', 'v1', credentials=creds)

    try:
        # Submit sitemap
        print(f"\nSubmitting sitemap...")
        print(f"  Site: {SITE_URL}")
        print(f"  Sitemap: {SITEMAP_URL}")

        service.sitemaps().submit(
            siteUrl=SITE_URL,
            feedpath=SITEMAP_URL
        ).execute()

        print("\n[SUCCESS] Sitemap submitted successfully!")

        # Get sitemap status
        print("\nFetching sitemap status...")
        response = service.sitemaps().get(
            siteUrl=SITE_URL,
            feedpath=SITEMAP_URL
        ).execute()

        print(f"\nSitemap Status:")
        print(f"  Path: {response.get('path')}")
        print(f"  Last Submitted: {response.get('lastSubmitted', 'N/A')}")
        print(f"  Last Downloaded: {response.get('lastDownloaded', 'N/A')}")
        print(f"  Is Pending: {response.get('isPending', False)}")

        if 'contents' in response:
            for content in response['contents']:
                print(f"\n  Content Type: {content.get('type')}")
                print(f"    Submitted: {content.get('submitted', 0)}")
                print(f"    Indexed: {content.get('indexed', 0)}")

        print("\n" + "="*70)
        print("SUBMISSION COMPLETE")
        print("="*70)
        print("\nGoogle will now:")
        print("  1. Download and parse the sitemap (within hours)")
        print("  2. Queue URLs for crawling (1-2 days)")
        print("  3. Index new pages (1-2 weeks)")
        print("\nCheck status in Search Console:")
        print("  https://search.google.com/search-console")

    except Exception as e:
        print(f"\n[ERROR] Error submitting sitemap: {e}")
        print("\nTroubleshooting:")
        print("  1. Verify you have access to lotterlaw.com in Search Console")
        print("  2. Check that the sitemap URL is accessible")
        print("  3. Ensure OAuth consent screen is configured")
        return False

    return True


if __name__ == '__main__':
    submit_sitemap()
