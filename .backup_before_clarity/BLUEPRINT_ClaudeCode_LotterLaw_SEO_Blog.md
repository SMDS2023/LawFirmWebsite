# Blueprint: LotterLaw.com SEO + Blog System Upgrade (Claude Code Execution Plan)
**Audience:** Developer/automation assistant using Claude Code (or similar).  
**Date:** 2025-12-20  
**Primary Goal:** Convert strong “hard-to-copy” content into a scalable, structured, searchable blog system that competes with the largest Orlando firms.

---

## 0) Outcomes This Blueprint Is Designed to Produce
### Business outcomes
1. Higher organic visibility for DUI/DV/Theft/Weapons/Sealing queries in Orlando/Orange County.
2. Higher consult conversion from blog traffic via cleaner CTAs and better page paths.
3. More durable authority signals (consistent author/date/schema across the blog).

### SEO/content outcomes
1. Every post has consistent EEAT: author credentials + published/updated dates.
2. Topic clusters are explicit and navigable: category pages + pillar pages + “related posts.”
3. Duplicate/overlapping “data advantage” content is canonicalized to a single pillar.
4. A weekly automated audit monitors regressions and opportunities.

---

## 1) High-Impact Fixes First (Consistency + Cannibalization)
### Issue A: Inconsistent publish-date/byline
Some posts clearly show “Published on … by Attorney Jeff Lotter,” while other pages read as content pages without visible publish metadata. This inconsistency weakens EEAT signals across the site.

**Non-negotiable rule**
- Every blog post must show:
  - Published date
  - Updated date (if edited)
  - Author name + credential (“Attorney Jeff Lotter”)
  - Link to attorney bio page

### Issue B: Topic overlap (data/analytics advantage)
Multiple pages/posts referencing “Lotter Law Edge / data analysis” can compete with each other.

**Rule**
- Create one pillar page: “Data-Driven Defense in Orange County” (or equivalent).
- All related posts link to that pillar.
- Merge or differentiate overlapping pages (avoid two pages targeting same intent).

---

## 2) Workstream A — Blog Architecture (Make it a Content System)
### A1) Create SEO-native blog structure
Required:
- `/blog/` index with pagination
- Category pages:
  - `/blog/category/dui/`
  - `/blog/category/domestic-violence/`
  - `/blog/category/theft/`
  - `/blog/category/weapons/`
  - `/blog/category/seal-expunge/`
- Optional: tag pages, but categories matter most.

**Acceptance criteria**
- Crawling `/blog/` reveals pagination and category taxonomy.
- Each post displays its category and links to the category page.

### A2) Add “Related Posts” module
Prefer manual curation (best quality), with an automated fallback (by category/tag).

**Acceptance criteria**
- 5 posts show related content links below the main body.

---

## 3) Workstream B — Template + Structured Data Standardization
### B1) Implement a reusable “post meta” component
**Display requirements**
- “Published:” date
- “Updated:” date (if applicable)
- “By Attorney Jeff Lotter” with link to bio

### B2) JSON-LD schema
- `BlogPosting` for posts
- `FAQPage` on posts that contain FAQs
- Ensure canonical link is present and correct

**Acceptance criteria**
- Rich Results Test validates BlogPosting on 5 posts.

---

## 4) Workstream C — Topic Clusters That Match Revenue (Pillars + Supporting Posts)
### Pillar list (recommended)
- DUI Defense (including refusal, SFST suppression, administrative suspension)
- Domestic Violence Defense
- Theft / Retail Theft
- Weapons / Firearms / “securely encased” issues
- Sealing and Expungement
- Driver’s License Restoration (if priority)

### Internal linking rule (“1–3–2 Rule”)
Each post must include:
- 1 link to relevant pillar
- 3 links to supporting posts
- 2 links to practice/intake pages

---

## 5) Workstream D — Conversion Optimization (Keep it Clean)
### Principle
Use fewer CTAs, but make them stronger and better placed. Avoid repeating “call/text” blocks excessively.

**Recommended CTA placement**
- Sticky header CTA (phone + consult button)
- Mid-post CTA (contextual)
- End-of-post CTA (strong, short)

**Acceptance criteria**
- Posts feel readable, not crowded.
- CTA is present without overwhelming content.

---

## 6) Workstream E — Weekly Automated Audit (Claude Code Project)
### Purpose
Generate weekly:
- New posts
- Missing byline/date/schema regressions
- Thin/overlapping content alerts
- Internal linking compliance report
- Refresh suggestions

### Inputs
- Domain: `lotterlaw.com`
- Blog index URL(s)
- Sitemap if available

### Outputs
- `reports/YYYY-MM-DD/lotterlaw_audit.md`
- `reports/YYYY-MM-DD/lotterlaw_post_table.csv`
- `reports/YYYY-MM-DD/lotterlaw_priority_fixes.md`

### Metrics per post
- URL
- Title tag/meta
- H1 and heading counts
- Author/date present
- Word count
- Internal link counts (pillar/practice/blog)
- CTA/FAQ/Related module presence
- Canonical URL
- Status code

### Scoring rubric (0–100)
- Freshness/cadence (25)
- Architecture (20)
- On-page (20)
- Conversion/UX (20)
- Topical focus (15)

### Acceptance criteria
- Script runs from CLI; output files produced.
- “Red flags” list includes missing byline/date/schema issues.

---

## 7) Execution Plan (Order of Operations)
### Phase 1 (Week 1)
1. Post meta component + consistent byline/date
2. BlogPosting JSON-LD
3. Create the “Data-Driven Defense” pillar and point related posts to it

### Phase 2 (Weeks 2–4)
1. Build categories + blog index pagination (if missing)
2. Add related posts module
3. Create 3 main pillars (DUI, DV, Theft) + internal linking

### Phase 3 (Weeks 5–8)
1. Refresh top posts with FAQs, local procedure blocks, internal links
2. Create a “Start Here” hub (best posts by topic)

### Phase 4 (Ongoing)
- Weekly audit + quarterly refresh cycle

---

## 8) “Definition of Done” Checklist
- [ ] Every post has author + publish date (+ updated date)
- [ ] BlogPosting schema validated across posts
- [ ] Category taxonomy exists and is navigable
- [ ] Topic clusters exist with pillars + related posts
- [ ] “Data advantage” pages are canonicalized to one pillar
- [ ] Weekly audit produces actionable fix list
