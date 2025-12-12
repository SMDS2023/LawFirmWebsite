# Google Calendar API Setup Guide

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" dropdown → "New Project"
3. Name it: `LotterLaw-BlogGenerator`
4. Click "Create"

## Step 2: Enable Calendar API

1. In the Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Calendar API"
3. Click on it → Click "Enable"

## Step 3: Create Service Account (Recommended for automation)

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name: `blog-topic-generator`
4. Click "Create and Continue"
5. Skip role assignment (not needed for Calendar read-only)
6. Click "Done"

## Step 4: Generate Key

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON" → Click "Create"
5. Save the downloaded file as:
   ```
   LotterLaw/Website/scripts/config/calendar_credentials.json
   ```

## Step 5: Share Calendar with Service Account

1. Open Google Calendar (calendar.google.com)
2. Find the calendar you want to scan (e.g., "Review" calendar)
3. Click the three dots → "Settings and sharing"
4. Under "Share with specific people", click "Add people"
5. Enter the service account email (looks like: `blog-topic-generator@lotterlaw-bloggenerator.iam.gserviceaccount.com`)
6. Set permission to "See all event details"
7. Click "Send"

## Step 6: Get Calendar ID

1. In Calendar Settings, scroll to "Integrate calendar"
2. Copy the "Calendar ID"
   - For your primary calendar, it's your email address
   - For other calendars, it's a long string like `abc123@group.calendar.google.com`
3. Add it to `scripts/config/calendar_config.json`

## Step 7: Install Dependencies

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Step 8: Test

```bash
cd LotterLaw/Website
python scripts/blog_topic_generator.py --days 7
```

---

## Configuration Files

### calendar_credentials.json (from Google Cloud)

This file is downloaded from Google Cloud Console. **Keep it secret!**

### calendar_config.json (you create)

```json
{
    "calendar_ids": [
        "your-email@gmail.com",
        "your-review-calendar-id@group.calendar.google.com"
    ],
    "keywords_to_scan": [
        "review", "case", "client", "court", "hearing", "trial"
    ]
}
```

---

## Security Notes

- **Never commit** `calendar_credentials.json` to Git
- The `.gitignore` already excludes `*credentials*.json`
- Service accounts can only see calendars explicitly shared with them

---

## Troubleshooting

### "The caller does not have permission"
- Make sure you shared the calendar with the service account email

### "Calendar API has not been used in project"
- Enable the Calendar API in Google Cloud Console

### "File not found: calendar_credentials.json"
- Download the key file and save it to `scripts/config/calendar_credentials.json`
