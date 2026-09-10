# Flow Hub

The interactive hub across the whole Cognition.X series:
[`apps/flow-hub/index.html`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/apps/flow-hub/index.html)
(~0.6 MB, single file, opens locally; fonts degrade gracefully offline).

Unlike the Education OS app, Flow Hub is a **build product of the
dataset**: `tools/build_flow_hub.py` compacts `data/blocks.csv` and
injects it into `apps/flow-hub/template.html`. Never edit `index.html`
directly — change the template or the data and rebuild.

## Surfaces

- **System** — live counts (blocks, packs, tracks, credentials) and the
  series-by-family distribution, all computed from the shipped data;
  the pack constellation links into the explorer.
- **Packs** — search and family filters across all packs, down to each
  theme's description, transfer check and band ladder; foundation
  packs render their original per-grade table.
- **Flow** — the flow-state engine. Pick a track and a starting skill;
  the engine serves blocks and moves the grade band from how each one
  lands (*Breezed / In the flow / Struggled*). The flow-channel chart
  plots every move on the skill–challenge plane with the channel
  shaded; a meter tracks time-in-channel. A Pacer runs 25/5 focus
  intervals.
- **Agents** — the four rule-based session agents and their activity
  feed: **Pathfinder** (selection), **Pacer** (rhythm), **Assessor**
  (evidence), **Archivist** (memory).
- **Ledger** — per-track credential progress (10 themes → credential),
  with copy/paste JSON export and import via the Archivist.

## The flow model

Flow is modeled on the challenge–skill channel: a session move counts as
in-channel when challenge sits within roughly `skill − 0.6` to
`skill + 1.1`. *Breezed* raises both skill and band; *Struggled* eases
the band off; *In the flow* nudges skill up and holds the band just
above it. Completing a transfer check records the theme at the current
band and feeds the ledger.

## State

Progress, skills and the agent feed persist per browser
(`localStorage`); the Archivist's export makes them portable. Nothing
leaves the machine.

## Deep links

`index.html#track=<PACKSLUG>/<PREFIX>` (e.g. `#track=ENERGY/EL`)
preselects that pack and track and opens the Flow view — the
integration point the Louisiana parish module plans use, and available
to any external system.

## Rebuilding

```bash
python3 tools/build_flow_hub.py   # reads data/blocks.csv + VERSION
```
