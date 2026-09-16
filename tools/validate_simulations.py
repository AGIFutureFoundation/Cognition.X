#!/usr/bin/env python3
"""Validate the Simulation Studio fact base (data/simulations/scenarios.json).

Referential integrity against the canonical dataset and the shape the
shared engine (tools/sim/engine.js) relies on:

  - every scenario names a pack slug in data/manifest.json and a track that
    exists in data/blocks.csv under that pack;
  - the carried transfer check is a real block of that track, quoted
    verbatim (the studio must never drift from the witnessed check);
  - every decision point has exactly one best option (score 2), one partial
    (1) and one missed (0), each tagged with a known discipline;
  - five steps, two complications and three debrief questions per scenario;
  - a trades kind (localized by region) must use {site}; every scenario is
    at band 9–10; the studio law and the run note are present verbatim.

Exit 1 on the first shape problem; prints a one-line summary on success.
Run by CI after validate_blocks.py.
"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FB = ROOT / "data" / "simulations" / "scenarios.json"
TRADES_KINDS = {"build", "elec", "water", "port", "transit", "service", "civic", "mech", "fire"}
ANCHORS = {None, "storm", "water", "corridor", "table", "culture"}


def load():
    return json.loads(FB.read_text(encoding="utf-8"))


def validate(doc, rows=None, manifest=None):
    """Return a list of problems (empty when the fact base is sound)."""
    errs = []
    rows = rows if rows is not None else list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    manifest = manifest if manifest is not None else json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))
    slugs = {p["slug"]: p["name"] for p in manifest["packs"]}
    by_id = {r["block_id"]: r for r in rows}
    tracks = {(r["block_id"].split("-")[1], r["track"]) for r in rows if r["track"]}

    if doc.get("format") != "cx-simulations/1":
        errs.append("format must be cx-simulations/1")
    for key in ("note", "law", "run_note", "next_rule"):
        if not doc.get(key):
            errs.append(f"missing {key}")
    if "Simulation ≠ certification" not in doc.get("law", "") or "Simulation ≠ certification" not in doc.get("run_note", ""):
        errs.append("the law and the run note must both carry 'Simulation ≠ certification' verbatim")
    if "NOT LEGAL ADVICE" not in doc.get("youth_note", ""):
        errs.append("youth_note must say NOT LEGAL ADVICE and tell the reader to verify with the state labor department")
    if "never a credential" not in doc.get("run_note", ""):
        errs.append("run_note must say a run is never a credential")
    disc = {d["id"] for d in doc.get("disciplines", [])}
    if len(disc) < 6:
        errs.append("fewer than six disciplines")
    levels = [d.get("level") for d in doc.get("difficulty", [])]
    if levels != [1, 2, 3]:
        errs.append("difficulty must be levels 1, 2, 3")

    ids = Counter()
    used_disc = Counter()
    for s in doc.get("scenarios", []):
        sid = s.get("id", "?")
        ids[sid] += 1
        for key in ("title", "role", "brief", "pack", "track", "site_default", "transfer", "steps", "complications", "debrief", "simulated", "live", "band"):
            if key not in s:
                errs.append(f"{sid}: missing {key}")
        if s.get("pack") not in slugs:
            errs.append(f"{sid}: unknown pack slug {s.get('pack')!r}")
        elif (s["pack"], s.get("track")) not in tracks:
            errs.append(f"{sid}: track {s.get('track')!r} not in pack {s['pack']}")
        elif s.get("packName") != slugs[s["pack"]]:
            errs.append(f"{sid}: packName drifted from the manifest")
        if s.get("band") != "9–10":
            errs.append(f"{sid}: band must be 9–10")
        kind = s.get("kind")
        if kind is not None and kind not in TRADES_KINDS:
            errs.append(f"{sid}: unknown trades kind {kind!r}")
        if kind in TRADES_KINDS and "{site}" not in s.get("brief", ""):
            errs.append(f"{sid}: a trades-kind scenario must localize with {{site}} in its brief")
        if kind in TRADES_KINDS and "Under 18" not in s.get("youth", ""):
            errs.append(f"{sid}: a trades-kind scenario must carry an 'Under 18' youth line (hazardous-occupation orders)")
        if s.get("localize") not in ANCHORS:
            errs.append(f"{sid}: unknown localize anchor {s.get('localize')!r}")
        t = s.get("transfer") or {}
        b = by_id.get(t.get("block_id"))
        if not b:
            errs.append(f"{sid}: transfer block {t.get('block_id')!r} does not exist")
        else:
            if b["track"] != s.get("track") or b["block_id"].split("-")[1] != s.get("pack"):
                errs.append(f"{sid}: transfer block belongs to another track")
            if b["transfer_check"] != t.get("check"):
                errs.append(f"{sid}: transfer check is not quoted verbatim from the dataset")
            if b["credential"] != t.get("credential"):
                errs.append(f"{sid}: transfer credential drifted from the dataset")
        if "never credits the ledger" not in t.get("note", ""):
            errs.append(f"{sid}: transfer note must say the run never credits the ledger")
        if len(s.get("steps", [])) != 5:
            errs.append(f"{sid}: expected 5 steps, found {len(s.get('steps', []))}")
        if len(s.get("complications", [])) != 2:
            errs.append(f"{sid}: expected 2 complications")
        if len(s.get("debrief", [])) != 3:
            errs.append(f"{sid}: expected 3 debrief questions")
        if len(s.get("simulated", [])) < 2 or len(s.get("live", [])) < 2:
            errs.append(f"{sid}: name at least two simulated hazards and two live practices")
        seen_steps = set()
        for st in s.get("steps", []) + s.get("complications", []):
            stid = st.get("id", "?")
            if stid in seen_steps:
                errs.append(f"{sid}: duplicate decision id {stid}")
            seen_steps.add(stid)
            if not st.get("prompt"):
                errs.append(f"{sid}/{stid}: empty prompt")
            opts = st.get("options", [])
            if sorted(o.get("s") for o in opts) != [0, 1, 2]:
                errs.append(f"{sid}/{stid}: options must score exactly 0, 1 and 2")
            for o in opts:
                if o.get("d") not in disc:
                    errs.append(f"{sid}/{stid}: unknown discipline {o.get('d')!r}")
                used_disc[o.get("d")] += 1
                if not o.get("t") or not o.get("c"):
                    errs.append(f"{sid}/{stid}: option needs text and a consequence")
    dup = [k for k, n in ids.items() if n > 1]
    if dup:
        errs.append(f"duplicate scenario ids: {dup}")
    unused = disc - set(used_disc)
    if unused:
        errs.append(f"disciplines never scored: {sorted(unused)}")
    return errs


def main():
    doc = load()
    errs = validate(doc)
    if errs:
        for e in errs:
            print("✗", e)
        sys.exit(1)
    n = len(doc["scenarios"])
    points = sum(len(s["steps"]) + len(s["complications"]) for s in doc["scenarios"])
    kinds = sum(1 for s in doc["scenarios"] if s.get("kind"))
    print(f"OK: {n} scenarios · {points} decision points · {kinds} trades kinds localized by region · "
          f"{len(doc['disciplines'])} disciplines · every transfer check quoted verbatim")


if __name__ == "__main__":
    main()
