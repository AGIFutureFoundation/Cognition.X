#!/usr/bin/env python3
"""Turn collected cx-evidence/1 files into block-revision priorities.

The evidence loop, review-board side: sites export opt-in, anonymized,
aggregate-only evidence files from the Louisiana platform (the export
box is the only exit — nothing is ever transmitted by the apps), a
human sends them here, and this tool merges them into a triage report:

  1. MIS-PITCHED?   Tracks whose witnessed checks fail often (high
                    "not yet" rate with enough attempts) — the check
                    may be pitched wrong for the band, or the theme
                    under-taught. Top revision priority.
  2. UNREPORTED     Tracks in the dataset that no submitted file mentions
                    at all — review for relevance or reachability. Read
                    it honestly: this means no SUBMITTING site reported
                    activity, not that nobody anywhere used the track.
  3. HEALTHY        Everything else, listed with its numbers.

Usage:
    python3 tools/evidence_triage.py [evidence.json ...]
    (no args: reads data/evidence/*.json)

Thresholds are deliberately conservative: a track needs >= MIN_WITNESSED
witnessed attempts before its not-yet rate means anything. The report is
input to the curriculum review board (docs/GOVERNANCE.md), never an
automatic edit — evidence proposes; the board disposes.
"""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_WITNESSED = 5
NOTYET_FLAG = 0.4


def load(paths):
    merged = {}
    files = 0
    for path in paths:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if data.get("format") != "cx-evidence/1":
            print(f"skipping {path}: not a cx-evidence/1 file", file=sys.stderr)
            continue
        files += 1
        for t in data.get("tracks", []):
            key = (t.get("pack", ""), t["track"])
            a = merged.setdefault(key, {"checksRecorded": 0, "witnessedConfirmed": 0,
                                        "witnessedNotYet": 0, "learners": 0, "sites": 0})
            for f in ("checksRecorded", "witnessedConfirmed", "witnessedNotYet", "learners"):
                a[f] += int(t.get(f, 0))
            a["sites"] += 1
    return merged, files


def dataset_tracks():
    """Every tracked (pack, track) in the canonical dataset — the universe
    the submitted evidence is measured against."""
    try:
        with open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8") as f:
            return {(r["pack"], r["track"]) for r in csv.DictReader(f) if r["track"]}
    except OSError:
        return set()


def main():
    paths = sys.argv[1:] or sorted((ROOT / "data" / "evidence").glob("*.json"))
    if not paths:
        sys.exit("no evidence files given and none under data/evidence/")
    merged, files = load(paths)
    if not merged:
        sys.exit("no usable cx-evidence/1 files")

    mispitched, healthy = [], []
    for (pack, track), a in merged.items():
        witnessed = a["witnessedConfirmed"] + a["witnessedNotYet"]
        rate = a["witnessedNotYet"] / witnessed if witnessed else 0.0
        row = {"pack": pack, "track": track, **a, "witnessed": witnessed, "notYetRate": rate}
        if witnessed >= MIN_WITNESSED and rate >= NOTYET_FLAG:
            mispitched.append(row)
        else:
            healthy.append(row)
    mispitched.sort(key=lambda r: -r["notYetRate"])
    healthy.sort(key=lambda r: -r["checksRecorded"])

    print(f"evidence triage — {files} file(s), {len(merged)} track(s) with activity\n")
    if mispitched:
        print(f"REVISION PRIORITIES (not-yet rate ≥ {NOTYET_FLAG:.0%} over ≥ {MIN_WITNESSED} witnessed attempts):")
        for r in mispitched:
            print(f"  {r['notYetRate']:>4.0%}  {r['track']}  [{r['pack']}]"
                  f"  — {r['witnessedNotYet']} not-yet / {r['witnessed']} witnessed across {r['sites']} site(s)")
        print("  → the check may be mis-pitched for its band, or the theme under-taught.")
        print("  → propose a supersession or teaching note to the review board; never edit ids.\n")
    else:
        print("REVISION PRIORITIES: none flagged at current thresholds.\n")
    universe = dataset_tracks()
    if universe:
        unreported = sorted(universe - set(merged))
        print(f"UNREPORTED ({len(unreported)} of {len(universe)} tracks in the dataset):")
        if unreported:
            for pack, track in unreported[:15]:
                print(f"  {track}  [{pack}]")
            if len(unreported) > 15:
                print(f"  …and {len(unreported)-15} more.")
            print("  → no submitting site reported activity on these. That is not the same")
            print("    as unused: review for relevance or reachability, and check whether")
            print("    the sites that use them simply have not sent evidence.\n")
        else:
            print("  none — every track in the dataset appears in the submitted evidence.\n")
    print("ACTIVE TRACKS:")
    for r in healthy[:20]:
        print(f"  {r['checksRecorded']:>5} checks  {r['track']}  [{r['pack']}]"
              f"  — {r['witnessedConfirmed']}✓/{r['witnessedNotYet']}↺ witnessed, {r['learners']} learner-touches")
    if len(healthy) > 20:
        print(f"  …and {len(healthy)-20} more.")


if __name__ == "__main__":
    main()
