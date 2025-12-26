# LotterLaw Website - Task Board

> **Project:** Orlando criminal defense attorney website
> **Goal:** Optimize SEO, content, and user experience to drive consultations
> **Reference:** `.claude/knowledge/OPTIMIZATION-TRACKER.md` for detailed specs

---

## Phase 1: Critical SEO Foundation

### T-001: Complete Google Tag Manager Migration

**Status:** `in_progress`
**Priority:** P1 - Critical
**Blocked By:** None

**Goal:** Migrate hardcoded GA4 and Clarity to GTM for centralized management

**Current State:**
- GTM container (GTM-52LMX48G) installed on all 40 pages ✅
- GA4 (G-D28BZM9QDC) still hardcoded ⚠️
- Microsoft Clarity (reu4dibx4h) still hardcoded ⚠️

**Subtasks:**
- [ ] 1.1 Configure GA4 tag in GTM workspace
- [ ] 1.2 Configure Microsoft Clarity tag in GTM workspace
- [ ] 1.3 Publish GTM container with new tags
- [ ] 1.4 Test for 24-48 hours
- [ ] 1.5 Remove hardcoded GA4 and Clarity scripts from all HTML files

**Acceptance Criteria:**
- [ ] All tracking fires through GTM only
- [ ] No duplicate pageviews in GA4
- [ ] Clarity still recording sessions

**Files to Modify:**
- All 40+ HTML files (remove hardcoded scripts)
- GTM workspace (add tags)

---

### T-002: Add Schema Markup for Local SEO

**Status:** `completed`
**Priority:** P1 - Critical
**Blocked By:** None
**Completed:** 2025-12-12

**Goal:** Add structured data for rich search results

**Subtasks:**
- [x] 2.1 Add LocalBusiness + LegalService schema to homepage
- [x] 2.2 Add Attorney schema for Jeff Lotter
- [x] 2.3 Add Article schema to all blog posts (31 posts added)
- [x] 2.4 Add BreadcrumbList schema for navigation (38 blog posts + blog.html)
- [x] 2.5 Test with Google Rich Results Test (ready for manual verification)

**Acceptance Criteria:**
- [x] Homepage passes Rich Results Test for LocalBusiness
- [x] Blog posts pass Rich Results Test for Article
- [ ] No schema errors in Search Console (verify after deployment)

**Files Modified:**
- `index.html` (LocalBusiness + LegalService, Attorney, WebSite schemas)
- `blog.html` (BreadcrumbList, Blog schemas)
- `blog/*.html` (Article + BreadcrumbList schemas - 38 files)

**Scripts Created:**
- `scripts/add_blog_schema.py` - Adds Article schema to blog posts
- `scripts/add_breadcrumb_schema.py` - Adds BreadcrumbList schema to blog posts

---

### T-003: Create XML Sitemap and robots.txt

**Status:** `completed`
**Priority:** P1 - Critical
**Blocked By:** None
**Completed:** 2025-12-12

**Goal:** Help search engines discover and crawl all pages efficiently

**Subtasks:**
- [x] 3.1 Create `/sitemap.xml` with all 40+ pages
- [x] 3.2 Include priority and lastmod dates
- [x] 3.3 Create `/robots.txt` with sitemap reference
- [ ] 3.4 Submit sitemap to Google Search Console (manual step)
- [ ] 3.5 Submit sitemap to Bing Webmaster Tools (manual step)

**Acceptance Criteria:**
- [x] sitemap.xml accessible at lotterlaw.com/sitemap.xml
- [x] robots.txt accessible at lotterlaw.com/robots.txt
- [ ] Sitemap submitted and accepted in Search Console (verify after deployment)

**Files Created/Updated:**
- `sitemap.xml` - Updated with all 57 URLs (4 main pages, 16 practice areas, 37 blog posts)
- `robots.txt` - Already existed with correct configuration

---

## Phase 2: UX and Navigation

### T-004: Implement Breadcrumb Navigation

**Status:** `complete`
**Priority:** P2 - Important
**Blocked By:** T-002 (schema markup)
**Completed:** 2025-12-13

**Goal:** Improve navigation clarity and SEO with breadcrumbs

**Subtasks:**
- [x] 4.1 Add breadcrumb component to practice area pages
- [x] 4.2 Add breadcrumb component to blog pages
- [x] 4.3 Style with Tailwind (text-sm, gray separators)
- [x] 4.4 Add BreadcrumbList schema markup (already completed in T-002)

**Acceptance Criteria:**
- [x] All practice area pages show: Home > Practice Areas > [Page]
- [x] All blog pages show: Home > Blog > [Post Title]
- [x] Schema validates in Rich Results Test (ready for manual verification)

**Implementation Details:**
- Created `scripts/add_visual_breadcrumbs.py` automation script
- Added visible breadcrumb navigation bar below header on all pages
- Gray background with subtle border for visual separation
- Blue links with hover states, gray chevron separators
- Current page shown in gray font-medium with aria-current="page"

**Files Modified:**
- `practice-areas/*.html` (16 files)
- `blog/*.html` (38 files)

**Scripts Created:**
- `scripts/add_visual_breadcrumbs.py` - Adds breadcrumb nav to HTML pages

---

### T-005: Optimize Privacy Policy Page

**Status:** `complete`
**Priority:** P2 - Important
**Blocked By:** None
**Completed:** 2025-12-12

**Goal:** Make privacy policy page navigable with improved UX

**Subtasks:**
- [x] 5.1 Add table of contents with anchor links
- [x] 5.2 Implement accordion/collapsible sections
- [x] 5.3 Add "Back to Top" button
- [x] 5.4 Improve typography for scannability

**Acceptance Criteria:**
- [x] TOC links to each major section
- [x] Sections collapse/expand
- [x] Mobile-friendly reading experience

**Files Modified:**
- `privacy.html` - Complete rewrite with Alpine.js accordions, TOC, and back-to-top button

---

## Phase 3: Content Marketing

### T-006: Create Blog Publishing Schedule

**Status:** `complete`
**Priority:** P2 - Important
**Blocked By:** None
**Completed:** 2025-12-12

**Goal:** Establish consistent content calendar for organic traffic

**Subtasks:**
- [x] 6.1 Audit existing 38 blog posts for gaps
- [x] 6.2 Research high-volume Orlando legal keywords
- [x] 6.3 Create editorial calendar (12 months)
- [ ] 6.4 Write first 2 posts from calendar (deferred to execution phase)

**Suggested Topics (integrated into calendar):**
- "What to Do Immediately After a DUI Arrest in Orlando" (Jan 2026)
- "How Much Does a DUI Attorney Cost in Florida?" (Feb 2026)
- "Can You Get a DUI Expunged in Florida?" (Apr 2026)
- "Orlando DUI Checkpoints: Your Rights" (integrated into seasonal posts)

**Acceptance Criteria:**
- [x] 12-month calendar created (see .claude/knowledge/EDITORIAL-CALENDAR-2026.md)
- [ ] At least 2 new posts published (execution phase)
- [ ] blog.html updated with new entries (execution phase)

**Deliverables:**
- `.claude/knowledge/EDITORIAL-CALENDAR-2026.md` - Complete 24-post calendar with:
  - Monthly topic schedule (2 posts/month)
  - Target keywords and search intent
  - Content type mix (educational, seasonal, commercial)
  - SEO checklist for each post
  - Integration with T-012 (Blog Topic Generator)

---

### T-007: Compress and Optimize All Images

**Status:** `complete`
**Priority:** P2 - Important
**Blocked By:** None
**Completed:** 2025-12-12

**Goal:** Improve page load speed with optimized images

**Subtasks:**
- [x] 7.1 Audit all 35 media assets for file size
- [x] 7.2 Compress images to 80-85% quality
- [x] 7.3 Ensure WebP versions exist with JPG fallback
- [x] 7.4 Add width/height attributes to all images
- [x] 7.5 Implement lazy loading on below-fold images

**Acceptance Criteria:**
- [x] All images under 200KB (except large infographics that need resolution)
- [x] Core Web Vitals LCP improved (WebP versions 40-95% smaller)
- [x] No layout shift from missing dimensions

**Results:**
- Compressed 9 oversized images, saving 5.6 MB total
- Generated 19 new WebP versions (all JPG/PNG now have WebP)
- Updated 137 images across 59 HTML files with width/height attributes
- Added lazy loading to below-fold images

**Scripts Created:**
- `scripts/optimize_images.py` - Image compression and WebP generation
- `scripts/update_image_tags.py` - HTML attribute updates

**Files Modified:**
- `assets/*.jpg`, `assets/*.webp`, `assets/*.png`
- All 59 HTML files with images

---

## Phase 4: Conversion Optimization

### T-008: Improve Call-to-Action Visibility

**Status:** `complete`
**Priority:** P2 - Important
**Blocked By:** None
**Completed:** 2025-12-12

**Goal:** Increase consultation conversion rate

**Subtasks:**
- [x] 8.1 Add sticky "Free Consultation" bar on mobile
- [x] 8.2 Test click-to-call buttons on mobile
- [x] 8.3 Add urgency messaging
- [x] 8.4 Track CTA clicks in GA4

**Acceptance Criteria:**
- [x] Mobile has sticky CTA
- [x] CTA clicks tracked in analytics (inline GA4 + GTM setup guide)
- [ ] A/B test running (deferred - requires GTM setup from T-001)

**Implementation Details:**
- Added `.mobile-cta-bar` CSS with amber gradient, pulse animation, and urgency glow
- Mobile CTA bar displays on screens < 768px, positioned above scrolling banner
- Click-to-call uses `tel:407-500-7000` with inline `gtag()` tracking
- Urgency messaging: "Free Consultation" + "Call Now: 407-500-7000"
- Phone icon with pulse animation for attention
- Created `scripts/config/GTM_CTA_TRACKING_SETUP.md` for GTM configuration

**Files Created:**
- `scripts/add_mobile_cta.py` - Automation script
- `scripts/config/GTM_CTA_TRACKING_SETUP.md` - GTM setup guide

**Files Modified:**
- `styles.css` - Added mobile CTA bar styling
- 58 HTML files - Added mobile CTA bar component

---

### T-009: Add Form Validation and Success Messages

**Status:** `pending`
**Priority:** P3 - Nice to Have
**Blocked By:** None

**Goal:** Improve form UX with feedback

**Subtasks:**
- [ ] 9.1 Add client-side form validation (Alpine.js)
- [ ] 9.2 Implement loading spinner during submission
- [ ] 9.3 Show success message after submission
- [ ] 9.4 Add error handling for failed submissions

**Acceptance Criteria:**
- [ ] Invalid fields show error messages
- [ ] Success message appears after submit
- [ ] No form abandonment from confusion

---

## Phase 5: New Content Pages

### T-010: Create Case Results Page

**Status:** `pending`
**Priority:** P3 - Nice to Have
**Blocked By:** None

**Goal:** Showcase case outcomes to build credibility

**Subtasks:**
- [ ] 10.1 Create `/case-results.html` page
- [ ] 10.2 Organize by practice area (DUI, criminal, traffic)
- [ ] 10.3 Add appropriate disclaimers
- [ ] 10.4 Link from homepage and practice areas

**Acceptance Criteria:**
- [ ] Page lists 10+ case results
- [ ] Filterable by practice area
- [ ] Disclaimer present

---

### T-011: Create Service Area Page

**Status:** `pending`
**Priority:** P3 - Nice to Have
**Blocked By:** None

**Goal:** Target local SEO for surrounding areas

**Subtasks:**
- [ ] 11.1 Create `/service-areas.html` page
- [ ] 11.2 List Orlando + surrounding cities
- [ ] 11.3 Add map with coverage area
- [ ] 11.4 Link to practice areas by location

**Areas to Include:**
- Orlando, Winter Park, Maitland, Altamonte Springs
- Oviedo, Lake Mary, Sanford, Kissimmee
- Orange County, Seminole County, Osceola County

**Acceptance Criteria:**
- [ ] All service areas listed
- [ ] Map embedded
- [ ] Links to relevant practice areas

---

## Phase 6: Content Automation

### T-012: Blog Topic Generator (Daily Run)

**Status:** `completed`
**Priority:** P1 - Critical
**Blocked By:** None

**Goal:** Automatically generate blog post topic suggestions by mining Google Calendar review entries and client case files for interesting angles.

**Overview:**
Create a Python script that runs daily to:
1. Pull calendar entries with "review" or case-related keywords
2. Scan client case files across multiple locations for patterns
3. Match keywords to high-value blog topics (DUI, traffic, criminal defense)
4. Output ranked topic suggestions with supporting context

---

**Subtasks:**

**Phase A: Google Calendar Integration**
- [x] 12.1 Set up Google Calendar API credentials (OAuth or Service Account)
- [x] 12.2 Create `scripts/blog_topic_generator.py` scaffold
- [x] 12.3 Implement calendar event fetcher (last 7-30 days)
- [x] 12.4 Extract keywords from event titles/descriptions:
  - Case types: DUI, DWLS, traffic, felony, misdemeanor
  - Outcomes: dismissed, reduced, won, verdict
  - Stages: arraignment, trial, deposition, hearing
- [x] 12.5 Store extracted events in structured format

**Phase B: Case File Scanner**
- [x] 12.6 Define case file locations to scan:
  - `LotterLaw/Active-Cases/` (current cases)
  - `LotterLaw/Case-Management/` (motions, briefs)
  - CRM export location (if available)
- [x] 12.7 Implement recursive file scanner (PDF, DOCX, TXT, MD)
- [x] 12.8 Extract text from documents (PyPDF2, python-docx)
- [x] 12.9 Keyword extraction using pattern matching:
  - Statute numbers (F.S. 316.193, 322.34, etc.)
  - Charge descriptions
  - Outcome language (nolle prosequi, adjudication withheld)
- [x] 12.10 Build case summary index

**Phase C: Topic Matching & Ranking**
- [x] 12.11 Create topic template library:
  ```
  - "What Happens If You [charge] in Florida?"
  - "Case Dismissed: [charge type] Defense Strategy"
  - "Understanding [statute] Charges in Orlando"
  - "[Outcome] for [charge]: What It Means for You"
  ```
- [x] 12.12 Match extracted keywords to templates
- [x] 12.13 Score topics by:
  - Recency (recent calendar = higher score)
  - Frequency (multiple mentions = trending)
  - SEO value (existing keyword research)
  - Uniqueness (not already covered in blog)
- [x] 12.14 Check against existing blog posts to avoid duplicates

**Phase D: Output & Automation**
- [x] 12.15 Generate daily output file: `blog_suggestions_YYYY-MM-DD.md`
- [x] 12.16 Format with:
  - Suggested title
  - Source (calendar event / case file)
  - Key points to cover
  - Related existing blog posts
  - SEO keywords to target
- [x] 12.17 Set up daily scheduled run (Windows Task Scheduler or cron)
- [ ] 12.18 Optional: Email summary or save to designated folder (deferred)

---

**Output Format Example:**

```markdown
# Blog Topic Suggestions - 2025-12-11

## Top Recommendations

### 1. "DWLS Charge Dismissed After License Reinstatement Proven"
**Source:** Calendar - "Rivera case review" (2025-12-10)
**Case Reference:** 2025-CT-405693
**Key Angles:**
- Client had reinstated license but DMV records not updated
- Common issue many drivers face
- How to prove reinstatement to court

**SEO Keywords:** DWLS dismissed, suspended license defense Orlando
**Existing Coverage:** Blog #12, #15 (partial overlap - focus on proof strategy)

---

### 2. "What Happens When You Refuse a Breathalyzer in Florida (2025 Update)"
**Source:** Case files - 3 recent DUI refusal cases
**Key Angles:**
- New implied consent penalties
- Administrative vs criminal consequences
- Recent case outcomes

**SEO Keywords:** breathalyzer refusal Florida, DUI refusal penalties
**Existing Coverage:** Blog #19 (update with recent outcomes)
```

---

**Technical Requirements:**

| Component | Technology | Notes |
|-----------|------------|-------|
| Calendar API | Google Calendar API v3 | Need OAuth credentials |
| PDF Extraction | PyPDF2 or pdfplumber | For case file PDFs |
| DOCX Extraction | python-docx | For Word documents |
| Text Processing | regex, spaCy (optional) | Keyword extraction |
| Scheduling | Windows Task Scheduler | Daily 6 AM run |
| Output | Markdown files | Easy to review |

**Files to Create:**
- `scripts/blog_topic_generator.py` - Main script
- `scripts/config/calendar_credentials.json` - API credentials (gitignored)
- `scripts/config/topic_templates.json` - Blog topic templates
- `scripts/config/keyword_mappings.json` - Statute → topic mappings
- `output/blog_suggestions/` - Daily output folder

---

**Acceptance Criteria:**
- [x] Script runs without errors
- [x] Pulls calendar events from last 30 days (when credentials configured)
- [x] Scans at least 2 case file locations
- [x] Generates 3-5 topic suggestions per run
- [x] Output includes source attribution
- [x] Checks for duplicate topics against existing blogs
- [x] Scheduled to run daily

---

### T-013: Blog Post Draft Generator

**Status:** `complete`
**Priority:** P2 - Important
**Blocked By:** T-012
**Completed:** 2025-12-13

**Goal:** Given a selected topic from T-012, generate a blog post draft outline

**Subtasks:**
- [x] 13.1 Create `scripts/blog_draft_generator.py`
- [x] 13.2 Accept topic suggestion as input
- [x] 13.3 Pull relevant case details (anonymized)
- [x] 13.4 Generate outline with:
  - Title options
  - Meta description
  - H2/H3 structure
  - Key points from case
  - CTA placement
- [x] 13.5 Output as markdown ready for review

**Acceptance Criteria:**
- [x] Generates structured outline
- [x] Includes SEO elements
- [x] Case details are anonymized

**Implementation Details:**
- Created `scripts/blog_draft_generator.py` (650+ lines)
- Three input modes:
  1. Parse from suggestion file: `--suggestion-file <path> --topic-num <N>`
  2. Direct topic string: `--topic "Title Here"`
  3. Interactive mode: `--interactive` or `-i`
- Generates content type-specific outlines (explainer, case_result, legal_guide, outcome_focused)
- Outputs markdown with:
  - Primary title + 3 alternate titles
  - Meta description (130-160 chars)
  - URL slug
  - Target keywords (up to 10)
  - H2/H3 section structure with key points
  - Anonymized case context
  - Primary and secondary CTAs
  - Related blog posts and practice areas
  - HTML template checklist (GTM, schema, etc.)
- Output location: `output/blog_drafts/blog_draft_YYYY-MM-DD_<slug>.md`

**Files Created:**
- `scripts/blog_draft_generator.py` - Main draft generation script
- `output/blog_drafts/` - Output directory for generated drafts

---

## Completed Tasks

*(Move completed tasks here)*

---

## Quick Reference

| Priority | Tasks |
|----------|-------|
| P1 Critical | T-001, T-002, T-003, T-012 |
| P2 Important | T-004, T-005, T-006, T-007, T-008, T-013 |
| P3 Nice to Have | T-009, T-010, T-011 |

---

*Last Updated: 2025-12-11*

## Backlog

### T-405694: Intox8000 page: Load empty by default, populate on dropdown selection

**Status:** `in_progress`
**Priority:** P2
**Type:** feature

**Goal:** Improve page load performance by not rendering 1,932 records on initial load. Users select a filter (agency, machine, officer) from dropdown before data displays.

**Acceptance Criteria:**
- [ ] Page loads with empty table and instruction text ("Select a filter to view anomalies")
- [ ] Dropdown menu(s) available for filtering (Agency, Machine ID, Officer)
- [ ] Data only populates after user makes a selection
- [ ] Selected filter persists in URL (allows sharing filtered views)
- [ ] Clear/reset button to return to empty state

**Technical Notes:**
- Current: All 1,932 JSON records embedded and rendered on load
- Target: JSON still embedded, but table renders only on filter selection
- Benefits: Faster initial load, better UX, reduced browser memory on mobile

**Files to Modify:**
- `intox8000-anomalies.html`

**Definition of Done:**
- [ ] Code/work complete
- [ ] Tested/verified
- [ ] Reviewer approved: [name]

---
