# Cognition.X — Deep Roadmap

Direction of travel: from a curriculum **dataset + demo app** (the
start) to a verifiable, federated **learning operating system** that a
school, parish, ministry or employer can run. Phases are sequential but
overlapping; versions follow SemVer and are cut when a phase's exit
criteria pass.

## Status at v0.48.0 (system review: [`SYSTEM_REVIEW.md`](SYSTEM_REVIEW.md))

- **Phase 0 — Foundation: complete.**
- **Phase 1 — Data completeness: complete** except the foundation
  library's authored tracks/descriptions (the standing content debt).
- **Phase 2 — Platform: nearly complete.** Shipped: Flow Hub, Education
  OS on the pipeline, learner state, credential ledger v1, assessor
  mode, printable workbooks, tutor swarm/voice/guide, styles, widget
  dashboards, PWA install metadata (v0.34.0), the accessibility first
  pass (v0.33.0), and all four canonical fact-base layers (v0.39.0,
  v0.43.0, v0.44.0). Open: the full WCAG 2.2 AA audit, restoring the
  Education OS's imported design system, and injecting the canonical
  layers back to shrink `template.html`.
- **Phase 3 — Deployment: well underway.** Shipped: Louisiana platform
  + adopted 2-wave plan + launch curriculum/budgets/readiness, Trades
  Network (6 regions), States app (50 states), Network OS automations
  with granular per-section boards (v0.40.0), dashboard agent swarms
  (v0.42.0), federation v1–v2 (v0.34.0, v0.38.0), educator authoring
  (v0.35.0), governance (v0.35.0), the evidence loop (v0.36.0) and the
  culture trades (v0.48.0: music creation→industry, culinary and
  arts-and-craft trade packs with the Makers' Hall of public-record
  examples by parish). Open: the v1.0 external-cohort gate (operational, below) and W3C
  Verifiable Credentials / Open Badges 3.0 envelope alignment.
- **Phase 4 — Intelligence: architecture shipped** (CX-Trace, flow
  model, data principles); adaptive sequencing exists in first working
  form (the ledger's recommendation + flow automations); the rest is
  post-1.0.
- **Engineering integrity (v0.41.0, v0.45.0):** a fresh clone plus
  Python 3 reproduces every app byte-for-byte, and CI enforces it;
  `tests/test_platform.py` holds the standing stances mechanically on
  every push, with `tests/browser/smoke.js` exercising the working
  models before an app ships.

**Recommended order of next work** — the ranked, self-contained
sessions are written out in
[`docs/NEXT_STEPS_OPUS5.md`](NEXT_STEPS_OPUS5.md). In short: ① restore
the Education OS design system (done, v0.46.0) → ② author the 24 missing credential
names (drafted v0.52.0; board adoption pending) → ③ finish the WCAG 2.2 AA audit (done, v0.53.0) → ④ close the
remaining verified review findings → ⑤ standards mapping and rubrics (done, v0.56.0) →
⑥ W3C VC / Open Badges alignment (done, v0.60.0) → ⑦ cut v1.0 when a named external
cohort completes credentials on an unmodified release.

---

## Phase 0 — Foundation (v0.3.x) ✅

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
  band-differentiated descriptions (most bands share one sentence
  with an "— at {band}" suffix) — the largest content-quality lift.
  Started in v0.65.0: pack specs and promotions carry `bands` (five
  sentences per theme in what the learner does); two core-spine packs
  authored (500 rows); the suffix count is a ratchet in the tests that
  only falls. Remaining core spine: Louisiana OS, Civic Leadership
  Legacy Louisiana, Basic Life Skills
- Standards mapping tables: Common Core / NGSS for K–12 packs; NICE, WHO
  competency frameworks for health packs; ESCO/O*NET for work packs
- Rubrics for transfer checks: each check gets pass evidence, common
  failure modes, and an assessor note
- Translation infrastructure: `data/i18n/<lang>/` with per-block string
  files; first target languages driven by pilot regions
- [x] Data quality dashboard generated in CI (v0.44.0):
  `tools/data_quality.py` → `docs/DATA_QUALITY.md`, per-pack
  completeness with the content debt counted openly; regenerated and
  drift-checked by the CI dataset job on every push. (Review status
  and reading-level lint remain future columns.)

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

- [x] Standards mapping, first two frameworks (v0.56.0):
  `data/standards/lss-k12.json` (generated from the K–12 program; block
  scope, *cites*) and `data/standards/ngss-ets-robotics.json` (four
  Robotics OS tracks × five bands; *touches*); every code carries the
  caveat to verify. `docs/STANDARDS.md`.
- [x] Transfer-check rubrics for the 30 core-spine tracks (v0.56.0):
  pass evidence, failure modes, assessor note — in Assessor Mode, the
  Flow Hub pack detail and the printed workbook.
- [x] Validator extended to rubric and mapping checks
  (`tools/validate_standards.py`, CI).

**Exit criteria:** zero empty fields dataset-wide; ≥2 packs
standards-mapped (done, v0.56.0); validator extended to rubric and
mapping checks (done, v0.56.0).

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
- [x] App-pipeline work, stage two (v0.39.0): the Louisiana
  region/parish fact base and the WLB Institute fact base are
  canonical repository data (`data/louisiana/fact_base.json`,
  `data/wlb/institute.json`, extracted once by
  `tools/extract_fact_bases.py`); the Louisiana and States builders
  read the canonical files and no longer evaluate the app template —
  round-trip verified byte-identical. The WLB leadership curriculum
  (strands, eras, 125 course ladders, modules, bridge, standards,
  seal) joined the canonical file in v0.43.0 and renders in the
  Louisiana and States Institute views. The K–12 program layer
  joined in v0.44.0 (`data/louisiana/k12_program.json`, rendered in
  the Curriculum view) — every named display layer is now canonical.
  Closed in v0.63.0: the Education OS is built FROM the canonical
  files — the template holds a placeholder where each of the seven
  literals stood (regions, hubs, parishes, the WLB fact base and
  principles, the K–12 grades and threads; 53 KB of duplicated
  facts gone), the builder injects the JSON in place, every view
  renders identically, and `tools/extract_fact_bases.py` reads the
  built app back and must reproduce the canonical files byte for
  byte in CI. One source of truth per fact, at last
- [x] Learner state, first working version (v0.25.0): local-first
  progress ledger in the Louisiana platform — per-learner check
  records on the 30 core-spine tracks, automatic credential award at
  50 checks, deterministic next-step recommendation and alerts,
  export/import, demo-cohort seeding; no account required. Durable
  state landed in v0.57.0–v0.62.0 (office key, ledger, trust and
  revocation lists in IndexedDB; restore from the custody bundle on a
  second device). Cross-device continuity is that bundle, carried by
  hand — no sync service, by design.
- [x] Credential ledger v1 (v0.29.0): signed completion records — a
  per-browser Records Office (ECDSA P-256 via WebCrypto), records
  issued offline as portable `cx-credential/1` JSON and verified
  offline against the office's published public key, with tamper
  detection. Open Badges 3.0 / VC 2.0 envelopes (`vc+jwt`, `did:jwk`,
  same key and record id) shipped in v0.60.0 — `docs/CREDENTIALS.md`.
- [x] Assessor mode (v0.32.0): witnessed-check queue (students request,
  assessors work oldest-first), three-line rubric display, per-learner
  access-profile check formats, evidence capture, and confirm /
  not-yet outcomes that credit the ledger honestly
- [x] Mission simulator promoted to a configurable engine driven by pack
  data (v0.54.0): the Simulation Studio — `data/simulations/scenarios.json`
  (18 scenarios tied to real tracks, each carrying its witnessed transfer
  check verbatim) played by one shared engine (`tools/sim/engine.js`) in
  all six apps; deterministic, three difficulties, no timers, `cx-simrun/1`
  run records that are practice and never credentials
- Accessibility: WCAG 2.2 AA audit and fixes; keyboard-complete; screen-
  reader labels on all interactive panels
- [x] Packaging (v0.32.0–v0.34.0): printable per-track workbooks
  (Flow Hub's 🖨 button) and PWA install metadata in all four apps
  (runtime manifest + theme metas). Honest scope: installability
  depends on the browser and https serving — the single offline file
  itself remains the primary packaging; a service-worker build is
  possible later work if the apps gain first-party hosting.

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
- [x] Network expansion, first round (v0.30.0): Baton Rouge–River
  Region, Houston–Gulf Coast and Los Angeles join on the fact-base
  pattern — 37 families × 6 regions = 222 entries, each new region
  with its own council front door, districts, sites and city map;
  the Baton Rouge Trade Hall's parishes gain their own union panels.
  Further regions continue on the same pattern.
- [x] Instance federation, first slice (v0.34.0): each Records Office
  publishes its public key; another instance adds it (after one
  out-of-band identity confirmation) to its **trusted-offices
  registry**, and verification then grades records three ways —
  invalid, valid-but-untrusted-key, or *signed by trusted office
  "X"* by name.
- [x] Federation v2 (v0.38.0): record ids and dataset versions in
  every issued payload, the portable `cx-trustlist/1` exchange
  format (imported entries marked second-hand until confirmed
  out-of-band), and revocation — `cx-revocation/1` lists signed by
  the issuing office's own key, verified before import, adding the
  fourth verification outcome *revoked by issuing office*.
  Remaining federation work: W3C VC / Open Badges 3.0 envelope
  alignment.
- [x] Educator authoring, first slice (v0.35.0): the **Pack Studio**
  (Flow Hub's Author view) — a form-driven spec editor with live
  generator-grade validation, a worked example, import-to-edit,
  browser-local drafts, and spec export verified to round-trip
  through `generate_pack.py`. Honest scope: the offline file exports
  the spec and the submit instructions; GitHub remains the review
  pipeline (the page cannot open the PR itself).
- [x] Governance (v0.35.0): the curriculum review board process is
  documented in [`docs/GOVERNANCE.md`](GOVERNANCE.md) — board
  composition, the six-point review checklist (accuracy, real checks,
  honesty stances, respectful terminology, shape/provenance, access),
  the acceptance flow, the supersede-never-rewrite breaking-change
  policy, and the standing review queue over the machine-authored
  packs. Seating the board itself is operational work outside the
  repository.
- [x] Evidence loop, first slice (v0.36.0): opt-in **cx-evidence/1**
  aggregate export (per-track counts only, no names, nothing ever
  auto-sent — the export box is the only exit) plus
  `tools/evidence_triage.py`, which merges collected files into
  block-revision priorities for the review board (high witnessed
  not-yet rates flag mis-pitched checks; unused tracks flag
  relevance reviews). Evidence proposes; the board disposes.

### The path to v1.0 (operational checklist)

The remaining v1.0 work is operational, not code — and since v0.61.0 it
has artifacts: `docs/BOARD_PACKET.md`, `docs/COHORT_ONBOARDING.md`,
`docs/templates/CONSENT_FORM.md` and `tools/cohort_report.py`:

1. **Seat the curriculum review board** (docs/GOVERNANCE.md) and
   begin the standing review queue, classroom-facing packs first.
2. **Recruit a named external cohort** — one hall, one class, one
   co-op — running an unmodified release.
3. **Exchange records-office keys** with that cohort (federation v1)
   and collect their opt-in evidence exports through one full track.
4. **Cut v1.0** when the cohort's learners hold verifiable
   credentials and the board has reviewed at least the packs that
   cohort used.
- v1.0 is cut when a named external cohort has completed credentials on an
  unmodified release

---

## Phase 4 — Intelligence (post-1.0, exploratory)

**Goal: adaptive delivery without losing verifiability.**

- [x] Machine-learning architecture (v0.10.0): CX-Trace v1 format,
  flow-state as machine curriculum, ecosystem evaluation criteria and
  the four data principles (`docs/AGENT_LEARNING.md`)
- Adaptive sequencing: recommend next block from prior transfer-check
  outcomes (the studio's next-difficulty rule — v0.54.0 — generalised
  from scenario runs to blocks)
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
