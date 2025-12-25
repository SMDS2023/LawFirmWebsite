#!/usr/bin/env python3
"""
Blog Post Draft Generator (T-013)

Generates blog post draft outlines from topic suggestions created by blog_topic_generator.py.
Outputs structured markdown with SEO elements, anonymized case details, and CTA placement.

Usage:
    python blog_draft_generator.py --topic "What Happens If You Get a DUI Charge in Florida?"
    python blog_draft_generator.py --suggestion-file ./output/blog_suggestions/blog_suggestions_2025-12-13.md --topic-num 1
    python blog_draft_generator.py --interactive

Output:
    Creates blog_draft_YYYY-MM-DD_topic-slug.md in output/blog_drafts/
"""

import argparse
import json
import re
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Configuration
BASE_DIR = Path(__file__).parent.parent.parent.parent  # Documents folder
WEBSITE_DIR = Path(__file__).parent.parent  # Website folder
CONFIG_DIR = Path(__file__).parent / "config"
OUTPUT_DIR = WEBSITE_DIR / "output" / "blog_drafts"
SUGGESTIONS_DIR = WEBSITE_DIR / "output" / "blog_suggestions"
EXISTING_BLOGS_DIR = WEBSITE_DIR / "blog"

# Case file locations (same as blog_topic_generator.py)
CASE_FILE_LOCATIONS = [
    BASE_DIR / "LotterLaw" / "Active-Cases",
    BASE_DIR / "LotterLaw" / "Case-Management",
    BASE_DIR / "LotterLaw" / "Blog",
]


@dataclass
class TopicSuggestion:
    """Parsed topic suggestion from blog_topic_generator output."""
    title: str
    source_type: str
    keyword: str
    score: int
    frequency: int
    outcomes: List[str]
    statutes: List[str]
    suggested_angles: List[str]
    calendar_events: List[Dict]
    case_files: List[Dict]
    gmail_threads: List[Dict]
    drive_files: List[Dict]


@dataclass
class BlogOutline:
    """Generated blog post outline."""
    # Title options
    primary_title: str
    alternate_titles: List[str]

    # SEO elements
    meta_description: str
    target_keywords: List[str]
    url_slug: str

    # Content structure
    intro_hook: str
    h2_sections: List[Dict]  # Each has 'heading', 'key_points', 'subsections'

    # Case references (anonymized)
    case_context: str

    # CTA elements
    cta_primary: str
    cta_secondary: str

    # Internal links
    related_blog_posts: List[str]
    related_practice_areas: List[str]


# Topic templates for different content types
CONTENT_TEMPLATES = {
    "explainer": {
        "intro_pattern": "If you're facing {charge} charges in Florida, understanding what happens next is crucial. As a former law enforcement officer turned defense attorney, I've seen these cases from both sides.",
        "h2_structure": [
            {"heading": "What Is {charge} Under Florida Law?", "focus": "legal_definition"},
            {"heading": "Penalties for {charge} in Florida", "focus": "penalties"},
            {"heading": "How {charge} Cases Are Investigated", "focus": "process"},
            {"heading": "Common Defenses for {charge} Charges", "focus": "defenses"},
            {"heading": "What to Do If You're Charged with {charge}", "focus": "action_steps"},
        ]
    },
    "case_result": {
        "intro_pattern": "Case Result: {outcome}. Every {charge} case is unique, but understanding how successful defenses work can help you know what to expect in your case.",
        "h2_structure": [
            {"heading": "The Situation", "focus": "case_background"},
            {"heading": "The Defense Strategy", "focus": "strategy"},
            {"heading": "The Outcome", "focus": "result"},
            {"heading": "Key Takeaways for Your Case", "focus": "lessons"},
            {"heading": "How We Can Help", "focus": "cta"},
        ]
    },
    "legal_guide": {
        "intro_pattern": "Florida Statute {statute} governs {charge} charges. If you're facing this charge, here's what you need to know about the law and your options.",
        "h2_structure": [
            {"heading": "Understanding F.S. {statute}", "focus": "statute_breakdown"},
            {"heading": "Elements the State Must Prove", "focus": "elements"},
            {"heading": "Common Scenarios", "focus": "examples"},
            {"heading": "Defense Strategies", "focus": "defenses"},
            {"heading": "Why Legal Representation Matters", "focus": "importance"},
        ]
    },
    "outcome_focused": {
        "intro_pattern": "A {outcome} outcome is possible in {charge} cases. Here's what made the difference and what it could mean for your situation.",
        "h2_structure": [
            {"heading": "How {outcome} Happens in {charge} Cases", "focus": "how_it_works"},
            {"heading": "What Led to This Outcome", "focus": "factors"},
            {"heading": "What This Means for You", "focus": "implications"},
            {"heading": "Steps to Take Now", "focus": "action_steps"},
        ]
    }
}

# Keyword to practice area mapping
KEYWORD_TO_PRACTICE_AREA = {
    "dui": "dui.html",
    "dwls": "suspended-license.html",
    "dwlsr": "suspended-license.html",
    "suspended license": "suspended-license.html",
    "traffic": "moving-violations.html",
    "speeding": "speeding-ticket.html",
    "toll": "tolls.html",
    "theft": "theft.html",
    "burglary": "theft.html",
    "drug": "drug-offense.html",
    "possession": "drug-offense.html",
    "marijuana": "drug-offense.html",
    "cannabis": "drug-offense.html",
    "domestic violence": "dv.html",
    "battery": "dv.html",
    "weapons": "weapons.html",
    "firearm": "weapons.html",
    "concealed": "weapons.html",
    "hit and run": "hit-and-run.html",
    "leaving scene": "hit-and-run.html",
    "expunge": "seal-and-expunge.html",
    "seal": "seal-and-expunge.html",
}

# Statute information
STATUTE_INFO = {
    "316.193": {"name": "DUI", "short": "Driving Under the Influence"},
    "322.34": {"name": "DWLS", "short": "Driving While License Suspended"},
    "322.03": {"name": "NVDL", "short": "No Valid Driver's License"},
    "316.027": {"name": "Hit and Run", "short": "Leaving Scene of Accident"},
    "316.1935": {"name": "Fleeing", "short": "Fleeing or Eluding"},
    "893.13": {"name": "Drug Possession", "short": "Possession of Controlled Substance"},
    "790.01": {"name": "CCW", "short": "Carrying Concealed Weapon"},
    "810.02": {"name": "Burglary", "short": "Burglary"},
    "812.014": {"name": "Theft", "short": "Theft"},
    "784.03": {"name": "Battery", "short": "Battery"},
    "741.28": {"name": "DV", "short": "Domestic Violence"},
    "316.183": {"name": "Speeding", "short": "Unlawful Speed"},
}


class BlogDraftGenerator:
    """Generate blog post draft outlines from topic suggestions."""

    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.existing_blogs = self._load_existing_blogs()
        self.topic_templates = self._load_topic_templates()
        self.keyword_mappings = self._load_keyword_mappings()

    def _load_existing_blogs(self) -> Dict[str, str]:
        """Load existing blog post titles and filenames."""
        blogs = {}
        if EXISTING_BLOGS_DIR.exists():
            for f in EXISTING_BLOGS_DIR.glob("*.html"):
                # Extract title from filename
                name = f.stem
                # Remove number prefix
                display_name = re.sub(r'^\d+-', '', name).replace('-', ' ').title()
                blogs[f.stem] = display_name
        return blogs

    def _load_topic_templates(self) -> Dict:
        """Load topic templates from config."""
        templates_file = CONFIG_DIR / "topic_templates.json"
        if templates_file.exists():
            try:
                return json.loads(templates_file.read_text())
            except Exception:
                pass
        return {"templates": [], "high_value_keywords": []}

    def _load_keyword_mappings(self) -> Dict:
        """Load keyword mappings from config."""
        mappings_file = CONFIG_DIR / "keyword_mappings.json"
        if mappings_file.exists():
            try:
                return json.loads(mappings_file.read_text())
            except Exception:
                pass
        return {"statutes": {}, "outcomes": {}}

    def parse_suggestion_file(self, filepath: Path, topic_num: int = 1) -> Optional[TopicSuggestion]:
        """Parse a blog suggestions markdown file and extract a specific topic."""
        if not filepath.exists():
            print(f"Suggestion file not found: {filepath}")
            return None

        content = filepath.read_text(encoding="utf-8")

        # Find the topic section
        pattern = rf'### {topic_num}\. "([^"]+)"'
        match = re.search(pattern, content)
        if not match:
            print(f"Topic #{topic_num} not found in {filepath}")
            return None

        title = match.group(1)

        # Extract the section for this topic (until next ### or ---)
        start_pos = match.start()
        end_match = re.search(r'\n---\n|\n### \d+\.', content[start_pos + 10:])
        end_pos = start_pos + 10 + end_match.start() if end_match else len(content)
        section = content[start_pos:end_pos]

        # Parse components
        keyword_match = re.search(r'\*\*Primary Keyword:\*\* (.+)', section)
        keyword = keyword_match.group(1).strip() if keyword_match else ""

        score_match = re.search(r'\*\*Score:\*\* (\d+)', section)
        score = int(score_match.group(1)) if score_match else 0

        freq_match = re.search(r'\*\*Mentions:\*\* (\d+)', section)
        frequency = int(freq_match.group(1)) if freq_match else 0

        outcomes_match = re.search(r'\*\*Outcomes Found:\*\* (.+)', section)
        outcomes = [o.strip() for o in outcomes_match.group(1).split(',')] if outcomes_match else []

        statutes_match = re.search(r'\*\*Related Statutes:\*\* (.+)', section)
        statutes = []
        if statutes_match:
            stat_str = statutes_match.group(1)
            statutes = re.findall(r'F\.S\. ([\d.]+)', stat_str)

        # Parse suggested angles
        angles = []
        angles_section = re.search(r'\*\*Suggested Angles:\*\*\n((?:- .+\n?)+)', section)
        if angles_section:
            angles = [line.strip('- ').strip() for line in angles_section.group(1).split('\n') if line.strip().startswith('-')]

        # Determine source type
        if "USER SUBMITTED" in section:
            source_type = "user_idea"
        elif "dismissed" in title.lower():
            source_type = "case_result"
        elif "statute" in title.lower() or any(s in title for s in STATUTE_INFO.keys()):
            source_type = "legal_guide"
        elif any(o in title.lower() for o in ["reduced", "not guilty", "dismissed"]):
            source_type = "outcome_focused"
        else:
            source_type = "explainer"

        return TopicSuggestion(
            title=title,
            source_type=source_type,
            keyword=keyword,
            score=score,
            frequency=frequency,
            outcomes=outcomes,
            statutes=statutes,
            suggested_angles=angles,
            calendar_events=[],
            case_files=[],
            gmail_threads=[],
            drive_files=[]
        )

    def parse_topic_string(self, topic_title: str) -> TopicSuggestion:
        """Create a TopicSuggestion from a plain topic title string."""
        # Extract keyword from title
        keyword = ""
        for kw in KEYWORD_TO_PRACTICE_AREA.keys():
            if kw.lower() in topic_title.lower():
                keyword = kw.upper() if len(kw) <= 4 else kw.title()
                break

        # Detect source type
        source_type = "explainer"
        if "dismissed" in topic_title.lower() or "case result" in topic_title.lower():
            source_type = "case_result"
        elif "statute" in topic_title.lower() or "f.s." in topic_title.lower():
            source_type = "legal_guide"
        elif any(o in topic_title.lower() for o in ["reduced", "not guilty"]):
            source_type = "outcome_focused"

        # Extract outcomes from title
        outcomes = []
        for outcome in ["dismissed", "reduced", "not guilty", "acquitted"]:
            if outcome in topic_title.lower():
                outcomes.append(outcome)

        # Extract statute from title
        statutes = re.findall(r'(\d{3}\.\d{2,4})', topic_title)

        return TopicSuggestion(
            title=topic_title,
            source_type=source_type,
            keyword=keyword,
            score=0,
            frequency=0,
            outcomes=outcomes,
            statutes=statutes,
            suggested_angles=[],
            calendar_events=[],
            case_files=[],
            gmail_threads=[],
            drive_files=[]
        )

    def generate_outline(self, topic: TopicSuggestion) -> BlogOutline:
        """Generate a blog post outline from a topic suggestion."""

        # Get the template for this content type
        template = CONTENT_TEMPLATES.get(topic.source_type, CONTENT_TEMPLATES["explainer"])

        # Generate title options
        primary_title = topic.title
        alternate_titles = self._generate_alternate_titles(topic)

        # Generate URL slug
        url_slug = self._generate_slug(primary_title)

        # Generate meta description
        meta_description = self._generate_meta_description(topic)

        # Generate target keywords
        target_keywords = self._generate_keywords(topic)

        # Generate intro hook
        intro_hook = self._generate_intro(topic, template)

        # Generate H2 sections
        h2_sections = self._generate_sections(topic, template)

        # Generate case context (anonymized)
        case_context = self._generate_case_context(topic)

        # Generate CTAs
        cta_primary = self._generate_primary_cta(topic)
        cta_secondary = self._generate_secondary_cta(topic)

        # Find related content
        related_blogs = self._find_related_blogs(topic)
        related_practice_areas = self._find_related_practice_areas(topic)

        return BlogOutline(
            primary_title=primary_title,
            alternate_titles=alternate_titles,
            meta_description=meta_description,
            target_keywords=target_keywords,
            url_slug=url_slug,
            intro_hook=intro_hook,
            h2_sections=h2_sections,
            case_context=case_context,
            cta_primary=cta_primary,
            cta_secondary=cta_secondary,
            related_blog_posts=related_blogs,
            related_practice_areas=related_practice_areas
        )

    def _generate_alternate_titles(self, topic: TopicSuggestion) -> List[str]:
        """Generate 2-3 alternate title options."""
        alts = []
        keyword = topic.keyword or "Criminal"

        if topic.source_type == "case_result":
            alts.append(f"How We Got a {keyword} Case Dismissed in Orlando")
            alts.append(f"Real {keyword} Defense: What Actually Works")
            if topic.outcomes:
                alts.append(f"{topic.outcomes[0].title()} Verdict: Lessons from a {keyword} Case")
        elif topic.source_type == "legal_guide" and topic.statutes:
            statute = topic.statutes[0]
            info = STATUTE_INFO.get(statute, {})
            alts.append(f"Florida Statute {statute} Explained: Your Defense Options")
            alts.append(f"{info.get('short', keyword)} Charges in Florida: The Complete Guide")
        else:
            alts.append(f"Orlando {keyword} Attorney Explains Your Options")
            alts.append(f"Facing {keyword} Charges? Here's What You Need to Know")
            alts.append(f"The Truth About {keyword} Cases in Florida")

        return alts[:3]

    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title."""
        # Remove special characters, lowercase, replace spaces with hyphens
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')[:60]  # Limit length

    def _generate_meta_description(self, topic: TopicSuggestion) -> str:
        """Generate SEO meta description (130-160 chars)."""
        keyword = topic.keyword or "criminal"

        if topic.source_type == "case_result":
            desc = f"See how we achieved a {topic.outcomes[0] if topic.outcomes else 'successful'} outcome in a {keyword} case. Free consultation with Orlando criminal defense attorney."
        elif topic.outcomes:
            desc = f"Learn how {keyword} charges get {topic.outcomes[0]} in Florida. As a former law enforcement officer, I know both sides. Free consultation: 407-500-7000."
        else:
            desc = f"Facing {keyword} charges in Orlando? Former law enforcement officer explains your rights and defense options. Free consultation available."

        # Trim to 160 chars
        if len(desc) > 160:
            desc = desc[:157] + "..."
        return desc

    def _generate_keywords(self, topic: TopicSuggestion) -> List[str]:
        """Generate target SEO keywords."""
        keywords = []
        keyword = topic.keyword or ""

        # Primary keyword variations
        if keyword:
            keywords.extend([
                f"{keyword} attorney Orlando",
                f"{keyword} lawyer Florida",
                f"{keyword} defense Orlando",
            ])

        # Add statute-based keywords
        for statute in topic.statutes:
            info = STATUTE_INFO.get(statute, {})
            if info:
                keywords.append(f"Florida Statute {statute}")
                keywords.append(f"{info.get('short', '')} Florida")

        # Add outcome-based keywords
        for outcome in topic.outcomes:
            keywords.append(f"{keyword} case {outcome}")
            keywords.append(f"get {keyword} {outcome} Florida")

        # Add location keywords
        keywords.extend([
            "Orlando criminal defense",
            "Orange County defense attorney",
        ])

        return keywords[:10]

    def _generate_intro(self, topic: TopicSuggestion, template: Dict) -> str:
        """Generate introduction paragraph hook."""
        keyword = topic.keyword or "criminal"
        outcome = topic.outcomes[0] if topic.outcomes else "resolved"
        statute = topic.statutes[0] if topic.statutes else ""

        intro = template["intro_pattern"].format(
            charge=keyword,
            outcome=outcome,
            statute=statute
        )

        # Add urgency if appropriate
        if topic.source_type in ["case_result", "outcome_focused"]:
            intro += f"\n\nIn this article, I'll share how we achieved a {outcome} outcome and what it means for your case."
        else:
            intro += "\n\nIn this article, I'll explain what you're up against and what steps you can take to protect your future."

        return intro

    def _generate_sections(self, topic: TopicSuggestion, template: Dict) -> List[Dict]:
        """Generate H2 section structure with key points."""
        sections = []
        keyword = topic.keyword or "criminal"
        outcome = topic.outcomes[0] if topic.outcomes else "favorable"
        statute = topic.statutes[0] if topic.statutes else "the relevant statute"

        for section_template in template["h2_structure"]:
            heading = section_template["heading"].format(
                charge=keyword,
                outcome=outcome,
                statute=statute
            )

            focus = section_template["focus"]
            key_points = self._get_key_points_for_focus(focus, topic)
            subsections = self._get_subsections_for_focus(focus, topic)

            sections.append({
                "heading": heading,
                "focus": focus,
                "key_points": key_points,
                "subsections": subsections
            })

        return sections

    def _get_key_points_for_focus(self, focus: str, topic: TopicSuggestion) -> List[str]:
        """Get key bullet points for a section focus area."""
        keyword = topic.keyword or "criminal"

        focus_points = {
            "legal_definition": [
                f"What legally constitutes {keyword} under Florida law",
                "Elements the State must prove beyond reasonable doubt",
                "Common misconceptions about the charge",
            ],
            "penalties": [
                "Fines and potential jail/prison time",
                "License suspension or revocation",
                "Probation requirements",
                "Long-term consequences (background checks, employment)",
            ],
            "process": [
                "What happens at arrest",
                "The arraignment process",
                "Discovery and evidence review",
                "Plea negotiations vs. trial",
            ],
            "defenses": [
                "Constitutional violations (illegal stop, search, seizure)",
                "Challenging the State's evidence",
                "Witness credibility issues",
                "Procedural errors by law enforcement",
            ],
            "action_steps": [
                "Exercise your right to remain silent",
                "Contact a defense attorney immediately",
                "Document everything you remember",
                "Don't discuss your case on social media",
            ],
            "case_background": [
                "The circumstances leading to the charge (anonymized)",
                "Initial challenges the case presented",
                "What the State's evidence showed",
            ],
            "strategy": [
                "How we analyzed the evidence",
                "The defense approach we developed",
                "Key motions or arguments",
            ],
            "result": [
                "The outcome achieved",
                "Impact on the client's record",
                "Timeline from charge to resolution",
            ],
            "lessons": [
                "What made this defense successful",
                "How similar cases might be handled",
                "The importance of early legal representation",
            ],
            "statute_breakdown": [
                "Plain-English explanation of the statute",
                "What prosecutors must establish",
                "Common fact patterns that trigger charges",
            ],
            "elements": [
                "Element 1 the State must prove",
                "Element 2 the State must prove",
                "How weakness in any element can help your defense",
            ],
            "examples": [
                "Scenario where charge applies",
                "Scenario where charge may not apply",
                "Gray areas in the law",
            ],
            "importance": [
                "Why self-representation is risky",
                "How an attorney can help at each stage",
                "Potential outcomes with vs. without counsel",
            ],
            "how_it_works": [
                f"How {topic.outcomes[0] if topic.outcomes else 'favorable outcomes'} happens procedurally",
                "What factors judges/prosecutors consider",
                "The defense work that makes it possible",
            ],
            "factors": [
                "Evidence weaknesses we identified",
                "Procedural issues we raised",
                "Client factors that helped the case",
            ],
            "implications": [
                "What this outcome means for your record",
                "Eligibility for expungement/sealing",
                "Moving forward after resolution",
            ],
            "cta": [
                "Free consultation available",
                "Former law enforcement perspective",
                "Aggressive defense for your case",
            ],
        }

        return focus_points.get(focus, [
            "Key point 1 for this section",
            "Key point 2 for this section",
            "Key point 3 for this section",
        ])

    def _get_subsections_for_focus(self, focus: str, topic: TopicSuggestion) -> List[str]:
        """Get H3 subsection headings for a focus area."""
        keyword = topic.keyword or "Criminal"

        # Only some focuses need subsections
        subsection_map = {
            "penalties": [
                "Misdemeanor vs. Felony Penalties",
                "Enhanced Penalties",
                "Collateral Consequences",
            ],
            "defenses": [
                "Constitutional Defenses",
                "Factual Defenses",
                f"Defenses Specific to {keyword} Cases",
            ],
            "statute_breakdown": [
                "The Exact Language of the Law",
                "How Courts Have Interpreted It",
                "Recent Changes or Updates",
            ],
        }

        return subsection_map.get(focus, [])

    def _generate_case_context(self, topic: TopicSuggestion) -> str:
        """Generate anonymized case context for the post."""
        keyword = topic.keyword or "criminal"

        if topic.source_type == "case_result":
            outcome = topic.outcomes[0] if topic.outcomes else "favorable"
            return f"""
**Case Context (Anonymized):**
- Charge Type: {keyword}
- Jurisdiction: Orange County, Florida
- Outcome: {outcome.title()}
- Key Factor: [Describe the defense strategy that worked]

*Note: All identifying details have been removed to protect client confidentiality.
This example is for educational purposes only and does not guarantee similar results.*
"""
        elif topic.frequency > 5:
            return f"""
**Why This Topic Matters Now:**
Based on recent case activity, {keyword} charges are trending in our practice area.
We've handled multiple cases involving these charges in the past 30 days.
"""
        else:
            return ""

    def _generate_primary_cta(self, topic: TopicSuggestion) -> str:
        """Generate primary call-to-action."""
        keyword = topic.keyword or "criminal"

        return f"""
## Need Help With {keyword} Charges?

Don't face {keyword} charges alone. As a former law enforcement officer,
I understand how these cases are investigated and prosecuted - and I use that
knowledge to build stronger defenses.

**Free Consultation | Aggressive Defense | Results-Focused**

**Call Now: 407-500-7000**

Law Office of Jeff Lotter PLLC
Serving Orlando, Orange County, and Central Florida
"""

    def _generate_secondary_cta(self, topic: TopicSuggestion) -> str:
        """Generate secondary/inline CTA for mid-article use."""
        return """
> **Need immediate help?** Call 407-500-7000 for a free consultation.
> We're available 24/7 for urgent criminal matters.
"""

    def _find_related_blogs(self, topic: TopicSuggestion) -> List[str]:
        """Find existing blog posts related to this topic."""
        related = []
        keyword_lower = (topic.keyword or "").lower()

        for slug, title in self.existing_blogs.items():
            title_lower = title.lower()

            # Check for keyword match
            if keyword_lower and keyword_lower in title_lower:
                related.append(f"blog/{slug}.html - {title}")
                continue

            # Check for outcome match
            for outcome in topic.outcomes:
                if outcome.lower() in title_lower:
                    related.append(f"blog/{slug}.html - {title}")
                    break

            # Check for statute match
            for statute in topic.statutes:
                if statute in title_lower:
                    related.append(f"blog/{slug}.html - {title}")
                    break

        return related[:5]  # Limit to 5 related posts

    def _find_related_practice_areas(self, topic: TopicSuggestion) -> List[str]:
        """Find related practice area pages."""
        related = []
        keyword_lower = (topic.keyword or "").lower()

        for kw, page in KEYWORD_TO_PRACTICE_AREA.items():
            if kw in keyword_lower or keyword_lower in kw:
                if page not in related:
                    related.append(f"practice-areas/{page}")

        # Always include criminal-traffic as fallback
        if not related:
            related.append("practice-areas/criminal-traffic.html")

        return related[:3]

    def render_outline_to_markdown(self, outline: BlogOutline) -> str:
        """Render the outline as formatted markdown."""
        lines = [
            f"# Blog Post Draft: {outline.primary_title}",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "---",
            "",
            "## Title Options",
            "",
            f"**Primary:** {outline.primary_title}",
            "",
            "**Alternates:**",
        ]

        for alt in outline.alternate_titles:
            lines.append(f"- {alt}")

        lines.extend([
            "",
            "---",
            "",
            "## SEO Elements",
            "",
            f"**Meta Description:** {outline.meta_description}",
            "",
            f"**URL Slug:** `{outline.url_slug}`",
            "",
            "**Target Keywords:**",
        ])

        for kw in outline.target_keywords:
            lines.append(f"- {kw}")

        lines.extend([
            "",
            "---",
            "",
            "## Content Outline",
            "",
            "### Introduction",
            "",
            outline.intro_hook,
            "",
            outline.cta_secondary,
            "",
        ])

        # Add H2 sections
        for section in outline.h2_sections:
            lines.append(f"### {section['heading']}")
            lines.append("")
            lines.append(f"*Focus: {section['focus']}*")
            lines.append("")
            lines.append("**Key Points:**")
            for point in section['key_points']:
                lines.append(f"- {point}")

            if section.get('subsections'):
                lines.append("")
                lines.append("**Subsections (H3):**")
                for sub in section['subsections']:
                    lines.append(f"- {sub}")

            lines.append("")

        # Add case context if present
        if outline.case_context:
            lines.extend([
                "---",
                "",
                outline.case_context,
            ])

        # Add CTA
        lines.extend([
            "---",
            "",
            outline.cta_primary,
            "",
        ])

        # Add related content
        lines.extend([
            "---",
            "",
            "## Internal Links",
            "",
            "**Related Blog Posts:**",
        ])

        if outline.related_blog_posts:
            for post in outline.related_blog_posts:
                lines.append(f"- [{post}](/{post})")
        else:
            lines.append("- [Search existing posts for related topics]")

        lines.extend([
            "",
            "**Related Practice Areas:**",
        ])

        for area in outline.related_practice_areas:
            lines.append(f"- [{area}](/{area})")

        lines.extend([
            "",
            "---",
            "",
            "## HTML Template Requirements",
            "",
            "When converting to HTML, include:",
            "- [ ] Google Tag Manager (GTM-52LMX48G)",
            "- [ ] GA4 analytics",
            "- [ ] Microsoft Clarity",
            "- [ ] Article schema markup",
            "- [ ] BreadcrumbList schema",
            "- [ ] Open Graph tags",
            "- [ ] Twitter Card tags",
            "- [ ] Canonical URL",
            "- [ ] Mobile CTA bar",
            "- [ ] Breadcrumb navigation",
            "",
            "---",
            "",
            "*Generated by blog_draft_generator.py*",
        ])

        return "\n".join(lines)

    def save_draft(self, outline: BlogOutline) -> Path:
        """Save the draft to a file."""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"blog_draft_{today}_{outline.url_slug[:40]}.md"
        filepath = self.output_dir / filename

        content = self.render_outline_to_markdown(outline)
        filepath.write_text(content, encoding="utf-8")

        return filepath

    def run_interactive(self):
        """Interactive mode to select and generate drafts."""
        print("=" * 60)
        print("Blog Post Draft Generator - Interactive Mode")
        print("=" * 60)
        print()

        # Find most recent suggestions file
        suggestion_files = sorted(SUGGESTIONS_DIR.glob("blog_suggestions_*.md"), reverse=True)

        if not suggestion_files:
            print("No suggestion files found. Run blog_topic_generator.py first.")
            return

        latest_file = suggestion_files[0]
        print(f"Using suggestions from: {latest_file.name}")
        print()

        # Display available topics
        content = latest_file.read_text(encoding="utf-8")
        topics = re.findall(r'### (\d+)\. "([^"]+)"', content)

        print("Available Topics:")
        print("-" * 40)
        for num, title in topics:
            print(f"  {num}. {title}")
        print()

        # Get user selection
        try:
            selection = input("Enter topic number (or 'q' to quit): ").strip()
            if selection.lower() == 'q':
                return

            topic_num = int(selection)

            # Parse and generate
            topic = self.parse_suggestion_file(latest_file, topic_num)
            if topic:
                print()
                print(f"Generating outline for: {topic.title}")
                print()

                outline = self.generate_outline(topic)
                filepath = self.save_draft(outline)

                print(f"Draft saved to: {filepath}")
                print()
                print("Preview of outline:")
                print("-" * 40)
                print(self.render_outline_to_markdown(outline)[:1500] + "...")

        except ValueError:
            print("Invalid selection. Please enter a number.")
        except KeyboardInterrupt:
            print("\nCancelled.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate blog post draft outlines from topic suggestions"
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--topic",
        type=str,
        help="Topic title to generate outline for (plain text)"
    )
    group.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Run in interactive mode"
    )

    parser.add_argument(
        "--suggestion-file",
        type=str,
        help="Path to blog suggestions markdown file"
    )
    parser.add_argument(
        "--topic-num",
        type=int,
        default=1,
        help="Topic number from suggestion file (default: 1)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory for drafts"
    )

    args = parser.parse_args()

    generator = BlogDraftGenerator()

    if args.output_dir:
        generator.output_dir = Path(args.output_dir)
        generator.output_dir.mkdir(parents=True, exist_ok=True)

    if args.interactive:
        generator.run_interactive()
    elif args.topic:
        # Generate from plain topic string
        topic = generator.parse_topic_string(args.topic)
        outline = generator.generate_outline(topic)
        filepath = generator.save_draft(outline)
        print(f"Draft saved to: {filepath}")
    elif args.suggestion_file:
        # Generate from suggestion file
        topic = generator.parse_suggestion_file(
            Path(args.suggestion_file),
            args.topic_num
        )
        if topic:
            outline = generator.generate_outline(topic)
            filepath = generator.save_draft(outline)
            print(f"Draft saved to: {filepath}")
    else:
        # Default: use most recent suggestion file, topic #1
        suggestion_files = sorted(SUGGESTIONS_DIR.glob("blog_suggestions_*.md"), reverse=True)
        if suggestion_files:
            topic = generator.parse_suggestion_file(suggestion_files[0], 1)
            if topic:
                outline = generator.generate_outline(topic)
                filepath = generator.save_draft(outline)
                print(f"Draft saved to: {filepath}")
        else:
            print("No suggestion files found. Run blog_topic_generator.py first,")
            print("or use --topic 'Your Topic Title' to generate directly.")


if __name__ == "__main__":
    main()
