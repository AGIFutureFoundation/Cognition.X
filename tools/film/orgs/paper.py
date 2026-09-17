#!/usr/bin/env python3
"""Render a white paper from docs/whitepapers/*.md to a print-ready HTML and PDF.

    python3 tools/film/orgs/paper.py docs/whitepapers/tenderloin-pilot.md [out_dir]

Markdown → HTML (python-markdown, tables + toc) with the platform's print
stylesheet embedded, then Chromium prints it to A4/Letter PDF through
Playwright. Nothing is fetched; fonts are the system serif."""
import sys, os, subprocess, json
from pathlib import Path
import markdown
src = Path(sys.argv[1]); out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else src.parent); out_dir.mkdir(parents=True, exist_ok=True)
md = src.read_text(encoding="utf-8")
title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), src.stem)
body = markdown.markdown(md, extensions=["tables", "toc", "sane_lists", "smarty"], extension_configs={"toc": {"toc_depth": "2-3"}})
CSS = """
@page { size: Letter; margin: 22mm 20mm 24mm 20mm; }
html { font: 11pt/1.5 Georgia, 'Times New Roman', serif; color: #14212b; }
body { max-width: 180mm; margin: 0 auto; padding: 0 0 40px; }
h1 { font-size: 26pt; line-height: 1.15; margin: 0 0 6pt; letter-spacing: -.01em; }
h2 { font-size: 16pt; margin: 26pt 0 8pt; padding-top: 8pt; border-top: 2px solid #D9A441; page-break-after: avoid; }
h3 { font-size: 12.5pt; margin: 16pt 0 5pt; page-break-after: avoid; }
p, li { orphans: 3; widows: 3; }
blockquote { margin: 12pt 0; padding: 10pt 14pt; border-left: 5px solid #D9A441; background: #f6f1e4; font-size: 10.5pt; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 8pt 0 14pt; page-break-inside: auto; }
th, td { border: 1px solid #cfd6dc; padding: 4pt 6pt; vertical-align: top; text-align: left; }
th { background: #0E1E2E; color: #fff; font-weight: 600; }
tr { page-break-inside: avoid; }
code { font: 9.5pt ui-monospace, Menlo, monospace; background: #f0f3f5; padding: 0 3pt; }
.kicker { font: 600 9pt ui-monospace, Menlo, monospace; letter-spacing: .28em; text-transform: uppercase; color: #8a6a1e; margin-bottom: 8pt; }
.toc { font-size: 9.5pt; columns: 2; column-gap: 24pt; margin: 10pt 0 6pt; padding: 10pt 12pt; border: 1px solid #cfd6dc; }
.toc ul { margin: 0; padding-left: 14pt; } .toc > ul > li { margin: 2pt 0; }
a { color: #14212b; text-decoration: none; }
hr { border: 0; border-top: 1px solid #cfd6dc; margin: 18pt 0; }
.foot { font-size: 8.5pt; color: #56646f; margin-top: 30pt; border-top: 1px solid #cfd6dc; padding-top: 8pt; }
"""
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head>
<body><div class="kicker">Cognition.X · Education OS · white paper</div>{body}
<div class="foot">Cognition.X is open source (github.com/AGIFutureFoundation/Cognition.X). Curriculum content CC BY 4.0. This paper describes a proposal built from public information; it claims no affiliation with, endorsement by, or contact with the organisation it is written for. Not legal advice. A simulation is practice; a credential names exactly what was witnessed.</div>
</body></html>"""
html_path = out_dir / (src.stem + ".html"); html_path.write_text(html, encoding="utf-8")
pdf_path = out_dir / (src.stem + ".pdf")
js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch({{ executablePath: process.env.CX_CHROMIUM || '/opt/pw-browsers/chromium' }}); const p = await b.newPage();
  await p.goto('file://{html_path.resolve()}'); await p.waitForTimeout(300);
  await p.pdf({{ path: '{pdf_path.resolve()}', format: 'Letter', printBackground: true, displayHeaderFooter: true, headerTemplate: '<div></div>', footerTemplate: '<div style="font:8px Georgia,serif;color:#56646f;width:100%;text-align:center">{title.replace("'", "&#39;")} · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>', margin: {{ top: '22mm', bottom: '24mm', left: '20mm', right: '20mm' }} }});
  await b.close(); }})();"""
subprocess.run(["node", "-e", js], check=True, env={**os.environ, "NODE_PATH": os.environ.get("NODE_PATH") or subprocess.check_output(["npm", "root", "-g"]).decode().strip()})
print(f"wrote {html_path} and {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")
