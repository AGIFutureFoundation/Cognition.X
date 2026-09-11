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
ALLOWED_HOSTS = {"fonts.googleapis.com", "fonts.gstatic.com", "github.com", "www2.ed.gov"}
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


# A level word is not a credential. 1,228 rows imported in v0.1.0 name their
# credential "Practitioner" — documented debt, pinned here as a ratchet so the
# defect can only shrink. Lower these numbers when the review board authors
# the real credential names; never raise them.
KNOWN_LEVEL_WORD_CREDENTIAL_ROWS = 1228
KNOWN_LEVEL_WORD_CREDENTIAL_TRACKS = 24
KNOWN_SPLIT_CREDENTIAL_TRACKS = 1
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


def test_docs_numbers_match_dataset():
    """Headline counts in the README and wiki must match the dataset."""
    rows = list(csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8")))
    blocks, packs = len(rows), len({r["pack"] for r in rows})
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    check("README block count current", f"{blocks:,}" in readme, f"expected {blocks:,}")
    check("README pack count current", f"{packs} packs" in readme, f"expected {packs} packs")
    home = (ROOT / "docs" / "wiki" / "Home.md").read_text(encoding="utf-8")
    check("wiki Home block count current", f"{blocks:,}" in home, f"expected {blocks:,}")


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
