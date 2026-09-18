#!/usr/bin/env python3
"""Insert authored per-band sentences (`bands`) into a pack spec.

    python3 tools/author_bands.py data/pack_specs/<spec>.json parts/*.py

Each part defines TRACKS = [(prefix, track name, [(theme, {band: sentence} × 5), …]), …].
Every (track, theme) must exist in the spec; every band sentence must be
≥ 40 characters, end with a full stop, carry no "— at" suffix, and the five
must differ. The spec is rewritten with its own indent only when every theme
is covered and nothing fails; then regenerate the pack:

    python3 tools/generate_pack.py data/pack_specs/<spec>.json > data/generated/<spec>.csv
    python3 tools/normalize_blocks.py
"""
import json, sys, importlib.util, re
from pathlib import Path
BANDS = ["K–2", "3–5", "6–8", "9–10", "11–12"]
spec_path = Path(sys.argv[1]); text = spec_path.read_text(encoding="utf-8")
indent = len(re.match(r"\{\n( +)", text).group(1)) if re.match(r"\{\n( +)", text) else 2
spec = json.loads(text)
authored = {}
for part in sys.argv[2:]:
    s = importlib.util.spec_from_file_location(Path(part).stem, part); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    for prefix, name, themes in m.TRACKS:
        for theme, bands in themes:
            authored[(name, theme)] = bands
errs, n = [], 0
for t in spec["tracks"]:
    for th in t["themes"]:
        k = (t["name"], th["theme"])
        if k not in authored: errs.append(f"not authored: {k}"); continue
        vals = [authored[k][b] for b in BANDS]
        if sorted(authored[k]) != sorted(BANDS): errs.append(f"bands keys: {k}")
        if len(set(vals)) != 5: errs.append(f"duplicate sentences: {k}")
        for v in vals:
            if len(v) < 40 or not v.endswith(".") or " — at " in v: errs.append(f"bad sentence: {k[1]}: {v[:60]}")
        th["bands"] = {b: authored[k][b] for b in BANDS}; n += 1
extra = [k for k in authored if k not in {(t["name"], th["theme"]) for t in spec["tracks"] for th in t["themes"]}]
print(f"{spec['pack']}: {n} themes authored, {len(errs)} errors, {len(extra)} authored themes not in the spec")
for e in errs[:20]: print("  ", e)
for k in extra[:20]: print("   extra:", k)
if errs or extra: sys.exit(1)
spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")
print("wrote", spec_path)
