# Organic lead attribution — prepared September 10, 2026

## What is captured
Every HTML document loads /assets/lead-tracking.js before form initialization, including articles without forms. The script makes no network requests and assigns no visitor identifier. It saves one entry record in sessionStorage under lotterlaw.lead-attribution.v2.

A visit starts when no usable entry record exists, more than 30 minutes have passed between page loads, or a new external referrer is observed. Internal navigation preserves the original entry and campaign tags as a bundle. Later internal campaign tags do not overwrite it. Blank referrers mean direct or unknown, not confirmed direct traffic. Same-tab/session limitations and browser restrictions still apply; this is observed evidence, not a complete browsing history.

Email and Lawmatics case_blurb receive:
- Source evidence (entry-referrer hostname, or an explicit uncertainty).
- Landing page (first recorded), as an absolute address.
- Submitted from page, separately from the entry page.
- Entry referrer and previous page before submission, separately.
- Tracking scope, including current-page-only fallback if storage is blocked.
- Actual supplied campaign tags; absent new-form tags stay blank.
Page/referrer addresses omit query strings and fragments. Campaign fields are retained separately. Google organic search phrases are not recovered. Facebook click IDs are never relabeled as Google click IDs.

English, Spanish, and car QR forms use the same tracking record. If the tracker fails to load or storage is unavailable, forms still submit with explicitly limited page evidence. Existing consent, validation, honeypot and recipient configuration remain in place.

## Verification
Site: node --test tests/lead-tracking.test.mjs
Lead service: npm run typecheck && npm test
Blog pipeline: PYTHONPATH=. /Users/jefflotter/Code/blog-pipeline/.venv/bin/python -m pytest tests/test_lead_tracking.py tests/test_format_cards.py -q

Tests cover a Google-referred article followed by a contact page, unknown/hidden sources, partial campaign tags, internal tags, Unicode body size, old forms, storage failures, all form types, and all 238 HTML documents. Form/network tests are simulated; no real prospects or notification emails are created. Live verification must follow approved deployment.

## Future pages
Website CI checks every HTML document for exactly one tracker before form scripts. New pages must include:
<script src="/assets/lead-tracking.js"></script>
The coordinated blog-pipeline formatter change inserts this automatically into future articles. It must ship with the website asset. Do not deploy the formatter before that asset exists.

## Deployment and rollback
The work is prepared in three codex/organic-lead-tracking branches, one per repository. Production approval is required. Deploy the backward-compatible lead service first, then publish the website, then update the blog formatter. Keep NOTIFY_TO as jeff@jlotterlaw.com, stacy@jlotterlaw.com.

The lead handler accepts up to 32 KiB for lead text plus attribution; field-level validation remains bounded. The separate agent-note endpoint remains capped at 4 KiB. The expanded request limit requires the new backend before the new forms.

For rollback, revert the website commit first so old payloads are restored, then restore the prior lead deployment. Revert the blog formatter change if withdrawing the tracking asset. Use revert commits rather than overwriting source history.

Old lead records cannot be backfilled with missing entry or submission information.
