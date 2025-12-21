# GTM CTA Click Tracking Setup

## Overview

This guide explains how to set up CTA (Call-to-Action) click tracking in Google Tag Manager for the LotterLaw website.

## Current Implementation

The mobile CTA bar already includes inline GA4 tracking via `gtag()`:

```html
onclick="if(typeof gtag === 'function') gtag('event', 'click_to_call', {
  event_category: 'CTA',
  event_label: 'Mobile Sticky Bar',
  phone_number: '407-500-7000'
});"
```

This will work once GA4 is configured in GTM (part of T-001).

## Setting Up CTA Tracking in GTM

### Step 1: Create a GA4 Event Tag for CTA Clicks

1. Log into [Google Tag Manager](https://tagmanager.google.com)
2. Select the LotterLaw container (GTM-PLX85K8L)
3. Go to **Tags** > **New**

**Tag Configuration:**
- **Tag Type:** Google Analytics: GA4 Event
- **Measurement ID:** G-D28BZM9QDC
- **Event Name:** `click_to_call`

**Event Parameters:**
| Parameter Name | Value |
|---------------|-------|
| event_category | CTA |
| event_label | {{Click Text}} |
| phone_number | 407-500-7000 |
| page_location | {{Page URL}} |

### Step 2: Create Click Trigger for Phone Links

1. Go to **Triggers** > **New**
2. **Trigger Type:** Just Links (Click - Just Links)
3. **Name:** Phone Link Clicks

**Trigger Configuration:**
- **This trigger fires on:** Some Link Clicks
- **Condition:** Click URL → contains → `tel:`

### Step 3: Connect Tag and Trigger

1. In your GA4 Event tag, add the Phone Link Clicks trigger
2. Save the tag

### Step 4: Create Variables (Optional but Recommended)

**Click Text Variable:**
1. Go to **Variables** > **User-Defined Variables** > **New**
2. **Variable Type:** Auto-Event Variable
3. **Variable Type (in dropdown):** Click Text
4. **Name:** Click Text

### Step 5: Preview and Test

1. Click **Preview** in GTM
2. Open the LotterLaw website in the preview mode
3. Click on the mobile CTA bar or any phone link
4. Verify the `click_to_call` event fires in the GTM debugger

### Step 6: Publish

1. Click **Submit** in GTM
2. Add a version name like "Add CTA Click Tracking"
3. Click **Publish**

## Viewing CTA Data in GA4

After publishing, CTA clicks will appear in:

1. **GA4 Real-Time:** Reports > Real-time > Events
2. **GA4 Events:** Reports > Engagement > Events
3. **GA4 Explore:** Custom reports filtering by `click_to_call`

## Creating a CTA Performance Report in GA4

1. Go to GA4 > **Explore**
2. Create a new **Free-form** exploration
3. Add dimensions: `event_label`, `page_location`
4. Add metrics: `event_count`, `sessions`
5. Filter by event_name = `click_to_call`

## A/B Testing (Future Enhancement)

Once T-001 is complete and GTM is managing all analytics, you can:

1. Create different CTA variants (text, colors)
2. Use GTM to randomly assign variants
3. Track conversion rates per variant
4. Use Google Optimize integration (optional)

## Files Modified

- `styles.css` - Added `.mobile-cta-bar` styling
- All public HTML pages - Added mobile CTA bar HTML component

## Related Tasks

- T-001: Complete GTM Migration (must be done first for full tracking)
- T-008: Improve Call-to-Action Visibility (this task)

---

*Last Updated: 2025-12-12*
