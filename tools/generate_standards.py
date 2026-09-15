#!/usr/bin/env python3
"""Generate data/standards/lss-k12.json from the Louisiana K–12 program.

The K–12 program (data/louisiana/k12_program.json, canonical since
v0.44.0) cites, for each of its 52 blocks, the Louisiana Student Standards
codes it was designed against: mathematics and ELA (LSSM / LSS ELA, which
carry CCSS numbering) and science (LSS Science, 2017, NGSS-style codes).
Those blocks are the K–12 pack's rows in data/blocks.csv, matched here by
theme and grade, so the citations become a block_id → codes mapping in
the standards schema every other framework uses.

Generated, never hand-edited; CI regenerates it and diffs. The caveat
travels with the data: these are the codes the program was designed
against, as cited — verify each against the current LDOE documents
before classroom use.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRAM = ROOT / "data" / "louisiana" / "k12_program.json"
BLOCKS = ROOT / "data" / "blocks.csv"
OUT = ROOT / "data" / "standards" / "lss-k12.json"

CAVEAT = ("These are the standards codes the block was designed against, as cited by the "
          "Louisiana K–12 program; verify each code against the current LDOE documents "
          "before classroom use. A code names an intended alignment, not a certification of it.")


def main():
    prog = json.loads(PROGRAM.read_text(encoding="utf-8"))
    rows = [r for r in csv.DictReader(open(BLOCKS, newline="", encoding="utf-8")) if r["pack"] == "K–12"]
    by_key = {(r["grade"], r["theme"]): r["block_id"] for r in rows}
    entries = []
    for g in prog["grades"]:
        for b in g["blocks"]:
            bid = by_key.get((g["g"], b[0]))
            if not bid:
                raise SystemExit(f"program block {g['g']!r} / {b[0]!r} has no K–12 row")
            entries.append({
                "block_id": bid,
                "theme": b[0],
                "grade": g["g"],
                "codes": {"lssm": list(b[1]), "lss_ela": list(b[2]), "lss_science": list(b[3])},
            })
    entries.sort(key=lambda e: e["block_id"])
    doc = {
        "format": "cx-standards/1",
        "id": "lss-k12",
        "framework": "Louisiana Student Standards — Mathematics (LSSM, CCSS-numbered), ELA (LSS ELA) and Science (LSS Science, NGSS-style codes)",
        "publisher": "Louisiana Department of Education",
        "documents": [
            {"key": "lssm", "title": "Louisiana Student Standards for Mathematics", "url": "https://doe.louisiana.gov/"},
            {"key": "lss_ela", "title": "Louisiana Student Standards for English Language Arts", "url": "https://doe.louisiana.gov/"},
            {"key": "lss_science", "title": "Louisiana Student Standards for Science", "url": "https://doe.louisiana.gov/"},
        ],
        "as_of": "as cited by data/louisiana/k12_program.json (extracted v0.44.0); document editions as published by LDOE",
        "scope": "block",
        "strength": "cites",
        "strength_note": "cites: the block's author named these codes as the design target. Stronger claims (an external body's alignment review) are not made anywhere in this repository.",
        "caveat": CAVEAT,
        "generated_by": "tools/generate_standards.py",
        "entries": entries,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    n = sum(len(v) for e in entries for v in e["codes"].values())
    print(f"wrote {OUT.relative_to(ROOT)}: {len(entries)} blocks · {n} code citations")


if __name__ == "__main__":
    main()
