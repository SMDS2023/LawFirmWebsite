---
name: blog
description: >
  End-to-end Lotter Law blog workflow: multi-source topic ideation (calendar,
  email, police academy manual, OCSO policy manual, verified case law library),
  research, writing, enrichment, staging, publishing, and distribution.
  Invoke for any blog request: /blog, /blog ideate, /blog write, /blog enrich,
  /blog stage, /blog golive, /blog facebook, /blog gmb, /blog status.
---

# Lotter Law Blog Workflow

The pipeline that turns what actually happens in Jeff's practice into
authoritative, SEO-strong blog posts. Every post cross-references real
authority sources so it says something no competitor can copy.

## Pipeline

```
IDEATE → RESEARCH → WRITE → [GATE 1: Jeff approves draft]
       → ENRICH → [GATE 2: Jeff approves enriched post]
       → STAGE → GOLIVE → DISTRIBUTE (facebook / gmb)
```

Stage instructions live in this directory:

| Stage | File | Output |
|-------|------|--------|
| Ideate | `ideate.md` | Story briefs appended to `BLOG_PIPELINE.md` |
| Research | `research.md` | Source Pack added to the brief |
| Write | `write.md` | `<slug>.draft.html` in the Drive drafts folder |
| Enrich | `enrich.md` | `<slug>.enriched.html` in the Drive drafts folder |
| Stage / Go-live | `publish.md` | Post at `blog/<slug>/`, listing + sitemap |
| Distribute | `facebook.md`, `gmb.md` | Copy-paste drafts for Jeff |

**Draft storage is Google Drive, not the repo** — folder "LotterLaw Blog
Drafts" (`DATA_SOURCES.md` §8). Drafts stay private until STAGE moves the
final HTML into `blog/<slug>/index.html`. The Drive connector cannot edit
files in place, so each revision is a fresh upload and `BLOG_PIPELINE.md`
records the **current** file ID — the ID in the pipeline is always the live
version.

Source registry (calendar IDs, Drive file IDs, case law library, OCSO,
academy manual): `DATA_SOURCES.md`. Read it before IDEATE or RESEARCH.

## Step 0 — Validate state (always, before anything else)

1. Read `BLOG_PIPELINE.md` (repo root). It is the single source of truth for
   what is proposed, drafted, approved, staged, or live — including the Drive
   file ID of every active draft.
2. Check slugs in the pipeline against `blog/` for collisions. A slug that
   already exists under `blog/` is taken — pick a new one.
3. Confirm you are on a feature branch (`claude/...`), never `master`.
4. If a pipeline entry says `awaiting-gate-1` or `awaiting-gate-2`, do not
   advance it without Jeff's explicit approval in this conversation.

## The two approval gates (hard rules)

- **Gate 1 (raw draft):** present the draft per `write.md` § "Gate 1 review".
  Jeff advances it by saying **"Enrich"** (or requests edits / cancels).
- **Gate 2 (enriched):** present per `enrich.md` § "Gate 2 review". Jeff
  chooses **Stage**, **Publish Now**, edits, back to draft, or cancel.
- Never skip a gate, even if Jeff's original request said "publish a post
  about X" — the gates are the point of the workflow.

## Privacy & anonymization (non-negotiable, applies at EVERY stage)

This repo is public. Calendar, Gmail, and case files are raw material —
their details never appear in any committed file or published post.

- **Never** include client names, opposing-party names, case numbers,
  citation numbers, phone numbers, email addresses, or exact hearing dates.
- Dates become month/season level ("this June", "recently").
- People become roles ("my client", "a driver in Orange County", "the ASA").
- Courts/counties may be named (Orange, Seminole, Osceola) — that is the
  local-SEO value — but never in combination with details that identify a case.
- Gmail is for *verifying how things actually worked*, never for quoting.
- Case-result posts require Jeff to confirm the client consented or the
  details are altered beyond recognition.

## Legal citation rule (from the Case Law Library operating manual)

**Never cite case law from training data.** Only cite cases verified in the
LegalAIntel case law library (see `DATA_SOURCES.md`) or read directly from a
source document this session (Drive PDF, Google Scholar, Justia,
CourtListener, Online Sunshine for statutes). If a proposition needs a case
you can't verify, write `[CITE NEEDED]` and flag it at the gate review.

## Git rules

- All work on a feature branch; merge to `master` via PR (protected).
- Direct push only if Jeff explicitly approves it in the conversation.
- Drafts are **never committed to the repo** — they live in the Drive drafts
  folder until STAGE writes the final post to `blog/<slug>/index.html`.

## Environment notes

- **Remote (claude.ai/code) sessions** have MCP connectors for Google
  Calendar, Gmail, and Drive — the full pipeline runs here.
- **Local sessions** without those connectors: skip live calendar/email
  sweeps and work from `BLOG_PIPELINE.md`, `BLOG_IDEAS.md`, and
  `.claude/knowledge/EDITORIAL-CALENDAR-2026.md`; drafts can be written
  locally but must reach the Drive drafts folder (Jeff uploads, or hand off
  to a remote session) before the pipeline advances. Say which sources were
  unavailable.
- **Case law library**: if `smds2023/legalaintel` isn't already in the
  session, ask Jeff to add it (`add_repo`) — he has approved this. The
  library markdown is `data/case-law/case_law_library.md` in that repo.
- The legacy Mac-only skill (`~/.claude/skills/blog/`) and Python generators
  (`scripts/blog_topic_generator.py`) are superseded by this workflow.

## Style corpus

The ~120 posts under `blog/*/index.html` are the style reference library.
Exemplars of the cross-reference formula this workflow exists to produce:

- `blog/fleeing-eluding-pursuit-policy-florida/` — statute + OCSO GO 8.1.7 +
  academy High Liability training in one argument.
- `blog/corpus-delicti-authority-vs-evidence-dui-trial/` — case story +
  doctrine.
- `blog/intoxilyzer-8000-data-analysis/` — original data as authority.

Match their voice: practitioner speaking plainly, concrete details, short
declarative sentences, no filler ("In today's fast-paced world...") and no
generic explainer framing ("If you've been charged with X in Florida...").
