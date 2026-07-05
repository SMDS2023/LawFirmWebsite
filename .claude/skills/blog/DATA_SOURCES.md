# Data Sources Registry

Every source the blog workflow can draw from, with the exact IDs needed to
query it. Verified working from a remote session on 2026-07-04.

## 1. Google Calendar (MCP: `mcp__Google_Calendar__*`)

The story engine. Hearings, motions, trials, consults — strip the details,
tell the story.

| Calendar | ID | Use |
|----------|----|-----|
| LLOJL (main law office) | `jeff@jlotterlaw.com` | Primary sweep — hearings, motions, consults. Event descriptions often carry case type, judge, posture, and Gmail links. |
| Lotter Law (firm) | `c_v38qea3tv75r1fhckmdr7tqd70@group.calendar.google.com` | Court dates, consults (often duplicates LLOJL as organizer). |
| AI Court Dates | `c_c065179d4189b0c973d541722ee3c2a5ff72350f4a8509b3f4541f3402e544cb@group.calendar.google.com` | Hearing dates auto-extracted from clerk emails. |
| Court Conditions Due | `c_cc55a345a420f270825c704cbcb9f90f886f06c7031fc40854bd79913a59ce2b@group.calendar.google.com` | Probation/pretrial condition deadlines — topic signals (interlock, DUI school, community service). |
| Blog Content Calendar | `c_a8af0e5310086df692ccedfe8156b05baae3c42a5fb298eef23facfc96a84df8@group.calendar.google.com` | Blog planning calendar — check for Jeff's own scheduled ideas; optionally write approved briefs back here. |
| Holidays in United States | `en.usa#holiday@group.v.calendar.google.com` | Seasonal hooks (July 4th DUI patrols, Labor Day, holiday DV spike). |
| Law Firm Admin | `c_a7f457f09beb643e2978ad669e70e5871c494120ffe1d2dce1ce7314e5550be5@group.calendar.google.com` | No-court dates; low value for ideation. |

**Excluded — personal, never sweep:** L&J Adventures, Client Birthdays,
National Junior Pickleball, and any event that is medical, family, or travel.

## 2. Gmail (MCP: `mcp__Gmail__*`)

Cross-reference layer: confirm how a story actually unfolded (offers made,
orders entered, continuances, discovery quirks) before asserting it in a post.

Useful query anchors: `from:sao9.org`, `from:sa18.org`, clerk domains
(`myorangeclerk`, `flcourts18`, `ninthcircuit`), `FLHSMV`, `formal review`,
`evidence.com`, `subject:"Notice"`. Calendar event descriptions frequently
embed direct `mail.google.com` thread links — follow those first.

**Rule:** email is verification material only. Never quote, never name, never
commit email content to the repo.

**Limit:** calendar + email still may not show how a matter resolved. Case
notes live in **Lawmatics** (CRM — no connector in this environment). When a
load-bearing fact can't be confirmed from email, ask Jeff at Gate 0 / Gate 1
instead of inferring.

## 3. Google Drive (MCP: `mcp__Google_Drive__*`)

| Document | File/Folder ID | What it proves |
|----------|----------------|----------------|
| Segment of Police Academy Manual (PDF) | `15ozvm1uKipvgnyToAsuy6T0CjVHOts_9` | How recruits are taught search & seizure 101 — stops, PC/RS, consent, pat-downs. |
| 2024 High Liability Instructor Guide (PDF) | `1TgIRV4QdlXfwQmHakaDC6Me5m6HGMIwZ` | Academy training on vehicle ops/pursuit, use of force — the standard officers are trained to. |
| OCSO Use of Force Policy (PDF) | `1WPEVN4APnBBn7bTGu4jnUBdKbI1m9ffY` | Agency UOF policy. |
| Towing_Vehicles OCSO (PDF) | `1tkqBIL40nQKgFQgxeCcHLdv8QLn3CMdE` | OCSO tow/inventory policy — inventory-search suppression angles. |
| OCSO folder | `1nUYly5Q6mVkpS15GI3ey3kLt5tbwpbjP` | Other collected OCSO orders. |
| Case-Law folder (recent) | `18vtG2U3dZZOUi_QFpTgtZr1YQmqn7OHn` | Downloaded opinion PDFs (Trujillo, Calvin, Harper, Lindsey, Rich, King, Jefferson, Love). |
| Case Law folder (older) | `1Bk5SA_WgRs95zn2981cuASVUoQXfR_Do` | More opinion PDFs. |
| DHSMV Case Law (PDF) | `1jxIMNXRFdqu8FG9NggunhLraY3Ou8m6U` | License/administrative-review case law compilation. |
| CASE_LAW_OWNER.md (Doc) | `1yeLv55KElWnw4mfQEPJhInwSEsgyYpo0Wdc5d1eNLMQ` | Case law library operating manual + hard rules. |

Large PDFs: `download_file_content` to the scratchpad, then read only the
pages you need.

## 4. Case Law Library (LegalAIntel)

- **Source of truth:** D1 database behind **app.legalaintel.com/case-law**
  (93 VERIFIED cases + 9 statutes across 21 topic categories — DUI, search &
  seizure, Stand Your Ground, Terry, Miranda, Brady/preservation, speedy
  trial, and more).
- **Repo mirror:** `SMDS2023/LegalAIntel` → `data/case-law/case_law_library.md`
  (reference backup with holdings, cites, links), plus saved opinion
  PDFs/HTML in the same directory. Jeff has approved adding this repo to any
  session via `add_repo` — do that at RESEARCH time and read the markdown
  mirror directly (when cloned: `/workspace/legalaintel/data/case-law/`).
- **Public PDFs:** `https://api.legalaintel.com/case-law/pdf/case-law/{filename}.pdf`
- **Fallbacks:** Drive case-law folders (§3) and approved public sources
  (Google Scholar, Florida Law Weekly, Justia, CourtListener).
- **HARD RULE:** only cite VERIFIED cases or opinions read this session.
  Otherwise `[CITE NEEDED]`.

## 5. Orange County Sheriff's Office public policy manual

OCSO publishes general and special orders (use of force, arrest procedures,
pursuit — GO 8.1.7, body-worn cameras, etc.) on ocso.com. Use WebSearch /
WebFetch to pull the current order text; prefer the Drive copies above when
they exist (they are the versions Jeff has vetted). Always record the GO
number and effective date you relied on.

## 6. Statutes

Florida Statutes via Online Sunshine (`leg.state.fl.us`). A local copy of
F.S. 322.03 sits at repo root. Cite as `F.S. §316.193` style, and link the
Online Sunshine page in posts where useful.

## 7. In-repo sources

| File | Use |
|------|-----|
| `.claude/knowledge/EDITORIAL-CALENDAR-2026.md` | Planned monthly topics + gap analysis. |
| `BLOG_IDEAS.md` | Idea backlog incl. Intoxilyzer 8000→9000 series (multi-part, ready). |
| `analytics/reports/` | GSC/GA4 weekly reports — ranking gaps, CTR opportunities. |
| `blog/*/index.html` | ~120-post corpus: style reference + duplicate check. |
| `.claude/knowledge/BRAND-GUIDE.md` | Voice, colors, imagery. |
| `blog/Speeding-Tickets-Orange-County-FL-Past-12-Months/`, `intox8000-data.json`, `officer-intel.html` | Original datasets — original-research angles. |

## 8. Image generation

| Item | Value |
|------|-------|
| xAI API | `https://api.x.ai/v1/images/generations`, model `grok-imagine-image` |
| Key | `XAI_API_KEY` env var (set in claude.ai/code environment settings — NEVER in this repo) |
| Network | `api.x.ai` must be in the environment's allowed domains; verify with a test call before relying on it |
| Known risks | Jeff's xAI account has auto-top-up OFF (402 on zero balance) and Tier 0 rate limits (429) — always fall back gracefully |
| Fallback | Local branded og card via headless Chromium + `templates/og-card-template.html` (see `enrich.md` §1) |

## 9. Draft storage (Google Drive)

| Item | Value |
|------|-------|
| Folder | **LotterLaw Blog Drafts** |
| Folder ID | `1B88L_n4ONjOP_VnOOmRRHj1vzxzxmdPq` |
| URL | https://drive.google.com/drive/folders/1B88L_n4ONjOP_VnOOmRRHj1vzxzxmdPq |

File naming: `<slug>.draft.html` (WRITE output) and `<slug>.enriched.html`
(ENRICH output). Drive files can't be edited in place through the connector —
every revision is a new upload, and `BLOG_PIPELINE.md` records the current
file ID. Drafts never enter the git repo.

## Cross-reference requirement

A topic brief is only viable when the story can be anchored to **at least two
independent authority sources** from: academy manual, OCSO policy, verified
case law, statute text, or Lotter Law original data. One source makes a blog
post; two make an argument nobody else in the market can write.
