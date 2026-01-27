#!/usr/bin/env python3
"""
Add Mobile CTA Bar to LotterLaw Website Pages
==============================================
Adds a sticky mobile CTA bar with click-to-call functionality
to all public-facing HTML pages.
"""

import os
import re
from pathlib import Path

# Mobile CTA bar HTML component with urgency messaging and GA4 tracking
MOBILE_CTA_HTML = '''
    <!-- Mobile Sticky CTA Bar -->
    <div class="mobile-cta-bar urgent" id="mobile-cta-bar">
        <a href="tel:407-500-7000"
           onclick="if(typeof gtag === 'function') gtag('event', 'click_to_call', {event_category: 'CTA', event_label: 'Mobile Sticky Bar', phone_number: '407-500-7000'});"
           aria-label="Call Lotter Law for a free consultation">
            <svg class="cta-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            <span class="cta-text">
                <span class="cta-text-main">Free Consultation</span>
                <span class="cta-text-sub">Call Now: 407-500-7000</span>
            </span>
        </a>
    </div>
'''

# Pages to skip (internal/system files)
SKIP_PATTERNS = [
    'analytics/',
    'templates/',
    'practice-area-template',
]

def should_skip(filepath: str) -> bool:
    """Check if file should be skipped."""
    for pattern in SKIP_PATTERNS:
        if pattern in filepath:
            return True
    return False

def has_mobile_cta(content: str) -> bool:
    """Check if page already has mobile CTA bar."""
    return 'mobile-cta-bar' in content

def add_mobile_cta(filepath: Path) -> bool:
    """Add mobile CTA bar to HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already has CTA
        if has_mobile_cta(content):
            print(f"  SKIP (already has CTA): {filepath.name}")
            return False

        # Find the closing </body> tag and insert CTA before it
        if '</body>' not in content:
            print(f"  SKIP (no </body> tag): {filepath.name}")
            return False

        # Insert CTA bar just before </body>
        new_content = content.replace('</body>', f'{MOBILE_CTA_HTML}\n</body>')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ADDED: {filepath.name}")
        return True

    except Exception as e:
        print(f"  ERROR ({filepath.name}): {e}")
        return False

def main():
    """Add mobile CTA bar to all public HTML pages."""
    website_dir = Path(__file__).parent.parent

    # Find all HTML files
    html_files = list(website_dir.glob('*.html'))
    html_files.extend(website_dir.glob('blog/*.html'))
    html_files.extend(website_dir.glob('practice-areas/*.html'))

    print("Adding Mobile CTA Bar to LotterLaw Website")
    print("=" * 50)

    added_count = 0
    skipped_count = 0

    for filepath in sorted(html_files):
        if should_skip(str(filepath)):
            print(f"  SKIP (pattern match): {filepath.name}")
            skipped_count += 1
            continue

        if add_mobile_cta(filepath):
            added_count += 1
        else:
            skipped_count += 1

    print("=" * 50)
    print(f"Added to: {added_count} files")
    print(f"Skipped: {skipped_count} files")

if __name__ == '__main__':
    main()
