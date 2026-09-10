# Cognition.X — Deep Roadmap

Direction of travel: from a curriculum **dataset + demo app** (today) to a
verifiable, federated **learning operating system** that a school, parish,
ministry or employer can run. Phases are sequential but overlapping;
versions follow SemVer and are cut when a phase's exit criteria pass.

---

## Phase 0 — Foundation (v0.3.x) ✅ *this release*

**Goal: one canonical, validated source of truth.**

- [x] Repository structure, CI validation, versioning, licensing
- [x] Canonical dataset (`blocks.csv`, 7,000 blocks) with stable
  `block_id`s; cross-pack code collisions resolved
- [x] Deterministic pack generator + spec format
- [x] First continuation pack: *Digital Life, Data & AI* (250 blocks)
- [x] Wiki source and data review published

**Exit criteria:** validator green in CI; every block addressable by a
stable id. ✅

---

## Phase 1 — Data completeness & quality (v0.4–v0.6)

**Goal: every block is complete, reviewed, and standards-mapped.**

- Backfill the legacy rows with `code`, `level` and `description` so
  every pack shares one schema:
  - [x] The five banded 250-row packs (Basic Life Skills, Preventive
    Health, Water/Land/Climate, Care Across a Life, Making/Repair/
    Reuse) — promoted via `data/promotions/` in v0.8.0 (1,250 rows)
  - [x] Structural fill for the irregular remainder (v0.14.0): all
    1,000 rows now carry `code` and `level`; validator requires both
    dataset-wide
  - Remaining content work on those 1,000 rows: authored `description`
    per row and, where genuine groupings exist (the credential groups
    in Civic & Leadership, Language/Culture, Empathy & EI, Community &
    Relationship, Regional), named `track` values — their shapes are
    irregular by design and will not be forced into 10×5
- [x] Replace the placeholder transfer checks surfaced by the v0.8.0
  review with real per-theme checks — shipped in v0.13.0 (217 themes /
  1,085 rows; guarded replacement, zero placeholders remain)
- Convert legacy packs to pack-spec JSON so the entire dataset is
  regenerable from specs (single source of truth becomes `data/pack_specs/`)
- De-duplicate `description` band suffixes: author genuinely
  band-differentiated descriptions (today most bands share one sentence
  with an "— at {band}" suffix) — the largest content-quality lift
- Standards mapping tables: Common Core / NGSS for K–12 packs; NICE, WHO
  competency frameworks for health packs; ESCO/O*NET for work packs
- Rubrics for transfer checks: each check gets pass evidence, common
  failure modes, and an assessor note
- Translation infrastructure: `data/i18n/<lang>/` with per-block string
  files; first target languages driven by pilot regions
- Data quality dashboard generated in CI (per-pack completeness, review
  status, reading-level lint)

**New packs (continue generating, same 250-block shape):**
- [x] Food, Cooking & Nutrition — shipped in v0.4.0
- [x] Energy, Grid & the Home — shipped in v0.5.0
- [x] Transport & Mobility — shipped in v0.5.0
- [x] Emergency Preparedness & First Response — shipped in v0.5.0
- [x] Arts, Making Media & Performance — shipped in v0.5.0
- [x] Law, Contracts & Everyday Rights — shipped in v0.5.0

All Phase 1 candidate packs are shipped; further packs come through the
community proposal route (see `docs/wiki/Authoring-Packs.md`).

**Legacy-track localizations** (the app's Willie L. Brown Jr. Institute
model, v29 state template; see `docs/wiki/Legacy-Tracks.md`):
- [x] Civic Leadership Legacy : Louisiana — shipped in v0.6.0
- [x] Civic Leadership Legacy : California (the original edition) —
  shipped in v0.11.0
- [x] Civic Leadership Legacy : Texas (the bridge begins) — shipped in
  v0.11.0
- Further state/country localizations on request, subject to the
  disclaimer and partnership rules on the Legacy Tracks wiki page

**Exit criteria:** zero empty fields dataset-wide; ≥2 packs
standards-mapped; validator extended to rubric and mapping checks.

---

## Phase 2 — Platform (v0.7–v0.9)

**Goal: the app becomes an installable product, not a single artifact.**

- [x] Prove the build pattern (v0.7.0): **Flow Hub** is generated from
  `blocks.csv` by `tools/build_flow_hub.py` — single-file output,
  flow-state session engine, session agents, credential ledger
- [x] Reconcile the app's embedded sector master-block library into
  the dataset (v0.17.0): 5,200 practice blocks extracted, including
  the app-only Education OS edition — `tools/extract_app_blocks.py`
- [x] Education OS onto the pipeline, first stage (v0.19.0):
  `index.html` is now built from `template.html` +
  `tools/build_education_os.py`, with `DATA.sectorBlocks` sourced from
  `data/blocks.csv` (the overlay also cures the template's duplicate
  inflation: 11,520 raw rows → 5,200 canonical). Output stays one
  offline file.
- [x] Enterprise-grade visualization layer (v0.20.0): deterministic
  recursive Voronoi engine (state + curriculum), expansion timelines,
  print program template
- [x] Tutor swarm, voice agents and the active Guide (v0.21.0);
  human-like three-persona voice model across all interactive apps
  (v0.23.0) — on-device only, off by default
- [x] Five style templates with a professional Enterprise default,
  full light/dark variants (v0.22.0)
- [x] Widgetized, deeply customizable role dashboards — six
  perspectives, 30 widgets, per-role layouts persisted (v0.23.0)
- Remaining app-pipeline work: source the app's other data layers
  (wlb course ladders, K–12 program, parish fact base) from canonical
  files the same way, shrinking `template.html` over time
- [x] Learner state, first working version (v0.25.0): local-first
  progress ledger in the Louisiana platform — per-learner check
  records on the 30 core-spine tracks, automatic credential award at
  50 checks, deterministic next-step recommendation and alerts,
  export/import, demo-cohort seeding; no account required. (IndexedDB
  migration and cross-app sync remain future work.)
- [x] Credential ledger v1 (v0.29.0): signed completion records — a
  per-browser Records Office (ECDSA P-256 via WebCrypto), records
  issued offline as portable `cx-credential/1` JSON and verified
  offline against the office's published public key, with tamper
  detection. Alignment with W3C Verifiable Credentials / Open Badges
  3.0 envelopes remains follow-on work.
- Assessor mode: transfer-check queue, rubric display, evidence capture
- Mission simulator: promote from demo to configurable engine driven by
  pack data
- Accessibility: WCAG 2.2 AA audit and fixes; keyboard-complete; screen-
  reader labels on all interactive panels
- Packaging: PWA install, and a printable per-track workbook generator
  (PDF) for zero-device settings

**Exit criteria:** app builds reproducibly from the dataset; a learner can
complete a track and hold a verifiable credential file.

---

## Phase 3 — Deployment & federation (v1.0)

**Goal: real cohorts run on it; instances interoperate.**

- [x] Parish-level platform (v0.9.0): **Cognition.X Louisiana** —
  independent dashboards for all 64 parishes, built from the app's
  fact base and the dataset (`tools/build_louisiana.py`)
- [x] Adopted rollout plan (v0.22.0): the two-year, two-wave statewide
  adoption — 33 parishes (~88% of population) in Wave 1 2026–27, all
  64 by 2027–28 — computed deterministically, with the original
  four-wave proposal kept as provenance
- [x] Pilot playbook as curriculum (v0.22.0): the **Parish Launch &
  Scale** pack (250 blocks — the first ninety days, the Trade Hall,
  training the trainers, enrollment, measure/report/scale) plus
  interactive per-parish Wave-1 readiness boards and a statewide
  rollup — every parish prepares to the Wave-1 standard now
- [x] Regional trades network (v0.23.0): **Cognition.X Trades
  Network** — 111 union & trade entries across San Francisco,
  Oakland–East Bay and New Orleans, regional training simulations,
  the flipped & gamified district model (`TRADESCLASS` pack), and
  district compacts; no union local numbers (councils are the front
  door), simulation never counts as certification
- [x] Parish ↔ union integration (v0.24.0): New Orleans-hall parish
  dashboards surface the trade families whose packs sit in their own
  module plans, sims localized to New Orleans ground
- [x] Staffing, space and device budgets (v0.29.0): a deterministic
  per-parish budget sketch (core team seats, assessor seats by
  population, hall spaces, device count, materials posture for the
  rural tier) on the Parish Admin dashboard and in the program
  export — a scaffold each parish refines, not a quote
- Network expansion: further regions join the Trades Network on the
  same fact-base pattern (families × regions, councils as front doors)
- Instance federation: an instance publishes its pack versions and
  credential issuer keys; credentials verify across instances
- Educator authoring: in-app pack-spec editor producing PRs against
  `data/pack_specs/` (GitHub is the review pipeline)
- Governance: curriculum review board process for accepting new packs and
  breaking changes to existing blocks (documented in the wiki; block ids
  are never reused)
- Evidence loop: anonymised, opt-in transfer-check pass/fail telemetry
  feeding back into block revision priorities
- v1.0 is cut when a named external cohort has completed credentials on an
  unmodified release

---

## Phase 4 — Intelligence (post-1.0, exploratory)

**Goal: adaptive delivery without losing verifiability.**

- [x] Machine-learning architecture (v0.10.0): CX-Trace v1 format,
  flow-state as machine curriculum, ecosystem evaluation criteria and
  the four data principles (`docs/AGENT_LEARNING.md`)
- Adaptive sequencing: recommend next block from prior transfer-check
  outcomes (the mission simulator's difficulty model, generalised)
- AI study partner: block-scoped tutoring with the *Working with AI*
  pack's own norms enforced (no substitution on transfer checks)
- Auto-drafted pack specs: model-generated first drafts routed through
  the human curriculum board — never merged unreviewed
- Cross-pack graphs: prerequisite inference between blocks across packs
  (e.g. Money ⇄ Housing ⇄ Reentry), rendered in the app

---

## Standing tracks (every phase)

- **Data integrity:** validator only ever gets stricter; ids are forever
- **Versioning discipline:** MINOR for additive packs/features, MAJOR for
  schema or id-format changes, PATCH for corrections
- **Openness:** everything in this repo stays Apache-2.0 / CC BY 4.0
