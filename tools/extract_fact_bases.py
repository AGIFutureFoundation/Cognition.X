#!/usr/bin/env python3
"""Round-trip the Education OS app's fact bases against the canonical data.

Roadmap Phase 2, pipeline stage two (v0.39.0): the Louisiana region/parish
fact base, the K-12 program and the Willie L. Brown Jr. Institute (WLB)
fact base once lived as JS literals inside apps/education-os/template.html.
This tool extracted them ONCE and wrote them as canonical repository data:

    data/louisiana/fact_base.json   regions · regionHubs · parishes
    data/louisiana/k12_program.json grades · threads
    data/wlb/institute.json         name … seal · principles

Since v0.63.0 the direction is reversed for the app as well: the template
carries a `__CXFACT:<name>__` placeholder where each literal stood, and
tools/build_education_os.py injects the canonical JSON in place at build
time (marked `/*cx:<name>*/ … /*cx:end*/` in the built file). This tool now
reads each layer from wherever it currently lives — the placeholder's
injected value in apps/education-os/index.html, or a literal still in the
template — and writes what it finds to the canonical files. Run it in CI
after a build: an unchanged tree proves the app carries exactly the
canonical data, byte for byte.

    python3 tools/extract_fact_bases.py           # write (CI then diffs)
    python3 tools/extract_fact_bases.py --check   # exit 1 if any would change

Deterministic; re-running against an unchanged app reproduces the files.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "apps" / "education-os" / "template.html"
BUILT = ROOT / "apps" / "education-os" / "index.html"
LAYERS = ["regions", "regionHubs", "parishes", "wlb", "wlbPrinciples", "lak12", "lak12Threads"]


def _literal_from_template(t, name):
    i = t.find("DATA." + name + "=")
    if i < 0:
        return None
    head = t[i + len("DATA." + name + "="):i + len("DATA." + name + "=") + 40]
    if head.startswith("__CXFACT:"):
        return None
    j1, j2 = t.find("];", i), t.find("};", i)
    j = min(x for x in (j1, j2) if x > 0)
    return t[i + len("DATA." + name + "="): j + 1]


def _literal_from_built(b, name):
    a = b.find("/*cx:" + name + "*/")
    if a < 0:
        return None
    a += len("/*cx:" + name + "*/")
    z = b.find("/*cx:end*/", a)
    return b[a:z]


def literals():
    t = TEMPLATE.read_text(encoding="utf-8", errors="replace")
    b = BUILT.read_text(encoding="utf-8", errors="replace") if BUILT.exists() else ""
    out = {}
    for name in LAYERS:
        lit = _literal_from_template(t, name)
        where = "template"
        if lit is None:
            lit = _literal_from_built(b, name)
            where = "built app"
        if lit is None:
            raise SystemExit(f"{name}: found neither a literal in the template nor an injected value in the built app — rebuild first")
        out[name] = (lit, where)
    return out


def extract():
    lits = literals()
    js = "".join(f"const {n}={lits[n][0]};" for n in LAYERS) + (
        "console.log(JSON.stringify({regions,hubs:regionHubs,parishes,"
        "wlb:{name:wlb.name,org:wlb.org,disclaimer:wlb.disclaimer,mission:wlb.mission,"
        "quote:wlb.quote,fellowshipQuote:wlb.fellowshipQuote,record:wlb.record,"
        "fellowship:wlb.fellowship,k12:wlb.k12,strands:wlb.strands,eras:wlb.eras,"
        "courses:wlb.courses,bridge:wlb.bridge,modules:wlb.modules,"
        "standards:wlb.standards,seal:wlb.seal},"
        "principles:wlbPrinciples.map(x=>({p:x.p,src:x.src,teach:x.teach,strands:x.strands})),"
        "k12:{grades:lak12,threads:lak12Threads}}));")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        path = f.name
    out = subprocess.run(["node", path], capture_output=True, text=True, check=True)
    return json.loads(out.stdout), {n: w for n, (_, w) in lits.items()}


def documents(fb):
    return {
        ROOT / "data" / "louisiana" / "fact_base.json": {
            "note": ("Louisiana fact base — canonical here since v0.39.0 (extracted once from the "
                     "Education OS app by tools/extract_fact_bases.py; since v0.63.0 the app is built "
                     "FROM this file and the tool round-trips it). Parish rows are "
                     "[name, region, seat, population_k, proposed_wave, districts, "
                     "industries, narrative_world, rural_tier]. Waves are the original "
                     "four-wave proposal kept as provenance; the adopted two-wave plan "
                     "is computed at build time."),
            "regions": fb["regions"],
            "regionHubs": fb["hubs"],
            "parishes": fb["parishes"],
        },
        ROOT / "data" / "louisiana" / "k12_program.json": {
            "note": ("Louisiana K-12 program — canonical here since v0.44.0 (extracted once from "
                     "the Education OS app by tools/extract_fact_bases.py; since v0.63.0 the app is "
                     "built FROM this file and the tool round-trips it). Thirteen grade rows (K-12), "
                     "each with an age-appropriate role and narrative world and six threads "
                     "(literacy, numeracy, science, computer science, safety, "
                     "assessment) citing Louisiana LDOE standard codes; the policy "
                     "threads name the LDOE acts and gates the program is built "
                     "around. A design mapped against public LDOE documents — "
                     "verify each code against the current documents before "
                     "classroom use."),
            "grades": fb["k12"]["grades"],
            "threads": fb["k12"]["threads"],
        },
        ROOT / "data" / "wlb" / "institute.json": {
            "note": ("Willie L. Brown Jr. Institute fact base — canonical here since v0.39.0 "
                     "(extracted once from the Education OS app by tools/extract_fact_bases.py; the "
                     "full leadership curriculum — strands, eras, course ladders, bridge, modules, "
                     "standards, seal — since v0.43.0; since v0.63.0 the app is built FROM this file "
                     "and the tool round-trips it). The disclaimer travels verbatim with every use; "
                     "principles carry their source attribution and the strands they anchor."),
            **fb["wlb"],
            "principles": fb["principles"],
        },
    }


def render(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def main():
    check = "--check" in sys.argv[1:]
    fb, where = extract()
    docs = documents(fb)
    changed = []
    for path, obj in docs.items():
        text = render(obj)
        same = path.exists() and path.read_text(encoding="utf-8") == text
        if not same:
            changed.append(path)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
        print(f"{'unchanged' if same else ('would change' if check else 'wrote')} {path.relative_to(ROOT)}")
    src = ", ".join(f"{n} from {w}" for n, w in where.items())
    print(f"layers read: {src}")
    if check and changed:
        raise SystemExit("the app's fact bases differ from the canonical files: " + ", ".join(str(p.relative_to(ROOT)) for p in changed))


if __name__ == "__main__":
    main()
