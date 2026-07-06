# ENRICH — Images, Links, Schema (ends at Gate 2)

Input: a Gate-1-approved draft — download it from Drive using the file ID in
the pipeline entry (`mcp__Google_Drive__download_file_content` or
`read_file_content`), work on it in the scratchpad, then upload the result
as `<slug>.enriched.html` (same folder, same upload rules as `write.md`).
The enriched file is the artifact that gets staged.

## 1. Images

- Hero: `assets/blog/<slug>-hero.jpg` (1920×1080) with a real, descriptive
  `alt`, explicit `width`/`height`, and a caption that adds meaning.
- Social: `assets/blog/<slug>-og.jpg` (1200×630); set og:image,
  twitter:image, and schema image to it.
- Uncomment the hero `<figure>` once the asset exists; if the asset is
  pending, leave it commented and mark image status "pending" at Gate 2.
- Never use photos that could identify a client, scene, or officer.

### Sourcing, in preference order

1. **xAI image API (photorealistic)** — requires `XAI_API_KEY` env var AND
   `api.x.ai` in the environment's allowed domains (both set at
   claude.ai/code → environment settings). POST
   `https://api.x.ai/v1/images/generations` with
   `{"model": "grok-imagine-image", "prompt": ..., "response_format":
   "b64_json"}`; decode, then crop/resize with Pillow (`pip install
   pillow`). On 402 (zero balance — auto-top-up is OFF on Jeff's xAI
   account), 429 (Tier 0 limits), or connection failure: fall through — do
   not stall the pipeline.
2. **Branded og card, generated locally (always works)** — edit
   `templates/og-card-template.html` (kicker · headline w/ gold accent ·
   subline · LOTTER LAW footer), render with the pre-installed Chromium:
   `chromium --headless --no-sandbox --hide-scrollbars
   --force-device-scale-factor=1 --window-size=1280,900 --screenshot=out.png
   file://.../og-card.html`, then Pillow-crop to exactly (0,0,1200,630) and
   save JPG quality≈88 (Chromium's window-size does not equal viewport —
   always render oversized and crop). Good enough to ship; a photorealistic
   hero can replace it later.
3. **Reuse a fitting image from `assets/`**, or flag Gate 2 with a one-line
   art-direction prompt for Jeff to run in the Grok/Gemini app UI.

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

Upload `<slug>.enriched.html` to the drafts folder. `BLOG_PIPELINE.md` →
status `awaiting-gate-2` with the enriched file's Drive ID and viewUrl.
Commit only the pipeline update (plus any new image assets under
`assets/blog/`) to the feature branch.

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
