# Lotter Law Website - GitHub Pages Deployment

This repository contains the source code for Lotter Law, a Florida-based legal practice specializing in DUI defense, criminal traffic, and other practice areas.

**Live Site:** https://lotterlaw.com
**GitHub Pages URL:** https://SMDS2023.github.io/LawFirmWebsite

---

## Table of Contents

- [Migration Summary](#migration-summary)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Making Website Updates](#making-website-updates)
- [Bluehost Cancellation Guide](#bluehost-cancellation-guide)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)

---

## Migration Summary

**Migrated from:** Bluehost shared hosting
**Migrated to:** GitHub Pages (free static site hosting)
**Migration date:** November 2025

### What Changed:
- ✅ Website now hosted on GitHub Pages (free, fast, reliable)
- ✅ Custom domain (lotterlaw.com) pointed to GitHub Pages
- ✅ HTTPS enabled automatically
- ✅ Updates deploy automatically when changes are merged to master branch
- ✅ No more FTP uploads or manual deployments
- ✅ Full version history tracked in Git

### What Stayed the Same:
- ✅ Google Workspace email (unchanged - uses separate DNS records)
- ✅ Domain name (lotterlaw.com)
- ✅ Website content and functionality
- ✅ All blog posts and practice area pages

### Cost Savings:
- **Before:** ~$78-218/year (Bluehost hosting + domain)
- **After:** ~$18/year (domain only at Bluehost) or ~$9/year (if transferred to Cloudflare)
- **Annual savings:** $60-200/year

---

## Project Structure

```
LawFirmWebsite/
├── index.html              # Homepage with DUI alert, practice areas, team bio
├── blog.html               # Blog listing page (19 articles)
├── styles.css              # Main stylesheet
├── privacy.html            # Privacy policy
├── terms-and-conditions.html
├── assets/                 # Images and media files
│   └── Attorney-Jeff-Lotter1.jpg
├── blog/                   # Blog posts (19 articles)
│   ├── 02-refuse-sfst.html
│   ├── 03-understanding-probable-cause.html
│   ├── 19-new-dui-refusal-law.html
│   └── ...
├── practice-areas/         # Practice area pages (16 pages)
│   ├── dui.html
│   ├── criminal-traffic.html
│   ├── speeding-ticket.html
│   └── ...
└── README.md               # This file
```

---

## How It Works

### GitHub Pages Deployment

GitHub Pages automatically builds and deploys your website whenever you push changes to the `master` branch.

**Deployment Flow:**
1. You make changes to HTML/CSS files (or ask Claude to make them)
2. Changes are committed to a feature branch (e.g., `claude/update-footer-XYZ`)
3. A pull request is created to merge into `master`
4. Once merged, GitHub Pages automatically rebuilds the site
5. Changes are live at lotterlaw.com in **2-5 minutes**

**No manual deployment required!**

### DNS Configuration

Your domain (lotterlaw.com) points to GitHub Pages via these DNS records in Bluehost:

**A Records (GitHub Pages IPs):**
```
@ → 185.199.108.153
@ → 185.199.109.153
@ → 185.199.110.153
@ → 185.199.111.153
```

**CNAME Record (www subdomain):**
```
www → smds2023.github.io
```

These DNS records tell the internet to route lotterlaw.com traffic to GitHub Pages instead of Bluehost.

---

## Making Website Updates

### Option 1: Working with Claude (Recommended)

This is the easiest method - just describe what you want changed!

**Example workflow:**
1. **Tell Claude what you need:**
   "Update the homepage to add a new practice area for Juvenile Defense"

2. **Claude makes the changes:**
   - Creates/edits files
   - Commits to a feature branch
   - Pushes to GitHub

3. **You review and merge:**
   - Visit the pull request URL Claude provides
   - Review the changes on GitHub
   - Click "Merge pull request"
   - Click "Confirm merge"

4. **Site updates automatically:**
   - Wait 2-5 minutes
   - Visit lotterlaw.com to see changes live

### Option 2: Manual Updates via GitHub Web Interface

For small text changes, you can edit directly on GitHub:

1. **Go to:** https://github.com/SMDS2023/LawFirmWebsite
2. **Navigate to the file** you want to edit (e.g., `index.html`)
3. **Click the pencil icon** (Edit this file)
4. **Make your changes**
5. **Scroll down** and click "Commit changes"
6. **Select:** "Create a new branch for this commit and start a pull request"
7. **Click "Propose changes"**
8. **Click "Create pull request"**
9. **Click "Merge pull request"** (after reviewing)
10. **Wait 2-5 minutes** for deployment

### Option 3: Local Development (Advanced)

If you want to work on your local computer:

**Setup (one-time):**
```bash
# Clone the repository
git clone https://github.com/SMDS2023/LawFirmWebsite.git
cd LawFirmWebsite

# Create a new branch for your changes
git checkout -b my-updates
```

**Make changes:**
```bash
# Edit files in your text editor
# Test by opening HTML files in your browser

# Stage changes
git add .

# Commit changes
git commit -m "Description of what you changed"

# Push to GitHub
git push origin my-updates
```

**Create pull request:**
1. Visit: https://github.com/SMDS2023/LawFirmWebsite
2. Click "Compare & pull request"
3. Review and click "Create pull request"
4. Merge when ready

### Adding New Content

#### Adding a New Blog Post

1. **Create the blog post HTML file:**
   - Save as `blog/20-your-post-title.html`
   - Use existing blog posts as templates

2. **Update blog.html:**
   - Add a new `<article>` entry at the top of the blog listing
   - Include title, date, summary, and link

3. **Commit and merge:**
   ```bash
   git add blog/20-your-post-title.html blog.html
   git commit -m "Add blog post: Your Title Here"
   git push origin your-branch-name
   ```

4. **Merge to master** via pull request

#### Adding a New Practice Area

1. **Create practice area page:**
   - Save as `practice-areas/new-area.html`
   - Use existing pages as templates

2. **Update homepage navigation:**
   - Edit `index.html` to add link in practice areas section

3. **Commit and merge** via pull request

---

## Bluehost Cancellation Guide

Now that your website is hosted on GitHub Pages, you can cancel Bluehost hosting and save money.

### Before You Cancel: Verify Everything Works

**Checklist:**
- [ ] lotterlaw.com loads correctly
- [ ] www.lotterlaw.com loads correctly
- [ ] HTTPS works (padlock icon shows)
- [ ] All pages work (homepage, blog, practice areas)
- [ ] Google Workspace email still works
- [ ] Site has been working for at least 2-3 days

### Cancellation Options

#### Option A: Cancel Hosting, Keep Domain at Bluehost (Easiest)

**When to choose this:**
- You want the simplest option
- You're comfortable with current domain costs
- You don't want to transfer domain right now

**Steps:**
1. **Call Bluehost Support:** 1-888-401-4678 (or use chat)
2. **Say:** "I want to cancel my web hosting plan but keep my domain registration for lotterlaw.com"
3. **They will:**
   - Downgrade you to domain-only service
   - Stop charging for hosting
   - Keep your domain active
4. **Request refund** if eligible (ask about remaining hosting time)
5. **Verify:**
   - Domain still renews automatically
   - You can still manage DNS in Bluehost
   - Hosting charges stop

**Cost after:** ~$15-18/year (domain registration only)

#### Option B: Transfer Domain to Cloudflare (Cheapest)

**When to choose this:**
- You want maximum savings
- You want better security/performance
- You're comfortable doing a domain transfer

**Cost:** ~$9/year (at-cost pricing, no markup)

**Steps:**

**Part 1: Prepare domain at Bluehost**
1. **Log into Bluehost**
2. **Go to:** Domains → My Domains → lotterlaw.com
3. **Unlock the domain:**
   - Look for "Domain Lock" or "Registrar Lock"
   - Turn it OFF/Unlock
4. **Get authorization code:**
   - Click "Get EPP Code" or "Authorization Code"
   - Save this code (you'll need it for transfer)
5. **Verify contact email:**
   - Make sure your email is current
   - You'll receive transfer confirmation emails here

**Part 2: Transfer to Cloudflare**
1. **Create Cloudflare account:** https://dash.cloudflare.com/sign-up
2. **Go to:** Domain Registration → Transfer Domains
3. **Enter:** lotterlaw.com
4. **Enter authorization code** from Bluehost
5. **Add payment method** ($9 + 1 year renewal)
6. **Confirm transfer**
7. **Check email** and approve transfer (from both Bluehost and Cloudflare)
8. **Wait 5-7 days** for transfer to complete

**Part 3: Update DNS at Cloudflare**

After transfer completes:
1. **Add the same DNS records:**
   - 4 A records pointing to GitHub Pages IPs (listed above)
   - 1 CNAME record for www
   - Keep Google Workspace MX/TXT records (if they exist)
2. **Wait 24 hours** for DNS propagation
3. **Verify site works**

**Part 4: Cancel Bluehost completely**
1. **Call Bluehost:** 1-888-401-4678
2. **Say:** "My domain has transferred, I want to cancel my account completely"
3. **Request refund** for any unused time
4. **Confirm cancellation**

**Cost after:** ~$9/year (domain at Cloudflare)

#### Option C: Transfer Domain to Google Domains/Squarespace

**When to choose this:**
- You want everything in one place with Google Workspace
- You prefer Google's interface
- Cost isn't the primary concern

**Cost:** ~$12/year

**Steps:** Similar to Cloudflare transfer above, but use Google Domains (now Squarespace Domains)

### Important Notes

**DO NOT cancel until:**
- ✅ lotterlaw.com has worked perfectly for 2-3 days
- ✅ You've tested all pages
- ✅ You've verified email still works
- ✅ You're confident the migration is complete

**Domain transfers:**
- Take 5-7 days to complete
- Your website stays online during transfer
- Email is not affected
- You'll get a free 1-year extension (you don't lose time)

**If something goes wrong:**
- You have DNS records backed up in this README
- You can recreate them at any registrar
- Google Workspace email is separate and won't be affected

---

## Technical Details

### GitHub Repository Settings

**Repository:** https://github.com/SMDS2023/LawFirmWebsite
**Branch for deployment:** `master`
**GitHub Pages source:** Deploy from a branch → master → / (root)
**Custom domain:** lotterlaw.com
**Enforce HTTPS:** ✅ Enabled

### DNS Records Reference

**Current DNS Configuration (at Bluehost):**

| Type  | Host | Points To              | TTL    |
|-------|------|------------------------|--------|
| A     | @    | 185.199.108.153        | 4 hours|
| A     | @    | 185.199.109.153        | 4 hours|
| A     | @    | 185.199.110.153        | 4 hours|
| A     | @    | 185.199.111.153        | 4 hours|
| CNAME | www  | smds2023.github.io     | 4 hours|

**Google Workspace DNS (if configured):**
- MX records for email (5 records pointing to google.com)
- TXT record for domain verification
- TXT record for SPF
- CNAME records for DKIM

*Note: These email DNS records are separate and won't be affected by website hosting changes*

### HTTPS Certificate

GitHub Pages automatically provisions and renews a free Let's Encrypt SSL certificate for lotterlaw.com.

**Certificate details:**
- Issued by: Let's Encrypt
- Auto-renewal: Yes
- Covers: lotterlaw.com and www.lotterlaw.com
- No manual renewal needed

### Build and Deployment

**How deployment works:**
1. Push to master branch triggers GitHub Pages build
2. GitHub validates HTML/CSS/JS files
3. Static site is built and deployed to CDN
4. Changes propagate globally in 2-5 minutes
5. Browser cache may take additional time to clear

**What gets deployed:**
- All HTML files
- All CSS files
- All images in `/assets`
- All blog posts in `/blog`
- All practice area pages in `/practice-areas`

**What doesn't get deployed:**
- `.git` directory (version control metadata)
- README.md (documentation only)
- Any files listed in `.gitignore`

---

## Troubleshooting

### Website Issues

**Problem: Changes not showing up after merge**
- **Wait 5-10 minutes** - deployment takes time
- **Clear browser cache:** Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
- **Check GitHub Pages status:** Settings → Pages → "Your site is live at..."
- **Check build status:** Actions tab → View recent workflow runs

**Problem: lotterlaw.com not loading**
- **Check DNS propagation:** https://www.whatsmydns.net/#A/lotterlaw.com
- **Should show 4 GitHub IP addresses** globally
- **If not:** DNS changes can take 24-48 hours
- **Verify custom domain:** Settings → Pages → Custom domain shows "lotterlaw.com"

**Problem: HTTPS not working (insecure warning)**
- **Wait 10-30 minutes** after initial domain setup
- **Verify "Enforce HTTPS" is checked** in Settings → Pages
- **Try:** Uncheck "Enforce HTTPS", wait 5 mins, check it again
- **Certificate may take up to 24 hours** to fully propagate

**Problem: www.lotterlaw.com not working**
- **Check CNAME record:** Should point to smds2023.github.io
- **Verify in DNS:** https://www.whatsmydns.net/#CNAME/www.lotterlaw.com
- **Check GitHub Pages custom domain** includes both versions

### Email Issues

**Problem: Email stopped working after migration**
- **Check Google Workspace admin:** https://admin.google.com
- **Verify MX records still exist** in your DNS
- **DNS records should include:**
  - 5 MX records pointing to google.com servers
  - TXT record for SPF verification
  - CNAME records for DKIM
- **If missing:** Re-add them in Bluehost DNS or contact Google Workspace support

**Problem: Email works but website doesn't**
- **Good news:** Email and website DNS are separate
- **Email uses:** MX records
- **Website uses:** A and CNAME records
- **Fix website DNS** without affecting email records

### Git/GitHub Issues

**Problem: Can't push to master branch**
- **This is expected:** Master branch is protected
- **Always create a feature branch:**
  ```bash
  git checkout -b my-feature-branch
  git push origin my-feature-branch
  ```
- **Then create pull request** on GitHub

**Problem: Merge conflicts**
- **Happens when:** Multiple people edit same file
- **Solution in GitHub:**
  1. Click "Resolve conflicts" on PR
  2. Edit the conflicting sections
  3. Mark as resolved
  4. Commit merge

**Problem: Accidentally committed sensitive info**
- **If not pushed yet:**
  ```bash
  git reset --soft HEAD~1  # Undo last commit, keep changes
  ```
- **If already pushed:**
  - Contact support immediately
  - May need to rotate credentials
  - Use `git filter-branch` or BFG Repo-Cleaner (advanced)

### Domain/DNS Issues

**Problem: DNS changes not taking effect**
- **DNS propagation takes 24-48 hours**
- **Check propagation:** https://www.whatsmydns.net
- **TTL affects speed:** 4 hours = changes can take 4 hours minimum
- **Clear local DNS cache:**
  - Windows: `ipconfig /flushdns`
  - Mac: `sudo dscacheutil -flushcache`
  - Linux: `sudo systemd-resolve --flush-caches`

**Problem: Lost DNS records during transfer**
- **Prevention:** Screenshot all DNS records before transfer
- **Recovery:** Re-add records from Technical Details section above
- **Critical records:**
  - 4 A records for GitHub Pages
  - 1 CNAME for www
  - 5 MX records for Google Workspace (if applicable)

### Bluehost Issues

**Problem: Bluehost won't let me cancel hosting**
- **Call instead of using online chat:** 1-888-401-4678
- **Be firm:** "I want to cancel web hosting but keep my domain"
- **They may offer discounts:** Decline if you don't need hosting
- **Ask for supervisor** if rep is difficult

**Problem: Bluehost says I'll lose my domain**
- **This is incorrect:** You can keep domain without hosting
- **Clarify:** "I want domain registration only, not web hosting"
- **Domain and hosting are separate services**

**Problem: Can't get authorization code for transfer**
- **Domain must be:**
  - Unlocked (registrar lock OFF)
  - At least 60 days old since registration/last transfer
  - Not expired or within 15 days of expiration
- **Contact Bluehost support** if button doesn't appear

---

## Best Practices

### Content Updates
1. **Always test changes** by reviewing the PR before merging
2. **Use descriptive commit messages:**
   - ✅ Good: "Add 2025 DUI law changes to blog post"
   - ❌ Bad: "Update" or "Changes"
3. **Make small, focused changes** rather than massive updates
4. **Review changes on GitHub** before merging to master

### Version Control
1. **Never commit sensitive information:**
   - No passwords
   - No API keys
   - No personal contact info beyond what's public
2. **Create feature branches** for all changes
3. **Use pull requests** even for small changes (creates audit trail)
4. **Keep commits atomic** (one logical change per commit)

### DNS Management
1. **Screenshot DNS records** before making changes
2. **Test one record at a time** when troubleshooting
3. **Keep MX records** for email separate from web hosting records
4. **Document all changes** with date/time and reason

### Backups
- **Git is your backup:** Every commit is stored permanently
- **View any previous version:**
  ```bash
  git log --oneline  # Find commit hash
  git checkout <commit-hash> file.html  # Restore old version
  ```
- **No need for manual backups** - GitHub stores everything

---

## Additional Resources

### Documentation
- **GitHub Pages:** https://docs.github.com/en/pages
- **Custom domains on GitHub Pages:** https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site
- **Git basics:** https://git-scm.com/doc
- **Cloudflare Registrar:** https://www.cloudflare.com/products/registrar/

### DNS Tools
- **DNS Propagation Checker:** https://www.whatsmydns.net
- **DNS Lookup:** https://mxtoolbox.com/DNSLookup.aspx
- **SSL Certificate Checker:** https://www.sslshopper.com/ssl-checker.html

### Support Contacts
- **GitHub Support:** https://support.github.com
- **Bluehost Support:** 1-888-401-4678 or https://my.bluehost.com/cgi/help
- **Cloudflare Support:** https://support.cloudflare.com
- **Google Workspace Support:** https://support.google.com/a

---

## Migration History

**November 2025: Migrated from Bluehost to GitHub Pages**
- Removed Florida Bar number from footer (homepage and blog)
- Configured DNS to point lotterlaw.com to GitHub Pages
- Enabled HTTPS via GitHub Pages
- Updated deployment workflow from FTP to GitHub pull requests
- Documented new workflow in this README

**Previous Setup:**
- Hosted on Bluehost shared hosting
- Manual FTP deployments using Python script
- Cost: ~$78-218/year

**Current Setup:**
- Hosted on GitHub Pages (free)
- Automatic deployments via Git push
- Cost: ~$18/year (domain only) or ~$9/year (if domain transferred)

---

## Quick Reference

### Common Commands

**Check what branch you're on:**
```bash
git branch
```

**Create a new branch:**
```bash
git checkout -b feature/my-new-feature
```

**See what changed:**
```bash
git status
git diff
```

**Commit changes:**
```bash
git add .
git commit -m "Description of changes"
```

**Push to GitHub:**
```bash
git push origin your-branch-name
```

### Common Tasks

**Update blog footer:**
- Edit `blog.html` around line 460-470
- Commit and merge to master

**Update homepage:**
- Edit `index.html`
- Test locally by opening in browser
- Commit and merge to master

**Add new blog post:**
1. Create `blog/XX-post-title.html`
2. Update `blog.html` to add link
3. Commit both files
4. Merge to master

**Check if site is live:**
- Visit: https://lotterlaw.com
- GitHub Pages URL: https://smds2023.github.io/LawFirmWebsite

---

**Questions or issues?** Contact Claude or create an issue on GitHub.

**Last updated:** November 2025
