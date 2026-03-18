# RingCentral Campaign C0IWY7N - Resubmission Guide

**Date Implemented:** 2026-03-18
**Deployment Status:** ✅ Live on all forms
**Campaign ID:** C0IWY7N

---

## What Was Fixed

Added TCPA/Campaign Registry compliant SMS disclosure text to all contact forms on www.lotterlaw.com. The disclosure appears as static text immediately below the phone number input field on every form.

### Compliance Requirements Met

✅ **Opt-out instructions** - "Reply STOP to unsubscribe"
✅ **Customer support** - "Reply HELP for help"
✅ **Message/data rates** - "Message and data rates may apply"
✅ **Message frequency** - "Message frequency varies"

---

## Disclosure Text

### English Version
> "By providing your phone number, you consent to receive SMS messages from Lotter Law. Message frequency varies. Message and data rates may apply. Reply HELP for help or STOP to unsubscribe."

### Spanish Version
> "Al proporcionar su número de teléfono, usted consiente recibir mensajes SMS de Lotter Law. La frecuencia de mensajes varía. Pueden aplicarse tarifas de mensajes y datos. Responda HELP para ayuda o STOP para cancelar la suscripción."

---

## Live Verification URLs

**English Forms (14 active):**
- Homepage: https://www.lotterlaw.com
- DUI Practice Area: https://www.lotterlaw.com/practice-areas/dui.html
- Criminal Traffic: https://www.lotterlaw.com/practice-areas/criminal-traffic.html
- Speeding Ticket: https://www.lotterlaw.com/practice-areas/speeding-ticket.html
- Driver License Restoration: https://www.lotterlaw.com/practice-areas/driver-license-restoration.html
- Suspended License: https://www.lotterlaw.com/practice-areas/suspended-license.html
- Seal and Expunge: https://www.lotterlaw.com/practice-areas/seal-and-expunge.html
- (+ 7 more practice area pages)

**Spanish Forms (12 active):**
- Spanish Homepage: https://www.lotterlaw.com/es/
- Spanish DUI: https://www.lotterlaw.com/es/practice-areas/dui.html
- (+ 10 more Spanish practice area pages)

---

## Resubmission Details

### Campaign Registration Portal
- **Portal URL:** RingCentral Campaign Registry
- **Action:** Resubmit Campaign C0IWY7N for review
- **Updated Field:** Opt-in form URL

### Form Information to Provide
- **Opt-in Form URL:** https://www.lotterlaw.com
- **Form Type:** Website contact form
- **Disclosure Location:** Below phone number input field
- **Disclosure Visibility:** Always visible (static text, not conditional)
- **Languages Supported:** English and Spanish

### Response to Previous Rejection

**Copy this into the resubmission comments:**

> "The opt-in form has been updated to include all four required SMS compliance disclosures:
>
> 1. Message frequency disclosure: 'Message frequency varies'
> 2. Message/data rates notice: 'Message and data rates may apply'
> 3. Customer support instruction: 'Reply HELP for help'
> 4. Opt-out instruction: 'Reply STOP to unsubscribe'
>
> The disclosure text appears immediately below the phone number input field on all contact forms throughout the website (26 pages total). The text is always visible to users before they submit their information.
>
> The website supports both English (https://www.lotterlaw.com) and Spanish (https://www.lotterlaw.com/es/) with appropriately translated disclosure text on all forms."

---

## Screenshot Instructions

### For RingCentral Verification

1. **Homepage Contact Form (English)**
   - Open: https://www.lotterlaw.com
   - Scroll to "Get Your Free Consultation" form (bottom of page)
   - Screenshot should show:
     - Phone number input field
     - SMS disclosure text below the field
     - The text should be fully visible and legible

2. **Spanish Homepage (Optional)**
   - Open: https://www.lotterlaw.com/es/
   - Scroll to contact form
   - Screenshot showing Spanish disclosure text

3. **Mobile View (Optional)**
   - Open homepage on mobile device or use browser DevTools (F12 → Toggle device toolbar)
   - Verify disclosure text is readable on mobile screens
   - Screenshot if requested

### What to Highlight in Screenshots
- The compliance text is clearly visible
- It appears before the submit button
- It's placed contextually near the phone field
- All four required elements are present

---

## Implementation Details

- **Files Updated:** 26 HTML files (14 English + 12 Spanish)
- **Method:** Python automation script with regex pattern matching
- **Placement:** After phone field error message, before closing div
- **Styling:** Tailwind CSS classes (text-gray-600, text-xs, mt-2, leading-relaxed)
- **Form Behavior:** No changes - forms still submit to JotForm exactly as before

---

## Verification Checklist

✅ Homepage (English) - Compliance text visible
✅ DUI Practice Area (English) - Compliance text visible
✅ Homepage (Spanish) - Compliance text visible
✅ Mobile display - Text properly formatted
✅ Form submission - Still works correctly

**Deployment Date:** 2026-03-18
**Next Review:** After RingCentral approval

---

## Contact Information

If RingCentral has questions about the implementation:
- Website owner: Lotter Law
- Primary URL: https://www.lotterlaw.com
- Forms processing: JotForm integration
- SMS provider: RingCentral

---

## Additional Notes

- Disclosure text meets FCC TCPA requirements
- Complies with Campaign Registry standards
- Provides clear opt-in consent mechanism
- No checkbox required (static disclosure is sufficient per TCPA)
- Users see disclosure before they can submit phone number
- Text is permanent (not dismissible or hideable)

**Status:** Ready for resubmission ✅
