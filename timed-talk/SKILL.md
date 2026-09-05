---
name: timed-talk
description: 'Build a talk that must fit a hard clock — a deck whose speaker notes carry the exact words to speak, timing measured rather than estimated. Use whenever a talk has a fixed slot and overrunning costs something, such as a thesis or PFE defense, a conference talk, a demo day pitch, or a slotted internal review. Trigger it even when the user only says "I have 15 minutes" or asks for help rehearsing something to time.'
---

# Timed talk

A talk with a fixed slot is not a document that happens to be spoken. The clock is the design
constraint, and it binds before content, structure or visuals do.

Three ideas carry the whole skill:

- **The script is the deliverable.** Slides are the visual aid. Write the words first.
- **The budget is arithmetic, not judgement.** Words ÷ rate = minutes. Compute it, then measure
  the draft against it.
- **Cut by design, not by acceleration.** Mark what can be dropped before you need to drop it.

## Time arithmetic

Do this before writing a word, and show the numbers.

- Delivery rate under stress: **130 words per minute**. Nervous speakers accelerate; planning
  above 140 is planning to be unintelligible.
- **Target 90% of the slot.** Fifteen minutes means a 13.5-minute script. The buffer absorbs a
  slow start, a projector fumble, and one lost thread.
- 13.5 min × 130 wpm ≈ **1,750 words**.
- **One slide per 50–70 seconds.** A 15-minute talk is 12–16 slides, not 30.

Write the per-slide word budget into a table before drafting.

**Measure, never estimate.** A word count you eyeballed will be wrong, and the error runs to
whole minutes — long enough to lose the ending. `scripts/check_timing.py` reads the script and
reports actual counts per slide and overall. Run it after every substantive edit, and report
what it returned rather than what you expected.

## Script convention

The spoken words live in the script file as blockquote lines, which is what
`check_timing.py` counts:

```markdown
## Slide 7 — Architecture
**Time:** 1:15 · CORE

> Everything you just saw runs through one chain.
> A source, three transforms, a destination.

CUE: click to reveal the second column
NEXT: "That chain only works because of one decision…"
```

Everything outside the blockquote is stage direction and costs no clock.

## Spoken-script style

- **Sentences under 20 words.** One clause per breath. If you cannot say it in one breath,
  split it.
- **Use contractions.** "It doesn't scale." Written-formal read aloud sounds like a hostage
  statement.
- **Say numbers the way a person says them.** "About a third of requests," not "31.7%."
  Precision belongs on the slide; the mouth rounds.
- **Signpost before enumerating.** "Three decisions shaped this. First…" The listener cannot
  see your outline — give them the shape before the content.
- **Chain, don't nest.** Written prose nests subordinate clauses; speech chains short
  sentences. Turn "which, because of X, meant Y" into two sentences.
- **Expand every acronym once on first use**, including the obvious ones. There is always one
  person from another specialism.
- **Write the transitions.** The sentence carrying the audience from slide 7 to slide 8 belongs
  in the script. Improvised transitions are where time disappears.
- **Draft in the language of delivery.** Translating a script kills its rhythm.

The mouth carries the verb, the slide carries the noun. Any sentence that is both on the screen
and in the script is a sentence the audience finishes before you do, and then stops listening.

## Timing control

- **Mark every slide CORE or CUTTABLE**, aiming for 20–25% cuttable. Running long, the speaker
  drops a marked slide. Speeding up destroys comprehension and is the reflex to design out.
- **Protect the graded content.** Whatever the talk is being judged on — the problem, the
  results, the ask — stays CORE.
- **Put a wall-clock checkpoint in the middle slide's notes.** One glance tells the speaker
  whether to cut.
- **The demo is the biggest timing risk.** Play a recording, pre-trimmed to the budgeted
  seconds, and keep two stills in reserve. A speaker fighting a video player for ninety seconds
  loses those ninety seconds permanently.

## Slide layout

Projector-safe and back-row legible. Conservative on purpose: a timed talk is a bad place to
discover that a visual choice does not survive the room.

- **One idea per slide.** If the title needs "and", it is two slides.
- **Body ≥ 24pt, titles ≥ 32pt.** Smaller is invisible past the third row.
- **Six lines, six words a line.** Fragments, not sentences.
- **High contrast, and assume the lights stay on.** Dark on light survives a bad projector;
  light on dark often does not.
- **Encode meaning in shape, label or position as well as colour.** Roughly 1 in 12 men has a
  colour vision deficiency and audiences are small enough that the odds are not on your side.
- **Regular or medium font weights.** Thin weights disappear under projection.
- **Fix the title position across every slide.** A title that shifts 20px reads as carelessness
  even when nobody notices it consciously.
- **Figures beat tables; tables beat paragraphs.** More than 4 rows or 3 columns means a
  figure.
- **Number every slide.** Someone will say "go back to slide 9."

## Workflow

1. **Read the whole source pile before structuring.** Report, notes, recording, prior decks.
2. **Establish the constraints:** exact slot, language, who is in the room and how technical,
   whether a template is imposed, whether the demo is recorded, whether questions follow.
3. **Produce the time budget and slide plan** — title, one-line purpose, CORE/CUTTABLE, word
   budget. Get approval before writing prose. Done when every slide has a row.
4. **Write the full script** as a standalone markdown file. This is what the speaker rehearses
   from, so it ships even when the deck does.
5. **Run `scripts/check_timing.py`** and cut or expand until it reports the script under
   target. Done when its output says so.
6. **Build the deck**, script into the speaker notes, verbatim.
7. **Deliver both files.** A speaker rehearsing from a deck cannot see the notes and the slide
   at once; a printable script solves it.

Generate the deck from the script file rather than typing notes twice — a deck and a script
that drift apart are worse than either alone, and by the last rehearsal only one of them is
true.

## Variants

The machinery above is the same for every timed talk. What differs is the section structure,
what the audience is listening for, and how questions work.

- **Academic defense** (soutenance, PFE, thesis) — `references/academic-defense.md`
- **Conference talk** — `references/conference-talk.md`

Read the one that matches before producing the slide plan.

## Verification

Report measured numbers, not assurances:

| Check | Bound |
|---|---|
| Total words ÷ 130 | ≤ 90% of the slot |
| Words per slide | Flag over 160 — that slide does two jobs |
| Longest sentence | Split anything over 25 words |
| CUTTABLE share | 20–25% |
| Acronyms | Each expanded on first use |
| Slide text vs script | No sentence appears in both |

If it overruns, say so and cut. A faster delivery rate is not a fix, it is the same overrun
with worse comprehension.
