#!/usr/bin/env python3
"""
Add Visual Breadcrumb Navigation to LotterLaw Website
======================================================
Adds breadcrumb navigation component to practice area and blog pages.
The schema markup already exists; this adds the visible navigation.

Usage:
    python add_visual_breadcrumbs.py
"""

import os
import re
from pathlib import Path

# Configuration
WEBSITE_ROOT = Path(__file__).parent.parent
PRACTICE_AREAS_DIR = WEBSITE_ROOT / "practice-areas"
BLOG_DIR = WEBSITE_ROOT / "blog"

# Files to skip
SKIP_FILES = {"practice-area-template-.html"}

def get_page_title(html_content: str) -> str:
    """Extract page title from <title> tag."""
    match = re.search(r'<title>([^|<]+)', html_content)
    if match:
        title = match.group(1).strip()
        # Remove common suffixes
        title = re.sub(r'\s*[-|]\s*Lotter Law.*$', '', title, flags=re.IGNORECASE)
        return title.strip()
    return "Page"

def get_breadcrumb_title_from_h1(html_content: str) -> str:
    """Extract page title from first H1 tag (often more concise)."""
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def create_breadcrumb_html(crumbs: list, is_practice_area: bool = False) -> str:
    """
    Create breadcrumb HTML component.

    crumbs: list of (name, url) tuples. Last item has no URL (current page).
    """
    # Determine the base path prefix for links
    prefix = "../" if is_practice_area else ""

    items = []
    for i, crumb in enumerate(crumbs):
        is_last = (i == len(crumbs) - 1)
        name, url = crumb

        if is_last:
            # Current page - no link, bold text
            items.append(f'<span class="text-gray-600 font-medium" aria-current="page">{name}</span>')
        else:
            # Linked item
            items.append(f'<a href="{url}" class="text-blue-600 hover:text-blue-800 hover:underline">{name}</a>')

    # Join with chevron separators
    separator = '''
            <svg class="w-4 h-4 text-gray-400 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>'''

    breadcrumb_items = separator.join(items)

    return f'''
    <!-- Breadcrumb Navigation -->
    <nav aria-label="Breadcrumb" class="bg-gray-100 border-b border-gray-200">
        <div class="container mx-auto px-6 py-3">
            <ol class="flex items-center text-sm">
                {breadcrumb_items}
            </ol>
        </div>
    </nav>
'''

def add_breadcrumb_to_file(file_path: Path, crumbs: list, is_practice_area: bool = False) -> bool:
    """Add breadcrumb navigation to a single HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if breadcrumb already exists
        if 'aria-label="Breadcrumb"' in content:
            print(f"  [SKIP] Already has breadcrumb: {file_path.name}")
            return False

        # Create the breadcrumb HTML
        breadcrumb_html = create_breadcrumb_html(crumbs, is_practice_area)

        # Find insertion point: right after </header> and before <main>
        # We'll insert it after the closing </header> tag

        # Pattern to find </header> followed by any whitespace and then <main> or content
        pattern = r'(</header>\s*)'

        def replacement(match):
            return match.group(1) + breadcrumb_html

        new_content = re.sub(pattern, replacement, content, count=1)

        if new_content == content:
            print(f"  [ERROR] Could not find insertion point: {file_path.name}")
            return False

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  [OK] Added breadcrumb: {file_path.name}")
        return True

    except Exception as e:
        print(f"  [ERROR] {file_path.name}: {e}")
        return False

def process_practice_area_pages():
    """Process all practice area pages."""
    print("\n=== Processing Practice Area Pages ===")

    if not PRACTICE_AREAS_DIR.exists():
        print(f"Practice areas directory not found: {PRACTICE_AREAS_DIR}")
        return 0

    count = 0
    for file_path in sorted(PRACTICE_AREAS_DIR.glob("*.html")):
        if file_path.name in SKIP_FILES:
            print(f"  [SKIP] Template file: {file_path.name}")
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Get page title
        page_title = get_breadcrumb_title_from_h1(content) or get_page_title(content)

        # Clean up title if too long
        if len(page_title) > 50:
            page_title = get_page_title(content)
            if len(page_title) > 50:
                page_title = page_title[:47] + "..."

        # Create breadcrumb trail for practice areas
        crumbs = [
            ("Home", "../index.html"),
            ("Practice Areas", "../index.html#practice-areas-grid"),
            (page_title, None)
        ]

        if add_breadcrumb_to_file(file_path, crumbs, is_practice_area=True):
            count += 1

    return count

def process_blog_pages():
    """Process all blog pages."""
    print("\n=== Processing Blog Pages ===")

    if not BLOG_DIR.exists():
        print(f"Blog directory not found: {BLOG_DIR}")
        return 0

    count = 0
    for file_path in sorted(BLOG_DIR.glob("*.html")):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Get page title
        page_title = get_breadcrumb_title_from_h1(content) or get_page_title(content)

        # Clean up title if too long
        if len(page_title) > 60:
            page_title = page_title[:57] + "..."

        # Create breadcrumb trail for blog posts
        # Blog posts are in /blog/ subfolder, so links need to go up one level
        crumbs = [
            ("Home", "../index.html"),
            ("Blog", "../blog.html"),
            (page_title, None)
        ]

        if add_breadcrumb_to_file(file_path, crumbs, is_practice_area=True):  # Same path structure
            count += 1

    return count

def main():
    print("=" * 60)
    print("LotterLaw Visual Breadcrumb Navigation Script")
    print("=" * 60)

    practice_count = process_practice_area_pages()
    blog_count = process_blog_pages()

    print("\n" + "=" * 60)
    print(f"SUMMARY: Added breadcrumbs to {practice_count} practice area pages")
    print(f"         Added breadcrumbs to {blog_count} blog pages")
    print(f"         Total: {practice_count + blog_count} files updated")
    print("=" * 60)

if __name__ == "__main__":
    main()
