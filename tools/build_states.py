#!/usr/bin/env python3
"""Build the Cognition.X States app: custom curriculum for all 50 states.

Crosses the 50-state fact base (data/states/states.json) with:
  - the Cognition.X : States OS blueprint pack (five universal tracks,
    localized per state by its water / corridor / table / culture / storm
    anchors),
  - the Civic Leadership Legacy : The Institute Model pack (the universal
    leadership + civics + EQ tracks, localized by capital and legislature),
  - the Willie L. Brown Jr. Institute principles carried by the Education
    OS app's fact base (extracted from apps/education-os/template.html,
    exactly as the Louisiana build does) — the Education OS remains the
    seed of the state model.

Output: apps/states/index.html from apps/states/template.html
(placeholder __STDATA__). A build product — never hand-edited.
"""

import csv
import json
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATES = ROOT / "data" / "states" / "states.json"
BLOCKS = ROOT / "data" / "blocks.csv"
TEMPLATE = ROOT / "apps" / "states" / "template.html"
OUT = ROOT / "apps" / "states" / "index.html"

CORE_PACKS = ["K12", "LIFESKILL", "EMERGENCY", "LAUNCH", "ACCESS"]


def pack_catalog():
    cat = OrderedDict()
    with open(BLOCKS, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            slug = r["block_id"].split("-")[1]
            p = cat.setdefault(slug, {"name": r["pack"], "blocks": 0,
                                      "tracks": OrderedDict()})
            p["blocks"] += 1
            if r["track"] and r["track"] not in p["tracks"]:
                p["tracks"][r["track"]] = r["credential"]
    for p in cat.values():
        p["tracks"] = [{"name": n, "credential": c} for n, c in p["tracks"].items()]
    return cat


def wlb_fact_base():
    """The Institute fact base, canonical in data/wlb/institute.json since
    v0.39.0 (extracted once from the Education OS app by
    tools/extract_fact_bases.py)."""
    w = json.loads((ROOT / "data" / "wlb" / "institute.json")
                   .read_text(encoding="utf-8"))
    return {
        "wlb": {k: w[k] for k in ("org", "disclaimer", "mission", "quote")},
        "principles": [{"p": x["p"], "teach": x["teach"]} for x in w["principles"]],
        # the Leadership Ladder headline (full ladder lives in the Louisiana app)
        "leadership": {
            "strands": [{"id": s["id"], "t": s["t"], "d": s["d"]} for s in w["strands"]],
            "eras": w["eras"], "seal": w["seal"],
            "counts": {"courses": sum(len(v2) for v in w["courses"].values()
                                      for v2 in v.values()),
                       "modules": len(w["modules"]), "bridge": len(w["bridge"])},
        },
    }


def main():
    sys.path.insert(0, str(ROOT / "tools"))
    from sim_lib import sim_payload
    from runtime_lib import inject_runtime
    fb = json.loads(STATES.read_text(encoding="utf-8"))
    assert len(fb["states"]) == 50, "fact base must carry all 50 states"
    catalog = pack_catalog()
    for slug in ["STATEOS", "LEGACYMODEL"] + CORE_PACKS:
        if slug not in catalog:
            raise SystemExit(f"missing pack in dataset: {slug}")
    wlb = wlb_fact_base()

    payload = {
        "version": (ROOT / "VERSION").read_text().strip(),
        "note": fb["note"],
        "states": fb["states"],
        "blueprint": catalog["STATEOS"],
        "model": catalog["LEGACYMODEL"],
        "corePacks": {s: {"name": catalog[s]["name"], "blocks": catalog[s]["blocks"]}
                      for s in CORE_PACKS},
        "wlb": wlb["wlb"],
        "principles": wlb["principles"],
        "leadership": wlb["leadership"],
        # the 50-state compliance layer (data/states/compliance.json, v0.51.0)
        "compliance": json.loads((ROOT / "data" / "states" / "compliance.json").read_text(encoding="utf-8")),
        # the Simulation Studio (v0.54.0): the scenarios that localize to a state anchor
        "sims": sim_payload(anchors={"water", "corridor", "table", "culture", "storm"}),
        "curriculum": {
            "blocks": sum(1 for _ in csv.DictReader(open(BLOCKS, newline="", encoding="utf-8"))),
            "packs": len(catalog),
        },
    }
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = TEMPLATE.read_text(encoding="utf-8")
    if "__STDATA__" not in template:
        raise SystemExit("template.html is missing the __STDATA__ placeholder")
    OUT.write_text(inject_runtime(template.replace("__STDATA__", data), "states"), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {OUT.stat().st_size/1e3:.0f} KB "
          f"(50 states, {len(payload['blueprint']['tracks'])} blueprint tracks, "
          f"{len(payload['model']['tracks'])} civic tracks)")


if __name__ == "__main__":
    main()
