#!/usr/bin/env python3
"""Validate the canonical dataset (data/blocks.csv).

Checks:
  1. block_id present and globally unique
  2. required fields non-empty (pack, grade, credential, theme, transfer_check)
  3. tracked rows carry code, level and description
  4. band/level pairing on tracked rows (K-2/3-5 Explorer, 6-8 Builder,
     9-10 Practitioner, 11-12 Lead)
  5. every tracked (pack, track) has exactly 10 themes x 5 bands = 50 rows
  6. codes unique within their pack

Exits non-zero on any failure; prints a census either way.
"""

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOCKS = ROOT / "data" / "blocks.csv"
BAND_LEVEL = {"K–2": "Explorer", "3–5": "Explorer", "6–8": "Builder",
              "9–10": "Practitioner", "11–12": "Lead"}
# code and level are guaranteed dataset-wide since v0.14.0 (light fill);
# description remains required on tracked rows only.
REQUIRED = ["pack", "grade", "code", "level", "credential", "theme", "transfer_check"]

errors = []


def err(msg):
    errors.append(msg)


def main():
    with open(BLOCKS, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    ids = Counter(r["block_id"] for r in rows)
    for i, n in ids.items():
        if n > 1:
            err(f"duplicate block_id {i} ({n} rows)")
    for idx, r in enumerate(rows, 2):
        if not r.get("block_id"):
            err(f"line {idx}: missing block_id")
        for f_ in REQUIRED:
            if not r.get(f_):
                err(f"line {idx} ({r.get('block_id')}): empty {f_}")

    tracked = [r for r in rows if r["track"]]
    for r in tracked:
        for f_ in ("code", "level", "description"):
            if not r[f_]:
                err(f"{r['block_id']}: tracked row missing {f_}")
        expect = BAND_LEVEL.get(r["grade"])
        if expect and r["level"] != expect:
            err(f"{r['block_id']}: grade {r['grade']} should be level {expect}, got {r['level']}")

    per_track = defaultdict(list)
    for r in tracked:
        per_track[(r["pack"], r["track"])].append(r)
    for (pack, track), trows in per_track.items():
        if len(trows) != 50:
            err(f"{pack} / {track}: {len(trows)} rows, expected 50")
        themes = {r["theme"] for r in trows}
        if len(themes) != 10:
            err(f"{pack} / {track}: {len(themes)} themes, expected 10")

    per_pack_codes = defaultdict(Counter)
    for r in tracked:
        per_pack_codes[r["pack"]][r["code"]] += 1
    for pack, codes in per_pack_codes.items():
        for c, n in codes.items():
            if n > 1:
                err(f"{pack}: code {c} appears {n} times")

    # --- observation-safe transfer checks -------------------------------
    #
    # Some packs teach work that is dangerous to rehearse. Their specs say
    # so: the New Orleans Trades pack refuses contact with energized,
    # suspended or moving equipment, and the First Responder pack refuses
    # to send a learner toward an incident or into a clinical, tactical or
    # rescue act. Those are stated as prose in the spec's `notes`, and
    # prose is not a check. This is.
    #
    # A transfer check is a thing a learner is told to GO AND DO, often a
    # child. A pack can carry a careful safety sentence in its notes and a
    # check that contradicts it, and nothing here would have noticed. The
    # guard runs over every pack, not only the two, because the next pack
    # written from a spec is the one nobody re-reads.
    UNSAFE = [
        # `administer` alone is NOT enough. The Education OS pack has a
        # legitimate theme called "Administer tests", meaning an
        # assessment, and the first draft of this guard flagged two of its
        # blocks. A guard that cries wolf on real content is a guard
        # somebody switches off, so the clinical patterns all require a
        # clinical OBJECT rather than a verb that has an everyday sense.
        (r"\badminister(?:ing)?\s+(?:a\s+|an\s+|the\s+)?"
         r"(?:medication|medicine|drug|dose|injection|epinephrine|"
         r"naloxone|oxygen|insulin|aspirin)\b", "a clinical act"),
        (r"\b(?:dosage|dose of|perform cpr|apply a tourniquet|"
         r"triage (?:the )?(?:patients|casualties))\b", "a clinical act"),
        (r"\b(?:forced entry|breach the|restrain|handcuff|takedown)\b",
         "a tactical act"),
        (r"\bapproach(?:ing)? (?:the |an |a )?"
         r"(?:incident|scene|fire|apparatus|crash|wreck)\b",
         "approaching an incident"),
        (r"\b(?:climb|enter) (?:the |a |an )?"
         r"(?:scaffold|excavation|trench|confined space|roof)\b",
         "entering a hazardous space"),
        (r"\b(?:touch|operate|start) (?:the |a |an )?"
         r"(?:crane|hydrant|apparatus|energized|live )\b",
         "handling equipment"),
    ]
    unsafe_hits = 0
    for r in rows:
        chk = (r.get("transfer_check") or "")
        for pat, why in UNSAFE:
            if re.search(pat, chk, re.I):
                unsafe_hits += 1
                err(f"{r['block_id']}: transfer check asks for {why} — "
                    f"checks are read, map, plan and compare, never do: "
                    f"{chk[:90]!r}")
                break

    # --- the sibling cross-check ------------------------------------------
    #
    # The First Responder pack mirrors the five services SmartCiti.X's
    # respond/ registry describes, and the two live in different
    # repositories. A pack that cites a sibling and is never compared
    # against it is a citation nobody checks; the same pattern is used the
    # other way round, where SmartCiti.X's geo/ pack cross-checks its
    # RECORDED coordinates against the Locator.X checkout.
    #
    # It runs only when the sibling is actually there, and says which
    # happened, because a check that silently does nothing when a path is
    # missing reads exactly like a check that passed.
    spec_path = ROOT / "data" / "pack_specs" / "smartcitix-first-responder.json"
    sibling = ROOT.parent / "SmartCiti.X" / "respond" / "registry" / "respond.json"
    if spec_path.exists():
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        declared = {t["prefix"]: t.get("mirrors_smartcitix_service")
                    for t in spec["tracks"]}
        missing = [k for k, v in declared.items() if not v]
        if missing:
            err(f"first-responder spec: tracks {missing} declare no "
                "mirrors_smartcitix_service")
        if sibling.exists():
            resp = json.loads(sibling.read_text(encoding="utf-8"))
            svc = resp["services"]
            ids = set(svc) if isinstance(svc, dict) else {x["id"] for x in svc}
            named = {v for v in declared.values() if v}
            for bad in sorted(named - ids):
                err(f"first-responder spec: a track mirrors service {bad!r}, "
                    f"which respond/registry/respond.json does not have "
                    f"(it has {sorted(ids)})")
            for gone in sorted(ids - named):
                err(f"first-responder spec: respond/ describes service "
                    f"{gone!r} and no track mirrors it - the pack has fallen "
                    "behind the registry it companions")
            print(f"cross-check: SmartCiti.X checkout present, "
                  f"{len(named)} tracks mirror {len(ids)} services, held")
        else:
            print("cross-check: SmartCiti.X checkout not present beside this "
                  "one, the first-responder mirror check was skipped")

    packs = Counter(r["pack"] for r in rows)
    print(f"{len(rows)} blocks, {len(packs)} packs, {len(per_track)} tracks, "
          f"{len(set(r['credential'] for r in rows))} credentials")
    for p, n in packs.most_common():
        print(f"  {n:>5}  {p}")

    if errors:
        print(f"\nFAILED: {len(errors)} problem(s)", file=sys.stderr)
        for e in errors[:50]:
            print(f"  - {e}", file=sys.stderr)
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more", file=sys.stderr)
        sys.exit(1)
    print(f"\nobservation-safe guard: {len(rows)} transfer checks scanned "
          f"against {len(UNSAFE)} unsafe patterns, {unsafe_hits} flagged")
    print("\nOK: all checks passed")


if __name__ == "__main__":
    main()
