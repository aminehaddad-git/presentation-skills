# Manual gaps — <design name>

**Design:** <edit URL>
**Re-contented:** <date> · pages <range>

What the API could not do. Written as the run goes, not reconstructed afterwards. Every row
names a page and an action.

---

## 1 · Pages to delete

There is no delete-page operation. These read coherently but have no place in the new deck.

| Page | Why |
|---|---|

---

## 2 · Images to replace

Local files cannot be uploaded through the API. Drag them into Canva Uploads, then click the
image and use Replace.

| Page | Currently shows | Should show | Priority |
|---|---|---|---|

Mark priority `high` when the original author's brand is visible, or when the slide's argument
depends on the image being right.

---

## 3 · Elements the API refused

`unsupported` types, usually styled text effects.

| Page | Element | Currently | Should be |
|---|---|---|---|

---

## 4 · Judgement calls

Where the layout did not fit the content and a choice was made. Each row says what was decided
and what would make the user want it back.

| Page | Decision | Revisit if… |
|---|---|---|

---

## 5 · Verified complete

Pages checked against their thumbnail, nothing clipped or overlapping.

Pages: <range>

---

## 6 · Before presenting

- [ ] Delete the pages in section 1
- [ ] Replace the images in section 2, high priority first
- [ ] Fix the elements in section 3 by hand
- [ ] Read every speaker note once
- [ ] Export to PDF as a fallback — removes font-substitution risk entirely
