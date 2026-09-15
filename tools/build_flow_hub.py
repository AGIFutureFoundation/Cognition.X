#!/usr/bin/env python3
"""Build the Flow Hub app from the canonical dataset.

Reads data/blocks.csv (+ VERSION), compacts it, and injects it into
apps/flow-hub/template.html at the __CXDATA__ placeholder, writing
apps/flow-hub/index.html. This is the roadmap Phase 2 pattern: the app
is a build product of the dataset, never hand-edited.

Compact payload:
  { version, bands, levels,
    packs: [ { name, slug, kind, blocks,
               tracks: [ { name, prefix, credential,
                           themes: [[theme, base_description, transfer_check], ...] } ],
               loose:  [[grade, credential, theme, transfer_check], ...]  # foundation packs
             } ] }

kind: "os" (500-block OS editions), "legacy" (legacy-track localizations),
"community" (tracked 250-block packs), "foundation" (untracked source packs).
"""

import csv
import json
import sys
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANDS = ["K–2", "3–5", "6–8", "9–10", "11–12"]
LEVELS = ["Explorer", "Explorer", "Builder", "Practitioner", "Lead"]


def kind_of(pack, has_tracks, blocks):
    if pack.startswith("Civic Leadership Legacy"):
        return "legacy"
    if pack.startswith("Cognition.X :") or pack == "Non-Profit Practice":
        return "os"
    if not has_tracks:
        return "foundation"
    return "community"


def standards_payload(rows):
    """Every framework's metadata plus the codes, keyed for the app: by block_id
    (block scope) and by slug|track|band (track-band scope)."""
    out = {"frameworks": [], "byBlock": {}, "byTrackBand": {}}
    for p in sorted((ROOT / "data" / "standards").glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        out["frameworks"].append({k: d[k] for k in ("id", "framework", "publisher", "as_of", "scope", "strength", "strength_note", "caveat")})
        if d["scope"] == "block":
            for e in d["entries"]:
                flat = [c for v in e["codes"].values() for c in v]
                out["byBlock"].setdefault(e["block_id"], []).append({"fw": d["id"], "codes": flat})
        else:
            for e in d["entries"]:
                out["byTrackBand"].setdefault(f'{d["pack"]}|{e["track"]}|{e["band"]}', []).append({"fw": d["id"], "codes": e["codes"], "why": e["why"]})
    return out


def rubrics_payload():
    d = json.loads((ROOT / "data" / "rubrics" / "core_spine.json").read_text(encoding="utf-8"))
    return {"how_to_read": d["how_to_read"], "bands": d["bands"],
            "byTrack": {f'{r["pack"]}|{r["track"]}': {"pass": r["pass"], "fails": r["fails"], "note": r["note"]} for r in d["rubrics"]}}


def main():
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    version = (ROOT / "VERSION").read_text().strip()

    packs = OrderedDict()
    for r in rows:
        p = packs.setdefault(r["pack"], {"rows": [], "slug": r["block_id"].split("-")[1]})
        p["rows"].append(r)

    out_packs = []
    for name, p in packs.items():
        prows = p["rows"]
        tracks = OrderedDict()
        loose = []
        for r in prows:
            if r["track"]:
                t = tracks.setdefault(r["track"], {
                    "name": r["track"],
                    "prefix": r["code"].rsplit("-", 1)[0],
                    "credential": r["credential"],
                    "themes": OrderedDict(),
                })
                th = t["themes"].setdefault(r["theme"], [r["theme"], "", r["transfer_check"]])
                base = re.sub(r"\s+—\s+at\s+[^—]+$", "", r["description"])
                th[1] = base
            else:
                loose.append([r["grade"], r["credential"], r["theme"], r["transfer_check"], r["block_id"]])
        tr = [{"name": t["name"], "prefix": t["prefix"], "credential": t["credential"],
               "themes": list(t["themes"].values())} for t in tracks.values()]
        entry = {
            "name": name,
            "slug": p["slug"],
            "kind": kind_of(name, bool(tr), len(prows)),
            "blocks": len(prows),
            "tracks": tr,
        }
        if loose:
            entry["loose"] = loose
        out_packs.append(entry)

    access = json.loads((ROOT / "data" / "learners" / "learner_types.json")
                        .read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT / "tools"))
    from sim_lib import sim_payload
    from runtime_lib import inject_runtime
    payload = {"version": version, "bands": BANDS, "levels": LEVELS, "packs": out_packs,
               "access": access,
               # the Simulation Studio (v0.54.0): every scenario, keyed in the app by pack slug + track
               "sims": sim_payload(),
               # standards mappings and track rubrics (v0.56.0)
               "standards": standards_payload(rows),
               "rubrics": rubrics_payload()}
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    # keep the JSON safe inside a <script> block
    data = data.replace("</", "<\\/")

    template = (ROOT / "apps" / "flow-hub" / "template.html").read_text(encoding="utf-8")
    if "__CXDATA__" not in template:
        raise SystemExit("template.html is missing the __CXDATA__ placeholder")
    html = inject_runtime(template.replace("__CXDATA__", data), "flow-hub")
    out = ROOT / "apps" / "flow-hub" / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}: {len(html)/1e6:.2f} MB "
          f"({len(out_packs)} packs, {sum(len(x['tracks']) for x in out_packs)} tracks)")


if __name__ == "__main__":
    main()
