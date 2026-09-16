#!/usr/bin/env python3
"""Write sbom/cognitionx.cdx.json — a CycloneDX 1.5 software bill of materials
for the release, generated from the build with no external dependency.

What it lists, honestly: the six built apps (with their SHA-256), the four
embedded typefaces (SIL OFL 1.1, from data/fonts/fonts.json), the build
toolchain (Python 3 standard library — there are no runtime or build
dependencies), and the development toolchain used by the browser tests
(Playwright, axe-core, Chromium) with the versions pinned in the
repository's notes. Regenerated and drift-checked in CI; the serial number
is derived from the release version so the file is reproducible.
"""

import hashlib
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "sbom" / "cognitionx.cdx.json"
APPS = ["education-os", "flow-hub", "louisiana", "platform", "states", "trades-network"]
DEV = [("playwright", "1.56.1", "npm", "Apache-2.0", "browser test runner (tests/browser/smoke.js, tools/a11y/audit.js)"),
       ("axe-core", "4.13.0", "npm", "MPL-2.0", "accessibility audit engine (tools/a11y/audit.js)")]


def main():
    version = (ROOT / "VERSION").read_text().strip()
    fonts = json.loads((ROOT / "data" / "fonts" / "fonts.json").read_text(encoding="utf-8"))["fonts"]
    comps = []
    for app in APPS:
        p = ROOT / "apps" / app / "index.html"
        comps.append({"type": "application", "bom-ref": f"cx:app:{app}", "name": f"Cognition.X {app}", "version": version,
                      "description": "single-file offline HTML application; no runtime dependencies",
                      "hashes": [{"alg": "SHA-256", "content": hashlib.sha256(p.read_bytes()).hexdigest()}],
                      "licenses": [{"license": {"id": "Apache-2.0"}}, {"license": {"id": "CC-BY-4.0", "name": "content"}}],
                      "properties": [{"name": "cx:path", "value": f"apps/{app}/index.html"}, {"name": "cx:network", "value": "none (CSP connect-src 'none')"}]})
    seen = set()
    for f in fonts:
        key = (f["family"], hashlib.sha256((ROOT / "data" / "fonts" / f["file"]).read_bytes()).hexdigest())
        if key in seen:
            continue
        seen.add(key)
        comps.append({"type": "file", "bom-ref": f"cx:font:{f['file']}", "name": f["family"], "version": f["source"].rsplit("/", 2)[-2],
                      "description": f"embedded typeface (latin subset), weight {f['weight']}",
                      "hashes": [{"alg": "SHA-256", "content": key[1]}],
                      "licenses": [{"license": {"id": "OFL-1.1"}}],
                      "properties": [{"name": "cx:path", "value": f"data/fonts/{f['file']}"}, {"name": "cx:source", "value": f["source"]}]})
    comps.append({"type": "platform", "bom-ref": "cx:build:python", "name": "Python", "version": "3.12 (standard library only)",
                  "description": "build toolchain: tools/build_*.py, validators, generators; no third-party packages",
                  "licenses": [{"license": {"id": "PSF-2.0"}}]})
    for name, ver, purl_type, lic, desc in DEV:
        comps.append({"type": "library", "bom-ref": f"cx:dev:{name}", "name": name, "version": ver, "purl": f"pkg:{purl_type}/{name}@{ver}",
                      "description": "development toolchain only — never shipped in any app: " + desc, "licenses": [{"license": {"id": lic}}],
                      "scope": "excluded"})
    doc = {
        "bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1,
        "serialNumber": "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/AGIFutureFoundation/Cognition.X/releases/" + version)),
        "metadata": {"component": {"type": "application", "bom-ref": "cx:release", "name": "Cognition.X", "version": version,
                                   "supplier": {"name": "AGI Future Foundation PBC"},
                                   "licenses": [{"license": {"id": "Apache-2.0"}}]},
                     "properties": [{"name": "cx:generated_by", "value": "tools/sbom.py"},
                                    {"name": "cx:runtime_dependencies", "value": "0"},
                                    {"name": "cx:note", "value": "The apps are single HTML files with no runtime dependencies and no network access. Development-only components are listed with scope 'excluded'."}]},
        "components": comps,
        "dependencies": [{"ref": "cx:release", "dependsOn": [c["bom-ref"] for c in comps if c["type"] in ("application",)]}]
                        + [{"ref": f"cx:app:{app}", "dependsOn": [c["bom-ref"] for c in comps if c["type"] == "file"]} for app in APPS if app != "education-os"]
                        + [{"ref": "cx:app:education-os", "dependsOn": []}],
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(comps)} components (6 apps, {len(seen)} typefaces, build + dev toolchains)")


if __name__ == "__main__":
    main()
