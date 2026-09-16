#!/usr/bin/env python3
"""Write apps/CHECKSUMS.sha256 — the SHA-256 of every built app.

The apps are single files that travel by USB stick, e-mail and district
file shares. A hall or an IT office can verify that the file it holds is
the file this repository released:

    sha256sum -c apps/CHECKSUMS.sha256        (from the repository root)

CI rebuilds every app from source and regenerates this file; the
byte-identical check on apps/ then holds both the builds and the sums.
"""

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPS = ["education-os", "flow-hub", "louisiana", "platform", "states", "trades-network"]
OUT = ROOT / "apps" / "CHECKSUMS.sha256"


def main():
    version = (ROOT / "VERSION").read_text().strip()
    lines = [f"# Cognition.X v{version} — SHA-256 of every built app; verify with: sha256sum -c apps/CHECKSUMS.sha256"]
    for app in APPS:
        p = ROOT / "apps" / app / "index.html"
        lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  apps/{app}/index.html")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(APPS)} apps")


if __name__ == "__main__":
    main()
