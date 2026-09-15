# Dataset schema — `data/blocks.csv`

One row per **block**: the smallest unit of the curriculum, one capability
at one grade band, with a transfer check that proves it.

| Column | Required | Description |
|---|---|---|
| `block_id` | always | Globally unique, stable id: `CX-<PACK>-<NNNN>` (pack slug + 1-based row number within the pack, source order). Never reused, never renumbered. Assigned by `tools/normalize_blocks.py`. |
| `pack` | always | Curriculum pack (38 today; see `manifest.json`). |
| `track` | tracked packs | Named journey inside a pack; one credential per track. Empty on legacy packs. |
| `code` | always | `<PREFIX>-<n>`, unique **within its pack only** (prefixes are reused across packs — always join on `block_id`). Foundation-library rows carry light-fill codes `LB-<n>`. |
| `grade` | always | Grade band `K–2 / 3–5 / 6–8 / 9–10 / 11–12` on tracked packs; single grades, bridge or adult bands on legacy packs. |
| `level` | always | Depth tier: K–2 & 3–5 → `Explorer`, 6–8 → `Builder`, 9–10 → `Practitioner`, 11–12 → `Lead`; single grades map into those bands, adult/capstone rows → `Lead`. |
| `credential` | always | Credential the block counts toward (the track credential on tracked packs; per-row credentials on legacy packs). |
| `theme` | always | The block's topic. Tracked packs: exactly 10 themes per track, each appearing once per band (track = 50 blocks). |
| `description` | tracked packs | What the block teaches, suffixed `— at <band>`. |
| `transfer_check` | always | The concrete, real-material task that demonstrates transfer. |

## Shapes

- **Tracked pack** = N tracks × 10 themes × 5 bands. Community packs have
  5 tracks (250 blocks); OS editions have 10 tracks (500 blocks).
- **Legacy packs** predate the tracked shape. Five of them (Basic Life
  Skills, Preventive Health, Water/Land/Climate, Care Across a Life,
  Making/Repair/Reuse) were promoted to the tracked schema in v0.8.0
  via `data/promotions/*.json` (empty fields filled; source values
  never overwritten). K–12, Trade School, Future-Work, Regional,
  Civic & Leadership, Health & Community, Language/Culture, Empathy &
  EI and Community & Relationship keep their original columns;
  their backfill is roadmap Phase 1.

## Files

- `source/Cognition.X_all_blocks.csv` — imported source (verbatim, 6,750 rows)
- `pack_specs/*.json` — authorable pack specifications
- `generated/*.csv` — packs expanded from specs by `tools/generate_pack.py`
- `promotions/*.json` — legacy-pack promotions: track names and base
  descriptions that fill empty fields during normalization
- `blocks.csv` — canonical dataset: source + generated, with `block_id`
- `manifest.json` — machine-readable per-pack index
- `standards/*.json` — standards mappings (`cx-standards/1`): a framework's
  codes by block (`scope: block`) or by track and band (`scope: track-band`),
  with publisher, as-of, strength (*cites* / *touches*) and a verifying caveat
- `rubrics/*.json` — transfer-check rubrics (`cx-rubrics/1`) per track: pass
  evidence, failure modes, assessor note; both validated by
  `tools/validate_standards.py`
- `simulations/scenarios.json` — the Simulation Studio fact base
  (`cx-simulations/1`): branching control-discipline scenarios, each tied
  to a pack slug + track and carrying that track's witnessed transfer
  check verbatim; validated by `tools/validate_simulations.py`

Rebuild with `python3 tools/normalize_blocks.py`; check with
`python3 tools/validate_blocks.py`.
