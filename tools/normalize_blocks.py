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
PROMOTIONS = ROOT / "data" / "promotions"
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
    "Civic Leadership Legacy : Louisiana": "LEGACYLA",
    "Civic Leadership Legacy : California": "LEGACYCA",
    "Civic Leadership Legacy : Texas": "LEGACYTX",
    "Cognition.X : Louisiana OS": "LAOS",
    "Cognition.X : Education OS": "EDUOS",
    "Civic Leadership Legacy : The Institute Model": "LEGACYMODEL",
    "SmartCiti.X : New Orleans Trades": "NOLATRADES",
    "Parish Launch & Scale": "LAUNCH",
    "Trades in the Classroom : Flipped & Gamified": "TRADESCLASS",
    "Trades Across School Subjects": "TRADESUBJ",
    "Learning States & Universal Access": "ACCESS",
    "Cognition.X : States OS": "STATEOS",
    "Music : Creation to Industry": "MUSICIND",
    "Culinary Trades : The Louisiana Kitchen": "CULINARY",
    "Arts & Craft Trades : Louisiana Makers": "ARTCRAFT",
}


def slug_for(pack):
    if pack in PACK_SLUGS:
        return PACK_SLUGS[pack]
    ascii_name = unicodedata.normalize("NFKD", pack).encode("ascii", "ignore").decode()
    words = re.findall(r"[A-Za-z0-9]+", ascii_name)
    return ("".join(w[0] for w in words).upper() or "PACK")[:8]


def assert_unique_slugs(rows):
    """The slug is the key four builders group by, and the middle field of
    every block_id. Two packs sharing one would keep ids unique — so every
    validator would pass — while silently merging the two packs into one
    everywhere downstream. Names are the source of truth; collisions are a
    build error, not a warning."""
    by_slug = {}
    for r in rows:
        by_slug.setdefault(slug_for(r["pack"]), set()).add(r["pack"])
    clashes = {s: sorted(p) for s, p in by_slug.items() if len(p) > 1}
    if clashes:
        lines = "; ".join(f"{s} <- {' + '.join(p)}" for s, p in sorted(clashes.items()))
        raise SystemExit(
            "slug collision: two packs would share one slug and merge silently "
            f"in every slug-keyed builder ({lines}). Give each an explicit entry "
            "in PACK_SLUGS.")


def read_rows():
    paths = [SOURCE] + sorted(GENERATED.glob("*.csv")) if GENERATED.is_dir() else [SOURCE]
    rows = []
    for path in paths:
        with open(path, newline="", encoding="utf-8") as f:
            rows.extend(csv.DictReader(f))
    return rows


BANDS = ["K–2", "3–5", "6–8", "9–10", "11–12"]
BAND_LEVEL = {"K–2": "Explorer", "3–5": "Explorer", "6–8": "Builder",
              "9–10": "Practitioner", "11–12": "Lead"}


# The two generic sentences the source uses where no real transfer check
# was authored. These, and ONLY these, may be replaced by a promotion's
# authored `transfer_check` — any other source check is real content and
# is never overwritten.
PLACEHOLDER_CHECKS = {
    "Demonstrate it once, correctly, to somebody who will use it",
    "Do it once, for real, and show it to somebody who will use it",
}


def apply_promotions(rows):
    """Fill empty track/code/level/description on legacy rows from
    data/promotions/*.json (keyed by exact theme text; empty fields only),
    and replace known-placeholder transfer checks with authored ones."""
    if not PROMOTIONS.is_dir():
        return
    promos = {}
    for path in sorted(PROMOTIONS.glob("*.json")):
        spec = json.loads(path.read_text(encoding="utf-8"))
        themap = {}
        for track in spec["tracks"]:
            for i, th in enumerate(track["themes"]):
                themap[th["theme"]] = (track["name"], track["prefix"], i,
                                       th["description"], th.get("transfer_check"))
        promos[spec["pack"]] = themap
    filled = checks = 0
    for r in rows:
        themap = promos.get(r["pack"])
        if not themap or r["track"] or r["theme"] not in themap or r["grade"] not in BAND_LEVEL:
            continue
        name, prefix, ti, desc, check = themap[r["theme"]]
        bi = BANDS.index(r["grade"])
        r["track"] = name
        r["code"] = r["code"] or f"{prefix}-{ti*5 + bi + 1}"
        r["level"] = r["level"] or BAND_LEVEL[r["grade"]]
        r["description"] = r["description"] or f"{desc} — at {r['grade']}"
        filled += 1
        if check and r["transfer_check"] in PLACEHOLDER_CHECKS:
            r["transfer_check"] = check
            checks += 1
    if filled:
        print(f"promotions: filled {filled} legacy rows from {len(promos)} pack(s)"
              + (f"; replaced {checks} placeholder transfer checks" if checks else ""))


# Level derivation for foundation-library rows that use single grades,
# adult bands, or capstone markers instead of the five standard bands.
GRADE_LEVEL = {
    **BAND_LEVEL,
    "K": "Explorer", "1": "Explorer", "2": "Explorer",
    "3": "Explorer", "4": "Explorer", "5": "Explorer",
    "6": "Builder", "7": "Builder", "8": "Builder",
    "9": "Practitioner", "10": "Practitioner",
    "11": "Lead", "12": "Lead",
    "9–12 · adult": "Lead", "11–12 · adult": "Lead",
    "—": "Lead",  # Trade School capstones
}


def light_fill(rows):
    """Structural completion for the irregular foundation packs: every row
    gets a code (LB-<n>, unique within its pack) and a level derived from
    its grade. track and description are content work and stay deferred —
    empty fields only; nothing is overwritten."""
    counters = {}
    coded = leveled = 0
    for r in rows:
        if not r["code"]:
            counters[r["pack"]] = counters.get(r["pack"], 0) + 1
            r["code"] = f"LB-{counters[r['pack']]}"
            coded += 1
        if not r["level"]:
            level = GRADE_LEVEL.get(r["grade"])
            if level:
                r["level"] = level
                leveled += 1
    if coded or leveled:
        print(f"light fill: assigned {coded} codes and {leveled} levels on foundation rows")


def main():
    rows = read_rows()
    assert_unique_slugs(rows)
    apply_promotions(rows)
    light_fill(rows)
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
