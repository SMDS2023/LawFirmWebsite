#!/usr/bin/env python3
"""
Sitewide blog SEO and link audit for lotterlaw.com.

This is intentionally dependency-free so it can run in GitHub Actions and on a
fresh local checkout. It checks the invariants that tend to drift on static
sites: local links, blog index coverage, sitemap coverage, canonical URLs,
social metadata, robots directives, and structured data.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://lotterlaw.com"
SITE_HOSTS = {"lotterlaw.com", "www.lotterlaw.com"}
ARTICLE_SCHEMA_TYPES = {"Article", "BlogPosting", "NewsArticle"}
HUB_SCHEMA_TYPES = {"WebPage", "CollectionPage"}
SKIP_SCHEMES = {"mailto", "tel", "sms", "javascript", "data"}
SKIP_PATH_PREFIXES = (
    ".backup_before_clarity/",
    "analytics/reports/",
    "analytics/templates/",
    "reports/",
)


@dataclass
class HtmlDoc:
    path: Path
    rel: str
    title: str = ""
    metas: list[dict[str, str]] = field(default_factory=list)
    links: list[dict[str, str]] = field(default_factory=list)
    anchors: list[dict[str, str]] = field(default_factory=list)
    refs: list[tuple[str, str, str]] = field(default_factory=list)
    images: list[dict[str, str]] = field(default_factory=list)
    h1_count: int = 0
    jsonld_raw: list[str] = field(default_factory=list)
    refresh_url: str = ""

    def meta(self, key: str, value: str) -> str:
        for meta in self.metas:
            if meta.get(key, "").lower() == value.lower():
                return meta.get("content", "")
        return ""

    def canonical(self) -> str:
        for link in self.links:
            rel = link.get("rel", "")
            if "canonical" in rel.lower().split():
                return link.get("href", "")
        return ""

    def has_noindex(self) -> bool:
        robots = self.meta("name", "robots").lower()
        return "noindex" in robots

    def schemas(self) -> tuple[list[Any], list[str]]:
        parsed: list[Any] = []
        errors: list[str] = []
        for raw in self.jsonld_raw:
            try:
                parsed.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                errors.append(f"{self.rel}: invalid JSON-LD ({exc.msg})")
        return parsed, errors


class DocParser(HTMLParser):
    def __init__(self, path: Path, rel: str) -> None:
        super().__init__(convert_charrefs=True)
        self.doc = HtmlDoc(path=path, rel=rel)
        self._in_title = False
        self._in_script = False
        self._script_type = ""
        self._script_buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()

        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.doc.metas.append(attrs_dict)
            if attrs_dict.get("http-equiv", "").lower() == "refresh":
                content = attrs_dict.get("content", "")
                match = re.search(r"url\s*=\s*([^;]+)", content, flags=re.I)
                if match:
                    self.doc.refresh_url = match.group(1).strip()
        elif tag == "link":
            self.doc.links.append(attrs_dict)
            href = attrs_dict.get("href")
            if href:
                self.doc.refs.append((tag, "href", href))
        elif tag == "a":
            self.doc.anchors.append(attrs_dict)
            href = attrs_dict.get("href")
            if href:
                self.doc.refs.append((tag, "href", href))
        elif tag == "img":
            self.doc.images.append(attrs_dict)
            src = attrs_dict.get("src")
            if src:
                self.doc.refs.append((tag, "src", src))
            srcset = attrs_dict.get("srcset")
            if srcset:
                for url in parse_srcset(srcset):
                    self.doc.refs.append((tag, "srcset", url))
        elif tag in {"script", "iframe", "source", "video", "audio"}:
            src = attrs_dict.get("src")
            if src:
                self.doc.refs.append((tag, "src", src))
            if tag == "script":
                self._in_script = True
                self._script_type = attrs_dict.get("type", "")
                self._script_buf = []
        elif tag == "h1":
            self.doc.h1_count += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            if self._script_type == "application/ld+json":
                raw = "".join(self._script_buf).strip()
                if raw:
                    self.doc.jsonld_raw.append(raw)
            self._in_script = False
            self._script_type = ""
            self._script_buf = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.doc.title += data
        if self._in_script:
            self._script_buf.append(data)


def parse_srcset(value: str) -> list[str]:
    urls = []
    for item in value.split(","):
        item = item.strip()
        if item:
            urls.append(item.split()[0])
    return urls


def tracked_files(patterns: list[str]) -> list[str]:
    cmd = ["git", "ls-files", "--", *patterns]
    try:
        result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)
        return [p.replace("\\", "/") for p in result.stdout.splitlines() if p]
    except Exception:
        files: list[str] = []
        for pattern in patterns:
            files.extend(path.relative_to(ROOT).as_posix() for path in ROOT.glob(pattern))
        return sorted(set(files))


def read_doc(rel: str) -> HtmlDoc:
    path = ROOT / rel
    parser = DocParser(path, rel)
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return parser.doc


def normalize_ref(base_rel: str, value: str) -> str | None:
    value = value.strip()
    if not value or value.startswith("#"):
        return None

    parsed = urlparse(value)
    if parsed.scheme and parsed.scheme.lower() in SKIP_SCHEMES:
        return None
    if parsed.scheme in {"http", "https"} and parsed.netloc.lower() not in SITE_HOSTS:
        return None

    raw_path = parsed.path or ""
    if not raw_path and parsed.fragment:
        return None

    raw_path = unquote(raw_path).replace("\\", "/")
    if raw_path.startswith("/"):
        rel = raw_path.lstrip("/")
    elif parsed.scheme in {"http", "https"}:
        rel = raw_path.lstrip("/")
    else:
        base_dir = posixpath.dirname(base_rel)
        rel = posixpath.normpath(posixpath.join(base_dir, raw_path))

    rel = rel.strip("/")
    if rel in {"", "."}:
        return "index.html"
    if rel.startswith("../"):
        return rel
    return rel


def local_target_exists(rel: str) -> bool:
    rel = rel.replace("\\", "/")
    candidates = []
    if rel.endswith("/"):
        candidates.append(ROOT / rel / "index.html")
    else:
        target = ROOT / rel
        candidates.append(target)
        if not Path(rel).suffix:
            candidates.append(ROOT / rel / "index.html")
            candidates.append(ROOT / f"{rel}.html")
    return any(candidate.exists() for candidate in candidates)


def schema_types(obj: Any) -> set[str]:
    found: set[str] = set()
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


def find_schema_objects(obj: Any, wanted: set[str]) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    if isinstance(obj, dict):
        if schema_types(obj) & wanted:
            matches.append(obj)
        for child in obj.values():
            matches.extend(find_schema_objects(child, wanted))
    elif isinstance(obj, list):
        for child in obj:
            matches.extend(find_schema_objects(child, wanted))
    return matches


def locs_from_sitemap() -> tuple[set[str], list[str]]:
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        return set(), ["sitemap.xml is missing"]
    try:
        tree = ET.parse(sitemap)
    except ET.ParseError as exc:
        return set(), [f"sitemap.xml is invalid XML: {exc}"]

    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs: set[str] = set()
    errors: list[str] = []
    for loc in tree.findall(".//sm:loc", ns):
        if not loc.text:
            continue
        if loc.text in locs:
            errors.append(f"sitemap.xml has duplicate loc: {loc.text}")
        locs.add(loc.text)
        parsed = urlparse(loc.text)
        if parsed.netloc.lower() not in SITE_HOSTS:
            errors.append(f"sitemap.xml loc is not on lotterlaw.com: {loc.text}")
    return locs, errors


def blog_slug_from_rel(rel: str) -> str | None:
    parts = rel.replace("\\", "/").split("/")
    if len(parts) == 3 and parts[0] == "blog" and parts[2] == "index.html" and parts[1] != "category":
        return parts[1]
    return None


def linked_blog_slugs(doc: HtmlDoc) -> set[str]:
    slugs: set[str] = set()
    for tag, attr, value in doc.refs:
        if tag != "a" or attr != "href":
            continue
        rel = normalize_ref(doc.rel, value)
        if not rel:
            continue
        slug = blog_slug_from_rel(rel if rel.endswith("index.html") else f"{rel.rstrip('/')}/index.html")
        if slug:
            slugs.add(slug)
    return slugs


def blog_slugs_from_sitemap(locs: set[str]) -> set[str]:
    slugs: set[str] = set()
    for loc in locs:
        parsed = urlparse(loc)
        match = re.fullmatch(r"/blog/([^/]+)/?", parsed.path)
        if match and match.group(1) != "category":
            slugs.add(match.group(1))
    return slugs


def check_local_refs(html_docs: list[HtmlDoc]) -> list[str]:
    errors: list[str] = []
    for doc in html_docs:
        if any(doc.rel.startswith(prefix) for prefix in SKIP_PATH_PREFIXES):
            continue
        for tag, attr, value in doc.refs:
            rel = normalize_ref(doc.rel, value)
            if not rel:
                continue
            if rel.startswith("../"):
                errors.append(f"{doc.rel}: {tag}[{attr}] escapes site root: {value}")
            elif not local_target_exists(rel):
                errors.append(f"{doc.rel}: missing local target for {tag}[{attr}]={value}")
    return errors


def validate_post(
    slug: str,
    doc: HtmlDoc,
    blog_index_slugs: set[str],
    sitemap_slugs: set[str],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    canonical = f"{SITE_URL}/blog/{slug}/"
    meta_description = doc.meta("name", "description")
    og_url = doc.meta("property", "og:url")
    og_image = doc.meta("property", "og:image")

    if slug not in blog_index_slugs:
        errors.append(f"{doc.rel}: published post is missing from blog.html")
    if slug not in sitemap_slugs:
        errors.append(f"{doc.rel}: published post is missing from sitemap.xml")
    if doc.canonical() != canonical:
        errors.append(f"{doc.rel}: canonical should be {canonical}, found {doc.canonical() or 'missing'}")
    if og_url != canonical:
        errors.append(f"{doc.rel}: og:url should match canonical {canonical}")
    if not doc.title.strip():
        errors.append(f"{doc.rel}: missing <title>")
    if doc.h1_count != 1:
        errors.append(f"{doc.rel}: expected exactly one H1, found {doc.h1_count}")
    if not meta_description:
        errors.append(f"{doc.rel}: missing meta description")
    elif len(meta_description) < 80 or len(meta_description) > 180:
        warnings.append(f"{doc.rel}: meta description length is {len(meta_description)} chars")

    required_og = ["og:title", "og:description", "og:type", "og:url", "og:image"]
    for prop in required_og:
        if not doc.meta("property", prop):
            errors.append(f"{doc.rel}: missing {prop}")
    required_twitter = ["twitter:card", "twitter:title", "twitter:description", "twitter:image"]
    for name in required_twitter:
        if not doc.meta("name", name):
            errors.append(f"{doc.rel}: missing {name}")
    if og_image:
        rel = normalize_ref(doc.rel, og_image)
        if rel and not local_target_exists(rel):
            errors.append(f"{doc.rel}: og:image does not resolve locally: {og_image}")

    schemas, schema_errors = doc.schemas()
    errors.extend(schema_errors)
    types = set().union(*(schema_types(schema) for schema in schemas)) if schemas else set()
    if slug == "start-here":
        if not (types & HUB_SCHEMA_TYPES):
            errors.append(f"{doc.rel}: start-here hub should include WebPage or CollectionPage schema")
    elif not (types & ARTICLE_SCHEMA_TYPES):
        errors.append(f"{doc.rel}: missing Article, BlogPosting, or NewsArticle schema")
    if "BreadcrumbList" not in types:
        errors.append(f"{doc.rel}: missing BreadcrumbList schema")

    article_objects: list[dict[str, Any]] = []
    for schema in schemas:
        article_objects.extend(find_schema_objects(schema, ARTICLE_SCHEMA_TYPES))
    if article_objects:
        article = article_objects[0]
        for field_name in ("datePublished", "dateModified"):
            if not article.get(field_name):
                errors.append(f"{doc.rel}: Article schema missing {field_name}")

    for image in doc.images:
        if not image.get("alt", "").strip():
            errors.append(f"{doc.rel}: image missing alt text: {image.get('src', 'unknown src')}")
        if image.get("src") and not image.get("width") and not image.get("height"):
            warnings.append(f"{doc.rel}: image has no explicit dimensions: {image.get('src')}")

    return errors, warnings


def audit() -> dict[str, Any]:
    html_rels = [
        rel for rel in tracked_files(["*.html", "**/*.html"])
        if rel.endswith(".html") and not any(rel.startswith(prefix) for prefix in SKIP_PATH_PREFIXES)
    ]
    html_docs = [read_doc(rel) for rel in sorted(set(html_rels))]
    docs_by_rel = {doc.rel: doc for doc in html_docs}

    errors: list[str] = []
    warnings: list[str] = []
    errors.extend(check_local_refs(html_docs))

    sitemap_locs, sitemap_errors = locs_from_sitemap()
    errors.extend(sitemap_errors)
    sitemap_slugs = blog_slugs_from_sitemap(sitemap_locs)

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8", errors="ignore") if (ROOT / "robots.txt").exists() else ""
    if "Sitemap: https://lotterlaw.com/sitemap.xml" not in robots:
        errors.append("robots.txt is missing the canonical sitemap directive")
    if re.search(r"(?im)^\s*Disallow:\s*/blog/?\s*$", robots):
        errors.append("robots.txt disallows /blog")

    blog_index = docs_by_rel.get("blog.html")
    if not blog_index:
        errors.append("blog.html is missing")
        blog_index_slugs: set[str] = set()
    else:
        blog_index_slugs = linked_blog_slugs(blog_index)

    publishable: dict[str, HtmlDoc] = {}
    redirects: dict[str, HtmlDoc] = {}
    for doc in html_docs:
        slug = blog_slug_from_rel(doc.rel)
        if not slug:
            continue
        if doc.has_noindex() or doc.refresh_url:
            redirects[slug] = doc
        else:
            publishable[slug] = doc

    for slug, doc in sorted(publishable.items()):
        post_errors, post_warnings = validate_post(slug, doc, blog_index_slugs, sitemap_slugs)
        errors.extend(post_errors)
        warnings.extend(post_warnings)

    for slug, doc in sorted(redirects.items()):
        if slug in sitemap_slugs:
            errors.append(f"{doc.rel}: noindex/redirect page appears in sitemap.xml")
        if slug in blog_index_slugs:
            errors.append(f"{doc.rel}: noindex/redirect page appears in blog.html")

    for slug in sorted(blog_index_slugs):
        if slug not in publishable:
            errors.append(f"blog.html links to missing or noindex blog post: {slug}")
    for slug in sorted(sitemap_slugs):
        if slug not in publishable:
            errors.append(f"sitemap.xml includes missing or noindex blog post: {slug}")

    category_rels = [rel for rel in docs_by_rel if rel.startswith("blog/category/") and rel.endswith(".html")]
    category_locs = {f"{SITE_URL}/{rel}" for rel in category_rels}
    missing_categories = sorted(category_locs - sitemap_locs)
    for loc in missing_categories:
        errors.append(f"blog category page is missing from sitemap.xml: {loc}")

    return {
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "html_files": len(html_docs),
            "published_blog_posts": len(publishable),
            "noindex_redirect_blog_pages": len(redirects),
            "blog_index_slugs": len(blog_index_slugs),
            "sitemap_blog_slugs": len(sitemap_slugs),
            "category_pages": len(category_rels),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Lotter Law blog SEO and local links")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    result = audit()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("Lotter Law Blog SEO Audit")
        print("=" * 72)
        for key, value in result["counts"].items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print(f"Errors: {len(result['errors'])}")
        print(f"Warnings: {len(result['warnings'])}")
        if result["errors"]:
            print("\nErrors")
            print("-" * 72)
            for error in result["errors"]:
                print(f"[ERROR] {error}")
        if result["warnings"]:
            print("\nWarnings")
            print("-" * 72)
            for warning in result["warnings"][:100]:
                print(f"[WARN] {warning}")
            if len(result["warnings"]) > 100:
                print(f"[WARN] ... {len(result['warnings']) - 100} more warnings omitted")
        if not result["errors"]:
            print("\n[OK] Blog SEO, indexing, and local link checks passed.")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
