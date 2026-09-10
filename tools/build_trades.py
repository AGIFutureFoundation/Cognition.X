#!/usr/bin/env python3
"""Build the Cognition.X Trades Network app from the unions fact base + dataset.

Crosses the 37 trade families in data/unions/trade_unions.json with its 3
regions (San Francisco, Oakland–East Bay, New Orleans) into 111 regional
union/trade entries — each with the family's international union (with
per-region overrides where the craft is organized differently by coast),
a training-simulation scenario localized to a real, publicly known site,
and the curriculum packs that back it. Local/chapter numbers are never
emitted: every entry routes through the regional council to find the
current local.

Reads data/blocks.csv only for pack metadata (names, block counts, track
lists) so the app's curriculum links always match the canonical dataset.

    python3 tools/build_trades.py     # writes apps/trades-network/index.html
"""

import csv
import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UNIONS = ROOT / "data" / "unions" / "trade_unions.json"
BLOCKS = ROOT / "data" / "blocks.csv"
TEMPLATE = ROOT / "apps" / "trades-network" / "template.html"
OUT = ROOT / "apps" / "trades-network" / "index.html"

# Slug -> pack-name map mirrors normalize_blocks.PACK_SLUGS via the dataset.


def pack_catalog():
    packs = OrderedDict()
    with open(BLOCKS, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            slug = r["block_id"].split("-")[1]
            p = packs.setdefault(slug, {"name": r["pack"], "blocks": 0,
                                        "tracks": OrderedDict()})
            p["blocks"] += 1
            if r["track"]:
                p["tracks"].setdefault(r["track"], r["credential"])
    for p in packs.values():
        p["tracks"] = [{"name": n, "credential": c} for n, c in p["tracks"].items()]
    return packs


def main():
    fb = json.loads(UNIONS.read_text(encoding="utf-8"))
    regions, families = fb["regions"], fb["families"]

    entries = []
    for fam in families:
        for reg in regions:
            intl = fam.get("intl_by_region", {}).get(reg["id"], fam["intl"])
            site = reg["sites"][fam["kind"]]
            entries.append({
                "family": fam["family"],
                "intl": intl,
                "kind": fam["kind"],
                "region": reg["id"],
                "sim": fam["sim"].replace("{site}", site),
                "site": site,
                "packs": fam["packs"],
            })
    assert len(entries) == len(families) * len(regions), "roster shape drifted"

    catalog = pack_catalog()
    used = sorted({s for fam in families for s in fam["packs"]} | {"TRADESCLASS"})
    packmeta = {s: catalog[s] for s in used if s in catalog}
    missing = [s for s in used if s not in catalog]
    if missing:
        raise SystemExit(f"union fact base references unknown pack slugs: {missing}")

    payload = {
        "version": (ROOT / "VERSION").read_text().strip(),
        "note": fb["note"],
        "regions": [{k: v for k, v in r.items()} for r in regions],
        "families": len(families),
        "entries": entries,
        "packmeta": packmeta,
        "flipped": packmeta["TRADESCLASS"],
    }
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = TEMPLATE.read_text(encoding="utf-8")
    if "__TNDATA__" not in template:
        raise SystemExit("template.html is missing the __TNDATA__ placeholder")
    OUT.write_text(template.replace("__TNDATA__", data), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {OUT.stat().st_size/1e3:.0f} KB "
          f"({len(entries)} regional union/trade entries, {len(families)} families, "
          f"{len(regions)} regions)")


if __name__ == "__main__":
    main()
