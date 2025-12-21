# Pillar Page Hero Image Specifications

**Project:** LotterLaw Website
**Purpose:** Hero images for 3 pillar guide pages
**Created:** December 21, 2025

---

## General Requirements (All 3 Images)

| Attribute | Specification |
|-----------|---------------|
| **Dimensions** | 1600 x 600 pixels (wide hero format, 2.67:1 ratio) |
| **Format** | WebP preferred, JPG fallback |
| **File Size** | Under 200KB (optimize for web) |
| **Style** | Professional, serious, not stock-photo-cheesy |
| **Tone** | Authoritative but approachable |
| **Text Overlay** | None (text added via HTML) |
| **Composition** | Subject slightly off-center (rule of thirds) |
| **Color Treatment** | Muted/dark tones work well with blue (#1E3A8A) text overlay |

---

## Image 1: DUI Defense Pillar

**Filename:** `pillar-dui-hero.webp`
**Page:** `blog/dui-defense-guide.html`

### Visual Concept
A moody, atmospheric shot suggesting a DUI stop scenario without showing faces or identifying features.

### Subject Options (choose one)
1. **Breathalyzer device** - Close-up of Intoxilyzer or similar device, dramatic lighting
2. **Police lights at night** - Blurred red/blue lights reflected on wet road surface
3. **Steering wheel perspective** - Driver's POV with rearview mirror showing lights behind
4. **Field sobriety scene** - Officer's flashlight beam, abstract/blurred

### Mood & Tone
- **Dark/moody** - Nighttime or low-light setting
- **Tension** - Conveys the stress of a DUI stop
- **Professional** - Not sensationalized or scary

### Color Palette
| Color | Use |
|-------|-----|
| Deep blue/navy | Primary background tones |
| Red/blue accent | Police lights (subtle) |
| Warm amber | Streetlight highlights |
| Black | Shadows, depth |

### Composition
- **Left-weighted** - Subject on left third (text overlays on right)
- **Horizontal lines** - Road, horizon create stability
- **Depth of field** - Sharp foreground, blurred background

### Do NOT Include
- Recognizable faces
- Specific car models/plates
- Actual alcohol containers
- Handcuffs or arrest imagery

### Alt Text
"DUI Defense - Field Sobriety Testing in Florida"

### Existing Reference Images
- `assets/hgn-eye-test.jpg` - Eye test close-up (current style)
- `assets/refuse-field-sobriety.webp` - Field test scene

---

## Image 2: Domestic Violence Defense Pillar

**Filename:** `pillar-dv-hero.webp`
**Page:** `blog/domestic-violence-defense-guide.html`

### Visual Concept
Legal defense imagery emphasizing protection, justice, and rights - NOT depicting violence or conflict.

### Subject Options (choose one)
1. **Scales of justice** - Dramatic lighting, close-up detail
2. **Gavel and legal documents** - Courtroom setting, authoritative
3. **Courthouse architecture** - Columns, steps, classical elements
4. **Attorney consultation** - Two figures (blurred/silhouette) across table

### Mood & Tone
- **Serious but hopeful** - Conveys gravity without despair
- **Protective** - Emphasis on defense and rights
- **Professional** - Courtroom/legal setting

### Color Palette
| Color | Use |
|-------|-----|
| Deep purple/burgundy | Authority, seriousness |
| Gold/bronze | Justice, scales, trim |
| Warm wood tones | Courtroom furniture |
| Soft cream/white | Legal documents, highlights |

### Composition
- **Centered or right-weighted** - Allows text on left
- **Strong vertical elements** - Columns, gavel standing upright
- **Shallow depth** - Focus on key symbol

### Do NOT Include
- People in distress or conflict
- Bruises, injuries, or violence
- Police/arrest imagery
- Broken objects or destruction

### Alt Text
"Domestic Violence Defense - Protecting Your Rights in Florida"

### Visual Message
"We defend the accused with dignity and professionalism"

---

## Image 3: Theft Defense Pillar

**Filename:** `pillar-theft-hero.webp`
**Page:** `blog/theft-defense-guide.html`

### Visual Concept
Retail/legal setting that suggests the context without being accusatory toward the viewer.

### Subject Options (choose one)
1. **Legal documents with gavel** - Defense focus, not accusation
2. **Retail store aisle** - Abstract, no people, security camera angle
3. **Security office monitors** - Multiple screens, professional setting
4. **Fingerprint on document** - Close-up, evidence/investigation theme

### Mood & Tone
- **Neutral/professional** - Not accusatory or shameful
- **Serious** - Legal consequences are real
- **Hopeful** - Defense is possible

### Color Palette
| Color | Use |
|-------|-----|
| Green accents | Money, retail, fresh start |
| Neutral gray | Security, professional |
| White/cream | Documents, clean slate |
| Blue tones | Trust, legal, Lotter Law brand |

### Composition
- **Wide angle** - Establishes setting/context
- **Center or left-weighted** - Subject placement
- **Clean lines** - Retail shelves, document edges

### Do NOT Include
- People stealing or looking guilty
- Handcuffs or arrest scenes
- Mugshots or surveillance stills
- Specific store logos or brands

### Alt Text
"Theft Defense - Protecting Your Future in Florida"

### Existing Reference Images
- `assets/Burglary_Nolle_Pross.webp` - Case result style
- `assets/Reasonable_Doubt_Video_Theft.webp` - Legal defense angle

---

## File Delivery Checklist

For each image, please provide:

- [ ] **WebP version** (primary): `pillar-dui-hero.webp`, etc.
- [ ] **JPG fallback** (optional): `pillar-dui-hero.jpg`, etc.
- [ ] **Dimensions verified**: 1600 x 600 px
- [ ] **File size**: Under 200KB each

### Where to Save
```
C:\Users\jeff\OneDrive\Documents\LotterLaw\Website\assets\
```

---

## Implementation Notes

Once images are ready, I will:
1. Add `<picture>` elements with WebP + JPG fallback
2. Add proper `alt`, `width`, `height` attributes
3. Insert hero sections into pillar pages
4. Update sitemap with new lastmod dates

---

## Quick Reference Table

| Image | Filename | Subject | Mood | Primary Colors |
|-------|----------|---------|------|----------------|
| DUI | `pillar-dui-hero.webp` | Breathalyzer/police lights | Dark, tense | Navy, red/blue, amber |
| DV | `pillar-dv-hero.webp` | Scales/gavel/courthouse | Serious, protective | Purple, gold, wood |
| Theft | `pillar-theft-hero.webp` | Legal docs/retail/security | Neutral, professional | Green, gray, blue |

---

*Specs created for Jeff Lotter - December 2025*
