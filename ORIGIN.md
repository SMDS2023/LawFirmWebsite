# Origin — Lotter Law website and blog

This repo is the **GitHub origin** for lotterlaw.com. Work here. Stay here. Only put on `master` what should be live.

## This system

| | |
|---|---|
| What | Public firm site + published blog HTML |
| GitHub origin | `https://github.com/SMDS2023/LawFirmWebsite` (public) |
| Deploy branch | `master` → GitHub Pages → https://lotterlaw.com |
| Operating clone | `Documents/LotterLaw/Website` on the Windows laptop |
| How it goes live | Feature branch → PR → merge `master`. Do not merge until the change is ready to be public. |

Agents: branch off `master`, PR, stop. Do not commit from leftover `claude/` / `codex/` / `mailer-*` branches.

## Blog — four homes, not one pile

Chosen factory: **LangGraph** in GitHub `SMDS2023/blog-pipeline` (work in progress). The `/blog` skill on disk is transitional, not origin. OneDrive is a sync accident, not a home. Court-data R2 is not the blog.

| Stage | Home | On this origin? |
|---|---|---|
| Idea / queue | `blog-pipeline` when that system is ready; until then local files under `LotterLaw/Blog/` | No |
| Draft HTML, WIP images, research | Same — local until `blog-pipeline` owns them. Not this public repo. | No |
| Published HTML + live images | `LotterLaw/Website/blog/` then PR to `master` | Yes |
| Factory *code* | GitHub `SMDS2023/blog-pipeline` (+ `langgraph-harness`). `blog-production` / `/blog` skill are not the destination. | No |

## Only take what we need (public repo)

**Keep on origin:** `index.html`, `practice-areas/`, `blog/`, `assets/`, `es/`, `go/`, `styles.css`, `CNAME`, `sitemap.xml`, `robots.txt`, and other pages that should be on lotterlaw.com.

**Already removed from origin** (PR #110, still true): `spanish-tutor/`, `analytics/` report scripts, `scripts/` publish helpers, `tmpclaude-*`, Bluehost `deploy.*`, agent session markdown (`WEBSITE_STATE.md`, SEO dumps). Do not put them back.

**Still on origin, should leave later (do not move this cycle):** `reports/` (internal HTML, including a case-number file), `documents/` reference PDFs, `intox8000-data.json` (public data file — PII review is in the System 1 receipt, not in this file).

**On disk, not origin:** `output/` (gitignored), `deploy-config.json` (gitignored), leftover OAuth token files under `scripts/config/` (gitignored — do not commit).

## Everything else has a home (not this repo)

| Thing | Lives |
|---|---|
| Court dashboard (lotterblotter.com) | GitHub `cases-v2` → Vercel |
| Weekly court-data *code* | GitHub `data-analysis` on the Mac mini |
| Court *data* | Neon + R2 — never GitHub |
| CRM / clients | Lawmatics. Files: Google Drive. Never GitHub |
| Secrets | `~/.config/CREDENTIALS.md` + host env. Never GitHub |
| Live tickets | Linear LOJL |
| Live skills | `~/.claude/skills/` on disk |

One system at a time. Next is not this file.

## Rules

1. Origin is GitHub. The clone is a copy of origin, not a second original.
2. `master` is live. If it is not ready for the public, it does not merge.
3. Drafts do not live in this public repo. Factory origin is `blog-pipeline` (LangGraph, WIP).
4. No client files, no tokens, no `.env` values.
