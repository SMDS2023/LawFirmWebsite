import os
import re

website_dir = r"C:\Users\jeff\OneDrive\Documents\LotterLaw\Website"

# Counters
svg_fixed = 0
maps_fixed = 0
favicon_added = 0

# New Google Maps direct link
new_maps_link = "https://www.google.com/maps/place/200+E+Robinson+St+%231140,+Orlando,+FL+32801"

# Favicon HTML (for pages in root)
favicon_html_root = '''    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='16' fill='%231e40af'/%3E%3Ctext x='16' y='21' font-family='Georgia,serif' font-size='14' font-weight='bold' fill='white' text-anchor='middle'%3ELL%3C/text%3E%3C/svg%3E">
    <link rel="apple-touch-icon" href="assets/Lotter-Law-logo-02.jpg">

'''

# Favicon HTML (for pages in subdirs like /blog/ or /practice-areas/)
favicon_html_subdir = '''    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='16' fill='%231e40af'/%3E%3Ctext x='16' y='21' font-family='Georgia,serif' font-size='14' font-weight='bold' fill='white' text-anchor='middle'%3ELL%3C/text%3E%3C/svg%3E">
    <link rel="apple-touch-icon" href="../assets/Lotter-Law-logo-02.jpg">

'''

for root, dirs, files in os.walk(website_dir):
    # Skip hidden directories and output directories
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['output', 'scripts', 'analytics']]

    for filename in files:
        if filename.endswith('.html'):
            filepath = os.path.join(root, filename)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # 1. Fix SVG dimensions
                if 'class="cta-icon" fill="none" viewBox' in content:
                    content = content.replace(
                        'class="cta-icon" fill="none" viewBox="0 0 24 24"',
                        'class="cta-icon" width="24" height="24" fill="none" viewBox="0 0 24 24"'
                    )
                    svg_fixed += 1

                # 2. Fix Google Maps broken link
                if 'maps.app.goo.gl/y7xK1jYj7k8zM6Q2A' in content:
                    content = content.replace(
                        'https://maps.app.goo.gl/y7xK1jYj7k8zM6Q2A',
                        new_maps_link
                    )
                    maps_fixed += 1

                # 3. Add favicon if missing (skip if already has favicon)
                if 'rel="icon"' not in content and '<title>' in content:
                    # Determine if in subdir
                    rel_path = os.path.relpath(filepath, website_dir)
                    is_subdir = os.path.dirname(rel_path) != ''

                    favicon_html = favicon_html_subdir if is_subdir else favicon_html_root

                    # Insert after </title>
                    content = content.replace('</title>\n', '</title>\n\n' + favicon_html)
                    favicon_added += 1

                # Write if changed
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated: {rel_path}")

            except Exception as e:
                print(f"Error processing {filepath}: {e}")

print(f"\n--- Summary ---")
print(f"SVG dimensions fixed: {svg_fixed}")
print(f"Google Maps links fixed: {maps_fixed}")
print(f"Favicons added: {favicon_added}")
