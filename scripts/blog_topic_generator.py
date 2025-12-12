#!/usr/bin/env python3
"""
Blog Topic Generator - Daily Run

Scans Google Calendar and case files to generate blog post topic suggestions.

Usage:
    python blog_topic_generator.py [--days 30] [--output-dir ./output/blog_suggestions]

Output:
    Creates blog_suggestions_YYYY-MM-DD.md with ranked topic suggestions.
"""

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Try to import optional dependencies
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False
    print("Warning: PyPDF2 not installed. PDF scanning disabled. Run: pip install PyPDF2")

try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False
    print("Warning: python-docx not installed. DOCX scanning disabled. Run: pip install python-docx")

# Google Calendar API imports
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    HAS_GOOGLE_API = True
except ImportError:
    HAS_GOOGLE_API = False
    print("Warning: Google API client not installed. Calendar scanning disabled.")
    print("  Run: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Documents folder
WEBSITE_DIR = Path(__file__).parent.parent  # Website folder
CONFIG_DIR = Path(__file__).parent / "config"

# Google API configuration
# OAuth credentials from LotterLaw/Admin/Calendar
GOOGLE_CLIENT_SECRET = BASE_DIR / "LotterLaw" / "Admin" / "Calendar" / "client_secret_1095806145319-lkef8fm7b3gdks3rshn44ne6h5v1idh8.apps.googleusercontent.com.json"
GOOGLE_TOKEN_FILE = CONFIG_DIR / "google_token.json"
CALENDAR_CONFIG_FILE = CONFIG_DIR / "calendar_config.json"

# Scopes for Google APIs (all read-only)
# Note: Keep requires Workspace enterprise, Chat requires Chat app config - not included
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
]

# Privacy/Disclosure settings - WHAT GETS SHOWN IN OUTPUT
DISCLOSURE_SETTINGS = {
    "show_client_names": False,      # NEVER show client names
    "show_case_numbers": False,      # Don't show case numbers
    "show_specific_dates": False,    # Show month/year only, not exact dates
    "show_email_subjects": False,    # Show keyword match only, not full subject
    "show_file_names": True,         # Show file names (usually don't have client names)
    "max_preview_length": 50,        # Truncate any text preview
}

# Case file locations to scan
CASE_FILE_LOCATIONS = [
    BASE_DIR / "LotterLaw" / "Active-Cases",
    BASE_DIR / "LotterLaw" / "Case-Management",
    BASE_DIR / "LotterLaw" / "Blog",  # Existing blog content for reference
]

# Existing blog posts location (to avoid duplicates)
EXISTING_BLOGS_DIR = WEBSITE_DIR / "blog"

# Keywords to extract
CASE_TYPE_KEYWORDS = [
    "DUI", "DWLS", "DWLSR", "suspended license", "traffic", "felony", "misdemeanor",
    "domestic violence", "battery", "assault", "theft", "burglary", "drug",
    "possession", "cannabis", "marijuana", "cocaine", "fleeing", "eluding",
    "hit and run", "leaving scene", "reckless driving", "speeding",
    "red light", "toll", "weapons", "firearm", "concealed carry",
    "expunge", "seal", "probation", "violation"
]

OUTCOME_KEYWORDS = [
    "dismissed", "nolle prosequi", "not guilty", "acquitted", "reduced",
    "withheld adjudication", "adjudication withheld", "diversion",
    "plea", "guilty", "convicted", "sentence", "probation"
]

# Keywords that are outcomes/programs, not charges (exclude from charge topics)
NON_CHARGE_KEYWORDS = ["PTI", "diversion", "plea", "probation", "sentence", "pre-trial"]

STAGE_KEYWORDS = [
    "arraignment", "trial", "hearing", "deposition", "motion",
    "pre-trial", "sentencing", "appeal", "review"
]

# Florida Statute patterns
STATUTE_PATTERN = re.compile(r'(?:F\.?S\.?|Florida Statute[s]?|§)\s*(\d{3}\.\d{2,4})', re.IGNORECASE)
STATUTE_PATTERN_ALT = re.compile(r'\b(\d{3}\.\d{2,4})\b')

# Common statute mappings
STATUTE_TO_TOPIC = {
    "316.193": "DUI",
    "322.34": "DWLS (Driving While License Suspended)",
    "322.03": "No Valid Driver's License",
    "316.027": "Leaving Scene of Accident (Hit and Run)",
    "316.1935": "Fleeing or Eluding",
    "893.13": "Drug Possession",
    "790.01": "Carrying Concealed Weapon",
    "810.02": "Burglary",
    "812.014": "Theft",
    "784.03": "Battery",
    "741.28": "Domestic Violence",
    "316.183": "Speeding",
    "316.074": "Red Light Violation",
}

# Blog topic templates
TOPIC_TEMPLATES = [
    "What Happens If You Get a {charge} Charge in Florida?",
    "Case Dismissed: {charge} Defense Strategy That Worked",
    "Understanding {statute} Charges in Orlando",
    "{outcome} for {charge}: What It Means for Your Case",
    "How to Beat a {charge} Charge in Orange County",
    "{charge} Penalties in Florida: What You Need to Know",
    "Common Defenses for {charge} Cases",
    "Real Case: {outcome} in {charge} Case",
]


class BlogTopicGenerator:
    """Generate blog topic suggestions from calendar and case files."""

    def __init__(self, days_back: int = 30, output_dir: Optional[Path] = None):
        self.days_back = days_back
        self.output_dir = output_dir or WEBSITE_DIR / "output" / "blog_suggestions"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.extracted_data = {
            "calendar_events": [],
            "case_files": [],
            "gmail_threads": [],
            "drive_files": [],
            "chat_messages": [],
            "keep_notes": [],
            "keywords": Counter(),
            "statutes": Counter(),
            "outcomes": Counter(),
        }
        self.google_creds = None  # Shared credentials for all Google APIs
        self.existing_blog_topics = self._load_existing_blogs()

    def _get_google_credentials(self):
        """Get or refresh Google API credentials (shared across Calendar, Gmail, Drive)."""
        if not HAS_GOOGLE_API:
            return None

        if not GOOGLE_CLIENT_SECRET.exists():
            print("  No OAuth client secret found")
            print(f"  Expected: {GOOGLE_CLIENT_SECRET}")
            return None

        # Return cached credentials if valid
        if self.google_creds and self.google_creds.valid:
            return self.google_creds

        creds = None

        # Check for existing token
        if GOOGLE_TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(str(GOOGLE_TOKEN_FILE), GOOGLE_SCOPES)

        # If no valid credentials, run OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print("  Opening browser for Google authorization...")
                print("  (Calendar + Gmail + Drive read-only access)")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(GOOGLE_CLIENT_SECRET), GOOGLE_SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for next run
            GOOGLE_TOKEN_FILE.write_text(creds.to_json())
            print(f"  Token saved to: {GOOGLE_TOKEN_FILE}")

        self.google_creds = creds
        return creds

    def _load_existing_blogs(self) -> List[str]:
        """Load existing blog post titles to avoid duplicates."""
        titles = []
        if EXISTING_BLOGS_DIR.exists():
            for f in EXISTING_BLOGS_DIR.glob("*.html"):
                # Extract title from filename
                name = f.stem
                # Remove number prefix (e.g., "01-" or "19-")
                if re.match(r'^\d+-', name):
                    name = re.sub(r'^\d+-', '', name)
                titles.append(name.lower().replace('-', ' '))
        return titles

    def scan_calendar(self) -> List[Dict]:
        """
        Scan Google Calendar for review entries and case-related events.

        Returns list of events with extracted keywords.
        """
        creds = self._get_google_credentials()
        if not creds:
            print("Calendar scanning: No valid credentials")
            return []

        # Load calendar config
        calendar_config = {"calendar_ids": ["primary"], "keywords_to_scan": []}
        if CALENDAR_CONFIG_FILE.exists():
            try:
                calendar_config = json.loads(CALENDAR_CONFIG_FILE.read_text())
            except Exception as e:
                print(f"  Warning: Could not load calendar config: {e}")

        results = []

        try:
            service = build('calendar', 'v3', credentials=creds)

            # Calculate time range
            now = datetime.now(timezone.utc)
            time_min = (now - timedelta(days=self.days_back)).isoformat().replace('+00:00', 'Z')
            time_max = now.isoformat().replace('+00:00', 'Z')

            # Scan each configured calendar
            for calendar_id in calendar_config.get("calendar_ids", ["primary"]):
                print(f"  Scanning calendar: {calendar_id}")

                try:
                    events_result = service.events().list(
                        calendarId=calendar_id,
                        timeMin=time_min,
                        timeMax=time_max,
                        maxResults=100,
                        singleEvents=True,
                        orderBy='startTime'
                    ).execute()

                    events = events_result.get('items', [])
                    print(f"    Found {len(events)} events")

                    for event in events:
                        title = event.get('summary', '')
                        description = event.get('description', '')
                        start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', ''))

                        # Combine title and description for keyword extraction
                        full_text = f"{title} {description}"

                        # Extract keywords
                        keywords = self._extract_keywords(full_text)
                        statutes = self._extract_statutes(full_text)

                        if keywords or statutes:
                            results.append({
                                "source": "calendar",
                                "title": title,
                                "date": start,
                                "calendar_id": calendar_id,
                                "keywords": keywords,
                                "statutes": statutes,
                                "text_preview": full_text[:200],
                            })

                            # Update global counters
                            for kw in keywords:
                                self.extracted_data["keywords"][kw] += 1
                            for st in statutes:
                                self.extracted_data["statutes"][st] += 1

                except HttpError as e:
                    print(f"    Error accessing calendar {calendar_id}: {e}")

        except Exception as e:
            print(f"  Calendar API error: {e}")
            print("  If this is your first run, a browser window should open for authorization.")

        print(f"  Total calendar events with keywords: {len(results)}")
        return results

    def scan_case_files(self) -> List[Dict]:
        """Scan case file directories for content."""
        results = []

        for location in CASE_FILE_LOCATIONS:
            if not location.exists():
                print(f"  Skipping (not found): {location}")
                continue

            print(f"  Scanning: {location}")
            file_count = 0

            for filepath in location.rglob("*"):
                if filepath.is_file():
                    text = self._extract_text(filepath)
                    if text:
                        file_count += 1
                        keywords = self._extract_keywords(text)
                        statutes = self._extract_statutes(text)

                        if keywords or statutes:
                            results.append({
                                "source": "case_file",
                                "path": str(filepath),
                                "filename": filepath.name,
                                "modified": datetime.fromtimestamp(filepath.stat().st_mtime),
                                "keywords": keywords,
                                "statutes": statutes,
                                "text_preview": text[:500] if text else "",
                            })

                            # Update global counters
                            for kw in keywords:
                                self.extracted_data["keywords"][kw] += 1
                            for st in statutes:
                                self.extracted_data["statutes"][st] += 1

            print(f"    Found {file_count} files with content")

        return results

    def _anonymize_text(self, text: str, for_output: bool = False) -> str:
        """
        Remove identifying information from text for privacy.

        Args:
            text: Raw text to anonymize
            for_output: If True, apply stricter rules for report output
        """
        if not text:
            return ""

        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

        # Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', text)

        # Remove case numbers (e.g., 2025-CT-123456, 2024-CF-789012)
        if not DISCLOSURE_SETTINGS.get("show_case_numbers", False):
            text = re.sub(r'\b\d{4}-[A-Z]{2,3}-\d+\b', '[CASE]', text)

        # Remove potential names (capitalized words that aren't keywords)
        if not DISCLOSURE_SETTINGS.get("show_client_names", False):
            # Common name patterns: "John Smith", "Smith, John", "v. Smith"
            # Keep legal keywords capitalized
            legal_terms = {'DUI', 'DWLS', 'DWLSR', 'PTC', 'MTW', 'DV', 'VOP', 'PTI',
                          'Court', 'Trial', 'Hearing', 'Motion', 'Plea', 'State',
                          'Florida', 'Orange', 'County', 'Orlando'}

            # Remove "v. Name" patterns
            text = re.sub(r'\bv\.\s+[A-Z][a-z]+', 'v. [CLIENT]', text)

            # Remove "Name - " at start (calendar format)
            text = re.sub(r'^[A-Z][a-z]+\s+[A-Z][a-z]+\s*[-–]', '[CLIENT] -', text)

            # Remove names after common prefixes
            text = re.sub(r'(Consult|Client|Meeting|Call)\s*[-–:]\s*[A-Z][a-z]+\s*[A-Z]?[a-z]*',
                         r'\1 - [CLIENT]', text, flags=re.IGNORECASE)

        # For output, apply additional restrictions
        if for_output:
            # Truncate to max length
            max_len = DISCLOSURE_SETTINGS.get("max_preview_length", 50)
            if len(text) > max_len:
                text = text[:max_len] + "..."

        return text.strip()

    def _format_date_for_output(self, date_str: str) -> str:
        """Format date according to disclosure settings."""
        if not date_str:
            return ""

        if DISCLOSURE_SETTINGS.get("show_specific_dates", True):
            return date_str[:10]  # YYYY-MM-DD
        else:
            # Show only month/year
            try:
                if len(date_str) >= 7:
                    return date_str[:7]  # YYYY-MM
            except:
                pass
            return date_str[:7] if len(date_str) >= 7 else date_str

    def scan_gmail(self) -> List[Dict]:
        """
        Scan Gmail for case-related emails.

        Returns list of email threads with extracted keywords (anonymized).
        """
        creds = self._get_google_credentials()
        if not creds:
            print("Gmail scanning: No valid credentials")
            return []

        results = []

        try:
            service = build('gmail', 'v1', credentials=creds)

            # Calculate date range for query
            after_date = (datetime.now() - timedelta(days=self.days_back)).strftime('%Y/%m/%d')

            # Search for case-related emails
            search_queries = [
                f"after:{after_date} (DUI OR DWLS OR traffic OR criminal OR court OR hearing)",
                f"after:{after_date} (dismissed OR reduced OR plea OR trial)",
                f"after:{after_date} subject:(case OR client OR court)",
            ]

            seen_thread_ids = set()

            for query in search_queries:
                try:
                    response = service.users().messages().list(
                        userId='me',
                        q=query,
                        maxResults=50
                    ).execute()

                    messages = response.get('messages', [])

                    for msg_info in messages:
                        thread_id = msg_info.get('threadId', '')
                        if thread_id in seen_thread_ids:
                            continue
                        seen_thread_ids.add(thread_id)

                        # Get message details
                        msg = service.users().messages().get(
                            userId='me',
                            id=msg_info['id'],
                            format='metadata',
                            metadataHeaders=['Subject', 'Date']
                        ).execute()

                        headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
                        subject = headers.get('Subject', '')
                        date = headers.get('Date', '')[:16]  # Truncate date

                        # Extract keywords from subject (anonymize)
                        anon_subject = self._anonymize_text(subject)
                        keywords = self._extract_keywords(anon_subject)
                        statutes = self._extract_statutes(anon_subject)

                        if keywords or statutes:
                            results.append({
                                "source": "gmail",
                                "subject": anon_subject[:100],  # Truncate for privacy
                                "date": date,
                                "thread_id": thread_id,
                                "keywords": keywords,
                                "statutes": statutes,
                            })

                            # Update global counters
                            for kw in keywords:
                                self.extracted_data["keywords"][kw] += 1
                            for st in statutes:
                                self.extracted_data["statutes"][st] += 1

                except HttpError as e:
                    if e.resp.status == 403:
                        print(f"    Gmail API not enabled or no permission")
                        break
                    print(f"    Gmail search error: {e}")

            print(f"  Total email threads with keywords: {len(results)}")

        except Exception as e:
            print(f"  Gmail API error: {e}")

        return results

    def scan_drive(self) -> List[Dict]:
        """
        Scan Google Drive for case-related documents.

        Returns list of files with extracted keywords (names anonymized).
        """
        creds = self._get_google_credentials()
        if not creds:
            print("Drive scanning: No valid credentials")
            return []

        results = []

        try:
            service = build('drive', 'v3', credentials=creds)

            # Calculate date range
            after_date = (datetime.now() - timedelta(days=self.days_back)).strftime('%Y-%m-%dT00:00:00')

            # Search for case-related files
            search_queries = [
                f"modifiedTime > '{after_date}' and (name contains 'DUI' or name contains 'case' or name contains 'motion')",
                f"modifiedTime > '{after_date}' and (name contains 'traffic' or name contains 'criminal')",
                f"modifiedTime > '{after_date}' and (fullText contains 'dismissed' or fullText contains 'court')",
            ]

            seen_file_ids = set()

            for query in search_queries:
                try:
                    response = service.files().list(
                        q=query,
                        spaces='drive',
                        fields='files(id, name, modifiedTime, mimeType)',
                        pageSize=50
                    ).execute()

                    files = response.get('files', [])

                    for file in files:
                        file_id = file.get('id', '')
                        if file_id in seen_file_ids:
                            continue
                        seen_file_ids.add(file_id)

                        name = file.get('name', '')
                        modified = file.get('modifiedTime', '')[:10]
                        mime_type = file.get('mimeType', '')

                        # Anonymize filename (remove potential client names)
                        anon_name = self._anonymize_text(name)

                        # Extract keywords from filename
                        keywords = self._extract_keywords(anon_name)
                        statutes = self._extract_statutes(anon_name)

                        if keywords or statutes:
                            results.append({
                                "source": "drive",
                                "filename": anon_name,
                                "modified": modified,
                                "file_id": file_id,
                                "mime_type": mime_type,
                                "keywords": keywords,
                                "statutes": statutes,
                            })

                            # Update global counters
                            for kw in keywords:
                                self.extracted_data["keywords"][kw] += 1
                            for st in statutes:
                                self.extracted_data["statutes"][st] += 1

                except HttpError as e:
                    if e.resp.status == 403:
                        print(f"    Drive API not enabled or no permission")
                        break
                    print(f"    Drive search error: {e}")

            print(f"  Total Drive files with keywords: {len(results)}")

        except Exception as e:
            print(f"  Drive API error: {e}")

        return results

    def scan_chat(self) -> List[Dict]:
        """
        Scan Google Chat for case-related messages.

        Returns list of chat messages with extracted keywords (anonymized).
        """
        creds = self._get_google_credentials()
        if not creds:
            print("Chat scanning: No valid credentials")
            return []

        results = []

        try:
            service = build('chat', 'v1', credentials=creds)

            # List spaces the user is a member of
            spaces_response = service.spaces().list(pageSize=50).execute()
            spaces = spaces_response.get('spaces', [])

            for space in spaces:
                space_name = space.get('name', '')
                space_display = space.get('displayName', 'Unknown Space')

                try:
                    # Get recent messages from this space
                    messages_response = service.spaces().messages().list(
                        parent=space_name,
                        pageSize=100,
                        orderBy='createTime desc'
                    ).execute()

                    messages = messages_response.get('messages', [])

                    for msg in messages:
                        text = msg.get('text', '')
                        create_time = msg.get('createTime', '')[:10]

                        # Anonymize and extract keywords
                        anon_text = self._anonymize_text(text)
                        keywords = self._extract_keywords(anon_text)
                        statutes = self._extract_statutes(anon_text)

                        if keywords or statutes:
                            results.append({
                                "source": "chat",
                                "space": space_display,
                                "date": create_time,
                                "keywords": keywords,
                                "statutes": statutes,
                                "preview": anon_text[:100] if anon_text else "",
                            })

                            for kw in keywords:
                                self.extracted_data["keywords"][kw] += 1
                            for st in statutes:
                                self.extracted_data["statutes"][st] += 1

                except HttpError as e:
                    if e.resp.status == 403:
                        print(f"    Chat API not enabled or no permission")
                        break
                    # Skip spaces we can't access

            print(f"  Total Chat messages with keywords: {len(results)}")

        except Exception as e:
            print(f"  Chat API error: {e}")

        return results

    def scan_keep(self) -> List[Dict]:
        """
        Scan Google Keep for case-related notes.

        Returns list of notes with extracted keywords (anonymized).
        """
        creds = self._get_google_credentials()
        if not creds:
            print("Keep scanning: No valid credentials")
            return []

        results = []

        try:
            service = build('keep', 'v1', credentials=creds)

            # List notes
            notes_response = service.notes().list(pageSize=100).execute()
            notes = notes_response.get('notes', [])

            for note in notes:
                title = note.get('title', '')
                body = note.get('body', {}).get('text', {}).get('text', '')
                update_time = note.get('updateTime', '')[:10]

                # Combine title and body for keyword extraction
                full_text = f"{title} {body}"
                anon_text = self._anonymize_text(full_text)
                keywords = self._extract_keywords(anon_text)
                statutes = self._extract_statutes(anon_text)

                if keywords or statutes:
                    results.append({
                        "source": "keep",
                        "title": self._anonymize_text(title, for_output=True),
                        "date": update_time,
                        "keywords": keywords,
                        "statutes": statutes,
                    })

                    for kw in keywords:
                        self.extracted_data["keywords"][kw] += 1
                    for st in statutes:
                        self.extracted_data["statutes"][st] += 1

            print(f"  Total Keep notes with keywords: {len(results)}")

        except Exception as e:
            if "not enabled" in str(e).lower() or "403" in str(e):
                print(f"    Keep API not enabled or no permission")
            else:
                print(f"  Keep API error: {e}")

        return results

    def _extract_text(self, filepath: Path) -> Optional[str]:
        """Extract text from various file types."""
        suffix = filepath.suffix.lower()

        try:
            if suffix == ".txt" or suffix == ".md":
                return filepath.read_text(encoding="utf-8", errors="ignore")

            elif suffix == ".pdf" and HAS_PYPDF2:
                text = ""
                with open(filepath, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages[:10]:  # Limit to first 10 pages
                        text += page.extract_text() or ""
                return text

            elif suffix == ".docx" and HAS_DOCX:
                doc = Document(filepath)
                return "\n".join([para.text for para in doc.paragraphs])

            elif suffix == ".html":
                # Simple HTML text extraction
                content = filepath.read_text(encoding="utf-8", errors="ignore")
                # Strip HTML tags
                text = re.sub(r'<[^>]+>', ' ', content)
                return text

        except Exception as e:
            # Silently skip files that can't be read
            pass

        return None

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract case-related keywords from text."""
        text_lower = text.lower()
        found = []

        for kw in CASE_TYPE_KEYWORDS:
            if kw.lower() in text_lower:
                found.append(kw)

        for kw in OUTCOME_KEYWORDS:
            if kw.lower() in text_lower:
                found.append(kw)
                self.extracted_data["outcomes"][kw] += 1

        return list(set(found))

    def _extract_statutes(self, text: str) -> List[str]:
        """Extract Florida Statute numbers from text."""
        statutes = set()

        # Try primary pattern (F.S. 316.193)
        for match in STATUTE_PATTERN.finditer(text):
            statutes.add(match.group(1))

        # Try alternate pattern (just numbers like 316.193)
        for match in STATUTE_PATTERN_ALT.finditer(text):
            num = match.group(1)
            # Validate it looks like a real statute
            if num in STATUTE_TO_TOPIC:
                statutes.add(num)

        return list(statutes)

    def _find_sources_for_keyword(self, keyword: str) -> Dict:
        """Find all sources (calendar, gmail, drive, chat, keep, case files) mentioning a keyword."""
        sources = {
            "calendar_events": [],
            "case_files": [],
            "gmail_threads": [],
            "drive_files": [],
            "chat_messages": [],
            "keep_notes": [],
            "outcomes": [],
            "statutes": []
        }

        keyword_lower = keyword.lower()

        # Search calendar events
        for event in self.extracted_data.get("calendar_events", []):
            if keyword_lower in [k.lower() for k in event.get("keywords", [])]:
                sources["calendar_events"].append({
                    "title": event.get("title", ""),
                    "date": event.get("date", "")[:10] if event.get("date") else "",
                })
                # Collect outcomes and statutes from this event
                for outcome in event.get("keywords", []):
                    if outcome.lower() in [o.lower() for o in OUTCOME_KEYWORDS]:
                        sources["outcomes"].append(outcome)
                sources["statutes"].extend(event.get("statutes", []))

        # Search Gmail threads
        for thread in self.extracted_data.get("gmail_threads", []):
            if keyword_lower in [k.lower() for k in thread.get("keywords", [])]:
                sources["gmail_threads"].append({
                    "subject": thread.get("subject", ""),
                    "date": thread.get("date", ""),
                })
                for outcome in thread.get("keywords", []):
                    if outcome.lower() in [o.lower() for o in OUTCOME_KEYWORDS]:
                        sources["outcomes"].append(outcome)
                sources["statutes"].extend(thread.get("statutes", []))

        # Search Drive files
        for file in self.extracted_data.get("drive_files", []):
            if keyword_lower in [k.lower() for k in file.get("keywords", [])]:
                sources["drive_files"].append({
                    "filename": file.get("filename", ""),
                    "modified": file.get("modified", ""),
                })
                for outcome in file.get("keywords", []):
                    if outcome.lower() in [o.lower() for o in OUTCOME_KEYWORDS]:
                        sources["outcomes"].append(outcome)
                sources["statutes"].extend(file.get("statutes", []))

        # Search Chat messages
        for msg in self.extracted_data.get("chat_messages", []):
            if keyword_lower in [k.lower() for k in msg.get("keywords", [])]:
                sources["chat_messages"].append({
                    "space": msg.get("space", ""),
                    "date": msg.get("date", ""),
                })
                for outcome in msg.get("keywords", []):
                    if outcome.lower() in [o.lower() for o in OUTCOME_KEYWORDS]:
                        sources["outcomes"].append(outcome)
                sources["statutes"].extend(msg.get("statutes", []))

        # Search Keep notes
        for note in self.extracted_data.get("keep_notes", []):
            if keyword_lower in [k.lower() for k in note.get("keywords", [])]:
                sources["keep_notes"].append({
                    "title": note.get("title", ""),
                    "date": note.get("date", ""),
                })
                for outcome in note.get("keywords", []):
                    if outcome.lower() in [o.lower() for o in OUTCOME_KEYWORDS]:
                        sources["outcomes"].append(outcome)
                sources["statutes"].extend(note.get("statutes", []))

        # Search local case files
        for case in self.extracted_data.get("case_files", []):
            if keyword_lower in [k.lower() for k in case.get("keywords", [])]:
                sources["case_files"].append({
                    "filename": case.get("filename", ""),
                    "path": case.get("path", ""),
                    "modified": case.get("modified").strftime("%Y-%m-%d") if case.get("modified") else "",
                })
                # Collect outcomes and statutes from this file
                for outcome in case.get("keywords", []):
                    if outcome.lower() in [o.lower() for o in OUTCOME_KEYWORDS]:
                        sources["outcomes"].append(outcome)
                sources["statutes"].extend(case.get("statutes", []))

        # Deduplicate
        sources["outcomes"] = list(set(sources["outcomes"]))
        sources["statutes"] = list(set(sources["statutes"]))

        return sources

    def generate_topics(self) -> List[Dict]:
        """Generate ranked topic suggestions with source details."""
        topics = []
        seen_keywords = set()

        # Get most common keywords and statutes
        top_keywords = self.extracted_data["keywords"].most_common(20)
        top_statutes = self.extracted_data["statutes"].most_common(10)
        top_outcomes = self.extracted_data["outcomes"].most_common(5)

        # Generate topics from keywords - one per keyword with full source details
        for keyword, count in top_keywords:
            # Skip non-charge keywords (outcomes/programs)
            if keyword.upper() in [k.upper() for k in NON_CHARGE_KEYWORDS]:
                continue

            if keyword.lower() in seen_keywords:
                continue
            seen_keywords.add(keyword.lower())

            if count >= 1:
                # Title case the keyword for display
                display_keyword = keyword.upper() if keyword.upper() in ["DUI", "DWLS", "DWLSR"] else keyword.title()

                # Find all sources for this keyword
                sources = self._find_sources_for_keyword(keyword)

                # Determine best title based on outcomes found
                if "dismissed" in [o.lower() for o in sources["outcomes"]]:
                    title = f"Case Dismissed: {display_keyword} Defense Strategy That Worked"
                elif "reduced" in [o.lower() for o in sources["outcomes"]]:
                    title = f"Charge Reduced: How We Won a {display_keyword} Case"
                elif "not guilty" in [o.lower() for o in sources["outcomes"]]:
                    title = f"Not Guilty: Winning a {display_keyword} Trial in Orlando"
                else:
                    title = f"What Happens If You Get a {display_keyword} Charge in Florida?"

                # Check if similar topic already exists
                if not self._is_duplicate(title):
                    # Calculate score: frequency + source bonuses
                    score = count * 10
                    if sources["calendar_events"]:
                        score += len(sources["calendar_events"]) * 15
                    if sources["gmail_threads"]:
                        score += len(sources["gmail_threads"]) * 12
                    if sources["drive_files"]:
                        score += len(sources["drive_files"]) * 10
                    if sources["chat_messages"]:
                        score += len(sources["chat_messages"]) * 8
                    if sources["keep_notes"]:
                        score += len(sources["keep_notes"]) * 8
                    if sources["outcomes"]:
                        score += len(sources["outcomes"]) * 10

                    topics.append({
                        "title": title,
                        "source_type": "keyword",
                        "keyword": display_keyword,
                        "frequency": count,
                        "score": score,
                        "calendar_events": sources["calendar_events"][:5],
                        "gmail_threads": sources["gmail_threads"][:5],
                        "drive_files": sources["drive_files"][:5],
                        "chat_messages": sources["chat_messages"][:5],
                        "keep_notes": sources["keep_notes"][:5],
                        "case_files": sources["case_files"][:5],
                        "outcomes": sources["outcomes"],
                        "statutes": sources["statutes"],
                    })

        # Generate topics from statutes
        for statute, count in top_statutes:
            if statute in STATUTE_TO_TOPIC:
                topic_name = STATUTE_TO_TOPIC[statute]
                title = f"Understanding Florida Statute {statute}: {topic_name}"

                if not self._is_duplicate(title):
                    topics.append({
                        "title": title,
                        "source_type": "statute",
                        "statute": statute,
                        "frequency": count,
                        "score": count * 15,  # Statutes get higher base score
                    })

        # Generate outcome-based topics
        for outcome, count in top_outcomes:
            if count >= 1:
                # Find most common keyword to pair with
                if top_keywords:
                    keyword = top_keywords[0][0]
                    title = f"Case {outcome.title()}: How We Won a {keyword} Case"

                    if not self._is_duplicate(title):
                        topics.append({
                            "title": title,
                            "source_type": "outcome",
                            "outcome": outcome,
                            "keyword": keyword,
                            "frequency": count,
                            "score": count * 20,  # Outcomes are high value
                        })

        # Sort by score descending
        topics.sort(key=lambda x: x["score"], reverse=True)

        return topics[:10]  # Return top 10

    def _is_duplicate(self, title: str) -> bool:
        """Check if topic is similar to existing blog posts."""
        title_words = set(title.lower().split())

        for existing in self.existing_blog_topics:
            existing_words = set(existing.split())
            # If more than 50% overlap, consider duplicate
            overlap = len(title_words & existing_words)
            if overlap > len(title_words) * 0.5:
                return True

        return False

    def generate_report(self, topics: List[Dict]) -> str:
        """Generate markdown report with privacy-compliant output."""
        today = datetime.now().strftime("%Y-%m-%d")

        cal_count = len(self.extracted_data.get('calendar_events', []))
        file_count = len(self.extracted_data.get('case_files', []))
        gmail_count = len(self.extracted_data.get('gmail_threads', []))
        drive_count = len(self.extracted_data.get('drive_files', []))
        chat_count = len(self.extracted_data.get('chat_messages', []))
        keep_count = len(self.extracted_data.get('keep_notes', []))

        lines = [
            f"# Blog Topic Suggestions - {today}",
            "",
            "⚠️ **CONFIDENTIALITY NOTICE**: This document contains topic suggestions only.",
            "All client names, case numbers, and identifying information have been removed.",
            "Sources shown are for internal reference only - do not include in published content.",
            "",
            "---",
            "",
            "## Sources Scanned",
            "",
            f"| Source | Items with Keywords |",
            f"|--------|---------------------|",
            f"| 📅 Calendar | {cal_count} |",
            f"| 📧 Gmail | {gmail_count} |",
            f"| 📁 Drive | {drive_count} |",
            f"| 💬 Chat | {chat_count} |",
            f"| 📝 Keep | {keep_count} |",
            f"| 📂 Local Files | {file_count} |",
            f"| **Total Keywords** | {sum(self.extracted_data['keywords'].values())} |",
            f"| **Statutes Found** | {sum(self.extracted_data['statutes'].values())} |",
            "",
            "---",
            "",
            "## Top Recommendations",
            "",
        ]

        for i, topic in enumerate(topics, 1):
            lines.extend([
                f"### {i}. \"{topic['title']}\"",
                "",
                f"**Score:** {topic['score']} | **Mentions:** {topic.get('frequency', 0)}",
                "",
            ])

            if topic.get("keyword"):
                lines.append(f"**Primary Keyword:** {topic['keyword']}")
            if topic.get("statute"):
                lines.append(f"**Statute:** F.S. {topic['statute']}")
            if topic.get("outcomes"):
                lines.append(f"**Outcomes Found:** {', '.join(topic['outcomes'])}")
            if topic.get("statutes"):
                statute_list = [f"F.S. {s}" for s in topic['statutes'][:3]]
                lines.append(f"**Related Statutes:** {', '.join(statute_list)}")

            # Show calendar events (anonymized)
            if topic.get("calendar_events"):
                lines.extend(["", "**📅 Calendar Events:**"])
                for event in topic["calendar_events"][:5]:
                    date_str = self._format_date_for_output(event.get("date", ""))
                    title_str = self._anonymize_text(event.get("title", ""), for_output=True)
                    lines.append(f"- {date_str}: {title_str if title_str else '[event]'}")

            # Show Gmail threads (anonymized - keyword match only)
            if topic.get("gmail_threads"):
                lines.extend(["", "**📧 Gmail Threads:**"])
                for thread in topic["gmail_threads"][:5]:
                    date_str = self._format_date_for_output(thread.get("date", ""))
                    # Don't show subject if disclosure settings say no
                    if DISCLOSURE_SETTINGS.get("show_email_subjects", False):
                        subject = self._anonymize_text(thread.get("subject", ""), for_output=True)
                        lines.append(f"- {date_str}: {subject}")
                    else:
                        lines.append(f"- {date_str}: [email thread matched keyword]")

            # Show Drive files
            if topic.get("drive_files"):
                lines.extend(["", "**📁 Drive Files:**"])
                for file in topic["drive_files"][:5]:
                    filename = self._anonymize_text(file.get("filename", ""), for_output=True)
                    modified = self._format_date_for_output(file.get("modified", ""))
                    lines.append(f"- {filename} ({modified})")

            # Show Chat messages
            if topic.get("chat_messages"):
                lines.extend(["", "**💬 Chat Messages:**"])
                for msg in topic["chat_messages"][:5]:
                    space = msg.get("space", "")
                    date = self._format_date_for_output(msg.get("date", ""))
                    lines.append(f"- {date}: [message in {space}]")

            # Show Keep notes
            if topic.get("keep_notes"):
                lines.extend(["", "**📝 Keep Notes:**"])
                for note in topic["keep_notes"][:5]:
                    title = self._anonymize_text(note.get("title", ""), for_output=True)
                    date = self._format_date_for_output(note.get("date", ""))
                    lines.append(f"- {date}: {title if title else '[untitled note]'}")

            # Show local case files
            if topic.get("case_files"):
                lines.extend(["", "**📂 Local Case Files:**"])
                for case in topic["case_files"][:5]:
                    filename = case.get("filename", "")
                    modified = case.get("modified", "")
                    lines.append(f"- {filename} ({modified})")

            # Suggested angles based on what we found
            lines.extend(["", "**Suggested Angles:**"])
            if topic.get("outcomes"):
                if "dismissed" in [o.lower() for o in topic.get("outcomes", [])]:
                    lines.append("- How the case was dismissed and what strategy worked")
                if "reduced" in [o.lower() for o in topic.get("outcomes", [])]:
                    lines.append("- How charges were reduced and what that means for clients")
            if topic.get("calendar_events"):
                lines.append("- Recent case outcomes to reference (anonymized)")
            if topic.get("statutes"):
                lines.append("- Explain the relevant Florida statutes")
            lines.extend([
                "- What clients facing this charge need to know",
                "- Common defenses and strategies",
                "- Call to action for free consultation",
                "",
                "---",
                "",
            ])

        # Add summary statistics
        lines.extend([
            "## Extraction Summary",
            "",
            "### Top Keywords Found",
            "",
            "| Keyword | Count |",
            "|---------|-------|",
        ])

        for kw, count in self.extracted_data["keywords"].most_common(10):
            lines.append(f"| {kw} | {count} |")

        lines.extend([
            "",
            "### Top Statutes Found",
            "",
            "| Statute | Topic | Count |",
            "|---------|-------|-------|",
        ])

        for st, count in self.extracted_data["statutes"].most_common(10):
            topic = STATUTE_TO_TOPIC.get(st, "Unknown")
            lines.append(f"| F.S. {st} | {topic} | {count} |")

        lines.extend([
            "",
            "---",
            "",
            "*Generated by blog_topic_generator.py*",
        ])

        return "\n".join(lines)

    def run(self) -> Path:
        """Run the full generation pipeline."""
        print("=" * 50)
        print("Blog Topic Generator")
        print("=" * 50)
        print()
        print("[!] Privacy Mode: Client names and case numbers will be anonymized")
        print()

        # Scan Google Calendar
        print("Step 1: Scanning Google Calendar...")
        self.extracted_data["calendar_events"] = self.scan_calendar()
        print()

        # Scan Gmail
        print("Step 2: Scanning Gmail...")
        self.extracted_data["gmail_threads"] = self.scan_gmail()
        print()

        # Scan Google Drive
        print("Step 3: Scanning Google Drive...")
        self.extracted_data["drive_files"] = self.scan_drive()
        print()

        # Google Chat - skipped (requires Chat app configuration)
        print("Step 4: Google Chat... (skipped - requires Chat app config)")
        self.extracted_data["chat_messages"] = []
        print()

        # Google Keep - skipped (requires Workspace enterprise access)
        print("Step 5: Google Keep... (skipped - requires Workspace)")
        self.extracted_data["keep_notes"] = []
        print()

        # Scan local case files
        print("Step 6: Scanning local case files...")
        self.extracted_data["case_files"] = self.scan_case_files()
        print()

        # Generate topics
        print("Step 7: Generating topic suggestions...")
        topics = self.generate_topics()
        print(f"  Generated {len(topics)} topic suggestions")
        print()

        # Generate report
        print("Step 8: Writing report...")
        report = self.generate_report(topics)

        # Save to file
        today = datetime.now().strftime("%Y-%m-%d")
        output_file = self.output_dir / f"blog_suggestions_{today}.md"
        output_file.write_text(report, encoding="utf-8")
        print(f"  Saved to: {output_file}")
        print()

        print("=" * 50)
        print("Complete!")
        print("=" * 50)

        return output_file


def main():
    parser = argparse.ArgumentParser(description="Generate blog topic suggestions")
    parser.add_argument("--days", type=int, default=30, help="Days back to scan")
    parser.add_argument("--output-dir", type=str, help="Output directory for suggestions")
    args = parser.parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else None

    generator = BlogTopicGenerator(days_back=args.days, output_dir=output_dir)
    output_file = generator.run()

    print(f"\nView suggestions: {output_file}")


if __name__ == "__main__":
    main()
