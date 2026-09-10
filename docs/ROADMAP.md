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
  - Remaining 1,000 rows: K–12 (64), Trade School (47), Future-Work,
    Regional, Civic & Leadership, Health & Community, Language/Culture
    (111 each), Empathy & EI and Community & Relationship (167 each) —
    irregular shapes needing per-pack design, not mechanical promotion
- Replace the placeholder transfer checks surfaced by the v0.8.0
  review ("Do it once, for real…" on most pre-promotion legacy rows)
  with real per-theme checks — content authoring, ~440 themes
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
- Split the 8 MB Education OS single-file app onto the same pipeline,
  keeping the *output* single-file and offline-first — that constraint
  is a feature for low-connectivity deployments
- Learner state: local-first progress store (IndexedDB) with export/import;
  no account required
- Credential ledger v1: signed completion records (W3C Verifiable
  Credentials / Open Badges 3.0), issuable offline, verifiable online
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
- Pilot playbook: the parish/Trade-Hall implementation plans in the app
  become operational checklists with staffing, space and device budgets
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
