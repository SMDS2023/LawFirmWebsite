# ENRICH — Images, Links, Schema (ends at Gate 2)

Input: a Gate-1-approved draft in `blog-drafts/<slug>/`. Work in place —
the draft file is the artifact that gets staged.

## 1. Images

- Hero: `assets/blog/<slug>-hero.jpg` (1920×1080) with a real, descriptive
  `alt`, explicit `width`/`height`, and a caption that adds meaning.
- Social: `assets/blog/<slug>-og.jpg` (1200×630); set og:image,
  twitter:image, and schema image to it.
- Sourcing: reuse a fitting image from `assets/`, or flag Gate 2 with a
  one-line art direction note for Jeff ("dashcam at dusk, no faces") — do not
  fabricate stock-looking images without telling him. Never use photos that
  could identify a client, scene, or officer.
- Uncomment the hero `<figure>` once the asset exists; if the asset is
  pending, leave it commented and mark image status "pending" at Gate 2.

## 2. Internal links (the 1-3-2 rule)

- 1 link to the relevant pillar page, 3 to supporting posts, 2 to
  practice-area/intake pages — woven into sentences, not dumped in a list.
- **Related Articles**: two cards before the footer (template format), chosen
  from the gap-check posts.
- Back-links: identify 1-2 existing posts that should link *to* this post;
  queue those edits for the GOLIVE commit (they ride the same PR).

## 3. Technical SEO pass

- Article schema valid; BreadcrumbList present; canonical/OG/Twitter URLs all
  end in `/blog/<slug>/`.
- Headings hierarchical (one H1); primary keyword in H1, first 100 words,
  and at least one H2.
- GTM `GTM-52LMX48G` present; **no hardcoded GA4/Clarity** (known pitfall).
- All internal hrefs relative (`../../blog/...`) and resolving to real files.
- Word count still in range; no `[CITE NEEDED]` remaining unless Jeff okayed.

## 4. Update state

`BLOG_PIPELINE.md` → status `awaiting-gate-2`. Commit to the feature branch.

## Gate 2 review (present to Jeff, then STOP)

```
ENRICHED REVIEW — <title>
Applied: <images / links added / schema fixes>
Images: hero <ready|pending: art note> · og <ready|pending>
Links: pillar 1/1 · supporting n/3 · practice n/2 · related 2 · backlinks queued: <posts>
SEO report: title ✓ · meta ✓ · schema ✓ · breadcrumbs ✓ · headings ✓
Preview: <hook + H2 outline>
Options: **Stage** · **Publish Now** · edits · back to draft · cancel
```

- **Stage** → `publish.md` § STAGE (live by direct URL, unlisted).
- **Publish Now** → `publish.md` § STAGE then § GOLIVE in one pass.
