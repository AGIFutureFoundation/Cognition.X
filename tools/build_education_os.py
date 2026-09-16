#!/usr/bin/env python3
"""Build the Education OS app from its template + the canonical dataset.

Roadmap Phase 2: apps/education-os/index.html is now a BUILD PRODUCT.
The base is apps/education-os/template.html (the last hand-grown "gov"
build, kept verbatim as the app shell and legacy content). This tool
injects the sector master-block library as it stands in data/blocks.csv
IN PLACE of the template's own copy (a __CXFACT:sectorBlocks__ placeholder
since v0.68.0; before that a trailing overlay replaced the template's 96
literal rounds after the fact) — so edits to the dataset flow into the
app, and the app's sector library has exactly one source of truth.

Field fidelity: the app renders each row's task and outcome separately;
blocks.csv stores them joined in transfer_check. The extraction sidecar
data/generated/app-master-blocks.map.json preserves the original
boundary per code. When a dataset row's check still equals the joined
original, the overlay re-emits the original [task, outcome]; when the
dataset row was edited, the edited check ships as the task with the
outcome left empty — the dataset wins.

Since v0.63.0 the Louisiana fact base, the K-12 program and the WLB
Institute fact base are injected IN PLACE too (see FACT_LAYERS): the
template holds a placeholder where each literal stood, so one source of
truth serves every app and the template no longer carries a copy that
could drift.

Output stays a single offline file, per the app's standing constraint.
Deterministic: same inputs -> same output.
"""

import csv
import json
import sys
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "apps" / "education-os" / "template.html"
OUT = ROOT / "apps" / "education-os" / "index.html"
MAP = ROOT / "data" / "generated" / "app-master-blocks.map.json"

PACK_SECTOR = {
    "Cognition.X : Corporate OS": "corp",
    "Cognition.X : Science OS": "sci",
    "Cognition.X : Robotics OS": "rob",
    "Cognition.X : Global Health OS": "gh",
    "Cognition.X : Multilateral OS": "mlt",
    "Cognition.X : Sapient OS": "sap",
    "Cognition.X : Education OS": "edu",
    "Non-Profit Practice": "npo",
}


# ---------------------------------------------------------------- the shell
# The v0.1.0 import captured the app's JavaScript — 149 view definitions and
# 143 renderers — but not the HTML shell they render into, nor the app's
# stylesheet. The result never ran: buildNav() threw on a missing #nav, no
# .view element existed for route() to activate, and a stray unwrapped
# `var DATA = {...}` block printed as visible page text.
#
# The shell is not invented here: it is DERIVED from the app's own VIEWS
# array, which carries every view's id, title, ordinal and nav group. This
# restores the app's structure and navigation. Its visual design is a
# separate matter — the imported stylesheet is gone, so the generated shell
# carries only the layout rules the app's own code depends on (a view is
# hidden unless active), plus a plain readable frame. See docs/DATA_REVIEW.md.

STUB = re.compile(
    r'<div class="container">.*?</div>\s*\n\s*var DATA = \{.*?\n\};\s*\n',
    re.S)

SHELL_CSS = """
  /* ---- tokens ------------------------------------------------------
     Recovered from the application itself, not invented: the gold, teal,
     ink and field values are the ones the app documents in its own brand
     view ("Gold — first contact", "Teal — application", "Ink — the
     keystone"); the status and rail values come from its DATA.vizTok
     fallbacks; the sequential scale, --seq-ink, --seq-wash, --gold-ink
     and --mark-line are already defined by the app's own injected
     stylesheet and are deliberately NOT redefined here. Only the tones
     between the documented anchors (--ink2, --bg3) are derived.
     The app's stated rule is honoured throughout: never decorated —
     flat ground or its own field, no gradients, no decorative shadow. */
  :root{
    --ink:#0E1E2E; --ink2:#3A4A59; --fg:#0E1E2E; --muted:#3A4A59;
    --bg:#F4F7F9; --bg2:#FFFFFF; --bg3:#EEF3F6; --card:#FFFFFF;
    --line:#DFE5EA; --line2:#C9D3D9;
    --gold:#B8871F; --gold2:#B8860B; --gold-soft:rgba(184,135,31,.10);
    --teal:#1E7A72; --term-teal:#176E66;
    --ok:#1F7A4D; --good:#1F7A4D; --warn:#96530A; --crit:#B22B2B;
    --osa:#176E66; --osw:#F0F6F6; --s:#176E66;
    --radius:10px; --shadow:0 1px 2px rgba(14,30,46,.06);
    --display:"Roboto Flex",Inter,system-ui,-apple-system,"Segoe UI",sans-serif;
    --body:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
    --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  }
  @media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
    --ink:#E6EDF3; --ink2:#9FB1C1; --fg:#E6EDF3; --muted:#9FB1C1;
    --bg:#0B1B2B; --bg2:#122536; --bg3:#17293A; --card:#10263A;
    --line:#24394C; --line2:#2F4759;
    --gold:#E7C56A; --gold2:#E7C56A; --gold-soft:rgba(231,197,106,.14);
    --teal:#4FC3B6; --term-teal:#63CEC1;
    --ok:#5FBF7C; --good:#5FBF7C; --warn:#E0A050; --crit:#E66767;
    --osa:#63CEC1; --osw:#123832; --s:#63CEC1;
    --shadow:0 1px 2px rgba(0,0,0,.4);
  }}
  :root[data-theme="dark"]{
    --ink:#E6EDF3; --ink2:#9FB1C1; --fg:#E6EDF3; --muted:#9FB1C1;
    --bg:#0B1B2B; --bg2:#122536; --bg3:#17293A; --card:#10263A;
    --line:#24394C; --line2:#2F4759;
    --gold:#E7C56A; --gold2:#E7C56A; --gold-soft:rgba(231,197,106,.14);
    --teal:#4FC3B6; --term-teal:#63CEC1;
    --ok:#5FBF7C; --good:#5FBF7C; --warn:#E0A050; --crit:#E66767;
    --osa:#63CEC1; --osw:#123832; --s:#63CEC1;
    --shadow:0 1px 2px rgba(0,0,0,.4);
  }

  /* ---- base -------------------------------------------------------- */
  *{box-sizing:border-box}
  html{color-scheme:light dark}
  body{margin:0;background:var(--bg);color:var(--ink);
       font:15px/1.6 var(--body);-webkit-text-size-adjust:100%}
  h1,h2,h3,h4{font-family:var(--display);line-height:1.2;margin:0 0 .4em;
              letter-spacing:-.01em;text-wrap:balance}
  h1{font-size:clamp(1.7rem,3.4vw,2.3rem);font-weight:800}
  h2{font-size:1.22rem;font-weight:700}
  h3{font-size:1.02rem;font-weight:700}
  h4{font-size:.92rem;font-weight:700}
  p{margin:0 0 .8em}
  a{color:var(--teal)}
  a:hover{color:var(--ink)}
  b,strong{font-weight:650}
  hr,.sep{border:0;border-top:1px solid var(--line);margin:16px 0}
  ul,ol{margin:0 0 .8em;padding-left:1.2em}
  li{margin:.2em 0}
  :focus-visible{outline:2px solid var(--gold);outline-offset:2px;border-radius:3px}
  img,svg{max-width:100%}

  /* ---- the frame --------------------------------------------------- */
  #cx-shell{display:flex;min-height:100vh;align-items:flex-start}
  #nav{flex:0 0 268px;position:sticky;top:0;max-height:100vh;overflow-y:auto;
       background:var(--bg2);border-right:1px solid var(--line);padding:16px 10px 28px}
  #nav .grp{font-family:var(--mono);font-size:10px;text-transform:uppercase;
            letter-spacing:.14em;color:var(--ink2);margin:16px 9px 6px;font-weight:600}
  #nav .grp:first-child{margin-top:2px}
  .navbtn{display:flex;gap:9px;align-items:baseline;width:100%;text-align:left;
          border:0;background:none;color:var(--ink);padding:7px 9px;border-radius:7px;
          font:inherit;font-size:13.5px;cursor:pointer;line-height:1.35}
  .navbtn:hover{background:var(--bg3)}
  .navbtn.active{background:var(--gold-soft);color:var(--ink);font-weight:650;
                 box-shadow:inset 2px 0 0 var(--gold)}
  .navbtn .k{font-family:var(--mono);color:var(--ink2);font-size:10.5px;min-width:2em}
  #cx-main{flex:1;min-width:0;padding:20px clamp(16px,3vw,36px) 80px}
  #cx-topbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 18px}
  #crumb{color:var(--ink2);font-size:.8rem;flex:1;min-width:140px}
  #cx-editionlab{font-family:var(--mono);font-size:10px;text-transform:uppercase;
                 letter-spacing:.12em;color:var(--ink2)}
  #stateSel{padding:5px 8px;font:inherit;font-size:.82rem;background:var(--bg2);
            color:var(--ink);border:1px solid var(--line2);border-radius:var(--radius)}
  #stateflag{font-family:var(--mono);font-size:10.5px;color:var(--ink2);
             border:1px solid var(--line);border-radius:999px;padding:2px 10px}
  .view{display:none}
  .view.active{display:block}
  #toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);
         background:var(--ink);color:var(--bg2);padding:9px 16px;border-radius:999px;
         font-size:.85rem;opacity:0;pointer-events:none;transition:opacity .18s;z-index:60}
  #toast.show{opacity:1}

  /* ---- layout ------------------------------------------------------ */
  .vhead{margin:0 0 18px;padding-bottom:14px;border-bottom:1px solid var(--line)}
  .section{margin:0 0 26px}
  .section>h2{margin-bottom:.5em}
  .grid{display:grid;gap:14px;align-items:start}
  .grid.g2{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
  .grid.g3{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}
  .grid.g4{grid-template-columns:repeat(auto-fit,minmax(168px,1fr))}
  .tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);
             background:var(--bg2)}
  .tablewrap table{margin:0;border:0}

  /* ---- surfaces ---------------------------------------------------- */
  .card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
        padding:15px 17px;min-width:0}
  .card>h3:first-child,.card>h2:first-child{margin-top:0}
  .card>:last-child{margin-bottom:0}
  .eyebrow{font-family:var(--mono);font-size:10px;text-transform:uppercase;
           letter-spacing:.14em;color:var(--ink2);margin:0 0 6px;font-weight:600}
  .lede,.lead{font-size:1.02rem;color:var(--ink2);max-width:72ch}
  .small{font-size:.82rem}
  .muted,.dim{color:var(--ink2)}
  .mono{font-family:var(--mono);font-size:.86em}
  /* a11y (v0.53.0): the app's own CSS paints ids and codes in #b8860b (3.0:1 on
     the page ground); the shell overrides that one colour with the brand's
     gold-ink, which reads at 4.5:1+ on every surface in both themes */
  summary .mono,td .mono,th .mono,.id .mono,.card .mono,.row .mono{color:var(--gold-ink)!important}
  details details>summary{color:var(--gold-ink)!important}
  .note{font-size:.82rem;color:var(--ink2);background:var(--bg3);border-radius:8px;
        padding:9px 12px;margin:8px 0}
  .term{font-family:var(--mono);font-size:12px;line-height:1.55;background:var(--ink);
        color:var(--term-teal);border-radius:var(--radius);padding:12px 14px;
        overflow:auto;min-height:120px;max-height:340px;white-space:pre-wrap;
        word-break:break-word}

  /* ---- the stat tile: .v is the value, .l the label ----------------- */
  .stat{background:var(--bg2);border:1px solid var(--line);border-radius:var(--radius);
        padding:13px 15px;min-width:0}
  .stat .v{font-family:var(--display);font-weight:800;font-size:27px;line-height:1.05;
           color:var(--ink);letter-spacing:-.015em;display:block}
  .stat .v small{font-size:.42em;font-weight:600;color:var(--ink2);margin-left:.35em;
                 letter-spacing:0}
  .stat .l{font-size:.78rem;color:var(--ink2);line-height:1.4;margin-top:5px}
  .stat .k,.k{font-family:var(--mono);font-size:10px;text-transform:uppercase;
              letter-spacing:.1em;color:var(--ink2)}

  /* ---- controls ---------------------------------------------------- */
  .btn{font:inherit;font-size:.85rem;border:1px solid var(--line2);background:var(--bg2);
       color:var(--ink);border-radius:var(--radius);padding:6px 13px;cursor:pointer;
       line-height:1.4}
  .btn:hover{border-color:var(--ink2)}
  .btn.primary,.primary{background:var(--gold);border-color:var(--gold);color:#1A1206;
                        font-weight:650}
  .btn.primary:hover{filter:brightness(1.05)}
  .btn.ghost,.ghost{background:none;border-color:var(--line)}
  .btn[disabled],.btn:disabled{opacity:.5;cursor:not-allowed}
  .tabs{display:flex;gap:4px;flex-wrap:wrap;margin:0 0 12px;border-bottom:1px solid var(--line)}
  .tab{font:inherit;font-size:.84rem;border:0;background:none;color:var(--ink2);
       padding:7px 12px;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px}
  .tab:hover{color:var(--ink)}
  .tab.active,.tab[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--gold);
                                         font-weight:650}
  .pill{display:inline-block;font-size:.74rem;border:1px solid var(--line2);
        border-radius:999px;padding:2px 10px;color:var(--ink2);margin:2px 4px 2px 0;
        white-space:nowrap}
  .pill.gold,.gold{color:var(--gold-ink);border-color:var(--gold2)}
  .pill.teal,.teal{color:var(--teal);border-color:var(--teal)}
  .pill.good,.good{color:var(--ok);border-color:var(--ok)}
  .pill.warn,.warn{color:var(--warn);border-color:var(--warn)}
  .pill.crit,.crit{color:var(--crit);border-color:var(--crit)}
  .field{display:block;margin:0 0 10px;min-width:0}
  .field label,.slider label{display:block;font-size:.78rem;color:var(--ink2);margin:0 0 4px}
  .field input,.field select,.field textarea,.slider input[type=range]{
    width:100%;font:inherit;font-size:.88rem;padding:6px 9px;color:var(--ink);
    background:var(--bg2);border:1px solid var(--line2);border-radius:8px}
  .field textarea{min-height:80px;resize:vertical}
  .slider{margin:0 0 12px}
  .slider label small{display:block;font-size:.72rem;color:var(--ink2);font-weight:400}
  .slider input[type=range]{padding:0;accent-color:var(--teal)}
  .check{display:flex;gap:8px;align-items:flex-start;font-size:.86rem;margin:5px 0;
         cursor:pointer}
  .check input{margin-top:.25em;accent-color:var(--teal)}

  /* ---- data display ------------------------------------------------ */
  table{width:100%;border-collapse:collapse;font-size:.86rem}
  th,td{text-align:left;padding:8px 11px;border-bottom:1px solid var(--line);
        vertical-align:top}
  th{font-family:var(--mono);font-size:10px;text-transform:uppercase;
     letter-spacing:.1em;color:var(--ink2);font-weight:600;white-space:nowrap}
  tbody tr:last-child td{border-bottom:0}
  dl.kv{margin:0;display:grid;grid-template-columns:minmax(90px,auto) 1fr;gap:5px 14px;
        font-size:.86rem}
  dl.kv dt{font-family:var(--mono);font-size:10px;text-transform:uppercase;
           letter-spacing:.1em;color:var(--ink2);padding-top:.25em}
  dl.kv dd{margin:0;color:var(--ink)}
  .bar{background:var(--bg3);border-radius:999px;height:7px;overflow:hidden;margin:5px 0}
  .bar>i{display:block;height:100%;background:var(--teal);border-radius:999px}
  .flagrow{display:flex;gap:12px;justify-content:space-between;align-items:flex-start;
           padding:9px 0;border-top:1px solid var(--line);font-size:.86rem}
  .flagrow:first-of-type{border-top:0}
  .tl{border-left:2px solid var(--line);margin:6px 0 0;padding-left:0}
  .tl>div{position:relative;padding:0 0 14px 18px}
  .tl>div::before{content:"";position:absolute;left:-5px;top:5px;width:8px;height:8px;
                  border-radius:50%;background:var(--bg2);border:2px solid var(--line2)}
  .tl>div.done::before{background:var(--teal);border-color:var(--teal)}
  .tl .d{font-family:var(--mono);font-size:10px;text-transform:uppercase;
         letter-spacing:.1em;color:var(--ink2)}
  .tl h3{font-size:.94rem;margin:2px 0 3px}
  .tl p{font-size:.84rem;color:var(--ink2);margin:0}
  .heat{display:grid;gap:2px;font-size:.72rem}
  .heat .row{display:grid;grid-template-columns:120px repeat(var(--n,8),1fr);gap:2px;
             align-items:center}
  .heat .hd,.heat .nm{font-size:.68rem;color:var(--ink2);padding:3px 4px;line-height:1.2}
  .legend{display:flex;gap:12px;flex-wrap:wrap;font-size:.76rem;color:var(--ink2);
          margin-top:8px}

  /* ---- responsive + motion + print --------------------------------- */
  @media (max-width:860px){
    #cx-shell{display:block}
    #nav{position:static;flex:none;max-height:none;border-right:0;
         border-bottom:1px solid var(--line);padding-bottom:12px}
    .navbtn{display:inline-flex;width:auto}
    #nav .grp{margin-top:10px}
  }
  @media (prefers-reduced-motion: reduce){
    *,*::before,*::after{transition:none!important;animation:none!important;
                         scroll-behavior:auto!important}
  }
  @media print{
    #nav,#cx-topbar,#toast{display:none!important}
    #cx-main{padding:0}
    .card,.stat,.tablewrap{border-color:#bbb;break-inside:avoid}
    body{background:#fff;color:#000}
  }
"""


def extract_views(template):
    """The app's own VIEWS array — [id, title, ordinal, group] per view."""
    i = template.find("const VIEWS=[")
    if i < 0:
        raise SystemExit("template.html: VIEWS array not found — cannot build the shell")
    j = template.find("];", i)
    literal = template[i + len("const VIEWS="):j + 1]
    js = "const V=" + literal + ";console.log(JSON.stringify(V.map(v=>[v[0],v[1],v[2],v[3]])));"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        path = f.name
    out = subprocess.run(["node", path], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def build_shell(views):
    sections = "\n".join(
        f'    <section class="view" id="v-{v[0]}"></section>' for v in views)
    return (
        f'<style>{SHELL_CSS}</style>\n'
        '<div id="cx-shell">\n'
        '  <nav id="nav" aria-label="Views"></nav>\n'
        '  <main id="cx-main">\n'
        '    <div id="cx-topbar">\n'
        '      <div id="crumb"></div>\n'
        '      <label id="cx-editionlab" for="stateSel">Edition</label>\n'
        '      <select id="stateSel" aria-label="State edition"></select>\n'
        '      <span id="stateflag"></span>\n'
        '    </div>\n'
        f'{sections}\n'
        '  </main>\n'
        '</div>\n'
        '<div id="toast" role="status" aria-live="polite"></div>\n'
    )


# ------------------------------------------------ the canonical fact bases
# v0.63.0 (roadmap prompt 7): the Louisiana region/parish fact base, the K-12
# program and the WLB Institute fact base are canonical in data/ and were once
# ALSO literals in the template — the same facts twice, free to drift. The
# template now carries a `__CXFACT:<name>__` placeholder where each literal
# stood and the canonical JSON is injected IN PLACE at build time, so every
# view that read DATA.parishes (or any of the others) at that point in the
# script reads exactly what the other apps read. tools/extract_fact_bases.py
# reads the injected values back (between the /*cx:<name>*/ … /*cx:end*/
# markers) and must reproduce the canonical files byte for byte; CI checks it.
FACT_LAYERS = {
    "regions":      ("data/louisiana/fact_base.json",   lambda d: d["regions"]),
    "regionHubs":   ("data/louisiana/fact_base.json",   lambda d: d["regionHubs"]),
    "parishes":     ("data/louisiana/fact_base.json",   lambda d: d["parishes"]),
    "wlb":          ("data/wlb/institute.json",         lambda d: {k: v for k, v in d.items() if k not in ("note", "principles")}),
    "wlbPrinciples": ("data/wlb/institute.json",        lambda d: d["principles"]),
    "lak12":        ("data/louisiana/k12_program.json", lambda d: d["grades"]),
    "lak12Threads": ("data/louisiana/k12_program.json", lambda d: d["threads"]),
}


def inject_fact_bases(template):
    """Replace every __CXFACT:<name>__ placeholder with the canonical JSON,
    marked so the extractor can read it back. Every placeholder must be
    present and used exactly once; a stray literal or a missing placeholder
    stops the build."""
    cache = {}
    injected = {}
    for name, (rel, pick) in FACT_LAYERS.items():
        token = "__CXFACT:" + name + "__"
        if template.count(token) != 1:
            raise SystemExit(f"template.html: expected exactly one {token}, found {template.count(token)}")
        if rel not in cache:
            cache[rel] = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        payload = json.dumps(pick(cache[rel]), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        template = template.replace(token, "/*cx:" + name + "*/" + payload + "/*cx:end*/")
        injected[name] = len(payload)
    return template, injected


def main():
    version = (ROOT / "VERSION").read_text().strip()
    parts = json.loads(MAP.read_text(encoding="utf-8"))
    rows = [r for r in csv.DictReader(open(ROOT / "data" / "blocks.csv", newline="", encoding="utf-8"))
            if r["code"].startswith("T0") and r["pack"] in PACK_SECTOR]
    out = []
    kept = edited = 0
    for r in sorted(rows, key=lambda x: (x["pack"], x["code"])):
        orig = parts.get(r["code"])
        joined = (orig[0].rstrip(".") + ". " + orig[1]).strip() if orig else None
        if orig and r["transfer_check"] == joined:
            task, outcome = orig
            kept += 1
        else:
            task, outcome = r["transfer_check"], ""
            edited += 1
        out.append([PACK_SECTOR[r["pack"]], r["credential"], r["code"],
                    r["theme"], task, outcome])
    payload = json.dumps(out, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    # v0.68.0: the library is injected IN PLACE where the template's own copy
    # stood (the 96 literal rounds — 3.4 MB — are gone from the template), so
    # every reader sees the canonical rows from the first line; the trailing
    # overlay that used to replace them after the fact is no longer needed.
    sector_injection = ("/*cx:sectorBlocks*/" + payload + "/*cx:end*/;\n"
                        "DATA.cxCanonical={version:'" + version + "',sectorBlocks:" + str(len(out)) + ",source:'data/blocks.csv'}")
    # the Simulation Studio (v0.54.0): the engine plus every canonical scenario, as DATA.simStudio
    sys.path.insert(0, str(ROOT / "tools"))
    from sim_lib import sim_payload
    from runtime_lib import head_snippet, body_snippet
    sims = json.dumps(sim_payload(), ensure_ascii=False, separators=(",", ":"))
    # the shared runtime (CSP, referrer, privacy notice, studio engine) with the
    # studio data as a global, all ahead of the app's own (single) script block
    # so the quest view finds it on first render
    studio = body_snippet("education-os", "window.CX_SIM_STUDIO = " + sims + ";\n") + "\n"
    template = TEMPLATE.read_text(encoding="utf-8", errors="replace")
    template, facts = inject_fact_bases(template)
    if template.count("__CXFACT:sectorBlocks__;") != 1:
        raise SystemExit("template.html: expected exactly one __CXFACT:sectorBlocks__ placeholder")
    template = template.replace("__CXFACT:sectorBlocks__;", sector_injection)
    facts["sectorBlocks"] = len(payload)
    if "__CXHEAD__" not in template:
        raise SystemExit("template.html is missing the __CXHEAD__ placeholder")
    template = template.replace("__CXHEAD__", head_snippet("education-os"))
    first = template.find("<script>")
    if first < 0:
        raise SystemExit("template.html: no script block to precede with the shared runtime")
    template = template[:first] + studio + template[first:]

    # replace the vestigial stub page (an unreferenced container plus an
    # unwrapped `var DATA` block that rendered as visible text) with the
    # shell the app's code actually expects, derived from its own VIEWS
    views = extract_views(template)
    template, n = STUB.subn(build_shell(views), template, count=1)
    if not n:
        raise SystemExit("template.html: stub block not found — shell insertion "
                         "would be unsafe; inspect the template before building")

    # a11y: every region that scrolls is reachable by keyboard (WCAG 2.1.1);
    # the app renders views on hashchange, so re-check after each render
    a11y = ("\n<script>/* CX a11y: scrollable regions are focusable */(function(){"
            "function mark(){document.querySelectorAll('.tablewrap,#fg-out,pre,.scroll,[style*=\"overflow\"]').forEach(function(el){"
            "if((el.scrollHeight>el.clientHeight+2||el.scrollWidth>el.clientWidth+2)&&!el.hasAttribute('tabindex')){el.tabIndex=0;if(!el.hasAttribute('aria-label'))el.setAttribute('aria-label','Scrollable content');}});}"
            "window.addEventListener('hashchange',function(){setTimeout(mark,80)});window.addEventListener('load',function(){setTimeout(mark,120)});"
            "})();</script>\n")
    html = template + a11y + "</body>\n</html>\n"
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(html)/1e6:.2f} MB — "
          f"{len(out)} canonical sector blocks injected ({kept} with original "
          f"task/outcome fields, {edited} dataset-edited); {len(facts)} canonical "
          f"fact-base layers injected in place ({sum(facts.values()):,} bytes); "
          f"shell generated for {len(views)} views")


if __name__ == "__main__":
    main()
