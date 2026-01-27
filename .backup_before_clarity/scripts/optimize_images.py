#!/usr/bin/env python3
"""
Image Optimization Script for LotterLaw Website
================================================
Compresses oversized images and generates WebP versions.

Usage:
    python optimize_images.py --audit          # Audit only, no changes
    python optimize_images.py --compress       # Compress oversized images
    python optimize_images.py --webp           # Generate missing WebP versions
    python optimize_images.py --all            # Do everything
    python optimize_images.py --dimensions     # Output image dimensions for HTML

Requirements:
    pip install Pillow
"""

import os
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

# Configuration
ASSETS_DIR = Path(__file__).parent.parent / "assets"
MAX_SIZE_KB = 200  # Target max size in KB
COMPRESSION_QUALITY = 85  # JPEG/WebP quality (0-100)
WEBP_QUALITY = 80  # WebP tends to be more efficient
PNG_OPTIMIZE = True
PNG_MAX_COLORS = 256  # For palette-based optimization of large PNGs


@dataclass
class ImageInfo:
    path: Path
    size_kb: float
    width: int
    height: int
    format: str
    has_webp: bool = False
    needs_compression: bool = False


def get_image_info(path: Path) -> ImageInfo:
    """Get information about an image file."""
    size_kb = path.stat().st_size / 1024

    with Image.open(path) as img:
        width, height = img.size
        fmt = img.format

    # Check if WebP version exists
    webp_path = path.with_suffix('.webp')
    has_webp = webp_path.exists() and webp_path != path

    needs_compression = size_kb > MAX_SIZE_KB

    return ImageInfo(
        path=path,
        size_kb=size_kb,
        width=width,
        height=height,
        format=fmt,
        has_webp=has_webp,
        needs_compression=needs_compression
    )


def audit_images() -> List[ImageInfo]:
    """Audit all images in the assets directory."""
    images = []

    for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
        for path in ASSETS_DIR.glob(ext):
            try:
                info = get_image_info(path)
                images.append(info)
            except Exception as e:
                print(f"  WARNING: Could not process {path.name}: {e}")

    return images


def print_audit_report(images: List[ImageInfo]):
    """Print a detailed audit report."""
    print("\n" + "=" * 70)
    print("IMAGE AUDIT REPORT")
    print("=" * 70)

    # Sort by size descending
    images_sorted = sorted(images, key=lambda x: x.size_kb, reverse=True)

    # Oversized images
    oversized = [img for img in images_sorted if img.needs_compression]
    if oversized:
        print(f"\n{'OVERSIZED IMAGES (> ' + str(MAX_SIZE_KB) + ' KB)':^70}")
        print("-" * 70)
        print(f"{'Filename':<40} {'Size':>10} {'Dims':>15}")
        print("-" * 70)
        for img in oversized:
            dims = f"{img.width}x{img.height}"
            size = f"{img.size_kb:.0f} KB" if img.size_kb < 1024 else f"{img.size_kb/1024:.1f} MB"
            print(f"{img.path.name:<40} {size:>10} {dims:>15}")
        print(f"\nTotal oversized: {len(oversized)}")

    # Images missing WebP
    jpg_png = [img for img in images_sorted if img.format in ['JPEG', 'PNG'] and not img.has_webp]
    if jpg_png:
        print(f"\n{'JPG/PNG IMAGES MISSING WEBP':^70}")
        print("-" * 70)
        print(f"{'Filename':<40} {'Size':>10} {'Format':>10}")
        print("-" * 70)
        for img in jpg_png:
            size = f"{img.size_kb:.0f} KB" if img.size_kb < 1024 else f"{img.size_kb/1024:.1f} MB"
            print(f"{img.path.name:<40} {size:>10} {img.format:>10}")
        print(f"\nTotal missing WebP: {len(jpg_png)}")

    # Summary
    total_size = sum(img.size_kb for img in images) / 1024  # MB
    webp_count = len([img for img in images if img.format == 'WEBP'])

    print(f"\n{'SUMMARY':^70}")
    print("-" * 70)
    print(f"Total images: {len(images)}")
    print(f"Total size: {total_size:.2f} MB")
    print(f"WebP versions: {webp_count}")
    print(f"Oversized (>{MAX_SIZE_KB}KB): {len(oversized)}")
    print(f"Missing WebP: {len(jpg_png)}")
    print("=" * 70)


def compress_png(img_info: ImageInfo, quality: int = COMPRESSION_QUALITY) -> Tuple[bool, float]:
    """Compress a PNG image. Returns (success, new_size_kb)."""
    path = img_info.path

    try:
        with Image.open(path) as img:
            # Convert to RGB if necessary (remove alpha for better compression)
            if img.mode == 'RGBA':
                # Keep alpha channel, but optimize
                optimized = img.copy()
            elif img.mode == 'P':
                optimized = img.copy()
            else:
                optimized = img.convert('RGB')

            # Save with optimization
            temp_path = path.with_suffix('.temp.png')
            optimized.save(temp_path, 'PNG', optimize=True)

            new_size_kb = temp_path.stat().st_size / 1024

            # If still too large, try converting to JPEG
            if new_size_kb > MAX_SIZE_KB and img.mode != 'RGBA':
                jpeg_path = path.with_suffix('.temp.jpg')
                rgb_img = img.convert('RGB')
                rgb_img.save(jpeg_path, 'JPEG', quality=quality, optimize=True)
                jpeg_size = jpeg_path.stat().st_size / 1024

                if jpeg_size < new_size_kb:
                    # JPEG is smaller, but we'll keep PNG and just note it
                    os.remove(jpeg_path)
                    print(f"  NOTE: {path.name} could be {jpeg_size:.0f}KB as JPEG")

            # Replace original with optimized
            os.replace(temp_path, path)

            return True, new_size_kb

    except Exception as e:
        print(f"  ERROR compressing {path.name}: {e}")
        # Clean up temp files
        for temp in path.parent.glob('*.temp.*'):
            temp.unlink()
        return False, img_info.size_kb


def compress_jpeg(img_info: ImageInfo, quality: int = COMPRESSION_QUALITY) -> Tuple[bool, float]:
    """Compress a JPEG image. Returns (success, new_size_kb)."""
    path = img_info.path

    try:
        with Image.open(path) as img:
            # Save with optimization
            temp_path = path.with_suffix('.temp.jpg')
            img.save(temp_path, 'JPEG', quality=quality, optimize=True)

            new_size_kb = temp_path.stat().st_size / 1024

            # Only replace if smaller
            if new_size_kb < img_info.size_kb:
                os.replace(temp_path, path)
                return True, new_size_kb
            else:
                os.remove(temp_path)
                return False, img_info.size_kb

    except Exception as e:
        print(f"  ERROR compressing {path.name}: {e}")
        return False, img_info.size_kb


def compress_oversized_images(images: List[ImageInfo]):
    """Compress all oversized images."""
    oversized = [img for img in images if img.needs_compression]

    if not oversized:
        print("\nNo oversized images to compress.")
        return

    print(f"\nCompressing {len(oversized)} oversized images...")
    print("-" * 70)

    total_saved = 0
    for img in oversized:
        old_size = img.size_kb

        if img.format == 'PNG':
            success, new_size = compress_png(img)
        elif img.format == 'JPEG':
            success, new_size = compress_jpeg(img)
        else:
            print(f"  SKIP: {img.path.name} (unsupported format: {img.format})")
            continue

        if success and new_size < old_size:
            saved = old_size - new_size
            total_saved += saved
            old_str = f"{old_size:.0f}KB" if old_size < 1024 else f"{old_size/1024:.1f}MB"
            new_str = f"{new_size:.0f}KB" if new_size < 1024 else f"{new_size/1024:.1f}MB"
            print(f"  {img.path.name}: {old_str} -> {new_str} (saved {saved:.0f}KB)")
        else:
            print(f"  {img.path.name}: No significant compression possible")

    print(f"\nTotal saved: {total_saved/1024:.2f} MB")


def generate_webp(img_info: ImageInfo, quality: int = WEBP_QUALITY) -> bool:
    """Generate a WebP version of an image."""
    path = img_info.path
    webp_path = path.with_suffix('.webp')

    if webp_path.exists():
        return False  # Already exists

    try:
        with Image.open(path) as img:
            # Convert to RGB if necessary (WebP handles RGBA too)
            if img.mode in ['RGBA', 'P']:
                # Keep as-is for transparency support
                pass
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            img.save(webp_path, 'WEBP', quality=quality, method=6)

        new_size = webp_path.stat().st_size / 1024
        return True

    except Exception as e:
        print(f"  ERROR creating WebP for {path.name}: {e}")
        return False


def generate_missing_webp(images: List[ImageInfo]):
    """Generate WebP versions for all images missing them."""
    missing = [img for img in images if img.format in ['JPEG', 'PNG'] and not img.has_webp]

    if not missing:
        print("\nAll JPG/PNG images already have WebP versions.")
        return

    print(f"\nGenerating WebP for {len(missing)} images...")
    print("-" * 70)

    for img in missing:
        success = generate_webp(img)
        if success:
            webp_path = img.path.with_suffix('.webp')
            webp_size = webp_path.stat().st_size / 1024
            orig_str = f"{img.size_kb:.0f}KB" if img.size_kb < 1024 else f"{img.size_kb/1024:.1f}MB"
            webp_str = f"{webp_size:.0f}KB"
            savings = ((img.size_kb - webp_size) / img.size_kb) * 100
            print(f"  {img.path.name} -> .webp ({orig_str} -> {webp_str}, {savings:.0f}% smaller)")


def print_dimensions_for_html(images: List[ImageInfo]):
    """Print image dimensions in a format useful for adding to HTML."""
    print("\n" + "=" * 70)
    print("IMAGE DIMENSIONS FOR HTML width/height ATTRIBUTES")
    print("=" * 70)
    print()

    # Sort alphabetically
    images_sorted = sorted(images, key=lambda x: x.path.name.lower())

    for img in images_sorted:
        print(f'{img.path.name}: width="{img.width}" height="{img.height}"')


def main():
    parser = argparse.ArgumentParser(description='Optimize images for LotterLaw website')
    parser.add_argument('--audit', action='store_true', help='Audit images only')
    parser.add_argument('--compress', action='store_true', help='Compress oversized images')
    parser.add_argument('--webp', action='store_true', help='Generate missing WebP versions')
    parser.add_argument('--dimensions', action='store_true', help='Print dimensions for HTML')
    parser.add_argument('--all', action='store_true', help='Do everything')

    args = parser.parse_args()

    # Default to audit if no action specified
    if not any([args.audit, args.compress, args.webp, args.dimensions, args.all]):
        args.audit = True

    print(f"Scanning: {ASSETS_DIR}")
    images = audit_images()

    if args.audit or args.all:
        print_audit_report(images)

    if args.compress or args.all:
        compress_oversized_images(images)
        # Re-audit after compression
        images = audit_images()

    if args.webp or args.all:
        generate_missing_webp(images)
        # Re-audit after WebP generation
        images = audit_images()

    if args.dimensions:
        print_dimensions_for_html(images)

    if args.all:
        # Final report
        print("\n" + "=" * 70)
        print("FINAL STATUS")
        print("=" * 70)
        print_audit_report(images)


if __name__ == '__main__':
    main()
