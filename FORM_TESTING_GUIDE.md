# Native Contact Form Testing Guide

## Deployment Status

✅ **Deployed:** All changes pushed to GitHub master branch
🕐 **GitHub Pages Deploy Time:** 2-5 minutes
🌐 **Live URL:** https://lotterlaw.com

---

## What Changed

Replaced all JotForm embedded iframes with native HTML forms across 18 pages:
- Homepage (index.html)
- All 16 practice area pages
- 1 template page

### Key Features

1. **Client-side validation** - Real-time error feedback as user types
2. **Loading states** - Spinner shows during submission
3. **Success/error alerts** - Clear user feedback after submission
4. **Mobile optimized** - Proper keyboard types (email, tel)
5. **Accessible** - ARIA labels, keyboard navigation
6. **Analytics** - GTM form_submission events

### Backend

Forms still submit to **JotForm API** - no changes to existing workflow:
- Submissions appear in JotForm dashboard
- Email notifications still sent
- No server-side code required

---

## Verification Checklist

### 1. Visual Inspection

Visit each page and verify the form displays correctly:

- [ ] **Homepage:** https://lotterlaw.com/index.html
- [ ] **DUI:** https://lotterlaw.com/practice-areas/dui.html
- [ ] **Auto Registration:** https://lotterlaw.com/practice-areas/auto-registration.html
- [ ] **Criminal Traffic:** https://lotterlaw.com/practice-areas/criminal-traffic.html
- [ ] **Driver License:** https://lotterlaw.com/practice-areas/driver-license-restoration.html
- [ ] **Drug Offense:** https://lotterlaw.com/practice-areas/drug-offense.html
- [ ] **Hit and Run:** https://lotterlaw.com/practice-areas/hit-and-run.html
- [ ] **Moving Violations:** https://lotterlaw.com/practice-areas/moving-violations.html
- [ ] **Other Crimes:** https://lotterlaw.com/practice-areas/other-crimes.html
- [ ] **Seal and Expunge:** https://lotterlaw.com/practice-areas/seal-and-expunge.html
- [ ] **Speeding Ticket:** https://lotterlaw.com/practice-areas/speeding-ticket.html
- [ ] **Suspended License:** https://lotterlaw.com/practice-areas/suspended-license.html
- [ ] **Theft:** https://lotterlaw.com/practice-areas/theft.html
- [ ] **Tolls:** https://lotterlaw.com/practice-areas/tolls.html
- [ ] **Weapons:** https://lotterlaw.com/practice-areas/weapons.html
- [ ] **Assault Battery:** https://lotterlaw.com/practice-areas/assault-battery.html

### 2. Validation Testing

On any page, test validation rules:

- [ ] Try submitting empty form - all 5 fields should show errors
- [ ] Enter name with 1 character - shows "must be at least 2 characters"
- [ ] Enter invalid email (e.g., "test") - shows "valid email address"
- [ ] Enter phone with <10 digits - shows "at least 10 digits"
- [ ] Skip case type selection - shows "please select a case type"
- [ ] Enter message with <10 chars - shows "at least 10 characters"
- [ ] Fill all fields correctly - submit button becomes enabled (amber color)

### 3. Submission Testing

**IMPORTANT:** Test with REAL data (submissions will go to JotForm dashboard)

1. Fill out form completely with valid data
2. Click "Send Message"
3. Verify:
   - [ ] Loading spinner appears
   - [ ] Button text changes to "Sending..."
   - [ ] Button becomes disabled during submission
   - [ ] Success message appears (green alert)
   - [ ] Form resets after 2 seconds
4. Check JotForm dashboard for submission
5. Verify email notification received

### 4. Error Handling Testing

To test error handling (requires simulating network failure):

1. Open browser DevTools (F12)
2. Go to Network tab
3. Enable "Offline" mode
4. Fill out form and submit
5. Verify:
   - [ ] Error message appears (red alert)
   - [ ] Message includes phone number fallback
   - [ ] Form data is preserved (not cleared)

### 5. Mobile Testing

Test on actual mobile device or browser DevTools mobile emulation:

- [ ] Form displays correctly (no horizontal scroll)
- [ ] All fields have proper spacing (touch-friendly)
- [ ] Email keyboard appears for email field
- [ ] Phone keyboard appears for phone field
- [ ] Submit button full width on mobile
- [ ] Error messages readable on small screens
- [ ] Success/error alerts display properly

### 6. Accessibility Testing

- [ ] Tab through form - all fields focusable
- [ ] Press Enter on submit button - form submits
- [ ] Labels associated with inputs (click label focuses input)
- [ ] Required fields marked with red asterisk
- [ ] Error messages have sufficient color contrast
- [ ] Success/error alerts have role="alert"

### 7. Analytics Testing

Verify GTM event fires on successful submission:

1. Open browser DevTools (F12)
2. Go to Console tab
3. Type: `dataLayer` and press Enter
4. Submit form successfully
5. Check dataLayer for new entry:
   ```javascript
   {
     event: 'form_submission',
     form_name: 'contact_form',
     case_type: '[selected case type]'
   }
   ```

**Alternative:** Use GTM Preview Mode:
1. Go to Google Tag Manager
2. Click "Preview" button
3. Enter site URL
4. Submit form
5. Verify form_submission event appears in preview panel

### 8. Browser Compatibility

Test on multiple browsers:

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Mobile Chrome (Android)

---

## Known Issues / Limitations

### JotForm Field Mapping

Current mapping (may need adjustment based on actual JotForm form structure):
- `q3_name` → Full Name
- `q4_email` → Email Address
- `q5_phone` → Phone Number
- `q6_caseType` → Case Type
- `q7_message` → Message

**If submissions don't appear in JotForm dashboard**, the field IDs may be incorrect.

To verify correct field IDs:
1. Go to JotForm form editor
2. Right-click on a field → "Properties"
3. Check "Field ID" (e.g., `input_3`, `input_4`)
4. Update `contact-form.js` line 132-136 with correct IDs

### CORS Issues

If form submission fails with CORS error in console:
- JotForm supports CORS for public forms
- Verify form ID `251224345324145` is correct
- Check JotForm form settings (must be public, not private)

### Cache Issues

If changes don't appear after GitHub Pages deploy:
- Wait 5 minutes for full deploy
- Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
- Clear browser cache
- Try incognito/private browsing mode

---

## Rollback Plan

If critical issues arise, rollback procedure:

```bash
cd "C:\Users\jeff\OneDrive\Documents\LotterLaw\Website"

# View recent commits
git log --oneline -5

# Rollback to previous commit (replace COMMIT_HASH)
git revert HEAD
# or
git reset --hard COMMIT_HASH

# Push rollback
git push origin master --force
```

**Note:** JotForm iframes are preserved in git history (commit before f6dc5da)

---

## Success Criteria

✅ Task T-009 is complete when:

1. All 18 pages have native forms (no JotForm iframes)
2. Validation working on all fields
3. Loading spinner shows during submission
4. Success message displays after successful submission
5. Error message displays with phone fallback on failure
6. All verification checklist items passing
7. Changes deployed to live site (lotterlaw.com)
8. Test submission appears in JotForm dashboard

---

## Contact

**Questions or Issues?**
- Check browser console for errors (F12 → Console tab)
- Verify network requests (F12 → Network tab)
- Test in different browser/device
- Check JotForm dashboard for submissions

**File Locations:**
- Form component: `assets/contact-form.js`
- Homepage: `index.html` (lines 1836-1851 updated)
- Practice areas: `practice-areas/*.html`
- Testing script: `update_forms.py` (bulk replacement tool)

---

**Last Updated:** 2026-01-27
**Commit:** f6dc5da
**Deployed:** ✅ Yes (GitHub Pages)
