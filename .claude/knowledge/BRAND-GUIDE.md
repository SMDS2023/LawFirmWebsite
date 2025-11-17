# Lotter Law - Brand & Style Guide

**Last Updated:** 2025-11-16
**Purpose:** Ensure consistent branding, voice, and formatting across all website content

---

## 1. BRAND IDENTITY

### 1.1 Firm Overview
- **Firm Name:** Lotter Law
- **Practice Focus:** Criminal Defense & DUI Attorney
- **Location:** Orlando, Florida
- **Key Differentiator:** Former State Trooper & Former Deputy Sheriff
- **Tagline:** "Protecting Your Rights & Future"

### 1.2 Brand Positioning
**We are:** Experienced, knowledgeable, aggressive defenders with insider law enforcement expertise
**We are not:** Corporate, impersonal, or inexperienced

**Brand Attributes:**
1. **Authoritative** - Law enforcement background commands respect
2. **Accessible** - Free consultations, prominent contact info, clear communication
3. **Urgent** - Understanding time-sensitive nature of criminal cases
4. **Client-Focused** - Protecting rights and futures, not just winning cases
5. **Local** - Orlando-based with deep community knowledge

---

## 2. VISUAL IDENTITY

### 2.1 Color Palette

#### Primary Colors
```css
/* Professional Blue - Primary Brand Color */
Blue-800: #1E3A8A    /* Main brand color, headings, primary elements */
Blue-700: #1D4ED8    /* Hover states, secondary headings */
Blue-600: #2563EB    /* Buttons, links, interactive elements */
Blue-100: #DBEAFE    /* Light backgrounds, borders, hover states */
```

**Usage:**
- Blue-800: Primary branding, footer, main headings
- Blue-700: Secondary headings, hover effects on dark elements
- Blue-600: Text links, primary action buttons
- Blue-100: Card hover states, light backgrounds, borders

#### Accent Colors
```css
/* Urgent Orange/Amber - Call-to-Action */
Amber-600: #D97706    /* Primary CTA hover state */
Amber-500: #F59E0B    /* Primary CTA button background */
Amber-400: #FBBF24    /* Accent highlights */
Amber-300: #FCD34D    /* Light hover states on CTAs */
```

**Usage:**
- Amber-500: "Call Now" buttons, "Free Consultation" CTAs
- Amber-600: Hover states on CTA buttons
- Creates sense of urgency while maintaining professionalism

#### Alert Colors
```css
/* Red - Urgency and Warnings */
Red-700: #B91C1C     /* Alert box borders */
Red-600: #DC2626     /* Alert backgrounds, urgent messaging */

/* Green - Success and Benefits */
Green-500: #22C55E   /* Success states, positive outcomes */
```

**Usage:**
- Red: DUI alert box on homepage, urgent action items
- Green: Success messages, case results, benefits

#### Neutral Colors
```css
/* Grays - Text and Backgrounds */
White: #FFFFFF       /* Primary page background */
Gray-50: #F9FAFB     /* Section backgrounds, alternating */
Gray-100: #F3F4F6    /* Light hover backgrounds */
Gray-200: #E5E7EB    /* Borders, dividers */
Gray-600: #4B5563    /* Body text, navigation */
Gray-700: #374151    /* Primary text */
Gray-800: #1F2937    /* Dark text, emphasis */
```

**Usage:**
- White: Main page background
- Gray-50: Alternating section backgrounds for visual separation
- Gray-700: Standard body text for readability
- Gray-200: Subtle borders and dividers

### 2.2 Typography

#### Font Families
```css
/* Primary Body Font */
font-family: 'Inter', sans-serif;
/* Weights: 400 (regular), 500 (medium), 600 (semi-bold), 700 (bold) */

/* Display/Hero Font */
font-family: 'Tinos', serif;
/* Weights: 400 (regular), 700 (bold) */
/* Custom class: .font-hero-heading */
```

#### Font Usage Guidelines

**Inter (Body Font):**
- All body text, paragraphs, lists
- Navigation menus
- Buttons and CTAs
- Form inputs and labels
- Footer content
- Blog post content

**Tinos (Display Font):**
- Main H1 headings
- Hero section headlines
- Page titles
- Use `.font-hero-heading` utility class

#### Typography Scale
```css
/* Headings */
H1: text-4xl (36px) to text-5xl (48px) on desktop - Tinos Bold
H2: text-3xl (30px) to text-4xl (36px) - Inter Bold
H3: text-2xl (24px) to text-3xl (30px) - Inter Semi-Bold
H4: text-xl (20px) to text-2xl (24px) - Inter Semi-Bold
H5: text-lg (18px) - Inter Semi-Bold
H6: text-base (16px) - Inter Semi-Bold

/* Body Text */
Body: text-base (16px) to text-lg (18px) - Inter Regular
Small: text-sm (14px) - Inter Regular
```

#### Line Height & Spacing
```css
Headings: leading-tight (1.25) to leading-snug (1.375)
Body: leading-relaxed (1.625) to leading-loose (2)
Paragraph Spacing: mb-4 (1rem) to mb-6 (1.5rem)
```

### 2.3 Logo Usage

**Primary Logo:** `Lotter-Law-logo-02.jpg`
**Fixed Height:** 65px (maintains aspect ratio)
**Background:** Works on white and dark backgrounds
**Minimum Clear Space:** 10px on all sides
**Do Not:** Stretch, distort, recolor, or add effects

**Logo Placement:**
- Header: Top left, 65px height
- Footer: Centered, same 65px height
- Favicons: Generate from logo if needed

### 2.4 Imagery Guidelines

#### Photography Style
- **Professional:** Attorney headshots in business attire
- **Authentic:** Real credentials and certificates
- **Local:** Orlando-specific imagery when possible
- **Trustworthy:** Law enforcement background photos

#### Image Categories
1. **Attorney Photos:** Professional headshots, consistent lighting
2. **Credentials:** Certificates, badges, academy photos
3. **Team Members:** Consistent 400x400px circular crops
4. **Hero Images:** Full-width, professional office/legal themes
5. **Blog Graphics:** Relevant illustrations, charts, diagrams

#### Image Specifications
```
Hero Images: 1920x1080px minimum, WebP + JPG fallback
Team Photos: 400x400px, circular crop, WebP format
Blog Images: 800x600px minimum, relevant to content
File Size: <200KB for hero, <50KB for team photos
Alt Text: Required on all images for accessibility
```

---

## 3. VOICE & TONE

### 3.1 Brand Voice Characteristics

#### Professional but Approachable
**DO:**
- Use clear, straightforward language
- Explain legal concepts in plain English
- Show empathy for client situations
- Maintain professional credibility

**DON'T:**
- Use excessive legalese or jargon
- Sound robotic or corporate
- Be overly casual or flippant
- Make promises that can't be kept

#### Authoritative but Not Arrogant
**DO:**
- Demonstrate expertise through law enforcement background
- Share relevant experience and credentials
- Provide educational content
- Reference case results appropriately

**DON'T:**
- Boast or exaggerate capabilities
- Guarantee outcomes
- Belittle other attorneys
- Overuse superlatives

#### Urgent but Not Fear-Mongering
**DO:**
- Emphasize importance of timely action
- Explain consequences of inaction
- Offer immediate consultations
- Acknowledge stress of legal situations

**DON'T:**
- Create unnecessary panic
- Use scare tactics
- Exaggerate potential penalties
- Pressure or manipulate

### 3.2 Writing Style Guidelines

#### Active Voice Over Passive
**Preferred:** "We fight for your rights"
**Avoid:** "Your rights will be fought for"

#### Second Person (You/Your)
**Preferred:** "Your future is too important to leave to chance"
**Avoid:** "A person's future is too important"

#### Concise and Scannable
- Short paragraphs (3-4 sentences)
- Bullet points for lists
- Clear subheadings every 200-300 words
- Highlight key information

#### Specific Over General
**Preferred:** "Former Florida Highway Patrol Trooper with 10 years experience"
**Avoid:** "Experienced attorney with law enforcement background"

### 3.3 Content Templates

#### Practice Area Page Opening
```
[Heading] Orlando [Practice Area] Attorney

If you're facing [charge type] in Orlando, you need an attorney who understands
both sides of the courtroom. As a former [law enforcement role], I've seen how
these cases are built—and how to defend against them.

At Lotter Law, we provide aggressive defense for [specific charges]. With [X]
years of experience and insider knowledge of Florida law enforcement procedures,
we're prepared to fight for your rights and your future.

Call 407-500-7000 for a free consultation today.
```

#### Blog Post Opening
```
[Compelling Question or Statement]

If you're [facing situation], understanding [legal concept] could make a
significant difference in your case outcome. As a former [law enforcement role]
turned defense attorney, I've seen both sides of [legal issue].

In this article, I'll explain [what you'll cover] and what you need to know to
protect your rights.
```

#### Call-to-Action
```
Standard CTA:
"Don't face [charge type] alone. Call 407-500-7000 for a free consultation with
an Orlando criminal defense attorney who knows how law enforcement builds cases—
and how to defend against them."

Urgent CTA (DUI):
"Time is critical in DUI cases. Call 407-500-7000 NOW for immediate help. Free
consultation available 24/7."
```

### 3.4 Word Choice Guidelines

#### Preferred Terms
- **Client** (not "defendant" or "accused")
- **Fight for** (conveys advocacy)
- **Protect your rights** (client-focused)
- **Free consultation** (removes barrier)
- **Former law enforcement** (credibility)
- **Aggressive defense** (active representation)
- **Orlando** (local focus)

#### Avoid
- **Cheap** (use "affordable" or "free consultation")
- **Guaranteed** (can't promise outcomes)
- **Best** (subjective, unverifiable)
- **Always/Never** (absolute statements)
- **Victim** (unless referring to alleged victim in case)

---

## 4. FORMATTING STANDARDS

### 4.1 HTML Structure

#### Required Page Elements
Every page must include:
1. **DOCTYPE and Meta Tags**
   - `<!DOCTYPE html>`
   - `<meta charset="UTF-8">`
   - `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
   - `<meta name="description" content="[Page-specific description]">`

2. **Title Tag Format**
   - Homepage: `"Orlando Criminal Defense & DUI Attorney | Lotter Law"`
   - Practice Areas: `"[Practice Area] Attorney Orlando | Lotter Law"`
   - Blog: `"[Blog Title] | Lotter Law Blog"`

3. **Header Navigation**
   - Logo (links to homepage)
   - Main navigation menu
   - Phone number (407-500-7000)
   - "Free Consultation" CTA button

4. **Footer**
   - Logo
   - Quick links
   - Contact information
   - Privacy policy & terms links
   - Copyright notice

5. **Analytics**
   - Google Tag Manager (GTM-PLX85K8L)

#### Heading Hierarchy
```html
<h1>Single H1 per page - Main topic</h1>
<h2>Major sections</h2>
<h3>Subsections</h3>
<h4>Minor subsections</h4>
<h5>Rarely used</h5>
<h6>Rarely used</h6>
```

**Rules:**
- One H1 per page only
- Don't skip levels (H2 → H4)
- Use semantic HTML5 tags (`<article>`, `<section>`, `<nav>`)

### 4.2 Tailwind CSS Conventions

#### Responsive Breakpoints
```css
/* Mobile First Approach */
Default: Mobile (< 640px)
sm: 640px and up
md: 768px and up
lg: 1024px and up
xl: 1280px and up
2xl: 1536px and up
```

#### Common Utility Patterns
```html
<!-- Containers -->
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

<!-- Sections -->
<section class="py-12 md:py-16 lg:py-20 bg-gray-50">

<!-- Cards -->
<div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6">

<!-- Buttons -->
<a href="#" class="inline-block bg-amber-500 hover:bg-amber-600 text-white font-semibold px-6 py-3 rounded-lg transition-colors">

<!-- Text -->
<p class="text-base md:text-lg text-gray-700 leading-relaxed mb-4">
```

#### Custom Classes (styles.css)
```css
.font-hero-heading         /* Tinos font for H1 elements */
.section-fade-in           /* Fade-in animation for sections */
.practice-area-grid-item   /* Hover effects for practice area cards */
.testimonial-slider        /* Testimonial carousel styling */
.scrolling-banner          /* Bottom scrolling text banner */
.floating-cta              /* Floating call button above banner */
```

### 4.3 Component Standards

#### Navigation Menu
- Sticky header on scroll
- Mobile hamburger menu (Alpine.js)
- Active page highlighting
- Dropdown for practice areas (if needed)

#### Hero Sections
```html
<section class="relative bg-blue-800 text-white">
  <div class="absolute inset-0 bg-gradient-to-r from-blue-800 to-transparent opacity-90"></div>
  <img src="hero.webp" alt="..." class="w-full h-[500px] object-cover">
  <div class="relative z-10 max-w-7xl mx-auto px-4 py-20">
    <h1 class="font-hero-heading text-4xl md:text-5xl font-bold mb-4">
      [Headline]
    </h1>
    <p class="text-xl md:text-2xl mb-8">[Subheadline]</p>
    <a href="tel:4075007000" class="bg-amber-500 hover:bg-amber-600...">
      Call Now: 407-500-7000
    </a>
  </div>
</section>
```

#### Practice Area Cards
```html
<div class="practice-area-grid-item bg-white rounded-lg shadow-md hover:shadow-lg hover:bg-blue-100 transition-all p-6">
  <h3 class="text-2xl font-semibold text-blue-800 mb-3">[Practice Area]</h3>
  <p class="text-gray-700 mb-4">[Brief description]</p>
  <a href="/practice-areas/[slug].html" class="text-blue-600 hover:text-blue-800 font-medium">
    Learn More →
  </a>
</div>
```

#### Testimonial Format
```html
<div class="bg-white rounded-lg shadow-md p-6">
  <div class="flex items-center mb-4">
    <div class="text-amber-500 text-xl">★★★★★</div>
  </div>
  <p class="text-gray-700 italic mb-4">"[Testimonial text]"</p>
  <p class="text-gray-600 font-medium">— [Client Name], [City]</p>
</div>
```

#### Blog Post Structure
```html
<article class="prose lg:prose-lg max-w-4xl mx-auto">
  <header>
    <h1>[Blog Title]</h1>
    <p class="text-gray-600">Published: [Date] | By Jeff Lotter</p>
  </header>

  <img src="[blog-image].webp" alt="[Description]" class="w-full rounded-lg mb-8">

  <div class="content">
    [Blog content with H2, H3 sections]
  </div>

  <footer class="border-t pt-8 mt-8">
    <div class="bg-blue-100 rounded-lg p-6">
      <h3>Need Legal Help?</h3>
      <p>Call 407-500-7000 for a free consultation...</p>
    </div>
  </footer>
</article>
```

### 4.4 Form Standards

#### Contact Form Fields
```html
<form action="[handler]" method="POST" class="space-y-4">
  <div>
    <label for="name" class="block text-gray-700 font-medium mb-2">Full Name *</label>
    <input type="text" id="name" name="name" required
           class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
  </div>

  <div>
    <label for="phone" class="block text-gray-700 font-medium mb-2">Phone Number *</label>
    <input type="tel" id="phone" name="phone" required
           class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
  </div>

  <div>
    <label for="email" class="block text-gray-700 font-medium mb-2">Email *</label>
    <input type="email" id="email" name="email" required
           class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
  </div>

  <div>
    <label for="message" class="block text-gray-700 font-medium mb-2">How can we help? *</label>
    <textarea id="message" name="message" rows="4" required
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"></textarea>
  </div>

  <button type="submit"
          class="w-full bg-amber-500 hover:bg-amber-600 text-white font-semibold px-6 py-3 rounded-lg transition-colors">
    Send Message
  </button>
</form>
```

#### Form Validation
- Required fields marked with *
- Client-side validation before submission
- Clear error messages
- Success confirmation after submission

---

## 5. ACCESSIBILITY STANDARDS

### 5.1 Required Accessibility Features

#### Images
- All images must have descriptive `alt` attributes
- Decorative images use `alt=""`
- Complex images include longer descriptions

#### Links
- Descriptive link text (not "click here")
- Phone numbers use `tel:` protocol
- External links open in new tab with warning

#### Color Contrast
- Text: Minimum 4.5:1 contrast ratio
- Large text (18px+): Minimum 3:1 contrast ratio
- Interactive elements: Clear focus states

#### Keyboard Navigation
- All interactive elements accessible via keyboard
- Logical tab order
- Visible focus indicators
- Skip to main content link

#### Screen Readers
- Proper heading hierarchy
- ARIA labels where needed
- Form labels associated with inputs
- Meaningful page titles

### 5.2 Mobile Optimization

#### Touch Targets
- Minimum 44x44px for all interactive elements
- Adequate spacing between clickable items
- No hover-only functionality

#### Responsive Text
- Readable font sizes (16px minimum for body)
- Scalable text (no fixed pixel sizes)
- Proper line length (45-75 characters)

#### Mobile Navigation
- Hamburger menu for smaller screens
- Easy-to-tap phone number in header
- Sticky mobile navigation for quick access

---

## 6. SEO STANDARDS

### 6.1 Required Meta Tags
```html
<title>[Page Title] | Lotter Law</title>
<meta name="description" content="[130-160 character description with keywords]">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="canonical" href="https://lotterlaw.com/[page-url].html">
```

### 6.2 URL Structure
- **Practice Areas:** `/practice-areas/[practice-area]-attorney-orlando.html`
- **Blog Posts:** `/blog/[number]-[title-slug].html`
- **Main Pages:** `/[page-name].html`

**Rules:**
- All lowercase
- Hyphens (not underscores)
- Descriptive slugs
- Include "attorney-orlando" for practice pages

### 6.3 Content Optimization
- **Target Keyword:** In title, H1, first paragraph, URL
- **Secondary Keywords:** Throughout content naturally
- **Location Keywords:** "Orlando" in key places
- **Content Length:** 800+ words for practice areas, 600+ for blog posts
- **Internal Links:** Link to related practice areas and blog posts

### 6.4 Image SEO
```html
<img src="attorney-jeff-lotter.jpg"
     alt="Attorney Jeff Lotter, Former State Trooper and Criminal Defense Attorney in Orlando"
     width="400"
     height="400"
     loading="lazy">
```

**Rules:**
- Descriptive file names
- Alt text with keywords (naturally)
- Width and height attributes
- Lazy loading for below-fold images

---

## 7. PERFORMANCE STANDARDS

### 7.1 Image Optimization
- **Format:** WebP with JPG fallback
- **Size:** Hero images <200KB, thumbnails <50KB
- **Dimensions:** Serve appropriate sizes for viewport
- **Compression:** 80-85% quality for photos

### 7.2 Code Optimization
- **Minimize CSS:** Use Tailwind's utility classes efficiently
- **Defer JavaScript:** Use `defer` attribute on scripts
- **CDN Delivery:** Load libraries from CDN
- **Inline Critical CSS:** For above-fold content (if needed)

### 7.3 Loading Performance
- **Target Load Time:** <3 seconds on mobile
- **First Contentful Paint:** <1.8 seconds
- **Time to Interactive:** <3.8 seconds
- **Cumulative Layout Shift:** <0.1

---

## 8. BRAND CONSISTENCY CHECKLIST

Before publishing any page or content, verify:

### Visual Consistency
- [ ] Uses approved color palette (blue/amber scheme)
- [ ] Typography follows Inter/Tinos guidelines
- [ ] Logo is 65px height and unmodified
- [ ] Images are optimized (WebP + JPG)
- [ ] Spacing follows Tailwind conventions

### Content Consistency
- [ ] Voice matches brand guidelines (professional, authoritative, urgent)
- [ ] Free consultation mentioned prominently
- [ ] Phone number (407-500-7000) is visible
- [ ] Former law enforcement background referenced
- [ ] "Orlando" mentioned for local SEO

### Technical Consistency
- [ ] Google Tag Manager installed
- [ ] Meta description present (130-160 chars)
- [ ] Proper heading hierarchy (single H1)
- [ ] All images have alt text
- [ ] Mobile-responsive design verified

### Legal/Compliance
- [ ] Appropriate disclaimers included
- [ ] No guaranteed outcomes promised
- [ ] Accurate representation of credentials
- [ ] Links to privacy policy and terms

---

## 9. REVISION HISTORY

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-11-16 | 1.0 | Initial brand guide created | Claude (Knowledge Sub-Agent) |

---

## Notes

**When in doubt:**
- Prioritize clarity over cleverness
- Match existing page structure and style
- Review similar pages for consistency
- Ask: "Does this protect the brand and serve the client?"

**For questions or clarifications:**
- Reference existing pages as examples
- Check `MASTER-AUDIT.md` for current inventory
- Review `OPTIMIZATION-TRACKER.md` for ongoing improvements

This guide is a living document and should be updated as the brand evolves.
