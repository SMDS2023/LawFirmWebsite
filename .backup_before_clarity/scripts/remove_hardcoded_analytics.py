#!/usr/bin/env python3
"""
Remove hardcoded GA4 and Clarity scripts from all HTML files.
GTM container script is preserved - it will handle all analytics.

Removes:
1. GA4 gtag.js loader and config block
2. Microsoft Clarity tracking script

Keeps:
- GTM container script (GTM-52LMX48G)
"""

import os
import re
from pathlib import Path

# Website root
WEBSITE_ROOT = Path(__file__).parent.parent

# Patterns to remove
GA4_PATTERN = re.compile(
    r'    <script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-[A-Z0-9]+"></script>\s*'
    r'    <script>\s*'
    r'      window\.dataLayer = window\.dataLayer \|\| \[\];\s*'
    r'      function gtag\(\)\{dataLayer\.push\(arguments\);\}\s*'
    r'      gtag\(\'js\', new Date\(\)\);\s*'
    r'\s*'
    r'      gtag\(\'config\', \'G-[A-Z0-9]+\'\);\s*'
    r'    </script>\s*',
    re.MULTILINE
)

CLARITY_PATTERN = re.compile(
    r'    <script type="text/javascript">\s*'
    r'        \(function\(c,l,a,r,i,t,y\)\{\s*'
    r'            c\[a\]=c\[a\]\|\|function\(\)\{\(c\[a\]\.q=c\[a\]\.q\|\|\[\]\)\.push\(arguments\)\};\s*'
    r'            t=l\.createElement\(r\);t\.async=1;t\.src="https://www\.clarity\.ms/tag/"\+i;\s*'
    r'            y=l\.getElementsByTagName\(r\)\[0\];y\.parentNode\.insertBefore\(t,y\);\s*'
    r'        \}\)\(window, document, "clarity", "script", "[a-z0-9]+"\);\s*'
    r'    </script>\s*',
    re.MULTILINE
)

def find_html_files():
    """Find all HTML files in the website."""
    html_files = []
    for pattern in ['*.html', 'blog/*.html', 'blog/category/*.html', 'practice-areas/*.html']:
        html_files.extend(WEBSITE_ROOT.glob(pattern))
    return sorted(set(html_files))

def remove_analytics(file_path):
    """Remove hardcoded analytics from a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove GA4
    content = GA4_PATTERN.sub('', content)

    # Remove Clarity
    content = CLARITY_PATTERN.sub('', content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    html_files = find_html_files()
    print(f"Found {len(html_files)} HTML files")

    modified = 0
    for file_path in html_files:
        rel_path = file_path.relative_to(WEBSITE_ROOT)
        if remove_analytics(file_path):
            print(f"  Cleaned: {rel_path}")
            modified += 1
        else:
            print(f"  Skipped (no changes): {rel_path}")

    print(f"\nDone! Modified {modified} files.")
    print("GA4 and Clarity scripts removed. GTM container preserved.")

if __name__ == '__main__':
    main()
