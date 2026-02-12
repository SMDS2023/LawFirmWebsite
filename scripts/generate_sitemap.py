#!/usr/bin/env python3
"""
Regenerative Sitemap Generator for LotterLaw Website

Scans ALL page types from filesystem and generates complete sitemap.xml.
Self-healing: Always reflects current filesystem state.

Page types scanned:
  - Root pages (*.html, with exclusion list)
  - Practice area pages (practice-areas/*.html)
  - Spanish practice area pages (es/practice-areas/*.html, with hreflang)
  - Blog category pages (blog/category/*.html)
  - Blog posts (blog/slug/index.html, gated by blog.html listing)
"""

import re
import subprocess
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

# Root pages to EXCLUDE from sitemap
EXCLUDED_ROOT = {
    '404.html',
    'thank-you.html',
    'Current_Week_Report.html',
}

# Practice area files to skip
EXCLUDED_PRACTICE_AREAS = {
    'practice-area-template-.html',
}

# Root page priority/changefreq overrides (unlisted pages get defaults)
ROOT_CONFIG = {
    'index.html':             {'priority': '1.0', 'changefreq': 'weekly'},
    'blog.html':              {'priority': '0.9', 'changefreq': 'daily'},
    'data-driven-defense.html': {'priority': '0.9', 'changefreq': 'monthly'},
    'service-areas.html':     {'priority': '0.9', 'changefreq': 'monthly'},
    'officer-intel.html':     {'priority': '0.7', 'changefreq': 'monthly'},
    'client-portal-guide.html': {'priority': '0.6', 'changefreq': 'monthly'},
    'privacy.html':           {'priority': '0.3', 'changefreq': 'yearly'},
    'terms-and-conditions.html': {'priority': '0.3', 'changefreq': 'yearly'},
}
ROOT_DEFAULT = {'priority': '0.7', 'changefreq': 'monthly'}

# Practice area priority overrides (default: 0.8)
PA_PRIORITY = {
    'dui.html': '0.9',
    'suspended-license.html': '0.7',
    'driver-license-restoration.html': '0.7',
    'seal-and-expunge.html': '0.7',
    'tolls.html': '0.6',
    'auto-registration.html': '0.6',
    'other-crimes.html': '0.6',
    'moving-violations.html': '0.7',
}
PA_DEFAULT_PRIORITY = '0.8'


def get_tracked_files(website_path):
    """Get set of git-tracked HTML files (relative to website_path).

    Only tracked files are deployed to GitHub Pages, so only these
    should appear in the sitemap.
    """
    try:
        result = subprocess.run(
            ['git', 'ls-files', '--', '*.html', '**/*.html'],
            capture_output=True, text=True, cwd=website_path
        )
        if result.returncode == 0:
            return {f for f in result.stdout.strip().split('\n')
                    if f and not f.startswith('.backup_before_clarity/')}
    except Exception:
        pass
    return None  # Fallback: no filtering


def extract_metadata_from_html(html_file):
    """Extract publish date and title from blog post HTML."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    date_match = re.search(r'"datePublished":\s*"([^"]+)"', content)
    date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")

    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else ""

    return date, title


def get_listed_blog_posts(blog_html_path):
    """Extract blog post slugs that are actually listed in blog.html.

    This ensures only published posts appear in sitemap, not staged posts.
    Supports both folder-style (blog/slug/) and legacy (blog/XX-slug.html) hrefs.
    """
    with open(blog_html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    listed_slugs = set()

    # Folder-style: href="blog/slug/" or href="/blog/slug/"
    folder_matches = re.findall(r'href="/?blog/([^/"]+)/"', content)
    listed_slugs.update(folder_matches)

    # Legacy flat file style: href="blog/XX-slug.html"
    flat_matches = re.findall(r'href="/?blog/([^"]+\.html)"', content)
    for fname in flat_matches:
        slug = Path(fname).stem
        num_match = re.match(r'^\d+-(.+)$', slug)
        if num_match:
            listed_slugs.add(num_match.group(1))
        else:
            listed_slugs.add(slug)

    return listed_slugs


def load_existing_lastmods(sitemap_path):
    """Read existing sitemap.xml to preserve lastmod dates."""
    lastmods = {}
    if not sitemap_path.exists():
        return lastmods

    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        for url_elem in root.findall('sm:url', ns):
            loc_elem = url_elem.find('sm:loc', ns)
            lastmod_elem = url_elem.find('sm:lastmod', ns)
            if loc_elem is not None and lastmod_elem is not None:
                lastmods[loc_elem.text] = lastmod_elem.text
    except Exception:
        pass

    return lastmods


def generate_sitemap(website_dir):
    """Generate complete sitemap.xml from filesystem."""
    website_path = Path(website_dir)
    today = datetime.now().strftime("%Y-%m-%d")

    # Only include git-tracked files (GitHub Pages only deploys tracked files)
    tracked = get_tracked_files(website_path)

    def is_tracked(rel_path):
        """Check if a file is git-tracked. If git unavailable, allow all."""
        if tracked is None:
            return True
        # Normalize path separators for comparison
        return rel_path.replace('\\', '/') in tracked

    # Preserve existing lastmod dates for non-blog pages
    existing_lastmods = load_existing_lastmods(website_path / 'sitemap.xml')

    def get_lastmod(loc):
        return existing_lastmods.get(loc, today)

    # Collect URL entries grouped by section
    main_pages = []
    practice_pages = []
    spanish_pages = []
    category_pages = []
    blog_entries = []

    # --- 1. Root pages ---
    for html_file in sorted(website_path.glob('*.html')):
        filename = html_file.name
        if filename in EXCLUDED_ROOT:
            continue
        if not is_tracked(filename):
            continue

        config = ROOT_CONFIG.get(filename, ROOT_DEFAULT)
        loc = "https://lotterlaw.com/" if filename == 'index.html' else f"https://lotterlaw.com/{filename}"

        main_pages.append({
            'loc': loc,
            'lastmod': get_lastmod(loc),
            'changefreq': config['changefreq'],
            'priority': config['priority'],
            'hreflang': [],
        })

    # --- 2. Practice area pages ---
    es_dir = website_path / 'es' / 'practice-areas'
    spanish_filenames = set()
    if es_dir.exists():
        spanish_filenames = {f.name for f in es_dir.glob('*.html')
                            if is_tracked(f'es/practice-areas/{f.name}')}

    pa_dir = website_path / 'practice-areas'
    if pa_dir.exists():
        for html_file in sorted(pa_dir.glob('*.html')):
            filename = html_file.name
            if filename in EXCLUDED_PRACTICE_AREAS:
                continue
            if not is_tracked(f'practice-areas/{filename}'):
                continue

            loc = f"https://lotterlaw.com/practice-areas/{filename}"
            priority = PA_PRIORITY.get(filename, PA_DEFAULT_PRIORITY)

            entry = {
                'loc': loc,
                'lastmod': get_lastmod(loc),
                'changefreq': 'monthly',
                'priority': priority,
                'hreflang': [],
            }

            if filename in spanish_filenames:
                entry['hreflang'] = [
                    {'lang': 'en', 'href': f"https://lotterlaw.com/practice-areas/{filename}"},
                    {'lang': 'es', 'href': f"https://lotterlaw.com/es/practice-areas/{filename}"},
                    {'lang': 'x-default', 'href': f"https://lotterlaw.com/practice-areas/{filename}"},
                ]

            practice_pages.append(entry)

    # --- 3. Spanish practice area pages ---
    if es_dir.exists():
        for html_file in sorted(es_dir.glob('*.html')):
            filename = html_file.name
            if not is_tracked(f'es/practice-areas/{filename}'):
                continue
            loc = f"https://lotterlaw.com/es/practice-areas/{filename}"

            en_priority = PA_PRIORITY.get(filename, PA_DEFAULT_PRIORITY)
            priority_drop = {'0.9': '0.8', '0.8': '0.7', '0.7': '0.6', '0.6': '0.5'}
            priority = priority_drop.get(en_priority, '0.7')

            spanish_pages.append({
                'loc': loc,
                'lastmod': get_lastmod(loc),
                'changefreq': 'monthly',
                'priority': priority,
                'hreflang': [
                    {'lang': 'en', 'href': f"https://lotterlaw.com/practice-areas/{filename}"},
                    {'lang': 'es', 'href': f"https://lotterlaw.com/es/practice-areas/{filename}"},
                    {'lang': 'x-default', 'href': f"https://lotterlaw.com/practice-areas/{filename}"},
                ],
            })

    # --- 4. Blog category pages ---
    cat_dir = website_path / 'blog' / 'category'
    if cat_dir.exists():
        for html_file in sorted(cat_dir.glob('*.html')):
            if not is_tracked(f'blog/category/{html_file.name}'):
                continue
            loc = f"https://lotterlaw.com/blog/category/{html_file.name}"
            category_pages.append({
                'loc': loc,
                'lastmod': get_lastmod(loc),
                'changefreq': 'weekly',
                'priority': '0.6',
                'hreflang': [],
            })

    # --- 5. Blog posts (gated by blog.html) ---
    blog_dir = website_path / 'blog'
    blog_html_path = website_path / 'blog.html'

    listed_slugs = get_listed_blog_posts(blog_html_path)

    raw_posts = []
    skipped_count = 0
    for index_file in sorted(blog_dir.glob('*/index.html')):
        slug = index_file.parent.name
        if slug == 'category':
            continue
        if slug not in listed_slugs:
            skipped_count += 1
            continue
        if not is_tracked(f'blog/{slug}/index.html'):
            continue
        try:
            date, title = extract_metadata_from_html(index_file)
            raw_posts.append({'slug': slug, 'date': date, 'title': title})
        except Exception as e:
            print(f"Warning: Could not parse {slug}/index.html: {e}")

    raw_posts.sort(key=lambda x: x['date'])

    for post in raw_posts:
        post_date = datetime.strptime(post['date'], '%Y-%m-%d')
        days_old = (datetime.now() - post_date).days
        if days_old < 30:
            priority = '0.9'
        elif days_old < 90:
            priority = '0.8'
        else:
            priority = '0.7'

        blog_entries.append({
            'loc': f"https://lotterlaw.com/blog/{post['slug']}/",
            'lastmod': post['date'],
            'changefreq': 'monthly',
            'priority': priority,
            'hreflang': [],
        })

    # --- Build XML ---
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    sections = [
        ('Main Pages', main_pages),
        ('Practice Area Pages', practice_pages),
        ('Spanish Practice Area Pages', spanish_pages),
        ('Blog Category Pages', category_pages),
        ('Blog Posts (Auto-Generated)', blog_entries),
    ]

    for section_name, entries in sections:
        if not entries:
            continue

        lines.append(f'  <!-- {section_name} -->')

        for url in entries:
            lines.append('  <url>')
            lines.append(f'    <loc>{url["loc"]}</loc>')

            for hl in url.get('hreflang', []):
                lines.append(f'    <xhtml:link rel="alternate" hreflang="{hl["lang"]}" href="{hl["href"]}"/>')

            lines.append(f'    <lastmod>{url["lastmod"]}</lastmod>')
            lines.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
            lines.append(f'    <priority>{url["priority"]}</priority>')
            lines.append('  </url>')

        lines.append('')

    # Remove trailing blank line before closing tag
    if lines[-1] == '':
        lines.pop()
    lines.append('</urlset>')

    # Write sitemap
    output_file = website_path / 'sitemap.xml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    total = len(main_pages) + len(practice_pages) + len(spanish_pages) + len(category_pages) + len(blog_entries)
    print(f"[OK] Generated sitemap.xml with {total} URLs")
    print(f"     {len(main_pages)} main, {len(practice_pages)} practice areas, "
          f"{len(spanish_pages)} Spanish, {len(category_pages)} categories, "
          f"{len(blog_entries)} blog posts")
    if skipped_count > 0:
        print(f"     Skipped {skipped_count} staged post(s) not yet listed in blog.html")
    return total


if __name__ == '__main__':
    import sys
    website_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    generate_sitemap(website_dir)
