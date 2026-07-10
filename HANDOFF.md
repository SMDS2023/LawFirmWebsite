# Session Handoff — Blog Workflow Build + First Post

> Written 2026-07-06 by the session that built the blog workflow.
> **New session: start here.** Read this, then `BLOG_PIPELINE.md`, then
> `.claude/skills/blog/SKILL.md`.

## First actions for the new session

1. `git fetch origin claude/blog-generation-workflow-ydpkhl && git checkout claude/blog-generation-workflow-ydpkhl`
   — ALL work below lives on this branch, not master. No PR exists yet.
2. Read `BLOG_PIPELINE.md` (pipeline state) and `.claude/skills/blog/SKILL.md`
   (the workflow: IDEATE → Gate 0 → RESEARCH → WRITE → Gate 1 → ENRICH →
   Gate 2 → STAGE/GOLIVE → distribute).
3. Test whether Jeff's environment changes landed:
   `curl -s -o /dev/null -w "%{http_code}" https://api.x.ai/` and check for
   `XAI_API_KEY` env var. If both work, generate the pending hero image
   (see below). If not, don't relitigate it — the local og-card fallback
   already shipped.

## Where things stand

### The workflow (DONE, on this branch)
- Skill suite at `.claude/skills/blog/` — SKILL.md, ideate/research/write/
  enrich/publish/facebook/gmb + DATA_SOURCES.md (all source IDs: calendars,
  Drive files, case law library, xAI image API) + templates
  (post-template.html, og-card-template.html).
- `BLOG_PIPELINE.md` at repo root = single source of truth for post states.
- Drafts live in Google Drive folder **"LotterLaw Blog Drafts"**
  (`1B88L_n4ONjOP_VnOOmRRHj1vzxzxmdPq`) as `<slug>.draft.html` /
  `<slug>.enriched.html`. Never committed to the repo. Drive connector
  can't edit in place — every revision is a new upload; pipeline records
  the current file ID.
- Case law library: repo `SMDS2023/LegalAIntel` — **Jeff pre-approved
  `add_repo`**; library markdown at `data/case-law/case_law_library.md`
  (93 VERIFIED cases + 9 statutes). HARD RULE: never cite case law from
  training data; VERIFIED library or opinions read this session only,
  else `[CITE NEEDED]`.

### The first post (AT GATE 2 — awaiting Jeff's decision)
- `dui-pretrial-diversion-orange-county` — "DUI Diversion in Orange County:
  Why the Tier You're Offered Changes the Answer." ~1,330 words.
- Passed Gate 0 (story confirmed), Gate 1 (approved with corrections:
  SCRAM = six months at Tier 2; program starts at 12 months, terms change
  regularly; any adjudication kills seal/expunge eligibility forever), and
  enrichment (1-3-2 links done, schema done).
- Enriched file (deploy this): Drive ID `1448YGkhCUWJt1bTfrY4e8pkqKSTrd49E`.
- og image DONE and committed: `assets/blog/dui-pretrial-diversion-orange-county-og.jpg`
  (locally generated branded card). Hero image PENDING (photorealistic, via
  xAI once network opens; hero `<figure>` is commented out in the HTML).
- Back-links queued for GOLIVE: add links to this post from
  `interlock-violation-kicked-from-diversion` and
  `can-dui-be-dismissed-florida`.
- **Waiting on one word from Jeff: "Stage" (post live by URL, unlisted) or
  "Publish Now" (post + blog.html card + sitemap + back-links).** Mechanics
  in `.claude/skills/blog/publish.md`. Master is protected — push branch,
  open PR.

### Confirmed briefs queued next (see BLOG_PIPELINE.md for full briefs)
1. **BRIEF-202607-03 DHSMV formal review deep-dive** — Jeff wants BOTH a
   post and an internal process map to rework firm systems.
2. **BRIEF-202607-04 how the State shares evidence** — Axon Evidence.com
   expiring links + Clerk eFiling + CIS, systems explainer.
3. **BRIEF-202607-05 back-to-school enforcement cluster** — school-zone
   speeding + texting + school-bus passing; anchor hearing is early August,
   so publish early August.

## Jeff's environment to-dos (he may have done these — verify, don't assume)
- claude.ai/code → cloud icon → environment settings → **Network access:
  Custom + `api.x.ai`** (or Full) and **env var `XAI_API_KEY`**. Applies to
  new sessions only. Until then, all external image APIs are firewalled
  (Grok, Higgsfield, all of them — it's the sandbox policy, not the
  provider).
- xAI account risks (from Jeff's other rig): auto-top-up OFF (402 on zero
  balance), Tier 0 rate limits (429). The image ladder in `enrich.md` §1
  handles fallback — never stall the pipeline on image generation.

## Hard-won lessons (already encoded in the skill, but internalize them)
- **Gate 0 exists because a calendared event ≠ an event that happened** (an
  SYG hearing on the calendar never took place). Present your outline of the
  story; Jeff confirms/corrects before research.
- **Never assert legal standards in briefs** — research pins them to actual
  texts; Jeff corrected the SYG burden framing once already.
- **Dedupe against EVERY blog slug** (full `ls`, plus grep) — a truncated
  listing missed 3 of 4 stand-your-ground posts.
- Jeff's corrections are gold — bake them into the post, the pipeline
  entry, AND the skill rules.
- Lawmatics holds case notes (source of truth for how matters resolved). A
  Zapier connector with `lawmatics_*` tools appeared in this session —
  consider wiring it into Gate 0/research when available.

## Open threads (lower priority)
- Merge this branch: when Jeff is ready, open a draft PR for
  `claude/blog-generation-workflow-ydpkhl` → master.
- Facebook/GMB distribution for the diversion post after it goes live
  (`facebook.md`, `gmb.md`).
- The self-contained preview trick (inline Tailwind build + Chromium
  screenshot) is documented by example in this session; useful for showing
  Jeff any post before it ships.
