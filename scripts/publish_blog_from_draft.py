#!/usr/bin/env python3
"""
Blog Publishing Pipeline - Full Automation

Converts a markdown draft to HTML and runs the complete publishing workflow:
1. Parse markdown draft
2. Generate HTML with full template (GTM, schema, breadcrumbs, CTA, etc.)
3. Run SEO check/fix
4. Run cross-linking
5. Set sequential publish date
6. Optionally commit and push to deploy

Usage:
    python publish_blog_from_draft.py output/blog_drafts/blog_draft_2025-12-15_hto-removed.md
    python publish_blog_from_draft.py output/blog_drafts/blog_draft_2025-12-15_hto-removed.md --publish
    python publish_blog_from_draft.py output/blog_drafts/blog_draft_2025-12-15_hto-removed.md --dry-run

Arguments:
    draft_file      Path to the markdown draft file
    --publish       Also commit and push to deploy (default: stop before git)
    --dry-run       Generate HTML but don't run any scripts
    --number N      Override auto-detected blog post number
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configuration
WEBSITE_DIR = Path(__file__).parent.parent
BLOG_DIR = WEBSITE_DIR / "blog"
SCRIPTS_DIR = WEBSITE_DIR / "scripts"

# Template constants
GTM_ID = "GTM-PLX85K8L"
GA4_ID = "G-2MCJ8E0XS5"
CLARITY_ID = "reu4dibx4h"
SITE_URL = "https://lotterlaw.com"
AUTHOR = "Jeff Lotter"


class MarkdownDraft:
    """Parsed markdown draft content."""

    def __init__(self):
        self.title = ""
        self.alternate_titles: List[str] = []
        self.meta_description = ""
        self.url_slug = ""
        self.keywords: List[str] = []
        self.category = "CRIMINAL DEFENSE"
        self.subtitle = ""
        self.intro = ""
        self.sections: List[Dict] = []  # [{heading, content, subsections}]
        self.case_context = ""
        self.cta_content = ""
        self.related_practice_areas: List[str] = []
        self.is_case_result = False


def get_next_blog_number() -> int:
    """Find the next available blog post number."""
    existing = list(BLOG_DIR.glob("*.html"))
    numbers = []
    for f in existing:
        match = re.match(r'^(\d+)-', f.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers) + 1 if numbers else 1


def parse_markdown_draft(filepath: Path) -> MarkdownDraft:
    """Parse markdown draft file into structured content."""
    content = filepath.read_text(encoding="utf-8")
    draft = MarkdownDraft()

    # Extract title
    title_match = re.search(r'^# Blog Post Draft: (.+)$', content, re.MULTILINE)
    if title_match:
        draft.title = title_match.group(1).strip()

    # Check if case result
    draft.is_case_result = "case result" in content.lower() or "success story" in content.lower()

    # Extract alternate titles
    alt_section = re.search(r'\*\*Alternates:\*\*\n((?:- .+\n?)+)', content)
    if alt_section:
        draft.alternate_titles = [
            line.strip('- \n') for line in alt_section.group(1).split('\n')
            if line.strip().startswith('-')
        ]

    # Extract meta description
    meta_match = re.search(r'\*\*Meta Description:\*\* (.+)', content)
    if meta_match:
        draft.meta_description = meta_match.group(1).strip()

    # Extract URL slug
    slug_match = re.search(r'\*\*URL Slug:\*\* `?([^`\n]+)`?', content)
    if slug_match:
        draft.url_slug = slug_match.group(1).strip()

    # Extract keywords
    keywords_section = re.search(r'\*\*Target Keywords:\*\*\n((?:- .+\n?)+)', content)
    if keywords_section:
        draft.keywords = [
            line.strip('- \n') for line in keywords_section.group(1).split('\n')
            if line.strip().startswith('-')
        ]

    # Extract category if specified
    cat_match = re.search(r'\*\*Category:\*\* (.+)', content)
    if cat_match:
        draft.category = cat_match.group(1).strip().upper()

    # Extract subtitle if present
    subtitle_match = re.search(r'\*\*Subtitle:\*\* (.+)', content)
    if subtitle_match:
        draft.subtitle = subtitle_match.group(1).strip()

    # Extract sections (H2 and H3 headings with content)
    # Look for ### H2: or ## Content Outline sections
    section_pattern = re.compile(
        r'### (?:H2: )?(.+?)\n\n'
        r'(?:\*\*Key Points:\*\*\n((?:- .+\n?)+))?'
        r'(?:\n\*\*Subsections[^:]*:\*\*\n((?:- .+\n?)+))?',
        re.MULTILINE
    )

    for match in section_pattern.finditer(content):
        heading = match.group(1).strip()
        key_points = []
        subsections = []

        if match.group(2):
            key_points = [
                line.strip('- \n') for line in match.group(2).split('\n')
                if line.strip().startswith('-')
            ]

        if match.group(3):
            subsections = [
                line.strip('- \n') for line in match.group(3).split('\n')
                if line.strip().startswith('-')
            ]

        # Skip meta sections
        if heading.lower() not in ['title options', 'seo elements', 'internal links',
                                    'html template requirements', 'notes for final draft',
                                    'notes for jeff']:
            draft.sections.append({
                'heading': heading,
                'key_points': key_points,
                'subsections': subsections
            })

    # Extract case context
    case_context_match = re.search(
        r'\*\*Case Context \(Anonymized\):\*\*\n(.+?)(?=\n---|\n\*Note:|\Z)',
        content, re.DOTALL
    )
    if case_context_match:
        draft.case_context = case_context_match.group(1).strip()

    # Also try table format
    if not draft.case_context:
        table_match = re.search(r'\| Element \| Detail \|.+?\n\n', content, re.DOTALL)
        if table_match:
            draft.case_context = table_match.group(0).strip()

    # Extract related practice areas
    pa_section = re.search(r'\*\*Related Practice Areas:\*\*\n((?:- .+\n?)+)', content)
    if pa_section:
        draft.related_practice_areas = [
            re.sub(r'\[|\]|\(.+?\)', '', line.strip('- \n')).strip()
            for line in pa_section.group(1).split('\n')
            if line.strip().startswith('-')
        ]

    return draft


def generate_html(draft: MarkdownDraft, blog_number: int) -> str:
    """Generate full HTML blog post from parsed draft."""

    filename = f"{blog_number:02d}-{draft.url_slug}.html"
    canonical_url = f"{SITE_URL}/blog/{filename}"
    today = datetime.now().strftime("%Y-%m-%d")
    display_date = datetime.now().strftime("%B %d, %Y")

    # Generate keywords meta tag
    keywords_meta = ", ".join(draft.keywords[:10]) if draft.keywords else ""

    # Generate article schema keywords
    schema_keywords = draft.keywords[:5] if draft.keywords else []

    # Build sections HTML
    sections_html = []
    for section in draft.sections:
        section_html = f'''
                <section class="mb-12">
                    <h2 class="text-3xl font-bold text-blue-800 mb-6">{section['heading']}</h2>
'''

        if section['key_points']:
            section_html += '''
                    <ul class="list-disc pl-6 mb-6 text-lg text-gray-700 space-y-2">
'''
            for point in section['key_points']:
                section_html += f'                        <li>{point}</li>\n'
            section_html += '                    </ul>\n'

        if section['subsections']:
            for sub in section['subsections']:
                section_html += f'''
                    <h3 class="text-2xl font-semibold text-blue-700 mb-4 mt-8">{sub}</h3>
                    <p class="text-lg text-gray-700 mb-4">[Content for {sub}]</p>
'''

        section_html += '                </section>'
        sections_html.append(section_html)

    all_sections = '\n'.join(sections_html)

    # Case result badge
    case_result_badge = ''
    if draft.is_case_result:
        case_result_badge = '''
                <span class="inline-block bg-green-100 text-green-800 text-sm font-semibold px-3 py-1 rounded-full mb-4">CASE RESULT</span>'''

    # Related practice areas links
    practice_area_links = ''
    if draft.related_practice_areas:
        links = []
        for pa in draft.related_practice_areas[:3]:
            pa_file = pa.replace('practice-areas/', '').strip('/')
            links.append(f'<a href="../practice-areas/{pa_file}" class="text-blue-600 hover:underline">{pa_file.replace(".html", "").replace("-", " ").title()}</a>')
        practice_area_links = ' | '.join(links)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','{GTM_ID}');</script>
    <!-- End Google Tag Manager -->
    <!-- Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA4_ID}');
    </script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{draft.title}</title>
    <meta name="description" content="{draft.meta_description}">
    <meta name="keywords" content="{keywords_meta}">

    <!-- Canonical URL -->
    <link rel="canonical" href="{canonical_url}">

    <!-- Open Graph Tags -->
    <meta property="og:title" content="{draft.title}">
    <meta property="og:description" content="{draft.meta_description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:image" content="{SITE_URL}/assets/Lotter-Law-logo-02.jpg">
    <meta property="og:locale" content="en_US">
    <meta property="og:site_name" content="Lotter Law">
    <meta property="article:published_time" content="{today}">
    <meta property="article:author" content="{AUTHOR}">

    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{draft.title}">
    <meta name="twitter:description" content="{draft.meta_description}">
    <meta name="twitter:image" content="{SITE_URL}/assets/Lotter-Law-logo-02.jpg">

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.tailwindcss.com/typography@0.5.x"></script>

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Tinos:wght@400;700&display=swap" rel="stylesheet">

    <!-- Alpine JS -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

    <!-- Site Styles -->
    <link rel="stylesheet" href="../styles.css">

    <!-- Clarity Analytics -->
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "{CLARITY_ID}");
    </script>

    <style>
        .info-box {{
            background: #eff6ff;
            border-left: 4px solid #2563eb;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0.375rem;
        }}
        .warning-box {{
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0.375rem;
        }}
        .tip-box {{
            background: #f0fdf4;
            border-left: 4px solid #22c55e;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0.375rem;
        }}
    </style>

    <!-- Article Schema -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{draft.title}",
        "description": "{draft.meta_description}",
        "author": {{
            "@type": "Person",
            "name": "{AUTHOR}",
            "jobTitle": "Criminal Defense Attorney",
            "url": "{SITE_URL}"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "Lotter Law",
            "logo": {{
                "@type": "ImageObject",
                "url": "{SITE_URL}/assets/Lotter-Law-logo-02.jpg"
            }}
        }},
        "datePublished": "{today}",
        "dateModified": "{today}",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "{canonical_url}"
        }},
        "articleSection": "{draft.category}",
        "keywords": {schema_keywords}
    }}
    </script>

    <!-- Schema.org BreadcrumbList -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "{SITE_URL}"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Blog",
          "item": "{SITE_URL}/blog.html"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{draft.title}",
          "item": "{canonical_url}"
        }}
      ]
    }}
    </script>
</head>
<body class="bg-gray-50 text-gray-800">
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->

    <!-- Header -->
    <header class="bg-white shadow-md sticky top-0 z-50">
        <nav class="container mx-auto px-6 py-3 flex justify-between items-center">
            <div>
                <a href="../index.html">
                    <img src="../assets/Lotter-Law-logo-02.jpg" alt="Lotter Law Logo" class="header-logo"
                         onerror="this.style.display='none'; this.parentElement.innerHTML = '<span class=\\'text-2xl font-bold text-blue-800\\'>Lotter Law</span>';">
                </a>
            </div>
            <div class="hidden md:flex space-x-4 items-center">
                <a href="../index.html#practice-areas-grid" class="text-gray-600 hover:text-blue-700 px-3 py-2 rounded-md text-sm font-medium">Practice Areas</a>
                <a href="../index.html#team" class="text-gray-600 hover:text-blue-700 px-3 py-2 rounded-md text-sm font-medium">Our Team</a>
                <a href="../index.html#testimonials" class="text-gray-600 hover:text-blue-700 px-3 py-2 rounded-md text-sm font-medium">Testimonials</a>
                <a href="../index.html#faq" class="text-gray-600 hover:text-blue-700 px-3 py-2 rounded-md text-sm font-medium">FAQ</a>
                <a href="../index.html#contact" class="text-gray-600 hover:text-blue-700 px-3 py-2 rounded-md text-sm font-medium">Contact</a>
                <a href="../blog.html" class="text-blue-700 font-semibold px-3 py-2 rounded-md text-sm font-medium">Blog</a>
                <a href="tel:407-500-7000" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-300 text-sm ml-2">Call Now: 407-500-7000</a>
            </div>
            <div class="md:hidden">
                <button id="mobile-menu-button" class="text-gray-600 hover:text-blue-700 focus:outline-none" aria-label="Open menu">
                    <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"/>
                    </svg>
                </button>
            </div>
        </nav>
        <div id="mobile-menu" class="md:hidden hidden bg-white border-t border-gray-200">
            <div class="px-2 pt-2 pb-3 space-y-1">
                <a href="../index.html#practice-areas-grid" class="text-gray-600 hover:bg-gray-100 block px-3 py-2 rounded-md text-base font-medium">Practice Areas</a>
                <a href="../blog.html" class="bg-blue-50 text-blue-700 block px-3 py-2 rounded-md text-base font-medium">Blog</a>
                <a href="../index.html#team" class="text-gray-600 hover:bg-gray-100 block px-3 py-2 rounded-md text-base font-medium">Our Team</a>
                <a href="../index.html#contact" class="text-gray-600 hover:bg-gray-100 block px-3 py-2 rounded-md text-base font-medium">Contact</a>
                <a href="tel:407-500-7000" class="bg-blue-600 text-white block text-center font-semibold py-2 px-4 rounded-lg mt-2">Call Now: 407-500-7000</a>
            </div>
        </div>
    </header>

    <!-- Breadcrumb Navigation -->
    <nav aria-label="Breadcrumb" class="bg-gray-100 border-b border-gray-200">
        <div class="container mx-auto px-6 py-3">
            <ol class="flex items-center text-sm">
                <a href="../index.html" class="text-blue-600 hover:text-blue-800 hover:underline">Home</a>
                <svg class="w-4 h-4 text-gray-400 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
                <a href="../blog.html" class="text-blue-600 hover:text-blue-800 hover:underline">Blog</a>
                <svg class="w-4 h-4 text-gray-400 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
                <span class="text-gray-600 font-medium" aria-current="page">{draft.title}</span>
            </ol>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="py-12 md:py-16">
        <div class="container mx-auto px-6 max-w-4xl">
            <!-- Hero Section -->
            <header class="mb-12">
                <p class="text-blue-600 font-semibold mb-2">{draft.category}</p>{case_result_badge}
                <h1 class="text-4xl md:text-5xl font-hero-heading font-bold text-blue-800 mb-6 text-center">
                    {draft.title}
                </h1>
                {f'<p class="text-2xl text-gray-700 mb-8 text-center font-semibold">{draft.subtitle}</p>' if draft.subtitle else ''}

                <div class="text-center mb-8">
                    <p class="text-sm text-gray-500 mb-4">{display_date} | Orlando, Florida</p>
                </div>
            </header>

            <div class="prose prose-lg max-w-none">
{all_sections}

                <!-- Final CTA -->
                <section class="mb-12">
                    <div class="bg-blue-700 text-white rounded-lg p-8 text-center">
                        <h2 class="text-3xl font-bold mb-4">Need Help With Your Case?</h2>
                        <p class="text-xl mb-6">
                            As a former law enforcement officer turned defense attorney, I understand how these cases work from both sides. Let's talk about your options.
                        </p>

                        <div class="space-y-4">
                            <p class="text-lg mb-6">
                                <strong>Free Consultation | Aggressive Defense | Results-Focused</strong>
                            </p>

                            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                                <a href="tel:407-500-7000" class="bg-amber-500 hover:bg-amber-600 text-white font-bold py-4 px-8 rounded-lg text-xl transition duration-300 shadow-lg inline-flex items-center justify-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                                    Call: 407-500-7000
                                </a>
                                <a href="../index.html#contact" class="bg-white hover:bg-gray-100 text-blue-700 font-bold py-4 px-8 rounded-lg text-xl transition duration-300 shadow-lg">
                                    Request Free Consultation
                                </a>
                            </div>

                            <p class="text-base mt-6">
                                Law Office of Jeff Lotter PLLC<br>
                                Serving Orlando, Orange County, and Central Florida
                            </p>
                        </div>
                    </div>
                </section>

            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-800 text-gray-400 py-6 text-center">
        <div class="container mx-auto px-6">
            <div class="mb-3">
                <p class="text-sm font-semibold text-gray-300 mb-1">Jeff Lotter, Attorney at Law</p>
                <p class="text-xs">Florida Bar Member since 2015 | Office in Orlando, Florida</p>
            </div>
            <div class="mb-2">
                <a href="../privacy.html" class="text-sm hover:text-white hover:underline">Privacy Policy</a>
            </div>
            <p class="text-sm">&copy; <span id="current-year"></span> Lotter Law. All Rights Reserved.</p>
            <p class="text-xs mt-2">Disclaimer: The information on this website is for general information purposes only. Nothing on this site should be taken as legal advice for any individual case or situation.</p>
        </div>
    </footer>

    <!-- Scripts -->
    <script>
        // Mobile Menu Toggle
        const menuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        if (menuButton && mobileMenu) {{
            menuButton.addEventListener('click', () => {{
                mobileMenu.classList.toggle('hidden');
            }});
        }}
        // Set current year
        document.getElementById('current-year').textContent = new Date().getFullYear();
    </script>

    <!-- Mobile Sticky CTA Bar -->
    <div class="mobile-cta-bar urgent" id="mobile-cta-bar">
        <a href="tel:407-500-7000"
           onclick="if(typeof gtag === 'function') gtag('event', 'click_to_call', {{event_category: 'CTA', event_label: 'Mobile Sticky Bar', phone_number: '407-500-7000'}});"
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

</body>
</html>
'''
    return html, filename


def update_blog_sidebar(filename: str, draft: MarkdownDraft, dry_run: bool = False) -> bool:
    """Update the floating blog sidebar on index.html with the new post."""
    index_html = WEBSITE_DIR / "index.html"

    if not index_html.exists():
        print(f"  Warning: index.html not found")
        return False

    content = index_html.read_text(encoding="utf-8")

    # Check if entry already exists
    if filename in content:
        print(f"  Entry already exists in sidebar")
        return True

    # Create short title (truncate if needed)
    short_title = draft.title
    if len(short_title) > 40:
        short_title = short_title[:37] + "..."

    # Build new entry
    case_result_span = ""
    if draft.is_case_result:
        case_result_span = '\n                <span class="case-result">Case Result</span>'

    new_entry = f'''            <a href="blog/{filename}" class="blog-link">{case_result_span}
                {short_title}
            </a>
'''

    # Find insertion point (after <h3>Recent Blog Posts</h3> and newline)
    marker = '<h3>Recent Blog Posts</h3>'
    marker_pos = content.find(marker)

    if marker_pos == -1:
        print(f"  Warning: Could not find 'Recent Blog Posts' in index.html")
        return False

    # Find the position after the marker and any whitespace
    insert_pos = marker_pos + len(marker)
    while insert_pos < len(content) and content[insert_pos] in '\n\r\t ':
        insert_pos += 1

    # Insert the new entry
    new_content = content[:insert_pos] + '\n' + new_entry + content[insert_pos:]

    # Now remove the 5th recent post (keep only 4) to prevent unlimited growth
    # Count blog-link entries before "Featured Topics" and remove the 5th one
    featured_marker = '<p class="category-label">Featured Topics</p>'
    featured_pos = new_content.find(featured_marker)

    if featured_pos != -1:
        # Find all blog-link entries between Recent Blog Posts and Featured Topics
        recent_section = new_content[marker_pos:featured_pos]
        blog_links = list(re.finditer(r'<a href="blog/[^"]+\.html" class="blog-link">.*?</a>\s*', recent_section, re.DOTALL))

        if len(blog_links) > 4:
            # Remove the 5th (oldest) entry
            fifth_link = blog_links[4]
            start = marker_pos + fifth_link.start()
            end = marker_pos + fifth_link.end()
            new_content = new_content[:start] + new_content[end:]
            print(f"  Removed oldest entry from sidebar (keeping 4 recent)")

    if dry_run:
        print(f"  [DRY RUN] Would update blog sidebar in index.html")
        return True

    index_html.write_text(new_content, encoding="utf-8")
    print(f"  Updated blog sidebar in index.html")
    return True


def add_to_blog_listing(filename: str, draft: MarkdownDraft, dry_run: bool = False) -> bool:
    """Add new blog post entry to blog.html."""
    blog_html = WEBSITE_DIR / "blog.html"

    if not blog_html.exists():
        print(f"  Warning: blog.html not found")
        return False

    content = blog_html.read_text(encoding="utf-8")

    # Check if entry already exists
    if filename in content:
        print(f"  Entry already exists in blog.html")
        return True

    # Extract post number from filename
    post_num = filename.split('-')[0]

    # Build the description (use meta description or first 150 chars of title)
    description = draft.meta_description if draft.meta_description else f"Read about {draft.title}"
    if len(description) > 160:
        description = description[:157] + "..."

    # Get today's date for display
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    date_display = today.strftime("%B %d, %Y").replace(" 0", " ")

    # Case result badge if applicable
    case_result_line = ""
    if draft.is_case_result:
        case_result_line = '        <p class="text-xs font-semibold text-green-600 uppercase tracking-wide mb-1">Case Result</p>\n'

    # Build new entry HTML
    new_entry = f'''
<!-- Blog Entry {post_num} - {draft.title[:50]} -->
<article class="bg-white p-6 md:p-8 rounded-lg shadow-lg blog-post-summary section-fade-in">
    <header>
{case_result_line}        <h2 class="text-2xl md:text-3xl font-semibold text-blue-700 mb-2">
            <a href="blog\\{filename}" class="hover:text-amber-500">{draft.title}</a>
        </h2>
        <p class="text-sm text-gray-500 mb-3">
            <time datetime="{date_str}">{date_display}</time> | {description}
        </p>
    </header>
    <a href="blog\\{filename}" class="inline-block text-amber-600 hover:text-amber-700 font-semibold transition duration-300 mt-2">
        Read Full Article →
    </a>
</article>

'''

    # Find insertion point (after <div class="max-w-3xl mx-auto space-y-10">)
    insertion_marker = '<div class="max-w-3xl mx-auto space-y-10">'

    if insertion_marker in content:
        # Insert after the marker and newline
        insert_pos = content.find(insertion_marker) + len(insertion_marker)
        # Skip any whitespace/newlines after marker
        while insert_pos < len(content) and content[insert_pos] in '\n\r':
            insert_pos += 1

        new_content = content[:insert_pos] + new_entry + content[insert_pos:]

        if dry_run:
            print(f"  [DRY RUN] Would add entry to blog.html")
            return True

        blog_html.write_text(new_content, encoding="utf-8")
        print(f"  Added entry to blog.html")
        return True
    else:
        print(f"  Warning: Could not find insertion point in blog.html")
        return False


def run_script(script_name: str, args: List[str], dry_run: bool = False) -> bool:
    """Run a Python script from the scripts directory."""
    script_path = SCRIPTS_DIR / script_name

    if not script_path.exists():
        print(f"  Warning: Script not found: {script_path}")
        return False

    cmd = [sys.executable, str(script_path)] + args

    if dry_run:
        print(f"  [DRY RUN] Would run: {' '.join(cmd)}")
        return True

    print(f"  Running: {script_name} {' '.join(args)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=WEBSITE_DIR)
        if result.returncode != 0:
            print(f"  Error: {result.stderr}")
            return False
        if result.stdout:
            print(f"  {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"  Error running script: {e}")
        return False


def run_git_commands(filename: str, dry_run: bool = False) -> bool:
    """Run git add, commit, and push."""
    if dry_run:
        print("  [DRY RUN] Would run git add, commit, push")
        return True

    try:
        # Git add
        print("  Running: git add")
        subprocess.run(["git", "add", f"blog/{filename}", "blog.html", "blog/*.html"],
                      cwd=WEBSITE_DIR, check=True, capture_output=True)

        # Git commit
        print("  Running: git commit")
        post_num = filename.split('-')[0]
        title_part = '-'.join(filename.split('-')[1:]).replace('.html', '')[:40]
        commit_msg = f"feat(blog): Publish post #{post_num} - {title_part}"
        subprocess.run(["git", "commit", "-m", commit_msg],
                      cwd=WEBSITE_DIR, check=True, capture_output=True)

        # Git push
        print("  Running: git push")
        subprocess.run(["git", "push", "origin", "master"],
                      cwd=WEBSITE_DIR, check=True, capture_output=True)

        return True
    except subprocess.CalledProcessError as e:
        print(f"  Git error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Convert markdown draft to HTML and run full publishing pipeline"
    )
    parser.add_argument("draft_file", help="Path to markdown draft file")
    parser.add_argument("--publish", action="store_true",
                       help="Also commit and push to deploy")
    parser.add_argument("--dry-run", action="store_true",
                       help="Generate HTML but don't run scripts")
    parser.add_argument("--number", type=int,
                       help="Override blog post number")

    args = parser.parse_args()

    draft_path = Path(args.draft_file)
    if not draft_path.exists():
        print(f"Error: Draft file not found: {draft_path}")
        sys.exit(1)

    print("=" * 60)
    print("Blog Publishing Pipeline")
    print("=" * 60)
    print()

    # Step 1: Parse markdown
    print("Step 1: Parsing markdown draft...")
    draft = parse_markdown_draft(draft_path)
    print(f"  Title: {draft.title}")
    print(f"  Slug: {draft.url_slug}")
    print(f"  Sections: {len(draft.sections)}")
    print()

    # Step 2: Determine blog number
    blog_number = args.number if args.number else get_next_blog_number()
    print(f"Step 2: Blog post number: {blog_number}")
    print()

    # Step 3: Generate HTML
    print("Step 3: Generating HTML...")
    html_content, filename = generate_html(draft, blog_number)
    output_path = BLOG_DIR / filename

    if not args.dry_run:
        output_path.write_text(html_content, encoding="utf-8")
        print(f"  Created: {output_path}")
    else:
        print(f"  [DRY RUN] Would create: {output_path}")
    print()

    # Step 4: Add to blog.html listing
    print("Step 4: Adding to blog.html listing...")
    add_to_blog_listing(filename, draft, args.dry_run)
    print()

    # Step 5: Update blog sidebar on index.html
    print("Step 5: Updating blog sidebar on index.html...")
    update_blog_sidebar(filename, draft, args.dry_run)
    print()

    # Step 6: SEO check/fix
    print("Step 6: Running SEO check/fix...")
    run_script("seo_checker.py", [f"blog/{filename}", "--fix"], args.dry_run)
    print()

    # Step 7: Cross-linking
    print("Step 7: Running cross-linker...")
    run_script("cross_linker.py", [f"blog/{filename}"], args.dry_run)
    print()

    # Step 8: Set publish date
    print("Step 8: Setting publish date...")
    run_script("backdate_posts.py", [f"blog/{filename}"], args.dry_run)
    print()

    # Step 9: Git (optional)
    if args.publish:
        print("Step 9: Committing and pushing...")
        run_git_commands(filename, args.dry_run)
        print()

        print("Step 10: Deployment...")
        print(f"  View at: {SITE_URL}/blog/{filename}")
        print("  (Wait 60-90 seconds for GitHub Pages)")
    else:
        print("Step 9: Skipped git (use --publish to deploy)")
        print()
        print(f"  HTML ready at: {output_path}")
        print(f"  To publish: python publish_blog_from_draft.py {draft_path} --publish")

    print()
    print("=" * 60)
    print("Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
