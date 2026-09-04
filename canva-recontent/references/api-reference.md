# Canva connector — what the docs do not tell you

Every entry here was paid for in a failed call or a wasted context window during a 70-page
re-content run. The tool descriptions do not carry them.

The five that bite on the first page are stated in `SKILL.md` and not repeated here. This file
is the long tail behind them.

---

## Silent failures

**`filter.element_ids: []`** returns zero elements rather than all of them. A page looks empty
and you conclude it has no text. Omit the key entirely when you want everything.

**The tool description says a trailing element id is enough.** It is not — see the locator
rule in `SKILL.md`. Worth knowing because the description reads authoritative, so the natural
response to the error is to doubt the page id and go re-read the page, which costs a full
element-JSON read to learn nothing.

**`replace_text` wipes list markers.** A bulleted list becomes unbulleted paragraphs and
nothing reports it. Restore with `format_text` carrying `list_marker` and `list_level`, or
avoid the loss with `find_and_replace_text`.

**`replace_text` collapses multi-region titles.** A heading built from several styled runs —
one word bold, the rest regular — becomes a single style. `find_and_replace_text` preserves
the regions. Reach for it whenever a title mixes weights.

---

## Element types that refuse edits

`type: "unsupported"` covers styled text effects, and often the decoration baked around them.
`replace_text` cannot touch it. Deleting it and rebuilding with `add_text` loses whatever came
with it — on one title slide, deleting the styled heading also removed the white card behind
it, which then had to be reconstructed as a shape and layered back.

Prefer leaving an `unsupported` element in place and logging it for the human. Delete only
when it carries text that would otherwise be plainly wrong, such as another project's name.

---

## Operations that do not exist

- **No delete-page.** `add_page` and `reorder_page` exist; removal does not. Surplus pages get
  translated so they read coherently, then logged for manual deletion.
- **No animation or transition control.** Nothing reads or writes them. They survive
  `copy-design` untouched, which is why copying beats rebuilding — but a page you add yourself
  has none, and you cannot give it any.
- **No image upload from a local path.** `update_fill` needs a Canva `asset_id`;
  `upload-asset-from-url` needs a public URL. Local files must be dragged into Canva Uploads
  by the human first.

---

## Sizes and limits

| Thing | Value |
|---|---|
| Element JSON, one page | ~16,000 characters |
| Read of four pages | ~64,000 characters — exceeds the limit, call fails |
| Edit response | The full page document, ~12,000 tokens, every call |
| Large-heading break point | ~18 characters at 61px, ~25 at 55px |

The edit-response size is the binding constraint on long runs, and it cannot be filtered.
Budget for it or delegate — see `orchestration.md`.

---

## Layout behaviour

**English runs longer than French.** Translating a deck lengthens most strings. Headings break
mid-word at large sizes. Shorten the wording rather than shrinking the font — a font change
propagates visually across a deck built on consistent type.

**Canva re-anchors text boxes** when replaced text wraps to a new line count. Usually correct.
Check the thumbnail rather than assuming either way.

**Groups nest one level in practice.** A card is typically `PAGE-GROUP-ELEMENT`. Recurse when
listing rather than assuming depth.

---

## Why the thumbnail is the only check

The thumbnail rule lives in `SKILL.md`; the reason it is worth a read per page is here. The
failure it catches is the one no status field can report: text that is correct, was applied,
and overflows its box. Every field in the response says success, and the page is unusable.
