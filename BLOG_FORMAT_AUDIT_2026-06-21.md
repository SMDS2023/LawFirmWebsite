# Blog Post Formatting Audit — 2026-06-21

**Scope:** All 123 real blog posts under `LotterLaw/Website/blog/*/index.html`
(plus 3 redirect stubs, excluded). Diagnosis only — **no files were changed.**

**Why the posts look different:** they were built across two main template
generations plus a handful of one-off custom layouts. The shared header, nav,
and breadcrumb are consistent everywhere; the divergence is in the **page
background, content wrapper, and column width.**

---

## How to read this

Each post was fingerprinted on 6 markers:

| Marker | What it controls | "Standard" value |
|--------|------------------|------------------|
| `body_bg` | Page background color | `bg-gray-50` (light gray) |
| `font_sans` | Generation tell only — **no visual effect** (`styles.css` forces Inter on `body` globally) | either |
| `prose` | Tailwind typography wrapper (paragraph/heading/list spacing) | `yes` |
| `maxw` | Article column width | `max-w-4xl` |
| `hero` | Opens with a hero image | content choice, not a bug |
| `cat_chip` | Links to a `/category/` page | Gen-1 only |

---

## The two generations (clean split on `font_sans`)

- **Gen 1 — older (mostly 2025):** `font_sans=no`, links to `/category/`
  pages, column width varies (3xl / 4xl / 5xl), hero images rare.
- **Gen 2 — newer (mostly 2026):** `font_sans=yes`, no category links,
  column width standardized on `max-w-4xl`, hero images common.

This split is *mostly cosmetically harmless* (the font renders identically).
The visible problems are the three groups below.

---

## PRIORITY 1 — White-background posts (6)

These render visibly brighter than the other 117. They are the location/service
cluster. **Lowest-risk fix:** change `bg-white` → `bg-gray-50` on `<body>`.

| Post | Published |
|------|-----------|
| `dui-lawyer-orange-county-florida` | 2026-02-06 |
| `dui-lawyer-kissimmee-osceola-county` | 2026-02-07 |
| `dui-attorney-seminole-county-sanford` | 2026-02-08 |
| `dui-defense-brevard-county` | 2026-02-09 |
| `orlando-dui-lawyer-local-experience` | 2026-01-22 |
| `restitution-evidence-florida` | 2026-01-17 |

---

## PRIORITY 2 — Custom layouts with no `prose` wrapper (4 + 1 hub)

These don't use the standard typography wrapper, so paragraph spacing,
headings, and lists read noticeably differently. Each needs individual review
(not a find-and-replace).

| Post | Published | Note |
|------|-----------|------|
| `florida-stand-your-ground-law` | 2026-01-14 | Slide-deck / infographic layout (12 slide images) — most divergent of all |
| `corpus-delicti-authority-vs-evidence-dui-trial` | 2026-01-12 | Hand-built columns (3xl + 4xl) |
| `dui-dwi-defense-florida-guide` | 2026-01-11 | Pillar/guide layout, no prose |
| `trial-ready-dui-metabolites-brevard` | 2026-01-28 | Custom "trial week" feature blocks |
| `start-here` | — | Hub/index page (not a true article) — leave as-is unless desired |

---

## PRIORITY 3 — Column-width outliers

Standard is `max-w-4xl`. These deviate on their **main text column** (single
non-4xl value), so the text measure looks wider or narrower than neighbors.
*(Posts with mixed widths — e.g. a full-width hero above a 4xl body — are
normal and not listed here.)*

**Narrower than standard (`max-w-3xl` only):**
- `Case-Analysis-01-fellow-officer-rule`
- `challenging-hgn-eye-test-dui`
- `refuse-sfst`

**Wider than standard (`max-w-5xl` only):**
- `intoxilyzer-8000-data-analysis`
- `intoxilyzer-8000-florida-history`
- `intoxilyzer-9000-florida-transition`
- `nta-citation-vs-traffic-ticket-florida`
- `repple-breath-test-jurisdiction`
- `toll-violations-orlando-florida`
- `traffic-stop-rights-florida`
- `trump-marijuana-reschedule-florida`

---

## Redirect stubs (not posts — exclude)

`domestic-violence-defense-guide`, `dui-defense-guide`, `theft-defense-guide`
are meta-refresh redirects to `/practice-areas/` pages. No formatting work needed.

---

## Recommended standardization order

1. **P1 white-bg → gray-50** (6 posts) — 1-line edit each, zero content risk.
2. **P3 width normalization** (11 posts) — change main column to `max-w-4xl`.
3. **P2 custom layouts** (4 posts) — case-by-case rebuild into the prose template.
4. *(Optional)* Decide a house rule on hero images so future posts are consistent.

---

## Full per-post inventory

`bg` = background · `fs` = font-sans (cosmetic only) · `prose` = typography wrapper ·
`maxw` = column width(s) · `hero` = hero image · `cat` = category-page link

| Post | bg | fs | prose | maxw | hero | cat | date | tel |
|------|----|----|-------|------|------|-----|------|-----|
| aggravated-assault-florida | gray-50 | yes | yes | 4xl | - | - | 2026-02-05 | 3 |
| ai-criminal-defense-judicial-system | gray-50 | yes | yes | 4xl | y | - | 2026-02-20 | 3 |
| ai-dui-trial-preparation-orlando | gray-50 | yes | yes | 4xl | - | - | 2026-01-23 | 3 |
| ai-police-reports-axon-draft-one | gray-50 | yes | yes | 4xl | y | - | 2026-02-26 | 2 |
| battery-charges-florida-degrees-defenses | gray-50 | yes | yes | 3xl,4xl | y | - | 2026-01-26 | 3 |
| battery-enhancement-factors-florida | gray-50 | yes | yes | 4xl | y | - | 2026-02-10 | 3 |
| booking-photos-mugshot-removal | gray-50 | yes | yes | 4xl | y | - | 2026-02-16 | 2 |
| can-ai-testify-against-you | gray-50 | no | yes | 4xl | - | y | 2025-12-12 | 5 |
| can-dui-be-dismissed-florida | gray-50 | yes | yes | 4xl | - | - | 2026-02-12 | 3 |
| cannabis-odor-probable-cause-florida | gray-50 | yes | yes | 4xl | y | - | 2026-01-16 | 4 |
| careless-driving-chain-reaction-not-guilty | gray-50 | no | yes | 4xl | - | y | 2025-12-05 | 5 |
| Case-Analysis-01-fellow-officer-rule | gray-50 | no | yes | **3xl** | - | y | 2025-12-12 | 4 |
| challenging-hgn-eye-test-dui | gray-50 | no | yes | **3xl** | - | y | 2025-11-12 | 3 |
| consent-search-dog-alert-attic | gray-50 | yes | yes | 4xl | - | - | 2026-02-03 | 3 |
| constructive-possession-drugs-car-dismissed | gray-50 | yes | yes | 4xl | - | - | 2026-01-09 | 4 |
| container-weight-drug-charges-florida | gray-50 | yes | yes | 4xl | - | - | 2026-01-10 | 4 |
| corpus-delicti-authority-vs-evidence-dui-trial | gray-50 | no | **NO** | 3xl,4xl | - | y | 2026-01-12 | 5 |
| crash-trauma-dui-reasonable-doubt | gray-50 | yes | yes | 4xl | y | - | 2026-02-15 | 3 |
| criminal-intent-florida-mens-rea | gray-50 | yes | yes | 4xl | y | - | 2026-02-17 | 2 |
| criminal-punishment-scoresheet-florida | gray-50 | yes | yes | 2xl,4xl | y | - | 2026-01-19 | 4 |
| data-driven-defense | gray-50 | no | yes | 3xl,4xl | y | y | 2025-05-17 | 4 |
| data-driven-defense-weekly-court-filings | gray-50 | yes | yes | 4xl | - | - | 2026-01-06 | 4 |
| deputy-sheriff | gray-50 | no | yes | 4xl | - | y | 2025-12-12 | 4 |
| dhsmv-formal-review-wrong-box-refusal | gray-50 | yes | yes | 2xl,4xl | - | - | 2026-06-15 | 2 |
| discovery-delays-ongoing-investigation | gray-50 | no | yes | 4xl | - | y | 2025-12-06 | 5 |
| disorderly-conduct-intoxication-defense | gray-50 | yes | yes | 4xl | - | - | 2026-01-13 | 4 |
| domestic-violence-no-bond-pretrial-release | gray-50 | no | yes | 3xl,4xl,5xl | - | y | 2025-11-25 | 6 |
| driverless-cars-no-steering-wheel-florida | gray-50 | yes | yes | 4xl | - | - | 2026-02-23 | 3 |
| drug-paraphernalia-charges-florida | gray-50 | yes | yes | 4xl | y | - | 2026-02-11 | 2 |
| dui-attorney-seminole-county-sanford | **white** | yes | yes | 4xl | - | - | 2026-02-08 | 4 |
| dui-checkpoint-rights-florida | gray-50 | yes | yes | 4xl | - | - | 2026-02-01 | 4 |
| dui-defense-brevard-county | **white** | yes | yes | 4xl | - | - | 2026-02-09 | 4 |
| dui-dwi-defense-florida-guide | gray-50 | no | **NO** | 4xl | - | - | 2026-01-11 | 5 |
| dui-lawyer-cost-orlando | gray-50 | yes | yes | 4xl | - | - | 2026-02-11 | 3 |
| dui-lawyer-kissimmee-osceola-county | **white** | yes | yes | 4xl | - | - | 2026-02-07 | 4 |
| dui-lawyer-orange-county-florida | **white** | yes | yes | 4xl | - | - | 2026-02-06 | 4 |
| dui-penalties-florida-fines-jail-license | gray-50 | yes | yes | 4xl | - | - | 2026-02-13 | 3 |
| dwlsr-vs-no-valid-license-florida | gray-50 | yes | yes | 4xl | - | - | 2026-01-27 | 4 |
| everyday-contact-battery-florida | gray-50 | yes | yes | 4xl | y | - | 2026-02-22 | 2 |
| eyewitness-identification-lineups-photo-arrays-florida | gray-50 | yes | yes | 4xl | y | - | 2026-02-05 | 3 |
| felon-possession-firearm-dismissed-terry-frisk | gray-50 | no | yes | 4xl | - | y | 2025-12-19 | 5 |
| firearm-carry-on-tsa-airport | gray-50 | no | yes | 4xl | - | y | 2025-11-26 | 6 |
| first-court-appearance-orlando | gray-50 | yes | yes | 4xl | y | - | 2026-02-09 | 3 |
| first-dui-florida-penalties | gray-50 | yes | yes | 4xl | - | - | 2026-02-10 | 3 |
| first-time-reckless-driving-florida | gray-50 | no | yes | 4xl | - | y | 2026-01-03 | 5 |
| first-traffic-court-hearing-florida | gray-50 | yes | yes | 4xl | - | - | 2026-01-21 | 4 |
| florida-dl-number-soundex-randomized | gray-50 | yes | yes | 4xl | y | - | 2026-01-31 | 3 |
| florida-laws-july-2025 | gray-50 | no | yes | 4xl | - | y | 2025-07-15 | 5 |
| florida-license-suspension-hto-administrative-review | gray-50 | no | yes | 4xl | - | - | 2026-02-12 | 4 |
| florida-privacy-rights-beyond-miranda | gray-50 | no | yes | 4xl | - | y | 2025-11-19 | 6 |
| florida-stand-your-ground-law | gray-50 | no | **NO** | 3xl,4xl | - | y | 2026-01-14 | 5 |
| Forensic-Video-Analysis | gray-50 | no | yes | 3xl,4xl | y | y | 2025-05-15 | 4 |
| fto-factor-rookie-tax | gray-50 | no | yes | 4xl | - | y | 2025-11-19 | 6 |
| hiring-attorney-tickets | gray-50 | no | yes | 4xl | - | y | 2025-08-08 | 5 |
| hit-and-run-corpus-delicti-defense | gray-50 | no | yes | 3xl,5xl | - | y | 2025-12-12 | 6 |
| hit-and-run-private-property-jurisdiction-dismissed | gray-50 | no | yes | 4xl | - | y | 2025-12-16 | 5 |
| holiday-domestic-violence-arrests | gray-50 | no | yes | 4xl,5xl | - | y | 2025-12-27 | 6 |
| hto-status-removed-vacating-dwls-conviction | gray-50 | no | yes | 4xl | - | y | 2025-12-08 | 5 |
| interlock-violation-kicked-from-diversion | gray-50 | no | yes | 3xl,4xl | - | y | 2025-05-19 | 3 |
| intoxilyzer-8000-data-analysis | gray-50 | no | yes | **5xl** | - | - | 2026-01-05 | 6 |
| intoxilyzer-8000-florida-history | gray-50 | no | yes | **5xl** | - | - | 2025-12-26 | 6 |
| intoxilyzer-9000-florida-transition | gray-50 | no | yes | **5xl** | - | - | 2026-01-08 | 6 |
| leave-scene-immigration-criminal-dropped | gray-50 | yes | yes | 4xl | - | - | 2026-01-29 | 4 |
| Legal-Data-Analysis | gray-50 | no | yes | 4xl | - | y | 2025-06-17 | 4 |
| lgops-decentralized-leadership | gray-50 | no | yes | 4xl | - | y | 2025-11-23 | 6 |
| license-plate-frames-florida-law | gray-50 | no | yes | 4xl | - | y | 2025-12-13 | 6 |
| mangione-backpack-search-arrest | gray-50 | yes | yes | 4xl | y | - | 2026-02-02 | 3 |
| marijuana-weapons-fss-790 | gray-50 | no | yes | 4xl | - | y | 2025-07-18 | 5 |
| medical-marijuana-original-packaging | gray-50 | no | yes | 4xl | - | y | 2025-11-17 | 5 |
| motion-to-suppress-what-to-expect | gray-50 | no | yes | 4xl | - | y | 2025-12-18 | 5 |
| multiple-toll-violations | gray-50 | yes | yes | 4xl | - | - | 2026-01-07 | 4 |
| new-dui-refusal-law | gray-50 | no | yes | 4xl | - | y | 2025-08-21 | 5 |
| news-13-super-speeder-interview | gray-50 | no | yes | 4xl | - | y | 2025-12-20 | 5 |
| new-year-clear-your-record-2026 | gray-50 | no | yes | 4xl | y | y | 2026-01-02 | 5 |
| no-jurisdiction-for-crash-investigation | gray-50 | no | yes | 4xl | y | y | 2025-12-12 | 4 |
| nta-citation-vs-traffic-ticket-florida | gray-50 | no | yes | **5xl** | - | y | 2025-12-21 | 6 |
| nvdl-mandatory-minimum-immigration-enforcement | gray-50 | no | yes | 4xl | - | y | 2025-12-04 | 5 |
| officer-jason-raynor-act-resisting-arrest | gray-50 | yes | yes | 4xl | y | - | 2026-02-04 | 3 |
| orange-county-court-data-15000-records | gray-50 | yes | yes | 4xl | - | - | 2026-03-30 | 3 |
| orlando-dui-lawyer-local-experience | **white** | yes | yes | 4xl | y | - | 2026-01-22 | 3 |
| orlando-weekly-arrest-breakdown-january-26-february-2-2026 | gray-50 | yes | yes | 4xl | - | - | 2026-02-06 | 3 |
| pre-trial-motions | gray-50 | no | yes | 4xl | - | y | 2025-12-12 | 4 |
| pretrial-release-violation-hb397-florida | gray-50 | yes | yes | 4xl | y | - | 2026-03-20 | 2 |
| refuse-sfst | gray-50 | no | yes | **3xl** | y | y | 2025-05-11 | 4 |
| repple-breath-test-jurisdiction | gray-50 | no | yes | **5xl** | - | - | 2025-12-31 | 6 |
| resisting-arrest-unlawful-arrest-defense | gray-50 | yes | yes | 4xl | - | - | 2026-01-15 | 4 |
| restitution-evidence-florida | **white** | yes | yes | 4xl | y | - | 2026-01-17 | 4 |
| retail-theft-five-year-statute-limitations | gray-50 | no | yes | 4xl,5xl | - | y | 2025-12-12 | 6 |
| return-stolen-property-charges-dropped | gray-50 | yes | yes | 4xl | - | - | 2026-02-24 | 3 |
| richardson-hearing-super-speeder-evidence-excluded | gray-50 | no | yes | 4xl | - | y | 2025-12-15 | 5 |
| sanford-police-fraud-accountability | gray-50 | no | yes | 4xl | - | y | 2025-12-17 | 5 |
| sealing-expunging-criminal-records | gray-50 | no | yes | 2xl,4xl,5xl | - | y | 2025-12-12 | 6 |
| sealing-expunging-vs-private-databases | gray-50 | yes | yes | 4xl | y | - | 2026-02-12 | 2 |
| seal-misdemeanor-conviction-hb745-florida | gray-50 | yes | yes | 4xl | y | - | 2026-03-16 | 2 |
| securely-encased-concealed-carry-dismissed | gray-50 | no | yes | 4xl | - | y | 2025-12-01 | 5 |
| securely-encased-vs-concealed | gray-50 | no | yes | 4xl | - | y | 2025-08-11 | 4 |
| simple-battery-florida-charges | gray-50 | yes | yes | 4xl | - | - | 2026-02-14 | 4 |
| single-incident-dv-injunction-sb32-florida | gray-50 | yes | yes | 4xl | y | - | 2026-03-18 | 2 |
| speeding-tickets-75-year-trap | gray-50 | no | yes | 4xl | - | y | 2025-01-29 | 5 |
| Speeding-Tickets-Orange-County-FL-Past-12-Months | gray-50 | no | yes | 4xl | - | y | 2025-01-30 | 5 |
| stand-your-ground-case-dropped-florida | gray-50 | yes | yes | 2xl,4xl | y | - | 2026-06-26 | 3 |
| stand-your-ground-florida-self-defense | gray-50 | yes | yes | 2xl,4xl | y | - | 2026-01-04 | 4 |
| stand-your-ground-motion-dismiss-vs-c4 | gray-50 | yes | yes | 4xl | - | - | 2026-01-24 | 3 |
| start-here | gray-50 | no | **NO** | 2xl,4xl | - | y | — | 4 |
| state-trooper | gray-50 | no | yes | 4xl | - | y | 2025-12-12 | 4 |
| st-patricks-day-dui-florida | gray-50 | yes | yes | 4xl | - | - | 2026-03-14 | 2 |
| super-bowl-dui-florida | gray-50 | yes | yes | 4xl | - | - | 2026-01-30 | 4 |
| super-bowl-sunday-enforcement-tactics | gray-50 | yes | yes | 4xl | y | - | 2026-02-07 | 3 |
| super-speeder-radar-foundation-dismissed | gray-50 | no | yes | 4xl | - | y | 2025-12-03 | 5 |
| tell-employer-about-arrest | gray-50 | yes | yes | 4xl | y | - | 2026-02-08 | 3 |
| thanksgiving-burglary-dismissal | gray-50 | no | yes | 4xl | - | y | 2025-12-02 | 5 |
| toll-violations-florida | gray-50 | yes | yes | 4xl | - | - | 2026-01-25 | 4 |
| toll-violations-orlando-florida | gray-50 | no | yes | **5xl** | - | - | 2025-12-24 | 6 |
| traffic-stop-rights-florida | gray-50 | no | yes | **5xl** | - | y | 2025-12-22 | 6 |
| trial-ready-dui-metabolites-brevard | gray-50 | yes | **NO** | 4xl | y | - | 2026-01-28 | 4 |
| trump-marijuana-reschedule-florida | gray-50 | no | yes | **5xl** | - | - | 2025-12-23 | 6 |
| understanding-probable-cause | gray-50 | no | yes | 3xl,4xl | y | y | 2025-05-13 | 3 |
| uscca-critical-response-attorney-orlando | gray-50 | yes | yes | 2xl,4xl | y | - | 2026-06-19 | 3 |
| valencia-police-academy | gray-50 | no | yes | 4xl | - | y | 2025-12-12 | 4 |
| veteran | gray-50 | no | yes | 4xl | - | y | 2025-12-12 | 4 |
| veterans-treatment-court-orlando | gray-50 | no | yes | 4xl | - | y | 2025-11-11 | 8 |
| withhold-wildcard-drug-offender-probation | gray-50 | yes | yes | 4xl | - | - | 2026-01-18 | 4 |
| withhold-wisdom-prior-withholds-not-convictions | gray-50 | yes | yes | 4xl | - | - | 2026-01-20 | 4 |

**Redirect stubs (excluded):** domestic-violence-defense-guide · dui-defense-guide · theft-defense-guide
