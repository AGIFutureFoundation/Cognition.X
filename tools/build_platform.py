#!/usr/bin/env python3
"""Build the Cognition.X Platform app — the working model of the platform.

One single-file page that models the whole system: the live architecture
(dataset → pipeline → apps → working models → the evidence loop back),
a runnable end-to-end demo of the learning loop executed with the
platform's real mechanics on labeled demo data, and the doors into the
six apps.

Reads data/manifest.json + VERSION for live totals. Output:
apps/platform/index.html from apps/platform/template.html (placeholder
__PXDATA__). A build product — never hand-edited.
"""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    manifest = json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    tracks = len({(r["pack"], r["track"]) for r in rows if r["track"]})
    creds = len({r["credential"] for r in rows})

    # one real track (Louisiana OS, first track) so the demo loop runs on
    # genuine dataset content, not invented text
    la = [r for r in rows if r["pack"] == "Cognition.X : Louisiana OS" and r["track"]]
    first_track = la[0]["track"]
    tr_rows = [r for r in la if r["track"] == first_track]
    demo_track = {
        "pack": "Cognition.X : Louisiana OS",
        "name": first_track,
        "credential": tr_rows[0]["credential"],
        "blocks": len(tr_rows),
        "sampleTheme": tr_rows[0]["theme"],
        "sampleCheck": tr_rows[0]["transfer_check"],
    }

    sys.path.insert(0, str(ROOT / "tools"))
    from sim_lib import sim_payload
    from runtime_lib import inject_runtime
    sims = sim_payload(ids={"SIM-HURRICANE-72"})
    sims["site"] = "Orleans Parish"

    payload = {
        "version": (ROOT / "VERSION").read_text().strip(),
        "totals": {
            "blocks": manifest["total_blocks"],
            "packs": len(manifest["packs"]),
            "tracks": tracks,
            "credentials": creds,
        },
        "demoTrack": demo_track,
        # the Simulation Studio (v0.54.0): the scenario from the demo track's own pack (Louisiana OS)
        "sims": sims,
    }
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = (ROOT / "apps" / "platform" / "template.html").read_text(encoding="utf-8")
    if "__PXDATA__" not in template:
        raise SystemExit("template.html is missing the __PXDATA__ placeholder")
    out = ROOT / "apps" / "platform" / "index.html"
    out.write_text(inject_runtime(template.replace("__PXDATA__", data), "platform"), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}: {out.stat().st_size/1e3:.0f} KB "
          f"({payload['totals']['blocks']} blocks, demo track: {demo_track['name']!r})")


if __name__ == "__main__":
    main()
