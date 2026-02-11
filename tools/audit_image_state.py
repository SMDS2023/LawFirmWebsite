#!/usr/bin/env python3
"""
Blog Image Location Audit
Generates migration manifest showing which posts have images in correct vs legacy locations
"""

import json
import re
from pathlib import Path
from collections import defaultdict

def clean_slug(slug):
    """Remove number prefix from slug"""
    return re.sub(r'^\d+-', '', slug)

def audit_blog_images():
    blog_dir = Path("blog")
    assets_blog = Path("assets/blog")
    
    report = {
        "audit_date": "2026-02-10",
        "summary": {},
        "posts": {},
        "legacy_images": [],
        "migration_needed": []
    }
    
    stats = defaultdict(int)
    
    # Find all blog posts
    for post_dir in sorted(blog_dir.iterdir()):
        if not post_dir.is_dir() or post_dir.name == "images":
            continue
            
        slug = post_dir.name
        clean = clean_slug(slug)
        html_file = post_dir / "index.html"
        images_dir = post_dir / "images"
        
        post_info = {
            "slug": slug,
            "clean_slug": clean,
            "has_html": html_file.exists(),
            "has_images_dir": images_dir.exists(),
            "image_files": [],
            "og_image_path": None,
            "image_location": None
        }
        
        # Check for images in correct location
        if images_dir.exists():
            post_info["image_files"] = [f.name for f in images_dir.glob("*.jpg")]
            stats["has_images_dir"] += 1
        
        # Parse HTML for og:image path
        if html_file.exists():
            content = html_file.read_text(encoding='utf-8', errors='ignore')
            match = re.search(r'<meta property="og:image" content="([^"]+)"', content)
            if match:
                post_info["og_image_path"] = match.group(1)
                
                # Determine image location pattern
                og_path = match.group(1)
                if f"/blog/{clean}/images/" in og_path:
                    post_info["image_location"] = "CORRECT"
                    stats["correct_location"] += 1
                elif "/assets/blog/" in og_path:
                    post_info["image_location"] = "LEGACY_ASSETS"
                    stats["legacy_assets"] += 1
                elif "logo" in og_path.lower() or "brand" in og_path.lower():
                    post_info["image_location"] = "LOGO_FALLBACK"
                    stats["logo_fallback"] += 1
                elif "/blog/images/" in og_path:
                    post_info["image_location"] = "BLOG_ROOT"
                    stats["blog_root"] += 1
                else:
                    post_info["image_location"] = "UNKNOWN"
                    stats["unknown"] += 1
        
        # Check if images exist where HTML points
        if post_info["og_image_path"]:
            # Convert URL to file path
            url_path = post_info["og_image_path"].replace("https://lotterlaw.com/", "")
            file_path = Path(url_path)
            post_info["image_exists"] = file_path.exists()
            
            if not post_info["image_exists"]:
                stats["broken_links"] += 1
        
        report["posts"][slug] = post_info
        
        # Track migration needs
        if post_info["image_location"] != "CORRECT":
            report["migration_needed"].append({
                "slug": slug,
                "current_location": post_info["image_location"],
                "has_images": bool(post_info["image_files"])
            })
    
    # Check for legacy images in assets/blog
    if assets_blog.exists():
        for img_file in assets_blog.glob("*.jpg"):
            report["legacy_images"].append(img_file.name)
    
    # Summary stats
    report["summary"] = {
        "total_posts": len(report["posts"]),
        "correct_location": stats["correct_location"],
        "legacy_assets": stats["legacy_assets"],
        "logo_fallback": stats["logo_fallback"],
        "blog_root": stats["blog_root"],
        "unknown": stats["unknown"],
        "broken_links": stats["broken_links"],
        "migration_needed": len(report["migration_needed"]),
        "legacy_image_files": len(report["legacy_images"])
    }
    
    return report

if __name__ == "__main__":
    report = audit_blog_images()
    
    # Save to JSON
    output_dir = Path("../Blog/.index")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "blog_image_state.json"
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"[OK] Audit complete: {output_file}")
    print(f"\nSummary:")
    print(f"  Total posts: {report['summary']['total_posts']}")
    print(f"  [OK] Correct location: {report['summary']['correct_location']}")
    print(f"  [WARN] Legacy assets: {report['summary']['legacy_assets']}")
    print(f"  [WARN] Logo fallback: {report['summary']['logo_fallback']}")
    print(f"  [WARN] Blog root: {report['summary']['blog_root']}")
    print(f"  [WARN] Unknown: {report['summary']['unknown']}")
    print(f"  [ERROR] Broken links: {report['summary']['broken_links']}")
    print(f"  [ACTION] Migration needed: {report['summary']['migration_needed']}")
    print(f"  [ACTION] Legacy files: {report['summary']['legacy_image_files']}")
