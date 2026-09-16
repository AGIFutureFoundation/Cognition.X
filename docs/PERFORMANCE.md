# Performance and footprint

> What each app costs a hall's browser, measured; what the v0.68.0 pass
> changed; what was deliberately left alone. Time figures are one laptop's
> (Chromium via Playwright, `file://`, median of three runs, see
> `tools/perf.js`); byte figures are exact and the tests hold them to a
> budget. Re-measure with
> `NODE_PATH=$(npm root -g) node tools/perf.js` after any change that
> touches a template or the data.

## Measured at v0.68.0

| App | Bytes | Gzip | Load | First content | Script eval | JS heap |
|---|---:|---:|---:|---:|---:|---:|
| education-os | 6.12 MB | 1.65 MB | 422 ms | 459 ms | 54 ms | 10 MB |
| flow-hub | 2.41 MB | 0.50 MB | 150 ms | 178 ms | 28 ms | 5 MB |
| louisiana | 0.91 MB | 0.33 MB | 190 ms | 233 ms | 75 ms | 4 MB |
| platform | 0.24 MB | 0.15 MB | 78 ms | 99 ms | 13 ms | 2 MB |
| states | 0.57 MB | 0.20 MB | 109 ms | 129 ms | 16 ms | 2 MB |
| trades-network | 0.43 MB | 0.19 MB | 116 ms | 143 ms | 32 ms | 3 MB |

*Load* is navigation to the `load` event; *first content* is when the
landing view has rendered real text; *script eval* is Chromium's
`ScriptDuration` up to settle; *gzip* is what a hosted copy sends when the
host compresses (`docs/HOSTING.md`).

## What the v0.68.0 pass changed

| App | Before | After | How |
|---|---|---|---|
| education-os | 9.54 MB · first content 630 ms | **6.12 MB · 459 ms** | The template carried its own copy of the sector master-block library — 96 literal rounds, 3.4 MB — that a trailing 1.3 MB overlay then *replaced* with the canonical rows from `data/blocks.csv`. Both were parsed on every load; only the second was ever read. The library is now injected **in place** where the template's copy stood (`__CXFACT:sectorBlocks__`, the prompt-7 pattern), the literal rounds are gone, and the overlay with them. Every one of the 149 views renders identically (hashed before and after; the only differences are random gradient ids, live-feed lines and the accessibility marker's timing). |
| louisiana | first content 468 ms · script 273 ms | **233 ms · 75 ms** | The two Voronoi maps (64 parishes by population; packs by family) are relaxed power diagrams on a 132×90 grid — deterministic functions of the build data, and 240 ms of the 273 ms of startup script. `tools/voronoi_precompute.js` now runs the template's *own* code (the region between the `@cx-voronoi` markers, unmodified) on the build payload and ships both grids run-length encoded (+33 KB); the app decodes them and falls back to computing when absent. The browser suite asserts decoded == freshly computed, so the two cannot drift. The canvas renderer also resolves each colour once instead of once per cell and fills horizontal runs instead of single cells (54 ms → 25 ms). |

Nothing else moved by more than measurement noise.

## What was measured and deliberately left alone

- **Fonts** (169 KB in each of the five branded apps; 70% of the Platform
  app's bytes). The files are already Latin subsets and the variable
  fonts are embedded once per family, not once per weight. Pinning
  Fraunces to a static optical size would save ~43 KB per app but would
  change how headings render across sizes; static instances of
  Instrument Sans would be *larger* than the one variable file. Not
  taken: fidelity over 43 KB.
- **Minification.** The apps are single, readable, diffable files that
  CI rebuilds from sources and compares byte for byte. Minifying would
  save bytes on `file://` and nothing on a compressing host, at the cost
  of the readability the reproducible-build check depends on. Not taken.
- **Flow Hub's 2.4 MB data payload** is the whole dataset (17,450
  blocks) in a compact array form; it compresses to 0.5 MB and parses in
  under 30 ms. Nothing to gain that a host's gzip does not already give.
- **`DATA.siteIndex` (296 KB) and `platformConformance` (152 KB)** in the
  Education OS are the next largest chunks; both are read by views, both
  are legitimate content.

## Budgets the tests hold

`test_footprint_budget` fails when a built app exceeds its byte budget,
so growth is a decision, not an accident. Budgets sit ~5% above the
measured size; raise one here and in the test in the same change, with
the reason.

| App | Budget |
|---|---:|
| education-os | 6.5 MB |
| flow-hub | 2.6 MB |
| louisiana | 1.0 MB |
| platform | 0.3 MB |
| states | 0.65 MB |
| trades-network | 0.5 MB |

## For a hosted copy

Serve the files compressed: gzip cuts every app by 60–80% on the wire
(the table's *Gzip* column), and pre-compressing at deploy time
(`gzip -9 -k index.html`, then `gzip_static on` in nginx or the
equivalent) costs the server nothing per request. The headers in
`docs/HOSTING.md` are unchanged by compression.
