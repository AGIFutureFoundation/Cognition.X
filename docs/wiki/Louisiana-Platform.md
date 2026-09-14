# Louisiana Platform

**Cognition.X Louisiana** models the Education OS over Louisiana's real
structure — 64 parishes, 8 regions, 8 Trade Halls — with an
**independent dashboard for every parish**:
[`apps/louisiana/index.html`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/apps/louisiana/index.html)
(~490 KB single file; opens locally).

## Surfaces

- **The State** — live totals, an interactive **stylized tile
  cartogram** of the 64 parishes colored by adopted rollout wave (click
  any tile), parishes-per-wave / parishes-per-region charts, and the
  statewide Wave-1 readiness rollup. The adopted plan is a **two-year,
  two-wave rollout** — 33 parishes (≈88% of population) in Wave 1
  2026–27, all 64 by 2027–28 — computed deterministically from the fact
  base; the original four-wave proposal is retained per parish as
  provenance.
- **Parish Dashboards** — one per parish, deep-linkable
  (`#/parish/east-baton-rouge`): parish seal, seat, region and Trade
  Hall, wave timeline with the parish's cohort highlighted, school
  systems, anchor industries and the parish's **narrative world**,
  region population context (parish emphasized), the curriculum ledger
  and credential ladder, the Louisiana civic tracks, and per-parish
  notes saved in the browser.
- **Parish module plans (v0.12.0)** — the deep integration: every
  parish dashboard lists the core spine — which since v0.15.0 includes
  **Cognition.X : Louisiana OS**, the state's own 500-block edition
  (river, coast, energy corridor, ports, agriculture, the Louisiana
  table, music, heritage languages, krewes & festivals, storm memory) —
  plus the packs matched to its own anchor industries by the build-time
  rules engine, each with the industry phrase that earned it; tracks deep-link into Flow Hub
  sessions (`#track=<SLUG>/<PREFIX>`) when the apps sit together in
  the repository.
- **Parish mission modules (v0.16.0)** — the custom capstone layer:
  each parish carries a five-rung ladder generated from its own
  narrative world (Explorer observes it, Builder models it,
  Practitioner works inside it, Lead proposes an improvement at the
  Trade Hall, the capstone teaches it to a younger cohort). Generated
  scaffolds, labeled for committee refinement; rural-tier parishes get
  offline-evidence wording.
- **The Makers' Hall (v0.48.0)** — the culture trades as a view of
  their own: music, culinary, and arts & craft, each drawn as an SVG
  **pathway map from creation to industry** whose five stages are the
  five tracks of its pack (*Music : Creation to Industry*, *Culinary
  Trades : The Louisiana Kitchen*, *Arts & Craft Trades : Louisiana
  Makers*). Clicking a stage filters the **role ladder** (154 job
  titles across the three trades — songwriter to sync-licensing agent,
  dishwasher to franchisee, sign painter to conservator), the track
  list (Flow Hub deep links), and the **Makers' Hall** of 63 figures
  from the public record — each with what they did, the lesson a
  learner can take, and a transfer check to actually do — filterable
  by parish or region, with 42 schools, programs, museums and
  festivals listed by parish. Naming is not endorsement; living local
  practitioners are left for the parish to name; every region has at
  least one maker. Parish dashboards gain a *Makers from this parish*
  panel (falling back to the region, and saying so), a parish whose
  makers worked a discipline earns that trade pack in its module plan
  with the reason stated, and the Student, Teacher, Parent and
  Homeschool dashboards carry *A maker from your parish* — one figure
  at a time, rotating daily or on demand, parish first, then region,
  then state. Deep link: `#/makers/<discipline>/<parish-slug>`.
- **Dashboard agent swarms (v0.42.0)** — every role dashboard opens
  with its own crew of agents on a shared blackboard (24 agents
  across the seven roles): each computes a priority and a concrete
  call from the browser's real state — the ledger, the flow engine,
  the witness queue, readiness boards, budgets and missions — and
  priority arbitration surfaces **one call as the swarm's**, spoken
  on demand by the voice model. Every agent's own call, priority
  and watch stay listed under the arbitrated call: *agents propose;
  the person disposes*. Recomputed on a 10-second pulse; a
  default-on widget, toggleable like any other.
- **Role dashboards (v0.18.0; widgetized v0.23.0)** — the *Dashboards*
  view: Student, Teacher, Parent, Homeschool, Parish Admin and State
  Admin — seven in all, Assessor included — each rebuilt on a widget
  system (52 widgets): every
  perspective composes its own dashboard — toggle panels, reorder
  them — with the layout persisted per role in the browser. Full-view
  widgets include the student's flow launcher and journal, the
  teacher's trainer track / flipped units / parish readiness, the
  parent's family ledger and hall card, the homeschool co-op guild,
  the parish admin's five honest numbers and launch team, and the
  state admin's readiness rollup and Trade Hall launch load.
- **The Evidence Loop (v0.36.0)** — an opt-in, consent-gated
  cx-evidence/1 export on the State Admin dashboard: per-track
  aggregates only (no names, no per-learner rows), never transmitted
  by the page; `tools/evidence_triage.py` turns collected files into
  block-revision priorities for the review board. Evidence proposes;
  the board disposes.
- **Federation v1 & v2 (v0.34.0, v0.38.0)** — the Records Office
  verifies records in four grades: invalid, valid-but-untrusted-key,
  *signed by trusted office "X"* by name (against a browser-local
  registry of other halls' published public keys, added after one
  out-of-band identity confirmation; public-half only; removable),
  and *⊘ revoked by issuing office* — checked against
  `cx-revocation/1` lists that the issuing office signs with the
  same key its records carry and that are signature-verified before
  import. Trusted-office registries exchange as portable
  `cx-trustlist/1` files, with imported entries marked second-hand
  until confirmed out-of-band; issued records carry a unique `rid`
  and the dataset version.
- **Assessor Mode (v0.32.0)** — the seventh role dashboard: a
  witnessed-check queue fed by student requests, the three-line
  rubric (real material · independent at band · would transfer),
  per-learner access-profile check formats, evidence capture, and
  confirm / not-yet outcomes that credit the ledger honestly — the
  witnessed record being what the Records Office signs.
- **Credential Ledger v1 & launch budgets (v0.29.0)** — the Records
  Office: a per-browser ECDSA P-256 keypair issues ledger-earned
  credentials as portable, offline-verifiable `cx-credential/1` JSON
  (tamper-detected; verification proves the record unaltered and
  signed by that key's holder, with issuer identity confirmed via the
  hall's published public key). Plus a deterministic per-parish
  staffing / spaces / devices / materials budget sketch on the Parish
  Admin dashboard and in the program export.
- **The Trade Hall Network OS (v0.28.0; granular v0.40.0)** — the
  Regions view as an eight-section operating console: eight system
  automations (Flow Keeper, Break Caller, Step Tuner, Credential
  Clerk, Cohort Watch, Readiness Sentinel, Teacher Relief, Network
  Sync) computing live from the browser's ledger, readiness boards
  and missions, each showing its current call, on a 20-second pulse.
  Since v0.40.0 every section expands into its own **granular
  drill-down board**: the automation's exact thresholds stated in
  plain terms, the per-learner or per-parish rows it computed from
  (channel positions with last-3 sums, moves-since-break against
  each profile's own cadence, pending step calls by name,
  near-credential counts like 49/50, the full alert list, each
  preparing parish's next missing requirement, the teacher-relief
  inputs, all eight halls' live counts), and a pulse log of recent
  calls — nothing the console says is a black box. Region cards
  carry their live section state, and the teacher's Class flow board
  opens with the teacher's own flow state and a concrete relief
  automation — keeping teachers, not just learners, in the channel.
- **Flow-state engine & access modules (v0.27.0)** — a per-learner
  flow model (warming up / in flow / cruising / overloaded / break
  called) whose automations steer the experience: shrink the step
  under overload, stretch when cruising, call the break on the
  learner's own cadence. Twenty learner-type access modules —
  **chosen supports, never diagnoses** — tune the cadence, the step
  bias and the check formats; the student runs a live Flow Session,
  the teacher reads the Class flow board, the parent sees What helps
  my child, and the admins see state distributions. Backed by the
  Learning States & Universal Access pack.
- **Learner ledger & standing (v0.25.0)** — a browser-local,
  consent-first progress model over the 30 core-spine tracks with
  working automations: automatic credential award at 50 recorded
  checks, deterministic next-step recommendations, near-credential
  and not-started alerts, export/import, and a one-tap demo cohort.
  Every role sees standing at its own altitude: the student's meters
  and suggested next step, the teacher's class bars + class×track
  heatmap + one-tap crediting, the parent's child view, the parish
  rollup, and the State Admin's complete-system overview.
- **Parish ↔ union integration (v0.24.0)** — parish dashboards in the
  New Orleans Trade Hall region surface the trade families (from the
  [[Trades Network]] fact base) whose packs sit in that parish's own
  module plan, each with its New Orleans-localized training sim;
  other parishes link across to the network.
- **Plan customizer & program export (v0.16.0)** — industry packs can
  be set aside, any catalog pack added as a parish choice (persisted
  per parish in the browser), and the whole program exported as
  `cxla-program/1` JSON.
- **Guide & voice (v0.21.0; humanized v0.23.0)** — the 🧭 Guide button
  walks users through all nine surfaces (helper-agent tour with
  Back/Next, navigating views itself); the voice option narrates via
  on-device speech synthesis with three personas (Warm / Steady /
  Brisk), a natural-voice preference list and sentence-level prosody —
  off by default, nothing leaves the page.
- **Voronoi cells & expansion timelines (v0.20.0)** — a recursive
  tessellating Voronoi of the state (regions → parishes, area ∝
  population, wave-colored, clickable) and of the curriculum
  (families → packs, area ∝ blocks), built by a deterministic
  power-diagram engine with no libraries; plus cumulative
  expansion-to-Wave-4 timelines (parishes live, population covered)
  and a print-ready parish program one-pager.
- **Regions & Trade Halls** — the eight regions, each hall's hub city,
  wave-mix bars, the packs most assessed at each hall, and parish
  links.
- **Curriculum** — dataset totals, the series-by-family bar, the
  *Civic Leadership Legacy : Louisiana* tracks, and the community packs
  every parish plan draws from.

## Data provenance

Built by `tools/build_louisiana.py` from canonical sources, never
hand-edited:

1. **`data/louisiana/fact_base.json`** — regions, hub cities, and
   per-parish name/seat/region/population/wave/districts/industries/
   narrative-world/rural-tier (canonical since v0.39.0; originally
   extracted from the Education OS app by
   `tools/extract_fact_bases.py`).
2. **`data/wlb/institute.json`** — the Institute fact base, with the
   disclaimer carried verbatim.
3. **`data/blocks.csv`** — curriculum totals and the Louisiana legacy
   pack's tracks, computed at build time.
4. **`data/unions/trade_unions.json`** and
   **`data/learners/learner_types.json`** — the trade-hall union
   slices and the 20 access profiles.

Waves are the proposal's planned rollout (2027–28 → 2030–31), not an
adopted schedule; the tile map is a stylized cartogram with approximate
positions. Parish notes live only in the viewer's browser.

## Design

Light-first civic design: warm paper ground, Fraunces display serif,
a Mardi Gras purple/gold/green identity in the wordmark and accents,
and a CVD-validated 4-color wave palette for every chart — with a full
dark theme mirrored token-for-token.
