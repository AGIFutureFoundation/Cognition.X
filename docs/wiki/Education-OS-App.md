# Education OS App

A single-file, offline-capable HTML application:
[`apps/education-os/index.html`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/apps/education-os/index.html)
(~8 MB — download and open locally; no server, no network).

## What's inside

- **Governance & pillars** — the five-pillar model, conformance levels,
  and how a learning day runs
- **Implementation plans** — four waves across sixty-four parishes, eight
  regional Trade Halls, eight narrative worlds
- **Five pathways, one credential ledger** — graduation redesigned but
  compliant
- **Mission simulator** — adaptive missions with difficulty bands, tiers
  and hint tracking
- **Master-block library** — the app's embedded block data (by internal
  iteration v227 it includes rounds beyond the CSV export; reconciliation
  is roadmap Phase 2)

## Build lineage

| Repo version | Build | Notes |
|---|---|---|
| v0.2.0 (current) | `index.html` ("gov") | Internal iteration v227: Sector Specialization, +120 master blocks; Google Fonts dependency removed — fully offline |
| v0.1.0 | `versions/v0.1.0-education-os.html` | Earlier build; fetches Inter from Google Fonts |

## On the pipeline (v0.19.0)

`index.html` is now **built**: the hand-grown "gov" build lives on as
`template.html` (shell + legacy content), and
`tools/build_education_os.py` appends a canonical overlay sourcing
`DATA.sectorBlocks` from `data/blocks.csv` — dataset edits flow into
the app, and the overlay cures the template's accumulated duplicate
inflation (11,520 raw rows → 5,200 canonical). Never edit `index.html`
directly.

## Constraint that is a feature

The app must remain deployable as **one file on a USB stick**. Roadmap
Phase 2 introduces a build pipeline (dataset injected from
`data/blocks.csv`) but the shipped artifact stays single-file and
offline-first for low-connectivity deployments.
