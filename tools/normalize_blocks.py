#!/usr/bin/env python3
"""Build the canonical dataset from source + generated packs.

Reads data/source/Cognition.X_all_blocks.csv plus every CSV under
data/generated/, prepends a globally unique `block_id`, and writes:

    data/blocks.csv      canonical dataset (block_id + original columns)
    data/manifest.json   per-pack summary used by docs and the app

Why block_id: the source `code` column is only unique within a pack
(track prefixes such as EV- or SF- are reused across packs — 450 codes
collide). block_id is deterministic:

    CX-<PACK>-<NNNN>

where <PACK> is a stable slug per pack and <NNNN> is the 1-based row
number within that pack, in source order. Re-running this script on the
same inputs always yields the same ids, so they are safe to reference
externally. Original columns are passed through untouched.
"""

import csv
import json
import re
import unicodedata
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "source" / "Cognition.X_all_blocks.csv"
GENERATED = ROOT / "data" / "generated"
OUT_CSV = ROOT / "data" / "blocks.csv"
OUT_MANIFEST = ROOT / "data" / "manifest.json"

# Stable, human-readable slugs for pack ids. New packs fall back to an
# acronym derived from the pack name; entries here pin the ones that exist
# so ids never change.
PACK_SLUGS = {
    "K–12": "K12",
    "Trade School": "TRADE",
    "Future-Work": "FWORK",
    "Regional": "REGION",
    "Civic & Leadership": "CIVIC",
    "Health & Community": "HEALTH",
    "Language, Culture & Communication": "LANG",
    "Empathy & Emotional Intelligence": "EMPATH",
    "Community & Relationship Practice": "COMREL",
    "Preventive Health & Everyday Care": "PREVCARE",
    "Basic Life Skills & Self-Reliance": "LIFESKILL",
    "Water, Land & Climate": "WLC",
    "Care Across a Life": "CARELIFE",
    "Making, Repair & Reuse": "MAKE",
    "Housing & Tenancy": "HOUSING",
    "Money, Benefits & Entitlements": "MONEY",
    "Reentry & Recovery Pathways": "REENTRY",
    "Neighbourhood, Safety & Civic Voice": "NEIGH",
    "Cognition.X : Corporate OS": "CORP",
    "Cognition.X : Science OS": "SCI",
    "Cognition.X : Robotics OS": "ROB",
    "Cognition.X : Global Health OS": "GHEALTH",
    "Cognition.X : Multilateral OS": "MULTI",
    "Cognition.X : Sapient OS": "SAPIENT",
    "Non-Profit Practice": "NPO",
    "Digital Life, Data & AI": "DIGITAL",
    "Food, Cooking & Nutrition": "FOOD",
    "Energy, Grid & the Home": "ENERGY",
    "Transport & Mobility": "TRANSPORT",
    "Emergency Preparedness & First Response": "EMERGENCY",
    "Arts, Making Media & Performance": "ARTS",
    "Law, Contracts & Everyday Rights": "LAW",
}


def slug_for(pack):
    if pack in PACK_SLUGS:
        return PACK_SLUGS[pack]
    ascii_name = unicodedata.normalize("NFKD", pack).encode("ascii", "ignore").decode()
    words = re.findall(r"[A-Za-z0-9]+", ascii_name)
    return ("".join(w[0] for w in words).upper() or "PACK")[:8]


def read_rows():
    paths = [SOURCE] + sorted(GENERATED.glob("*.csv")) if GENERATED.is_dir() else [SOURCE]
    rows = []
    for path in paths:
        with open(path, newline="", encoding="utf-8") as f:
            rows.extend(csv.DictReader(f))
    return rows


def main():
    rows = read_rows()
    counters = {}
    for r in rows:
        slug = slug_for(r["pack"])
        counters[slug] = counters.get(slug, 0) + 1
        r_id = f"CX-{slug}-{counters[slug]:04d}"
        r_new = OrderedDict(block_id=r_id)
        r_new.update(r)
        r.clear()
        r.update(r_new)

    fields = ["block_id", "pack", "track", "code", "grade", "level",
              "credential", "theme", "description", "transfer_check"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    packs = OrderedDict()
    for r in rows:
        p = packs.setdefault(r["pack"], {
            "slug": slug_for(r["pack"]),
            "blocks": 0,
            "tracks": OrderedDict(),
            "credentials": OrderedDict(),
            "grades": OrderedDict(),
        })
        p["blocks"] += 1
        if r["track"]:
            p["tracks"][r["track"]] = p["tracks"].get(r["track"], 0) + 1
        p["credentials"][r["credential"]] = None
        p["grades"][r["grade"]] = None
    manifest = {
        "dataset": "Cognition.X blocks",
        "total_blocks": len(rows),
        "packs": [
            {
                "name": name,
                "slug": p["slug"],
                "blocks": p["blocks"],
                "tracks": list(p["tracks"]),
                "credentials": len(p["credentials"]),
                "grade_bands": list(p["grades"]),
            }
            for name, p in packs.items()
        ],
    }
    with open(OUT_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"wrote {OUT_CSV.name}: {len(rows)} blocks across {len(packs)} packs")


if __name__ == "__main__":
    main()
