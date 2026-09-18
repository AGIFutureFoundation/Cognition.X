#!/usr/bin/env python3
"""Platform invariant tests — the standing rules, enforced mechanically.

Until now every release was verified by throwaway browser scripts that
never entered the repository: CI could prove the apps REBUILD, but
nothing proved they still HOLD THE RULES. This suite closes that gap
with the same guarantee the rest of the pipeline gives — Python 3
alone, no packages, no browser, no network — so it runs anywhere the
build runs.

What it asserts, per the platform's standing stances:

  Build integrity   every app is a build product with its payload
                    substituted, carrying the current VERSION.
  No network        no app contains network CALL SYNTAX (prose that
                    merely names fetch/WebSocket is fine — the
                    Education OS describes its own security audit) and
                    loads nothing external but the documented font
                    stylesheet; document links are user-clicked
                    navigation, never runtime loads.
  Dataset           block_ids are unique and well-formed; the manifest
                    agrees with blocks.csv; tracked packs keep the
                    50-block/10-theme/5-band shape.
  Honesty stances   simulation is never certification; no union local
                    or chapter numbers anywhere; access profiles are
                    chosen supports, never diagnoses; the Willie L.
                    Brown Jr. Institute disclaimer travels verbatim.
  Working models    the credential threshold is 50 everywhere it is
                    written down; the evidence export is consent-gated
                    in code, not only in the UI.

Run: python3 tests/test_platform.py        (exit 0 = all green)
The deeper browser checks live in tests/browser/ and need Playwright.
"""

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPS = ["education-os", "flow-hub", "louisiana", "trades-network", "states", "platform"]

FAILURES = []
CHECKS = [0]


def check(name, ok, detail=""):
    CHECKS[0] += 1
    if not ok:
        FAILURES.append(f"{name}: {detail}" if detail else name)


def app_html(app):
    return (ROOT / "apps" / app / "index.html").read_text(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------- build integrity
def test_build_products():
    version = (ROOT / "VERSION").read_text().strip()
    for app in APPS:
        p = ROOT / "apps" / app / "index.html"
        check(f"{app}: built file exists", p.exists())
        if not p.exists():
            continue
        t = app_html(app)
        check(f"{app}: non-trivial build", len(t) > 20_000, f"{len(t)} bytes")
        # no unsubstituted payload placeholder survived the build
        left = re.findall(r"__[A-Z]{2,10}DATA__", t)
        check(f"{app}: payload substituted", not left, f"left: {left}")
        # Five apps are deliberate HTML5 fragments (the browser implies
        # html/body). The rule is only: whatever you open explicitly, close.
        # The Education OS shipped 44 releases with an opened-but-unclosed
        # <body> and a stray unwrapped `var DATA` block rendering as text.
        if "<body" in t:
            check(f"{app}: explicit <body> is closed", "</body>" in t)
        if "<html" in t:
            check(f"{app}: explicit <html> is closed", "</html>" in t)
        check(f"{app}: no script source leaking into the body",
              not re.search(r"^\s*var DATA = \{", t, re.M))
        # every app but the imported flagship carries the current version string
        if app != "education-os":
            check(f"{app}: carries VERSION {version}", version in t)


# ---------------------------------------------------------------- no network
# Call SYNTAX, not mere mention: the Education OS names these primitives in
# its own security-audit prose, which is exactly the claim being made.
NETWORK_CALLS = {
    "fetch()": re.compile(r"(?<![\w.$])fetch\s*\("),
    "new XMLHttpRequest": re.compile(r"new\s+XMLHttpRequest\s*\("),
    "new WebSocket": re.compile(r"new\s+WebSocket\s*\("),
    "new EventSource": re.compile(r"new\s+EventSource\s*\("),
    "sendBeacon()": re.compile(r"\.sendBeacon\s*\("),
    "navigator.share()": re.compile(r"navigator\.share\s*\("),
    "dynamic import()": re.compile(r"(?<![\w.$])import\s*\("),
    "eval()": re.compile(r"(?<![\w.$])eval\s*\("),
}
# Hosts an app may REFERENCE. The font stylesheet is the one runtime load;
# the rest are documentation links a person clicks, never fetched by code.
# v0.55.0: the typefaces are embedded; the only hosts an app may name are link targets a person clicks
ALLOWED_HOSTS = {"github.com", "www2.ed.gov"}
HOST_REF = re.compile(r"""(?:src|href)\s*=\s*["'](?:https?:)?//([^/"']+)""", re.I)


def test_no_network():
    for app in APPS:
        t = app_html(app)
        for label, pat in NETWORK_CALLS.items():
            hits = pat.findall(t)
            check(f"{app}: no {label}", not hits, f"{len(hits)} occurrence(s)")
        hosts = {m.group(1) for m in HOST_REF.finditer(t)}
        # template-expression artifacts are not hosts
        hosts = {h for h in hosts if not h.startswith("$")}
        stray = hosts - ALLOWED_HOSTS
        check(f"{app}: no undocumented external hosts", not stray, f"{sorted(stray)}")


# ---------------------------------------------------------------- dataset
BLOCK_ID = re.compile(r"^CX-[A-Z0-9]+-\d{4}$")


def test_dataset():
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    check("dataset: non-empty", len(rows) > 10_000, f"{len(rows)} rows")

    ids = [r["block_id"] for r in rows]
    dupes = [i for i, n in Counter(ids).items() if n > 1]
    check("block_ids unique", not dupes, f"{len(dupes)} duplicated, e.g. {dupes[:3]}")
    bad = [i for i in ids if not BLOCK_ID.match(i)]
    check("block_ids well-formed", not bad, f"{len(bad)} malformed, e.g. {bad[:3]}")

    # structural fill: the validator requires code+level dataset-wide
    missing = [r["block_id"] for r in rows if not r["code"].strip() or not r["level"].strip()]
    check("every row carries code+level", not missing, f"{len(missing)} missing")

    manifest = json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))
    check("manifest total matches blocks.csv",
          manifest["total_blocks"] == len(rows),
          f"manifest {manifest['total_blocks']} vs csv {len(rows)}")
    check("manifest pack count matches",
          len(manifest["packs"]) == len({r["pack"] for r in rows}),
          f"manifest {len(manifest['packs'])} vs csv {len({r['pack'] for r in rows})}")

    # tracked packs keep the 50-block shape: 10 themes x 5 bands, one credential
    by_track = {}
    for r in rows:
        if r["track"]:
            by_track.setdefault((r["pack"], r["track"]), []).append(r)
    wrong = {k: len(v) for k, v in by_track.items() if len(v) != 50}
    check("every tracked track is 50 blocks", not wrong,
          f"{len(wrong)} off-shape, e.g. {list(wrong.items())[:2]}")
    multi = {k: {x["credential"] for x in v} for k, v in by_track.items()}
    bad_cred = {k: c for k, c in multi.items() if len(c) != 1}
    # One track carries two credential strings — the legacy "Practitioner"
    # naming defect below, partially corrected for its first theme. Pinned so
    # it cannot spread; see docs/DATA_REVIEW.md.
    check("no NEW tracks with split credentials", len(bad_cred) <= KNOWN_SPLIT_CREDENTIAL_TRACKS,
          f"{len(bad_cred)} tracks, known baseline {KNOWN_SPLIT_CREDENTIAL_TRACKS}: {list(bad_cred)[:3]}")


# A level word is not a credential. The v0.1.0 import named 1,228 rows'
# credential "Practitioner"; v0.52.0 corrected the 1,195 that sit in the 24
# promoted tracks through data/promotions/ (names proposed to the review
# board, applied as a counted exception to fill-empty-only). The 33 that
# remain are the Empathy & Emotional Intelligence pack's trackless (EW)
# theme group — a partial group with no 50-block track to hang a credential
# on; the board decides whether to complete it as a track. Ratchets: lower
# them when that happens; never raise them.
KNOWN_LEVEL_WORD_CREDENTIAL_ROWS = 33
KNOWN_LEVEL_WORD_CREDENTIAL_TRACKS = 0
KNOWN_SPLIT_CREDENTIAL_TRACKS = 0
LEVEL_WORDS = {"Explorer", "Builder", "Practitioner", "Lead"}


def test_credential_naming_debt_does_not_grow():
    """Credentials must name an accomplishment, not a level. The legacy
    import left 1,228 rows whose credential is the bare word "Practitioner";
    that scope is pinned so new content cannot repeat the mistake."""
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    offenders = [r for r in rows if r["credential"].strip() in LEVEL_WORDS]
    tracks = {(r["pack"], r["track"]) for r in offenders if r["track"]}
    check("level-word credentials do not grow",
          len(offenders) <= KNOWN_LEVEL_WORD_CREDENTIAL_ROWS,
          f"{len(offenders)} rows, baseline {KNOWN_LEVEL_WORD_CREDENTIAL_ROWS}")
    check("level-word credential tracks do not grow",
          len(tracks) <= KNOWN_LEVEL_WORD_CREDENTIAL_TRACKS,
          f"{len(tracks)} tracks, baseline {KNOWN_LEVEL_WORD_CREDENTIAL_TRACKS}")
    # every pack shipped since the import must be clean
    legacy = {"Basic Life Skills & Self-Reliance", "Preventive Health & Everyday Care",
              "Water, Land & Climate", "Care Across a Life", "Making, Repair & Reuse",
              "Empathy & Emotional Intelligence"}
    new_offenders = sorted({r["pack"] for r in offenders} - legacy)
    check("no pack outside the legacy import has level-word credentials",
          not new_offenders, f"{new_offenders}")


# ---------------------------------------------------------------- honesty stances
LOCAL_NUMBER = re.compile(r"\b(?:Local|Lodge|Chapter|Branch)\s+(?:No\.?\s*)?\d+", re.I)


def test_no_union_local_numbers():
    """The regional council is the front door — local/chapter numbers are
    deliberately absent so no page implies a specific local's endorsement."""
    unions = (ROOT / "data" / "unions" / "trade_unions.json").read_text(encoding="utf-8")
    hits = LOCAL_NUMBER.findall(unions)
    check("unions fact base: no local numbers", not hits, f"{hits[:5]}")
    for app in ("trades-network", "louisiana"):
        hits = LOCAL_NUMBER.findall(app_html(app))
        check(f"{app}: no local numbers", not hits, f"{hits[:5]}")


def test_simulation_is_not_certification():
    t = app_html("trades-network")
    check("trades: simulation-vs-certification stance present",
          re.search(r"(?:never|not|no)\b[^.]{0,80}(?:certification|certif)", t, re.I) is not None
          or "simulation is not" in t.lower())


def test_access_profiles_are_not_diagnoses():
    types = json.loads((ROOT / "data" / "learners" / "learner_types.json").read_text(encoding="utf-8"))
    n = len(types["types"])
    check("20 access profiles", n == 20, f"{n}")
    t = app_html("louisiana")
    check("louisiana: 'never diagnoses' stance present",
          re.search(r"never\s+(?:a\s+)?diagnos", t, re.I) is not None)
    # no profile text may frame itself as a diagnosis or disorder label
    banned = re.compile(r"\b(?:diagnos\w+|disorder|deficit|impairment)\b", re.I)
    offenders = [x["id"] for x in types["types"]
                 if banned.search(json.dumps(x, ensure_ascii=False))]
    check("no profile text uses diagnostic language", not offenders, f"{offenders}")


def test_wlb_disclaimer_verbatim():
    """The Institute disclaimer travels verbatim wherever the model is shown."""
    inst = json.loads((ROOT / "data" / "wlb" / "institute.json").read_text(encoding="utf-8"))
    disc = inst["disclaimer"].strip()
    check("disclaimer is substantial", len(disc) > 80, f"{len(disc)} chars")
    for app in ("louisiana", "states"):
        t = app_html(app)
        # the payload is JSON-encoded into the page, so compare on the
        # JSON-escaped form as well as the raw one
        encoded = json.dumps(disc, ensure_ascii=False)[1:-1]
        check(f"{app}: WLB disclaimer verbatim", disc in t or encoded in t)


# ---------------------------------------------------------------- working models
def test_credential_threshold_is_fifty():
    """A credential is earned at exactly the 50th recorded check — the
    number appears in the ledger, the assessor flow and the demo loop."""
    la = app_html("louisiana")
    check("louisiana: ledger credits at 50", ">=50" in la or ">= 50" in la)
    px = app_html("platform")
    check("platform: demo loop uses the 50-check line", ">=50" in px or ">= 50" in px)


def test_evidence_export_is_consent_gated():
    """The consent box gates the export in code, not merely in copy."""
    la = app_html("louisiana")
    check("louisiana: evidence consent control present", "ev-consent" in la)
    check("louisiana: export button disabled until consent",
          re.search(r"ev-export[^\n]{0,400}disabled|disabled[^\n]{0,400}ev-consent", la) is not None
          or re.search(r'#ev-export"\)\.disabled', la) is not None)


def test_education_os_shell():
    """The generated shell must cover every view the app declares — one
    missing container and route() activates nothing."""
    t = app_html("education-os")
    views = re.findall(r'<section class="view" id="v-([\w-]+)"></section>', t)
    check("education-os: shell generated for every view", len(views) >= 149, f"{len(views)} sections")
    check("education-os: view ids unique", len(views) == len(set(views)))
    for required in ("nav", "toast", "crumb", "stateSel", "stateflag"):
        check(f"education-os: #{required} exists for boot code", f'id="{required}"' in t)
    check("education-os: hidden-unless-active rule present", ".view.active" in t)


# The classes the app's 143 renderers actually emit, by usage. Each needs a
# rule or the view renders as unstyled markup — which is how the app shipped
# for 44 releases. Ordered as in the builder's stylesheet.
EDU_REQUIRED_RULES = [
    ".view{", ".view.active{", ".card{", ".eyebrow{", ".section{", ".vhead{",
    ".grid{", ".grid.g2{", ".grid.g3{", ".grid.g4{", ".stat{", ".stat .v{",
    ".stat .l{", ".btn{", ".tabs{", ".tab{", ".pill{", ".field{", ".slider{",
    ".check{", ".term{", ".bar{", ".flagrow{", ".tl{", ".heat{", ".note{",
    ".tablewrap{", ".legend{", "dl.kv{", ".small{",
]
# Tokens the renderers reference inline as var(--x); an undefined one renders
# as an invalid value and the element loses its colour entirely.
EDU_REQUIRED_TOKENS = [
    "--ink", "--ink2", "--bg", "--bg2", "--bg3", "--card", "--line", "--line2",
    "--gold", "--gold2", "--gold-soft", "--teal", "--ok", "--good", "--warn",
    "--crit", "--radius", "--display", "--body", "--mono", "--osa", "--osw",
]


def test_education_os_design_system():
    """The generated stylesheet must cover what the renderers emit, in both
    themes. (--seq*, --seq-ink, --seq-wash, --gold-ink and --mark-line are
    defined by the app's own injected stylesheet and are not redefined.)"""
    t = app_html("education-os")
    missing = [r for r in EDU_REQUIRED_RULES if r not in t]
    check("education-os: every emitted class has a rule", not missing, f"missing {missing}")
    undefined = [tok for tok in EDU_REQUIRED_TOKENS if f"{tok}:" not in t]
    check("education-os: every referenced token is defined", not undefined, f"missing {undefined}")
    # both dark paths: the media query for system preference and the explicit
    # override, exactly as the other five apps do it
    check("education-os: dark theme via prefers-color-scheme",
          'prefers-color-scheme:dark' in t or 'prefers-color-scheme: dark' in t)
    check("education-os: dark theme via explicit data-theme",
          ':root[data-theme="dark"]' in t)
    check("education-os: reduced motion honoured", "prefers-reduced-motion" in t)


# The culture trades (v0.48.0): three trade packs and the Makers' Hall fact
# base behind the Louisiana app's Makers view. Every named person comes from
# the public record and the note must say naming is not endorsement.
CULTURE_PACKS = {
    "MUSICIND": "Music : Creation to Industry",
    "CULINARY": "Culinary Trades : The Louisiana Kitchen",
    "ARTCRAFT": "Arts & Craft Trades : Louisiana Makers",
}


def test_culture_trade_packs():
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    for slug, name in CULTURE_PACKS.items():
        mine = [r for r in rows if r["pack"] == name]
        check(f"{slug}: 250 blocks in the dataset", len(mine) == 250, f"{len(mine)}")
        check(f"{slug}: block_ids carry the slug", all(r["block_id"].startswith(f"CX-{slug}-") for r in mine))
        check(f"{slug}: five tracks", len({r["track"] for r in mine}) == 5)
        check(f"{slug}: no level-word credentials",
              not any(r["credential"].strip() in LEVEL_WORDS for r in mine))
    unions = json.loads((ROOT / "data" / "unions" / "trade_unions.json").read_text(encoding="utf-8"))
    fam = {f["family"]: f["packs"] for f in unions["families"]}
    check("unions: Musicians back the music pack", "MUSICIND" in fam.get("Musicians", []))
    check("unions: culinary workers back the culinary pack",
          "CULINARY" in fam.get("Culinary & hospitality workers", []))
    check("unions: stagehands & exhibition workers back the arts pack",
          "ARTCRAFT" in fam.get("Stagehands & exhibition workers", []))
    check("unions: still 37 families (no new family for the culture trades)", len(fam) == 37, str(len(fam)))


def test_makers_fact_base():
    M = json.loads((ROOT / "data" / "louisiana" / "makers.json").read_text(encoding="utf-8"))
    fb = json.loads((ROOT / "data" / "louisiana" / "fact_base.json").read_text(encoding="utf-8"))
    parishes = {p[0] for p in fb["parishes"]}
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    tracks = {(r["pack"], r["track"]) for r in rows if r["track"]}
    note = M.get("note", "")
    check("makers: note says naming is not endorsement", "not endorsement" in note and "public record" in note)
    check("makers: note leaves living local practitioners to the community", "name their own" in note)
    discs = M["disciplines"]
    check("makers: three disciplines", [d["id"] for d in discs] == ["music", "culinary", "arts"])
    seen = set()
    for d in discs:
        check(f"makers/{d['id']}: pack is a culture-trade pack", CULTURE_PACKS.get(d["pack"]) == d["packName"])
        check(f"makers/{d['id']}: five stages, each one real track of the pack",
              len(d["stages"]) == 5 and all((d["packName"], st["track"]) in tracks for st in d["stages"]),
              str([st["track"] for st in d["stages"]]))
        stage_ids = {st["id"] for st in d["stages"]}
        check(f"makers/{d['id']}: every stage has roles", all(len(st["roles"]) >= 5 for st in d["stages"]))
        check(f"makers/{d['id']}: at least ten makers", len(d["figures"]) >= 10, str(len(d["figures"])))
        for f in d["figures"]:
            key = ("name", "years", "parish", "place", "craft", "stage", "did", "lesson", "check")
            empty = [k for k in key if not str(f.get(k, "")).strip()]
            check(f"maker {f.get('name', '?')}: no empty field", not empty, str(empty))
            check(f"maker {f['name']}: parish is a real parish", f["parish"] in parishes, f["parish"])
            check(f"maker {f['name']}: stage is on the pathway", f["stage"] in stage_ids, f["stage"])
            check(f"maker {f['name']}: named once", f["name"] not in seen); seen.add(f["name"])
        for o in d["orgs"]:
            check(f"org {o['name']}: parish is a real parish", o["parish"] in parishes, o["parish"])
    regions = {p[0]: fb["regions"][p[1]] for p in fb["parishes"]}
    covered = {regions[f["parish"]] for d in discs for f in d["figures"]}
    check("makers: every region has at least one maker", covered == set(fb["regions"][1:]),
          str(set(fb["regions"][1:]) - covered))


# The 50-state compliance layer (v0.51.0): a checklist, not legal advice —
# the file must say so, every fee must carry an as-of year and a verify flag,
# every state must be one of the fifty, and every domain must be present.
def test_state_compliance_layer():
    c = json.loads((ROOT / "data" / "states" / "compliance.json").read_text(encoding="utf-8"))
    fb = json.loads((ROOT / "data" / "states" / "states.json").read_text(encoding="utf-8"))
    abbrs = [s["abbr"] for s in fb["states"]]
    check("compliance: note says it is not legal advice", "NOT LEGAL ADVICE" in c["note"] and "verify" in c["note"])
    check("compliance: disclaimer present", "Not legal advice" in c["disclaimer"])
    check("compliance: fifty states, same set as the fact base", sorted(s["abbr"] for s in c["states"]) == sorted(abbrs))
    dom = [d["id"] for d in c["domains"]]
    check("compliance: eleven domains (breach notification added v0.57.0)", len(dom) == 11 and "breach" in dom, str(dom))
    fees_seen = 0
    for s in c["states"]:
        missing = [d for d in dom if d not in s]
        check(f"compliance/{s['abbr']}: every domain present", not missing, str(missing))
        check(f"compliance/{s['abbr']}: homeschool tier valid", s["homeschool"]["tier"] in ("none", "low", "moderate", "high"))
        check(f"compliance/{s['abbr']}: apprenticeship type valid", s["apprenticeship"]["type"] in ("SAA", "OA"))
        check(f"compliance/{s['abbr']}: privacy tier valid", s["privacy"]["tier"] in ("operator-law", "baseline"))
        check(f"compliance/{s['abbr']}: cost roll-up sane",
              0 <= s["cost"]["one_time"]["low"] <= s["cost"]["one_time"]["high"] and 0 <= s["cost"]["annual"]["low"] <= s["cost"]["annual"]["high"] and s["cost"]["verify"] is True)
        check(f"compliance/{s['abbr']}: sources listed", len(s["sources"]) >= 3)
        b = s["breach"]
        check(f"compliance/{s['abbr']}: breach entry complete and flagged verify",
              b["law"] and b["deadline"] and b["regulator"] and b["verify"] is True and b["asOf"] == c["asOf"]
              and (b["deadline_days"] is None or 30 <= b["deadline_days"] <= 60))
        for d in dom:
            for k, v in s[d].items():
                if isinstance(v, dict) and "verify" in v and "asOf" in v:
                    fees_seen += 1
                    check(f"compliance/{s['abbr']}/{d}/{k}: fee flagged verify with as-of year",
                          v["verify"] is True and v["asOf"] == c["asOf"] and (v["amount"] is not None or v["band"]))
    check("compliance: fees carry verify flags (many)", fees_seen >= 400, str(fees_seen))
    check("compliance: the stance survives", "Simulation ≠ certification" in c["states"][0]["cte"]["note"] or "simulation" in c["national"]["apprenticeship"]["note"].lower())
    # the report must match the data (CI regenerates it; this holds the headline)
    doc = (ROOT / "docs" / "STATE_COMPLIANCE.md").read_text(encoding="utf-8")
    reg = sum(1 for s in c["states"] if s["charity"]["required"])
    check("STATE_COMPLIANCE.md current: charity count", f"**{reg}** states require charitable-solicitation" in doc)
    check("STATE_COMPLIANCE.md carries the disclaimer", "Not legal advice" in doc)


# The accessibility audit (v0.53.0): tools/a11y/audit.js writes
# docs/ACCESSIBILITY.json from axe-core over every route of every app. The
# committed result must carry no WCAG-tagged violation; best-practice rules
# (heading-order) are documented deviations, not failures.
def test_accessibility_audit_is_clean():
    d = json.loads((ROOT / "docs" / "ACCESSIBILITY.json").read_text(encoding="utf-8"))
    check("a11y: audit covers every app", {r["label"].split(" ")[0] for r in d["runs"]} >=
          {"louisiana", "flow-hub", "trades-network", "states", "platform", "education-os"})
    check("a11y: at least 40 views audited", len(d["runs"]) >= 40, str(len(d["runs"])))
    wcag = [(r["label"], v["id"], v["nodes"]) for r in d["runs"] for v in r["violations"]
            if any(t.startswith("wcag") for t in v["tags"])]
    check("a11y: zero WCAG-tagged violations", not wcag, str(wcag[:5]))
    serious = [(r["label"], v["id"]) for r in d["runs"] for v in r["violations"] if v["impact"] in ("serious", "critical")]
    check("a11y: zero serious or critical violations", not serious, str(serious[:5]))
    check("a11y: every focusable control has an accessible name",
          not any(r["keyboard"]["noName"] for r in d["runs"]))
    check("a11y: no click-only div/span controls", not any(r["keyboard"]["clickOnly"] for r in d["runs"]))
    doc = (ROOT / "docs" / "ACCESSIBILITY.md").read_text(encoding="utf-8")
    check("ACCESSIBILITY.md names what remains", "heading-order" in doc and "remains" in doc.lower())


def test_simulation_studio():
    """The Simulation Studio (v0.54.0): the fact base is sound, every app
    carries the one engine and the honesty lines, and a run can never be
    mistaken for a check."""
    sys.path.insert(0, str(ROOT / "tools"))
    from validate_simulations import validate, load
    doc = load()
    errs = validate(doc)
    check("sims: fact base validates", not errs, "; ".join(errs[:3]))
    check("sims: 18 scenarios", len(doc["scenarios"]) == 18, str(len(doc["scenarios"])))
    check("sims: nine trades kinds localized by region",
          len({s["kind"] for s in doc["scenarios"] if s.get("kind")}) == 9)
    check("sims: every scenario carries its track's transfer check verbatim",
          all(s["transfer"]["check"] and s["transfer"]["block_id"] for s in doc["scenarios"]))
    engine = (ROOT / "tools" / "sim" / "engine.js").read_text(encoding="utf-8")
    check("sims: engine never touches the network or storage",
          not re.search(r"\b(fetch|XMLHttpRequest|localStorage|sessionStorage|indexedDB|navigator\.sendBeacon)\b", engine))
    check("sims: engine is deterministic (no Math.random)", "Math.random" not in engine)
    check("sims: engine has no timers driving play", "setTimeout" not in engine and "setInterval" not in engine)
    for app in ("education-os", "flow-hub", "louisiana", "trades-network", "states", "platform"):
        t = app_html(app)
        check(f"sims: {app} carries the engine", "Cognition.X Simulation Studio — the shared scenario engine" in t)
        check(f"sims: {app} carries the run record format", "cx-simrun/1" in t)
        check(f"sims: {app} carries the studio law verbatim", doc["law"] in t or doc["law"].replace("\u2260", "≠") in t)
        check(f"sims: {app} says a run is never a credential", "never a credential" in t)
        check(f"sims: {app} has no __CXSIM__ placeholder left", "__CXSIM__" not in t)
    sdoc = (ROOT / "docs" / "SIMULATION.md").read_text(encoding="utf-8")
    check("SIMULATION.md states the scenario count", f"{len(doc['scenarios'])} scenarios" in sdoc)
    check("SIMULATION.md carries the law", "Simulation ≠ certification" in sdoc)


def test_app_compliance_review():
    """v0.55.0 — the review of the apps themselves, held mechanically:
    no third-party request on load, a browser-enforced no-network policy,
    no referrer leakage, and an in-app disclosure with an erase control."""
    priv = json.loads((ROOT / "data" / "policy" / "privacy.json").read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT / "tools"))
    from runtime_lib import CSP, APPS as RT, font_faces
    check("compliance: CSP blocks every connection", "connect-src 'none'" in CSP and "default-src 'none'" in CSP)
    check("compliance: CSP allows no eval", "unsafe-eval" not in CSP)
    for app in APPS:
        t = app_html(app)
        check(f"compliance: {app} carries the CSP meta", f'http-equiv="Content-Security-Policy" content="{CSP}"' in t)
        check(f"compliance: {app} sends no referrer", '<meta name="referrer" content="no-referrer">' in t)
        check(f"compliance: {app} loads no Google Fonts", "fonts.googleapis.com" not in t and "fonts.gstatic.com" not in t)
        faces = t.count("@font-face")
        want = font_faces(RT[app]["fonts"]).count("@font-face")
        check(f"compliance: {app} embeds its typefaces once each ({want} faces)", faces == want, f"{faces} @font-face rules")
        if want:
            check(f"compliance: {app} fonts are data: URIs", "src:url(data:font/woff2;base64," in t)
        check(f"compliance: {app} carries the Data & privacy notice", 'id = "cx-privbtn"' in t and "window.CX_PRIVACY=" in t)
        check(f"compliance: {app} notice text is canonical", priv["leaves"] in t and priv["erase_label"] in t)
        check(f"compliance: {app} no __CXHEAD__ placeholder left", "__CXHEAD__" not in t)
        # the Education OS carries one deliberate probe — new Function('return 1') inside a try —
        # that reports whether a CSP is active; nothing else may construct code from text
        probes = 1 if app == "education-os" else 0
        check(f"compliance: {app} has no eval", re.search(r"[^\w.$]eval\s*\(", t) is None and t.count("new Function(") <= probes)
    for key in ("stays", "leaves", "exports", "minors", "rights", "security", "not_advice"):
        check(f"privacy notice: {key} present", bool(priv.get(key)))
    check("privacy notice: says nothing leaves on its own", "Nothing leaves this page on its own" in priv["leaves"])
    check("privacy notice: is not legal advice", "not legal advice" in priv["not_advice"])
    doc = (ROOT / "docs" / "COMPLIANCE_REVIEW.md").read_text(encoding="utf-8")
    for needle in ("not legal advice", "FERPA", "COPPA", "Content-Security-Policy", "Data map", "Findings"):
        check(f"COMPLIANCE_REVIEW.md mentions {needle}", needle in doc)
    lic = (ROOT / "docs" / "LICENSING.md").read_text(encoding="utf-8")
    check("LICENSING.md covers the embedded typefaces (OFL)", "Open Font License" in lic)
    check("fonts: licence file present", (ROOT / "data" / "fonts" / "LICENSE-OFL.txt").exists())


def test_standards_and_rubrics():
    """v0.56.0 — standards mappings and transfer-check rubrics: valid against
    the dataset, honest about strength, and surfaced where assessors work."""
    sys.path.insert(0, str(ROOT / "tools"))
    from validate_standards import validate as validate_standards
    errs, cov = validate_standards()
    check("standards: mappings and rubrics validate", not errs, "; ".join(errs[:3]))
    check("standards: at least two frameworks", len(cov["frameworks"]) >= 2)
    check("standards: at least two packs mapped", cov["blocks_covered"] >= 200, str(cov["blocks_covered"]))
    check("rubrics: the 30 core-spine tracks", cov["tracks_with_rubric"] == 30, str(cov["tracks_with_rubric"]))
    for p in sorted((ROOT / "data" / "standards").glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        check(f"standards: {p.name} never claims an external alignment", d["strength"] != "aligns")
        check(f"standards: {p.name} caveat says verify", "verify" in d["caveat"].lower())
    la = app_html("louisiana")
    check("louisiana: track rubrics embedded", "Common failure modes" in la and '"byTrack"' in la)
    fh = app_html("flow-hub")
    check("flow hub: standards embedded with the caveat", "HS-ETS1-3" in fh and "verify each code against the current" in fh.lower())
    check("flow hub: rubrics embedded", "How an assessor reads a check on this track" in fh)
    doc = (ROOT / "docs" / "STANDARDS.md").read_text(encoding="utf-8")
    check("STANDARDS.md states the coverage", f"{cov['blocks_covered']} of 17,450 blocks" in doc and f"{cov['tracks_with_rubric']} of {cov['tracks']} tracks" in doc)
    dq = (ROOT / "docs" / "DATA_QUALITY.md").read_text(encoding="utf-8")
    check("DATA_QUALITY.md reports standards coverage", "## Standards and rubrics" in dq)


def test_security_compliance_register():
    """v0.57.0 — the control register validates and every evidence reference
    resolves; release checksums are current; the security policy, the youth
    hazard lines and the adopter templates exist."""
    sys.path.insert(0, str(ROOT / "tools"))
    import hashlib
    from controls_report import validate as validate_controls
    reg = json.loads((ROOT / "data" / "policy" / "controls.json").read_text(encoding="utf-8"))
    errs = validate_controls(reg)
    check("register: validates and every evidence reference resolves", not errs, "; ".join(errs[:3]))
    check("register: at least forty controls across six levels", len(reg["controls"]) >= 40 and len({c["level"] for c in reg["controls"]}) == 6)
    check("register: every platform control that is met carries a test, smoke or CI evidence",
          all(any(e["type"] in ("test", "smoke", "ci") for e in c["evidence"]) for c in reg["controls"] if c["level"] == "platform" and c["status"] == "met"))
    sums = (ROOT / "apps" / "CHECKSUMS.sha256").read_text(encoding="utf-8").splitlines()
    for line in sums:
        if line.startswith("#") or not line.strip():
            continue
        digest, path = line.split("  ", 1)
        check(f"checksums: {path} current", hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest)
    check("checksums: all six apps listed", sum(1 for l in sums if l.endswith("/index.html")) == 6)
    sec = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
    check("SECURITY.md names a reporting channel and the checksum step", "Report" in sec and "CHECKSUMS.sha256" in sec)
    sims = json.loads((ROOT / "data" / "simulations" / "scenarios.json").read_text(encoding="utf-8"))
    check("studio: every trades scenario carries an under-18 hazard line",
          all("Under 18" in s.get("youth", "") for s in sims["scenarios"] if s.get("kind")))
    check("studio: youth note is not legal advice", "NOT LEGAL ADVICE" in sims["youth_note"])
    for app in ("trades-network", "louisiana"):
        check(f"studio: {app} carries the youth lines", "Hazardous Occupations Orders" in app_html(app))
    for t in ("DATA_PROCESSING_STATEMENT", "INCIDENT_RESPONSE_RUNBOOK", "RECORDS_CUSTODY_STATEMENT", "DEVICE_AND_DATA_HYGIENE"):
        check(f"templates: {t} exists and is not legal advice", "Not legal advice" in (ROOT / "docs" / "templates" / f"{t}.md").read_text(encoding="utf-8"))
    hyg = (ROOT / "docs" / "templates" / "DEVICE_AND_DATA_HYGIENE.md").read_text(encoding="utf-8")
    check("hygiene sheet: ten rules, a yearly re-sign, and the runbook named", hyg.count("\n1. **") == 1 and "10. **" in hyg and "Once a year" in hyg and "INCIDENT_RESPONSE_RUNBOOK.md" in hyg and "ST-03" in hyg)
    check("register: no open item remains (v0.64.0)", not [c["id"] for c in reg["controls"] if c["status"] == "open"], str([c["id"] for c in reg["controls"] if c["status"] == "open"]))
    la_hall = app_html("louisiana")
    check("hall checklist: the device-sheet line names the hygiene sheet and the MOU line the city clerk's permit", "DEVICE_AND_DATA_HYGIENE.md" in la_hall and "city clerk" in la_hall and "PA-01 · ST-03" in la_hall and "PA-04 · LO-02" in la_hall)
    la = app_html("louisiana")
    check("louisiana: private key never exported (no extractable sign key)", 'namedCurve:"P-256"}, true, ["sign"]' not in la and 'generateKey({name:"ECDSA", namedCurve:"P-256"}, false' in la)
    check("louisiana: durable ledger store and custody bundle present", "cxla.ledgerdb" in la and "cx-custody/1" in la and "HALL_REQS" in la)
    import hashlib as _h
    sbom = json.loads((ROOT / "sbom" / "cognitionx.cdx.json").read_text(encoding="utf-8"))
    apps_in = [c for c in sbom["components"] if c["type"] == "application"]
    check("sbom: CycloneDX 1.5 with the six apps", sbom["bomFormat"] == "CycloneDX" and sbom["specVersion"] == "1.5" and len(apps_in) == 6)
    check("sbom: app hashes current", all(_h.sha256((ROOT / c["properties"][0]["value"]).read_bytes()).hexdigest() == c["hashes"][0]["content"] for c in apps_in))
    check("sbom: four typeface families listed under OFL", len({c["name"] for c in sbom["components"] if c["type"] == "file"}) == 4 and all(c["licenses"][0]["license"]["id"] == "OFL-1.1" for c in sbom["components"] if c["type"] == "file"))
    check("sbom: dev toolchain excluded from the shipped scope", all(c.get("scope") == "excluded" for c in sbom["components"] if c["type"] == "library"))
    check("sbom: declares zero runtime dependencies", any(p["name"] == "cx:runtime_dependencies" and p["value"] == "0" for p in sbom["metadata"]["properties"]))
    from runtime_lib import CSP as _CSP
    hosting = (ROOT / "docs" / "HOSTING.md").read_text(encoding="utf-8")
    check("HOSTING.md carries the exact CSP as a header", _CSP in hosting and "Strict-Transport-Security" in hosting and "no-referrer" in hosting)
    cisa = (ROOT / "docs" / "CISA_K12_SUMMARY.md").read_text(encoding="utf-8")
    check("CISA summary maps to register ids", "PL-01" in cisa and "ST-02" in cisa and "Not legal advice" in cisa)
    road = (ROOT / "docs" / "COMPLIANCE_ROADMAP.md").read_text(encoding="utf-8")
    check("COMPLIANCE_ROADMAP.md states the register counts", f"{len(reg['controls'])} controls" in road)


def test_open_badge_envelope():
    """v0.60.0 — the Open Badges 3.0 / VC 2.0 envelope: present in the app,
    documented, pseudonymous by design, and verifiable from the command line."""
    la = app_html("louisiana")
    check("ob3: the app issues vc+jwt with did:jwk", '"vc+jwt"' in la and "did:jwk:" in la and "OpenBadgeCredential" in la)
    check("ob3: the subject stays pseudonymous (no subject id, unhashed nickname labelled so)", 'identityType: "name", hashed: false' in la and "credentialSubject.id" not in la)
    check("ob3: the native payload rides inside the envelope", '"cx:record": p' in la)
    check("ob3: the honest-scope wording travels in the narrative", "criteria: {narrative: p.note + \" \" + rec.verify}" in la)
    v = (ROOT / "tools" / "verify_record.js").read_text(encoding="utf-8")
    check("cli verifier: no dependencies, both forms, four grades", "require(\"fs\")" in v and "vc+jwt" in v and "cx-credential/1" in v and all(g in v for g in ("INVALID", "VALID", "TRUSTED", "REVOKED")) and "require(\"node_modules" not in v)
    doc = (ROOT / "docs" / "CREDENTIALS.md").read_text(encoding="utf-8")
    check("CREDENTIALS.md states what a signature proves and does not", "does not prove who" in doc and "out-of-band" in doc and "Revoked outranks trusted" in doc)


def test_v1_gate_materials():
    """v0.61.0 — the v1.0 gate is executable: the board packet, the cohort
    onboarding path and its consent sheet match the code, and the cohort
    report runs on the sample evidence."""
    import subprocess
    packet = (ROOT / "docs" / "BOARD_PACKET.md").read_text(encoding="utf-8")
    src = {r["pack"] for r in csv.DictReader(open(ROOT / "data" / "source" / "Cognition.X_all_blocks.csv", newline="", encoding="utf-8"))}
    packs = json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))["packs"]
    mach = [p for p in packs if p["name"] not in src]
    check("board packet: standing queue counts match the dataset", f"**{len(mach)} packs, {sum(p['blocks'] for p in mach):,} blocks**" in packet)
    check("board packet: every machine-authored pack is in the queue", all(f"(`{p['slug']}`)" in packet for p in mach))
    check("board packet: the 24 proposed names are the first decision", packet.count("| Basic Life Skills") + packet.count("| Care Across") + packet.count("| Making,") + packet.count("| Preventive") + packet.count("| Water, Land") == 24 and "First decision" in packet)
    check("board packet: the six-point checklist is a form", all(f"| {i} |" in packet for i in range(1, 7)) and "Reviewer:" in packet)
    onb = (ROOT / "docs" / "COHORT_ONBOARDING.md").read_text(encoding="utf-8")
    consent = (ROOT / "docs" / "templates" / "CONSENT_FORM.md").read_text(encoding="utf-8")
    la = app_html("louisiana")
    check("consent: says nothing is sent and the browser blocks it — true (CSP connect-src 'none')", "cannot send anything anywhere" in consent and "connect-src 'none'" in la)
    check("consent: says only a nickname, band and supports are asked — true", "first name or a nickname" in consent and "a first name or nickname" in la and "Nothing here needs a legal name" in la)
    check("consent: aggregate export is optional and nameless — true", "no names in it" in consent and "per-track counts only" in la and "I choose to export this aggregate" in la)
    check("consent: simulation is practice — true", "never a check and never a credential" in consent and "never a credential" in la)
    check("onboarding: key exchange is out-of-band with a confirmation step", "out-of-band" in onb and "confirm the office name" in onb)
    check("onboarding: names the checksum step and the unmodified-release rule", "sha256sum -c apps/CHECKSUMS.sha256" in onb and "unmodified" in onb)
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "cohort_report.py")], capture_output=True, text=True, cwd=ROOT)
    check("cohort report: runs on the sample evidence", r.returncode == 0, r.stderr[-200:])
    for sec in ("## 1. The cohort at a glance", "## 3. Revision priorities", "## 5. Standing-queue status", "## 6. The v1.0 gate"):
        check(f"cohort report: has section {sec[3:24]}", sec in r.stdout)
    check("cohort report: evidence proposes, the board disposes", "Evidence proposes; the board disposes" in r.stdout)


def test_durable_lists_and_restore():
    """v0.62.0 — the trust and revocation lists take the ledger's durable
    path and a custody bundle restores by merge; the register, the review
    and the onboarding path say so."""
    la = app_html("louisiana")
    check("durable lists: the accessors route through the seam", 'function trustLoad(){ return dlLoad("cxla.trust"); }' in la and 'function revlistsSave(l){ return dlSave("cxla.revlists", l); }' in la)
    check("durable lists: the seam writes through to IndexedDB and announces a refused save", "async function dlInit()" in la and "cxla.dmeta" in la and "refused to save the " in la)
    check("durable lists: startup initializes the seam", "llInit(); dlInit();" in la)
    check("restore: the merge never overwrites from an older bundle", "async function restoreCustody(" in la and 'if (!cur){ d.learners.push(l); out.learnersAdded++; }' in la and "else if (newer && " in la)
    check("restore: revocation lists are re-verified and a foreign office's revoked ids are skipped", "await verifyRecord(doc)" in la and "out.revokedSkipped = b.revoked.length" in la)
    check("restore: an office is noted by public key only, never with a private key", 'durable: false, restored: true' in la and "e.publicKey.d) continue" in la and "!doc.publicKey.d" in la)
    check("restore: the control is in the Records Office", 'id="ro-restore"' in la and 'id="ro-restore-file"' in la and "No sync service" in la)
    reg = json.loads((ROOT / "data" / "policy" / "controls.json").read_text(encoding="utf-8"))
    pl19 = next(c for c in reg["controls"] if c["id"] == "PL-19")
    check("register: PL-19 covers the lists and the restore with browser evidence", "trust list" in pl19["requirement"] and any(e["ref"] == "testDurableListsAndRestore" for e in pl19["evidence"]))
    check("review: the data map names the durable copy", "cxla.dmeta" in (ROOT / "docs" / "COMPLIANCE_REVIEW.md").read_text(encoding="utf-8"))
    onb = (ROOT / "docs" / "COHORT_ONBOARDING.md").read_text(encoding="utf-8")
    check("onboarding: a second device restores by merge and never receives a private key", "Restore" in onb and "never overwrites" in onb and "private key never travels" in onb)
    check("smoke: the browser suite covers migration, quota and restore", "testDurableListsAndRestore" in (ROOT / "tests" / "browser" / "smoke.js").read_text(encoding="utf-8"))


def test_education_os_canonical_injection():
    """v0.63.0 — the Education OS is built from the canonical fact bases:
    placeholders in the template, JSON injected in place, the extractor a
    clean round trip, each injected layer byte-equal to its file."""
    import subprocess
    sys.path.insert(0, str(ROOT / "tools"))
    from build_education_os import FACT_LAYERS
    tpl = (ROOT / "apps" / "education-os" / "template.html").read_text(encoding="utf-8", errors="replace")
    built = app_html("education-os")
    for name, (rel, pick) in FACT_LAYERS.items():
        check(f"education-os: template holds one placeholder for {name} and no literal", tpl.count(f"__CXFACT:{name}__") == 1 and tpl.count(f"DATA.{name}=") == 1 and f"DATA.{name}=[" not in tpl and f"DATA.{name}={{" not in tpl)
        a = built.find(f"/*cx:{name}*/")
        z = built.find("/*cx:end*/", a)
        canonical = json.dumps(pick(json.loads((ROOT / rel).read_text(encoding="utf-8"))), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        check(f"education-os: {name} injected in place, byte-equal to {rel}", a > 0 and built[a + len(f"/*cx:{name}*/"):z] == canonical)
        check(f"education-os: {name} injected before its first reader", built.find(f"DATA.{name}", a + 1) > a and built.count(f"DATA.{name}=") == 1)
    check("education-os: no __CXFACT placeholder survives the build", "__CXFACT:" not in built)
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "extract_fact_bases.py"), "--check"], capture_output=True, text=True, cwd=ROOT)
    check("extractor: the built app reproduces the canonical files byte for byte", r.returncode == 0 and "would change" not in r.stdout, (r.stdout + r.stderr)[-300:])
    check("extractor: every layer was read from the built app", r.stdout.count("from built app") == len(FACT_LAYERS), r.stdout[-200:])
    inst = json.loads((ROOT / "data" / "wlb" / "institute.json").read_text(encoding="utf-8"))
    check("institute: every principle carries its strands", all(isinstance(x.get("strands"), list) and x["strands"] for x in inst["principles"]))


KNOWN_BAND_SUFFIX_ROWS = 0                  # 11,250 before tranche one (v0.65.0); 10,750; 10,250; 9,750 after tranche three (v0.67.0); 9,250 Corporate OS (v0.72.0); 8,750 Science OS (v0.73.0); 8,250 Robotics OS (v0.74.0); 7,750 Global Health OS (v0.75.0); 7,250 Multilateral OS (v0.76.0); 6,750 Sapient OS (v0.77.0); 6,250 Non-Profit Practice (v0.78.0, all seven sector packs); 5,750 SmartCiti.X New Orleans Trades + States OS (v0.79.0, prompt 2 tranche one); 5,250 Trades in the Classroom + Trades Across School Subjects (v0.80.0, prompt 2 tranche two); 4,500 Music + Culinary Trades + Arts, Making Media & Performance (v0.81.0, prompt 2 tranche three, the three culture packs); 4,000 Digital Life, Data & AI + Law, Contracts & Everyday Rights (v0.82.0, prompt 2 tranche four); 3,500 Preventive Health & Everyday Care + Care Across a Life (v0.83.0, prompt 2 tranche five, the life-skills family begins); 3,000 Water, Land & Climate + Making, Repair & Reuse (v0.84.0, prompt 2 tranche six); 2,500 Arts & Craft Trades : Louisiana Makers + Energy, Grid & the Home (v0.85.0, prompt 2 tranche seven); 1,750 the three Civic Leadership Legacy packs (v0.86.0, prompt 2 tranche eight); 1,000 Food, Cooking & Nutrition + Learning States & Universal Access + Transport & Mobility (v0.87.0, prompt 2 tranche nine, the last pack-spec-based packs); 500 Housing & Tenancy + Money, Benefits & Entitlements (v0.88.0, prompt 2 tranche ten, the first override-based community packs); 0 Reentry & Recovery Pathways + Neighbourhood, Safety & Civic Voice (v0.89.0, prompt 2 tranche eleven, the last two community packs — prompt 2 closed, every band-suffix row in the dataset now carries an authored sentence); the ratchet only falls
BAND_AUTHORED_PACKS = {"Emergency Preparedness & First Response", "Parish Launch & Scale",
                       "Civic Leadership Legacy : Louisiana", "Basic Life Skills & Self-Reliance",
                       "Cognition.X : Louisiana OS", "SmartCiti.X : New Orleans Trades",
                       "Cognition.X : States OS", "Trades in the Classroom : Flipped & Gamified",
                       "Trades Across School Subjects", "Music : Creation to Industry",
                       "Culinary Trades : The Louisiana Kitchen", "Arts, Making Media & Performance",
                       "Digital Life, Data & AI", "Law, Contracts & Everyday Rights",
                       "Preventive Health & Everyday Care", "Care Across a Life",
                       "Water, Land & Climate", "Making, Repair & Reuse",
                       "Arts & Craft Trades : Louisiana Makers", "Energy, Grid & the Home",
                       "Civic Leadership Legacy : The Institute Model",
                       "Civic Leadership Legacy : California", "Civic Leadership Legacy : Texas",
                       "Food, Cooking & Nutrition", "Learning States & Universal Access",
                       "Transport & Mobility"}
BAND_AUTHORED_THEMES = {"Cognition.X : Louisiana OS": 100}   # two spec parts, one pack
# packs whose source rows carried the suffix and were overridden through an
# `override: band-suffix` promotion (v0.72.0): themes overridden, rows expected
BAND_OVERRIDDEN_PACKS = {"Cognition.X : Corporate OS": (100, 500), "Cognition.X : Science OS": (100, 500), "Cognition.X : Robotics OS": (100, 500), "Cognition.X : Global Health OS": (100, 500), "Cognition.X : Multilateral OS": (100, 500), "Cognition.X : Sapient OS": (100, 500), "Non-Profit Practice": (100, 500), "Housing & Tenancy": (50, 250), "Money, Benefits & Entitlements": (50, 250), "Reentry & Recovery Pathways": (50, 250), "Neighbourhood, Safety & Civic Voice": (50, 250)}


def test_band_differentiated_descriptions():
    """v0.65.0 — roadmap prompt 6, tranche one: per-band descriptions flow
    through the pipeline; the packs that carry them have five distinct
    sentences per theme and no suffix; the dataset-wide suffix count never
    rises again; the generator refuses malformed bands."""
    import re, subprocess, tempfile
    sys.path.insert(0, str(ROOT / "tools"))
    from generate_pack import band_description, BAND_LABELS
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    suffix = re.compile(r"— at .{1,20}$")
    suffixed = [r for r in rows if suffix.search(r["description"].strip())]
    check("band descriptions: the suffix count never rises", len(suffixed) <= KNOWN_BAND_SUFFIX_ROWS, f"{len(suffixed)} rows, baseline {KNOWN_BAND_SUFFIX_ROWS}")
    for pack in BAND_AUTHORED_PACKS:
        pr = [r for r in rows if r["pack"] == pack]
        by_theme = {}
        for r in pr:
            by_theme.setdefault(r["theme"], []).append(r["description"])
        check(f"band descriptions: {pack} — no row carries the suffix", not [r for r in pr if suffix.search(r["description"])])
        check(f"band descriptions: {pack} — five distinct sentences per theme, {BAND_AUTHORED_THEMES.get(pack, 50)} themes", len(by_theme) == BAND_AUTHORED_THEMES.get(pack, 50) and all(len(v) == 5 and len(set(v)) == 5 for v in by_theme.values()))
        check(f"band descriptions: {pack} — every description is a full sentence that says what the learner does", all(len(r["description"]) >= 40 and r["description"].endswith(".") for r in pr))
    good = {"theme": "t", "description": "d", "bands": {b: f"Do the {i} thing." for i, b in enumerate(BAND_LABELS)}}
    check("generator: an authored band sentence is used verbatim", band_description(good, "6–8") == "Do the 2 thing.")
    check("generator: without bands the shared sentence is suffixed", band_description({"theme": "t", "description": "d"}, "K–2") == "d — at K–2")
    for bad in ({"bands": {b: "same." for b in BAND_LABELS}}, {"bands": {b: f"x{i}" for i, b in enumerate(BAND_LABELS[:4])}}, {"bands": {b: f"x{i} — at K–2" for i, b in enumerate(BAND_LABELS)}}):
        try:
            band_description({"theme": "t", "description": "d", **bad}, "K–2"); ok = False
        except ValueError:
            ok = True
        check("generator: refuses duplicate, missing or suffixed band sentences", ok)
    specs = {}
    for d in ("pack_specs", "promotions"):
        for p in (ROOT / "data" / d).glob("*.json"):
            specs.setdefault(json.loads(p.read_text(encoding="utf-8"))["pack"], []).append(p)
    for pack in BAND_AUTHORED_PACKS:
        parts = [json.loads(p.read_text(encoding="utf-8")) for p in specs[pack]]
        check(f"spec: {pack} carries bands on every theme", all("bands" in th for s in parts for t in s["tracks"] for th in t["themes"]))
    # v0.72.0 — the band-suffix override: counted, suffix-only, refused otherwise
    from normalize_blocks import override_description, BANDS
    dq = (ROOT / "docs" / "DATA_QUALITY.md").read_text(encoding="utf-8")
    total_over = 0
    for pack, (themes_n, rows_n) in BAND_OVERRIDDEN_PACKS.items():
        pr = [r for r in rows if r["pack"] == pack and r["track"]]
        by_theme = {}
        for r in pr:
            by_theme.setdefault((r["track"], r["theme"]), []).append(r["description"])   # a theme name may recur across tracks
        check(f"override: {pack} — no tracked row carries the suffix", not [r for r in pr if suffix.search(r["description"])])
        check(f"override: {pack} — {themes_n} themes with five distinct sentences", len(by_theme) == themes_n and all(len(v) == 5 and len(set(v)) == 5 for v in by_theme.values()), str(len(by_theme)))
        check(f"override: {pack} — every sentence is a full sentence that says what the learner does", all(len(r["description"]) >= 40 and r["description"].endswith(".") for r in pr))
        check(f"override: {pack} — the rows' track, code and credential are untouched", all(r["code"] and r["credential"] for r in pr) and len(pr) == rows_n, str(len(pr)))
        promo = [p for p in (ROOT / "data" / "promotions").glob("*.json") if json.loads(p.read_text(encoding="utf-8"))["pack"] == pack]
        check(f"override: {pack} — declared as an override promotion with bands on every theme", promo and json.loads(promo[0].read_text(encoding="utf-8")).get("override") == "band-suffix")
        total_over += rows_n
    check("override: the dashboard counts the exception", f"replaced by an authored band sentence: **{total_over:,}**" in dq)
    good = {b: f"Do the {i} thing for real." for i, b in enumerate(BANDS)}
    check("override: a suffix row for its own band is replaced", override_description({"code": "X-1", "pack": "p", "theme": "t", "grade": "6–8", "description": "Shared sentence — at 6–8"}, good) == "Do the 2 thing for real.")
    check("override: an empty description is left to the fill-empty path", override_description({"code": "X-1", "pack": "p", "theme": "t", "grade": "6–8", "description": ""}, good) is None)
    for bad_row, bad_bands in (({"description": "An authored sentence that must never be overwritten."}, good), ({"description": "Shared — at 9–10"}, good), ({"description": "Shared — at 6–8"}, {b: "same." for b in BANDS})):
        try:
            override_description({"code": "X-1", "pack": "p", "theme": "t", "grade": "6–8", **bad_row}, bad_bands); ok = False
        except SystemExit:
            ok = True
        check("override: refuses an authored target, a wrong band and malformed bands", ok)
    packs_by_slug = {p["slug"]: p["name"] for p in json.loads((ROOT / "data" / "manifest.json").read_text(encoding="utf-8"))["packs"]}
    spine = {packs_by_slug.get(r["pack"], r["pack"]) for r in json.loads((ROOT / "data" / "rubrics" / "core_spine.json").read_text(encoding="utf-8"))["rubrics"]}
    check("core spine: every core-spine pack is band-authored (v0.67.0)", spine <= BAND_AUTHORED_PACKS, str(sorted(spine - BAND_AUTHORED_PACKS)))


# v0.90.0 — prompt 3 tranche one: foundation packs where each theme names
# exactly one row (not five spanning the band ladder), promoted with
# `"unbanded": true` so the empty description fills in as one complete
# sentence with no per-band suffix.
UNBANDED_FILLED_PACKS = {"Future-Work"}

KNOWN_EMPTY_DESCRIPTION_ROWS = 6089  # 6,200 before prompt 3 (docs/NEXT_STEPS_2.md #3); 6,089 after Future-Work (v0.90.0, prompt 3 tranche one, 111 rows); the ratchet only falls


def test_unbanded_descriptions():
    """v0.90.0 — prompt 3 tranche one: a foundation pack where each theme
    names exactly one row (not five spanning the band ladder) is promoted
    with `"unbanded": true` (tools/normalize_blocks.py `apply_promotions`,
    `unbanded_description`); its description fills in as one complete
    sentence, never a per-band suffix, since the row's own grade column
    already says which band it is. Plain fill-empty, not a new counted
    exception: the field starts empty and stays that way until a
    promotion supplies it — so the dataset's empty-description count only
    falls, and it is never overwritten once filled."""
    sys.path.insert(0, str(ROOT / "tools"))
    from normalize_blocks import unbanded_description
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    empty = [r for r in rows if not r["description"].strip()]
    check("unbanded fill: the empty-description count never rises", len(empty) <= KNOWN_EMPTY_DESCRIPTION_ROWS, f"{len(empty)} rows, baseline {KNOWN_EMPTY_DESCRIPTION_ROWS}")
    suffix = re.compile(r"— at .{1,20}$")
    for pack in UNBANDED_FILLED_PACKS:
        pr = [r for r in rows if r["pack"] == pack]
        check(f"unbanded fill: {pack} — no row is empty", pr and all(r["description"].strip() for r in pr))
        check(f"unbanded fill: {pack} — no row carries the band suffix", not [r for r in pr if suffix.search(r["description"])])
        check(f"unbanded fill: {pack} — every description is a full sentence", all(len(r["description"]) >= 40 and r["description"].endswith(".") for r in pr))
        check(f"unbanded fill: {pack} — descriptions are distinct (one row per theme)", len({r["description"] for r in pr}) == len(pr))
        promo = [p for p in (ROOT / "data" / "promotions").glob("*.json") if json.loads(p.read_text(encoding="utf-8"))["pack"] == pack]
        check(f"unbanded fill: {pack} — declared as an unbanded promotion", promo and json.loads(promo[0].read_text(encoding="utf-8")).get("unbanded") is True)
    check("normalize_blocks: unbanded_description accepts a full sentence",
          unbanded_description("Do the real task correctly, on your own, without any help at all.")
          == "Do the real task correctly, on your own, without any help at all.")
    for bad in ("too short.", "No trailing period", "A sentence with a suffix that is long enough — at 6–8"):
        check(f"normalize_blocks: unbanded_description refuses {bad!r}", unbanded_description(bad) is None)


FOOTPRINT_BUDGET_MB = {"education-os": 6.5, "flow-hub": 2.6, "louisiana": 1.0, "platform": 0.3, "states": 0.65, "trades-network": 0.5}


def test_footprint_budget():
    """v0.68.0 — every built app stays under its byte budget (docs/PERFORMANCE.md);
    the performance pass's structural changes hold."""
    for app, mb in FOOTPRINT_BUDGET_MB.items():
        size = (ROOT / "apps" / app / "index.html").stat().st_size
        check(f"footprint: {app} within {mb} MB", size <= mb * 1e6, f"{size/1e6:.2f} MB — raise the budget in docs/PERFORMANCE.md and here, with the reason")
    perf = (ROOT / "docs" / "PERFORMANCE.md").read_text(encoding="utf-8")
    check("PERFORMANCE.md states the budgets the test holds", all(f"| {app} | {mb} MB |" in perf for app, mb in FOOTPRINT_BUDGET_MB.items()))
    ed = app_html("education-os"); tpl = (ROOT / "apps" / "education-os" / "template.html").read_text(encoding="utf-8", errors="replace")
    check("education-os: the sector library is injected in place, once, with no trailing overlay", ed.count("/*cx:sectorBlocks*/") == 1 and "CX canonical overlay" not in ed and "DATA.cxCanonical={version:" in ed)
    check("education-os: the template holds the placeholder and no literal rounds", tpl.count("__CXFACT:sectorBlocks__") == 1 and "DATA.sectorBlocks=DATA.sectorBlocks.concat(" not in tpl)
    la = app_html("louisiana"); ltpl = (ROOT / "apps" / "louisiana" / "template.html").read_text(encoding="utf-8", errors="replace")
    check("louisiana: both Voronoi grids ship precomputed and the marker region exists for the precompute tool", '"voronoi":{"state":{"gw":132,"gh":90' in la and '"curr":{"gw":132' in la and "/* @cx-voronoi-begin */" in ltpl and "/* @cx-voronoi-end */" in ltpl and "function tessFromPre(" in ltpl)
    check("perf tooling present", (ROOT / "tools" / "perf.js").exists() and (ROOT / "tools" / "voronoi_precompute.js").exists())


def test_xr_integration():
    """v0.69.0 — the WebXR view of a studio run: one engine in six apps, no
    network, storage or randomness, valid cx-xrscene/1 and glTF 2.0 output,
    the honesty lines on the sign, and the privacy, register and hosting
    lines that go with it."""
    import subprocess
    xr = (ROOT / "tools" / "xr" / "engine.js").read_text(encoding="utf-8")
    check("xr: engine never touches the network or storage", not re.search(r"\b(fetch|XMLHttpRequest|localStorage|sessionStorage|indexedDB|navigator\.sendBeacon|WebSocket)\b", xr))
    check("xr: engine is deterministic (no Math.random)", "Math.random" not in xr)
    check("xr: engine requests no hand, eye or face tracking feature", '"hand-tracking"' not in xr and "eye-tracking" not in xr and "face-tracking" not in xr)
    check("xr: only the viewer pose is used, per frame, and the note says so", "getViewerPose" in xr and "nothing about where you look or move is recorded" in xr)
    check("xr: optionalFeatures ask for the floor reference only", 'optionalFeatures: ["local-floor"]' in xr and "hand-tracking" not in xr)
    for app in ("education-os", "flow-hub", "louisiana", "trades-network", "states", "platform"):
        t = app_html(app)
        check(f"xr: {app} carries the XR engine and the studio offers it", "Cognition.X Studio in space" in t and "Open in 3D / VR" in t)
    js = ("require(process.argv[1]); require(process.argv[2]); const fb = require(process.argv[3]); CXSIM.configure(fb);"
          "const sc = fb.scenarios[0]; const plan = CXSIM.plan(CXSIM.localize(sc, 'the yard'), 3, 'seed-1');"
          "const scene = CXXR.scene(sc, 'the yard', plan); const g = CXXR.gltf(scene); const buf = Buffer.from(g.buffers[0].uri.split(',')[1], 'base64');"
          "console.log(JSON.stringify({format: scene.format, total: scene.nodes.length, stations: scene.nodes.filter(n => n.kind === 'station').length, plan: plan.length, law: scene.nodes.find(n => n.kind === 'sign').text, note: scene.note,"
          " v: g.asset.version, nodes: g.nodes.length, bufOk: buf.length === g.buffers[0].byteLength, acc: g.accessors.length, extras: g.nodes.every(n => n.extras && n.extras.cx && n.extras.cx.scenario === sc.id), score: /\"s\":|score/.test(JSON.stringify(g))}));")
    r = subprocess.run(["node", "-e", js, str(ROOT / "tools" / "sim" / "engine.js"), str(ROOT / "tools" / "xr" / "engine.js"), str(ROOT / "data" / "simulations" / "scenarios.json")], capture_output=True, text=True, cwd=ROOT)
    check("xr: scene and glTF writers run in node", r.returncode == 0, r.stderr[-300:])
    if r.returncode == 0:
        o = json.loads(r.stdout.strip().splitlines()[-1])
        sims = json.loads((ROOT / "data" / "simulations" / "scenarios.json").read_text(encoding="utf-8"))
        check("xr: cx-xrscene/1 has one station per decision point and the law on the sign", o["format"] == "cx-xrscene/1" and o["stations"] == o["plan"] and o["law"] == sims["law"] and "never a credential" in o["note"])
        check("xr: glTF 2.0 is well formed — one node per scene node, accessors, embedded buffer, scenario extras, no score", o["v"] == "2.0" and o["nodes"] == o["total"] and o["total"] >= o["stations"] + 3 and o["bufOk"] and o["acc"] == 3 and o["extras"] and not o["score"])
    js2 = ("require(process.argv[1]); require(process.argv[2]); const fb = require(process.argv[3]); CXSIM.configure(fb);"
           "const sc = fb.scenarios.find(s => s.youth); const plan = CXSIM.plan(CXSIM.localize(sc, 'the yard'), 3, 'seed-1'); const scene = CXXR.scene(sc, 'the yard', plan); const g = CXXR.gltf(scene);"
           "const r1 = CXXR.parseGltf(JSON.stringify(g));"
           "const jt = JSON.stringify(Object.assign({}, g, {buffers: [{byteLength: g.buffers[0].byteLength}]})); const bin = Buffer.from(g.buffers[0].uri.split(',')[1], 'base64'); const pad = n => (4 - n % 4) % 4; const jb = Buffer.from(jt);"
           "const total = 28 + jb.length + pad(jb.length) + bin.length + pad(bin.length); const out = Buffer.alloc(total); out.writeUInt32LE(0x46546C67, 0); out.writeUInt32LE(2, 4); out.writeUInt32LE(total, 8);"
           "let o = 12; out.writeUInt32LE(jb.length + pad(jb.length), o); out.writeUInt32LE(0x4E4F534A, o + 4); jb.copy(out, o + 8); out.fill(0x20, o + 8 + jb.length, o + 8 + jb.length + pad(jb.length)); o += 8 + jb.length + pad(jb.length);"
           "out.writeUInt32LE(bin.length + pad(bin.length), o); out.writeUInt32LE(0x004E4942, o + 4); bin.copy(out, o + 8);"
           "const r2 = CXXR.parseGltf(out.buffer.slice(out.byteOffset, out.byteOffset + out.length)); let refused = false; try { CXXR.parseGltf(JSON.stringify(Object.assign({}, g, {buffers: [{byteLength: 1, uri: 'room.bin'}]}))); } catch (e) { refused = /fetches nothing/.test(e.message); }"
           "console.log(JSON.stringify({signs: scene.nodes.filter(n => n.kind === 'sign').map(n => n.id), n: g.nodes.length, m1: r1.meshes.length, t1: r1.triangles, m2: r2.meshes.length, t2: r2.triangles, floor: Math.abs(Math.min(...r2.meshes.map(m => m.model[13] + 0))) >= 0, refused}));")
    r2 = subprocess.run(["node", "-e", js2, str(ROOT / "tools" / "sim" / "engine.js"), str(ROOT / "tools" / "xr" / "engine.js"), str(ROOT / "data" / "simulations" / "scenarios.json")], capture_output=True, text=True, cwd=ROOT)
    check("xr: room reader round-trips our own glTF as JSON and as GLB, and refuses external buffers", r2.returncode == 0, r2.stderr[-300:])
    if r2.returncode == 0:
        o2 = json.loads(r2.stdout.strip().splitlines()[-1])
        check("xr: a trades scenario's room carries the law, the simulated and live lists and the under-18 line as signs", set(o2["signs"]) >= {"sign", "sign-simulated", "sign-live", "sign-youth"})
        check("xr: every exported node comes back as a 12-triangle mesh from both containers", o2["m1"] == o2["n"] and o2["t1"] == o2["n"] * 12 and o2["m2"] == o2["n"] and o2["t2"] == o2["n"] * 12 and o2["refused"])
    priv = json.loads((ROOT / "data" / "policy" / "privacy.json").read_text(encoding="utf-8"))
    check("privacy: the notice covers XR sessions", "WebXR" in priv["security"] and "never records it" in priv["security"] and "no hand, eye or face tracking" in priv["security"])
    reg = json.loads((ROOT / "data" / "policy" / "controls.json").read_text(encoding="utf-8"))
    check("register: PL-21 holds the XR control as met", any(c["id"] == "PL-21" and c["status"] == "met" for c in reg["controls"]))
    hosting = (ROOT / "docs" / "HOSTING.md").read_text(encoding="utf-8")
    check("hosting: xr-spatial-tracking allowed to self, camera still denied by policy", hosting.count("xr-spatial-tracking=(self)") >= 4 and "camera=()" in hosting)
    review = (ROOT / "docs" / "XR_REVIEW.md").read_text(encoding="utf-8")
    check("XR_REVIEW.md takes the stances", all(k in review for k in ("WebXR", "glTF 2.0", "No hand, eye or face tracking", "never a check, never a credential", "No platform integrations", "Not legal advice")))


def test_docs_numbers_match_dataset():
    """Headline counts in the README and wiki must match the dataset."""
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    blocks, packs = len(rows), len({r["pack"] for r in rows})
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("README block count current", f"{blocks:,}" in readme, f"expected {blocks:,}")
    check("README pack count current", f"{packs} packs" in readme, f"expected {packs} packs")
    home = (ROOT / "docs" / "wiki" / "Home.md").read_text(encoding="utf-8")
    check("wiki Home block count current", f"{blocks:,}" in home, f"expected {blocks:,}")


def test_system_review_2():
    """v0.71.0 — the second system review's claims are held: the documents
    exist with the shape they promise, their numbers match the sources they
    cite, the stale claims it corrected stay corrected, and the tools it
    committed are the ones the claims rest on."""
    import subprocess
    rev = (ROOT / "docs" / "SYSTEM_REVIEW_2.md").read_text(encoding="utf-8")
    nxt = (ROOT / "docs" / "NEXT_STEPS_2.md").read_text(encoding="utf-8")
    # the register's counts, as the review states them
    c = json.loads((ROOT / "data" / "policy" / "controls.json").read_text(encoding="utf-8"))
    cs = c["controls"] if isinstance(c, dict) else c
    n, met, part, opn = len(cs), *[sum(1 for x in cs if x["status"] == k) for k in ("met", "partial", "open")]
    check("review 2: register counts match", f"{n} controls — {met} met, {part} partial, {opn} open" in rev, f"{n}/{met}/{part}/{opn}")
    # the dataset numbers, as the review and the dashboard state them
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    empty = sum(1 for r in rows if not r["description"].strip())
    suffix = sum(1 for r in rows if re.search(r"— at [^—]+$", r["description"]))
    # the review is a snapshot at v0.70.0; both debts only ever fall, so its figures bound the current ones
    rev_empty = int(re.search(r"(\d[\d,]*) rows \(\d+%\) have no description", rev).group(1).replace(",", ""))
    rev_suffix = int(re.search(r"(\d[\d,]*) rows \(\d+%\) carry one sentence", rev).group(1).replace(",", ""))
    check("review 2: empty-description count has not risen since the review", empty <= rev_empty, f"{empty} vs {rev_empty}")
    check("review 2: band-suffix count has not risen since the review", suffix <= rev_suffix, f"{suffix} vs {rev_suffix}")
    real = len({r["credential"] for r in rows} - {"Explorer", "Builder", "Practitioner", "Lead"})
    dq = (ROOT / "docs" / "DATA_QUALITY.md").read_text(encoding="utf-8")
    check("data quality headline counts real credentials", f"{real:,} credentials**" in dq, str(real))
    check("wiki Home agrees on credentials", f"{real:,} credentials" in (ROOT / "docs" / "wiki" / "Home.md").read_text(encoding="utf-8"))
    # the accessibility re-run covers the studio and its XR room
    a11y = json.loads((ROOT / "docs" / "ACCESSIBILITY.json").read_text(encoding="utf-8"))
    labels = [r["label"] for r in a11y["runs"]]
    check("a11y: the studio and the XR room are audited views", any("studio open" in l for l in labels) and any("Open in 3D / VR" in l for l in labels))
    check("a11y: at least 47 views audited", len(a11y["runs"]) >= 47, str(len(a11y["runs"])))
    check("review 2: audit view count matches", f"**{len(a11y['runs'])} views**" in rev)
    check("audit runner carries the in-page steps", "STEPS" in (ROOT / "tools" / "a11y" / "audit.js").read_text(encoding="utf-8"))
    # the next ten prompts have the shape the first ten had
    heads = re.findall(r"^## (\d+) — ", nxt, re.M)
    check("next steps 2: ten numbered prompts", heads == [str(i) for i in range(1, 11)], str(heads))
    for part_name in ("**Why.**", "**Evidence.**", "**Steps.**", "**Acceptance.**"):
        check(f"next steps 2: every prompt has {part_name}", nxt.count(part_name) >= 10, str(nxt.count(part_name)))
    check("next steps 2: standing rules carried forward", "Never overwrite a non-empty source field" in nxt and "A simulation is practice" in nxt)
    check("first prompt set marked complete", "> **Complete.**" in (ROOT / "docs" / "NEXT_STEPS_OPUS5.md").read_text(encoding="utf-8"))
    # the corrected claims stay corrected
    roadmap = (ROOT / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
    check("roadmap no longer lists shipped work as open", "Open: the full WCAG" not in roadmap and "Remaining federation work: W3C" not in roadmap)
    xr_lines = len((ROOT / "tools" / "xr" / "engine.js").read_text(encoding="utf-8").splitlines())
    m = re.search(r"~(\d+) lines", (ROOT / "docs" / "XR_REVIEW.md").read_text(encoding="utf-8"))
    check("XR review states the engine's size within 15%", m and abs(int(m.group(1)) - xr_lines) <= xr_lines * 0.15, f"doc {m and m.group(1)} vs {xr_lines}")
    # the tools the claims rest on are in the repository
    sweep = (ROOT / "tools" / "view_sweep.js").read_text(encoding="utf-8")
    check("view sweep tool committed with a compare mode", "--compare" in sweep and "normalise" in sweep)
    tags = (ROOT / "tools" / "release_tags.py").read_text(encoding="utf-8")
    check("release-tag checker exists and CI runs it", "--check" in tags and "release_tags.py --check" in (ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8"))
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "release_tags.py"), "--backfill", "--dry-run"], capture_output=True, text=True, cwd=ROOT)
    check("release-tag backfill runs", r.returncode == 0 and "tags" in r.stdout, r.stdout[-120:] + r.stderr[-120:])
    check("versioning wiki still documents the tag step", "git tag -a vX.Y.Z" in (ROOT / "docs" / "wiki" / "Versioning-and-Releases.md").read_text(encoding="utf-8"))


def main():
    for fn in [v for k, v in sorted(globals().items()) if k.startswith("test_")]:
        try:
            fn()
        except Exception as exc:  # a broken test is a failure, not a crash
            FAILURES.append(f"{fn.__name__} raised {type(exc).__name__}: {exc}")
    print(f"ran {CHECKS[0]} checks")
    if FAILURES:
        print(f"\nFAILED ({len(FAILURES)}):")
        for f in FAILURES:
            print(f"  ✗ {f}")
        return 1
    print("OK: every platform invariant holds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
