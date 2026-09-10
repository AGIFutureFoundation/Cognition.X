# Trades Network

**Cognition.X Trades Network** ([`apps/trades-network/`](https://github.com/AGIFutureFoundation/Cognition.X/tree/main/apps/trades-network))
is the platform's regional union-and-trades layer: **37 trade families ×
6 regions = 222 regional union & trade entries** on two working coasts —
**San Francisco**, **Oakland–East Bay** and **Los Angeles** on the
Pacific; **New Orleans**, **Baton Rouge–River Region** and
**Houston–Gulf Coast** on the Gulf (expanded from 3 regions in
v0.30.0) — each carrying a training simulation set on its region's own
publicly known ground, the curriculum packs behind it, and the flipped,
gamified classroom model that brings the trades into school districts.

Built by [`tools/build_trades.py`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/tools/build_trades.py)
from the unions fact base
([`data/unions/trade_unions.json`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/data/unions/trade_unions.json))
plus the canonical dataset — never hand-edit `index.html`.

## Surfaces

- **The Network** — totals, the three-region arc map, the learner's
  five-step path (flipped lesson → simulation studio → bench & transfer
  check → the hall → the pathway is the learner's).
- **Regions** — per-region cards, each headed by a **stylized city
  map** (v0.26.0): approximate hand-placed geography — the Gate, the
  Bay, the Lake and the river crescent — with the nine training-ground
  sites as nodes carrying their trade-family counts; clicking a node
  opens the roster filtered to that region and category, so all 222
  entries are reachable from the maps (six maps since v0.30.0 — the
  Mississippi through Baton Rouge, the Houston Ship Channel, the
  Pacific under Los Angeles). Below the map: the council (always the
  front door) and the school districts.
- **Unions & Trades** — the full 222-entry roster, searchable and
  filterable by region and category; every card names the international
  union, its localized training sim, and Flow Hub deep links into its
  backing packs.
- **Simulations** — nine control-discipline categories on all three
  coasts, each under the studio law.
- **Flipped Classroom** — the four-node flipped cycle and the honest
  game layer, with the *Trades in the Classroom : Flipped & Gamified*
  pack's five tracks, plus (v0.26.0) the **Trades Across School
  Subjects** pack — the early-pathways layer that teaches the working
  world inside math, science, ELA and civics from K–2 up. Every
  roster card carries its own "In class" hook (subject chips + one
  concrete classroom connection) into these tracks.
- **Districts** — the district–council compact in six commitments,
  localized to SFUSD, OUSD and NOLA Public Schools.

## Two hard rules

1. **No local numbers.** Union locals merge, renumber and redistrict, so
   the fact base names only international unions (with per-coast
   overrides where a craft is organized differently — ILWU on the West
   Coast, ILA on the Gulf) and routes every entry through the regional
   building-trades or labor council to find the current local.
2. **Simulation ≠ certification.** Carried verbatim from the SmartCiti.X
   stance: a simulator teaches control discipline and observation; it
   never counts as equipment certification, union credit, or
   apprenticeship standing. Nothing energized, suspended or moving is
   practiced live in a classroom studio.

The network is independent and not affiliated with, endorsed by, or
reviewed by any union, council, port, district or agency named.

## Voice & guide

Like the other apps, the Trades Network ships the **three-persona voice
model** (Warm / Steady / Brisk — natural-voice preference list,
sentence-level prosody, fully on-device) and a 7-stop active Guide.
