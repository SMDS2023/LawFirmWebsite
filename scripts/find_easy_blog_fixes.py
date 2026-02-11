#!/usr/bin/env python3
"""
Find blog posts that are close to optimal and easy to fix.
Focus on posts that are within 15 chars of target (150-160).
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from audit_all_meta_descriptions import audit_all_pages, OPTIMAL_LENGTH_MIN, OPTIMAL_LENGTH_MAX

def find_easy_fixes():
    """Find blog posts that are close to optimal length."""
    results = audit_all_pages()

    easy_fixes = {
        'too_short': [],
        'too_long': []
    }

    for page in results['blog_posts']:
        analysis = page['analysis']
        length = analysis['length']

        # Skip if no description or has other issues
        if length == 0:
            continue

        # Skip if missing location (harder fix)
        if not analysis['has_location']:
            continue

        # Find posts within 15 chars of target
        if 135 <= length < OPTIMAL_LENGTH_MIN:
            chars_needed = OPTIMAL_LENGTH_MIN - length
            easy_fixes['too_short'].append({
                'file': page['file'],
                'length': length,
                'chars_needed': chars_needed,
                'desc': page['description']
            })
        elif OPTIMAL_LENGTH_MAX < length <= 175:
            chars_to_cut = length - OPTIMAL_LENGTH_MAX
            easy_fixes['too_long'].append({
                'file': page['file'],
                'length': length,
                'chars_to_cut': chars_to_cut,
                'desc': page['description']
            })

    return easy_fixes

if __name__ == '__main__':
    fixes = find_easy_fixes()

    print("=" * 80)
    print("EASY BLOG POST FIXES (Within 15 chars of target)")
    print("=" * 80)

    print(f"\nTOO SHORT (need 1-15 more chars):")
    print("-" * 80)
    for post in sorted(fixes['too_short'], key=lambda x: x['chars_needed']):
        print(f"\n{post['file']}")
        print(f"  Current: {post['length']} chars (+{post['chars_needed']} needed)")
        print(f"  Text: {post['desc'][:100]}...")

    print(f"\n\nTOO LONG (need to cut 1-15 chars):")
    print("-" * 80)
    for post in sorted(fixes['too_long'], key=lambda x: x['chars_to_cut']):
        print(f"\n{post['file']}")
        print(f"  Current: {post['length']} chars (-{post['chars_to_cut']} to cut)")
        print(f"  Text: {post['desc'][:100]}...")

    print(f"\n\nSUMMARY:")
    print(f"  Easy too-short fixes: {len(fixes['too_short'])}")
    print(f"  Easy too-long fixes: {len(fixes['too_long'])}")
    print(f"  Total easy fixes: {len(fixes['too_short']) + len(fixes['too_long'])}")
