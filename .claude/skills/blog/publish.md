# PUBLISH — Stage and Go-Live

Controlling rule: **feature branch + PR** (master is protected). Direct push
only on Jeff's explicit say-so in the conversation.

## STAGE (reachable by URL, not listed anywhere)

1. Move `blog-drafts/<slug>/index.html` → `blog/<slug>/index.html` (create
   the folder; delete the draft folder). Fix any path depth changes.
2. Do **not** touch `blog.html` or `sitemap.xml`.
3. Commit (`feat(blog): Stage <slug>`), push the feature branch, open a PR
   titled `Stage: <post title>`. After merge + 2-5 min Pages deploy, the post
   is live at `https://lotterlaw.com/blog/<slug>/` for Jeff's private review.
4. `BLOG_PIPELINE.md` → status `staged`.

## GOLIVE (listed, indexed, dated)

1. **Set the publish date** (today unless Jeff says otherwise) in all four
   places: visible `<time datetime>`, `article:published_time` /
   `datePublished` + `dateModified` in schema, and the blog.html card.
2. **blog.html**: insert a new card at the **top** of the listing (directly
   after the listing container opens), using the card format below. Category
   chips must match the post's chips. Case-outcome posts get the green
   `Case Result` chip.
3. **sitemap.xml**: add a `<url>` entry (format below) with today's date.
4. **Back-links**: apply the queued edits from ENRICH so 1-2 older posts link
   to the new one.
5. Commit (`feat(blog): Publish <slug> - <short title>`), push, PR. If a
   Stage PR is already open, add these commits to the same branch/PR instead
   of opening a second one.
6. After merge: wait 2-5 min, verify `https://lotterlaw.com/blog/<slug>/`
   returns the post and the card appears on `/blog.html` (cache-bust).
7. `BLOG_PIPELINE.md` → status `live` with URL and date. Offer Jeff the
   distribution steps (`facebook.md`, `gmb.md`).

### blog.html card format

```html
<!-- <slug> -->
<article class="bg-white p-6 md:p-8 rounded-lg shadow-lg blog-post-summary section-fade-in">
    <header>
        <div class="flex gap-2 mb-1 flex-wrap">
            <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-medium">{{CATEGORY}}</span>
        </div>
        <h2 class="text-2xl md:text-3xl font-semibold text-blue-700 mb-2">
            <a href="blog/{{SLUG}}/" class="hover:text-amber-500">{{TITLE}}</a>
        </h2>
        <p class="text-sm text-gray-500 mb-3">
            Published on <time datetime="{{ISO_DATE}}">{{HUMAN_DATE}}</time>
        </p>
    </header>
    <div class="text-gray-700 mb-4 leading-relaxed">
        <p>{{ONE_SENTENCE_SUMMARY}}</p>
    </div>
    <footer>
        <a href="blog/{{SLUG}}/" class="text-blue-600 font-semibold hover:text-amber-500">
            Read More &rarr;
        </a>
    </footer>
</article>
```

### sitemap.xml entry format

```xml
<url>
    <loc>https://lotterlaw.com/blog/{{SLUG}}/</loc>
    <lastmod>{{ISO_DATE}}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
</url>
```
