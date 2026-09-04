#!/usr/bin/env python3
"""Measure a talk script against its clock.

Word counts eyeballed from a draft are wrong by whole minutes, which is long enough
to lose the ending of a talk. This counts what will actually be spoken.

Spoken words are the blockquote lines (`> `). Everything else — headings, stage
directions, cues — is not spoken and does not count.

Usage:
    python3 check_timing.py script.md --slot 15
    python3 check_timing.py script.md --slot 20 --wpm 140
"""
import argparse
import re
import sys

SLIDE_RE = re.compile(r"^#{1,4}\s*(?:Slide\s*)?(\d+)\s*[—\-–:]\s*(.+)$", re.I)
SENTENCE_RE = re.compile(r"[.!?]+\s+")
# Narration for a recorded demo is often a timed table: | 3 | 1:20-1:35 | words |
CUE_ROW_RE = re.compile(r"^\|[^|]*\|\s*\d+:\d\d\s*[—\-–]\s*\d+:\d\d\s*\|(.+)\|")


def parse(path):
    """Return [(slide_label, spoken_text, is_cuttable)] in document order."""
    slides, label, spoken, cuttable = [], None, [], False
    for line in open(path, encoding="utf-8"):
        m = SLIDE_RE.match(line.strip())
        if m:
            if label:
                slides.append((label, " ".join(spoken), cuttable))
            label = f"{m.group(1)} — {m.group(2)}"
            spoken, cuttable = [], False
            continue
        if "CUTTABLE" in line:
            cuttable = True
        s = line.strip()
        if s.startswith(">"):
            body = s.lstrip("> ").strip()
            if body:
                spoken.append(body)
        else:
            row = CUE_ROW_RE.match(s)
            if row:
                spoken.append(row.group(1).strip(" |"))
    if label:
        slides.append((label, " ".join(spoken), cuttable))
    return slides


def mmss(minutes):
    total = int(round(minutes * 60))
    return f"{total // 60}:{total % 60:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--slot", type=float, required=True, help="allotted minutes")
    ap.add_argument("--wpm", type=float, default=130.0)
    ap.add_argument("--target", type=float, default=0.90,
                    help="fraction of the slot to aim for")
    args = ap.parse_args()

    slides = parse(args.script)
    if not slides:
        sys.exit("no slides found — expected headings like '## Slide 7 — Title'")

    print(f"{'slide':<44} {'words':>6} {'time':>7}  ")
    print("-" * 62)
    total = 0
    for label, text, cut in slides:
        n = len(text.split())
        total += n
        flag = " ⚠ over 160" if n > 160 else ""
        print(f"{label[:44]:<44} {n:>6} {mmss(n / args.wpm):>7}"
              f"  {'CUT' if cut else 'core':<4}{flag}")

    minutes = total / args.wpm
    budget = args.slot * args.target
    cuttable = sum(1 for _, _, c in slides if c)

    print("-" * 62)
    print(f"{'TOTAL':<44} {total:>6} {mmss(minutes):>7}")
    print(f"\nslot {args.slot:g} min · target {mmss(budget)} "
          f"({args.target:.0%}) · rate {args.wpm:g} wpm")
    print(f"cuttable: {cuttable}/{len(slides)} slides ({cuttable / len(slides):.0%}, want 20-25%)")

    longest = max(
        (s.strip() for _, t, _ in slides for s in SENTENCE_RE.split(t) if s.strip()),
        key=lambda s: len(s.split()), default="")
    if len(longest.split()) > 25:
        print(f"\nlongest sentence is {len(longest.split())} words — split it:\n  {longest[:120]}")

    over = minutes - budget
    if over > 0:
        print(f"\nOVER by {mmss(over)}. Cut roughly {int(over * args.wpm)} words.")
        sys.exit(1)
    print(f"\nOK — {mmss(budget - minutes)} under target.")


def _selfcheck():
    """python3 check_timing.py --selftest"""
    import tempfile, os
    src = ("## Slide 1 — Intro\n**Time:** CUTTABLE\n\n> one two three four five\n"
           "CUE: ignore me\n\n## Slide 2 — Body\n\n> six seven\n> eight\n"
           "\n## Slide 3 — Demo\n\n| 1 | 0:00—0:10 | nine ten eleven |\n"
           "| head | col | ignored |\n")
    fd, p = tempfile.mkstemp(suffix=".md")
    os.write(fd, src.encode()); os.close(fd)
    got = parse(p)
    os.unlink(p)
    assert len(got) == 3, got
    assert got[0] == ("1 — Intro", "one two three four five", True), got[0]
    assert got[1][1] == "six seven eight", got[1]
    assert got[2][1] == "nine ten eleven", got[2]   # timed table row counts, header does not
    print("selfcheck ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selfcheck()
    else:
        main()
