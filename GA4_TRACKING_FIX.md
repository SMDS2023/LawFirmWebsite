# GA4 Attribution Fix - Step-by-Step Guide

> **Issue:** Google organic traffic showing as "self-referral (lotterlaw.com)" instead of "Organic Search"
> **Impact:** Can't track organic conversions properly
> **Fix Time:** 5 minutes

---

## The Problem

**Google Search Console shows:** 180 clicks from Google
**Google Analytics 4 shows:**
- 4 views as "Organic Search" ❌
- 112 views as "Self-referral (lotterlaw.com)" ← These ARE your Google clicks
- 45 views as "Direct"
- 30 views as "Unassigned"

**Root Cause:** GA4 is seeing lotterlaw.com as the referrer instead of google.com

---

## The Fix (2 Options)

### Option 1: Add to Unwanted Referrals (RECOMMENDED - Quickest)

This is the fastest fix that solves 90% of the problem.

**Steps:**

1. Go to **Google Analytics 4**
   - URL: https://analytics.google.com/

2. Click **Admin** (gear icon, bottom left)

3. Under **Data collection and modification**, click **Data Streams**

4. Click your web stream: **lotterlaw.com**

5. Scroll down to **Additional Settings**, click **Configure tag settings**

6. Click **Show more**

7. Find **List unwanted referrals**, click it

8. Click **Add domain**

9. Enter: `lotterlaw.com`

10. Click **Add**

11. Click **Save**

**Result:** Within 24-48 hours, new traffic will be properly attributed to Google instead of self-referral.

---

### Option 2: Verify GA4 Tag Placement (Thorough Fix)

This ensures the root cause is addressed.

**Check 1: Verify GA4 Tag on All Pages**

1. Open Chrome DevTools (F12)
2. Go to **Network** tab
3. Visit homepage: https://lotterlaw.com
4. Filter by: `google-analytics.com` or `gtag`
5. You should see:
   - `collect` requests to GA4
   - gtag/config with measurement ID

**Check 2: Verify on Internal Pages**

1. From homepage, click to a practice area page
2. Check Network tab again
3. Should still see GA4 hits firing
4. Source should still show as "Google" (if you came from Google)

**Check 3: Look for Redirect Issues**

1. Test: http://lotterlaw.com (no HTTPS)
2. Does it redirect to https://lotterlaw.com?
3. Check if GA4 fires BEFORE or AFTER redirect
4. If after redirect, referrer is lost

**Fix if needed:**

Edit `.htaccess` or server config to redirect BEFORE GA4 fires:
```apache
# Add to .htaccess
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

Or ensure GA4 tag is in GTM (Google Tag Manager) which handles this better.

---

## Validation After Fix

Wait 24-48 hours, then check:

**In Google Analytics 4:**
1. Go to **Reports → Acquisition → Traffic Acquisition**
2. Look at "Session source/medium"
3. You should now see:
   - `google / organic` with ~180 sessions (matching GSC)
   - `(direct) / (none)` with ~30-40 sessions (legitimate direct)
   - Self-referral should drop to near zero

**Compare to Search Console:**

Run this to verify the numbers match:
```bash
cd ~/.claude/skills/search-console
python query.py overview --days 7
```

Then in GA4:
1. Reports → Acquisition → Traffic Acquisition
2. Filter to last 7 days
3. Google organic sessions should be within 5-10% of GSC clicks

---

## Why This Happened

**Common Causes:**

1. **User Journey:**
   - User searches Google
   - Clicks your result
   - Lands on page without GA4 tag (or it fails to load)
   - Clicks internal link
   - GA4 fires on second page, sees lotterlaw.com as referrer

2. **Redirect Chain:**
   - Google → http://lotterlaw.com → https://lotterlaw.com
   - Referrer gets lost in redirect

3. **Missing Tag:**
   - GA4 not on landing page
   - Only fires on subsequent pages

4. **GTM Issues:**
   - GTM firing late
   - GTM not configured to capture referrer correctly

---

## Current GTM Setup Check

Your site uses GTM (ID: GTM-52LMX48G). Verify:

1. Go to **Google Tag Manager**
   - URL: https://tagmanager.google.com/

2. Check GA4 tag configuration:
   - Tags → GA4 Configuration tag
   - Triggering: Should fire on "All Pages"
   - Advanced Settings → Tag Sequencing: Should be one of the first tags

3. Check if there's a "Referral Exclusion" variable:
   - Variables → User-Defined Variables
   - Look for anything related to referral exclusion

---

## Alternative Quick Fix (If Option 1 Doesn't Work)

If adding to Unwanted Referrals doesn't fully solve it, you may have a deeper issue with tag placement.

**Quick Test:**
1. Open an incognito window
2. Go to Google and search: `jeff lotter attorney`
3. Click your result
4. Open DevTools (F12) → Console
5. Type: `dataLayer`
6. Check the output - should show GA4 data with referrer as google.com

If it shows lotterlaw.com, the tag is firing too late.

**Fix:** Move GA4 tag earlier in the page load sequence (in GTM, set as highest priority tag).

---

## Expected Timeline

| Time | What Happens |
|------|--------------|
| Immediately | Unwanted referral rule saved in GA4 |
| 24-48 hours | New traffic starts being attributed correctly |
| 7 days | Historical data unchanged, but new data is clean |
| 30 days | Full month of clean data for analysis |

**Note:** Historical data (the 112 self-referral views) won't change. Only NEW traffic will be properly attributed.

---

## Monitoring

After making the fix, check weekly:

```bash
# Get GSC data
cd ~/.claude/skills/search-console
python query.py overview --days 7

# Then compare in GA4:
# Reports → Acquisition → Traffic Acquisition
# Filter to last 7 days
# google/organic should match GSC clicks ±10%
```

If they match, you've fixed it! 🎉

---

## Summary

**Fix Option 1 (5 minutes):**
GA4 Admin → Data Streams → Configure tag settings → List unwanted referrals → Add `lotterlaw.com`

**Fix Option 2 (if needed):**
Verify GA4 tag fires on all pages, especially landing pages from Google

**Validation:**
GA4 organic sessions should match GSC clicks within 5-10%

---

**Need Help?** If Option 1 doesn't fix it within 48 hours, I can help debug the GTM tag configuration.
