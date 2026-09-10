# Louisiana Platform

**Cognition.X Louisiana** models the Education OS over Louisiana's real
structure — 64 parishes, 8 regions, 8 Trade Halls — with an
**independent dashboard for every parish**:
[`apps/louisiana/index.html`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/apps/louisiana/index.html)
(~42 KB single file; opens locally).

## Surfaces

- **The State** — live totals, an interactive **stylized tile
  cartogram** of the 64 parishes colored by rollout wave (click any
  tile), and parishes-per-wave / parishes-per-region charts.
- **Parish Dashboards** — one per parish, deep-linkable
  (`#/parish/east-baton-rouge`): parish seal, seat, region and Trade
  Hall, wave timeline with the parish's cohort highlighted, school
  systems, anchor industries and the parish's **narrative world**,
  region population context (parish emphasized), the curriculum ledger
  and credential ladder, the Louisiana civic tracks, and per-parish
  notes saved in the browser.
- **Parish module plans (v0.12.0)** — the deep integration: every
  parish dashboard lists the core spine plus the packs matched to its
  own anchor industries by the build-time rules engine, each with the
  industry phrase that earned it; tracks deep-link into Flow Hub
  sessions (`#track=<SLUG>/<PREFIX>`) when the apps sit together in
  the repository.
- **Regions & Trade Halls** — the eight regions, each hall's hub city,
  wave-mix bars, the packs most assessed at each hall, and parish
  links.
- **Curriculum** — dataset totals, the series-by-family bar, the
  *Civic Leadership Legacy : Louisiana* tracks, and the community packs
  every parish plan draws from.

## Data provenance

Built by `tools/build_louisiana.py` from two sources, never hand-edited:

1. **The Louisiana fact base embedded in the Education OS app** —
   regions, hub cities, and per-parish name/seat/region/population/
   wave/districts/industries/narrative-world/rural-tier.
2. **`data/blocks.csv`** — curriculum totals and the Louisiana legacy
   pack's tracks, computed at build time.

Waves are the proposal's planned rollout (2027–28 → 2030–31), not an
adopted schedule; the tile map is a stylized cartogram with approximate
positions. Parish notes live only in the viewer's browser.

## Design

Light-first civic design: warm paper ground, Fraunces display serif,
a Mardi Gras purple/gold/green identity in the wordmark and accents,
and a CVD-validated 4-color wave palette for every chart — with a full
dark theme mirrored token-for-token.
