#!/usr/bin/env python3
"""
update_sitemap.py - Add or remove URLs from sitemap.xml

Usage:
    python update_sitemap.py add blog/82-stand-your-ground.html
    python update_sitemap.py add blog/82-stand-your-ground.html --priority 0.7
    python update_sitemap.py remove blog/old-post.html
    python update_sitemap.py list --filter blog/
    python update_sitemap.py check blog/82-stand-your-ground.html

Part of the LotterLaw blog publishing workflow.
"""

import argparse
import re
from datetime import datetime
from pathlib import Path

# Configuration
SITEMAP_PATH = Path(__file__).parent.parent / "sitemap.xml"
BASE_URL = "https://lotterlaw.com"

# Default priorities by content type
PRIORITIES = {
    "blog/": 0.6,
    "practice-areas/": 0.8,
    "": 0.5  # default
}

def get_priority(path: str) -> str:
    """Determine priority based on URL path."""
    for prefix, priority in PRIORITIES.items():
        if path.startswith(prefix):
            return str(priority)
    return "0.5"

def read_sitemap() -> str:
    """Read sitemap.xml content."""
    if not SITEMAP_PATH.exists():
        raise FileNotFoundError(f"Sitemap not found: {SITEMAP_PATH}")
    return SITEMAP_PATH.read_text(encoding="utf-8")

def write_sitemap(content: str) -> None:
    """Write sitemap.xml content."""
    SITEMAP_PATH.write_text(content, encoding="utf-8")
    print(f"Updated: {SITEMAP_PATH}")

def url_exists(content: str, path: str) -> bool:
    """Check if URL already exists in sitemap."""
    full_url = f"{BASE_URL}/{path}"
    return full_url in content

def add_url(path: str, priority: str = None, changefreq: str = "monthly") -> bool:
    """
    Add a URL to sitemap.xml.

    Args:
        path: Relative path (e.g., "blog/82-slug.html")
        priority: Priority value (0.0-1.0), auto-detected if None
        changefreq: Change frequency (daily, weekly, monthly, yearly)

    Returns:
        True if added, False if already exists
    """
    content = read_sitemap()

    # Check if already exists
    if url_exists(content, path):
        print(f"URL already exists: {BASE_URL}/{path}")
        return False

    # Auto-detect priority if not specified
    if priority is None:
        priority = get_priority(path)

    # Get today's date for lastmod
    today = datetime.now().strftime("%Y-%m-%d")

    # Create new URL entry
    new_entry = f"""  <url>
    <loc>{BASE_URL}/{path}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
</urlset>"""

    # Insert before closing </urlset> tag
    if "</urlset>" in content:
        content = content.replace("</urlset>", new_entry)
        write_sitemap(content)
        print(f"Added: {BASE_URL}/{path}")
        print(f"  lastmod: {today}")
        print(f"  priority: {priority}")
        print(f"  changefreq: {changefreq}")
        return True
    else:
        print("Error: Could not find </urlset> tag in sitemap")
        return False

def remove_url(path: str) -> bool:
    """
    Remove a URL from sitemap.xml.

    Args:
        path: Relative path (e.g., "blog/old-post.html")

    Returns:
        True if removed, False if not found
    """
    content = read_sitemap()
    full_url = f"{BASE_URL}/{path}"

    if not url_exists(content, path):
        print(f"URL not found: {full_url}")
        return False

    # Pattern to match the entire <url>...</url> block containing this URL
    pattern = rf'\s*<url>\s*<loc>{re.escape(full_url)}</loc>.*?</url>'

    new_content, count = re.subn(pattern, '', content, flags=re.DOTALL)

    if count > 0:
        write_sitemap(new_content)
        print(f"Removed: {full_url}")
        return True
    else:
        print(f"Error: Could not remove URL pattern")
        return False

def list_urls(filter_prefix: str = None) -> list:
    """
    List all URLs in sitemap, optionally filtered by prefix.

    Args:
        filter_prefix: Optional prefix to filter (e.g., "blog/")

    Returns:
        List of URLs
    """
    content = read_sitemap()

    # Extract all URLs
    pattern = r'<loc>([^<]+)</loc>'
    urls = re.findall(pattern, content)

    # Filter if prefix specified
    if filter_prefix:
        filter_url = f"{BASE_URL}/{filter_prefix}"
        urls = [u for u in urls if u.startswith(filter_url)]

    return urls

def check_url(path: str) -> bool:
    """
    Check if a URL exists in the sitemap.

    Args:
        path: Relative path to check

    Returns:
        True if exists, False otherwise
    """
    content = read_sitemap()
    exists = url_exists(content, path)

    full_url = f"{BASE_URL}/{path}"
    if exists:
        print(f"Found: {full_url}")
    else:
        print(f"Not found: {full_url}")

    return exists

def main():
    parser = argparse.ArgumentParser(
        description="Manage sitemap.xml URLs for LotterLaw website"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a URL to sitemap")
    add_parser.add_argument("path", help="Relative path (e.g., blog/82-slug.html)")
    add_parser.add_argument("--priority", "-p", help="Priority (0.0-1.0)")
    add_parser.add_argument("--changefreq", "-c", default="monthly",
                          choices=["daily", "weekly", "monthly", "yearly"],
                          help="Change frequency")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a URL from sitemap")
    remove_parser.add_argument("path", help="Relative path to remove")

    # List command
    list_parser = subparsers.add_parser("list", help="List URLs in sitemap")
    list_parser.add_argument("--filter", "-f", help="Filter by prefix (e.g., blog/)")

    # Check command
    check_parser = subparsers.add_parser("check", help="Check if URL exists")
    check_parser.add_argument("path", help="Relative path to check")

    args = parser.parse_args()

    if args.command == "add":
        add_url(args.path, args.priority, args.changefreq)
    elif args.command == "remove":
        remove_url(args.path)
    elif args.command == "list":
        urls = list_urls(args.filter)
        print(f"Found {len(urls)} URLs:")
        for url in urls:
            print(f"  {url}")
    elif args.command == "check":
        check_url(args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
