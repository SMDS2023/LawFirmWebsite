# LOJ-472 broken-link report

Audit date: 2026-09-01  
Scope: live `https://lotterlaw.com` plus this branch’s HTML.  
Seeds: live `sitemap.xml` (200 this run; earlier 500 not reproduced) + homepage/nav, `blog.html`, all EN/ES practice-area pages.  
Checks: internal `href`/`src` plus outbound `legalaintel.com`, `fdle.state.fl.us`, and `lotterblotter.com`.  
Repo pass: 4,161 internal `<a href>` values in published HTML resolve to a file in this tree.

## Confirmed 404 / dead hosts (live, before this PR)

| Source | Target | Status | This PR |
|---|---|---|---|
| `/practice-areas/dui.html` | `https://legalaintel.com/intox8000_Anomalies/` | 404 (GitHub Pages “Site not found”) | Retarget → `/intox8000-anomalies.html` |
| `/es/practice-areas/dui.html` | `https://legalaintel.com/intox8000_Anomalies/` | 404 | Same |
| `/blog/intoxilyzer-8000-data-analysis/` | `https://legalaintel.com/intox8000_Anomalies/` (CTA + sources) | 404 | Same |
| `/blog/orlando-weekly-arrest-breakdown-january-26-february-2-2026/` | `https://legalaintel.com/dashboard.html?v=6` (iframe) | 404 | Replace embed with Lotter Blotter link |
| (direct) | `https://lotterlaw.com/intox8000-anomalies.html` | 404 on live today | Restored in this PR (not deployed yet) |
| (direct) | `https://lotterlaw.com/intox8000_Anomalies/` | 404 on live today | Alias redirect added |
| (direct / old nav) | `https://lotterlaw.com/contact.html` | 404 | `404.html` now maps `/contact.html` → `/#contact` |

`legalaintel.com` itself is a dead GitHub Pages host. No working Intox lookup URL remains on that domain.

## Outbound that is live

| Target | Status |
|---|---|
| `https://www.fdle.state.fl.us/alcohol-testing-program` | 200 |
| `https://www.fdle.state.fl.us/alcohol-testing-program/intoxilyzer-8000-records` | 200 |
| `https://www.fdle.state.fl.us/Alcohol-Testing-Program/Intoxilyzer-8000-Records` | 200 |
| `https://www.fdle.state.fl.us/alcohol-testing-program/breath-testing-home/curriculum` | 200 |
| Intox 9000 curriculum PDF on FDLE | 200 |
| Five sampled `fdle_url` values from `intox8000-data.json` | 200 |
| `https://lotterlaw.com/intox8000-data.json` | 200 (already live) |
| `https://lotterlaw.com/sitemap.xml` | 200 (HEAD/GET this run) |

`lotterblotter.com` returned 429 to this crawler (rate limit). Same host is already linked from `/blog/orange-county-july-4-court-data/` and is the documented court-dashboard home. Not treated as a 404.

## False positives (not 404s)

These asset URLs contain spaces. The crawler rejected the raw string; browsers percent-encode and the files return 200:

- `/assets/Case Statistics.webp`
- `/assets/FHP 300400.webp`
- `/assets/FL vs. GWOREK County Court Brevard County_ 18 Fla. L. Weekly Supp. 543a.pdf`
- `/assets/Hero Police_In_rear_view_Mirror.png`
- `/assets/McDaniels v State.pdf`
- `/assets/Medical Marijuana.jpg`
- `/assets/Radar Mind Map.png`
- `/assets/Recruit and FTO.jpg`
- `/assets/Seal and Expunge_Arrested.jpg`
- `/assets/Seal and Expunge_Job_Interview.jpg`

`/assets/blog/asleep-behind-wheel-actual-physical-control-florida-hero.jpg` returned 503 once, then 200 on retry.

## Safe internal 404s fixed here

- Dead Intox CTAs → live tool path (see above)
- `/intox8000_Anomalies/` alias
- `/contact.html` 404 map
- Weekly-arrest iframe (dead host) → Lotter Blotter

No other missing internal page hrefs in the published HTML tree.

## Follow-up (not this PR)

1. **LegalAIntel host** — `SMDS2023/LegalAIntel` still exists, but `legalaintel.com` GitHub Pages is down. The public lookup is restored on lotterlaw.com. The fuller SaaS/dashboard (and `dashboard.html`) is a separate restore if that product is still wanted.
2. **Data refresh** — `intox8000-data.json` `generated` is 2025-12-26 (1,932 anomaly records / 393 machines). FDLE refresh pipeline lives outside this repo.
3. **Certified PDFs** — later tool revisions showed a Certified column; current JSON has no `certified_url` values, so that column is omitted.
4. **Asset filenames with spaces** — live, but brittle for some clients. Rename+redirect later if anyone wants cleanup.

No client names in this report.
