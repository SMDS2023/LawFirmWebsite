#!/usr/bin/env python3
"""
Backdate blog posts to ensure exactly one post per day.
Starts from the most recent date and works backward.
"""

import re
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Start date: One day before post #104 (which is 2026-02-22)
START_DATE = datetime(2026, 2, 21)

# Get list of blog post folders (excludes category folders)
blog_dir = Path("blog")
post_folders = sorted([
    d for d in blog_dir.iterdir()
    if d.is_dir() and d.name != "category" and (d / "index.html").exists()
], reverse=True)  # Newest first

print(f"Found {len(post_folders)} blog posts")
print(f"Starting backdate from {START_DATE.strftime('%Y-%m-%d')}")
print()

# Assign dates (one per day, going backward)
current_date = START_DATE
updates = []

for folder in post_folders:
    post_file = folder / "index.html"
    date_str = current_date.strftime("%Y-%m-%d")
    date_display = current_date.strftime("%B %d, %Y")

    updates.append({
        "folder": folder.name,
        "file": post_file,
        "old_date": None,  # Will extract
        "new_date": date_str,
        "new_display": date_display
    })

    # Move to previous day
    current_date -= timedelta(days=1)

print(f"Will backdate {len(updates)} posts")
print(f"Date range: {updates[-1]['new_date']} to {updates[0]['new_date']}")
print()

# Dry run: show what would be updated
auto_yes = len(sys.argv) > 1 and sys.argv[1] == "--yes"
if not auto_yes:
    input("Press Enter to preview changes (or Ctrl+C to cancel)...")

for i, update in enumerate(updates[:10], 1):  # Show first 10
    print(f"{i}. {update['folder'][:50]:50s} -> {update['new_date']}")

if len(updates) > 10:
    print(f"... and {len(updates) - 10} more")

print()

if len(sys.argv) > 1 and sys.argv[1] == "--yes":
    proceed = "yes"
else:
    proceed = input("Proceed with backdating? (yes/no): ")

if proceed.lower() != "yes":
    print("Cancelled.")
    exit(0)

# Update each post file
for update in updates:
    with open(update["file"], "r", encoding="utf-8") as f:
        content = f.read()

    # Update schema datePublished
    content = re.sub(
        r'"datePublished":\s*"[^"]*"',
        f'"datePublished": "{update["new_date"]}"',
        content
    )

    # Update schema dateModified
    content = re.sub(
        r'"dateModified":\s*"[^"]*"',
        f'"dateModified": "{update["new_date"]}"',
        content
    )

    # Update <time datetime>
    content = re.sub(
        r'<time datetime="[^"]*">([^<]*)</time>',
        f'<time datetime="{update["new_date"]}">{update["new_display"]}</time>',
        content
    )

    with open(update["file"], "w", encoding="utf-8") as f:
        f.write(content)

    print(f"OK Updated {update['folder']}")

print()
print(f"OK Updated {len(updates)} blog posts")
print()
print("Next steps:")
print("1. Update blog.html listing (manually or via script)")
print("2. Regenerate sitemap: python scripts/generate_sitemap.py .")
print("3. Git commit and push")
