# Long decks — delegating to subagents

## Why

Every `edit-design` call returns the full page document, roughly 12,000 tokens, and the API
offers no way to filter it. Reads can be compressed with `scripts/canva_peek.py`; edit
responses cannot.

Past about fifteen pages the context window fills faster than the work advances. You start
re-reading pages you already handled, and each re-read costs another 16,000 characters. The
run slows as it goes.

One subagent per section fixes it: the responses land in their context, and what comes back is
a short report.

Measured on a 70-page rebuild: roughly 300,000–440,000 tokens per agent for 12–16 pages,
50 tool calls each. Four agents carried 66 pages.

## Briefing pattern

Write one shared brief the agents read rather than repeating instructions per dispatch. It
carries the rules, the gotchas, the workflow and the page map. Each dispatch then adds only
that agent's page range and assignments.

Every dispatch must include:

**Verified state, and permission to distrust it.** Say which pages are done. Then tell the
agent to confirm with one `presenter_notes` read before editing, and to report the real
boundary. On a 70-page run this caught an assignment that was off by three pages, because
earlier work had gone further than the log recorded.

**The page range, and nothing outside it.** Overlapping agents will fight over transactions.

**Per-page assignments.** Which source content fills which page. Vague scope produces invented
content.

**The method rules verbatim.** Full locator paths, one page per read, `replace_text` over
`add_text`, commit every five pages, check every thumbnail. Agents that skip these rediscover
them expensively.

**What to report back.** Ask for: pages completed, the real boundary found, layouts that did
not fit and what they did, anything the API refused, what they logged. Cap it — 200 words
keeps the summary useful and the context small.

## Sequential, not parallel

Agents share one design. Concurrent transactions collide. Dispatch one, wait, dispatch the
next with the state it left behind.

## Committing

Instruct every agent to commit every five pages. Session limits end agents mid-run — this
happened twice on the 70-page rebuild. Committed pages survived; the open transaction did not.

When an agent dies, do not assume where it stopped. Read `presenter_notes` across its range
and resume from the first page still in the source language.
