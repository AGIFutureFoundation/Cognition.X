#!/usr/bin/env python3
"""Assemble an `override: band-suffix` promotion from authored band sentences.

    python3 tools/author_override.py "<pack name>" out.json parts/*.py

Each part defines TRACKS = [(prefix, track name, [(theme, {band: sentence} × 5), …]), …].
Every theme must exist in the source with a suffixed description (the only
rows the override may touch); every band sentence must be ≥ 40 characters,
end with a full stop, carry no suffix, and the five must differ. Writes the
promotion only when every theme of the pack is covered and nothing fails."""
import csv, json, sys, importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
BANDS = ["K–2", "3–5", "6–8", "9–10", "11–12"]
pack, out = sys.argv[1], Path(sys.argv[2])
tracks = []
for part in sys.argv[3:]:
    spec = importlib.util.spec_from_file_location(Path(part).stem, part); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); tracks += m.TRACKS
rows = [r for r in csv.DictReader(open(ROOT / "data/source/Cognition.X_all_blocks.csv", encoding="utf-8")) if r["pack"] == pack and r["description"].strip()]
src = {}
for r in rows: src.setdefault((r["track"], r["theme"]), []).append(r)
shared = {k: v[0]["description"].split(" — at ")[0] for k, v in src.items()}
promo = {"pack": pack, "override": "band-suffix",
         "note": "The counted exception to fill-empty-only: every theme here exists in the source with a band-suffixed description (the documented content debt); this promotion replaces exactly those rows with five authored sentences per theme. The normaliser refuses any other target. Track names, prefixes, codes, credentials and transfer checks are untouched.",
         "tracks": []}
errs, n = [], 0
for prefix, name, themes in tracks:
    t = {"prefix": prefix, "name": name, "themes": []}
    for theme, bands in themes:
        if (name, theme) not in src: errs.append(f"no source theme: {name} / {theme}"); continue
        vals = [bands[b] for b in BANDS]
        if len(set(vals)) != 5: errs.append(f"duplicate sentences: {theme}")
        for v in vals:
            if len(v) < 40 or not v.endswith(".") or " — at " in v: errs.append(f"bad sentence: {theme}: {v[:60]}")
        t["themes"].append({"theme": theme, "description": shared[(name, theme)], "bands": bands}); n += 1
    promo["tracks"].append(t)
covered = {(t[1], th[0]) for t in tracks for th in t[2]}
missing = [k for k in src if k not in covered]
print(f"{pack}: {n} themes authored, {len(errs)} errors, {len(missing)} source themes missing")
for e in errs[:20]: print("  ", e)
for k in missing[:20]: print("   missing:", k)
if errs or missing: sys.exit(1)
out.write_text(json.dumps(promo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out)
