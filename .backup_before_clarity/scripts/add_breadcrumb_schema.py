#!/usr/bin/env python3
"""
Add BreadcrumbList Schema to Blog Posts
========================================
Adds breadcrumb structured data to blog posts for improved SEO.
"""

import os
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
    schema = f'''
    <!-- Schema.org BreadcrumbList -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "{BASE_URL}"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "{BASE_URL}/blog.html"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{title}",
          "item": "{canonical_url}"
        }}
      ]
    }}
    </script>
'''
    return schema

def add_breadcrumb_to_file(filepath: Path) -> bool:
    """Add BreadcrumbList schema to a blog post file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_breadcrumb_schema(content):
        print(f"  SKIP: {filepath.name} (already has breadcrumb)")
        return False

    # Extract title and canonical URL
    title = extract_title(content)
    # Escape quotes in title for JSON
    title = title.replace('"', '\\"')

    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content)
    if canonical_match:
        canonical_url = canonical_match.group(1)
    else:
        canonical_url = f"{BASE_URL}/blog/{filepath.name}"

    schema = generate_breadcrumb_schema(title, canonical_url)

    # Insert breadcrumb schema just before </head>
    if '</head>' in content:
        new_content = content.replace('</head>', f'{schema}</head>')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ADDED: {filepath.name}")
        return True
    else:
        print(f"  ERROR: {filepath.name} (no </head> tag found)")
        return False

def main():
    """Process all blog posts and add breadcrumb schema."""
    print("=" * 60)
    print("Adding BreadcrumbList Schema to Blog Posts")
    print("=" * 60)

    if not BLOG_DIR.exists():
        print(f"ERROR: Blog directory not found: {BLOG_DIR}")
        return

    html_files = list(BLOG_DIR.glob("*.html"))
    print(f"\nFound {len(html_files)} HTML files in {BLOG_DIR}\n")

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
