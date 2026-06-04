# Analytics Credentials

This directory is intentionally gitignored for secrets.

Expected local files:

- `ga4_service_account.json` - preferred GA4 Data API service account key.
- `analytics_token.json` - optional GA4 OAuth token alternative.
- `clarity_token.txt` - Microsoft Clarity API key/token.

Do not commit credential files. After adding credentials, run:

```bash
cd /Users/jefflotter/LawFirmWebsite
analytics/.venv/bin/python analytics/analytics_report.py --week 2026-W20 --dry-run
```

The command must succeed without `--allow-mock` before any report is treated as real.
