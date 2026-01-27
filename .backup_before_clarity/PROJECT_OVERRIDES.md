# Project Overrides - LotterLaw Website

> **Project:** LotterLaw Website
> **Type:** Static Site + Python Scripts
> **Deployment:** GitHub Pages

---

## Additional Required Artifacts

Beyond the standard ACE template, this project requires:

| File | Purpose |
|------|---------|
| `index.html` | Homepage |
| `blog.html` | Blog listing page |
| `scripts/` | Python automation scripts |

---

## Extra Definition of Done Requirements

### Blog Post Tasks
- [ ] SEO tags complete (title, description, og:*, canonical)
- [ ] Post added to blog.html listing
- [ ] Internal links to practice areas included
- [ ] Mobile responsive verified

### Script Tasks
- [ ] Script runs without errors
- [ ] Output format documented
- [ ] Scheduled task configured (if recurring)

### Deployment Tasks
- [ ] Changes committed to feature branch
- [ ] PR created and merged
- [ ] GitHub Pages deployment verified
- [ ] Live site tested (lotterlaw.com)

---

## Git Workflow

1. Create feature branch: `git checkout -b claude/task-description`
2. Make changes
3. Commit with task ID reference
4. Push and create PR
5. Merge via GitHub UI
6. Wait 2-5 minutes for GitHub Pages deploy

---

## Contract Requirements

This project has contracts with:

| Provider | Contract | Location |
|----------|----------|----------|
| Google Calendar | Blog topic data | `CONTRACTS/GOOGLE_CALENDAR_CONTRACT.md` |
| Court-Dashboards | Dashboard embeds (future) | `CONTRACTS/DASHBOARD_CONTRACT.md` |

---

## SEO Checklist

Every new page must have:

- [ ] `<title>` tag (60 chars max)
- [ ] `<meta name="description">` (160 chars max)
- [ ] `<link rel="canonical">`
- [ ] `<meta property="og:title">`
- [ ] `<meta property="og:description">`
- [ ] `<meta property="og:image">`

---

*Last Updated: 2025-12-12*
