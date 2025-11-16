# Lotter Law Website Knowledge System

**Created:** 2025-11-16
**Purpose:** Centralized knowledge management for lotterlaw.com website maintenance and optimization

---

## Overview

This knowledge system serves as the **single source of truth** for all information about the Lotter Law website, including:
- Complete website inventory and audit
- Branding and style guidelines
- Optimization priorities and next steps
- Content strategy and voice standards
- Technical architecture documentation

## Knowledge Base Structure

```
.claude/
├── knowledge/
│   ├── README.md                    # This file - system overview
│   ├── MASTER-AUDIT.md             # Complete website inventory & current state
│   ├── BRAND-GUIDE.md              # Branding, voice, and formatting standards
│   └── OPTIMIZATION-TRACKER.md     # Prioritized tasks and next steps
└── commands/
    └── knowledge.md                 # /knowledge slash command
```

---

## Document Descriptions

### MASTER-AUDIT.md
**Purpose:** Complete website inventory and current state analysis

**Contents:**
- Website inventory (40 pages: core, practice areas, blog)
- Technical architecture (tech stack, hosting, analytics)
- Current state analysis (strengths & areas for improvement)
- Performance metrics and statistics
- Content strategy overview
- Brand consistency assessment
- SEO status and opportunities
- Security and compliance review
- Maintenance history

**When to Update:**
- Monthly: Add new content (blog posts, practice areas)
- Quarterly: Review analytics and performance metrics
- Annually: Comprehensive audit refresh
- As needed: Major changes or migrations

**Last Updated:** 2025-11-16

---

### BRAND-GUIDE.md
**Purpose:** Ensure consistent branding, voice, and formatting across all content

**Contents:**
- **Visual Identity:** Color palette, typography, logo usage, imagery
- **Voice & Tone:** Writing style, word choice, content templates
- **Formatting Standards:** HTML structure, Tailwind CSS conventions, components
- **Accessibility Standards:** WCAG compliance, mobile optimization
- **SEO Standards:** Meta tags, URL structure, image SEO
- **Performance Standards:** Image optimization, code efficiency
- **Brand Consistency Checklist:** Pre-publish verification

**When to Update:**
- When brand colors or fonts change
- When adding new component patterns
- When content templates evolve
- After major redesigns
- As needed for clarifications

**Last Updated:** 2025-11-16

---

### OPTIMIZATION-TRACKER.md
**Purpose:** Track ongoing optimization tasks and website improvement priorities

**Contents:**
- **Critical Tasks:** Immediate priorities (GTM migration, schema markup)
- **High Priority:** Important next steps (sitemap, robots.txt, breadcrumbs)
- **Medium Priority:** Valuable improvements (form validation, CTAs, case results)
- **Low Priority:** Nice-to-have features (live chat, video, Spanish version)
- **Completed Tasks:** Historical record of optimizations
- **Ongoing Maintenance:** Monthly, quarterly, annual checklists
- **Quick Wins:** High-impact, low-effort tasks
- **Tracking Metrics:** KPIs for measuring success

**When to Update:**
- Weekly: Update task statuses as work progresses
- Monthly: Review and reprioritize based on business goals
- When completing tasks: Move to "Completed" section
- When identifying new opportunities: Add to appropriate priority level
- After analytics review: Add data-driven optimization tasks

**Last Updated:** 2025-11-16

---

## How to Use This System

### For Content Creation
1. Review `BRAND-GUIDE.md` for voice, tone, and formatting
2. Use content templates for consistency
3. Follow SEO standards for all new pages
4. Verify brand consistency checklist before publishing

### For Website Updates
1. Check `MASTER-AUDIT.md` for current state and structure
2. Review `BRAND-GUIDE.md` for visual and technical standards
3. Update `OPTIMIZATION-TRACKER.md` with new tasks as identified
4. Update `MASTER-AUDIT.md` after significant changes

### For Planning & Prioritization
1. Review `OPTIMIZATION-TRACKER.md` for current priorities
2. Use "Quick Wins" section for immediate improvements
3. Reference "Tracking Metrics" for success measurement
4. Update task statuses weekly to track progress

### For Brand Consistency
1. Reference `BRAND-GUIDE.md` color codes and typography
2. Use approved content templates
3. Follow HTML and Tailwind conventions
4. Complete brand consistency checklist before publishing

### For Onboarding New Team Members
1. Start with this README for system overview
2. Read `MASTER-AUDIT.md` to understand current state
3. Study `BRAND-GUIDE.md` for standards and guidelines
4. Review `OPTIMIZATION-TRACKER.md` for priorities

---

## Quick Access: /knowledge Command

Use the `/knowledge` slash command in Claude Code for quick access to the knowledge base:

### Usage Examples

```bash
/knowledge                    # Overview and quick stats
/knowledge audit             # Full website inventory
/knowledge brand             # Branding guidelines
/knowledge optimize          # Current priorities
/knowledge colors            # Brand color palette
/knowledge next steps        # What to work on next
/knowledge [topic]           # Search for specific info
```

The knowledge command reads from these documents and provides relevant information based on your query.

---

## Maintenance Schedule

### Weekly
- [ ] Update `OPTIMIZATION-TRACKER.md` task statuses
- [ ] Note any new optimization opportunities discovered

### Monthly
- [ ] Update `MASTER-AUDIT.md` with new content (blog posts, pages)
- [ ] Review `OPTIMIZATION-TRACKER.md` and reprioritize tasks
- [ ] Check completed tasks and move to "Completed" section
- [ ] Update "Last Updated" dates on modified documents

### Quarterly
- [ ] Comprehensive review of all three knowledge documents
- [ ] Update analytics and performance metrics in `MASTER-AUDIT.md`
- [ ] Refresh `OPTIMIZATION-TRACKER.md` priorities based on business goals
- [ ] Review and update `BRAND-GUIDE.md` if brand evolves

### Annually
- [ ] Full audit refresh in `MASTER-AUDIT.md`
- [ ] Brand guide review and updates
- [ ] Archive completed optimization tasks
- [ ] Set new annual goals in `OPTIMIZATION-TRACKER.md`

---

## Version Control

All knowledge base documents include:
- **Last Updated** date at the top
- **Revision History** table at the bottom
- Version numbers (e.g., 1.0, 1.1, 2.0)

When updating documents:
1. Change "Last Updated" to current date
2. Add entry to "Revision History" with date, version, changes, and author
3. Increment version number appropriately (major.minor)
4. Commit changes with descriptive message

---

## Key Website Information

### Quick Reference

| Item | Value |
|------|-------|
| **Firm Name** | Lotter Law |
| **Domain** | lotterlaw.com |
| **Location** | Orlando, Florida |
| **Phone** | 407-500-7000 |
| **Hosting** | GitHub Pages |
| **Repository** | SMDS2023/LawFirmWebsite |
| **Total Pages** | 40 (4 core + 16 practice areas + 21 blog posts) |
| **Analytics** | GTM-PLX85K8L, GA4 (G-D28BZM9QDC), Clarity (reu4dibx4h) |

### Brand Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Blue-800 | #1E3A8A | Primary brand color |
| Blue-600 | #2563EB | Links, buttons |
| Amber-500 | #F59E0B | CTAs |
| Gray-700 | #374151 | Body text |

### Fonts
- **Body:** Inter (400, 500, 600, 700)
- **Headings:** Tinos (400, 700)

---

## Related Documentation

- **`/README.md`** - Project overview, deployment, and technical setup
- **`/GTM-SETUP-GUIDE.md`** - Google Tag Manager implementation guide
- **`.claude/commands/knowledge.md`** - Knowledge slash command definition

---

## Questions or Issues?

If you have questions about:
- **Website inventory or current state** → See `MASTER-AUDIT.md`
- **Branding or style guidelines** → See `BRAND-GUIDE.md`
- **What to work on next** → See `OPTIMIZATION-TRACKER.md`
- **How to use the system** → See this README
- **Quick lookup** → Use `/knowledge` command

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-16 | 1.0 | Initial knowledge system created | Claude (Knowledge Sub-Agent) |

---

**This knowledge system is a living resource. Keep it updated, accurate, and useful!**
