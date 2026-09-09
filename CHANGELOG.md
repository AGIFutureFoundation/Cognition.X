# Changelog

All notable changes to Cognition.X are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org).

## [0.4.0] — 2026-09-09

### Added
- New community pack **Food, Cooking & Nutrition** (250 blocks, 5 tracks
  × 10 themes × 5 bands): kitchen craft & tools, nutrition literacy,
  planning/budget/shopping, food safety from market to plate, and food
  culture & systems. First of the roadmap Phase 1 candidate packs.
  Canonical totals: **7,250 blocks · 27 packs · 100 tracks · 407
  credentials**.

## [0.3.0] — 2026-09-09

First versioned release from this repository. Earlier versions (below)
predate the repo and are reconstructed from the imported artifacts.

### Added
- Repository structure: `apps/`, `data/`, `tools/`, `docs/`, CI.
- Canonical dataset `data/blocks.csv` — 7,000 blocks, 26 packs — with a
  globally unique, deterministic `block_id` per block
  (source `code` values collide across packs; see `docs/DATA_REVIEW.md`).
- New community pack **Digital Life, Data & AI** (250 blocks, 5 tracks ×
  10 themes × 5 bands): device & account security, information literacy,
  privacy & data stewardship, working with AI, online conduct & repair.
- Tooling: `tools/generate_pack.py` (spec → blocks),
  `tools/normalize_blocks.py` (source + generated → canonical CSV +
  `manifest.json`), `tools/validate_blocks.py` (structural checks), wired
  into GitHub Actions.
- Documentation: README, deep roadmap (`docs/ROADMAP.md`), data review
  (`docs/DATA_REVIEW.md`), licensing rationale (`docs/LICENSING.md`),
  data schema (`data/schema.md`), wiki source (`docs/wiki/`),
  contribution guide.
- Licensing: Apache-2.0 for code, CC BY 4.0 for curriculum content/data.

### Changed
- The Education OS app now lives at `apps/education-os/index.html`
  (the v0.2.0 build); the superseded build is archived under
  `apps/education-os/versions/`.

## [0.2.0] — imported ("gov" build, app iteration v227)

### Added
- Sector Specialization round: 120 more master blocks across the eight OS
  editions (Corporate, Science, Robotics, Global Health, Multilateral,
  Sapient, Education, Non-Profit), embedded in the app.

### Changed
- Removed the Google Fonts network dependency — the app is fully
  offline-capable.

## [0.1.0] — imported ("affeducationos" build)

### Added
- Cognition.X Education OS single-file application: governance model,
  five pillars, parish/region implementation plans, credential ledger,
  mission simulator, and the embedded master-block library.
- Blocks dataset export `Cognition.X_all_blocks.csv` (6,750 blocks,
  25 packs).
