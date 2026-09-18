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
LEVEL_WORDS = {"Explorer", "Builder", "Practitioner", "Lead"}

PLACEHOLDER_CHECKS = {
    "Demonstrate it once, correctly, to somebody who will use it",
    "Do it once, for real, and show it to somebody who will use it",
}


SUFFIX_RE = re.compile(r"^(?P<shared>.+?) — at (?P<band>K–2|3–5|6–8|9–10|11–12)$")


def override_description(row, bands):
    """The second deliberate exception to fill-empty-only (v0.72.0): a
    promotion declaring `"override": "band-suffix"` may replace a NON-EMPTY
    description, but only one that is the documented content debt — the
    shared sentence with its "— at <band>" suffix, for the row's own band —
    and only with the authored sentence for that band. Anything else is
    refused with the row id, so an authored source sentence can never be
    overwritten. Returns the new description or None when the row is not a
    suffix row (already authored, or empty: the fill-empty path owns those)."""
    m = SUFFIX_RE.match(row["description"].strip())
    if not m:
        if row["description"].strip():
            raise SystemExit(f"override refused: {row['block_id'] if 'block_id' in row else row['code']} "
                             f"({row['pack']!r}, theme {row['theme']!r}) carries an authored description, not a band suffix")
        return None
    if m.group("band") != row["grade"]:
        raise SystemExit(f"override refused: {row.get('block_id', row['code'])} suffix names {m.group('band')!r} but the row's band is {row['grade']!r}")
    if sorted(bands) != sorted(BANDS) or len({str(bands[b]).strip() for b in BANDS}) != 5 or any(not str(bands[b]).strip() for b in BANDS):
        raise SystemExit(f"promotion {row['pack']!r}, theme {row['theme']!r}: bands must name the five bands with five distinct non-empty sentences")
    if any(" — at " in str(bands[b]) for b in BANDS):
        raise SystemExit(f"promotion {row['pack']!r}, theme {row['theme']!r}: a band sentence must not carry the '— at <band>' suffix")
    return str(bands[row["grade"]]).strip()


def unbanded_description(desc):
    """Validate a plain fill sentence for an `"unbanded": true` promotion
    theme (see apply_promotions): the row is the only occurrence of its
    theme at its grade, so the sentence stands alone with no per-band
    suffix. Returns the trimmed sentence, or None if it fails the check."""
    d = str(desc).strip()
    if len(d) < 40 or not d.endswith(".") or " — at " in d:
        return None
    return d


def partial_band_description(bands, grade):
    """Validate a `"partial_bands": true` promotion theme's sentence for one
    grade (see apply_promotions): the theme's rows span only some of the
    five bands — a sliding, sometimes wrap-around window of three or four —
    so `bands` carries only the keys the theme actually has rows at, each a
    complete standalone sentence for a learner at that one grade, with no
    suffix. Returns the trimmed sentence for `grade`, or None if `grade`
    has no authored sentence or the sentence fails the check."""
    if not isinstance(bands, dict) or grade not in bands:
        return None
    d = str(bands[grade]).strip()
    if len(d) < 40 or not d.endswith(".") or " — at " in d:
        return None
    return d


def apply_promotions(rows):
    """Fill empty track/code/level/description on legacy rows from
    data/promotions/*.json (keyed by exact theme text; empty fields only),
    and replace known-placeholder transfer checks with authored ones. A
    promotion declaring `"override": "band-suffix"` additionally replaces
    band-suffixed descriptions on rows that already carry a track — see
    override_description() for the rule and the refusals.

    A promotion declaring `"unbanded": true` is for a foundation pack where
    each theme names exactly one row at one grade, not five rows spanning
    the band ladder (Future-Work, Civic & Leadership, etc.). There, a
    theme's `description` is filled in as the row's complete sentence with
    no "— at <band>" suffix — appending one would be meaningless (the
    grade is already the row's own column) and would recreate the exact
    band-suffix content debt the override mechanism exists to remove. This
    is still plain fill-empty, not a new counted exception: the field
    starts empty and stays that way until a promotion supplies it.

    A promotion declaring `"partial_bands": true` is for a foundation pack
    where each theme's rows span only SOME of the five bands — a sliding,
    sometimes wrap-around window of three or four (Empathy & Emotional
    Intelligence, Community & Relationship Practice) — rather than all
    five (the original `bands` mechanism) or exactly one (`unbanded`).
    There, a theme's `bands` carries only the keys it actually has rows
    at; each grade's row is filled from that grade's own sentence, with
    no suffix. Also plain fill-empty, and `track`/`code` are left
    deferred for the same tracked-shape reason as `unbanded`.

    Grade filter (v0.95.0): rows are eligible whenever their `grade` is in
    `GRADE_LEVEL`, not just the five standard `BANDS` — this reaches K–12,
    Trade School and Regional's single-grade and adult-route rows, and
    Health & Community's two `—`-grade capstones, none of which fit in
    `BAND_LEVEL`. Those packs use `unbanded` (one sentence per theme; a
    theme repeated verbatim across several rows, as Regional's four
    cross-region themes are, still gets that one sentence on every row)."""
    if not PROMOTIONS.is_dir():
        return
    promos, overriders, overmap, unbanded, partial_bands_packs = {}, {}, {}, set(), set()
    for path in sorted(PROMOTIONS.glob("*.json")):
        spec = json.loads(path.read_text(encoding="utf-8"))
        themap = {}
        for track in spec["tracks"]:
            for i, th in enumerate(track["themes"]):
                themap[th["theme"]] = (track["name"], track["prefix"], i,
                                       th.get("description", ""), th.get("transfer_check"),
                                       track.get("credential"), th.get("bands"))
                # override rows already carry a track, so a theme name that two
                # tracks share (the Multilateral OS has one) resolves per track
                overmap[(spec["pack"], track["name"], th["theme"])] = th.get("bands")
        # A pack can be the target of more than one promotion file (v0.99.0):
        # the sector-OS packs already carry a "band-suffix" override promotion
        # from prompt 2, and prompt 3 adds a second, unbanded promotion for
        # the same pack's still-empty foundation rows. Merge themaps across
        # files targeting the same pack; a theme both files promote is a real
        # authoring conflict (ambiguous which sentence wins), not something to
        # silently resolve by file order, so it's refused loudly.
        existing = promos.setdefault(spec["pack"], {})
        collide = set(existing) & set(themap)
        if collide:
            raise SystemExit(f"{path.name}: theme(s) already promoted for pack {spec['pack']!r} by another promotion file: {sorted(collide)[:5]}")
        existing.update(themap)
        if spec.get("override"):
            if spec["override"] != "band-suffix":
                raise SystemExit(f"{path.name}: the only override kind is \"band-suffix\", got {spec['override']!r}")
            if not all(th.get("bands") for t in spec["tracks"] for th in t["themes"]):
                raise SystemExit(f"{path.name}: an override promotion must carry bands on every theme")
            overriders[spec["pack"]] = path.name
        if spec.get("unbanded"):
            if any(th.get("bands") for t in spec["tracks"] for th in t["themes"]):
                raise SystemExit(f"{path.name}: an unbanded promotion may not carry bands (one row per theme already names the grade)")
            unbanded.add(spec["pack"])
        if spec.get("partial_bands"):
            if spec.get("unbanded") or spec.get("override"):
                raise SystemExit(f"{path.name}: partial_bands cannot combine with unbanded or override")
            for t in spec["tracks"]:
                for th in t["themes"]:
                    b = th.get("bands")
                    if not b or not set(b) <= set(BANDS) or len(b) >= len(BANDS):
                        raise SystemExit(f"{path.name}: a partial_bands theme must carry a non-empty, incomplete subset of {BANDS}: {th['theme']!r}")
                    if len({str(v).strip() for v in b.values()}) != len(b) or any(not str(v).strip() for v in b.values()):
                        raise SystemExit(f"{path.name}: a partial_bands theme's sentences must be distinct and non-empty: {th['theme']!r}")
            partial_bands_packs.add(spec["pack"])
    filled = checks = creds = overrode = 0
    for r in rows:
        themap = promos.get(r["pack"])
        if themap and r["track"] and r["pack"] in overriders and (r["pack"], r["track"], r["theme"]) in overmap and r["grade"] in BAND_LEVEL:
            new = override_description(r, overmap[(r["pack"], r["track"], r["theme"])])
            if new is not None:
                r["description"] = new
                overrode += 1
            continue
        if not themap or r["track"] or r["theme"] not in themap or r["grade"] not in GRADE_LEVEL:
            continue
        name, prefix, ti, desc, check, cred, bands = themap[r["theme"]]
        is_unbanded = r["pack"] in unbanded
        is_partial = r["pack"] in partial_bands_packs
        if not is_unbanded and not is_partial:
            # An unbanded or partial_bands promotion's themes are grouped for
            # the file's own readability only: neither forms a 10-theme,
            # 50-block track, so filling `track`/`code` here would create a
            # track that fails the tracked-shape check in test_dataset().
            # Those two stay deferred; light_fill() still assigns `code` and
            # `level` structurally, exactly as it does for every foundation
            # row that receives no promotion at all. bi only makes sense for
            # the standard five-band mechanism, whose grades are always in
            # BANDS by construction.
            bi = BANDS.index(r["grade"])
            r["track"] = name
            r["code"] = r["code"] or f"{prefix}-{ti*5 + bi + 1}"
            r["level"] = r["level"] or BAND_LEVEL[r["grade"]]
        # a promotion theme may carry per-band sentences (`bands`, the same
        # shape and rules as a pack spec's); otherwise the shared sentence
        # takes the documented "— at <band>" suffix
        if not r["description"]:
            if is_partial:
                d = partial_band_description(bands, r["grade"])
                if d is None:
                    raise SystemExit(f"partial_bands promotion {r['pack']!r}, theme {r['theme']!r}: no valid sentence authored for grade {r['grade']!r}")
                r["description"] = d
            elif bands:
                if sorted(bands) != sorted(BANDS) or len({str(bands[b]).strip() for b in BANDS}) != 5 or any(not str(bands[b]).strip() for b in BANDS):
                    raise SystemExit(f"promotion {r['pack']!r}, theme {r['theme']!r}: bands must name the five bands with five distinct non-empty sentences")
                r["description"] = str(bands[r["grade"]]).strip()
            elif is_unbanded:
                d = unbanded_description(desc)
                if d is None:
                    raise SystemExit(f"unbanded promotion {r['pack']!r}, theme {r['theme']!r}: description must be a complete sentence with no suffix: {str(desc)[:60]!r}")
                r["description"] = d
            else:
                r["description"] = f"{desc} — at {r['grade']}"
        filled += 1
        if check and r["transfer_check"] in PLACEHOLDER_CHECKS:
            r["transfer_check"] = check
            checks += 1
        # The one deliberate exception to fill-empty-only: a track's
        # `credential` in a promotion replaces a bare level word ("Practitioner")
        # that the v0.1.0 import used where a credential name belonged. A real
        # credential name is never overwritten. Counted and printed so the
        # correction is always visible (docs/DATA_REVIEW.md, Finding 6).
        if cred and r["credential"].strip() in LEVEL_WORDS:
            r["credential"] = cred
            creds += 1
    if filled:
        print(f"promotions: filled {filled} legacy rows from {len(promos)} pack(s)"
              + (f"; replaced {checks} placeholder transfer checks" if checks else "")
              + (f"; corrected {creds} level-word credentials to the promotion's named credential" if creds else ""))
    if overrode:
        print(f"promotions: overrode {overrode} band-suffix descriptions with authored band sentences "
              f"({', '.join(sorted(overriders.values()))}) — the counted exception, docs/DATA_QUALITY.md")


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
