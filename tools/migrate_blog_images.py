#!/usr/bin/env python3
"""
Blog Image Migration Tool
Fixes HTML paths for posts that have images in correct location but HTML points elsewhere
"""

import json
import re
from pathlib import Path
import shutil
from datetime import datetime

def load_manifest(manifest_path):
    """Load the audit manifest"""
    with open(manifest_path, 'r') as f:
        return json.load(f)

def build_migration_plan(manifest):
    """
    Build migration plan for posts that have images but wrong HTML paths

    Returns dict with:
    - html_updates: [{slug, file, old_path, new_path, backup}, ...]
    - stats: summary counts
    """
    plan = {
        "html_updates": [],
        "stats": {
            "total_posts": len(manifest['posts']),
            "needs_html_fix": 0,
            "needs_images": 0,
            "already_correct": 0
        }
    }

    for slug, info in manifest['posts'].items():
        # Skip if no HTML file
        if not info['has_html']:
            continue

        # Skip if already correct
        if info['image_location'] == 'CORRECT' and info.get('image_exists') != False:
            plan['stats']['already_correct'] += 1
            continue

        # If has images in folder but wrong HTML path
        if info['image_files'] and info['image_location'] != 'CORRECT':
            # Only fix if og.jpg or hero.jpg actually exist
            has_og = 'og.jpg' in info['image_files']
            has_hero = 'hero.jpg' in info['image_files']

            if not (has_og or has_hero):
                # Skip - no standard images to point to
                continue

            clean_slug = info['clean_slug']
            html_file = Path(f"blog/{slug}/index.html")

            if not html_file.exists():
                continue

            # Expected correct paths
            new_og = f"https://lotterlaw.com/blog/{clean_slug}/images/og.jpg"
            new_hero = f"https://lotterlaw.com/blog/{clean_slug}/images/hero.jpg"

            update_entry = {
                "slug": slug,
                "clean_slug": clean_slug,
                "file": str(html_file),
                "backup": str(html_file.with_suffix('.html.backup')),
                "old_og_path": info.get('og_image_path', 'NONE'),
                "new_og_path": new_og,
                "new_hero_path": new_hero,
                "has_og": has_og,
                "has_hero": has_hero
            }

            plan['html_updates'].append(update_entry)
            plan['stats']['needs_html_fix'] += 1

        # If no images at all
        elif not info['image_files']:
            plan['stats']['needs_images'] += 1

    return plan

def dry_run_migration(plan):
    """Simulate migration without touching files"""
    print("=" * 80)
    print("DRY RUN MODE - No files will be modified")
    print("=" * 80)
    print()

    print("[STATISTICS]")
    print(f"  Total posts: {plan['stats']['total_posts']}")
    print(f"  Already correct: {plan['stats']['already_correct']}")
    print(f"  Need HTML path fix: {plan['stats']['needs_html_fix']}")
    print(f"  Need images created: {plan['stats']['needs_images']}")
    print()

    if plan['html_updates']:
        print("[HTML UPDATES]")
        for update in plan['html_updates'][:5]:  # Show first 5
            print(f"\n  Post: {update['slug']}")
            print(f"    File: {update['file']}")
            print(f"    Old: {update['old_og_path']}")
            print(f"    New: {update['new_og_path']}")
            if not update['has_og']:
                print(f"    WARNING: og.jpg missing in images folder!")
            if not update['has_hero']:
                print(f"    WARNING: hero.jpg missing in images folder!")

        if len(plan['html_updates']) > 5:
            print(f"\n  ... and {len(plan['html_updates']) - 5} more")

    print()
    print("=" * 80)
    print(f"Ready to fix {plan['stats']['needs_html_fix']} posts")
    print("Run with --execute to apply changes")
    print("=" * 80)

def execute_migration(plan):
    """Execute the migration"""
    print("=" * 80)
    print("EXECUTING MIGRATION")
    print("=" * 80)
    print()

    success_count = 0
    error_count = 0

    for update in plan['html_updates']:
        try:
            html_file = Path(update['file'])
            backup_file = Path(update['backup'])

            # Read HTML
            content = html_file.read_text(encoding='utf-8', errors='ignore')

            # Backup original
            shutil.copy2(html_file, backup_file)

            # Update og:image
            og_pattern = r'<meta property="og:image" content="[^"]*"'
            og_replacement = f'<meta property="og:image" content="{update["new_og_path"]}"'
            content = re.sub(og_pattern, og_replacement, content)

            # Update twitter:image
            twitter_pattern = r'<meta name="twitter:image" content="[^"]*"'
            twitter_replacement = f'<meta name="twitter:image" content="{update["new_og_path"]}"'
            content = re.sub(twitter_pattern, twitter_replacement, content)

            # Update Schema.org image (if present)
            schema_pattern = r'"image":\s*"[^"]*"'
            schema_replacement = f'"image": "{update["new_og_path"]}"'
            content = re.sub(schema_pattern, schema_replacement, content)

            # Write updated HTML
            html_file.write_text(content, encoding='utf-8')

            print(f"[OK] {update['slug']}")
            success_count += 1

        except Exception as e:
            print(f"[ERROR] {update['slug']}: {e}")
            error_count += 1

    print()
    print("=" * 80)
    print("MIGRATION COMPLETE")
    print("=" * 80)
    print(f"  Success: {success_count}")
    print(f"  Errors: {error_count}")
    print(f"  Backups: *.html.backup files created")
    print()

    # Generate rollback script
    rollback_path = Path("ROLLBACK.sh")
    with open(rollback_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Rollback blog image migration\n")
        f.write("# Generated: " + datetime.now().isoformat() + "\n\n")

        for update in plan['html_updates']:
            f.write(f"mv \"{update['backup']}\" \"{update['file']}\"\n")

    rollback_path.chmod(0o755)
    print(f"Rollback script: {rollback_path}")
    print("To rollback: bash ROLLBACK.sh")
    print()

def validate_migration():
    """Validate that all links work after migration"""
    print("=" * 80)
    print("VALIDATING MIGRATION")
    print("=" * 80)
    print()

    blog_dir = Path("blog")
    broken_count = 0
    checked_count = 0

    for post_dir in blog_dir.iterdir():
        if not post_dir.is_dir() or post_dir.name == "images":
            continue

        html_file = post_dir / "index.html"
        if not html_file.exists():
            continue

        content = html_file.read_text(encoding='utf-8', errors='ignore')

        # Extract og:image path
        match = re.search(r'<meta property="og:image" content="([^"]+)"', content)
        if not match:
            continue

        og_url = match.group(1)

        # Convert URL to file path
        file_path = Path(og_url.replace("https://lotterlaw.com/", ""))

        checked_count += 1

        if not file_path.exists():
            print(f"[BROKEN] {post_dir.name}: {og_url}")
            broken_count += 1

    print()
    print("=" * 80)
    print(f"Checked: {checked_count} posts")
    print(f"Broken links: {broken_count}")

    if broken_count == 0:
        print("[OK] All image links valid!")
    else:
        print("[WARN] Some broken links found - review above")

    print("=" * 80)

if __name__ == "__main__":
    import sys

    # Parse args
    mode = "dry-run"
    manifest_path = "../Blog/.index/blog_image_state.json"

    if "--execute" in sys.argv:
        mode = "execute"
    elif "--validate" in sys.argv:
        mode = "validate"

    if "--manifest" in sys.argv:
        idx = sys.argv.index("--manifest")
        if idx + 1 < len(sys.argv):
            manifest_path = sys.argv[idx + 1]

    # Run migration
    if mode == "validate":
        validate_migration()
    else:
        manifest = load_manifest(manifest_path)
        plan = build_migration_plan(manifest)

        if mode == "dry-run":
            dry_run_migration(plan)
        else:
            execute_migration(plan)
            print("\nRunning post-migration validation...\n")
            validate_migration()
