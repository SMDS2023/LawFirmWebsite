# Enable Gmail and Drive APIs

The blog topic generator can cross-reference topics with Gmail and Google Drive, but these APIs need to be enabled first.

## Steps

1. **Open Google Cloud Console**
   - Go to: https://console.cloud.google.com/apis/library
   - Ensure project `avid-grid-456712-h7` is selected (top dropdown)

2. **Enable Gmail API**
   - Search for "Gmail API"
   - Click on it
   - Click **Enable**

3. **Enable Google Drive API**
   - Search for "Google Drive API"
   - Click on it
   - Click **Enable**

4. **Re-run the script**
   ```bash
   cd LotterLaw/Website
   python scripts/blog_topic_generator.py --days 30
   ```

## What Gets Scanned

| Source | What's Searched | Privacy |
|--------|-----------------|---------|
| Gmail | Subject lines for case keywords (DUI, traffic, etc.) | Anonymized - no names shown |
| Drive | File names with case keywords | Anonymized - no client names |
| Calendar | Event titles | Shows event titles |
| Local Files | Case files in Active-Cases, Case-Management | Shows filenames |

## Permissions Used

All APIs use **read-only** access:
- `gmail.readonly` - Can read email metadata (subject, date) but not compose
- `drive.readonly` - Can list/read files but not modify
- `calendar.readonly` - Can read events but not create/modify

## Re-Authorization

If you need to re-authorize (add/remove permissions), delete:
```
scripts/config/google_token.json
```
Then run the script again to trigger new OAuth flow.
