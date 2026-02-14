# Conversion Tracking Phase 1 - UTM Capture on JotForm

**Date:** 2026-02-14
**Status:** Live and Verified
**PRs:** [#45](https://github.com/SMDS2023/LawFirmWebsite/pull/45) (UTM tracking), [#46](https://github.com/SMDS2023/LawFirmWebsite/pull/46) (Alpine.js fix)

---

## The Problem

LotterLaw's marketing funnel was disconnected. When a potential client filled out the consultation form, **all knowledge of how they found the site was lost.** GA4, Facebook Pixel, JotForm, LawMatics, and Square each knew a piece of the story but none were linked.

The #1 gap: JotForm captured zero source attribution data. There was no way to answer: "I spent $X on Google Ads last month -- how many consultation requests did that actually generate?"

---

## What Was Built

### 1. JotForm Hidden Fields (Form ID: 251224345324145)

Seven hidden fields were added to the consultation form via the JotForm API:

| Field | Question ID | Purpose |
|-------|-------------|---------|
| utm_source | q24 | Traffic source (google, facebook, direct) |
| utm_medium | q25 | Marketing medium (cpc, organic, social, referral) |
| utm_campaign | q26 | Campaign name (dui_orlando_2026, etc.) |
| utm_content | q27 | Ad content variant (for A/B testing) |
| utm_term | q28 | Paid search keyword |
| gclid | q29 | Google/Facebook click ID (auto-tagged) |
| landing_page | q30 | Which page the user was on when they submitted |

These fields are hidden from users but accept values when the form is submitted programmatically.

### 2. JavaScript UTM Capture (contact-form.js + contact-form-es.js)

An `init()` method was added to the Alpine.js contact form component that runs on every page load:

**On page load:**
- Reads UTM parameters from the URL (`?utm_source=google&utm_medium=cpc&...`)
- Stores them in `sessionStorage` using first-touch attribution (the first source wins, even if the user clicks another link later in the same session)
- Also captures `fbclid` (Facebook click ID) and maps it to the `gclid` field
- Records the landing page path (first page the user visited)

**On form submit:**
- Appends all 7 hidden field values to the JotForm POST request
- Includes UTM data in the GTM `dataLayer.push` event for GA4/Facebook attribution

**Key design decisions:**
- **First-touch attribution:** If a user arrives via a Google Ad, then navigates around the site, their original source is preserved. The UTM params are stored in `sessionStorage` and only the first set is kept.
- **sessionStorage vs localStorage:** `sessionStorage` was chosen because it clears when the browser tab closes. This means each new visit starts fresh, which is appropriate for lead attribution.
- **fbclid mapped to gclid field:** Both are click IDs from ad platforms. Rather than adding a separate field, Facebook's click ID is stored in the same gclid field since a user can only arrive from one ad platform per session.

### 3. GTM DataLayer Enhancement

The `form_submission` event pushed to GTM's dataLayer now includes:
- `utm_source` (defaults to "direct" if no UTM params)
- `utm_medium`
- `utm_campaign`
- `landing_page`

This means GA4 and Facebook Pixel can see attribution data on form submission events without needing to query JotForm.

---

## Issues Encountered

### Issue 1: Alpine.js Missing on DUI Page (Critical)

**Symptom:** After deploying UTM tracking, testing on the live DUI page showed both "Success!" and "Error!" messages visible on page load, before any form submission. The form submission appeared to work (success message showed) but no data reached JotForm.

**Root Cause:** The DUI practice area page (`practice-areas/dui.html`) was missing the Alpine.js CDN script tag:
```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

Without Alpine.js loaded, the `x-data="contactForm()"` directive never initialized, `x-show` directives never evaluated (so success/error messages were always visible), and `@submit.prevent` never attached (so the form's default submit behavior may have fired instead of the JavaScript handler).

**Impact:** The Alpine.js contact form on the DUI page was **never functional** -- not just after our changes, but likely since it was created. The 136 existing JotForm submissions came through a separate JotForm iframe embed at the bottom of the page, not the Alpine.js form.

**Fix:** Added the missing Alpine.js script tag (PR #46).

**Audit results:** Only 3 of 18 practice area pages were missing Alpine.js:
- `dui.html` -- Fixed (has contact form)
- `dv.html` -- Not an issue (redirect page only)
- `excessive-speed.html` -- Has Alpine `x-data` toggles but no contact form (should be fixed separately)

### Issue 2: JotForm Hidden Fields Created as Visible

**Symptom:** The JotForm API created the 7 new fields as visible text fields instead of hidden fields.

**Resolution:** A second API call was made to add a conditional hide rule that hides all 7 fields. The fields are hidden on the form display but still accept values when submitted via the API POST.

---

## How UTM Parameters Work (For Reference)

UTM parameters are tags added to URLs that tell analytics tools where traffic came from. When you create a Google Ad or Facebook campaign, these get added automatically:

```
lotterlaw.com/practice-areas/dui.html?utm_source=google&utm_medium=cpc&utm_campaign=dui_orlando_2026&gclid=abc123
```

| Parameter | Example | Meaning |
|-----------|---------|---------|
| utm_source | google | Which platform sent the traffic |
| utm_medium | cpc | How (paid click, organic, social, referral) |
| utm_campaign | dui_orlando_2026 | Which specific campaign |
| utm_content | headline_v2 | Which ad variant (A/B testing) |
| utm_term | dui lawyer orlando | Which keyword triggered the ad |
| gclid | EAIaIQobC... | Google's auto-generated click ID |
| fbclid | fb0gY2x... | Facebook's auto-generated click ID |

Google Ads adds `gclid` automatically. Facebook adds `fbclid` automatically. The `utm_*` parameters are either auto-added by the ad platform or manually added when creating campaign links.

---

## How to Verify It's Working

### Check a JotForm Submission
1. Go to [JotForm Submissions](https://www.jotform.com/tables/251224345324145)
2. Look at recent submissions
3. The UTM columns (utm_source, utm_medium, etc.) should have values for any lead that arrived via a tracked link

### Test Manually
1. Visit: `lotterlaw.com/practice-areas/dui.html?utm_source=test&utm_medium=manual&utm_campaign=testing`
2. Open browser DevTools (F12) -> Console
3. Type: `sessionStorage.getItem('utm_source')` -- should return `"test"`
4. Submit the form with test data
5. Check JotForm for the submission with UTM values
6. Delete the test submission when done

### Check GTM DataLayer
1. Visit any page with UTM params
2. Open DevTools -> Console
3. Submit the form
4. Type: `dataLayer.filter(e => e.event === 'form_submission')`
5. The event should include `utm_source`, `utm_medium`, `utm_campaign`, `landing_page`

---

## What Should Be Done Next

### Phase 2: JotForm -> LawMatics Integration (High Priority)

Right now UTM data lives only in JotForm. To connect it to actual client records:

1. **Create LawMatics custom fields** for source tracking:
   - Lead Source (utm_source)
   - Lead Medium (utm_medium)
   - Lead Campaign (utm_campaign)
   - Landing Page
   - Google Click ID

2. **Build JotForm -> LawMatics automation** (via Zapier or direct API):
   - When a new JotForm submission arrives, create/update a LawMatics contact
   - Map UTM fields from JotForm to LawMatics custom fields
   - This closes the gap between "where did they come from?" and "did they hire us?"

### Phase 3: Revenue Attribution (Medium Priority)

Link Square payments back to the original lead source:

1. When a client pays via Square, match the payment to their LawMatics matter
2. LawMatics matter has UTM data from Phase 2
3. Now you can calculate: "Google Ads spent $2,000 -> generated 15 leads -> 4 hired -> $12,000 revenue"

### Phase 4: Marketing ROI Dashboard (Lower Priority)

Build a Power BI dashboard combining:
- GA4 traffic data (by source/medium)
- JotForm submissions (by UTM params)
- LawMatics conversion rates (lead -> hired)
- Square revenue (by client/matter)

This would show real ROI per marketing channel in one view.

### Other Improvements

- **Fix Alpine.js on excessive-speed.html:** This page has Alpine `x-data` directives for expand/collapse toggles and the testimonial slider but no Alpine.js script. The toggles and slider are broken there.

- **UTM capture on all pages (not just form pages):** Currently UTM params are only captured when the user lands on a page that loads `contact-form.js`. If someone lands on the homepage with UTMs then navigates to a practice area page, the params are captured because `sessionStorage` persists. But if they land on a blog post (which doesn't load `contact-form.js`), the UTMs are lost. A lightweight UTM capture script on all 58 pages would fix this.

- **Phone call tracking:** Form submissions are only one conversion channel. Phone calls (the "Call Now" button) are not tracked by source. A service like CallRail could assign dynamic phone numbers based on traffic source, connecting phone leads to marketing channels.

---

## Files Modified

| File | Change |
|------|--------|
| `assets/contact-form.js` | Added `init()` for UTM capture, hidden field submission, GTM dataLayer enhancement |
| `assets/contact-form-es.js` | Same changes as above (Spanish version) |
| `practice-areas/dui.html` | Added missing Alpine.js CDN script tag |
| JotForm form 251224345324145 | Added 7 hidden fields (q24-q30) via API |
