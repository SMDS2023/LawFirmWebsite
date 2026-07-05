# Blog Pipeline State

> Single source of truth for the blog workflow (`.claude/skills/blog/SKILL.md`).
> Statuses: `proposed` → `story-confirmed` (Gate 0) → `researching` →
> `awaiting-gate-1` → `enriching` → `awaiting-gate-2` → `staged` → `live`
> (or `killed`).
> This file is public — everything here must already be anonymized.
>
> Draft HTML lives in the Drive folder
> ["LotterLaw Blog Drafts"](https://drive.google.com/drive/folders/1B88L_n4ONjOP_VnOOmRRHj1vzxzxmdPq)
> — each active entry below records the current draft's Drive file ID.

## Active drafts

### dui-pretrial-diversion-orange-county — awaiting-gate-1
- **Brief:** BRIEF-202607-02
- **Draft:** `dui-pretrial-diversion-orange-county.draft.html` · Drive ID
  `1MfG-22-fUvGImi1nhhIHT8sKsJBMcxQP` (uploaded 2026-07-05, 1,318 words)
- **Gate-1 open items for Jeff:** verify tier terms (lengths, costs, SCRAM
  scope/duration) against the served PTI contract; confirm "no seal/expunge
  for DUI conviction" phrasing is how he wants it stated.

## Proposed briefs

> Generated 2026-07-04 from a live sweep: law-office calendars (past ~6 weeks
> + next ~6 weeks), US holidays, editorial calendar, BLOG_IDEAS backlog,
> existing-post gap check. Awaiting Jeff's pick for RESEARCH.

### BRIEF-202607-01: What Actually Happens at a Stand Your Ground Hearing
- **Status:** killed (2026-07-04)
- **Kill reason:** Duplicate — the dedupe check missed three existing SYG
  posts (`stand-your-ground-motion-dismiss-vs-c4` already covers the
  immunity hearing; also `stand-your-ground-florida-self-defense`,
  `stand-your-ground-case-dropped-florida`). Jeff also flagged the brief's
  legal characterization of the hearing as wrong — reinforcing the rule that
  briefs never assert legal standards (see `ideate.md`).

### BRIEF-202607-02: The State Offered DUI Diversion. Should You Take It?
- **Status:** awaiting-gate-1 (drafted 2026-07-05 — see Active drafts)
- **The story (Jeff-confirmed, anonymized):** In late June, a client and I
  worked through a real decision: the State Attorney approved him for DUI
  pre-trial diversion (Tier 1, breath result under .15). The email looked
  like good news — but the answer depends on the tier. **Jeff's correction
  that reframes the post:** DUI diversion now requires **SCRAM (continuous
  alcohol monitoring) at Tier 2** — a device that is expensive, invasive,
  and prone to problems, which can make diversion an unacceptable option at
  that tier. The tier you're offered changes the answer.
- **Why now:** SAO9's tiered DUI PTI program is active and offers are
  arriving on real cases; nothing on the site explains the tiers, the SCRAM
  requirement, or the trade-offs.
- **Authority cross-refs (verify at research):** SAO9 DUI PTI program terms
  → tier structure, conditions, SCRAM requirement; SCRAM device
  documentation + reliability litigation → cost, false-positive record;
  F.S. §316.193 / §316.656 → verify how diversion differs from a plea and
  what minimums apply; existing posts
  `interlock-violation-kicked-from-diversion` (cautionary companion) and
  `dui-reduced-reckless-driving-florida`.
- **The hook:** "The State's email said my client was approved. Approved for
  what, exactly, is where the real decision started."
- **SEO:** "DUI diversion program Orange County" / "DUI PTI Florida" /
  "SCRAM device Florida DUI" · commercial-informational · gap: diversion
  mentioned in passing only.
- **CTA angle:** An offer is a fork in the road — the tier and its
  conditions decide whether to take it, and that's a lawyer's call.
- **Score:** S3 A2 T2 G2 = **9/10**

#### Source Pack (researched 2026-07-05)
- **Narrative timeline (anonymized, email-verified):** PTI referral
  requested mid-June → approved for DUI PTI Tier 1 (BAC < .15) about a week
  later → PTI contract served by the SAO at month's end → attorney-client
  decision call. Parallel matters this month show the program's
  administrative texture: contracts delivered via Dropbox, hard report-by
  deadlines to Community Corrections, payment by money order with receipt
  upload, extensions generally refused except near the program end date.
- **Authorities:**
  - F.S. §316.656(1) — no court may suspend, defer, or **withhold
    adjudication** for a §316.193 violation (DUI conviction = mandatory
    adjudication) · via flsenate.gov · proves why a diversion dismissal is
    uniquely valuable for DUI.
  - F.S. §316.656(2)(a) — no judge may accept a plea to a **lesser offense**
    where BAC ≥ .15 · same source · proves the .15 line cuts twice.
  - SAO9 DUI PTI program structure — Tier 1: BAC < .15 (per SAO approval
    language); Tier 2: refusal or ≥ .15; ~12 vs ~15 months, higher costs at
    Tier 2; **Jeff (Gate 0): Tier 2 now requires SCRAM/continuous alcohol
    monitoring — expensive, invasive, problem-prone.** `[VERIFY at Gate 1:
    tier terms against the served PTI contract — lengths, contributions,
    SCRAM scope/duration]`
  - SCRAM CAM manufacturer materials (scramsystems.com media FAQ) — setup
    $50–100, ~$10–12/day (~$300–360/month); transdermal sampling; defense
    commentary documents false-positive risk from environmental alcohol
    (sanitizers, lotions, gasoline) · proves cost + reliability argument.
- **Defense theory / thesis:** Diversion's value is the dismissal (the only
  clean exit §316.656 leaves open), but the tier decides the price — Tier 2's
  SCRAM requirement can make 15 months of diversion costlier and riskier
  than defending the case; and even Tier 1 is an unforgiving compliance
  gauntlet where one administrative slip puts you back on the trial docket.
- **Internal links:** pillar `dui-dwi-defense-florida-guide`; supporting
  `interlock-violation-kicked-from-diversion`,
  `can-dui-be-dismissed-florida`, `first-dui-florida-penalties`; practice
  `practice-areas/dui.html` + contact CTA.
- **Open items:** tier terms vs. served contract (Jeff, Gate 1); SCRAM
  duration within Tier 2 (Jeff, Gate 1).

### BRIEF-202607-03: The Other DUI Trial: Your DHSMV Formal Review
- **Status:** story-confirmed (Gate 0 · 2026-07-05). Jeff: do a **deep dive
  into the whole formal-review process** — dual purpose: the blog post AND a
  process map that helps rework the firm's own systems for these hearings.
  Research output should include an internal-facing process outline, not
  just post material.
- **The story (anonymized):** This spring and summer I've handled a run of
  DHSMV formal review hearings — the administrative fight over your license
  that starts a 10-day clock the night of a DUI arrest and finishes long
  before criminal court. Final orders, subpoenaed officers, continuances:
  it's a full contested hearing most defendants never see coming.
- **Why now:** Multiple formal reviews on the docket recently; the existing
  post covers one narrow win (wrong box checked), not the process.
- **Authority cross-refs:** F.S. §322.2615 (formal review procedure,
  10-day rule, scope) → the process; "DHSMV Case Law" compilation (Drive) →
  what hearing officers must find and how orders get invalidated; existing
  posts `dhsmv-formal-review-wrong-box-refusal` and
  `florida-license-suspension-hto-administrative-review` (links).
- **The hook:** "Ten days. That's how long you have after a DUI arrest to
  demand the hearing most people never find out existed."
- **SEO:** "DHSMV formal review hearing" · informational-commercial · gap:
  process post missing; two adjacent posts to interlink.
- **CTA angle:** The license fight starts now, not at arraignment.
- **Score:** S3 A3 T1 G2 = **9/10**

### BRIEF-202607-04: How the State Actually Shares the Evidence Against You
- **Status:** story-confirmed (Gate 0 · 2026-07-05, angle broadened by Jeff)
- **The story (Jeff-confirmed, anonymized):** In a pending misdemeanor, the
  State's digital evidence — body-cam video, a 911 call — arrived as an
  Evidence.com link with an expiration date. **Jeff's reframe:** make the
  post an explainer of the three systems through which the State shares
  video and document evidence — **Axon Evidence.com** (agency video/audio,
  expiring share links), the **Clerk's eFiling portal** (court filings), and
  **CIS** (the State Attorney's discovery/case system) — how each works,
  what lives where, and where evidence can quietly slip away.
- **Why now:** Live issue in current caseload; pairs with the site's Axon
  Draft One post while AI-generated police reports are in the news.
- **Authority cross-refs (verify at research):** Axon Evidence.com
  sharing/retention documentation → how links and expirations work; Florida
  eFiling portal / Ninth Circuit clerk documentation → what defendants can
  see; SAO discovery-portal practice → how discovery is transmitted; case
  law library "Brady / Evidence Preservation" category (VERIFIED) → what
  happens legally when evidence disappears; existing post
  `ai-police-reports-axon-draft-one` (link).
- **The hook:** "The State's best evidence against my client came with an
  expiration date — and the countdown was already running."
- **SEO:** "how to get police body cam footage Florida" / "evidence.com
  link expired" / "criminal discovery Florida" · informational, low
  competition · gap: nothing on the discovery systems themselves.
- **CTA angle:** Deadlines in a case aren't just court dates — hire counsel
  who knows the systems and preserves the record before it evaporates.
- **Score:** S3 A2 T2 G2 = **9/10**

### BRIEF-202607-05: School Zones Are Back — and So Are the Cameras
- **Status:** story-confirmed (Gate 0 · 2026-07-05, scope broadened by
  Jeff): cover the back-to-school enforcement cluster — school-zone
  speeding AND texting-while-driving (hand-held ban in school zones),
  passing a stopped school bus, and related school-zone offenses. Anchor
  story remains the pending Orange County school-zone speeding hearing
  (scheduled August; not yet held — no outcome claims).
- **The story (anonymized):** I have a school-zone speeding case set for
  hearing in Orange County traffic court in early August — right as Central
  Florida schools reopen and the school-zone speed cameras and stepped-up
  enforcement come back online. Doubled fines, camera citations, and the
  new super-speeder regime make August the most expensive month to be heavy
  on the pedal.
- **Why now:** Back-to-school (Orange County resumes mid-August);
  seasonal search spike for school zone tickets.
- **Authority cross-refs:** Florida's school-zone speed detection statute
  and doubled-fine provisions `[CITE NEEDED — pin at research]` → how camera
  citations differ from officer citations (and their defenses); Lotter Law
  original data `Speeding-Tickets-Orange-County-FL-Past-12-Months` →
  where enforcement concentrates; existing posts
  `news-13-super-speeder-interview` and `first-traffic-court-hearing-florida`
  (links).
- **The hook:** "The most expensive quarter-mile in Orlando is about to turn
  back on."
- **SEO:** "school zone speeding ticket Florida" / "school zone camera
  ticket" · informational, strongly seasonal · gap: not covered.
- **CTA angle:** Camera tickets look automatic; they're not — options before
  you just pay.
- **Score:** S2 A2 T2 G2 = **8/10**

## Dedupe notes from this sweep

- July 4th DUI enforcement → covered (`july-4th-dui-enforcement-florida`); skip.
- Holiday DV arrests → covered (`holiday-domestic-violence-arrests`); revisit in November.
- Toll-court matters on the docket → covered (`multiple-toll-violations`, toll posts); no new angle found this sweep.
- Intoxilyzer 8000→9000 series (BLOG_IDEAS.md) → still "ready to go"; multi-part, needs its own scheduling decision rather than a sweep slot.

## Recently completed

*(workflow initialized 2026-07-04 — history starts here)*
