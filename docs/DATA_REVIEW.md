# Data Review — imported artifacts (2026-09-09)

Findings from reviewing the five imported files, and what was done about
each. The validator (`tools/validate_blocks.py`) enforces the fixes going
forward.

## What was imported

| Artifact | Verdict | Disposition |
|---|---|---|
| `Cognition.X_all_blocks.csv` (×2 uploads) | Byte-identical duplicates (same MD5) | One copy kept at `data/source/` |
| `Cognition.X_.pdf` (85 pp) | The same CSV rendered as a table — no additional content | Not committed (redundant, 1.6 MB) |
| `affeducationos.html` (7.9 MB) | Education OS app, earlier build | Archived as `apps/education-os/versions/v0.1.0-education-os.html` |
| `gov.html` (8.1 MB) | Same app, later iteration — internal changelog reaches **v227 "Sector Specialization"** (+120 master blocks); Google Fonts dependency removed, so fully offline | Canonical app at `apps/education-os/index.html` |

The two app builds are otherwise structurally identical (same 545 `<h2>`
sections; the only other diff is the fonts `<link>`).

## Dataset findings (6,750 source rows)

1. **Cross-pack code collisions (fixed).** `code` is only unique within a
   pack: track prefixes are reused across packs (`EV-*` in both Housing &
   Tenancy and Sapient OS; `SF-*` in three packs; 450 codes, 550 rows
   affected). Fix: `tools/normalize_blocks.py` prepends a deterministic,
   globally unique `block_id` (`CX-<PACK>-<NNNN>`); the original `code` is
   kept untouched. The validator now allows duplicate codes only across
   packs, never within one.

2. **Two schemas in one file (backfill in progress).** 4,500
   "tracked" source rows carry `track`/`code`/`level`/`description`; 2,250
   "legacy" rows left those empty. *Update (v0.8.0):* the five cleanly
   banded 250-row packs (Basic Life Skills, Preventive Health,
   Water/Land/Climate, Care Across a Life, Making/Repair/Reuse) carried
   their track structure as `(XX)` suffixes in theme names and are now
   promoted to the tracked schema via `data/promotions/*.json` — 1,250
   rows backfilled, source values untouched. *Update (v0.14.0):* the
   1,000 irregular rows (K–12, Trade School, and seven thematic packs)
   received a structural light fill — deterministic `code` (`LB-<n>`)
   and grade-derived `level` on every row, with the validator now
   requiring both dataset-wide. Their shapes are irregular by design
   and are not forced into 10×5; authored `description` (and `track`
   where genuine groupings exist) is the remaining content work — see
   the [roadmap](ROADMAP.md).

2b. **Placeholder transfer checks (found during promotion — resolved
   in v0.13.0).** Most pre-promotion legacy rows carried a generic
   check — "Demonstrate it once, correctly, to somebody who will use
   it" / "Do it once, for real, and show it to somebody who will use
   it" — rather than a per-theme task (217 themes / 1,085 rows across
   the five promoted packs). *Resolution:* real per-theme checks were
   authored in the promotion specs, and the normalizer replaces a
   source check **only** when it is one of the two known placeholder
   sentences — real source checks are never overwritten. Zero
   placeholder checks remain dataset-wide.

3. **Band descriptions are suffixed, not differentiated (scheduled).**
   Within a theme, all five grade bands share one description
   distinguished only by an "— at {band}" suffix, and the transfer check
   is identical across bands. Real band differentiation is the largest
   content-quality item in Phase 1.

4. **Minor anomalies (documented).** Two rows have grade `—` (Trade
   School capstones); grades `9–12 · adult` (7 rows) and `11–12 · adult`
   (47 rows) appear only in Trade School; K–12 uses single grades K–12
   plus bridge rows. All legitimate on inspection; the validator treats
   them as legacy-pack shapes.

5. **App data vs. CSV (documented).** The app embeds its own master-block
   library, which by v227 has grown past the CSV export (the CSV predates
   the last app rounds, e.g. the 120 Sector Specialization blocks and an
   Education OS edition present in the app but absent from the CSV).
   Reconciling app-embedded data with `blocks.csv` — one source of truth,
   injected at build time — is Phase 2 of the roadmap.

## Continuation

Following the established shape (5 tracks × 10 themes × 5 bands), a new
community pack **Digital Life, Data & AI** (250 blocks; spec at
`data/pack_specs/digital-life-data-ai.json`) was generated and merged into
the canonical dataset — the domain most conspicuously missing from the 25
existing packs. Canonical totals: **7,000 blocks · 26 packs · 95 tracks ·
402 credentials**, all green under the validator.
