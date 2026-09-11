#!/usr/bin/env python3
"""Build the Education OS app from its template + the canonical dataset.

Roadmap Phase 2: apps/education-os/index.html is now a BUILD PRODUCT.
The base is apps/education-os/template.html (the last hand-grown "gov"
build, kept verbatim as the app shell and legacy content). This tool
appends a canonical overlay <script> that, after all the app's own
rounds have run, replaces DATA.sectorBlocks with the sector master-block
library as it stands in data/blocks.csv — so edits to the dataset flow
into the app, and the app's sector library has exactly one source of
truth.

Field fidelity: the app renders each row's task and outcome separately;
blocks.csv stores them joined in transfer_check. The extraction sidecar
data/generated/app-master-blocks.map.json preserves the original
boundary per code. When a dataset row's check still equals the joined
original, the overlay re-emits the original [task, outcome]; when the
dataset row was edited, the edited check ships as the task with the
outcome left empty — the dataset wins.

Output stays a single offline file, per the app's standing constraint.
Deterministic: same inputs -> same output.
"""

import csv
import json
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
  :root{--ink:#1a1f26;--muted:#5a6472;--line:#dfe4ea;--bg:#f6f7f9;--surface:#fff;--accent:#2456a6}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
       font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}
  #cx-shell{display:flex;min-height:100vh;align-items:flex-start}
  #nav{flex:0 0 260px;position:sticky;top:0;max-height:100vh;overflow-y:auto;
       background:var(--surface);border-right:1px solid var(--line);padding:14px 10px}
  #nav .grp{font-size:.68rem;text-transform:uppercase;letter-spacing:.14em;
            color:var(--muted);margin:14px 8px 6px;font-weight:700}
  .navbtn{display:flex;gap:8px;width:100%;text-align:left;border:0;background:none;
          color:var(--ink);padding:7px 9px;border-radius:8px;font:inherit;cursor:pointer}
  .navbtn:hover{background:var(--bg)}
  .navbtn.active{background:rgba(36,86,166,.1);color:var(--accent);font-weight:600}
  .navbtn .k{color:var(--muted);font-size:.72rem;min-width:1.8em}
  #cx-main{flex:1;min-width:0;padding:20px clamp(16px,3vw,34px) 70px}
  #cx-topbar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:0 0 16px}
  #crumb{color:var(--muted);font-size:.8rem;flex:1;min-width:140px}
  #cx-editionlab{font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}
  #stateSel{padding:4px 8px;font:inherit;font-size:.82rem}
  #stateflag{font-size:.72rem;color:var(--muted);border:1px solid var(--line);
             border-radius:999px;padding:2px 10px}
  .view{display:none}
  .view.active{display:block}
  #toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);
         background:var(--ink);color:#fff;padding:9px 16px;border-radius:999px;
         font-size:.85rem;opacity:0;pointer-events:none;transition:opacity .18s}
  #toast.show{opacity:1}
  @media (max-width:820px){#cx-shell{display:block}#nav{position:static;flex:none;
    max-height:none;border-right:0;border-bottom:1px solid var(--line)}}
  @media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important}}
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
    overlay = (
        "\n<script>/* CX canonical overlay v" + version + " — generated by "
        "tools/build_education_os.py; DATA.sectorBlocks now sourced from "
        "data/blocks.csv. Do not edit: rebuild instead. */\n"
        ";(function(){try{\n"
        " if (typeof DATA !== 'undefined'){\n"
        "  DATA.sectorBlocks = " + payload + ";\n"
        "  DATA.cxCanonical = {version:'" + version + "', sectorBlocks: DATA.sectorBlocks.length,"
        " source:'data/blocks.csv'};\n"
        " }\n"
        "}catch(e){}})();\n</script>\n"
    )
    template = TEMPLATE.read_text(encoding="utf-8", errors="replace")

    # replace the vestigial stub page (an unreferenced container plus an
    # unwrapped `var DATA` block that rendered as visible text) with the
    # shell the app's code actually expects, derived from its own VIEWS
    views = extract_views(template)
    template, n = STUB.subn(build_shell(views), template, count=1)
    if not n:
        raise SystemExit("template.html: stub block not found — shell insertion "
                         "would be unsafe; inspect the template before building")

    html = template + overlay + "</body>\n</html>\n"
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(html)/1e6:.2f} MB — "
          f"{len(out)} canonical sector blocks injected ({kept} with original "
          f"task/outcome fields, {edited} dataset-edited); shell generated for "
          f"{len(views)} views")


if __name__ == "__main__":
    main()
