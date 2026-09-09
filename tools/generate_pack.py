#!/usr/bin/env python3
"""Expand a pack specification into curriculum blocks.

A pack spec (JSON) declares tracks; each track declares a two-letter code
prefix, a credential name, and ten themes. Every theme is expanded across
the five grade bands used by every tracked Cognition.X pack:

    K-2   Explorer
    3-5   Explorer
    6-8   Builder
    9-10  Practitioner
    11-12 Lead

so a 5-track pack yields 5 x 10 x 5 = 250 blocks, matching the shape of
the existing community packs (Housing & Tenancy, Money, Benefits &
Entitlements, ...).

Usage:
    python3 tools/generate_pack.py data/pack_specs/<spec>.json > out.csv
"""

import csv
import json
import sys

BANDS = [
    ("K–2", "Explorer"),
    ("3–5", "Explorer"),
    ("6–8", "Builder"),
    ("9–10", "Practitioner"),
    ("11–12", "Lead"),
]

FIELDS = [
    "pack", "track", "code", "grade", "level",
    "credential", "theme", "description", "transfer_check",
]


def expand(spec):
    rows = []
    for track in spec["tracks"]:
        if len(track["themes"]) != 10:
            raise ValueError(
                f"track {track['name']!r} has {len(track['themes'])} themes, expected 10"
            )
        n = 0
        for theme in track["themes"]:
            for grade, level in BANDS:
                n += 1
                rows.append({
                    "pack": spec["pack"],
                    "track": track["name"],
                    "code": f"{track['prefix']}-{n}",
                    "grade": grade,
                    "level": level,
                    "credential": track["credential"],
                    "theme": theme["theme"],
                    "description": f"{theme['description']} — at {grade}",
                    "transfer_check": theme["transfer_check"],
                })
    return rows


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    rows = expand(spec)
    w = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)
    print(f"generated {len(rows)} blocks for pack {spec['pack']!r}", file=sys.stderr)


if __name__ == "__main__":
    main()
