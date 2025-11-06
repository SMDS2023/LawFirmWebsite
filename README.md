# Legal Website - Deployment & Version Control

This repository contains the source code for a legal practice website specializing in Florida law, including DUI defense, criminal traffic, and other practice areas.

## Table of Contents

- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Version Control with Git](#version-control-with-git)
- [Deployment to Bluehost](#deployment-to-bluehost)
- [Workflow](#workflow)
- [Troubleshooting](#troubleshooting)

## Project Structure

```
WEBSITE/
├── index.html              # Homepage
├── blog.html               # Blog listing page
├── styles.css              # Main stylesheet
├── privacy.html            # Privacy policy
├── terms-and-conditions.html
├── assets/                 # Images and media files
├── blog/                   # Blog posts (20 articles)
│   ├── 01-no-jurisdiction-for-crash-investigation.html
│   ├── 02-refuse-sfst.html
│   └── ...
└── practice-areas/         # Practice area pages (16 pages)
    ├── dui.html
    ├── criminal-traffic.html
    ├── speeding-ticket.html
    └── ...
```

## Getting Started

### Prerequisites

1. **Git** - For version control
   - Download: https://git-scm.com/downloads
   - Verify installation: `git --version`

2. **Python 3.x** - For deployment script (recommended method)
   - Usually pre-installed on most systems
   - Download: https://www.python.org/downloads/
   - Verify installation: `python --version` or `python3 --version`

3. **Bluehost FTP Credentials** - Required for deployment
   - Host: Usually `ftp.yourdomain.com` or `ftp.bluehost.com`
   - Username: Your FTP username
   - Password: Your FTP password
   - Remote Path: Usually `/public_html`

## Version Control with Git

### Basic Git Commands

**Check status of your files:**
```bash
git status
```

**Add changes to staging:**
```bash
# Add specific file
git add index.html

# Add all changes
git add .
```

**Commit changes:**
```bash
git commit -m "Description of changes"
```

**View commit history:**
```bash
git log --oneline
```

**View changes before committing:**
```bash
git diff
```

### Recommended Workflow

1. **Before making changes:**
   ```bash
   git status  # Check current state
   ```

2. **Make your edits** to HTML, CSS, or other files

3. **Review changes:**
   ```bash
   git status  # See what files changed
   git diff    # See detailed changes
   ```

4. **Commit changes:**
   ```bash
   git add .
   git commit -m "Updated DUI practice area page with new case results"
   ```

5. **Deploy to Bluehost** (see next section)

## Deployment to Bluehost

### First-Time Setup

1. **Copy the configuration template:**
   ```bash
   # On Windows (Command Prompt)
   copy deploy-config-template.json deploy-config.json

   # On Git Bash or Mac/Linux
   cp deploy-config-template.json deploy-config.json
   ```

2. **Edit `deploy-config.json` with your credentials:**
   ```json
   {
     "host": "ftp.yourdomain.com",
     "username": "your-ftp-username",
     "password": "your-ftp-password",
     "remote_path": "/public_html",
     "port": 21
   }
   ```

   **IMPORTANT:** Never commit `deploy-config.json` to Git (it's already in `.gitignore`)

### How to Get Bluehost FTP Credentials

1. Log in to your Bluehost account
2. Go to **Advanced** → **FTP Accounts**
3. Use your main cPanel username/password, or create a new FTP account
4. Note your:
   - FTP Server: `ftp.yourdomain.com`
   - Username: Your FTP username
   - Password: Your FTP password

### Deploying Your Website

**Method 1: Python Script (Recommended - Works on all systems)**
```bash
python deploy.py
```
or
```bash
python3 deploy.py
```

**Method 2: PowerShell (Windows with WinSCP)**
```powershell
.\deploy.ps1
```
Requires WinSCP: https://winscp.net/eng/download.php

**Method 3: Bash Script (Git Bash with lftp)**
```bash
./deploy.sh
```
Requires lftp (install via Chocolatey: `choco install lftp`)

## Workflow

### Making Updates to Your Website

1. **Make your changes** to HTML, CSS, or add new blog posts

2. **Test locally** - Open files in your browser to verify changes

3. **Commit to Git:**
   ```bash
   git add .
   git commit -m "Added new blog post about Florida traffic laws"
   ```

4. **Deploy to Bluehost:**
   ```bash
   python deploy.py
   ```

5. **Verify** - Visit your website to confirm changes are live

### Adding a New Blog Post

1. Create new HTML file in `blog/` directory
2. Update `blog.html` to include link to new post
3. Add images (if any) to `assets/` directory
4. Commit and deploy:
   ```bash
   git add .
   git commit -m "Added blog post: Understanding Florida DUI Laws 2025"
   python deploy.py
   ```

### Adding a New Practice Area

1. Create new HTML file in `practice-areas/` directory
2. Update navigation in `index.html` and other pages
3. Commit and deploy:
   ```bash
   git add .
   git commit -m "Added new practice area: Juvenile Defense"
   python deploy.py
   ```

## Troubleshooting

### Git Issues

**Problem: "git: command not found"**
- Solution: Install Git from https://git-scm.com/downloads

**Problem: Need to undo last commit**
```bash
git reset --soft HEAD~1  # Keeps your changes
```

**Problem: Want to see what changed in a specific file**
```bash
git diff index.html
```

### Deployment Issues

**Problem: "deploy-config.json not found"**
- Solution: Copy `deploy-config-template.json` to `deploy-config.json` and fill in credentials

**Problem: FTP connection fails**
- Verify credentials in Bluehost cPanel
- Check if your IP is blocked by firewall
- Try changing port from 21 to 22 (if using SFTP)

**Problem: Some files not uploading**
- Check file permissions
- Ensure files aren't listed in `.gitignore`
- Verify remote path in `deploy-config.json`

**Problem: Python script fails**
- Verify Python is installed: `python --version`
- Try `python3 deploy.py` instead of `python deploy.py`

### Common Deployment Errors

**Error: "ftplib.error_perm: 550 Create directory operation failed"**
- The remote directory may already exist, or you don't have permissions
- Verify `remote_path` in `deploy-config.json`

**Error: Connection timeout**
- Check internet connection
- Verify FTP host address
- Check if Bluehost firewall is blocking your IP

## Best Practices

1. **Always commit before deploying**
   ```bash
   git add .
   git commit -m "Description of changes"
   python deploy.py
   ```

2. **Use descriptive commit messages**
   - Good: "Updated DUI page with 2025 law changes"
   - Bad: "Changes" or "Update"

3. **Test locally before deploying**
   - Open HTML files in browser
   - Check all links work
   - Verify images load

4. **Backup your `deploy-config.json`**
   - Keep a copy in a secure location
   - Never share or commit to Git

5. **Regular commits**
   - Commit after each logical change
   - Don't wait until end of day

## Additional Resources

- **Git Documentation:** https://git-scm.com/doc
- **Bluehost FTP Guide:** https://www.bluehost.com/help/article/ftp-access
- **Python FTP Documentation:** https://docs.python.org/3/library/ftplib.html

---

**Need Help?**
- Git issues: Check [Git Documentation](https://git-scm.com/doc)
- Bluehost issues: Contact Bluehost support
- Deployment issues: Review error messages and check credentials
