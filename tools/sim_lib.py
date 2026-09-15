"""Shared helper for the Simulation Studio (v0.54.0).

Every app builder calls `sim_payload()` for the data it embeds and
`sim_script()` for the engine it injects at the template's `__CXSIM__`
placeholder. One engine, one fact base, six hosts.

    from sim_lib import sim_payload, sim_script, inject_sim
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FB = ROOT / "data" / "simulations" / "scenarios.json"
ENGINE = ROOT / "tools" / "sim" / "engine.js"


def load_sims():
    return json.loads(FB.read_text(encoding="utf-8"))


def sim_payload(kinds=None, ids=None, anchors=None):
    """The subset an app embeds: the studio law, disciplines, difficulty
    ladder and the scenarios selected by trades kind, id or localize anchor.
    With no filter, every scenario."""
    fb = load_sims()
    scs = fb["scenarios"]
    if kinds is not None or ids is not None or anchors is not None:
        keep = []
        for s in scs:
            if kinds is not None and s.get("kind") in kinds:
                keep.append(s)
            elif ids is not None and s["id"] in ids:
                keep.append(s)
            elif anchors is not None and s.get("localize") in anchors:
                keep.append(s)
        scs = keep
    return {
        "format": fb["format"],
        "law": fb["law"],
        "run_note": fb["run_note"],
        "next_rule": fb["next_rule"],
        "difficulty": fb["difficulty"],
        "disciplines": fb["disciplines"],
        "scenarios": scs,
        "total": len(fb["scenarios"]),
    }


def sim_script():
    """The engine source, safe inside a <script> block."""
    return ENGINE.read_text(encoding="utf-8").replace("</", "<\\/")


def inject_sim(html):
    """Replace the template's __CXSIM__ placeholder with the engine."""
    if "__CXSIM__" not in html:
        raise SystemExit("template is missing the __CXSIM__ placeholder")
    return html.replace("__CXSIM__", sim_script())
