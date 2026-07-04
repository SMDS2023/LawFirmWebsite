# Blog Drafts

Working drafts for the blog pipeline (`.claude/skills/blog/SKILL.md`).

- One folder per post: `blog-drafts/<slug>/index.html`.
- Drafts exist **only on feature branches** — the publish step moves the
  final post to `blog/<slug>/index.html` and deletes the draft folder, so
  nothing here should ever reach `master`.
- Everything in a draft must already pass the anonymization checklist in
  `SKILL.md` (this repository is public).
- Status tracking lives in `BLOG_PIPELINE.md` at the repo root.
