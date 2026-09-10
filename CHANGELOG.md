# Changelog

All notable changes to Cognition.X are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org).

## [0.20.0] — 2026-09-10

### Added
- **Recursive tessellating Voronoi graphics** (deterministic power-
  diagram engine, no libraries, offline): *The state as cells* — the
  eight regions partition the plane, each tessellated by its parishes,
  **cell area ∝ population**, color by wave, stitched heavy borders
  between regions, hover tooltips and click-through to parish
  dashboards; and *The curriculum as cells* — families tessellated by
  packs, area ∝ blocks. Both redraw on theme change; the State Admin
  dashboard embeds the state Voronoi.
- **Expansion to Wave 4 timelines**: cumulative step-area charts of
  the build-out to full run — parishes live (5 → 21 → 40 → 64) and
  population covered (27% → 76% → 92% → 100% by 2030–31).
- **Print template**: a "Print program" button and print stylesheet
  turn any parish dashboard into a clean program one-pager.
- Ambiguous parish abbreviations disambiguated (LFR/SMY/SMT) across
  the tile map, Voronoi and seals.

## [0.19.0] — 2026-09-10

### Changed
- **The Education OS app is now a build product** (roadmap Phase 2
  finale, first stage). The hand-grown "gov" build becomes
  `apps/education-os/template.html` (kept verbatim as the shell and
  legacy content); `tools/build_education_os.py` produces `index.html`
  by appending a canonical overlay that replaces `DATA.sectorBlocks`
  with the sector master-block library **as it stands in
  `data/blocks.csv`** — dataset edits now flow into the app, and the
  sector library has one source of truth. Field fidelity is preserved
  via the extraction sidecar (`app-master-blocks.map.json`): original
  task/outcome fields re-emitted where the dataset is unchanged, the
  dataset winning where edited.
- Side effect measured in the browser: the template's accumulated
  library had inflated to **11,520 rows with duplicates** across
  rounds; the canonical overlay serves the clean **5,200**. The app's
  single pre-existing page error is unchanged (template baseline).
- The extractor and the Louisiana fact-base reader now read
  `template.html`; the output remains one offline file.

## [0.18.0] — 2026-09-10

### Added
- **Parish curriculum in full run.** Parish review passed (all 64
  parishes: 5/5 missions, matched plans, worlds, waves), and mission
  modules are now *runnable*: each rung has a completion checkbox with
  a progress meter, persisted per parish in the browser and rolled up
  into the admin dashboards.
- **The Institute Model — the universal all-states pack.**
  *Civic Leadership Legacy : The Institute Model* (250 blocks, 5
  tracks): leadership as service (the twelve principles in practice),
  the room and the count (coalition/negotiation/consensus), **emotional
  intelligence for public life** (a full EQ track — self-awareness,
  de-escalation, empathy without surrender, the steady presence), civic
  duty anywhere (the eight slots as literacy), and ethics under
  pressure. State-agnostic, localizable through the eight-slot
  template; the Institute view now presents it as the universal
  training model. Disclaimer carried.
- **Six role dashboards** (new *Dashboards* view): **Student** (parish
  + runnable mission ladder), **Teacher** (class roster, Louisiana OS
  unit picker, transfer-check roll), **Parent** (band explainer with
  ladder highlight, home log), **Homeschool** (band picker, weekly
  planner, spine chips, home-study note), **Parish Admin** (plan/
  mission/wave tiles, districts, hall), **State Admin** (totals, wave
  rollout, mission-record count). All records browser-local, stated
  plainly.
- Canonical totals: **15,200 blocks · 38 packs · 180 tracks**.

## [0.17.0] — 2026-09-10

### Added
- **App reconciliation, first slice (roadmap Phase 2).** The Education
  OS app's embedded **sector master-block library** — 5,200 uniform
  practice blocks (`DATA.sectorBlocks`, codes `T0A…T0Z`) accumulated
  across the app's internal rounds and never present in the CSV
  export — is now extracted into the canonical dataset by the new
  `tools/extract_app_blocks.py` (deterministic; later-round
  redefinitions win). 909 adult practice tracks land as `Lead`-level
  micro-blocks (task + outcome as the transfer check) across the seven
  existing OS editions and Non-Profit Practice — and reveal a whole
  new edition: **Cognition.X : Education OS** (660 blocks), previously
  app-only.
- Flow Hub surfaces each OS edition's practice library ("+660 master
  practice blocks…") alongside its banded tracks; pack-family
  classification now keys on names so grown OS packs stay OS.
- Canonical totals: **14,950 blocks · 37 packs · 175 tracks · 1,360
  credentials**.

## [0.16.0] — 2026-09-10

### Added
- **Parish mission modules** — the custom layer over the universal
  dataset: every parish dashboard now carries a five-rung capstone
  ladder (Explorer→Builder→Practitioner→Lead→capstone) generated at
  build time from *that parish's* narrative world in the fact base —
  Acadia models its rice-mill automation line, Cameron its LNG loading
  arm — with Lead presenting at the parish's own Trade Hall, the
  capstone teaching a younger parish cohort, and rural-tier parishes
  getting offline-evidence wording. 64 parishes × 5 missions = 320
  generated scaffolds, labeled as such for committee refinement.
- **Plan customizer**: each parish's module plan can now be locally
  tailored — industry packs can be set aside (and restored), any pack
  in the full catalog added as a "parish choice" — persisted per
  parish in the browser.
- **Parish program export**: one button produces the complete parish
  program (`cxla-program/1` JSON — spine, industry packs with reasons,
  parish choices, set-asides, missions) for sharing with a committee.

## [0.15.0] — 2026-09-10

### Added
- **Cognition.X : Louisiana OS** — the state's own full OS edition and
  the deep Louisiana program curriculum: 500 blocks (10 tracks × 10
  themes × 5 bands). The working state: *The river* (Old River
  Control, spillways, gauges, sediment), *The working coast* (land
  loss, the Master Plan, fisheries, stay-or-go), *The energy corridor*
  (refineries, LNG, turnarounds, fence line, transition), *Ports and
  the river highway* (grain, pilots, dredging, intermodal), and
  *Agriculture* (rice, the crawfish rotation, sugarcane, extension).
  The culture: *The Louisiana table* (roux, gumbo lineages, the boil,
  boudin), *Music* (Congo Square, jazz, brass bands, zydeco, Cajun,
  gospel, blues), *French, Creole and the languages of home* (Kouri-
  Vini, the punishment generation, immersion, the elders' tapes),
  *Krewes and festivals* (the krewe as organization, float craft,
  social aid & pleasure clubs), and *The storm and the long memory*
  (1927, Katrina from the investigations, the diaspora, oral history).
  Every transfer check is phrased against the learner's own parish.
- Louisiana OS joins the **core spine** of every parish module plan
  (with K–12, the civic legacy pack, life skills and emergency
  response).
- Canonical totals: **9,750 blocks · 36 packs · 175 tracks · 451
  credentials**.

## [0.14.0] — 2026-09-10

### Added
- **Structural backfill complete.** The 1,000 irregular foundation rows
  (K–12, Trade School, Future-Work, Regional, Civic & Leadership,
  Health & Community, Language/Culture, Empathy & EI, Community &
  Relationship) now carry a `code` (`LB-<n>`, unique within pack) and a
  `level` derived from their grade — including single grades (K→
  Explorer … 12→Lead), adult bands (→Lead) and Trade School capstones.
  These packs' shapes are genuinely irregular (per-grade ladders, adult
  capstones, staggered themes), so they are deliberately **not** forced
  into the 10×5 tracked shape; `track` and `description` on these rows
  remain the last content-authoring item.
- **Validator strengthened**: `code` and `level` are now required on
  every row dataset-wide, locking in the guarantee.

## [0.13.0] — 2026-09-10

### Changed
- **Placeholder transfer checks eliminated.** Authored real, per-theme
  transfer checks for all 217 themes that carried the source's generic
  placeholder sentences (Basic Life Skills 50, Water Land & Climate 50,
  Care Across a Life 50, Making Repair & Reuse 50, Preventive Health
  17) — 1,085 rows updated. The replacement is guarded: the normalizer
  substitutes an authored check **only** when the existing value is one
  of the two known placeholder sentences (`PLACEHOLDER_CHECKS` in
  `tools/normalize_blocks.py`); real source checks are never touched.
  Zero placeholder checks remain dataset-wide. Closes the data-review
  finding 2b and the roadmap item it opened.

## [0.12.0] — 2026-09-10

### Added
- **Deep module ↔ system integration, Louisiana first.** Each parish
  dashboard now carries a **Parish module plan**: the core spine every
  parish runs (K–12, the Louisiana civic pack, Basic Life Skills,
  Emergency Preparedness) plus curriculum packs matched to that
  parish's own anchor industries by a rules engine in
  `tools/build_louisiana.py` — every match labeled with the industry
  phrase that earned it ("because: LNG terminals (Sabine Pass…)").
  All 64 parishes match at least one industry pack.
- **Flow Hub deep links**: `#track=<PACKSLUG>/<PREFIX>` preselects a
  pack and track and opens the Flow view; parish module plans link
  each track straight into a flow session when the apps sit together
  in the repository.
- Trade Hall cards now list the packs most assessed at each hall
  (union of member-parish plans); the State view gains a
  **modules-matched-to-industries** chart across the 64 parishes.

## [0.11.0] — 2026-09-10

### Added
- Two more legacy-track localizations, extending the flagship across
  states (250 blocks each, 5 tracks × 10 themes × 5 bands):
  - **Civic Leadership Legacy : California** — the original edition:
    the Fellowship ladder, counties & cities (Brown Act, Prop 13,
    general plans), the Sacramento Legislature (including the craft of
    counting votes), elections with the top-two primary and the
    initiative system, and fire/water/fault-line resilience civics.
  - **Civic Leadership Legacy : Texas** — the edition of the bridge
    (Mineola, 1934): education as the bridge across barriers, the 254
    counties and commissioners courts, the biennial Austin Legislature,
    Texas elections, and storm/grid/coast resilience civics (Harvey,
    Uri, the aquifers).
  Both carry the Institute's not-affiliated disclaimer in their specs.
- The Institute localizer in the Louisiana platform gains a **Texas**
  edition row.
- Canonical totals: **9,250 blocks · 35 packs · 165 tracks · 441
  credentials**.

## [0.10.0] — 2026-09-10

### Added
- **Legacy Institute flagship** in the Louisiana platform: the twelve
  Willie L. Brown Jr. Institute principles rendered as leadership /
  ethics / civic-duty arcs with sources and teaching notes, the record
  behind them, the vision-statement quote, and an interactive
  **eight-slot localizer** resolving the model for Louisiana,
  California, any U.S. state and any country — the cornerstone for
  every edition. The app's not-affiliated disclaimer travels with it.
- **Agents & Robots view**: the one-block-two-learners loop diagram,
  the five machine-learnable signals per module, flow-state as machine
  curriculum (Explorer→Lead for robots), the **CX-Trace v1** format,
  four named ecosystem candidates (Sentient Foundation, Virtuals
  Protocol, Hugging Face LeRobot, ROS 2 — evaluation only, no
  affiliation), and the four non-negotiable data principles.
  Architecture doc: `docs/AGENT_LEARNING.md`.
- **Style options** across the platform: theme (System/Light/Dark) and
  style (Parade/Classic) switchers in Louisiana; theme switcher in
  Flow Hub. Preferences persist per browser.
- **Flow Hub trace export**: the Archivist's *Copy training trace*
  produces CX-Trace v1 (anonymized, `share:false` by default) from the
  local session data.

## [0.9.0] — 2026-09-10

### Added
- **Cognition.X Louisiana** (`apps/louisiana/`): a parish-level
  education platform modeled on Louisiana's real structure — an
  **independent, deep-linkable dashboard for each of the 64 parishes**
  (seal, seat, region & Trade Hall, rollout wave timeline, school
  systems, anchor industries and narrative world, region population
  context, curriculum ledger, Louisiana civic tracks, per-parish notes),
  plus a State overview with an interactive **stylized tile cartogram**
  of the 64 parishes colored by rollout wave, wave and region charts,
  a Regions & Trade Halls view, and a Curriculum view. Light-first
  civic design with a Mardi Gras (purple/gold/green) identity, Fraunces
  display type, a validated 4-wave chart palette, and a full dark theme.
- `tools/build_louisiana.py`: builds the platform from the Louisiana
  fact base embedded in the Education OS app (regions, hubs, 64
  parishes with seats/population/waves/industries) plus curriculum
  stats computed from `data/blocks.csv` — same Phase 2 pattern as
  Flow Hub: a build product, never hand-edited.

## [0.8.0] — 2026-09-09

### Added
- **Legacy backfill, first slice** (roadmap Phase 1): the five cleanly
  banded legacy packs — Basic Life Skills & Self-Reliance, Preventive
  Health & Everyday Care, Water Land & Climate, Care Across a Life,
  Making Repair & Reuse — are promoted to the tracked schema. Their
  track groups were already embedded in the source as `(XX)` theme
  suffixes; promotion specs (`data/promotions/*.json`) supply track
  names and 250 authored base descriptions, and the normalizer fills
  the empty `track`/`code`/`level`/`description` fields (source values
  are never overwritten; `block_id`s unchanged). 1,250 rows backfilled;
  **155 tracks** now tracked; untracked foundation rows drop from
  2,250 to 1,000 (K–12, Trade School, and the seven irregular thematic
  packs remain).
- Flow Hub rebuilt: the five promoted packs join the flow engine and
  the community family.

### Noted
- New data-review finding: most legacy transfer checks are generic
  placeholders ("Do it once, for real…"); authoring real per-theme
  checks is the next backfill target (see `docs/DATA_REVIEW.md`).

## [0.7.0] — 2026-09-09

### Added
- **Flow Hub** (`apps/flow-hub/`): a professional interactive app
  connecting the whole Cognition.X series — System overview (live counts
  and family distribution computed from the dataset), Packs explorer
  (search/filter across all 33 packs down to block level), a **flow
  engine** (challenge-vs-skill session loop with a flow-channel chart
  and time-in-channel meter), four rule-based **session agents**
  (Pathfinder selection, Pacer focus intervals, Assessor transfer-check
  recording, Archivist ledger export/import), and a **credential
  ledger** with per-track progress. Dark-first with a full light theme;
  per-browser persistence.
- First realization of the roadmap Phase 2 build pattern:
  `tools/build_flow_hub.py` injects the canonical dataset into
  `apps/flow-hub/template.html` — the app is a build product of
  `data/blocks.csv`, never hand-edited.

## [0.6.0] — 2026-09-09

### Added
- First **legacy-track localization** in the dataset: pack **Civic
  Leadership Legacy : Louisiana** (250 blocks, 5 tracks × 10 themes ×
  5 bands) — the Willie L. Brown Jr. Institute civic-leadership model
  (Education OS app iterations v28–v30) localized to Louisiana via the
  app's v29 template (capital, legislature, **parish** unit, standards,
  civic seal *verify*, anchor industries, placement ladder, fellowship
  partner). Tracks: the Louisiana public-service ladder, parish
  government, the Legislature & civil-law tradition, Louisiana
  elections, and coastal civics (water, storm, levee boards, recovery).
  Carries the app's not-affiliated proposal disclaimer; see
  `docs/wiki/Legacy-Tracks.md`.
- Wiki page `docs/wiki/Legacy-Tracks.md`: the legacy-track model, the
  localization template, and the disclaimer rules for honouring named
  public figures.
- Canonical totals: **8,750 blocks · 33 packs · 130 tracks · 437
  credentials**.

## [0.5.0] — 2026-09-09

### Added
- Five new community packs (250 blocks each, 5 tracks × 10 themes × 5
  bands), completing the roadmap Phase 1 candidate list:
  - **Energy, Grid & the Home** — home electricity, heating/cooling,
    grid literacy, water/gas utilities, energy efficiency
  - **Transport & Mobility** — transit navigation, cycling & bike
    mechanics, car ownership, road safety, journey planning
  - **Emergency Preparedness & First Response** — household readiness,
    lay first aid, fire safety, natural hazards, community response
  - **Arts, Making Media & Performance** — drawing & visual craft,
    music, camera & editing, stage & speech, design & making
  - **Law, Contracts & Everyday Rights** — the legal system, contracts,
    consumer rights, workplace rights, citizen & state
- Canonical totals: **8,500 blocks · 32 packs · 125 tracks · 432
  credentials**.

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
