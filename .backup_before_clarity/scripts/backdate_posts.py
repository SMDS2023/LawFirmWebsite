#!/usr/bin/env python3
"""
Backdate Posts - Sequential Dating

Sets a blog post's publish date to the day after the most recent post.

Usage:
    python backdate_posts.py blog/35-discovery-delays.html
"""

import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_most_recent_date(blog_dir: Path, exclude_file: str = None) -> datetime:
    """Find the most recent publish date from existing blog posts."""
    latest_date = None

    for post_file in blog_dir.glob("*.html"):
        if post_file.name == exclude_file or post_file.name == "index.html":
            continue

        try:
            content = post_file.read_text(encoding="utf-8")

            # Look for article:published_time meta tag
            match = re.search(r'article:published_time["\s]+content="(\d{4}-\d{2}-\d{2})', content)
            if match:
                date_str = match.group(1)
                post_date = datetime.strptime(date_str, "%Y-%m-%d")

                if latest_date is None or post_date > latest_date:
                    latest_date = post_date
                continue

            # Fallback: look for datePublished in schema
            match = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})', content)
            if match:
                date_str = match.group(1)
                post_date = datetime.strptime(date_str, "%Y-%m-%d")

                if latest_date is None or post_date > latest_date:
                    latest_date = post_date

        except Exception as e:
            print(f"  Warning: Could not parse date from {post_file.name}: {e}")

    return latest_date


def update_post_date(filepath: Path, new_date: datetime) -> bool:
    """Update all date references in a blog post."""
    content = filepath.read_text(encoding="utf-8")
    original = content
    date_str = new_date.strftime("%Y-%m-%d")
    date_display = new_date.strftime("%B %d, %Y")  # e.g., "December 11, 2025"
    date_display_short = new_date.strftime("%B %-d, %Y") if sys.platform != "win32" else new_date.strftime("%B %d, %Y").replace(" 0", " ")

    changes = 0

    # Update article:published_time meta tag
    pattern = r'(article:published_time["\s]+content=")(\d{4}-\d{2}-\d{2})(")'
    if re.search(pattern, content):
        content = re.sub(pattern, rf'\g<1>{date_str}\3', content)
        changes += 1

    # Update datePublished in JSON-LD schema
    pattern = r'("datePublished":\s*")(\d{4}-\d{2}-\d{2})(")'
    if re.search(pattern, content):
        content = re.sub(pattern, rf'\g<1>{date_str}\3', content)
        changes += 1

    # Update dateModified in JSON-LD schema
    pattern = r'("dateModified":\s*")(\d{4}-\d{2}-\d{2})(")'
    if re.search(pattern, content):
        content = re.sub(pattern, rf'\g<1>{date_str}\3', content)
        changes += 1

    # Update <time datetime=""> tags
    pattern = r'(<time datetime=")(\d{4}-\d{2}-\d{2})(">)'
    if re.search(pattern, content):
        content = re.sub(pattern, rf'\g<1>{date_str}\3', content)
        changes += 1

    # Update display dates like "December 11, 2025" or "Published on December 11, 2025"
    # Match various date formats: December 11, 2025 or December 2, 2025
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    for month in months:
        pattern = rf'({month}\s+\d{{1,2}},\s+\d{{4}})'
        if re.search(pattern, content):
            content = re.sub(pattern, date_display_short, content, count=1)
            changes += 1
            break

    # Update text like "December 11, 2025 | Orlando, Florida"
    pattern = r'(\d{4}-\d{2}-\d{2}\s*\|\s*Orlando)'
    if re.search(pattern, content):
        content = re.sub(pattern, rf'{date_display_short} | Orlando', content)

    if content != original:
        filepath.write_text(content, encoding="utf-8")
        return True

    return False


def update_blog_listing(blog_html: Path, post_filename: str, new_date: datetime) -> bool:
    """Update the date in blog.html for the specified post."""
    if not blog_html.exists():
        print(f"  Warning: blog.html not found at {blog_html}")
        return False

    content = blog_html.read_text(encoding="utf-8")
    original = content
    date_str = new_date.strftime("%Y-%m-%d")
    date_display = new_date.strftime("%B %-d, %Y") if sys.platform != "win32" else new_date.strftime("%B %d, %Y").replace(" 0", " ")

    # Find the blog entry for this post and update its date
    # Pattern to find the post entry and its datetime
    post_pattern = rf'(href="blog/{re.escape(post_filename)}".*?<time datetime=")(\d{{4}}-\d{{2}}-\d{{2}})(">)([^<]*)(</time>)'

    def replace_date(match):
        return f'{match.group(1)}{date_str}{match.group(3)}{date_display}{match.group(5)}'

    content = re.sub(post_pattern, replace_date, content, flags=re.DOTALL)

    # Also try alternate pattern with different quote style
    post_pattern = rf'(href="blog\\\\{re.escape(post_filename)}".*?<time datetime=")(\d{{4}}-\d{{2}}-\d{{2}})(">)([^<]*)(</time>)'
    content = re.sub(post_pattern, replace_date, content, flags=re.DOTALL)

    if content != original:
        blog_html.write_text(content, encoding="utf-8")
        return True

    return False


def main():
    parser = argparse.ArgumentParser(description="Set blog post date to day after most recent post")
    parser.add_argument("filepath", help="Path to the blog post")
    parser.add_argument("--date", help="Override date (YYYY-MM-DD format)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    args = parser.parse_args()

    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    blog_dir = filepath.parent
    blog_html = blog_dir.parent / "blog.html"

    print("=" * 60)
    print("BACKDATE POSTS")
    print("=" * 60)
    print(f"Target: {filepath.name}")
    print()

    if args.date:
        # Use provided date
        new_date = datetime.strptime(args.date, "%Y-%m-%d")
        print(f"Using provided date: {new_date.strftime('%Y-%m-%d')}")
    else:
        # Find most recent date and add one day
        latest = find_most_recent_date(blog_dir, exclude_file=filepath.name)
        if latest:
            new_date = latest + timedelta(days=1)
            print(f"Most recent post date: {latest.strftime('%Y-%m-%d')}")
            print(f"New post date: {new_date.strftime('%Y-%m-%d')}")
        else:
            new_date = datetime.now()
            print(f"No existing dates found, using today: {new_date.strftime('%Y-%m-%d')}")

    print()

    if args.dry_run:
        print(f"[DRY RUN] Would set date to: {new_date.strftime('%B %d, %Y')}")
        sys.exit(0)

    # Update the blog post
    print("Updating dates...")
    post_updated = update_post_date(filepath, new_date)
    listing_updated = update_blog_listing(blog_html, filepath.name, new_date)

    print()
    print("-" * 60)
    print(f"Post updated: {'Yes' if post_updated else 'No changes needed'}")
    print(f"blog.html updated: {'Yes' if listing_updated else 'No changes needed'}")
    print(f"New date: {new_date.strftime('%B %d, %Y')} ({new_date.strftime('%Y-%m-%d')})")
    print("-" * 60)


if __name__ == "__main__":
    main()
