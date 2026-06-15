#!/usr/bin/env python3
"""
SEO Checker for Blog Posts

Analyzes a blog post HTML file for SEO best practices.
Can auto-fix common issues with --fix flag.

Usage:
    python seo_checker.py blog/35-discovery-delays.html
    python seo_checker.py blog/35-discovery-delays.html --fix
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser


class SEOParser(HTMLParser):
    """Parse HTML and extract SEO-relevant elements."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_description = ""
        self.canonical = ""
        self.og_tags = {}
        self.twitter_tags = {}
        self.h1_count = 0
        self.h1_text = ""
        self.h2_count = 0
        self.internal_links = []
        self.external_links = []
        self.schema_jsons = []
        self.in_title = False
        self.in_h1 = False
        self.in_script = False
        self.script_type = ""
        self.current_script = ""

        # Word count tracking
        self.word_count = 0
        self.body_text = []
        self.excluded_tag_depth = 0  # Track depth of excluded tags

        # Analytics tracking
        self.has_gtm = False
        self.has_ga4 = False
        self.has_clarity = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Track excluded tags (script, style, nav, footer, header)
        if tag in ("script", "style", "nav", "footer", "header"):
            self.excluded_tag_depth += 1

        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h1_count += 1
            self.in_h1 = True
        elif tag == "h2":
            self.h2_count += 1
        elif tag == "meta":
            name = attrs_dict.get("name", "")
            prop = attrs_dict.get("property", "")
            content = attrs_dict.get("content", "")

            if name == "description":
                self.meta_description = content
            elif prop.startswith("og:"):
                self.og_tags[prop] = content
            elif name.startswith("twitter:"):
                self.twitter_tags[name] = content

        elif tag == "link":
            rel = attrs_dict.get("rel", "")
            href = attrs_dict.get("href", "")
            if rel == "canonical":
                self.canonical = href

        elif tag == "a":
            href = attrs_dict.get("href", "")
            if href:
                if href.startswith("http") and "lotterlaw.com" not in href:
                    self.external_links.append(href)
                elif not href.startswith("http") or "lotterlaw.com" in href:
                    if not href.startswith("#") and not href.startswith("tel:") and not href.startswith("mailto:"):
                        self.internal_links.append(href)

        elif tag == "script":
            self.in_script = True
            self.script_type = attrs_dict.get("type", "")
            src = attrs_dict.get("src", "")
            if "GTM-52LMX48G" in src:
                self.has_gtm = True
            if "G-2MCJ8E0XS5" in src:
                self.has_ga4 = True
            if "reu4dibx4h" in src:
                self.has_clarity = True

    def handle_endtag(self, tag):
        # Track excluded tags
        if tag in ("script", "style", "nav", "footer", "header"):
            self.excluded_tag_depth = max(0, self.excluded_tag_depth - 1)

        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
        elif tag == "script":
            self.in_script = False
            if self.script_type == "application/ld+json":
                schema_json = self.current_script.strip()
                if schema_json:
                    self.schema_jsons.append(schema_json)
            self.current_script = ""
            self.script_type = ""

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_h1:
            self.h1_text += data
        elif self.in_script:
            self.current_script += data
            # Check for analytics
            if "GTM-52LMX48G" in data:
                self.has_gtm = True
            if "G-2MCJ8E0XS5" in data:
                self.has_ga4 = True
            if "reu4dibx4h" in data:
                self.has_clarity = True

        # Track body content for word count (exclude script/style/nav/footer/header content)
        if self.excluded_tag_depth == 0 and data.strip():
            self.body_text.append(data.strip())


def count_words(text_parts: list) -> int:
    """Count words in a list of text parts."""
    full_text = " ".join(text_parts)
    # Split on whitespace and filter empty strings
    words = [w for w in re.split(r'\s+', full_text) if w]
    return len(words)


def schema_types(obj) -> set:
    """Recursively collect @type values from JSON-LD."""
    found = set()
    if isinstance(obj, dict):
        value = obj.get("@type")
        if isinstance(value, str):
            found.add(value)
        elif isinstance(value, list):
            found.update(str(item) for item in value)
        for child in obj.values():
            found.update(schema_types(child))
    elif isinstance(obj, list):
        for child in obj:
            found.update(schema_types(child))
    return found


def check_link_quality(parser: SEOParser, results: dict):
    """
    Check link quality based on SEO best practices.

    Best practices:
    - Total links < 150 (PageRank dilution threshold)
    - Contextual links: 3-5 per 1,000 words
    - Link density: < 10 links per 1,000 words
    """
    # Calculate word count
    word_count = count_words(parser.body_text)
    parser.word_count = word_count  # Store for reference

    # Add word count info check (informational)
    results["checks"].append({
        "name": "Word Count",
        "status": "PASS",
        "value": f"{word_count} words"
    })
    results["passed"] += 1

    # Count all links (internal + external)
    total_links = len(parser.internal_links) + len(parser.external_links)
    unique_internal = len(set(parser.internal_links))

    # Check 1: Total link count
    if total_links < 150:
        results["checks"].append({
            "name": "Total Link Count",
            "status": "PASS",
            "value": f"{total_links} links (limit: 150)"
        })
        results["passed"] += 1
    else:
        results["checks"].append({
            "name": "Total Link Count",
            "status": "FAIL",
            "value": f"{total_links} links (exceeds 150 - PageRank dilution risk)"
        })
        results["failed"] += 1

    # Check 2: Contextual link minimum (3 per 1000 words)
    if word_count > 0:
        expected_min_links = max(3, int(word_count / 1000 * 3))  # 3 links per 1000 words

        if unique_internal >= expected_min_links:
            results["checks"].append({
                "name": "Contextual Links",
                "status": "PASS",
                "value": f"{unique_internal} links ({word_count} words, target: {expected_min_links})"
            })
            results["passed"] += 1
        elif unique_internal >= 2:
            # Warn if at least 2 but below target
            results["checks"].append({
                "name": "Contextual Links",
                "status": "WARN",
                "value": f"{unique_internal} links ({word_count} words, target: {expected_min_links})"
            })
            results["warnings"] += 1
        else:
            results["checks"].append({
                "name": "Contextual Links",
                "status": "FAIL",
                "value": f"{unique_internal} links ({word_count} words, target: {expected_min_links})"
            })
            results["failed"] += 1

    # Check 3: Link density (< 10 per 1000 words)
    if word_count > 0:
        link_density = (total_links / word_count) * 1000

        if link_density < 10:
            results["checks"].append({
                "name": "Link Density",
                "status": "PASS",
                "value": f"{link_density:.1f} links/1000 words (limit: 10)"
            })
            results["passed"] += 1
        else:
            results["checks"].append({
                "name": "Link Density",
                "status": "FAIL",
                "value": f"{link_density:.1f} links/1000 words (exceeds 10)"
            })
            results["failed"] += 1


def check_seo(filepath: Path) -> dict:
    """Run SEO checks on a blog post file."""

    content = filepath.read_text(encoding="utf-8")

    parser = SEOParser()
    parser.feed(content)

    results = {
        "file": str(filepath),
        "checks": [],
        "passed": 0,
        "failed": 0,
        "warnings": 0
    }

    # Title check
    title_len = len(parser.title.strip())
    if 50 <= title_len <= 60:
        results["checks"].append({"name": "Title Length", "status": "PASS", "value": f"{title_len} chars"})
        results["passed"] += 1
    elif 40 <= title_len <= 70:
        results["checks"].append({"name": "Title Length", "status": "WARN", "value": f"{title_len} chars (ideal: 50-60)"})
        results["warnings"] += 1
    else:
        results["checks"].append({"name": "Title Length", "status": "FAIL", "value": f"{title_len} chars (ideal: 50-60)"})
        results["failed"] += 1

    # Meta description check
    desc_len = len(parser.meta_description)
    if 150 <= desc_len <= 160:
        results["checks"].append({"name": "Meta Description", "status": "PASS", "value": f"{desc_len} chars"})
        results["passed"] += 1
    elif 120 <= desc_len <= 180:
        results["checks"].append({"name": "Meta Description", "status": "WARN", "value": f"{desc_len} chars (ideal: 150-160)"})
        results["warnings"] += 1
    else:
        results["checks"].append({"name": "Meta Description", "status": "FAIL", "value": f"{desc_len} chars (ideal: 150-160)"})
        results["failed"] += 1

    # Canonical URL
    if parser.canonical:
        results["checks"].append({"name": "Canonical URL", "status": "PASS", "value": parser.canonical})
        results["passed"] += 1
    else:
        results["checks"].append({"name": "Canonical URL", "status": "FAIL", "value": "Missing"})
        results["failed"] += 1

    # Open Graph tags
    required_og = ["og:title", "og:description", "og:image", "og:url", "og:type"]
    missing_og = [tag for tag in required_og if tag not in parser.og_tags]
    if not missing_og:
        results["checks"].append({"name": "Open Graph Tags", "status": "PASS", "value": "All present"})
        results["passed"] += 1
    else:
        results["checks"].append({"name": "Open Graph Tags", "status": "FAIL", "value": f"Missing: {', '.join(missing_og)}"})
        results["failed"] += 1

    # Twitter cards
    required_twitter = ["twitter:card", "twitter:title", "twitter:description"]
    missing_twitter = [tag for tag in required_twitter if tag not in parser.twitter_tags]
    if not missing_twitter:
        results["checks"].append({"name": "Twitter Cards", "status": "PASS", "value": "All present"})
        results["passed"] += 1
    else:
        results["checks"].append({"name": "Twitter Cards", "status": "FAIL", "value": f"Missing: {', '.join(missing_twitter)}"})
        results["failed"] += 1

    # H1 tag
    if parser.h1_count == 1:
        results["checks"].append({"name": "H1 Tag", "status": "PASS", "value": f"1 H1 found"})
        results["passed"] += 1
    elif parser.h1_count == 0:
        results["checks"].append({"name": "H1 Tag", "status": "FAIL", "value": "No H1 tag found"})
        results["failed"] += 1
    else:
        results["checks"].append({"name": "H1 Tag", "status": "WARN", "value": f"{parser.h1_count} H1 tags (should be 1)"})
        results["warnings"] += 1

    # Link Quality Checks (Enhancement 3: SEO Best Practices)
    check_link_quality(parser, results)

    # Schema markup
    if parser.schema_jsons:
        parsed_schemas = []
        invalid_count = 0
        for schema_json in parser.schema_jsons:
            try:
                parsed_schemas.append(json.loads(schema_json))
            except json.JSONDecodeError:
                invalid_count += 1

        if invalid_count:
            results["checks"].append({"name": "Article Schema", "status": "FAIL", "value": f"{invalid_count} invalid JSON-LD block(s)"})
            results["failed"] += 1
        else:
            types = set()
            for schema in parsed_schemas:
                types.update(schema_types(schema))
            article_types = {"Article", "BlogPosting", "NewsArticle"}
            if types & article_types:
                results["checks"].append({"name": "Article Schema", "status": "PASS", "value": f"Valid JSON-LD ({', '.join(sorted(types & article_types))})"})
                results["passed"] += 1
            else:
                results["checks"].append({"name": "Article Schema", "status": "WARN", "value": f"Types: {', '.join(sorted(types)) or 'unknown'}"})
                results["warnings"] += 1
    else:
        results["checks"].append({"name": "Article Schema", "status": "FAIL", "value": "No schema found"})
        results["failed"] += 1

    # Analytics checks
    if parser.has_gtm:
        results["checks"].append({"name": "Google Tag Manager", "status": "PASS", "value": "GTM-52LMX48G"})
        results["passed"] += 1
    else:
        results["checks"].append({"name": "Google Tag Manager", "status": "FAIL", "value": "Missing GTM-52LMX48G"})
        results["failed"] += 1

    if parser.has_ga4:
        results["checks"].append({"name": "Google Analytics 4", "status": "PASS", "value": "G-2MCJ8E0XS5"})
        results["passed"] += 1
    else:
        results["checks"].append({"name": "Google Analytics 4", "status": "WARN", "value": "No direct GA4 tag found; may be routed through GTM"})
        results["warnings"] += 1

    if parser.has_clarity:
        results["checks"].append({"name": "Microsoft Clarity", "status": "PASS", "value": "reu4dibx4h"})
        results["passed"] += 1
    else:
        results["checks"].append({"name": "Microsoft Clarity", "status": "WARN", "value": "No direct Clarity tag found; may be routed through GTM"})
        results["warnings"] += 1

    return results


def shorten_title(title: str, max_len: int = 60) -> str:
    """Intelligently shorten a title while keeping it meaningful."""
    # Remove " | Lotter Law" suffix if present
    title = re.sub(r'\s*\|\s*Lotter Law\s*$', '', title)

    if len(title) <= max_len:
        return title

    # Try removing common filler phrases
    fillers = [
        r'\s*in Florida\s*',
        r'\s*Criminal Cases?\s*',
        r'\s*What You Need to Know\s*',
        r'\s*:\s*',
    ]

    shortened = title
    for filler in fillers:
        if len(shortened) <= max_len:
            break
        shortened = re.sub(filler, ' ', shortened, count=1).strip()

    # If still too long, truncate at word boundary
    if len(shortened) > max_len:
        shortened = shortened[:max_len-3].rsplit(' ', 1)[0] + '...'

    return shortened.strip()


def shorten_description(desc: str, max_len: int = 160) -> str:
    """Intelligently shorten a meta description."""
    if len(desc) <= max_len:
        return desc

    # Truncate at sentence boundary if possible
    sentences = re.split(r'(?<=[.!?])\s+', desc)
    shortened = ""
    for sentence in sentences:
        if len(shortened) + len(sentence) + 1 <= max_len:
            shortened = (shortened + " " + sentence).strip()
        else:
            break

    # If we got at least one sentence, use it
    if shortened and len(shortened) >= 100:
        return shortened

    # Otherwise truncate at word boundary
    shortened = desc[:max_len-3].rsplit(' ', 1)[0] + '...'
    return shortened


def fix_seo_issues(filepath: Path, results: dict) -> list:
    """Auto-fix SEO issues and return list of repairs made."""
    content = filepath.read_text(encoding="utf-8")
    original = content
    repairs = []

    for check in results["checks"]:
        if check["status"] != "FAIL":
            continue

        if check["name"] == "Title Length":
            # Extract current title
            match = re.search(r'<title>([^<]+)</title>', content)
            if match:
                old_title = match.group(1)
                new_title = shorten_title(old_title)
                if new_title != old_title:
                    content = content.replace(f'<title>{old_title}</title>', f'<title>{new_title}</title>')
                    repairs.append({
                        "field": "title",
                        "old": old_title,
                        "new": new_title,
                        "old_len": len(old_title),
                        "new_len": len(new_title)
                    })

                    # Also update og:title if it matches
                    content = re.sub(
                        rf'(og:title["\s]+content=")[^"]+(")',
                        rf'\g<1>{new_title}\2',
                        content
                    )

        elif check["name"] == "Meta Description":
            # Extract current description
            match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
            if match:
                old_desc = match.group(1)
                new_desc = shorten_description(old_desc)
                if new_desc != old_desc:
                    content = content.replace(
                        f'<meta name="description" content="{old_desc}"',
                        f'<meta name="description" content="{new_desc}"'
                    )
                    repairs.append({
                        "field": "meta_description",
                        "old": old_desc,
                        "new": new_desc,
                        "old_len": len(old_desc),
                        "new_len": len(new_desc)
                    })

                    # Also update og:description if similar
                    content = re.sub(
                        rf'(og:description["\s]+content=")[^"]+(")',
                        rf'\g<1>{new_desc}\2',
                        content
                    )

    if content != original:
        filepath.write_text(content, encoding="utf-8")

    return repairs


def log_repairs(filepath: Path, repairs: list):
    """Log repairs to a repair log file."""
    log_dir = filepath.parent.parent / "output" / "seo_repairs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "repair_log.md"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"\n## {filepath.name} - {timestamp}\n\n"

    for repair in repairs:
        log_entry += f"### {repair['field']}\n"
        log_entry += f"- **Old** ({repair['old_len']} chars): {repair['old']}\n"
        log_entry += f"- **New** ({repair['new_len']} chars): {repair['new']}\n\n"

    # Append to log file
    if log_file.exists():
        existing = log_file.read_text(encoding="utf-8")
    else:
        existing = "# SEO Repair Log\n\nAutomated repairs made by seo_checker.py\n"

    log_file.write_text(existing + log_entry, encoding="utf-8")

    return log_file


def print_results(results: dict):
    """Print SEO check results."""

    print("=" * 60)
    print("SEO ANALYSIS REPORT")
    print("=" * 60)
    print(f"File: {results['file']}")
    print()

    for check in results["checks"]:
        status = check["status"]
        if status == "PASS":
            symbol = "[OK]"
        elif status == "WARN":
            symbol = "[!!]"
        else:
            symbol = "[XX]"
        print(f"  {symbol} {check['name']}: {check['value']}")

    print()
    print("-" * 60)
    print(f"PASSED: {results['passed']} | WARNINGS: {results['warnings']} | FAILED: {results['failed']}")
    print("-" * 60)

    if results["failed"] > 0:
        print("\n[!] Fix failed checks before publishing!")
        return False
    elif results["warnings"] > 0:
        print("\n[!] Consider addressing warnings for better SEO.")
        return True
    else:
        print("\n[OK] All SEO checks passed!")
        return True


def main():
    parser = argparse.ArgumentParser(description="Check blog post SEO")
    parser.add_argument("filepath", help="Path to blog post HTML file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues")
    args = parser.parse_args()

    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    results = check_seo(filepath)

    if args.json:
        print(json.dumps(results, indent=2))
        sys.exit(0)

    # Print initial results
    print_results(results)

    # Auto-fix if requested and there are failures
    if args.fix and results["failed"] > 0:
        print("\n" + "=" * 60)
        print("AUTO-FIXING ISSUES...")
        print("=" * 60)

        repairs = fix_seo_issues(filepath, results)

        if repairs:
            print(f"\nRepairs made: {len(repairs)}")
            for repair in repairs:
                print(f"  - {repair['field']}: {repair['old_len']} -> {repair['new_len']} chars")

            # Log repairs
            log_file = log_repairs(filepath, repairs)
            print(f"\nRepairs logged to: {log_file}")

            # Re-run check to confirm fixes
            print("\n" + "=" * 60)
            print("RE-CHECKING AFTER FIXES...")
            print("=" * 60)
            new_results = check_seo(filepath)
            success = print_results(new_results)
            sys.exit(0 if success else 1)
        else:
            print("\nNo auto-fixable issues found.")
            sys.exit(1)
    else:
        sys.exit(0 if results["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
