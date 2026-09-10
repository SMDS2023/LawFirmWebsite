# Organic lead attribution — LOJ-545, September 10, 2026

## Captured evidence

Every one of the 238 HTML documents loads `/assets/lead-tracking.js` before form initialization, including articles without forms. The tracker makes no network requests and assigns no visitor identifier. It keeps an entry record in `sessionStorage`, key `lotterlaw.lead-attribution.v2`.

A record starts when no usable record exists or a new external arrival is detected. There is no idle timer: reading an article for 45 minutes preserves its entry evidence. Internal navigation keeps the entry page, referrer and supplied campaign tags together. Back/forward restoration reads the current tab record. Blank referrers mean direct or unknown; an undetectable external return cannot reliably start a new visit. This is the first recorded page in the same browser tab, not a complete browsing history. Independent new tabs start separately, but browsers may copy session storage into a tab opened with an opener; restored tabs and cross-origin www/apex navigation have browser-dependent limits.

English, Spanish and car native forms send the same evidence to the lead service:

- Entry page and submission page separately, as absolute site URLs.
- Entry referrer and previous page before submission separately.
- Storage scope (`session` or explicitly limited `page-only`).
- Actual supplied campaign tags; missing tags remain blank for version 2 forms.
- Google click ID only when actually supplied as `gclid`; Facebook click IDs are dropped.

Page and referrer URLs exclude query strings and fragments. Android app referrers retain only the app host. If storage or the tracker is unavailable, the form can still submit with limited current-page evidence. Legacy submissions remain accepted and labeled; their historical defaults are not proof of marketing source.

The server labels known search hosts and the Google Android app as **inferred** organic search, `qr1.be` as a QR redirect, other external hosts as referral, and a blank referrer as direct or unknown. Supplied campaign tags or a Google click ID take priority over an organic inference. Search-host matching uses an explicit allow-list; unknown search providers remain referrals. A bare `/car/` visit is never proof of a QR scan. The browser evidence and campaign tags are client supplied, not independently authenticated. No per-person Google organic keyword is recovered.

The email includes human-readable attribution. Lawmatics `case_blurb` includes those lines plus exactly one final line beginning `Attribution-JSON: ` followed by JSON containing version, landing, submitted, entry_ref_host, source_class, scope, form and utm fields. User-entered multiline content is indented so it cannot impersonate that final marker. Old records cannot be backfilled with evidence never captured.

## Analytics

All three native forms push one `form_submission` event only after the lead API returns success with a prospect ID. A successful honeypot no-op response does not count as a lead. Analytics receives an allow-list from the same tracking record: real or empty source/medium/campaign, landing page, submission page, entry-referrer host and storage scope, alongside form/case/language. It receives no contact details, message, honeypot value or user agent from this payload.

This deliberately refines the QA request to copy `trackingPayload()` verbatim: that full API payload contains fields that should not enter analytics. Real browser checks verify that event and request attribution agree.

Live GTM inspection on September 10 found the existing `form_submission` trigger connected only to Clarity. A GA4 event tag is still required under LOJ-529. GA4 `form_submit` and custom `form_submission` are different events; seeing the former does not prove CRM success or this connection.

## Verification

Use Node 24 for the website and lead service. In the website checkout:

```sh
npm ci
npm test
npx playwright install chromium webkit
npm run test:browser
```

The browser runner saves evidence under `../verification/browser` by default, or `BROWSER_PROOF_DIR`. It serves the actual checkout files at intercepted site URLs. Only UI runtime CDNs are fetched; the lead API, analytics and third-party forms are intercepted or blocked. It creates no real prospect and sends no email. The Google origin is a synthetic referral page, Android referrer is explicitly simulated, and the 45-minute interval advances the browser clock. WebKit here is not a physical iPhone or Safari field test.

Results on September 10: website **16/16** unit checks; lead service **27/27** plus typecheck; blog formatter **7/7**. Browser **12/12** across Chromium and WebKit: article → homepage after a 45-minute clock advance, direct car, Spanish, blocked storage, simulated Android app referrer, and back/forward plus an independent new tab. Coverage checks all 238 HTML documents.

These verify behavior before publication. They do **not** prove production persistence, email delivery or GA4 collection. The production proof must separately read saved Lawmatics data, observe Jeff's and Stacy's receipt, verify one GA4 custom event per journey, and clean up only identified TEST prospects with DELETE followed by GET 404 under the approved proof packet.

## Rollout and remaining scope

Use three reviewed PRs and the Jeff-run rollout packet. First merge and deploy the backward-compatible lead service, then prove one legacy submission before merging the website, then verify the published tracker and merge/activate the blog formatter. Keep `NOTIFY_TO` as `jeff@jlotterlaw.com, stacy@jlotterlaw.com`. Do not run the superseded direct-push script. The lead body cap is 32 KiB; agent-note remains 4 KiB.

New pages require exactly one `<script src="/assets/lead-tracking.js"></script>` before form scripts. Website CI enforces this; the coordinated blog formatter inserts it automatically. Publish the asset before activating the formatter.

For a rollback, revert the website PR first, restore the recorded previous lead deployment, then revert the blog formatter PR; use reviewed revert commits, not rewritten history. Verify the old payload and endpoint checks after rollback.

LOJ-517's 23 JotForm iframe pages, QR target retagging and pipeline outcome reporting remain separate work. Loading this tracker on an iframe page does not connect that iframe's submission to the native lead service. LOJ-516's delivery-failure monitoring remains open.
