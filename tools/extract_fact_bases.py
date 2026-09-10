#!/usr/bin/env python3
"""Canonicalize the Education OS app's embedded fact bases.

Roadmap Phase 2, pipeline stage two: the Louisiana region/parish fact
base and the Willie L. Brown Jr. Institute (WLB) fact base have lived
as JS literals inside apps/education-os/template.html, and the
Louisiana and States builders extracted them at build time by
evaluating the app. This tool performs that extraction ONCE and writes
the results as canonical repository data:

    data/louisiana/fact_base.json   regions · regionHubs · parishes
    data/wlb/institute.json         org · disclaimer · mission · quote
                                    · record · principles

After this, tools/build_louisiana.py and tools/build_states.py read
the canonical files and no longer depend on the app template. The
Education OS template keeps its own copy as the app's display source
(shrinking the template itself is later pipeline work); if that copy
is ever edited, re-run this tool and review the diff — the canonical
files are the source of truth for every OTHER app.

Deterministic; re-running against an unchanged template reproduces
the files byte-for-byte.
"""

import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDU = ROOT / "apps" / "education-os" / "template.html"


def extract():
    t = EDU.read_text(encoding="utf-8", errors="replace")

    def grab(name):
        i = t.find(name + "=")
        j = t.find("];", i)
        return t[i + len(name) + 1: j + 1]

    def grab_obj(name):
        i = t.find(name + "=")
        j1, j2 = t.find("];", i), t.find("};", i)
        j = min(x for x in (j1, j2) if x > 0)
        return t[i + len(name) + 1: j + 1]

    js = ("const regions=" + grab("DATA.regions") + ";"
          "const hubs=" + grab("DATA.regionHubs") + ";"
          "const parishes=" + grab("DATA.parishes") + ";"
          "const wlb=" + grab_obj("DATA.wlb") + ";"
          "const principles=" + grab("DATA.wlbPrinciples") + ";"
          "console.log(JSON.stringify({regions,hubs,parishes,"
          "wlb:{org:wlb.org,disclaimer:wlb.disclaimer,mission:wlb.mission,"
          "quote:wlb.quote,record:wlb.record},"
          "principles:principles.map(x=>({p:x.p,src:x.src,teach:x.teach}))}));")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(js)
        path = f.name
    out = subprocess.run(["node", path], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, indent=1) + "\n"
    changed = (not path.exists()) or path.read_text(encoding="utf-8") != text
    path.write_text(text, encoding="utf-8")
    print(f"{'wrote' if changed else 'unchanged'} {path.relative_to(ROOT)}")


def main():
    fb = extract()
    write(ROOT / "data" / "louisiana" / "fact_base.json", {
        "note": ("Louisiana fact base — extracted from the Education OS app "
                 "(apps/education-os/template.html) by tools/extract_fact_bases.py "
                 "and canonical here since v0.39.0. Parish rows are "
                 "[name, region, seat, population_k, proposed_wave, districts, "
                 "industries, narrative_world, rural_tier]. Waves are the original "
                 "four-wave proposal kept as provenance; the adopted two-wave plan "
                 "is computed at build time."),
        "regions": fb["regions"],
        "regionHubs": fb["hubs"],
        "parishes": fb["parishes"],
    })
    write(ROOT / "data" / "wlb" / "institute.json", {
        "note": ("Willie L. Brown Jr. Institute fact base — extracted from the "
                 "Education OS app by tools/extract_fact_bases.py and canonical "
                 "here since v0.39.0. The disclaimer travels verbatim with every "
                 "use; principles carry their source attribution."),
        **fb["wlb"],
        "principles": fb["principles"],
    })


if __name__ == "__main__":
    main()
