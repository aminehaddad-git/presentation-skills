# Academic defense

Soutenance, PFE, thesis, viva. The jury is small, expert, and grading you — not the project.
Questions follow, and they are where the mark moves.

## Structure

Shares of speaking time for a 15-minute slot. Adjust with the user, but defend a large
deviation rather than drifting into one.

| Section | Share | ~Time | Purpose |
|---|---|---|---|
| Title and identity | 3% | 25s | Name, title, supervisor, institution. Do not linger. |
| Problem and context | 12% | 1m40 | What was broken, for whom, why it mattered. Concrete. |
| Objectives | 7% | 1m | Stated as testable claims. |
| State of the art | 8% | 1m10 | Only what justifies your choices. Not a literature review. |
| Architecture | 18% | 2m30 | The one diagram that carries the system. |
| Key design decisions | 15% | 2m | Decision → alternatives → why → what it cost. |
| Demo | 12% | 1m40 | Recording, narrated. |
| Results and validation | 12% | 1m40 | Evidence the objectives were met. |
| Limitations | 6% | 50s | Honest and bounded. |
| Contribution and perspectives | 7% | 1m | What is specifically yours, then next steps. |

**Weight the design decisions.** A jury grades reasoning, not a feature list. One slide saying
"I chose X over Y because Z, and here is what it cost me" outperforms five feature slides.

## Annex slides

After the final slide, add 3–6 unshown annexes: the detailed architecture, the full results
table, the awkward algorithm, the data model. The speaker jumps to them during questions.

This is the highest-leverage item in a defense deck. "Yes — here it is" beats reconstructing a
diagram from memory in front of people who know it better than you do. Number them separately
(A1, A2…) and keep an index slide the speaker can find under pressure.

Build the annex set from the questions the limitations section invites. A limitation you raise
is a question you have already been asked.

## Presenting limitations

A jury respects a candidate who bounds their own work and punishes one who oversells. Three
moves per limitation:

1. **State it plainly.** "The system was tested with twelve concurrent users, not the two
   hundred it targets."
2. **Bound it.** What it does and does not invalidate. "That validates the workflow logic; it
   says nothing about connection pooling."
3. **Resolve it.** One concrete next step — "a load test with a simulated pool at 200
   connections," not "more testing."

State, bound, resolve. No apology, no hedging. The same three moves answer the question
verbatim when it comes back in Q&A.

Pick the two or three a jury would find anyway. Volunteering a weakness they spotted defuses
it; volunteering trivial ones spends time and buys nothing.

**Where no measurement exists, say so rather than producing a number.** An invented baseline is
the one failure a specialist jury catches instantly, and it costs more than the missing
measurement would have. Build the claim on what was actually counted — steps, clicks, lines,
a single timed figure — and let the script say plainly that the rest was not measured.

## Separating your contribution

Final-year projects sit on frameworks, templates and teams. State early and explicitly which
parts are yours: a dedicated slide, two columns, **provided** and **built by me**.

Juries ask this in nearly every defense. Answering before it is asked reads as confidence;
answering after reads as defensiveness.

## Reading the room

Ask who the jury is and how technical each member is. Three specialists in your own area is a
different talk from two specialists and an outsider — the outsider decides how much vocabulary
you can assume, and they are usually the one who asks the question you cannot answer.
