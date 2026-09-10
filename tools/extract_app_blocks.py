#!/usr/bin/env python3
"""Extract the sector master-block library embedded in the Education OS app.

The app (apps/education-os/index.html) accumulated a DATA.sectorBlocks
library across its internal iterations (the sector-specialization rounds)
that never made it into the CSV export: uniform rows

    [sector, practiceTrack, 'T0X-SEC-ABC-n', theme, task, outcome]

across eight sectors. This tool parses them all and writes
data/generated/app-master-blocks.csv in the dataset schema, so the
canonical dataset finally contains the app's full library (roadmap
Phase 2: one source of truth).

Mapping (documented in docs/DATA_REVIEW.md):
  pack           <- sector (the matching OS edition; 'edu' becomes the
                    new pack "Cognition.X : Education OS")
  track          <- "" (practice blocks are adult micro-blocks, not the
                    10-themes x 5-bands tracked shape; kept untracked)
  code           <- the original T0X code (unique within its pack)
  grade / level  <- "11–12 · adult" / "Lead" (professional practice)
  credential     <- the practice-track name ("... Practice")
  theme          <- the block's action theme
  transfer_check <- task + outcome sentences, joined
  description    <- "" (untracked; authoring deferred like other
                    foundation descriptions)

Duplicated codes (rows redefined by later app rounds) keep the LAST
occurrence. Deterministic: same app build -> same CSV.
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "apps" / "education-os" / "index.html"
OUT = ROOT / "data" / "generated" / "app-master-blocks.csv"

SECTOR_PACK = {
    "corp": "Cognition.X : Corporate OS",
    "sci": "Cognition.X : Science OS",
    "rob": "Cognition.X : Robotics OS",
    "gh": "Cognition.X : Global Health OS",
    "mlt": "Cognition.X : Multilateral OS",
    "sap": "Cognition.X : Sapient OS",
    "edu": "Cognition.X : Education OS",
    "npo": "Non-Profit Practice",
}

ROW_RE = re.compile(
    r"\['(corp|sci|rob|gh|mlt|sap|edu|npo)','((?:[^'\\]|\\.)*)',"
    r"'(T0[A-Z]-[A-Z0-9]+-[A-Z0-9]+-\d+)','((?:[^'\\]|\\.)*)',"
    r"'((?:[^'\\]|\\.)*)','((?:[^'\\]|\\.)*)'\]"
)


def unesc(s):
    return s.replace("\\'", "'").replace('\\"', '"')


def main():
    t = APP.read_text(encoding="utf-8", errors="replace")
    rows = {}
    for m in ROW_RE.finditer(t):
        sector, track, code, theme, task, outcome = m.groups()
        rows[code] = {
            "pack": SECTOR_PACK[sector],
            "track": "",
            "code": code,
            "grade": "11–12 · adult",
            "level": "Lead",
            "credential": unesc(track),
            "theme": unesc(theme),
            "description": "",
            "transfer_check": (unesc(task).rstrip(".") + ". " + unesc(outcome)).strip(),
        }
    out_rows = sorted(rows.values(), key=lambda r: (r["pack"], r["code"]))
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["pack", "track", "code", "grade", "level",
                                          "credential", "theme", "description", "transfer_check"])
        w.writeheader()
        w.writerows(out_rows)
    packs = {}
    for r in out_rows:
        packs[r["pack"]] = packs.get(r["pack"], 0) + 1
    creds = len({r["credential"] for r in out_rows})
    print(f"extracted {len(out_rows)} master blocks -> {OUT.relative_to(ROOT)}")
    print(f"  {creds} practice tracks across {len(packs)} packs: "
          + ", ".join(f"{k.split(' : ')[-1]} {v}" for k, v in sorted(packs.items())))


if __name__ == "__main__":
    main()
