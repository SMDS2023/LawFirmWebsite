# SEO Automation & Monitoring Setup

> **Generated:** 2026-01-28
> **Purpose:** Automate weekly SEO monitoring and track meta description improvements

---

## What's Been Set Up

### 1. ✅ GA4 Attribution Fix
**File:** `GA4_TRACKING_FIX.md`

**What it does:** Fixes Google organic traffic showing as "self-referral" in GA4

**Action Required:**
1. Open Google Analytics 4
2. Admin → Data Streams → lotterlaw.com → Configure tag settings
3. Show more → List unwanted referrals → Add `lotterlaw.com`
4. Save

**Time:** 5 minutes
**Impact:** Proper organic traffic attribution in GA4

---

### 2. ✅ Next Batch of Meta Descriptions
**File:** `META_DESCRIPTIONS_BATCH_2.md`

**What it includes:**
- Moving Violations page
- Seal & Expunge page
- Suspended License page

**Expected Impact:** +152 clicks/month
**Status:** Ready to deploy (just say "update batch 2")

---

### 3. ✅ Weekly Monitoring Automation
**Location:** `~/.claude/skills/search-console/`

**Files Created:**
- `weekly_monitor.py` - Monitoring script
- `run_weekly_monitor.bat` - Batch wrapper
- `setup_weekly_monitoring.ps1` - Task Scheduler setup

**What it does:**
- Runs every Monday at 9 AM automatically
- Pulls last 7 days of Search Console data
- Tracks CTR improvements on optimized pages
- Identifies pages needing attention
- Saves report to `.index/weekly_report_YYYY-MM-DD.txt`

---

## Setup Instructions

### Step 1: Install Scheduled Task (One-Time Setup)

**Option A: PowerShell (Recommended)**
```powershell
cd C:\Users\jeff\.claude\skills\search-console
powershell -ExecutionPolicy Bypass -File setup_weekly_monitoring.ps1
```

**Option B: Manual Task Scheduler**
1. Open Task Scheduler: `Win+R` → `taskschd.msc`
2. Action → Create Basic Task
3. Name: `SEO_Weekly_Monitor`
4. Trigger: Weekly, Monday, 9:00 AM
5. Action: Start a program
6. Program: `C:\Users\jeff\.claude\skills\search-console\run_weekly_monitor.bat`
7. Finish

### Step 2: Test It Now (Optional)

Don't wait until Monday - test it immediately:

```bash
cd ~/.claude/skills/search-console
python weekly_monitor.py
```

You should see:
```
================================================================================
WEEKLY SEO MONITORING REPORT
Generated: 2026-01-28 11:15
================================================================================

OVERALL PERFORMANCE (Last 7 Days)
--------------------------------------------------------------------------------
Clicks:      45
Impressions: 7,500
CTR:         0.60%
Avg Pos:     13.5

OPTIMIZED PAGES TRACKING
--------------------------------------------------------------------------------
Page                                               CTR  Target     Status
--------------------------------------------------------------------------------
/practice-areas/tolls.html                       0.5%    3.0%   ➡️ Stable
/                                                0.4%    3.0%   ➡️ Stable
/practice-areas/excessive-speed.html             0.5%    3.0%   ➡️ Stable
```

**Expected Status:**
- Week 1-2: "➡️ Stable" (Google still re-crawling)
- Week 3-4: "📈 Improving" (New metas showing, CTR rising)
- Week 5+: "✅ Good" (Target met or approaching)

---

## How Monitoring Works

### What Gets Tracked

**3 Metrics for Each Optimized Page:**
1. **Current CTR** - Last 7 days actual CTR
2. **Target CTR** - Goal (usually 3%)
3. **Status:**
   - ✅ Good: Within 90% of target
   - 📈 Improving: 20%+ better than baseline
   - ➡️ Stable: No significant change yet
   - ⚠️ Check: Dropped below baseline

### When to Act

**Week 1-2 After Changes:**
- Expected: "➡️ Stable" (normal - Google needs time)
- Action: None, wait for re-crawl

**Week 3-4 After Changes:**
- Expected: "📈 Improving" (CTR starting to rise)
- If still "➡️ Stable": Check if Google re-indexed
  - Go to: `site:lotterlaw.com/practice-areas/tolls.html` in Google
  - Check if new meta description is showing

**Week 5+ After Changes:**
- Expected: "✅ Good" (target met)
- If still "➡️ Stable" or "⚠️ Check":
  - A/B test alternative meta descriptions
  - Check if competitors changed their listings
  - Consider optimizing title tags too

---

## Weekly Monitoring Schedule

### Automatic (Scheduled Task)
- **When:** Every Monday at 9:00 AM
- **What:** Runs `weekly_monitor.py` automatically
- **Output:** Saved to `.index/weekly_report_YYYY-MM-DD.txt`
- **Log:** `.index/weekly_monitor_output.log`

### Manual (On-Demand)
```bash
cd ~/.claude/skills/search-console
python weekly_monitor.py
```

### View Reports
```bash
# View latest report
cat ~/.claude/skills/search-console/.index/weekly_report_*.txt | tail -100

# View log
cat ~/.claude/skills/search-console/.index/weekly_monitor_output.log
```

---

## Expected Timeline & Results

### Batch 1 (Already Deployed)

| Page | Deployed | Week 2 | Week 4 | Week 8 | Target |
|------|----------|--------|--------|--------|--------|
| Tolls | 2026-01-28 | 0.5% → 0.8% | 1.2% | 2.5% | 3.0% |
| Homepage | 2026-01-28 | 0.4% → 0.6% | 1.0% | 2.0% | 3.0% |
| Excessive Speed | 2026-01-28 | 0.5% → 0.8% | 1.3% | 2.5% | 3.0% |

**Projected Clicks:**
- Week 2: +50 clicks/month
- Week 4: +150 clicks/month
- Week 8: +300 clicks/month (full impact)

### Batch 2 (Ready to Deploy)

Deploy after seeing Batch 1 improvements (Week 4-6):
- Moving Violations
- Seal & Expunge
- Suspended License

**Additional:** +152 clicks/month at maturity

---

## Monitoring Checklist

### Weekly (Automated)
- [x] Monday 9 AM: Automated report runs
- [ ] Monday 10 AM: Review report (check email or log file)
- [ ] Note any "⚠️ Check" pages
- [ ] Compare to previous week

### Monthly (Manual)
```bash
cd ~/.claude/skills/search-console
python query.py full --days 28
```

- [ ] Review overall traffic trend
- [ ] Check for new keyword opportunities
- [ ] Identify next pages to optimize
- [ ] Update state index

### Quarterly (Strategic)
- [ ] Analyze conversion data (GSC + GA4)
- [ ] Calculate ROI of SEO efforts
- [ ] Plan next optimization batch
- [ ] Review competitor changes

---

## Troubleshooting

### Task Not Running

**Check task status:**
```powershell
Get-ScheduledTask -TaskName "SEO_Weekly_Monitor"
```

**Check last run result:**
```powershell
Get-ScheduledTask -TaskName "SEO_Weekly_Monitor" | Get-ScheduledTaskInfo
```

**Check log file:**
```bash
cat ~/.claude/skills/search-console/.index/weekly_monitor_output.log
```

### Python Errors

**Check Python path:**
```bash
where python
```

**Test script directly:**
```bash
cd ~/.claude/skills/search-console
python weekly_monitor.py
```

**Common fixes:**
- Ensure Search Console token is valid: `python connect.py --test`
- Refresh token if expired: `python connect.py --auth`

### No Data Showing

**Possible causes:**
1. Page not getting traffic (check GSC)
2. Date range issue (script looks at last 7 days)
3. Token expired (refresh with `connect.py --auth`)

**Fix:**
```bash
# Check if page has data
python query.py pages --days 28 | grep "tolls"
```

---

## Email Notifications (Future Enhancement)

To get email reports automatically:

1. Uncomment email function in `weekly_monitor.py`
2. Integrate with `/gmail` skill:
   ```python
   from gmail import send_email
   send_email(
       to='jeff@jlotterlaw.com',
       subject='Weekly SEO Report',
       body=report_text
   )
   ```
3. Update Task Scheduler to run with network access

---

## Files Created

| File | Purpose |
|------|---------|
| `GA4_TRACKING_FIX.md` | Guide to fix GA4 attribution |
| `META_DESCRIPTIONS_BATCH_2.md` | Next 3 pages to optimize |
| `weekly_monitor.py` | Monitoring script |
| `run_weekly_monitor.bat` | Batch wrapper for Task Scheduler |
| `setup_weekly_monitoring.ps1` | One-time setup script |
| `.index/weekly_report_YYYY-MM-DD.txt` | Weekly reports (auto-generated) |
| `.index/weekly_monitor_output.log` | Script execution log |

---

## Quick Commands Reference

### Setup (One-Time)
```powershell
cd C:\Users\jeff\.claude\skills\search-console
powershell -ExecutionPolicy Bypass -File setup_weekly_monitoring.ps1
```

### Test Monitoring
```bash
python weekly_monitor.py
```

### Check Full Report
```bash
python query.py full --days 28
```

### View Latest Weekly Report
```bash
cat .index/weekly_report_$(date +%Y-%m-%d).txt
```

### Check Task Status
```powershell
Get-ScheduledTask -TaskName "SEO_Weekly_Monitor"
```

---

## Summary

✅ **GA4 fix:** 5-minute manual step (one-time)
✅ **Batch 2 meta descriptions:** Ready to deploy (+152 clicks/month)
✅ **Weekly monitoring:** Automated - runs every Monday at 9 AM

**Next Steps:**
1. Fix GA4 unwanted referrals (5 minutes)
2. Run setup script to install scheduled task (1 minute)
3. Test monitoring: `python weekly_monitor.py`
4. Deploy Batch 2 when ready: "update batch 2"

**Expected Result:** Automated weekly reports tracking your SEO improvements with zero ongoing effort.
