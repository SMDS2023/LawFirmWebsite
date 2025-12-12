# Publish Blog Post

Full blog publishing workflow with SEO analysis, analytics verification, cross-linking, and sequential dating.

## Arguments
$1 = Blog post filename (e.g., "35-discovery-delays-ongoing-investigation.html")

## Instructions

### 1. SEO Analysis & Auto-Fix

Run SEO check with auto-fix enabled:

```
cd C:\Users\jeff\OneDrive\Documents\LotterLaw\Website
python scripts/seo_checker.py blog/$1 --fix
```

This will:
- Check title length, meta description, OG tags, schema, analytics
- Auto-fix title if too long (removes filler, truncates smartly)
- Auto-fix meta description if too long (sentence boundary truncation)
- Log all repairs to `output/seo_repairs/repair_log.md`
- Re-run checks to confirm fixes

If issues remain after auto-fix, manually review and fix before proceeding.

### 2. Analytics Verification

Confirm these tracking tags are present in the blog post:
- Google Tag Manager: `GTM-PLX85K8L`
- Google Analytics 4: `G-2MCJ8E0XS5`
- Microsoft Clarity: `reu4dibx4h`

If any are missing, add them using the standard template from other blog posts.

### 3. Cross-Linking

```
python scripts/cross_linker.py blog/$1
```

This will:
- Analyze the post's topic and keywords
- Find 2-3 related posts in /blog/
- Add a "Related Articles" section before the final CTA
- Update related posts to link back to this new post

### 4. Set Publish Date

```
python scripts/backdate_posts.py blog/$1
```

This will:
- Find the most recent post's publish date
- Set this post's date to the day after
- Update `<time datetime="">` in the HTML
- Update `article:published_time` meta tag
- Update `datePublished` in JSON-LD schema
- Update the date in blog.html listing

### 5. Git Commit & Push

Stage all modified files:
```
git add blog/$1 blog.html
git add blog/*.html  # For cross-linked posts
```

Commit with descriptive message:
```
git commit -m "feat(blog): Publish post #[NUMBER] - [SHORT TITLE]"
```

Push to deploy:
```
git push origin master
```

### 6. Verify Deployment

Wait 60-90 seconds for GitHub Pages to deploy, then open:
```
start https://lotterlaw.com/blog/$1
```

Check GitHub Actions for deploy status:
https://github.com/SMDS2023/LawFirmWebsite/actions

## Notes
- Each new post is dated one day after the previous post
- Always run SEO check before publishing
- Cross-linking updates multiple files - review git diff before committing
