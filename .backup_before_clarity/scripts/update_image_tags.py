#!/usr/bin/env python3
"""
Update Image Tags Script for LotterLaw Website
================================================
Adds width/height attributes and lazy loading to images in HTML files.

Usage:
    python update_image_tags.py --audit          # Show what would be changed
    python update_image_tags.py --update         # Apply changes
    python update_image_tags.py --fix            # Fix corrupted tags from previous run

Requirements:
    pip install Pillow
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, Tuple, Optional

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

# Configuration
WEBSITE_DIR = Path(__file__).parent.parent
ASSETS_DIR = WEBSITE_DIR / "assets"

# Images that should NOT be lazy loaded (above fold / critical)
NO_LAZY_PATTERNS = [
    r'logo',
    r'header-logo',
    r'hero',
]


def build_dimensions_lookup() -> Dict[str, Tuple[int, int]]:
    """Build a lookup dict of image filename -> (width, height)."""
    dimensions = {}

    for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
        for path in ASSETS_DIR.glob(ext):
            try:
                with Image.open(path) as img:
                    dimensions[path.name] = img.size
            except Exception as e:
                print(f"  WARNING: Could not get dimensions for {path.name}: {e}")

    return dimensions


def should_lazy_load(img_tag: str, img_src: str) -> bool:
    """Determine if an image should have lazy loading."""
    for pattern in NO_LAZY_PATTERNS:
        if re.search(pattern, img_tag, re.IGNORECASE):
            return False
        if re.search(pattern, img_src, re.IGNORECASE):
            return False

    if img_src.startswith('http'):
        return False

    return True


def extract_filename_from_src(src: str) -> Optional[str]:
    """Extract filename from src attribute."""
    if not src or src.startswith('http'):
        return None

    filename = src.split('/')[-1]
    filename = filename.split('?')[0]
    return filename


def update_img_tag(img_tag: str, dimensions: Dict[str, Tuple[int, int]]) -> Tuple[str, bool]:
    """Update a single img tag with dimensions and lazy loading."""
    original = img_tag
    modified = False

    # Extract src
    src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
    if not src_match:
        return img_tag, False

    src = src_match.group(1)
    filename = extract_filename_from_src(src)

    # Skip tags that have onerror with innerHTML (complex tags)
    # These already have proper dimensions or would be corrupted by our regex
    if 'onerror=' in img_tag and 'innerHTML' in img_tag:
        # For these, only add loading="lazy" if appropriate and not already present
        if should_lazy_load(img_tag, src) and 'loading=' not in img_tag:
            # Find the closing > that's not inside a quoted string
            # This is tricky, so we'll skip lazy loading for complex onerror tags
            pass
        return img_tag, False

    # Add width/height if we have dimensions and they're not already present
    if filename and filename in dimensions:
        width, height = dimensions[filename]

        has_width = re.search(r'\bwidth\s*=\s*["\']?\d+', img_tag)
        has_height = re.search(r'\bheight\s*=\s*["\']?\d+', img_tag)

        if not has_width or not has_height:
            # Find position right before the closing >
            # Be careful not to match > inside attribute values
            close_pos = img_tag.rfind('>')
            if close_pos > 0:
                insert_pos = close_pos
                # Handle self-closing />
                if img_tag[close_pos-1:close_pos] == '/':
                    insert_pos = close_pos - 1

                attrs_to_add = ''
                if not has_width:
                    attrs_to_add += f' width="{width}"'
                if not has_height:
                    attrs_to_add += f' height="{height}"'

                img_tag = img_tag[:insert_pos] + attrs_to_add + img_tag[insert_pos:]
                modified = True

    # Add lazy loading if appropriate and not already present
    if should_lazy_load(img_tag, src) and 'loading=' not in img_tag:
        close_pos = img_tag.rfind('>')
        if close_pos > 0:
            insert_pos = close_pos
            if img_tag[close_pos-1:close_pos] == '/':
                insert_pos = close_pos - 1

            img_tag = img_tag[:insert_pos] + ' loading="lazy"' + img_tag[insert_pos:]
            modified = True

    return img_tag, modified


def fix_corrupted_tags(content: str) -> Tuple[str, int]:
    """Fix tags that were corrupted by previous run."""
    fixes = 0

    # Pattern to find corrupted innerHTML with width/height inside the span
    # Example: '<span class=\'text-2xl font-bold text-blue-800\' width="1784" height="544">Lotter Law</span>'
    pattern = re.compile(
        r"(<span[^>]*)'(\s+width=\"\d+\"\s+height=\"\d+\")>",
        re.IGNORECASE
    )

    def fix_match(m):
        nonlocal fixes
        fixes += 1
        # Remove the width/height from inside the span, restore the closing '
        return m.group(1) + "'>"

    content = pattern.sub(fix_match, content)

    return content, fixes


def process_html_file(filepath: Path, dimensions: Dict[str, Tuple[int, int]],
                      dry_run: bool = True, fix_mode: bool = False) -> int:
    """Process a single HTML file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}")
        return 0

    if fix_mode:
        new_content, fixes = fix_corrupted_tags(content)
        if fixes > 0:
            if not dry_run:
                filepath.write_text(new_content, encoding='utf-8')
                print(f"  Fixed {fixes} corrupted tags in {filepath.name}")
            else:
                print(f"  Would fix {fixes} corrupted tags in {filepath.name}")
        return fixes

    # Find all img tags - match from <img to the first > that's not inside quotes
    # This is a simple approach that works for well-formed HTML
    img_pattern = re.compile(r'<img\s+[^>]+>', re.IGNORECASE)

    changes = []

    def replace_img(match):
        img_tag = match.group(0)
        updated_tag, was_modified = update_img_tag(img_tag, dimensions)
        if was_modified:
            changes.append((img_tag, updated_tag))
        return updated_tag

    new_content = img_pattern.sub(replace_img, content)

    if changes:
        if dry_run:
            print(f"\n  {filepath.relative_to(WEBSITE_DIR)}:")
            for old, new in changes[:3]:
                print(f"    - Would update img tag")
            if len(changes) > 3:
                print(f"    ... and {len(changes) - 3} more")
        else:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"  Updated {len(changes)} images in {filepath.name}")

    return len(changes)


def main():
    parser = argparse.ArgumentParser(description='Update image tags in HTML files')
    parser.add_argument('--audit', action='store_true', help='Show what would be changed (dry run)')
    parser.add_argument('--update', action='store_true', help='Apply changes')
    parser.add_argument('--fix', action='store_true', help='Fix corrupted tags from previous run')

    args = parser.parse_args()

    if not args.audit and not args.update and not args.fix:
        args.audit = True

    dry_run = args.audit and not args.update and not args.fix

    print("Building dimensions lookup from assets...")
    dimensions = build_dimensions_lookup()
    print(f"  Found dimensions for {len(dimensions)} images")

    action = 'Fixing' if args.fix else ('Auditing' if dry_run else 'Updating')
    print(f"\n{action} HTML files...")

    html_files = list(WEBSITE_DIR.glob('*.html'))
    html_files.extend(WEBSITE_DIR.glob('blog/*.html'))
    html_files.extend(WEBSITE_DIR.glob('practice-areas/*.html'))

    total_changes = 0
    files_changed = 0

    for filepath in sorted(html_files):
        changes = process_html_file(filepath, dimensions, dry_run=dry_run, fix_mode=args.fix)
        if changes:
            total_changes += changes
            files_changed += 1

    verb = 'Would fix' if args.fix and dry_run else ('Fixed' if args.fix else ('Would update' if dry_run else 'Updated'))
    print(f"\n{verb} {total_changes} {'tags' if args.fix else 'images'} in {files_changed} files")

    if dry_run and not args.fix:
        print("\nRun with --update to apply changes")


if __name__ == '__main__':
    main()
