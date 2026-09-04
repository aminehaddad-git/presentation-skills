# Presentation skills for AI agents

Two agent skills for presentations, both written from a single real project rather than from
general advice

| Skill | For |
|---|---|
| [`canva-recontent`](#canva-recontent) | Reusing an existing Canva design with new content |
| [`timed-talk`](#timed-talk) | Any talk with a hard clock, script in the speaker notes |

Install with the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add aminehaddad-git/presentation-skills
```

Or pick one:

```bash
npx skills add aminehaddad-git/presentation-skills --skill canva-recontent
```

---

## `canva-recontent`

**Rebuild an existing Canva design with new content while its layout, build steps and
animations survive intact.**

A finished deck is a solved problem — someone already worked out the spacing, the rhythm, the
progressive reveals. Rebuilding from scratch throws that away. This re-contents it: keep the
design, replace what it says.

Handles template filling, reusing a deck a colleague shared, rebranding, and translating a
presentation into another language.

### Why it exists

The Canva connector's tool descriptions are accurate but incomplete, and the gaps are
expensive. This skill is mostly a cache of what a 70-page rebuild cost to discover:

| Behaviour | What actually happens |
|---|---|
| Bare element ids | Fail with `"Page ID did not match the expected pattern"` — which blames the page, not the element. Use the full `PAGE-GROUP-ELEMENT` path. |
| Reading four pages | ~64,000 characters. Exceeds the limit; the call fails. One page per read. |
| `filter.element_ids: []` | Returns zero elements, not all of them. The page looks empty. |
| `add_text` | Lands at 16px regardless of context. Needs a `format_text` pass behind it. |
| `replace_text` | Silently wipes list markers, and collapses multi-region titles to one style. |
| `unsupported` elements | Cannot be text-replaced. Deleting one may take its decoration with it. |
| Delete page | Does not exist. Neither does animation control. |
| Every edit response | Returns the whole page document, ~12,000 tokens, unfilterable. |

That last row is the one that shapes the architecture: past about fifteen pages it fills the
context window faster than the work advances, so the skill delegates by section.

### What it does not do

Image replacement needs a Canva `asset_id`, so local files must be uploaded by hand. Pages
cannot be deleted through the API. Animations survive a copy but cannot be created or edited.

The skill treats these as a **required output**, not a footnote: every run produces a
manual-gaps file naming each page and what to do there. A rebuild that claims to be finished
when the original author's logo is still on slide 14 is worse than one that says so.

### Ships with

- `scripts/canva_peek.py` — turns a 16,000-character page payload into ~40 readable lines
- `references/api-reference.md` — the full behaviour catalogue
- `references/orchestration.md` — the subagent pattern, with measured token costs
- `templates/manual-gaps.md` — the handover file

### Permission

Re-content designs you own, that are licensed for reuse, or that their author gave you for
this purpose. Templates and a colleague's shared deck qualify. Someone's portfolio piece does
not.

---

## `timed-talk`

**A talk that must fit a hard clock, delivered as a deck whose speaker notes carry the exact
words to speak.**

The clock is the design constraint, and it binds before content or visuals do. The skill does
the arithmetic — 130 words per minute, 90% of the slot, one slide per 50–70 seconds — then
measures the draft against it.

### Why it exists

Timing a talk by eye does not work. Writing this project's own defense script, the estimate
was wrong twice, once by a full minute — long enough to lose the ending, which is the part
being graded.

So the skill ships `scripts/check_timing.py`. It reads the script, counts only what will
actually be spoken, and reports per slide:

```
$ python3 check_timing.py defense-script.md --slot 15

slide                                         words    time
26 — 4.2 Forecasting — protocol and result      121    0:56  core
...
TOTAL                                          1774   13:39

slot 15 min · target 13:30 (90%) · rate 130 wpm
cuttable: 1/33 slides (3%, want 20-25%)
longest sentence is 45 words — split it: …

OVER by 0:09. Cut roughly 18 words.
```

It also names the sentence too long to say in one breath, and flags slides doing two jobs.

### Variants

The arithmetic, script style, slide rules and verification are the same for every timed talk.
What differs is section structure and how questions work, so those live in
`references/academic-defense.md` and `references/conference-talk.md`.

The defense material is the earned half — annex slides for Q&A, the state/bound/resolve shape
for limitations, and separating your contribution from the framework you built on. The
conference file is shorter and more general; treat it as a starting structure rather than
hard-won.

---

## Requirements

`canva-recontent` needs the Canva connector (MCP): `copy-design`, `read-design`,
`edit-design`. `timed-talk` needs Python 3 for the timing script and pairs with whatever
builds your deck.

## Testing the descriptions

A skill that never fires is worse than no skill. Each skill ships a 20-query trigger eval in
`evals/trigger-eval.json` — half should fire it, half are near-misses that should not. Run
them with the description optimiser in Anthropic's
[skill-creator](https://github.com/anthropics/skills):

```bash
python -m scripts.run_loop --eval-set canva-recontent/evals/trigger-eval.json \
  --skill-path canva-recontent --max-iterations 5
```

## Licence

MIT — see [LICENSE](LICENSE).
