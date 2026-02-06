#!/usr/bin/env python3
"""
Regenerative Sitemap Generator for LotterLaw Website

Scans blog directory and generates complete sitemap.xml from scratch.
Self-healing: Always reflects current filesystem state.
"""

import re
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

def extract_metadata_from_html(html_file):
    """Extract publish date and title from blog post HTML."""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract datePublished from Schema.org JSON-LD
    date_match = re.search(r'"datePublished":\s*"([^"]+)"', content)
    date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")

    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else ""

    return date, title

def get_listed_blog_posts(blog_html_path):
    """Extract blog post filenames that are actually listed in blog.html.

    This ensures only published posts appear in sitemap, not staged posts.
    """
    with open(blog_html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all blog post links in blog.html
    # Pattern: href="blog/XX-slug.html" or href="/blog/XX-slug.html"
    pattern = r'href="/?blog/([^"]+\.html)"'
    matches = re.findall(pattern, content)

    return set(matches)  # Return unique filenames

def generate_sitemap(website_dir):
    """Generate complete sitemap.xml from filesystem."""
    website_path = Path(website_dir)
    blog_dir = website_path / 'blog'
    blog_html_path = website_path / 'blog.html'

    # Get posts that are actually listed in blog.html (not staged posts)
    listed_posts = get_listed_blog_posts(blog_html_path)

    # Get all blog posts, but only include those in the listing
    blog_posts = []
    skipped_count = 0
    for html_file in sorted(blog_dir.glob('*.html')):
        # Skip posts not yet listed (staged posts)
        if html_file.name not in listed_posts:
            skipped_count += 1
            continue

        try:
            date, title = extract_metadata_from_html(html_file)
            blog_posts.append({
                'filename': html_file.name,
                'date': date,
                'title': title
            })
        except Exception as e:
            print(f"Warning: Could not parse {html_file.name}: {e}")

    # Build sitemap XML
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <!-- Main Pages -->',
    ]

    # Add non-blog pages (read from current sitemap.xml)
    current_sitemap = website_path / 'sitemap.xml'
    if current_sitemap.exists():
        tree = ET.parse(current_sitemap)
        root = tree.getroot()
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        for url_elem in root.findall('sm:url', ns):
            loc = url_elem.find('sm:loc', ns).text
            if '/blog/' not in loc:
                # Preserve non-blog URLs as-is
                sitemap_lines.append('  <url>')
                sitemap_lines.append(f'    <loc>{loc}</loc>')

                lastmod = url_elem.find('sm:lastmod', ns)
                if lastmod is not None:
                    sitemap_lines.append(f'    <lastmod>{lastmod.text}</lastmod>')

                changefreq = url_elem.find('sm:changefreq', ns)
                if changefreq is not None:
                    sitemap_lines.append(f'    <changefreq>{changefreq.text}</changefreq>')

                priority = url_elem.find('sm:priority', ns)
                if priority is not None:
                    sitemap_lines.append(f'    <priority>{priority.text}</priority>')

                sitemap_lines.append('  </url>')

    # Add blog posts section
    sitemap_lines.append('')
    sitemap_lines.append('  <!-- Blog Posts (Auto-Generated) -->')

    # Sort by date (oldest first)
    blog_posts.sort(key=lambda x: x['date'])

    for post in blog_posts:
        sitemap_lines.append('  <url>')
        sitemap_lines.append(f'    <loc>https://lotterlaw.com/blog/{post["filename"]}</loc>')
        sitemap_lines.append(f'    <lastmod>{post["date"]}</lastmod>')
        sitemap_lines.append('    <changefreq>monthly</changefreq>')

        # Priority based on age
        post_date = datetime.strptime(post['date'], '%Y-%m-%d')
        days_old = (datetime.now() - post_date).days

        if days_old < 30:
            priority = '0.9'
        elif days_old < 90:
            priority = '0.8'
        else:
            priority = '0.7'

        sitemap_lines.append(f'    <priority>{priority}</priority>')
        sitemap_lines.append('  </url>')

    sitemap_lines.append('</urlset>')

    # Write sitemap
    output_file = website_path / 'sitemap.xml'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sitemap_lines))

    print(f"[OK] Generated sitemap.xml with {len(blog_posts)} blog posts")
    if skipped_count > 0:
        print(f"     Skipped {skipped_count} staged post(s) not yet listed in blog.html")
    return len(blog_posts)

if __name__ == '__main__':
    import sys
    website_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    generate_sitemap(website_dir)
