#!/usr/bin/env python3
"""
Cross-Linker for Blog Posts

Finds related blog posts and adds cross-links between them.

Usage:
    python cross_linker.py blog/35-discovery-delays.html
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from html.parser import HTMLParser


# Topic clusters - related keywords that should link together
TOPIC_CLUSTERS = {
    "dui": ["dui", "dwi", "drunk driving", "impaired", "breathalyzer", "breath test", "bac", "blood alcohol", "f.s. 316.193", "316.193"],
    "traffic": ["traffic", "speeding", "speed", "radar", "citation", "ticket", "moving violation", "excessive speed"],
    "dwls": ["dwls", "dwlsr", "driving while license suspended", "suspended license", "f.s. 322.34", "322.34"],
    "drugs": ["drug", "drugs", "marijuana", "cannabis", "possession", "controlled substance", "narcotics"],
    "theft": ["theft", "shoplifting", "retail theft", "petit theft", "grand theft", "stealing", "f.s. 812.014"],
    "assault": ["assault", "battery", "domestic violence", "violence", "fight", "attack"],
    "weapons": ["weapon", "firearm", "gun", "concealed carry", "f.s. 790", "securely encased"],
    "burglary": ["burglary", "breaking and entering", "trespass", "f.s. 810"],
    "discovery": ["discovery", "evidence", "disclosure", "ongoing investigation", "motion to compel"],
    "criminal_procedure": ["arraignment", "plea", "trial", "sentencing", "probation", "diversion", "pretrial"],
}

# Practice areas for matching
PRACTICE_AREAS = {
    "dui": ["dui", "dwi", "drunk", "impaired", "breathalyzer"],
    "traffic": ["traffic", "speeding", "ticket", "citation", "radar"],
    "criminal": ["felony", "misdemeanor", "arrest", "charge", "criminal"],
    "defense": ["defense", "dismissed", "reduced", "not guilty", "acquittal"],
}


class BlogPostParser(HTMLParser):
    """Parse blog post to extract title, content, and keywords."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.h1_text = ""
        self.text_content = []
        self.in_title = False
        self.in_h1 = False
        self.in_body = False
        self.in_script = False
        self.in_style = False
        self.meta_keywords = ""
        self.meta_description = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
        elif tag == "body":
            self.in_body = True
        elif tag == "script":
            self.in_script = True
        elif tag == "style":
            self.in_style = True
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            content = attrs_dict.get("content", "")
            if name == "keywords":
                self.meta_keywords = content
            elif name == "description":
                self.meta_description = content

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
        elif tag == "body":
            self.in_body = False
        elif tag == "script":
            self.in_script = False
        elif tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_h1:
            self.h1_text += data
        elif self.in_body and not self.in_script and not self.in_style:
            self.text_content.append(data)

    def get_text(self):
        return " ".join(self.text_content)


def extract_keywords(text: str) -> set:
    """Extract relevant keywords from text."""
    text_lower = text.lower()
    found_keywords = set()

    # Check for topic cluster keywords
    for cluster, keywords in TOPIC_CLUSTERS.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_keywords.add(cluster)
                break

    # Check for Florida statute references
    statutes = re.findall(r'f\.s\.\s*(\d{3}\.\d+)', text_lower)
    for statute in statutes:
        found_keywords.add(f"statute_{statute}")

    return found_keywords


def get_post_info(filepath: Path) -> dict:
    """Get info about a blog post."""
    content = filepath.read_text(encoding="utf-8")
    parser = BlogPostParser()
    parser.feed(content)

    all_text = f"{parser.title} {parser.h1_text} {parser.meta_description} {parser.meta_keywords} {parser.get_text()}"
    keywords = extract_keywords(all_text)

    return {
        "path": filepath,
        "filename": filepath.name,
        "title": parser.title.strip(),
        "h1": parser.h1_text.strip(),
        "keywords": keywords,
    }


def find_related_posts(target_post: dict, all_posts: list, max_results: int = 3) -> list:
    """Find posts related to the target post."""
    target_keywords = target_post["keywords"]
    if not target_keywords:
        return []

    scored_posts = []
    for post in all_posts:
        if post["filename"] == target_post["filename"]:
            continue

        # Calculate similarity score
        common = target_keywords.intersection(post["keywords"])
        if common:
            score = len(common)
            scored_posts.append((score, post, common))

    # Sort by score descending
    scored_posts.sort(key=lambda x: x[0], reverse=True)

    return [(post, common) for score, post, common in scored_posts[:max_results]]


def add_related_section(filepath: Path, related_posts: list) -> bool:
    """Add Related Articles section to a blog post."""
    content = filepath.read_text(encoding="utf-8")

    # Check if Related Articles section already exists
    if "Related Articles" in content or "related-posts" in content:
        print(f"  Related section already exists in {filepath.name}")
        return False

    # Build the related articles HTML
    related_html = """
                <!-- Related Articles -->
                <section class="mb-12">
                    <h2 class="text-2xl font-bold text-blue-800 mb-4">Related Articles</h2>
                    <div class="space-y-3">
"""
    for post, common in related_posts:
        title = post["h1"] or post["title"].replace(" | Lotter Law", "")
        related_html += f'                        <a href="{post["filename"]}" class="block p-4 bg-gray-50 hover:bg-blue-50 rounded-lg transition">\n'
        related_html += f'                            <span class="text-blue-700 font-semibold">{title}</span>\n'
        related_html += f'                        </a>\n'

    related_html += """                    </div>
                </section>
"""

    # Find insertion point - before the final CTA section
    cta_pattern = r'(<!-- Final CTA -->|<section class="mb-12">\s*<div class="bg-blue-700)'
    match = re.search(cta_pattern, content)

    if match:
        insert_pos = match.start()
        new_content = content[:insert_pos] + related_html + "\n" + content[insert_pos:]
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  Added related section to {filepath.name}")
        return True
    else:
        # Try inserting before </main>
        main_end = content.rfind("</main>")
        if main_end > 0:
            # Find the last </section> before </main>
            last_section = content.rfind("</section>", 0, main_end)
            if last_section > 0:
                insert_pos = last_section + len("</section>")
                new_content = content[:insert_pos] + "\n" + related_html + content[insert_pos:]
                filepath.write_text(new_content, encoding="utf-8")
                print(f"  Added related section to {filepath.name}")
                return True

    print(f"  [!] Could not find insertion point in {filepath.name}")
    return False


def add_backlink(filepath: Path, new_post: dict) -> bool:
    """Add a link to the new post in an existing post's Related section."""
    content = filepath.read_text(encoding="utf-8")

    # Check if Related Articles section exists
    if "Related Articles" not in content and "related-posts" not in content:
        return False  # No related section to update

    # Check if already linked
    if new_post["filename"] in content:
        return False  # Already linked

    # Find the related articles section and add the new link
    title = new_post["h1"] or new_post["title"].replace(" | Lotter Law", "")
    new_link = f'                        <a href="{new_post["filename"]}" class="block p-4 bg-gray-50 hover:bg-blue-50 rounded-lg transition">\n'
    new_link += f'                            <span class="text-blue-700 font-semibold">{title}</span>\n'
    new_link += f'                        </a>\n'

    # Find the closing </div> of the related articles section
    pattern = r'(Related Articles.*?<div class="space-y-3">)(.*?)(</div>\s*</section>)'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        new_content = content[:match.end(2)] + new_link + content[match.end(2):]
        filepath.write_text(new_content, encoding="utf-8")
        print(f"  Added backlink in {filepath.name}")
        return True

    return False


def main():
    parser = argparse.ArgumentParser(description="Cross-link blog posts")
    parser.add_argument("filepath", help="Path to the new blog post")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    args = parser.parse_args()

    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    blog_dir = filepath.parent

    print("=" * 60)
    print("CROSS-LINKER")
    print("=" * 60)
    print(f"Target: {filepath.name}")
    print()

    # Get all blog posts
    all_posts = []
    for post_file in blog_dir.glob("*.html"):
        if post_file.name not in ["index.html"]:
            try:
                post_info = get_post_info(post_file)
                all_posts.append(post_info)
            except Exception as e:
                print(f"  Warning: Could not parse {post_file.name}: {e}")

    print(f"Found {len(all_posts)} blog posts")

    # Get target post info
    target_post = get_post_info(filepath)
    print(f"Keywords: {', '.join(target_post['keywords'])}")
    print()

    # Find related posts
    related = find_related_posts(target_post, all_posts)

    if not related:
        print("[!] No related posts found")
        sys.exit(0)

    print("Related Posts:")
    for post, common in related:
        print(f"  - {post['filename']}")
        print(f"    Common: {', '.join(common)}")
    print()

    if args.dry_run:
        print("[DRY RUN] No changes made")
        sys.exit(0)

    # Add related section to target post
    print("Adding cross-links...")
    added = add_related_section(filepath, related)

    # Add backlinks from related posts
    backlinks_added = 0
    for post, common in related:
        if add_backlink(post["path"], target_post):
            backlinks_added += 1

    print()
    print("-" * 60)
    print(f"Related section added: {'Yes' if added else 'No (already exists)'}")
    print(f"Backlinks added: {backlinks_added}")
    print("-" * 60)


if __name__ == "__main__":
    main()
