# IDEATE — Multi-Source Topic Generation

Goal: produce **story briefs**, not titles. The old pipeline failed because it
emitted templated titles ("What to Know About X Charges in Florida") scored by
keyword volume. A brief earns its place by having a story, a timing hook, and
authority sources to cross-reference.

## Sweep (in order)

Window: **past 60 days + next 45 days** unless Jeff specifies otherwise.

1. **Calendar** (`DATA_SOURCES.md` §1): list events from LLOJL, Lotter Law,
   AI Court Dates, and Court Conditions Due. Keep events that are hearings,
   motions, trials, formal reviews, or decision points (plea/PTI/diversion
   offers). Discard personal events immediately — don't even summarize them.
2. **Holidays/seasonal**: US Holidays calendar + known enforcement seasons
   (July 4th saturation patrols, back-to-school zones in August, holiday DV
   spike, New Year seal-and-expunge).
3. **Editorial calendar**: `.claude/knowledge/EDITORIAL-CALENDAR-2026.md` —
   what was planned for this month and next?
4. **Backlog**: `BLOG_IDEAS.md` — anything `Ready to go` (e.g., the
   Intoxilyzer series) or worth reviving with a fresh hook?
5. **Analytics**: newest report in `analytics/reports/` — ranking gaps and
   high-impression/low-CTR queries that a story could serve.
6. **Gmail enrichment** (per candidate, not a broad sweep): follow the thread
   linked in the calendar event, or search the case-type anchor, to confirm
   what actually happened. Verification only — nothing quoted.

## Build each candidate into a brief

For each surviving candidate, draft:

```markdown
### BRIEF-YYYYMM-NN: <working title>
- **Status:** proposed
- **The story (anonymized):** 2-4 sentences. What happened / is happening,
  told as a narrative. Month-level dates, roles not names.
- **Why now:** the timing hook (season, recent hearing, law change, trend).
- **Authority cross-refs (≥2 required):** each as `source → what it will
  prove` (e.g., "Academy manual pp. on consent searches → officers are
  trained X", "OCSO GO 8.1.7 → pursuits require Y", "Library: <Case>, VERIFIED
  → holding Z", "F.S. §316.193", "intox8000 dataset").
- **The hook:** one draft opening line. If you can't write a hook, the brief
  isn't ready.
- **SEO:** primary keyword · search intent · gap check result (see below).
- **CTA angle:** why a reader with this problem calls Jeff.
- **Score:** S_/3 A_/3 T_/2 G_/2 = _/10
```

## Duplicate / gap check

List **every** slug under `blog/` (full `ls`, never a truncated or sampled
listing) AND `grep -rli` the corpus for the candidate's core terms — a topic
often has multiple posts under non-obvious slugs (lesson: "stand your ground"
had four). If the topic is covered, the brief must state a **new angle** not
covered by ANY existing post, or be killed. List every existing related post
in the brief — they become mandatory internal links.

## No legal assertions in briefs

A brief describes what a source will be *checked for* — it never states a
legal standard, burden, or holding as fact. Write "F.S. §776.032 → verify
burden and hearing procedure," not "the State must prove X." Legal accuracy
enters the pipeline at RESEARCH, from the actual texts; and Jeff corrects
the story itself at brief review. He was there — the brief wasn't.

## Scoring

- **Story (0-3):** 3 = specific narrative from real practice; 0 = generic
  explainer. *Score 0 ⇒ kill the brief. This is the filter the old system
  lacked.*
- **Authority (0-3):** 3 = two-plus strong cross-refs already located; 1 =
  cross-refs assumed but not yet found.
- **Timeliness (0-2):** 2 = tied to the next 45 days or an active trend.
- **SEO gap (0-2):** 2 = clear gap or documented ranking opportunity.

## Output

1. Append briefs to `BLOG_PIPELINE.md` under "Proposed briefs" (anonymized —
   the file is public).
2. Present the top ~5 to Jeff ranked by score, one short paragraph each.
3. For the briefs Jeff picks, run **Gate 0 (Story Check — see SKILL.md)**:
   give your outline of understanding of each story and ask "Do I have it
   right?" Only confirmed stories advance to RESEARCH. Remember: a calendar
   entry proves something was scheduled, never that it happened.

## Kill list (learned failures — reject on sight)

- Template titles with no story ("Understanding X Charges in Florida").
- CRM/inquiry noise outside practice areas (copyright, civil suits).
- Anything whose only source is "recent inquiries about X".
- Topics already covered with no new angle or no new authority.
