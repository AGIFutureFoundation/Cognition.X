# Versioning and Releases

Cognition.X follows [Semantic Versioning](https://semver.org). The current
version is in [`VERSION`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/VERSION);
history is in [`CHANGELOG.md`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/CHANGELOG.md).

## What bumps what

| Change | Bump |
|---|---|
| Fixing typos, correcting a transfer check, doc edits | **PATCH** |
| New pack, new app feature, new tooling | **MINOR** |
| Dataset schema change, `block_id` format change, removing a pack | **MAJOR** |

## Invariants

- `block_id`s are never reused or renumbered — a MAJOR bump does not
  license breaking them; supersede blocks instead.
- Superseded app builds are archived under
  `apps/education-os/versions/`, never silently overwritten.
- Every release tag `vX.Y.Z` points at a commit where CI (the dataset
  validator) is green.

## History

| Version | Summary |
|---|---|
| **v0.15.0** | Cognition.X : Louisiana OS (500 blocks, 10 tracks — river, coast, corridor, ports, agriculture, table, music, languages, festivals, storm memory), added to every parish's core spine |
| v0.14.0 | Structural backfill complete: code + level on all 9,250 rows (light fill for the 1,000 irregular foundation rows); validator requires both dataset-wide |
| v0.13.0 | All 217 placeholder transfer checks replaced with authored per-theme checks (1,085 rows; guarded substitution) — zero placeholders remain |
| v0.12.0 | Deep module↔system integration: per-parish module plans from an industry rules engine, Flow Hub track deep links, Trade Hall pack rosters |
| v0.11.0 | California and Texas legacy localizations (500 blocks) — dataset at 9,250 blocks / 35 packs / 165 tracks |
| v0.10.0 | Legacy Institute flagship (12 principles, state/country localizer), Agents & Robots view + CX-Trace v1 export, style options across the platform |
| v0.9.0 | Cognition.X Louisiana: 64 independent parish dashboards, tile cartogram, Trade Hall regions — built from the app's fact base + the dataset |
| v0.8.0 | Legacy backfill, first slice: five banded packs promoted to the tracked schema (1,250 rows; 155 tracks); placeholder transfer checks documented |
| v0.7.0 | Flow Hub app: flow-state engine, session agents, credential ledger — built from the dataset by the Phase 2 pipeline pattern |
| v0.6.0 | First legacy-track localization: *Civic Leadership Legacy : Louisiana* (250 blocks, Willie L. Brown Jr. Institute model) — dataset at 8,750 blocks / 33 packs |
| v0.5.0 | Five community packs (Energy, Transport, Emergency, Arts, Law — 1,250 blocks), completing the Phase 1 candidate list — dataset at 8,500 blocks / 32 packs |
| v0.4.0 | *Food, Cooking & Nutrition* pack (250 blocks) — dataset at 7,250 blocks / 27 packs |
| v0.3.0 | First repo release: structure, CI, canonical dataset (7,000 blocks) with stable ids, *Digital Life, Data & AI* pack, docs/roadmap/wiki, dual licensing |
| v0.2.0 | Imported "gov" app build (internal v227, Sector Specialization, offline fonts) |
| v0.1.0 | Imported "affeducationos" app build + 6,750-block CSV export |

## Cutting a release

1. Update `VERSION` and move `CHANGELOG.md` *Unreleased* items under the
   new version heading.
2. Merge to `main` with CI green.
3. `git tag -a vX.Y.Z -m "Cognition.X vX.Y.Z" && git push origin vX.Y.Z`
4. Optionally publish a GitHub Release pointing at the tag, attaching the
   app HTML as a downloadable asset.
