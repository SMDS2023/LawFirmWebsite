# WRITE — Draft the Post (ends at Gate 1)

Input: a brief with a completed Source Pack. Output: `<slug>.draft.html`
uploaded to the Drive drafts folder, presented to Jeff for Gate 1.

## Slug

Kebab-case, keyword-bearing, no client-identifying words, not already under
`blog/` or claimed by a pipeline entry. Example:
`stand-your-ground-hearing-florida`.

## Format

Start from `templates/post-template.html` (the Gen-2 standard:
`bg-gray-50`, `prose lg:prose-lg`, `max-w-4xl`, GTM only — never hardcode
GA4/Clarity). Fill every `{{PLACEHOLDER}}`; leave the hero `<figure>` block
commented out (ENRICH owns images) but set the og/schema image URLs to the
post's future asset path.

## The hook (first 2 sentences — where posts live or die)

Open with the story's tension or the counterintuitive fact. Test: would a
non-lawyer read sentence three?

- Good: "The deputy never saw my client drive. By the end of the hearing,
  that was the only fact that mattered."
- Good: "The State's evidence arrived as a link — and the link had an
  expiration date."
- Banned: "If you've been charged with X in Florida...", "Being arrested can
  be a stressful experience...", any opening that could start fifty other
  posts.

## Structure (adapt, don't fill in blindly)

1. **Hook + story** — the anonymized narrative from the Source Pack.
2. **The authority deep-dive** — what the academy manual / OCSO order / case
   law actually says, with pinpoints. This is the section competitors can't
   write; give it the most space. Use a blue callout box for the "read that
   again" moment.
3. **Where the defense lives** — gray box, bulleted, concrete.
4. **Bottom line** — short, plain, ties back to the hook.
5. **CTA** — green box, contextual to the charge, phone 407-500-7000. One
   mid-post text CTA is allowed for long posts; never stack CTAs.

1,200–2,000 words. Voice: Jeff — practitioner, first person, plain,
concrete, short sentences. Match the exemplars in SKILL.md.

## Non-negotiables

- **Anonymization** per SKILL.md — run the checklist before saving: names,
  case numbers, exact dates, contact info, unique identifying fact patterns.
- **Citations**: only Source Pack authorities. `[CITE NEEDED]` markers must
  be surfaced at Gate 1, never silently dropped.
- **Legal safety**: educational framing; no outcome guarantees; case-result
  posts state results depend on facts; no advice to a specific reader
  ("call to discuss your case", not "you should refuse the test").
- **Statute formatting**: `F.S. §316.193(1)` style, consistent throughout.
- **SEO block**: title tag ≤ 60 chars with primary keyword; meta description
  ≤ 160 chars with keyword + hook; canonical
  `https://lotterlaw.com/blog/<slug>/`; og:* and twitter:* complete; Article
  schema with author Jeff Lotter, `datePublished` = intended publish date;
  primary keyword in H1 and first 100 words.
- **Internal links**: from the Source Pack (1 pillar / 3 supporting / 2
  practice-intake target — final count trued up at ENRICH).

## Save the draft (Drive, not the repo)

1. Compose the full HTML in the scratchpad.
2. Upload with `mcp__Google_Drive__create_file`: title `<slug>.draft.html`,
   `parentId` = drafts folder ID (`DATA_SOURCES.md` §8),
   `contentMimeType: text/html`, `disableConversionToGoogleType: true`,
   content via `textContent`.
3. Gate-1 edit rounds re-upload a fresh `<slug>.draft.html` — Drive can't
   edit in place. The newest file ID is recorded in the pipeline; earlier
   uploads are dead versions.

## Update state

Set the brief's status in `BLOG_PIPELINE.md` to `awaiting-gate-1` with the
draft's **Drive file ID and viewUrl**. Commit only the pipeline update to the
feature branch — never the draft itself.

## Gate 1 review (present to Jeff, then STOP)

```
DRAFT REVIEW — <title>
Draft: <slug>.draft.html · <Drive viewUrl> · Words: N
Hook: <first two sentences verbatim>
Preview: <H2 outline>
SEO: title N chars · meta N chars · keyword "<kw>" in H1/first-100 ✓/✗
Authorities used: <list with pinpoints> · [CITE NEEDED]: n
CTA: ✓ placement/wording · Statutes: ✓ format
Anonymization: ✓ checklist run · Legal-safety: ✓/flags
Options: **Enrich** · request edits · cancel
```

Do not proceed until Jeff answers.
