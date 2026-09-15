#!/usr/bin/env python3
"""Validate the standards mappings (data/standards/*.json) and the
transfer-check rubrics (data/rubrics/*.json) against the dataset.

Standards (cx-standards/1):
  - required metadata: framework, publisher, documents, as_of, scope,
    strength, caveat — and the caveat must tell the reader to verify;
  - scope "block": every block_id exists, and its theme/grade match;
  - scope "track-band": every (pack, track, band) exists in the dataset;
  - every code is a non-empty string and no entry is empty.

Rubrics (cx-rubrics/1):
  - every (pack, track) exists; exactly three pass-evidence lines, three
    failure modes and an assessor note; no two rubrics for one track.

Prints a coverage summary; exits 1 on any problem. Run by CI after the
simulations validator.
"""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STD = ROOT / "data" / "standards"
RUB = ROOT / "data" / "rubrics"
BANDS = {"K–2", "3–5", "6–8", "9–10", "11–12"}


def load_rows():
    return list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))


def validate(rows=None):
    rows = rows if rows is not None else load_rows()
    by_id = {r["block_id"]: r for r in rows}
    tracks = {}
    for r in rows:
        if r["track"]:
            tracks.setdefault((r["block_id"].split("-")[1], r["track"]), set()).add(r["grade"])
    errs = []
    covered = set()
    frameworks = []
    for p in sorted(STD.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        name = p.name
        if d.get("format") != "cx-standards/1":
            errs.append(f"{name}: format must be cx-standards/1")
        for k in ("id", "framework", "publisher", "documents", "as_of", "scope", "strength", "strength_note", "caveat", "entries"):
            if not d.get(k):
                errs.append(f"{name}: missing {k}")
        if "verify" not in d.get("caveat", "").lower():
            errs.append(f"{name}: the caveat must tell the reader to verify the codes")
        if d.get("strength") not in ("cites", "aligns", "touches"):
            errs.append(f"{name}: strength must be cites, aligns or touches")
        n_codes = 0
        if d.get("scope") == "block":
            for e in d.get("entries", []):
                r = by_id.get(e.get("block_id"))
                if not r:
                    errs.append(f"{name}: block {e.get('block_id')!r} does not exist")
                    continue
                if e.get("theme") and r["theme"] != e["theme"]:
                    errs.append(f"{name}: {e['block_id']} theme drifted")
                if e.get("grade") and r["grade"] != e["grade"]:
                    errs.append(f"{name}: {e['block_id']} grade drifted")
                codes = e.get("codes", {})
                flat = [c for v in (codes.values() if isinstance(codes, dict) else [codes]) for c in v]
                if not flat or any(not isinstance(c, str) or not c.strip() for c in flat):
                    errs.append(f"{name}: {e['block_id']} has an empty code list or code")
                n_codes += len(flat)
                covered.add(e["block_id"])
        elif d.get("scope") == "track-band":
            pack = d.get("pack")
            for e in d.get("entries", []):
                key = (pack, e.get("track"))
                if key not in tracks:
                    errs.append(f"{name}: track {e.get('track')!r} not in pack {pack}")
                    continue
                if e.get("band") not in BANDS or e["band"] not in tracks[key]:
                    errs.append(f"{name}: band {e.get('band')!r} not in {e['track']!r}")
                    continue
                if not e.get("codes") or any(not c.strip() for c in e["codes"]):
                    errs.append(f"{name}: {e['track']} / {e['band']} has an empty code")
                if not e.get("why"):
                    errs.append(f"{name}: {e['track']} / {e['band']} needs a one-line why")
                n_codes += len(e.get("codes", []))
                for r in rows:
                    if r["block_id"].split("-")[1] == pack and r["track"] == e["track"] and r["grade"] == e["band"]:
                        covered.add(r["block_id"])
        else:
            errs.append(f"{name}: scope must be block or track-band")
        frameworks.append((d.get("id"), d.get("scope"), len(d.get("entries", [])), n_codes))

    rubric_tracks = set()
    for p in sorted(RUB.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        name = p.name
        if d.get("format") != "cx-rubrics/1":
            errs.append(f"{name}: format must be cx-rubrics/1")
        for k in ("note", "how_to_read", "rubrics"):
            if not d.get(k):
                errs.append(f"{name}: missing {k}")
        for rb in d.get("rubrics", []):
            key = (rb.get("pack"), rb.get("track"))
            if key not in tracks:
                errs.append(f"{name}: rubric for unknown track {key}")
                continue
            if key in rubric_tracks:
                errs.append(f"{name}: two rubrics for {key}")
            rubric_tracks.add(key)
            if len(rb.get("pass", [])) != 3 or any(not x.strip() for x in rb["pass"]):
                errs.append(f"{name}: {rb['track']} needs exactly three pass-evidence lines")
            if len(rb.get("fails", [])) != 3 or any(not x.strip() for x in rb["fails"]):
                errs.append(f"{name}: {rb['track']} needs exactly three failure modes")
            if not rb.get("note", "").strip():
                errs.append(f"{name}: {rb['track']} needs an assessor note")
    return errs, {"frameworks": frameworks, "blocks_covered": len(covered), "blocks": len(rows),
                  "tracks_with_rubric": len(rubric_tracks), "tracks": len(tracks)}


def main():
    errs, cov = validate()
    if errs:
        for e in errs:
            print("✗", e)
        sys.exit(1)
    fw = " · ".join(f"{i} ({s}: {n} entries, {c} codes)" for i, s, n, c in cov["frameworks"])
    print(f"OK: standards {fw} · {cov['blocks_covered']} of {cov['blocks']} blocks carry a code · "
          f"rubrics for {cov['tracks_with_rubric']} of {cov['tracks']} tracks")


if __name__ == "__main__":
    main()
