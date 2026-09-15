#!/usr/bin/env python3
"""Build the Cognition.X Louisiana platform from the dataset + app fact base.

Inputs:
  - the parish/region/wave fact base embedded in the Education OS app
    (extracted verbatim into this script's PARISH_JS block source at
    apps/education-os/index.html: DATA.regions / DATA.regionHubs /
    DATA.parishes)
  - data/blocks.csv for curriculum stats and the Louisiana legacy pack
  - VERSION

Output: apps/louisiana/index.html from apps/louisiana/template.html
(placeholder __LADATA__). Like Flow Hub, the app is a build product —
never hand-edited.
"""

import csv
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Stylized tile-cartogram positions [row, col] — approximate geography,
# north (row 0) to gulf, west (col 0) to east. A map of tiles, not borders.
POS = {
    "Caddo": (0, 0), "Bossier": (0, 1), "Webster": (0, 2), "Claiborne": (0, 3),
    "Union": (0, 4), "Morehouse": (0, 5), "West Carroll": (0, 6), "East Carroll": (0, 7),
    "DeSoto": (1, 0), "Red River": (1, 1), "Bienville": (1, 2), "Lincoln": (1, 3),
    "Jackson": (1, 4), "Ouachita": (1, 5), "Richland": (1, 6), "Madison": (1, 7),
    "Sabine": (2, 0), "Natchitoches": (2, 1), "Winn": (2, 2), "Caldwell": (2, 4),
    "Franklin": (2, 5), "Tensas": (2, 6),
    "Vernon": (3, 0), "Rapides": (3, 1), "Grant": (3, 2), "LaSalle": (3, 3),
    "Catahoula": (3, 4), "Concordia": (3, 5),
    "Beauregard": (4, 0), "Allen": (4, 1), "Evangeline": (4, 2), "Avoyelles": (4, 3),
    "Pointe Coupee": (4, 4), "West Feliciana": (4, 5), "East Feliciana": (4, 6),
    "St. Helena": (4, 7), "Tangipahoa": (4, 8), "Washington": (4, 9),
    "Calcasieu": (5, 0), "Jefferson Davis": (5, 1), "Acadia": (5, 2), "St. Landry": (5, 3),
    "West Baton Rouge": (5, 4), "East Baton Rouge": (5, 5), "Livingston": (5, 6),
    "St. Tammany": (5, 8),
    "Cameron": (6, 0), "Vermilion": (6, 1), "Lafayette": (6, 2), "St. Martin": (6, 3),
    "Iberville": (6, 4), "Ascension": (6, 5), "St. James": (6, 6),
    "St. John the Baptist": (6, 7), "St. Charles": (6, 8), "Orleans": (6, 9),
    "St. Bernard": (6, 10),
    "Iberia": (7, 2), "St. Mary": (7, 3), "Assumption": (7, 4), "Lafourche": (7, 5),
    "Jefferson": (7, 8), "Plaquemines": (7, 9),
    "Terrebonne": (8, 4),
}

WAVE_YEARS = ["2027–28", "2028–29", "2029–30", "2030–31"]

# The adopted rollout: a two-year, two-wave plan. Wave 1 (2026–27) takes 33
# parishes — every parish from the original proposal's waves 1–2 plus the
# largest wave-3 parishes — reaching ~88% of the state's population in year
# one; Wave 2 (2027–28) takes the remaining 31. The original 4-wave phasing
# above is kept as proposal provenance on every parish.
ACC_YEARS = ["2026–27", "2027–28"]
ACC_WAVE1_SIZE = 33


def adopted_waves(parishes):
    """Assign each parish dict an accWave (1 or 2) under the adopted plan.

    Deterministic rule: order by (original proposal wave, population desc,
    name); the first 33 launch in Wave 1. Mutates in place."""
    order = sorted(parishes, key=lambda p: (p["wave"], -p["pop"], p["name"]))
    for i, p in enumerate(order):
        p["accWave"] = 1 if i < ACC_WAVE1_SIZE else 2

# Industry-phrase → curriculum-pack mapping. Each parish's anchor-industry
# phrases (from the fact base) are matched against these rules to build its
# module plan; the matching phrase is kept as the human-readable reason.
CORE_PACKS = ["K12", "LAOS", "LEGACYLA", "LIFESKILL", "EMERGENCY", "LAUNCH"]
INDUSTRY_RULES = [
    (r"LNG|oil|gas|petrochemical|chemical|hydrogen|carbon|energy|hydro|refin|pipeline|grid",
     ["ENERGY", "ROB"]),
    (r"rice|sugar|agricult|ag-tech|poultry|catfish|timber|forestry|farm|aquaculture|food|seafood|fisher",
     ["WLC", "FOOD"]),
    (r"health", ["PREVCARE", "GHEALTH"]),
    (r"cyber|logistics|aerospace|manufactur|film|automation|robot",
     ["ROB", "DIGITAL"]),
    (r"port|marine|river|coastal|shipbuild|terminal", ["TRANSPORT", "EMERGENCY"]),
    (r"corrections", ["REENTRY"]),
    (r"casino|hospitality|tourism|culture|music", ["CORP", "ARTS"]),
    # the culture trades (v0.48.0): kitchens where people are fed, and
    # the arts and music trades where a parish's culture is the industry
    (r"hospitality|tourism|casino|restaurant|food|seafood|meat|crawfish|oyster|shrimp", ["CULINARY"]),
    (r"film|music|culture\b|cultural|festival|arts", ["MUSICIND", "ARTCRAFT"]),
    (r"military|Fort |AFB|Barksdale", ["EMERGENCY", "ROB"]),
    (r"government|research|universit|LSU|Southern|SOWELA", ["SCI", "LEGACYLA"]),
    (r"restoration", ["WLC", "EMERGENCY"]),
]


def match_packs(industries):
    """Return [(slug, reason-phrase)] for a parish's industry text."""
    out = []
    seen = set()
    # split on commas/semicolons, but never inside parentheses
    for phrase in re.split(r"[,;]\s*(?![^()]*\))", industries):
        phrase = phrase.strip()
        if not phrase:
            continue
        for pat, slugs in INDUSTRY_RULES:
            if re.search(pat, phrase, re.IGNORECASE):
                for s in slugs:
                    if s not in seen:
                        seen.add(s)
                        out.append([s, phrase])
    return out


def parish_missions(name, seat, world, hub, rural):
    """Generate the parish's custom mission module: a five-rung ladder
    localized to its narrative world from the fact base. These are
    generated scaffolds (deterministic, template-based) — the parish's
    custom capstone layer over the universal dataset, labeled as such
    in the app."""
    offline = (" The module runs fully offline — paper logs and physical models count as evidence."
               if rural else "")
    return [
        {"band": "K–2 · 3–5", "level": "Explorer",
         "title": f"The {world}, seen whole",
         "task": f"Visit or study the {world} setting near {seat}; name its five working parts and draw its flow from arrival to output."},
        {"band": "6–8", "level": "Builder",
         "title": f"Model the {world}",
         "task": f"Build or simulate a working model of the {world} and demonstrate one measured improvement over your first version." + offline},
        {"band": "9–10", "level": "Practitioner",
         "title": f"Inside the real {world}",
         "task": f"Complete a supervised visit, placement or data collection connected to the {world}, and keep a real observation log a stranger could learn from."},
        {"band": "11–12", "level": "Lead",
         "title": f"Improving the {world}",
         "task": f"Propose one evidenced improvement to the {world} operation and present it to a real audience at the parish hall or the {hub} Trade Hall."},
        {"band": "12 · capstone", "level": "Lead",
         "title": f"Teaching the {world}",
         "task": f"Teach this module's core process to a younger {name} Parish cohort, with their demonstration as your evidence."},
    ]


def load_fact_base():
    """The Louisiana and Institute fact bases, canonical in data/ since
    v0.39.0 (extracted once from the Education OS app by
    tools/extract_fact_bases.py; re-run that tool if the app's copy is
    ever edited)."""
    fb = json.loads((ROOT / "data" / "louisiana" / "fact_base.json")
                    .read_text(encoding="utf-8"))
    w = json.loads((ROOT / "data" / "wlb" / "institute.json")
                   .read_text(encoding="utf-8"))
    return {
        "regions": fb["regions"], "hubs": fb["regionHubs"],
        "parishes": fb["parishes"],
        "wlb": {k: w[k] for k in ("org", "disclaimer", "mission", "quote", "record")},
        "principles": [{"p": x["p"], "src": x["src"], "teach": x["teach"]}
                       for x in w["principles"]],
        # the Institute's full leadership curriculum (canonical since v0.43.0)
        "leadership": {k: w[k] for k in ("name", "fellowshipQuote", "fellowship",
                                         "k12", "strands", "eras", "courses",
                                         "bridge", "modules", "standards", "seal")},
        # the Louisiana K-12 program (canonical since v0.44.0)
        "k12program": json.loads((ROOT / "data" / "louisiana" / "k12_program.json")
                                 .read_text(encoding="utf-8")),
        # the Makers' Hall: public-record makers, role ladders and
        # organisations for the three culture-trade packs (v0.48.0)
        "makers": json.loads((ROOT / "data" / "louisiana" / "makers.json")
                             .read_text(encoding="utf-8")),
    }


def la_compliance():
    """Louisiana's entry of the 50-state compliance layer (v0.51.0) with the
    national baseline and domain list — for the State Admin dashboard."""
    c = json.loads((ROOT / "data" / "states" / "compliance.json").read_text(encoding="utf-8"))
    la = next(s for s in c["states"] if s["abbr"] == "LA")
    return {"asOf": c["asOf"], "disclaimer": c["disclaimer"], "domains": c["domains"],
            "national": c["national"], "state": la}


def maker_packs(makers, parish):
    """[(slug, reason)] — a parish whose public-record makers worked a
    discipline earns that discipline's trade pack in its module plan."""
    out = []
    for d in makers["disciplines"]:
        n = sum(1 for f in d["figures"] if f["parish"] == parish)
        if n:
            out.append([d["pack"], f"{n} {d['name'].lower()} maker{'s' if n > 1 else ''} on the public record"])
    return out


def pack_catalog():
    """slug → {name, tracks:[{name,prefix,credential}]} for every pack,
    from the canonical dataset (block_id carries the slug)."""
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    cat = OrderedDict()
    for r in rows:
        slug = r["block_id"].split("-")[1]
        p = cat.setdefault(slug, {"name": r["pack"], "blocks": 0, "tracks": OrderedDict()})
        p["blocks"] += 1
        if r["track"] and r["track"] not in p["tracks"]:
            p["tracks"][r["track"]] = {"name": r["track"],
                                       "prefix": r["code"].rsplit("-", 1)[0],
                                       "credential": r["credential"]}
    for p in cat.values():
        p["tracks"] = list(p["tracks"].values())
    return cat


def curriculum_stats():
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    packs = OrderedDict()
    for r in rows:
        packs.setdefault(r["pack"], []).append(r)
    la = packs.get("Civic Leadership Legacy : Louisiana", [])
    la_tracks = OrderedDict()
    for r in la:
        if r["track"] and r["track"] not in la_tracks:
            la_tracks[r["track"]] = r["credential"]
    model = packs.get("Civic Leadership Legacy : The Institute Model", [])
    model_tracks = OrderedDict()
    for r in model:
        if r["track"] and r["track"] not in model_tracks:
            model_tracks[r["track"]] = r["credential"]
    tracked_tracks = len({(r["pack"], r["track"]) for r in rows if r["track"]})
    return {
        "blocks": len(rows),
        "packs": len(packs),
        "tracks": tracked_tracks,
        "credentials": len({r["credential"] for r in rows}),
        "laTracks": [{"name": k, "credential": v} for k, v in la_tracks.items()],
        "modelTracks": [{"name": k, "credential": v} for k, v in model_tracks.items()],
        "communityPacks": [p for p, pr in packs.items()
                           if pr[0]["track"] and len(pr) == 250 and not p.startswith("Civic Leadership")],
    }


def hall_unions():
    """Trade-union slices of the Trades Network fact base for the Louisiana
    Trade Halls that anchor a network region — keyed by hub city name, with
    sims localized to that region's ground."""
    fb = json.loads((ROOT / "data" / "unions" / "trade_unions.json")
                    .read_text(encoding="utf-8"))
    hubs = {"New Orleans": "nola", "Baton Rouge": "br"}
    out = {}
    for hub, rid in hubs.items():
        reg = next(r for r in fb["regions"] if r["id"] == rid)
        entries = []
        for fam in fb["families"]:
            intl = fam.get("intl_by_region", {}).get(rid, fam["intl"])
            entries.append({
                "family": fam["family"], "intl": intl, "kind": fam["kind"],
                "sim": fam["sim"].replace("{site}", reg["sites"][fam["kind"]]),
                "packs": fam["packs"],
            })
        out[hub] = {"region": reg["name"], "council": reg["council"],
                    "districts": reg["districts"], "entries": entries}
    return out


def learner_types():
    """The 20 access profiles (support preferences, never diagnoses) that
    drive the flow-state automations and access guidance."""
    return json.loads((ROOT / "data" / "learners" / "learner_types.json")
                      .read_text(encoding="utf-8"))


def main():
    fb = load_fact_base()
    missing = [p[0] for p in fb["parishes"] if p[0] not in POS]
    if missing:
        raise SystemExit(f"parishes without tile positions: {missing}")

    catalog = pack_catalog()
    used_slugs = set(CORE_PACKS)
    parishes = []
    for name, region, seat, pop_k, wave, districts, industries, world, rural in fb["parishes"]:
        r, c = POS[name]
        matched = match_packs(industries)
        have = {s for s, _ in matched}
        matched += [m for m in maker_packs(fb["makers"], name) if m[0] not in have]
        used_slugs.update(s for s, _ in matched)
        parishes.append({
            "name": name, "region": region, "seat": seat, "pop": pop_k,
            "wave": wave, "districts": districts, "industries": industries,
            "world": world, "rural": rural, "row": r, "col": c,
            "packs": matched,
            "missions": parish_missions(name, seat, world, fb["hubs"][region], rural),
        })
    adopted_waves(parishes)
    # the Makers' Hall links every culture-trade track, matched or not
    used_slugs.update(d["pack"] for d in fb["makers"]["disciplines"])
    packmeta = {s: catalog[s] for s in sorted(used_slugs) if s in catalog}
    # full catalog (light) so the plan customizer can offer every pack
    catalog_light = {s: {"name": c["name"], "blocks": c["blocks"],
                         "ntracks": len(c["tracks"])} for s, c in catalog.items()}

    payload = {
        "version": (ROOT / "VERSION").read_text().strip(),
        "regions": fb["regions"], "hubs": fb["hubs"],
        "waveYears": WAVE_YEARS,
        "accYears": ACC_YEARS,
        "parishes": parishes,
        "curriculum": curriculum_stats(),
        "wlb": fb["wlb"],
        "principles": fb["principles"],
        "leadership": fb["leadership"],
        "k12program": fb["k12program"],
        "makers": fb["makers"],
        "compliance": la_compliance(),
        "corePacks": CORE_PACKS,
        "packmeta": packmeta,
        "catalog": catalog_light,
        "unions": hall_unions(),
        "access": learner_types(),
    }
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = (ROOT / "apps" / "louisiana" / "template.html").read_text(encoding="utf-8")
    if "__LADATA__" not in template:
        raise SystemExit("template.html is missing the __LADATA__ placeholder")
    out = ROOT / "apps" / "louisiana" / "index.html"
    out.write_text(template.replace("__LADATA__", data), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}: {out.stat().st_size/1e3:.0f} KB "
          f"({len(parishes)} parishes, {len(payload['curriculum']['laTracks'])} LA tracks)")


if __name__ == "__main__":
    main()
