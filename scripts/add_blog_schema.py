#!/usr/bin/env python3
"""
Add Article Schema to Blog Posts
=================================
Adds structured data (Article schema) to blog posts that are missing it.
"""

import os
import re
from pathlib import Path
from datetime import datetime

BLOG_DIR = Path(__file__).parent.parent / "blog"
BASE_URL = "https://lotterlaw.com/blog"

def has_schema(content: str) -> bool:
    """Check if the file already has JSON-LD schema."""
    return 'application/ld+json' in content

def extract_metadata(content: str, filename: str) -> dict:
    """Extract metadata from HTML file for schema generation."""
    metadata = {
        'title': '',
        'description': '',
        'keywords': '',
        'canonical': '',
        'published_date': datetime.now().strftime('%Y-%m-%d'),
        'image': 'https://lotterlaw.com/assets/Lotter-Law-logo-02.jpg'
    }

    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', content)
    if title_match:
        metadata['title'] = title_match.group(1).replace(' - Lotter Law', '').replace(' | Lotter Law', '').strip()

    # Extract description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    if desc_match:
        metadata['description'] = desc_match.group(1)

    # Extract keywords
    kw_match = re.search(r'<meta\s+name="keywords"\s+content="([^"]+)"', content)
    if kw_match:
        metadata['keywords'] = kw_match.group(1)

    # Extract canonical URL
    canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content)
    if canonical_match:
        metadata['canonical'] = canonical_match.group(1)
    else:
        metadata['canonical'] = f"{BASE_URL}/{filename}"

    # Extract published date from og:article:published_time or og meta
    date_match = re.search(r'<meta\s+property="article:published_time"\s+content="([^"]+)"', content)
    if date_match:
        metadata['published_date'] = date_match.group(1)[:10]

    # Extract og:image if exists
    img_match = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', content)
    if img_match:
        metadata['image'] = img_match.group(1)

    return metadata

def generate_article_schema(metadata: dict) -> str:
    """Generate Article schema JSON-LD markup."""
    schema = f'''
    <!-- Schema.org Article -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{metadata['title']}",
      "description": "{metadata['description']}",
      "author": {{
        "@type": "Person",
        "name": "Jeff Lotter",
        "jobTitle": "Attorney",
        "url": "https://lotterlaw.com"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Lotter Law",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://lotterlaw.com/assets/Lotter-Law-logo-02.jpg"
        }}
      }},
      "datePublished": "{metadata['published_date']}",
      "dateModified": "{metadata['published_date']}",
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{metadata['canonical']}"
      }},
      "image": "{metadata['image']}",
      "articleSection": "Legal",
      "keywords": "{metadata['keywords']}"
    }}
    </script>
'''
    return schema

def add_schema_to_file(filepath: Path) -> bool:
    """Add Article schema to a blog post file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_schema(content):
        print(f"  SKIP: {filepath.name} (already has schema)")
        return False

    metadata = extract_metadata(content, filepath.name)
    schema = generate_article_schema(metadata)

    # Insert schema just before </head>
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
    """Process all blog posts and add schema where missing."""
    print("=" * 60)
    print("Adding Article Schema to Blog Posts")
    print("=" * 60)

    if not BLOG_DIR.exists():
        print(f"ERROR: Blog directory not found: {BLOG_DIR}")
        return

    html_files = list(BLOG_DIR.glob("*.html"))
    print(f"\nFound {len(html_files)} HTML files in {BLOG_DIR}\n")

    added_count = 0
    skipped_count = 0

    for filepath in sorted(html_files):
        if add_schema_to_file(filepath):
            added_count += 1
        else:
            skipped_count += 1

    print("\n" + "=" * 60)
    print(f"Summary: Added schema to {added_count} files, skipped {skipped_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
