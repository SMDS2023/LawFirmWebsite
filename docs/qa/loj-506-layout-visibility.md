# LOJ-506 — Layout and content visibility

2026-09-29. Base: e4e958c (existing PR #132, claude/stoic-cerf-vynh5b).

PR #132 already contains the five homepage copy corrections and root-home link normalization. This companion change fixes the remaining homepage logo `#` link, floating sidebar overlap, and observer-dependent content visibility. It does not independently approve or review all of PR #132.

Content now defaults to full opacity and no entrance translation in both shared stylesheets and the 16 EN/ES pages with embedded copies. This deliberately removes the scroll-reveal effect: initial content, anchor destinations, and pages with absent or failed observers remain readable. Existing hover effects and disclosure controls are retained.

The sidebar is hidden below 2160 CSS pixels. The 1536px container plus two 312px gutters requires 2160px; the issue's approximate 1760px breakpoint would still overlap the actual container. At 2160px Chrome measured the content right edge at 1840.5px and sidebar left edge at 1869px (28.5px clearance including the scrollbar).

Verification on local HTTP server (port 8506):
- 1440px homepage: sidebar display none; zero hidden section-fade-in nodes; header logo href `/`.
- 2160px homepage: sidebar display block with the clearance above; zero hidden sections.
- Blog index: all 158 section-fade-in cards at opacity 1.
- 390px toll page: no horizontal overflow; zero hidden sections; Toll Scams warning opacity 1.
- Source diff covers both shared and all embedded `.section-fade-in` base rules, so visibility does not depend on JavaScript execution.
- `git diff --check` passed.

Scope: mechanical presentation fixes only, existing palette and assets preserved. No content drafting, forms, analytics behavior, public deployment, or production merge. Review and merge PR #132 first, then retarget this companion PR to master and rerun diff/browser verification. Rollback is a revert of the eventual companion merge. Jeff's Article IV production approval remains required.
