#!/usr/bin/env python3
"""
Remove hardcoded Microsoft Clarity scripts from all HTML files.
Now that Clarity is managed via GTM, remove the duplicate hardcoded scripts.
"""

import os
import re
from pathlib import Path

# Pattern to match the entire Clarity script block including comments
# More flexible pattern to handle various whitespace/formatting
CLARITY_PATTERN = re.compile(
    r'<!--\s*Microsoft Clarity\s*-->.*?'
    r'<script[^>]*>.*?reu4dibx4h.*?</script>.*?'
    r'<!--\s*End Microsoft Clarity\s*-->\s*',
    re.DOTALL | re.IGNORECASE
)

def remove_clarity_from_file(filepath):
    """Remove Clarity script from a single HTML file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        original_content = content

        # Remove the Clarity script block
        content = CLARITY_PATTERN.sub('', content)

        if content != original_content:
            filepath.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Find and remove Clarity scripts from all HTML files."""
    website_dir = Path(r"C:\Users\jeff\OneDrive\Documents\LotterLaw\Website")

    print("="*70)
    print("  REMOVING HARDCODED MICROSOFT CLARITY SCRIPTS")
    print("="*70)
    print(f"\nSearching in: {website_dir}")
    print("\nClarity is now managed via GTM, removing duplicate hardcoded scripts...\n")

    # Find all HTML files recursively
    html_files = list(website_dir.rglob('*.html'))

    # Exclude backup and output directories
    html_files = [f for f in html_files if '.backup' not in str(f) and 'output' not in str(f)]

    modified_count = 0
    skipped_count = 0

    for filepath in html_files:
        if remove_clarity_from_file(filepath):
            print(f"[REMOVED] {filepath.relative_to(website_dir)}")
            modified_count += 1
        else:
            skipped_count += 1

    print("\n" + "="*70)
    print("  SUMMARY")
    print("="*70)
    print(f"Files modified: {modified_count}")
    print(f"Files skipped (no Clarity found): {skipped_count}")
    print(f"Total files checked: {len(html_files)}")
    print("\n[OK] Clarity script removal complete!")
    print("\nNext steps:")
    print("1. Test your website to verify Clarity still works via GTM")
    print("2. Check https://clarity.microsoft.com for session recordings")
    print("3. Commit the changes to git when ready")

if __name__ == "__main__":
    main()
