#!/usr/bin/env python3
"""
Comprehensive meta description audit for all website pages.
Checks every HTML file for meta description quality.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Configuration
WEBSITE_DIR = Path(__file__).parent.parent
OPTIMAL_LENGTH_MIN = 150
OPTIMAL_LENGTH_MAX = 160
LOCATION_KEYWORDS = ['orlando', 'florida', 'central florida', 'orange county', 'seminole', 'osceola']

def extract_meta_description(html_file):
    """Extract meta description from HTML file."""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Check standard meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content']

        # Check OG description as fallback
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc and og_desc.get('content'):
            return og_desc['content']

        return None

    except Exception as e:
        return f"ERROR: {str(e)}"

def analyze_description(desc):
    """Analyze meta description quality."""
    if desc is None:
        return {
            'length': 0,
            'has_location': False,
            'optimal_length': False,
            'issues': ['MISSING - No meta description found']
        }

    if isinstance(desc, str) and desc.startswith('ERROR:'):
        return {
            'length': 0,
            'has_location': False,
            'optimal_length': False,
            'issues': [desc]
        }

    length = len(desc)
    issues = []

    # Check length
    optimal_length = OPTIMAL_LENGTH_MIN <= length <= OPTIMAL_LENGTH_MAX
    if length < OPTIMAL_LENGTH_MIN:
        issues.append(f'TOO SHORT ({length} chars, need {OPTIMAL_LENGTH_MIN}+)')
    elif length > OPTIMAL_LENGTH_MAX:
        issues.append(f'TOO LONG ({length} chars, max {OPTIMAL_LENGTH_MAX})')

    # Check location keywords
    has_location = any(keyword in desc.lower() for keyword in LOCATION_KEYWORDS)
    if not has_location:
        issues.append('NO LOCATION KEYWORD (Orlando/Florida missing)')

    # Check if location is in first 120 chars
    first_120 = desc[:120].lower()
    location_early = any(keyword in first_120 for keyword in LOCATION_KEYWORDS)
    if has_location and not location_early:
        issues.append('LOCATION TOO LATE (should be in first 120 chars)')

    return {
        'length': length,
        'has_location': has_location,
        'optimal_length': optimal_length,
        'issues': issues if issues else ['OK']
    }

def audit_all_pages():
    """Audit all HTML pages in the website."""

    # Get all HTML files (excluding backups and reports)
    html_files = []
    for root, dirs, files in os.walk(WEBSITE_DIR):
        # Skip backup and report directories
        if '.backup' in root or 'reports' in root:
            continue

        for file in files:
            if file.endswith('.html') and not file.startswith('_'):
                html_files.append(Path(root) / file)

    # Organize by category
    results = {
        'main_pages': [],
        'practice_areas': [],
        'blog_posts': [],
        'other': []
    }

    for html_file in sorted(html_files):
        rel_path = html_file.relative_to(WEBSITE_DIR)
        desc = extract_meta_description(html_file)
        analysis = analyze_description(desc)

        result = {
            'file': str(rel_path),
            'description': desc,
            'analysis': analysis
        }

        # Categorize
        if 'practice-areas' in str(rel_path):
            results['practice_areas'].append(result)
        elif 'blog' in str(rel_path):
            results['blog_posts'].append(result)
        elif rel_path.parent == Path('.'):
            results['main_pages'].append(result)
        else:
            results['other'].append(result)

    return results

def print_results(results):
    """Print audit results."""

    total_issues = 0
    total_pages = 0

    print("=" * 80)
    print("META DESCRIPTION AUDIT - ALL PAGES")
    print("=" * 80)

    for category, pages in results.items():
        if not pages:
            continue

        print(f"\n{category.upper().replace('_', ' ')} ({len(pages)} pages)")
        print("-" * 80)

        for page in pages:
            total_pages += 1
            issues = page['analysis']['issues']
            has_issues = issues != ['OK']

            if has_issues:
                total_issues += 1
                status = "[!] NEEDS WORK"
            else:
                status = "[OK]"

            print(f"\n{status} - {page['file']}")
            print(f"  Length: {page['analysis']['length']} chars")
            print(f"  Issues: {', '.join(issues)}")

            if page['description'] and not page['description'].startswith('ERROR:'):
                # Show first 80 chars
                preview = page['description'][:80]
                if len(page['description']) > 80:
                    preview += "..."
                print(f"  Current: {preview}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total pages audited: {total_pages}")
    print(f"Pages needing work: {total_issues}")
    print(f"Pages OK: {total_pages - total_issues}")
    print(f"Completion: {((total_pages - total_issues) / total_pages * 100):.1f}%")

if __name__ == '__main__':
    results = audit_all_pages()
    print_results(results)
