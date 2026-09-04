---
name: canva-recontent
description: Rebuild an existing Canva design with new content while its layout, build steps and animations survive intact. Use whenever a Canva design is filled from a template, adapted after someone shared it, rebranded, translated, or edited across many pages at once — including when the user only says they want to reuse a deck rather than build one from scratch.
---

# Canva re-content

Needs the Canva connector: `copy-design`, `read-design`, `edit-design`.

A finished deck is a **template**: someone already solved the layout, the rhythm, the
progressive reveals. Re-contenting keeps that solution and replaces only what it says.

Text and speaker notes go through the API cleanly. Images, page deletion and animations do
not — those become a **gaps file** the human finishes by hand. A run that pretends otherwise
ships a broken deck.

## Before you start

Confirm the design is one the user owns, has a licence to reuse, or was given by its author
for this purpose. Templates and a colleague's shared deck qualify. If provenance is unclear,
ask once.

## Steps

**1 · Copy first.** `copy-design` with the source id; every later operation targets the copy.
The original stays as found, which is what makes a bad result cheap to throw away and rerun.
Done when you hold a new design id.

**2 · Survey before you touch anything.** One `read-design` with
`filter.fields:["presenter_notes"]` across the full page range shows which pages are already
converted — cheap, and it catches resumed work. Then one `read-design` with
`filter.fields:["design_content"]` (no transaction) returns plain readable text for many pages
at once. Field-scoped reads stay small; the full element JSON of step 4 does not. Done when
you can name what is on every page.

**3 · Write the page map before editing.** A table: page number, what it currently holds,
what it becomes, which source content fills it. Show it to the user. Done when every page in
scope has a row, including the ones you plan to leave alone.

**4 · Edit one page at a time.** Read the page with `open_transaction:true`, run
`scripts/canva_peek.py` on the saved payload for a compact locator listing, then batch
`replace_text` plus `replace_speaker_notes`.

Every operation reports `applied_unverified`, which says only that the call was accepted. The
response also carries a **thumbnail** URL rendering the page with the uncommitted edits on it.
That image is the evidence; the status field is not. Done when the thumbnail shows the new
text with nothing clipped or overlapping.

**5 · Commit every five pages.** `finalize:"commit"` with an empty `operations` array, then
reopen a transaction. Long runs hit session limits, and uncommitted work dies with them. Done
when the commit returns and every page behind you is in the gaps log or verified complete.

**6 · Log every gap as you meet it.** Append to the gaps file — see
`templates/manual-gaps.md`. Done when every image you left, page you would have deleted, and
element the API refused has a row naming the page and what to do.

## Rules that bite immediately

- **Locator ids are full paths.** `PAGE-LBxxx`, or `PAGE-GROUP-LBxxx` for anything inside a
  group. A bare element id fails with `"Page ID did not match the expected pattern"`, which
  names the wrong thing and costs a retry.
- **Read one page per call.** Four pages of element JSON runs past 60,000 characters and the
  call fails outright.
- **Reach for `replace_text` first.** It inherits the element's existing styling. `add_text`
  lands at 16px and needs a `format_text` pass behind it.
- **Keep every position, size, colour and font as found.** Move something only when the
  thumbnail shows it clipped, and log the move.

`references/api-reference.md` holds the rest: silent failures, element types that refuse
edits, what `replace_text` does to list markers, and the operations that do not exist.

## Long decks

Edit responses return the whole page document — roughly 12,000 tokens each. Past about fifteen
pages this fills the context window faster than the work progresses. Dispatch one subagent per
section so the responses land in their context, not yours.
`references/orchestration.md` has the briefing pattern and what each agent must report back.

## Finishing

Hand back three things: the design URL, the gaps file, and a one-line honest statement of what
is not done. The gaps are the deliverable's other half — a user who thinks the deck is
finished will find the original author's logo on a slide during their talk.
