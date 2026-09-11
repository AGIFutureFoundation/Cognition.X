#!/usr/bin/env python3
"""Validate the canonical dataset (data/blocks.csv).

Checks:
  1. block_id present and globally unique
  2. required fields non-empty (pack, grade, credential, theme, transfer_check)
  3. tracked rows carry code, level and description
  4. band/level pairing on tracked rows (K-2/3-5 Explorer, 6-8 Builder,
     9-10 Practitioner, 11-12 Lead)
  5. every tracked (pack, track) has exactly 10 themes x 5 bands = 50 rows
  6. codes unique within their pack

Exits non-zero on any failure; prints a census either way.
"""

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

BLOCKS = Path(__file__).resolve().parent.parent / "data" / "blocks.csv"
BAND_LEVEL = {"K–2": "Explorer", "3–5": "Explorer", "6–8": "Builder",
              "9–10": "Practitioner", "11–12": "Lead"}
# code and level are guaranteed dataset-wide since v0.14.0 (light fill);
# description remains required on tracked rows only.
REQUIRED = ["pack", "grade", "code", "level", "credential", "theme", "transfer_check"]

errors = []


def err(msg):
    errors.append(msg)


def main():
    with open(BLOCKS, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    ids = Counter(r["block_id"] for r in rows)
    for i, n in ids.items():
        if n > 1:
            err(f"duplicate block_id {i} ({n} rows)")
    for idx, r in enumerate(rows, 2):
        if not r.get("block_id"):
            err(f"line {idx}: missing block_id")
        for f_ in REQUIRED:
            if not r.get(f_):
                err(f"line {idx} ({r.get('block_id')}): empty {f_}")

    tracked = [r for r in rows if r["track"]]
    for r in tracked:
        for f_ in ("code", "level", "description"):
            if not r[f_]:
                err(f"{r['block_id']}: tracked row missing {f_}")
        expect = BAND_LEVEL.get(r["grade"])
        if expect and r["level"] != expect:
            err(f"{r['block_id']}: grade {r['grade']} should be level {expect}, got {r['level']}")

    per_track = defaultdict(list)
    for r in tracked:
        per_track[(r["pack"], r["track"])].append(r)
    for (pack, track), trows in per_track.items():
        if len(trows) != 50:
            err(f"{pack} / {track}: {len(trows)} rows, expected 50")
        # The documented shape is 10 themes x 5 bands. Checking only the row
        # count and the theme count let a track pass with a band taught twice
        # and another missing, which is exactly what the shape exists to stop.
        themes = {r["theme"] for r in trows}
        if len(themes) != 10:
            err(f"{pack} / {track}: {len(themes)} distinct themes, expected 10")
        for theme in sorted(themes):
            bands = [r["grade"] for r in trows if r["theme"] == theme]
            if sorted(bands) != sorted(BAND_LEVEL):
                err(f"{pack} / {track} / {theme}: bands {sorted(bands)}, "
                    f"expected one row at each of {sorted(BAND_LEVEL)}")
        # every tracked row must carry a grade the band table knows, or the
        # grade/level agreement check above silently skips it
        unknown = sorted({r["grade"] for r in trows if r["grade"] not in BAND_LEVEL})
        if unknown:
            err(f"{pack} / {track}: unknown grade band(s) {unknown}")
        themes = {r["theme"] for r in trows}
        if len(themes) != 10:
            err(f"{pack} / {track}: {len(themes)} themes, expected 10")

    per_pack_codes = defaultdict(Counter)
    for r in tracked:
        per_pack_codes[r["pack"]][r["code"]] += 1
    for pack, codes in per_pack_codes.items():
        for c, n in codes.items():
            if n > 1:
                err(f"{pack}: code {c} appears {n} times")

    packs = Counter(r["pack"] for r in rows)
    print(f"{len(rows)} blocks, {len(packs)} packs, {len(per_track)} tracks, "
          f"{len(set(r['credential'] for r in rows))} credentials")
    for p, n in packs.most_common():
        print(f"  {n:>5}  {p}")

    if errors:
        print(f"\nFAILED: {len(errors)} problem(s)", file=sys.stderr)
        for e in errors[:50]:
            print(f"  - {e}", file=sys.stderr)
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more", file=sys.stderr)
        sys.exit(1)
    print("\nOK: all checks passed")


if __name__ == "__main__":
    main()
