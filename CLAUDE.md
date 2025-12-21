# LotterLaw Website

> **Last Updated:** 2025-12-11
> **Live URL:** https://lotterlaw.com
> **Repository:** SMDS2023/LawFirmWebsite

## Project Purpose

Orlando criminal defense and DUI attorney website. Static site hosted on GitHub Pages with 58 HTML pages, Tailwind CSS, and Alpine.js.

---

## Folder Structure

> **Last indexed:** 2025-12-11

| Path | Purpose | Key Contents |
|------|---------|--------------|
| `/` | Project root | index.html, blog.html, CLAUDE.md, TASKS.md |
| `/blog/` | Blog posts | 31 numbered HTML posts (01-31) |
| `/practice-areas/` | Practice area pages | 16 pages (dui.html, criminal-traffic.html, etc.) |
| `/assets/` | Images and media | Logo, hero images, team photos |
| `/documents/` | Legal documents | Guides, templates |
| `/.claude/` | Claude Code config | knowledge/, commands/ |

### File Type Summary

| Type | Count | Location |
|------|-------|----------|
| `.html` | 58 | /, /blog/, /practice-areas/ |
| `.css` | 2 | /assets/ |
| `.md` | 8 | /, /.claude/knowledge/ |
| `.jpg/.webp` | ~35 | /assets/ |

### Key Entry Points

- **Homepage:** `index.html`
- **Blog listing:** `blog.html`
- **Knowledge:** `.claude/knowledge/MASTER-AUDIT.md`, `OPTIMIZATION-TRACKER.md`
- **Brand guide:** `.claude/knowledge/BRAND-GUIDE.md`

---

## Agent Orchestration Protocol

### Startup Sequence

1. **Read State Files**
   - `TASKS.md` - Find active task
   - `PROGRESS.md` - Read handoff notes
   - `CLAUDE.md Playbook` - Review relevant strategies

2. **Select Task**
   - Continue `in_progress` task from handoff
   - Or select highest priority `pending` task

3. **Retrieve Playbook Strategies**
   - Blog task? → Check "Blog / Content" strategies
   - SEO task? → Check "SEO / Technical" strategies
   - Check "Pitfalls to Avoid" for known issues

4. **Create Session Entry**
   - Update PROGRESS.md with session ID
   - Set task status to `in_progress`

### During Work

- Update PROGRESS.md "Work Completed" as you progress
- Check off acceptance criteria in TASKS.md
- **Always commit via pull request** (master is protected)
- Test changes locally before pushing

### Task Completion

1. **Verify:** All checkboxes checked in TASKS.md
2. **Commit:** Push to feature branch, create PR
3. **Reflect:** Extract lessons for Playbook
4. **Update State:** Move task to Completed, update PROGRESS.md

### Git Workflow

```bash
# Create feature branch
git checkout -b claude/task-description

# Make changes, commit
git add .
git commit -m "feat(blog): Add new post about X"

# Push and create PR
git push origin claude/task-description
# Then merge via GitHub UI
```

---

## Playbook: Reusable Strategies

> **Purpose:** Accumulated insights from website work. Strategies with higher usage counts are proven patterns.

### Blog / Content

| Strategy | Usage | Source |
|----------|-------|--------|
| Use SEO tags template: canonical, og:*, twitter:* for every blog post | 3 | README |
| Number blog posts sequentially (XX-title.html) | 3 | Convention |
| Update blog.html listing when adding new posts | 3 | README |
| Add "Case Result" green label for case outcome posts | 2 | Convention |
| Check YT_Comments_Scrape for topic ideas before writing | 1 | README |

### SEO / Technical

| Strategy | Usage | Source |
|----------|-------|--------|
| Test schema markup with Google Rich Results Test | 1 | OPTIMIZATION-TRACKER |
| Add LocalBusiness + Attorney schema to homepage | 1 | OPTIMIZATION-TRACKER |
| Add Article schema to all blog posts | 1 | OPTIMIZATION-TRACKER |
| Use `<picture>` element with WebP + JPG fallback | 1 | OPTIMIZATION-TRACKER |
| Add width/height attributes to all images | 1 | OPTIMIZATION-TRACKER |

### HTML / CSS

| Strategy | Usage | Source |
|----------|-------|--------|
| Use Tailwind utility classes, avoid custom CSS | 2 | Convention |
| Use Alpine.js for interactivity (accordions, modals) | 2 | Convention |
| Follow mobile-first responsive design | 2 | Convention |
| Copy existing page structure when creating new pages | 2 | README |

### Deployment

| Strategy | Usage | Source |
|----------|-------|--------|
| Always use feature branches, never push direct to master | 3 | README |
| Wait 2-5 minutes after merge for GitHub Pages deploy | 2 | README |
| Clear browser cache (Ctrl+F5) to see changes | 2 | README |
| Check DNS propagation at whatsmydns.net if issues | 1 | README |

### Pitfalls to Avoid

| Pitfall | Times Encountered | Lesson |
|---------|-------------------|--------|
| Forgetting SEO tags on new blog posts | 2 | Use the template from README every time |
| Not updating blog.html after adding post | 1 | Always update listing page too |
| Pushing to master directly | 1 | Always use feature branch + PR |
| Hardcoding analytics (GA4/Clarity) | 1 | Use GTM for all tracking |

---

## Tiered Memory Model

| Tier | Location | Purpose | Retention |
|------|----------|---------|-----------|
| **Working Context** | CLAUDE.md Playbook | Per-call strategies | Permanent |
| **Session State** | PROGRESS.md | Active task state | Until task complete |
| **Knowledge Base** | .claude/knowledge/ | Brand guide, audit, tracker | Permanent |
| **Task Registry** | TASKS.md | All tasks with criteria | Permanent |

---

## Reflector Protocol

### When to Reflect

1. **Blog post published:** What SEO worked? What could improve?
2. **Bug fixed:** What caused it? How to prevent?
3. **Performance improved:** What was the bottleneck?

### Reflection Template

```markdown
### Reflection: [Task ID]

**What Happened:**
[Brief description]

**What Worked:**
- [Strategy that succeeded]

**New Playbook Entry:**
| Strategy | Source |
|----------|--------|
| [Actionable rule] | [Task ID] |
```

---

## Key Knowledge Files

| File | Purpose |
|------|---------|
| `.claude/knowledge/MASTER-AUDIT.md` | Complete site inventory and status |
| `.claude/knowledge/OPTIMIZATION-TRACKER.md` | Prioritized task list with next steps |
| `.claude/knowledge/BRAND-GUIDE.md` | Brand colors, voice, imagery standards |
| `README.md` | Deployment workflow, DNS, troubleshooting |

---

*Last Updated: 2025-12-11*
