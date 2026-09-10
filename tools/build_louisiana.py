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


def extract_fact_base():
    """The fact base lives as JS array literals inside the Education OS app;
    evaluate them with node (strings/numbers/booleans only) to get JSON."""
    import subprocess
    import tempfile
    t = (ROOT / "apps" / "education-os" / "index.html").read_text(
        encoding="utf-8", errors="replace")

    def grab(name):
        i = t.find(name + "=")
        j = t.find("];", i)
        return t[i + len(name) + 1: j + 1]

    js = ("const regions=" + grab("DATA.regions") + ";"
          "const hubs=" + grab("DATA.regionHubs") + ";"
          "const parishes=" + grab("DATA.parishes") + ";"
          "console.log(JSON.stringify({regions,hubs,parishes}));")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(js)
        path = f.name
    out = subprocess.run(["node", path], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


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
    tracked_tracks = len({(r["pack"], r["track"]) for r in rows if r["track"]})
    return {
        "blocks": len(rows),
        "packs": len(packs),
        "tracks": tracked_tracks,
        "credentials": len({r["credential"] for r in rows}),
        "laTracks": [{"name": k, "credential": v} for k, v in la_tracks.items()],
        "communityPacks": [p for p, pr in packs.items()
                           if pr[0]["track"] and len(pr) == 250 and not p.startswith("Civic Leadership")],
    }


def main():
    fb = extract_fact_base()
    missing = [p[0] for p in fb["parishes"] if p[0] not in POS]
    if missing:
        raise SystemExit(f"parishes without tile positions: {missing}")

    parishes = []
    for name, region, seat, pop_k, wave, districts, industries, world, rural in fb["parishes"]:
        r, c = POS[name]
        parishes.append({
            "name": name, "region": region, "seat": seat, "pop": pop_k,
            "wave": wave, "districts": districts, "industries": industries,
            "world": world, "rural": rural, "row": r, "col": c,
        })

    payload = {
        "version": (ROOT / "VERSION").read_text().strip(),
        "regions": fb["regions"], "hubs": fb["hubs"],
        "waveYears": WAVE_YEARS,
        "parishes": parishes,
        "curriculum": curriculum_stats(),
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
