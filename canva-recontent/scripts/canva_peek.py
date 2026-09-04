#!/usr/bin/env python3
"""Compact-print a saved Canva `read-design` payload.

One page of element JSON runs about 16,000 characters; four pages exceeds the
tool-result limit and the call fails outright. This prints only what is needed to
write edit operations — locator id, type, font size, colour, current text —
recursing into groups, in roughly forty lines per page.

Usage:
    python3 canva_peek.py <saved-payload.txt>
    python3 canva_peek.py --latest [search-root]

`--latest` picks the most recently modified file matching *read-design* under the
search root (default: current directory).
"""
import json
import os
import sys
import glob


def find_latest(root="."):
    hits = glob.glob(os.path.join(root, "**", "*read-design*"), recursive=True)
    hits = [h for h in hits if os.path.isfile(h)]
    if not hits:
        sys.exit(f"no read-design payload found under {root!r}")
    return max(hits, key=os.path.getmtime)


def walk(elements, depth=0):
    for el in elements:
        kind = el.get("type")
        lid = el.get("locator_id", "")
        pad = "  " * (depth + 1)

        if kind == "text":
            regions = el.get("textRegions", [])
            body = " | ".join(
                r["characters"].replace("\n", "⏎") for r in regions
            )
            if regions:
                fmt = regions[0]["formatting"]
                size = fmt.get("fontSize", "?")
                size = round(size) if isinstance(size, (int, float)) else size
                colour = fmt.get("color", "")
            else:
                size, colour = "?", ""
            print(f"{pad}TXT {lid}")
            print(f"{pad}    {size}px {colour} :: {body[:130]}")

        elif kind == "group":
            print(f"{pad}GRP {lid}")
            walk(el.get("children") or el.get("elements") or [], depth + 1)

        elif kind in ("rect", "shape"):
            media = (el.get("fill") or {}).get("media") or {}
            asset = media.get("mediaId") or media.get("videoId") or "-"
            colour = ""
            if el.get("paths"):
                colour = (
                    el["paths"][0].get("fill", {}).get("color", {}).get("color", "")
                )
            print(f"{pad}{kind.upper():5} {lid}  media={asset} {colour}")

        else:
            # unsupported, line, table, embed — cannot be text-replaced
            print(f"{pad}{str(kind).upper():5} {lid}")


def main():
    args = sys.argv[1:]
    if not args or args[0] == "--latest":
        path = find_latest(args[1] if len(args) > 1 else ".")
        print(f"# {path}\n")
    else:
        path = args[0]

    raw = open(path, encoding="utf-8").read()
    start = raw.find("{")
    if start < 0:
        sys.exit("no JSON object in payload")
    data = json.loads(raw[start:])

    txid = (data.get("transaction") or {}).get("transaction_id")
    if txid:
        print("TRANSACTION:", txid)

    content = data.get("design_content") or data.get("document") or data
    pages = content.get("pages") or ([content["page"]] if "page" in content else [])
    if not pages:
        sys.exit("no pages in payload — check filter.fields included design_content")

    for page in pages:
        notes = page.get("notes") or ""
        print(f"\n=== PAGE {page.get('locator_id')}   notes={len(notes)}ch")
        walk(page.get("elements", []))


if __name__ == "__main__":
    main()
