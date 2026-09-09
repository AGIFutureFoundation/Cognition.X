# Dataset schema — `data/blocks.csv`

One row per **block**: the smallest unit of the curriculum, one capability
at one grade band, with a transfer check that proves it.

| Column | Required | Description |
|---|---|---|
| `block_id` | always | Globally unique, stable id: `CX-<PACK>-<NNNN>` (pack slug + 1-based row number within the pack, source order). Never reused, never renumbered. Assigned by `tools/normalize_blocks.py`. |
| `pack` | always | Curriculum pack (33 today; see `manifest.json`). |
| `track` | tracked packs | Named journey inside a pack; one credential per track. Empty on legacy packs. |
| `code` | tracked packs | Source code `<PREFIX>-<n>`, unique **within its pack only** (prefixes are reused across packs — always join on `block_id`). |
| `grade` | always | Grade band `K–2 / 3–5 / 6–8 / 9–10 / 11–12` on tracked packs; single grades, bridge or adult bands on legacy packs. |
| `level` | tracked packs | Depth tier bound to the band: K–2 & 3–5 → `Explorer`, 6–8 → `Builder`, 9–10 → `Practitioner`, 11–12 → `Lead`. |
| `credential` | always | Credential the block counts toward (the track credential on tracked packs; per-row credentials on legacy packs). |
| `theme` | always | The block's topic. Tracked packs: exactly 10 themes per track, each appearing once per band (track = 50 blocks). |
| `description` | tracked packs | What the block teaches, suffixed `— at <band>`. |
| `transfer_check` | always | The concrete, real-material task that demonstrates transfer. |

## Shapes

- **Tracked pack** = N tracks × 10 themes × 5 bands. Community packs have
  5 tracks (250 blocks); OS editions have 10 tracks (500 blocks).
- **Legacy packs** (K–12, Trade School, Future-Work, Regional, Civic &
  Leadership, Health & Community, Language/Culture/Communication, Empathy
  & EI, Community & Relationship) predate the tracked shape and keep
  their original columns; backfill is roadmap Phase 1.

## Files

- `source/Cognition.X_all_blocks.csv` — imported source (verbatim, 6,750 rows)
- `pack_specs/*.json` — authorable pack specifications
- `generated/*.csv` — packs expanded from specs by `tools/generate_pack.py`
- `blocks.csv` — canonical dataset: source + generated, with `block_id`
- `manifest.json` — machine-readable per-pack index

Rebuild with `python3 tools/normalize_blocks.py`; check with
`python3 tools/validate_blocks.py`.
