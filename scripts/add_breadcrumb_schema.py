#!/usr/bin/env python3
"""
Add BreadcrumbList Schema to Blog Posts
========================================
Adds breadcrumb structured data to blog posts for improved SEO.
"""

import json
import re
from pathlib import Path

BLOG_DIR = Path(__file__).parent.parent / "blog"
BASE_URL = "https://lotterlaw.com"

def has_breadcrumb_schema(content: str) -> bool:
    """Check if the file already has BreadcrumbList schema."""
    return 'BreadcrumbList' in content

def extract_title(content: str) -> str:
    """Extract page title from HTML."""
    title_match = re.search(r'<title>([^<]+)</title>', content)
    if title_match:
        title = title_match.group(1)
        # Clean up common suffixes
        title = re.sub(r'\s*[-|]\s*Lotter Law.*$', '', title)
        return title.strip()
    return "Article"

def generate_breadcrumb_schema(title: str, canonical_url: str) -> str:
    """Generate BreadcrumbList schema JSON-LD markup."""
    schema_obj = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": BASE_URL,
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Blog",
                "item": f"{BASE_URL}/blog.html",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": title,
                "item": canonical_url,
            },
        ],
    }
    schema_json = json.dumps(schema_obj, indent=2)
    schema = f'''
    <!-- Schema.org BreadcrumbList -->
    <script type="application/ld+json">
{schema_json}
    </script>
'''
    return schema

def add_breadcrumb_to_file(filepath: Path) -> bool:
    """Add BreadcrumbList schema to a blog post file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_breadcrumb_schema(content):
        print(f"  SKIP: {filepath.parent.name}/index.html (already has breadcrumb)")
        return False
    if re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', content, re.I) or re.search(r'<meta\s+http-equiv="refresh"', content, re.I):
        print(f"  SKIP: {filepath.parent.name}/index.html (noindex or redirect)")
        return False

    title = extract_title(content)

    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content)
    if canonical_match:
        canonical_url = canonical_match.group(1)
    else:
        canonical_url = f"{BASE_URL}/blog/{filepath.parent.name}/"

    schema = generate_breadcrumb_schema(title, canonical_url)

    # Insert breadcrumb schema just before </head>
    if '</head>' in content:
        new_content = content.replace('</head>', f'{schema}</head>')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ADDED: {filepath.parent.name}/index.html")
        return True
    else:
        print(f"  ERROR: {filepath.parent.name}/index.html (no </head> tag found)")
        return False

def main():
    """Process all blog posts and add breadcrumb schema."""
    print("=" * 60)
    print("Adding BreadcrumbList Schema to Blog Posts")
    print("=" * 60)

    if not BLOG_DIR.exists():
        print(f"ERROR: Blog directory not found: {BLOG_DIR}")
        return

    html_files = [
        path for path in BLOG_DIR.glob("*/index.html")
        if path.parent.name != "category"
    ]
    print(f"\nFound {len(html_files)} folder-style blog post files in {BLOG_DIR}\n")

    added_count = 0
    skipped_count = 0

    for filepath in sorted(html_files):
        if add_breadcrumb_to_file(filepath):
            added_count += 1
        else:
            skipped_count += 1

    print("\n" + "=" * 60)
    print(f"Summary: Added breadcrumb to {added_count} files, skipped {skipped_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
