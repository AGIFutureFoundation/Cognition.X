# Changelog

All notable changes to Cognition.X are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org).

## [0.62.0] — 2026-09-16

### Changed — durable state closed out (roadmap prompt 9)
- **Trust and revocation lists on the ledger's durable path.** `cxla.trust`,
  `cxla.revoked` and `cxla.revlists` are now served from an in-memory copy
  behind the same accessors every earlier release called, written through
  to localStorage (the compatibility copy) and to an IndexedDB record in
  `cxla.ledgerdb`; on startup the IndexedDB copy wins when it is at least
  as new (`cxla.dmeta` keeps the localStorage save times). A browser that
  held the lists only in localStorage migrates once, without loss; a save
  refused by localStorage is announced and the list reloads from
  IndexedDB; a save refused everywhere is announced as such.

### Added — restore from a records-custody bundle
- **Records Office → *Restore (merge)*.** A second device, a replacement
  after a loss, a hall that moves rooms: load the dated `cx-custody/1`
  file and the browser merges it — learners by id (the bundle's copy
  replaces a local learner only when the bundle was saved later; an older
  bundle never overwrites), the assessor queue by row, trusted offices by
  key (arriving second-hand, the bundle's office as voucher, until
  confirmed out-of-band again), imported revocation lists only after
  their signatures verify again here, readiness and hall checklists by
  OR for the same parish. This office's own revoked ids restore only
  when the bundle's key is this office's key or no office exists here —
  in which case the office is noted by name and **public** key only, so
  records it signed verify by name while signing stays on the device
  that holds the non-extractable private key. No sync service: a file, a
  person, a channel the two devices already trust.
- Browser suite: `testDurableListsAndRestore` (migration, quota failure,
  merge rules, tampered list rejected, another office's revoked ids
  skipped, the control end to end); Python: `test_durable_lists_and_restore`.
- Register PL-19 widened to the lists and the restore;
  `docs/COMPLIANCE_REVIEW.md` data map and *What remains*,
  `docs/COHORT_ONBOARDING.md` §2, `docs/COMPLIANCE_ROADMAP.md` wave 2,
  `docs/ROADMAP.md`, prompt 9 marked done.

## [0.61.0] — 2026-09-16

### Added — the v1.0 gate made executable (roadmap step ⑦)
- **`docs/BOARD_PACKET.md`** — the Curriculum Review Board's
  first-meeting packet, generated from the repository's own data: the
  agenda, the six-point checklist as a working form, the first decision
  (the 24 proposed credential names from v0.52.0, listed), the standing
  queue of the 22 generated packs (6,160 blocks) in the governance
  order with reviewer and sitting columns, what the board receives at
  every later sitting, and the gate restated. Held to the dataset by
  the tests.
- **`docs/COHORT_ONBOARDING.md`** — the path a hall, class or co-op
  follows: verify the release, meet the thirteen operating controls,
  create the office, enrol with a nickname, run one track to the
  credential, export the custody bundle weekly, exchange keys
  out-of-band with the confirmation step, issue the record, send
  evidence by hand. Every claim matches the code.
- **`docs/templates/CONSENT_FORM.md`** — a consent sheet a family can
  read; the "what the software does" paragraphs are held true by the
  tests (nothing is sent and the browser blocks it; nickname, band and
  chosen supports only; aggregate export optional and nameless;
  simulation is practice).
- **`tools/cohort_report.py`** — turns collected `cx-evidence/1` files
  into the board's packet: the cohort at a glance, every track with its
  witnessed rate and rubric, revision priorities, unreported tracks,
  the standing-queue status of the packs used, and the v1.0 gate status
  as a form. Reuses `evidence_triage.py`.

## [0.60.0] — 2026-09-16

### Added — Open Badges 3.0 / W3C VC 2.0 envelopes (roadmap step ⑥)
- **Issue as Open Badge 3.0.** The Records Office issues the same
  credential, from the same non-extractable key and with the same
  record id, as a compact `vc+jwt`: ES256, `kid` a `did:jwk` of the
  office's public key, the payload an `OpenBadgeCredential` (VC 2.0 and
  OB 3.0 contexts, issuer Profile, AchievementSubject with a
  pseudonymous unhashed IdentityObject, Achievement with the witnessed
  count and the honest-scope wording in its criteria narrative) and the
  native `cx-credential/1` payload embedded as `cx:record`.
- **Verify either form.** The verify box reads a pasted native record or
  a JWT and grades both the same four ways — invalid, valid but
  untrusted, trusted by name, revoked — and a native `cx-revocation/1`
  list revokes the envelope because the rid is shared.
- **`tools/verify_record.js`** — a dependency-free Node verifier for
  both forms with `--trust` and `--revocations`; exit codes 0 / 1 / 2.
- **`docs/CREDENTIALS.md`** — the two forms, what a verifier learns and
  does not, the envelope exactly, and the honest limits of a
  third-party round trip.
- Nothing changed in the native path, the threshold, the witnessed
  count on the face of every record, the trust list or revocation.

## [0.59.0] — 2026-09-16

### Added — roadmap wave 2 closed out
- **`docs/HOSTING.md`** — the hardening guide for a district that wants
  a URL: serve the released file unchanged, one origin per app, the same
  Content-Security-Policy as an HTTP header, HSTS, no cookies, no
  analytics, `no-store`; nginx, Apache and Caddy examples; a checking
  procedure. `testHostedCopy` serves the apps over HTTP in the browser
  suite and proves a hosted copy behaves like the file (no request, no
  CSP violation, fetch refused, fonts resolve); `CX_HOSTED_BASE` points
  it at a real host.
- **`sbom/cognitionx.cdx.json`** — a CycloneDX 1.5 software bill of
  materials generated from the build by `tools/sbom.py` and diffed in
  CI: the six apps with hashes, the four embedded typefaces under OFL,
  the build toolchain, the development toolchain marked excluded, and
  zero runtime dependencies declared.
- **`docs/CISA_K12_SUMMARY.md`** — the one-page vendor answer to CISA's
  K–12 cybersecurity recommendations, each mapped to who answers, how,
  and the register control.
- The register: 28 met, 13 partial, 3 open (signed tags, cybersecurity
  training, municipal permits).

## [0.58.0] — 2026-09-16

### Added — roadmap wave 2 in the Louisiana app
- **A durable ledger.** The learner ledger and the assessor queue are kept
  in IndexedDB behind the existing accessors (localStorage stays as the
  compatibility copy every earlier release read); on startup the
  IndexedDB copy is authoritative when it is at least as new, and a
  localStorage-only ledger migrates once. A localStorage quota failure is
  reported on screen, not swallowed, and the ledger written after it
  reloads from IndexedDB. A 400-learner ledger saves and reloads whole.
- **The records-custody bundle.** One dated `cx-custody/1` file — the
  ledger, the Records Office name and public key, trust and revocation
  lists, the readiness and hall checklists — exported from the Records
  Office widget and Parish Admin. Never the private key.
- **The hall safety & compliance checklist.** The thirteen wave-3
  operating controls (device sheet, weekly export, incident lead, DPA,
  records custody, background checks, fire marshal, insurance, OSHA 10,
  youth lines, employment certificates, two-adult rule, MOU), per parish
  in the parish dashboard and Parish Admin, each tagged with its
  register id and exported with the bundle.
- The control register moves two platform controls to *met* and twelve
  adopter controls from *open* to *partial* with the checklist as
  evidence: 25 met, 15 partial, 4 open.

## [0.57.0] — 2026-09-16

### Added — the security and compliance register, the roadmap, and wave one
- **`docs/COMPLIANCE_ROADMAP.md`** — the review of the apps and the
  deployment they imply against state, parish/county, local and district
  security and compliance expectations; findings, eight recommendations,
  a four-wave roadmap with owners and acceptance, and a ten-step
  begin-now checklist for a Louisiana parish pilot. Not legal advice.
- **`data/policy/controls.json` → `docs/CONTROL_REGISTER.md`** — 44
  controls across six levels (platform, federal, state, parish, local,
  district), each with requirement, source, owner, status, evidence and
  next step. `tools/controls_report.py` regenerates the register in CI
  and refuses any evidence reference (test, browser check, CI step,
  document or file) that does not exist.
- **The Records Office private key is non-extractable** (finding 7 of
  the v0.55.0 review, fixed): a WebCrypto key held in IndexedDB that no
  script, extension or export can read and that cannot be copied to
  another machine; a pre-v0.57.0 office migrates once with the same
  public key; *Retire this office* destroys it; page-memory fallback
  where IndexedDB is unavailable, stated on the widget.
- **Release checksums and a security policy** — `tools/checksums.py`
  writes `apps/CHECKSUMS.sha256` in CI; `SECURITY.md` gives the
  reporting channel, response times, the verification step and the
  threat model.
- **Breach notification for all fifty states** — an eleventh domain in
  the compliance layer (statute, outer deadline after discovery,
  regulator notice, the K–12 policy line; every entry flagged verify),
  a *Breach-notification deadline* lens and checklist row in the States
  app, a row in the Louisiana State Admin dashboard, and the report.
- **Youth hazard orders in the studio** — every trades scenario carries
  an *Under 18* line naming the FLSA Hazardous Occupations Orders and
  OSHA rules that keep minors off the live task; the engine shows it in
  the brief; the validator requires it.
- **Adopter templates** — `docs/templates/`: a data-processing
  statement for a district's DPA, an incident-response runbook keyed to
  the state clock, and a records-custody statement for public bodies.

## [0.56.0] — 2026-09-15

### Added — standards mapping and transfer-check rubrics (roadmap step ⑤)
- **`data/standards/lss-k12.json`** — generated by
  `tools/generate_standards.py` from the Louisiana K–12 program: the
  Louisiana Student Standards codes (mathematics, ELA, science) each of
  the 52 K–12 blocks was designed against, 299 citations, block scope,
  strength *cites*. CI regenerates and diffs it.
- **`data/standards/ngss-ets-robotics.json`** — authored: the NGSS
  Engineering Design performance expectations (K-2 / 3-5 / MS / HS
  ETS1) that four Robotics OS tracks practise at each band, 20 entries
  with a one-line *why* each, track-band scope, strength *touches*.
- **`data/rubrics/core_spine.json`** — 30 transfer-check rubrics, one
  per core-spine track the Louisiana ledger credits: three pass-evidence
  lines, three common failure modes, an assessor note. The theme-level
  specific stays the block's own transfer check.
- **Where they appear.** Louisiana Assessor Mode shows the track's
  rubric under the three lines when a request is open, and reports the
  coverage in *The honest witness*. Flow Hub pack detail opens the
  rubric above a track's themes, shows codes as chips per band with the
  framework and caveat on hover, and gives the K–12 rows a *Standards
  (as cited)* column; the printed workbook carries the rubric under the
  track header and the codes in each band's row.
- **`tools/validate_standards.py`** in CI: every block, track and band
  exists, themes and grades match, no empty code, every framework has
  publisher, documents, as-of and a verifying caveat, every rubric is
  complete. `docs/DATA_QUALITY.md` gains a *Standards and rubrics*
  coverage section. `docs/STANDARDS.md` documents the schema, the
  strength words and how to extend.
- Every code names an intended alignment, never a certification of
  one; no framework claims an external alignment review.

## [0.55.0] — 2026-09-15

### Changed — the compliance and regulatory review of the apps
- **No third-party request, ever.** Five apps loaded their typefaces from
  Google Fonts on every open — a request carrying the reader's IP
  address and user agent, contradicting "nothing leaves the page on its
  own" and the offline promise. The latin subsets of the four families
  (Fraunces, Instrument Sans, IBM Plex Mono, Archivo — all SIL Open Font
  License, `data/fonts/`) are now embedded into each build as `data:`
  URIs by the shared runtime (`tools/runtime_lib.py`); no app names a
  font host and the tests forbid it.
- **A browser-enforced no-network policy.** Every app carries a strict
  Content-Security-Policy meta (`default-src 'none'`, `connect-src
  'none'`, no eval, no frames, no objects, no workers). The smoke suite
  proves the browser refuses a fetch from inside each app.
- **No referrer leakage** on outbound links (`referrer: no-referrer`).
- **A Data & privacy notice in every app** (`tools/privacy/notice.js`,
  canonical text `data/policy/privacy.json`): the keys this app has
  written and their size, what stays, what leaves, learners under
  thirteen, rights, security, and *Erase everything this app stored in
  this browser* behind a confirm — a native dialog, keyboard-complete.
- The Louisiana ledger asks for a first name or nickname; the Education
  OS's own network self-review no longer claims a font origin.

### Added
- **`docs/COMPLIANCE_REVIEW.md`** — scope and method, nine findings with
  status, the data map per app, and the posture under FERPA, COPPA,
  state student-privacy law, access/correction/erasure rights, WCAG,
  security, claims about AI, licensing and securities. Not legal advice.
- `tests/test_platform.py` holds the review mechanically (CSP, referrer,
  embedded fonts, the canonical notice, no eval, no font hosts);
  `tests/browser/smoke.js` sweeps every app for CSP violations and
  external requests, checks the fonts resolve, and proves erase-all
  removes this app's keys and nothing else.

## [0.54.0] — 2026-09-15

### Added — the Simulation Studio
- **`data/simulations/scenarios.json`** — a canonical fact base of 18
  branching control-discipline scenarios (126 decision points, 378
  options), each tied to a real track in `data/blocks.csv` and carrying
  that track's witnessed transfer check verbatim so the studio can never
  be mistaken for the check. Nine scenarios take a trades kind and are
  localized by the host to a region's publicly known site; the rest take
  a place anchor. Six disciplines are scored: verify before you act,
  stop-work authority, say it out loud, the order is the safety,
  escalate rather than improvise, the person in front of you. The
  studio law and the run note are carried verbatim.
- **`tools/sim/engine.js`** — one shared engine injected into all six
  apps: deterministic (seeded, no `Math.random`), three difficulties
  (rehearsal, one complication, full drill — complications land at
  seeded positions), no timers, a live region for consequences, a
  debrief with the scenario's three questions, and a portable
  `cx-simrun/1` run record with a next-difficulty recommendation (85%
  up, under 50% down; advice, never a gate). The engine never touches
  the network or storage; the host decides what to keep.
- **Six hosts.** Trades Network: the Simulations view runs any category
  on any region's real site, and every roster card offers its scenario.
  Louisiana: a student widget whose kept runs attach to the learner as
  *practice* — never to progress, evidence or the queue — and a teacher
  widget with the class's runs; the sanitizer carries practice through
  import. Platform: the studio sits between stage 2 and stage 3 of the
  loop, from the demo track's own pack, and adds nothing to the count.
  Flow Hub: a session on a track with a scenario offers the rehearsal,
  and pack detail marks the tracks that carry one. States: the nine
  anchored scenarios run on each state's own water, corridor, table,
  culture and storm memory. Education OS: the canonical library sits
  under the quest simulator, loaded ahead of the app.
- **`tools/validate_simulations.py`** — referential integrity against
  the dataset (pack, track, transfer block and its check text), exactly
  one best option per decision, discipline coverage, the honesty lines —
  run by CI after the dataset validator. `tools/sim_lib.py` is the
  helper every builder shares. `tests/test_platform.py` holds the
  engine's stances (no network, no storage, no randomness, no timers)
  and every app's copy of them; `tests/browser/smoke.js` plays a run to
  the debrief in every host and proves a kept run changes nothing else.
- **`docs/SIMULATION.md`** and the wiki page *Simulation Studio*.

### Changed
- `docs/ROADMAP.md`: the Phase 2 item "Mission simulator: promote from
  demo to configurable engine driven by pack data" is done; the Phase 4
  difficulty model exists in first working form (the studio's
  next-difficulty rule).

## [0.53.2] — 2026-09-15

### Documentation
- **`docs/PITCH_DECK.md`** — the three-page investor deck as canonical
  text: the problem, the solution, the ask — use of proceeds, milestones,
  the round on standard forms, the call to action, the risk paragraph.
  The proof strip (54 releases, 17,450 blocks, 6 apps, 64 parishes, 0
  WCAG-tagged violations, 50 states) is held to the dataset by the tests.
- **`docs/CAPITAL_STRUCTURE.md`** — new section *Recommended terms on
  standard forms*: the YC post-money SAFE (cap only, no discount, no MFN,
  one form per round), AGI Corp as a Delaware C-corp issuer, a cap set
  from a fully diluted model, the pro rata side letter as the only side
  letter, NVCA documents at the priced round, Regulation D 506(b) with
  Form D and blue-sky notices, a written Mission Rights Agreement, the
  reporting cadence, and what not to do. Proposals until counsel has
  papered them; not legal, tax or securities advice.

### Tooling
- **`tools/film/deck3/`** — the three-page deck generator (`gen3.py`
  writes the clickable page, the print edition and the eight-slide video
  edition with its narration), the overflow/overlap measurer and PDF
  exporter (`check3.js`), and the narrate → record → align → mux chain
  (`synth.py`, `rec.js`, `mux.py`). Rendered PDF and MP4 are not committed.

## [0.53.1] — 2026-09-15

### Documentation
- **`docs/INVESTOR_BRIEF.md`** — the AGI Future Foundation PBC investor
  brief: mission and structure, the investment thesis, the twelve-module
  training portfolio and launch sequence, the Robotics.X layers and
  hardware strategy, the $5.0M ask with allocation and milestones,
  standards and governance requirements, the diligence package, the
  claims to avoid — and a closing section, **What the repository proves
  today**, that lists claim by claim what the code already backs (the
  loop, signed credentials, the audit, the compliance layer, the honesty
  stances) and what the brief promises that is not yet built (model-backed
  coaching, SCORM/xAPI/LTI, immersive simulation, Robotics.X as a product,
  SOC 2, revenue).
- **`docs/CAPITAL_STRUCTURE.md`** — capital structure, governance and
  risk: separated capital pools by entity, the ownership architecture,
  narrow mission-protection rights, instruments by stage, the full risk
  register framed as disciplined governance, investor protections,
  cap-table guidance, use-of-proceeds controls and reporting cadence —
  with a note on where Cognition.X sits (the education line; evidence,
  not revenue; open source by design).
- Both are published together as one designed data-room page; the
  Markdown is canonical. Neither is legal, tax or securities advice.

## [0.53.0] — 2026-09-15

The accessibility audit — prompt 4 of the ranked next steps.

### Fixed — WCAG 2.2 AA
- axe-core over 45 views of the six apps, light and dark, found 1,182
  colour-contrast nodes, 82 target-size, 16 nested-interactive, 12
  select-name and 4 scrollable-region findings. All fixed at the token or
  component level in the templates: `--faint`, `--gold`, the region
  colours and Flow Hub's accent brought to ≥4.5:1 on every surface;
  gold buttons take ink text in dark themes (`--on-gold`); the States
  compliance tier colours darkened; the Education OS shell overrides the
  app's `#b8860b` id colour; the dashboard reorder buttons meet the 24 px
  target size; tile and city maps are `role="group"`; set-aside buttons
  moved out of `<summary>`; every generated `<select>` carries an
  accessible name; output boxes and scrolling tables are keyboard
  focusable. Result: **0 WCAG-tagged violations**; keyboard sweep 4,849
  focusable elements, 0 unnamed, 0 click-only.
- `docs/ACCESSIBILITY.md` records the method, the findings, the fixes,
  and what remains (heading-order as a documented best-practice
  deviation, axe “needs review” items, non-default styles, the missing
  human screen-reader pass); `docs/ACCESSIBILITY.json` is the committed
  result and `tests/test_platform.py` fails if it ever carries a
  WCAG-tagged violation.

## [0.52.0] — 2026-09-15

The credential-naming correction — prompt 2 of the ranked next steps.

### Changed — dataset (proposed to the review board, not yet adopted)
- **Twenty-four credential names** for the tracks the v0.1.0 import left
  named with the bare level word “Practitioner” (1,228 rows, 7% of the
  dataset): *Household Keeper*, *Home Budget Keeper*, *Working Life
  Navigator*, *Everyday Navigator*, *First-Minutes Responder*; *Infant
  Care Companion*, *Childhood Companion*, *Adult Life Steward*, *Elder
  Care Companion*, *Family Carer*; *Workshop Maker*, *Everyday Repairer*,
  *Reuse Steward*, *Workshop Hand*, *Trade Pathfinder*; *Oral Health Peer*
  (the split track unified), *Sight and Hearing Peer*, *Food and Water
  Peer*, *Recovery Peer*; *Water Reader*, *Land Reader*, *Local Climate
  Reader*, *Home Energy Reader*, *Resilience Planner*. A person and a
  capability; never a level word; never a job title the credential
  cannot confer.
- Applied **through the pipeline**: each track in `data/promotions/*.json`
  carries a `credential` and a `credential_correction` note;
  `tools/normalize_blocks.py` replaces a bare level word with it as the
  one deliberate, counted exception to fill-empty-only (“corrected 1,195
  level-word credentials”, printed on every run). Real names are never
  overwritten; no `block_id` changed. 33 trackless rows in the Empathy &
  Emotional Intelligence (EW) group remain and are documented.
- Ratchets in `tests/test_platform.py`: 1,228 → **33 rows**, 24 → **0
  tracks**, 1 → **0 split tracks**. `docs/DATA_REVIEW.md` Finding 6
  rewritten with the table of names and the board's decision;
  `docs/DATA_QUALITY.md` regenerated (0% level-word credentials in every
  pack; 1,431 distinct credential strings).

### Added — tooling
- **`tools/a11y/audit.js`** — the accessibility audit runner for prompt 4:
  axe-core (WCAG 2.2 A/AA + best-practice rules) over every route of every
  app, in-app view switches included, plus a keyboard sweep (focusable
  count, unnamed controls, click-only elements); writes
  `docs/ACCESSIBILITY.json`. The audit itself ships next.

## [0.51.0] — 2026-09-15

The compliance layer. What each of the fifty states asks of a program
office that deploys Cognition.X — the forms, applications, agencies and
fees — as a checklist with costs, not legal advice.

### Added — data
- **`data/states/compliance.json`** — for every state, ten domains: student
  data privacy (the statute and the agreement a district will ask for —
  SOPIPA-style operator laws in 31 states, the SDPC National Data Privacy
  Agreement where a state alliance exists), homeschool notice and
  assessment (regulation tier and the state's own forms — from Louisiana's
  BESE Home Study application to New York's IHIP and quarterly reports),
  foreign nonprofit qualification (form, fee, annual report, registered
  agent), charitable-solicitation registration (38 states; the form, the
  initial and renewal fee, thresholds), background checks for adults with
  unsupervised access (statute and per-person cost), mandated reporting
  (universal-reporter states and training rules), apprenticeship
  registration (28 State Apprenticeship Agencies vs. the federal Office of
  Apprenticeship; youth-apprenticeship programs), the state's CTE
  industry-recognized credential list, the digital-accessibility standard
  (plus the 2024 ADA Title II web rule everywhere), and sales-tax exemption
  (form or none). Each state carries a **cost roll-up** (one-time and
  annual, under stated assumptions) and its sources. **Every fee carries
  `asOf` and `verify`**; the file's note says plainly that it is not legal
  advice, that fees and forms change yearly, and that nothing in it claims
  Cognition.X is approved, registered or listed anywhere.
- **`docs/STATE_COMPLIANCE.md`** — generated by `tools/compliance_report.py`
  (a fifty-row table plus the national baseline), regenerated and
  drift-checked in CI like the data-quality dashboard.

### Added — apps
- **States app · Compliance view** (`#/compliance`, `#/compliance/<ST>`):
  summary tiles; the nation as a **lens map** (homeschool tier, charity
  registration, operator law, SAA/OA, sales-tax exemption, universal
  mandated reporting, one-time cost band) with a legend that counts; a
  per-state **checklist** of the ten domains with agency, form, fee,
  as-of year and verify flag, the cost roll-up and its assumptions, and
  where to confirm — exportable as `cxstate-compliance/1` JSON and
  printable; the national baseline; the honesty box. Every state page
  gains a *Compliance in <state> — the short list* panel linking to the
  full checklist; a Guide tour stop.
- **Louisiana · State Admin dashboard** — *Compliance — Louisiana*: the
  state's ten rows and cost tiles from the same file.

### Tests
- `tests/test_platform.py` (+~1,000 checks): fifty states matching the
  fact base, ten domains each, valid tiers and types, sane cost roll-ups,
  every fee flagged verify with the as-of year, the not-legal-advice
  note, and the report's headline matching the data.
- `tests/browser/smoke.js` (+9): the view routes with the state from the
  hash, fifty tiles, ten rows, verify flags, the disclaimer, the lens
  recolors, a tile click opens that state, the state-page panel, the
  Louisiana widget.

## [0.50.1] — 2026-09-15

### Changed
- **A more human narration voice.** `tools/film/tts.py` now fronts the
  film kit's narration: kokoro-onnx by default (the `af_heart` voice;
  `CX_TTS_VOICE` selects another, e.g. `am_michael`, `bm_george`), with
  piper kept as the fallback engine (`CX_TTS=piper`). The five feature
  shorts and the pitch-deck video were re-rendered with it; the deck's
  per-slide synthesis is `tools/film/deck/synth.py`. Still offline, still
  no service — model files live in the git-ignored `tools/film/kokoro/`.

## [0.50.0] — 2026-09-14

The film kit speaks. Narration, five feature shorts for social channels,
and the pitch deck — all rendered from the platform's own apps and an
offline voice; no external service, no credits.

### Added
- **Narration in `tools/film/film.js`** — a scene's `say` text is
  rendered by piper (offline neural TTS) into a clip; the scene is held
  at least as long as the clip, the audio track is assembled from the
  recorded scene start times, and ffmpeg muxes it (loudness-normalised).
  Scenes without `say` record silent, as before.
- **Five narrated feature shorts** (`tools/film/social1.js` … `social5.js`,
  1080p, 72–90 s): *Sixty-four parishes* (Louisiana dashboards, a parish
  plan, its makers, the Network OS); *The Flow Zone* (a Flow Hub session,
  the engine's three answers, dashboard swarms, access modules); *The
  Makers' Hall* (the pathway, the industry stage, makers by parish, the
  kitchen, art and craft, the honesty note); *Proof, not attendance* (the
  runnable loop to a signed, verified, tamper-checked record); *Leadership
  as craft* (the Legacy Institute: principles, the record, the Leadership
  Ladder, the Fellowship pattern, any state, the disclaimer).
- **The pitch deck** (`tools/film/deck/`) — `gen.py` writes a 15-slide
  16:9 HTML deck on the platform's own tokens and faces (keyboard/click
  navigation) plus per-slide narration; `shots.js` captures the real app
  screens the slides embed; `rec.js` records it to the narration timings
  and muxes — a 7-minute narrated pitch video. The opening slide is dataset
  row CX-MUSICIND-0054, unedited; every number is the manifest's.

## [0.49.1] — 2026-09-14

### Documentation
- **`docs/WALKTHROUGH.md`** — the investor walkthrough: the block as the
  unit (one real dataset row, unedited), the manifest, the six-stage
  learning loop, the automated flow system (flow-state engine, 20 access
  modules, 24-agent dashboard swarms, the eight-automation Network OS,
  CX-Trace), Louisiana as the flagship, the Legacy Institute curriculum
  with the Institute's disclaimer verbatim, trades and SmartCiti.X,
  portable records, the fifty-state pattern, engineering integrity, the
  eight stances the platform will not round up, and the v1.0 gate as the
  roadmap states it. A designed edition of the same text is published as
  a page; the Markdown is the canonical copy.

## [0.49.0] — 2026-09-14

The film kit. Two short product films rendered from the platform's own
apps — every frame the software as shipped — plus the production briefs
for the cinematic cuts.

### Added
- **`tools/film/`** — a Playwright + ffmpeg film kit: `film.js` records a
  scene list from the real apps at 1920×1080 (generated kinetic-type
  title cards from `card.js`; injected captions, chapter labels, a
  visible cursor and dissolves; real clicks, selects, typing and
  scrolling on the live dashboards) and encodes H.264. `scenes1.js` is
  *The Flow Zone* (3:04 — the platform model and runnable loop, the
  Education OS, Cognition.X Louisiana as the flagship: tile map,
  parish dashboards, the Network OS, role dashboards and swarms; the
  flipped classroom and honest gamification; a Flow Hub session; the
  Legacy Institute and Leadership Ladder for educators; the States app;
  the Makers' Hall). `scenes2.js` is *Training that proves itself*
  (2:15 — organisation packs, Pack Studio, and SmartCiti.X: the Trades
  Network's city maps, roster, simulations under the studio law, the
  district compact, the Trade Hall Network OS, Assessor Mode and the
  Records Office signing a credential). Renders one film at a time;
  output is git-ignored.
- **`docs/film/PRODUCTION_BRIEFS.md`** — for each film: the narration
  script with timestamps, a shot list with generation prompts for the
  dramatized inserts, and the assembly plan — so a cinematic cut can be
  produced from the product cut without any shot claiming a feature the
  platform does not have. The briefs carry the platform's stances:
  simulation ≠ certification, nothing leaves the page, the Institute
  referenced through its public record with the app's disclaimer, no
  living local practitioner depicted, SmartCiti.X presented as the
  VR/AR training center whose curriculum engine is Cognition.X.

## [0.48.0] — 2026-09-14

The culture trades. Three new trade packs — the music trade end to end,
the professional kitchen, and the art and craft trades — and the
Louisiana app's **Makers' Hall**, where each trade is drawn as a pathway
from creation to industry and taught through the example of makers from
the public record, parish by parish.

### Added — dataset (17,450 blocks · 47 packs · 225 tracks)
- **Music : Creation to Industry** (`CX-MUSICIND`, 250 blocks): *The
  sound: instrument, voice and ear* → *The song: writing and arranging*
  → *The room: live performance* → *The studio: recording and
  production* → *The industry: rights, money and roles* — the whole
  trade, from ear training and the instrument you can afford through
  songwriting, arranging, gigging, the sound and stage crew, recording,
  mixing and mastering, to publishing, PROs, royalties, contracts,
  management, booking, festivals, labels, distribution, sync and the
  nonprofit and teaching roles.
- **Culinary Trades : The Louisiana Kitchen** (`CX-CULINARY`, 250):
  knife, fire and mise en place; the roux and the Louisiana table;
  sourcing, safety and the supply line; front of house and hospitality;
  the business of menu, money and ownership.
- **Arts & Craft Trades : Louisiana Makers** (`CX-ARTCRAFT`, 250):
  seeing and drawing for work; materials (clay, wood, metal, textile,
  paint); the crafts of the state (beadwork, floats, basketry, boats,
  ironwork); showing the work (exhibition and public art); the working
  artist's money, rights and studio.
- **`data/louisiana/makers.json`** — the Makers' Hall fact base: for
  each discipline, five pathway stages mapped one-to-one onto the pack's
  tracks with **154 industry roles** in all; **63 makers from the public
  record** (each with years, parish and place, craft, what they did, the
  lesson a learner can take, and a transfer check to actually do) — from
  Buddy Bolden, Amédé Ardoin and Lead Belly to Cosimo Matassa, Harold
  Battiste and Boozoo Chavis's contract; from Lena Richard, Leah Chase
  and Paul Prudhomme's roux chart to Ella Brennan's dining room and Al
  Copeland's balance sheet; from Clementine Hunter, Tootie Montana and
  Ada Thomas to Blaine Kern's float shop and John T. Scott's public
  works — spread so that every one of the eight regions has at least
  one; and **42 organisations** (NOCCA, the Ellis Marsalis Center,
  Tipitina's Foundation, the John Folse Culinary Institute, NOCHI, Café
  Reconcile, the Chitimacha cultural department, the Folklife Center…)
  by parish. The file's `note` states the stance: public record only,
  naming is not endorsement, living people only through what is already
  public, working local practitioners left for the parish to name.
- The Musicians (AFM), Culinary & hospitality workers (UNITE HERE) and
  Stagehands & exhibition workers (IATSE) union families now back the
  three packs — no new families; still 222 regional entries.

### Added — Louisiana app
- **The Makers' Hall view** (`#/makers`): discipline chips; an SVG
  **pathway map** whose five stage nodes are keyboard-operable buttons
  (click or Enter filters roles, tracks and makers to that stage; again
  clears); the role ladder grouped by stage; the pack's tracks with Flow
  Hub deep links (`#track=CULINARY/KN`); the Makers' Hall of figure
  cards with the check under a disclosure, filterable by parish or
  region (`#/makers/<discipline>/<parish-slug>` deep-links both); the
  organisations by parish; and the honesty box. A Guide tour stop.
- **Parish dashboards** — *Makers from this parish*: the parish's own
  figures across the three trades, or its region's with the plain
  statement that none is listed for the parish yet and that it names
  its own. The build-time rules engine adds a culture-trade pack to a
  parish's module plan when its makers worked that discipline (reason
  shown: "2 music makers on the public record"), and the industry rules
  now map hospitality/food phrases to the culinary pack and
  film/music/festival/arts phrases to the music and arts packs.
- **Role dashboards** — *A maker from your parish* on the Student,
  Teacher, Parent and Homeschool dashboards: one maker at a time from
  the parish, then the region, then the state, rotating daily and on
  demand (*Another maker*), with the transfer check and a link into the
  hall.

### Tests
- `tests/test_platform.py` (+~230 checks): each culture pack is 250
  blocks / five tracks / no level-word credentials; the union links; and
  the makers fact base — the note's two stance sentences, every figure's
  fields non-empty, every parish a real parish, every stage on its
  pathway, every stage a real track, no name twice, every region
  covered.
- `tests/browser/smoke.js` (+17 assertions): the view routes and
  renders three disciplines, five stages, five tracks, the honesty note;
  stage click and keyboard Enter filter and clear; the parish filter and
  the deep link; culinary Flow Hub links; St. Landry's makers and the
  pack they earn; Winn's honest fallback; the student widget renders and
  rotates.

### Documentation
- README packs-at-a-glance, wiki Home / Packs / Louisiana Platform /
  Trades Network / Versioning, ROADMAP status, SYSTEM_REVIEW numbers,
  and a DATA_REVIEW stance section on named people.

## [0.47.0] — 2026-09-11

The adversarial multi-agent review of v0.44.0 finished: 116 agents, 36
findings, each put to three independent refuters — **24 confirmed, 12
refuted**. This release closes the confirmed ones.

### Fixed — correctness
- **The Student standing panel went dead as soon as a witnessed check was
  waiting.** `el.innerHTML +=` ran *after* four listeners were bound,
  re-parsing the panel and discarding the nodes they were attached to; the
  learner picker, Add learner, Record a practice check and Request a
  witnessed check all stopped working, silently, until an assessor cleared
  the queue. The waiting note is now part of the single write that happens
  before binding.
- **A refused save looked like a saved one.** `store()` swallowed every
  localStorage failure, so trust-list imports, revocations and ledger
  credits reported success while persisting nothing. A refusal now says so
  once, plainly, in an alert the page cannot hide.
- **Every re-render stole the control you were using.** `saveR()` rebuilds
  the whole dashboard, and the Network OS (20s) and swarm (10s) pulses
  replace their boards wholesale. Focus and caret are now restored by
  element id, and a pulse skips any board the user is currently inside.
- **Flow Hub's Pack Studio could never be submitted**: the *Pack name* and
  *Notes* fields carried no `data-ps` attribute, so `psBind()` never bound
  them and the validator rejected every hand-authored pack for a missing
  name.
- **Every cross-app "open in Flow Hub" chip landed nowhere.** The deep-link
  regex required `SLUG/PREFIX`; the Trades Network and States apps emit a
  bare slug. Both forms now work.
- **The Parent swarm described a different child** than the panels beside
  it — it read the Student's `R.me` while every Parent widget reads
  `R.child`.
- A pasted Flow Hub ledger with a non-object `done` made the next completed
  check throw and silently drop the save; the shape is checked first.

### Fixed — honesty
- **A signed credential asserted witnessing it could not see.** Practice
  checks and witnessed checks credit the same counter, yet every
  `cx-credential/1` payload read *"witnessed per the pack's checks"* — and
  the Records Office would sign that over a randomly-seeded demo learner.
  The payload now carries the **witnessed count the evidence log actually
  supports**, marks demo learners `demo: true` on their face, and says
  plainly how much of the 50 is the learner's own practice log. A signature
  over a false claim is worse than no signature.
- The Platform app's headline tile read **"0 network calls in any app"**
  while that very page loads a Google Fonts stylesheet. It now reads
  *"0 data calls — fonts only"*.
- `tools/evidence_triage.py` documented an **UNUSED** category `main()`
  never computed. It is now computed against the dataset and renamed
  **UNREPORTED**, with the distinction stated: no submitting site reported
  activity is not the same as nobody used it.
- The Packs wiki still said classroom hooks feed "all 111 roster entries";
  the fact base has had 222 since v0.30.0.

### Fixed — the pipeline
- **CI never re-derived 60% of the dataset.** 9,950 of 16,700 blocks are
  generated from `data/pack_specs/`, and every fact base is extracted from
  the Education OS app, but CI checked neither — both were committed
  artifacts nothing verified. The `dataset` job now regenerates **every
  pack from its spec** and **re-extracts every fact base**, failing on any
  drift. (All 19 specs were confirmed to reproduce their CSVs
  byte-identically before the gate was added.)
- **A slug collision would have merged two packs silently.** `slug_for`'s
  acronym fallback can map two pack names to one slug; `block_id`s stay
  unique so every validator passes, while all four slug-keyed builders
  quietly treat the two packs as one. A collision is now a build error
  naming both packs.
- **The validator checked half the shape it documents.** "10 themes × 5
  bands" was enforced as "50 rows and 10 themes", so a track could pass
  with one band taught twice and another missing. Band coverage is now
  verified per theme, and an unknown grade band is an error rather than a
  silently skipped level check. All 210 tracks pass the stricter rule.

### Fixed — accessibility
- The **Assessor queue header** was a click-only `<div>`: a keyboard or
  screen-reader assessor could never open any request but the first. It is
  now a real control with `role`, `tabindex`, `aria-expanded` and Enter/Space.
- **Trades Network pack chips** were mouse-only `<span>`s; they now carry
  `role="link"`, `tabindex` and key handling.
- The **Records Office verdict** is announced (`role="status"`,
  `aria-live`) — a screen-reader user pressing Verify previously got
  nothing at all.

### Security
- **Imported ledgers are validated, not trusted.** Learner and queue ids
  reach HTML attributes and object keys; a pasted ledger is third-party
  data. Ids are now constrained to a safe alphabet, names/bands/progress
  coerced to the expected shape, unknown track keys dropped, and queue rows
  referencing unknown learners discarded — plus `esc()` on every id that
  reaches an attribute.

### Verified
126 Python invariants and **72 browser assertions**, twelve of them new
regressions written directly against these fixes: the standing panel stays
live after a request, a hostile imported id is neutralised, a signed record
states its witnessed basis, a demo record says so, the assessor queue opens
by keyboard, and a bare-slug deep link resolves.

## [0.46.0] — 2026-09-11

### Added
- **The Education OS has a design system again.** v0.45.0 made the app
  *run*; this makes it *readable*. The v0.1.0 import lost the
  stylesheet along with the shell, so every view rendered as unstyled
  markup. The stylesheet is now generated by
  `tools/build_education_os.py` — and it is **recovered, not invented**:
  - **Tokens from the app's own record.** The gold, teal, ink and field
    values are the ones the application documents in its own brand view
    (“Gold — first contact” `#B8871F`, “Teal — application” `#1E7A72`,
    “Ink — the keystone” `#0E1E2E`, Field `#FFFFFF` / `#122536` dark);
    the status and rail colours come from its own `DATA.vizTok`
    fallbacks (`--warn #96530A`, `--crit #B22B2B`, `--ok #1F7A4D`,
    `--ink3 #556572`, `--line #DFE5EA`, `--line2 #C9D3D9`). Only the
    tones *between* documented anchors (`--ink2`, `--bg3`) are derived.
  - **Nothing is redefined that survived.** The app injects 16 KB of its
    own CSS at runtime (the figure lockup, the scale strip, the command
    palette, brand marks, rubric boards). Its `--seq1…5`, `--seq-ink`,
    `--seq-wash`, `--gold-ink` and `--mark-line` definitions are left
    untouched; the new stylesheet supplies only the ~35 base classes
    that were missing.
  - **The app's own rule is honoured**: *never decorated — flat ground
    or its own field, no gradients, no decorative shadow.*
  - Full light and dark themes on all three paths the platform uses
    (`:root`, `prefers-color-scheme`, explicit `data-theme`), plus
    reduced-motion and print rules.
- **Contrast verified numerically, not by eye.** Every text token clears
  **4.5:1** on every ground in both themes. Two failures were found and
  fixed: `--gold2` was being used as text at 2.8–3.3:1 (the app's own
  brand note says the darker `--gold-ink` is the text gold — now it is),
  and teal on `--bg3` sat at 4.48:1 (`--bg3` lightened to `#EEF3F6`,
  which lifts every accent above the line).
- `tests/test_platform.py` gains a design-system guard: every class the
  renderers emit must have a rule, every token they reference inline
  must be defined, and both dark-theme paths plus reduced motion must be
  present — 126 checks in all.

### Verified
Boot is clean in light and dark (zero page errors in both). A
representative sweep — every sixth view, 25 of 149 — found zero
renderer errors, zero empty views and zero horizontal overflow; a full
149-view sweep did not complete in this environment, where each view
renders thousands of blocks, so the sampled result is what is claimed
here and the exhaustive sweep remains open work. Both committed suites
pass: 126 Python invariants and 60 browser assertions.

## [0.45.0] — 2026-09-11

### Fixed
- **The Education OS runs.** The flagship app had never rendered. The
  v0.1.0 import captured its JavaScript — 149 view definitions and 143
  renderers, ~8 MB — but neither its HTML shell nor its stylesheet, so
  it threw on boot at `buildNav()` (no `#nav`), had no `.view` element
  for `route()` to activate, and printed a stray unwrapped
  `var DATA = {…}` block as visible page text. No version in the
  repository, including the v0.1.0 archive, ever contained the shell.
  `tools/build_education_os.py` now **generates the shell from the
  app's own `VIEWS` array** — nav, crumb, edition picker, toast, and one
  container per view — replacing the vestigial stub page and closing the
  document. The app boots with zero errors and renders its views. Its
  imported visual design is still missing; the generated shell carries
  only the layout rules the app's own code requires (see prompt 1 of
  `docs/NEXT_STEPS_OPUS5.md`).

### Added
- **Committed tests — the standing rules, enforced.** Every release
  since v0.22.0 was verified by throwaway scripts that never entered the
  repository; CI could prove the apps *rebuilt*, never that they
  *worked*.
  - `tests/test_platform.py` — 121 checks, Python 3 only, no browser and
    no packages, wired into the CI `apps` job: build integrity, no
    network call syntax in any app (distinguishing calls from the
    Education OS's own security-audit prose), no undocumented external
    hosts, `block_id` uniqueness and shape, manifest agreement, the
    50-block track shape, the honesty stances (no union local numbers,
    profiles never diagnoses, the WLB disclaimer verbatim, simulation
    ≠ certification), the 50-check threshold, the consent gate, and the
    generated Education OS shell.
  - `tests/browser/smoke.js` — 60 assertions over the working models:
    the credential firing at exactly 50 and never twice, genuine ECDSA
    signing with the private half never leaving, all four verification
    grades including a rejected forged revocation list, the consent gate
    and a name-free export, the flow state machine's four transitions,
    swarm arbitration, Network OS drill-downs, the Platform loop end to
    end, and the Education OS booting.
- **`docs/NEXT_STEPS_OPUS5.md`** — ten ranked, self-contained briefs for
  the next sessions, each with its evidence, files, acceptance criteria
  and verification commands.

### Changed
- **Credential-naming defect documented and pinned.** 1,228 rows — 7% of
  the dataset, 24 tracks across five community packs — name their
  credential with the bare band level “Practitioner”; the headline
  “1,394 credentials” counts it as one, leaving 1,393 real. Found by the
  new suite, traced to the v0.1.0 source import, and correct behaviour
  by the pipeline (non-empty source fields are never overwritten).
  Authoring 24 names is review-board work, so instead:
  `docs/DATA_REVIEW.md` gains Finding 6 with full scope,
  `docs/DATA_QUALITY.md` gains a per-pack *Level-word cred %* column and
  a Credential-naming section, and `tests/test_platform.py` pins the
  scope as a ratchet — it can only shrink, and no pack outside the
  legacy import may ever contain one.
- **Documentation corrected against the code**: the OS editions are
  1,120–1,160 blocks each (8,040 in all), not “500 blocks each”; the
  roadmap status block was frozen at v0.32.0 and listed shipped work as
  open; `SYSTEM_REVIEW.md` §2 was titled “the six apps” while listing
  five (Platform added) and described the Education OS as having “one
  pre-existing page error” when it had no shell at all; the Louisiana
  wiki said six roles and 30 widgets (seven and 52) and “~42 KB” for a
  410 KB app; the Trades Network guide still told users “one hundred and
  eleven entries” when it renders 222; `build_trades.py`'s docstring
  still claimed 3 regions and 111 entries.

## [0.44.0] — 2026-09-11

### Added
- **The Louisiana K–12 program, canonical** — the last named layer of
  the app-pipeline roadmap item: `data/louisiana/k12_program.json`
  (via the same deterministic extractor) carries the thirteen grade
  rows — each with an age-appropriate role inside a narrative world
  and six threads (literacy, numeracy, science, computer science,
  safety, assessment) citing Louisiana LDOE standard codes — plus
  the eight policy threads (Act 108 science-of-reading training, the
  Act 422 grade-3 gate, and the rest) the design is built around.
  The Louisiana **Curriculum view** renders it grade by grade with a
  grade picker, carrying the caveat verbatim: a design mapped
  against public LDOE documents — verify each code against the
  current documents before classroom use.
- **The data-quality dashboard, generated in CI** — the roadmap's
  Phase 1 item: `tools/data_quality.py` writes
  `docs/DATA_QUALITY.md`, a per-pack completeness table (blocks,
  tracks, description %, band-suffix %, code+level %, shortest
  transfer check) with the known content debt counted, not hidden
  (the irregular foundation packs' unauthored descriptions and the
  generated packs' band-suffix duplicates both show plainly). The
  CI `dataset` job regenerates it on every push and fails on drift,
  the same pattern as the dataset and the apps.

## [0.43.0] — 2026-09-11

### Added
- **The Leadership Ladder — the Willie L. Brown Jr. Institute
  program, canonical and visible.** The Institute's full leadership
  curriculum, which lived only inside the Education OS app, is now
  canonical dataset content and a first-class program surface:
  - `data/wlb/institute.json` gains the complete program (extracted
    by the same deterministic tool): **5 strands** (Public Service &
    Civic Leadership, Democracy Law & Rights, Economic Development &
    Opportunity, Community Health & Wellbeing, Equity Inclusion &
    Access) × **5 eras** (K–2 → 11–12) × **125 courses**, the
    **ten-module method** every course runs on, the **8 public
    bridge milestones**, per-era standards (the original California
    mapping, labeled as such), the **5-part graduation seal**, the
    junior placement ladder, and the Fellowship pattern.
  - **Louisiana Institute view** gains the Leadership Ladder: a
    strand picker over the era-by-era course table with the
    standards column, the ten-module method, the bridge & seal, the
    junior placement ladder and the Fellowship pattern — with the
    Institute disclaimer carried verbatim, course titles keeping
    their original San Francisco ground, and every edition
    localizing through the existing slots.
  - **States app Institute view** gains the ladder headline (strand
    cards, era arc, counts, the seal) linking to the full ladder.
  - Verified headlessly: 5 strand options, 5 era rows × 25 course
    chips per strand, 10 modules, 8 bridge rows, 5 seal items,
    disclaimer verbatim, zero page errors in both apps.

## [0.42.0] — 2026-09-11

### Added
- **Dashboard agent swarms** (Louisiana, all seven role dashboards):
  every perspective now opens with its own crew of agents on a
  shared blackboard — 24 agents in all — each computing a **priority
  (0–100) and a concrete call from the browser's real state** (the
  ledger, the flow engine, the witness queue, the readiness boards,
  the budgets, the missions), with priority arbitration surfacing
  **one call as the swarm's**, spoken on demand by the voice model.
  Everything stays inspectable: each agent's own call, its priority
  and what it watches are always listed under the arbitrated call —
  *agents propose; the person disposes*.
  - Student: Coach, Motivator, Pathfinder, Credential Watch, Access
    Ally. Teacher: Class Keeper, Triage, Relief, Witness Router.
    Assessor: Queue Agent, Format Agent (serves the next learner's
    chosen check formats), Evidence Scribe. Parent: Home Coach,
    Family Watch, Break Keeper. Homeschool: Co-op Planner, Witness
    Router, Pace Setter. Parish Admin: Readiness, Records, Budget,
    Mission agents. State Admin: Rollout, Evidence, Network agents.
  - Recomputed on a 10-second pulse while the view is open; a
    default-on widget, toggleable and orderable like any other.
  - Verified headlessly against seeded state: arbitration correct
    (a break-due call at priority 95 out-ranks a 49/50 credential
    watch at 90), every role's crew renders its granular rows, the
    pulse re-render is stable, the widget toggles off cleanly, zero
    page errors.

## [0.41.0] — 2026-09-11

### Added
- **Reproducible build from the repository, guaranteed in CI.**
  Verified first by hand: a fresh `git clone` of the GitHub
  repository plus Python 3 regenerates the entire platform —
  `normalize_blocks.py` reproduces the dataset with no diff,
  `validate_blocks.py` passes, and all six app builders reproduce
  every committed `index.html` **byte-for-byte** (no node, no
  package installs, no network beyond the clone). Then locked in:
  the `validate` workflow gains an **`apps` job** that rebuilds all
  six apps from their sources on every push and pull request and
  fails on any drift — mechanically enforcing the two standing
  rules that build products are never hand-edited and that apps are
  always current with their dataset, templates and fact bases.

## [0.40.0] — 2026-09-10

### Changed
- **Granular Network OS** — a deep, granular update of each of the
  eight section automations (Louisiana, Regions view). Every section
  row now expands into its own drill-down board
  (keyboard-operable, `aria-expanded`, state kept across the
  20-second pulse), showing three things no section showed before:
  - **Its live thresholds, stated exactly** — the flow-state cut
    lines, each profile's own break cadence, the 34%/15% and 6/3
    teacher-relief trip points, the never-overridden 50-check
    credential line, the five readiness requirements.
  - **The exact rows it computed from**: Flow Keeper lists every
    learner's channel position with the last-3 sum; Break Caller
    every learner's moves-since-break against their own cadence
    ("due now" flagged); Step Tuner the pending step-down and
    stretch calls by name; Credential Clerk each near-credential
    learner with track and count (49/50 · 1 to go); Cohort Watch
    the full uncapped alert list (the dashboard widget still caps
    at 8); Readiness Sentinel each preparing parish's n/5 with its
    *next missing requirement named*; Teacher Relief its actual
    inputs (class size, load %, open alerts → state → relief);
    Network Sync all eight halls' live counts (parishes, Wave-1
    cohort, browser-local readiness and mission rungs).
  - **A per-section pulse log** of recent distinct calls.
  - Verified headlessly: all eight drill-downs render the expected
    granular rows from a seeded cohort (including a crafted 49/50,
    break-due learner and a 3/5 parish), all eight stay open through
    a pulse re-render, collapse works, zero page errors.

## [0.39.0] — 2026-09-10

### Changed
- **Education OS pipeline, stage two — canonical fact bases.** The
  Louisiana region/parish fact base and the Willie L. Brown Jr.
  Institute fact base, which downstream builders extracted at build
  time by evaluating JS literals inside
  `apps/education-os/template.html`, are now canonical repository
  data:
  - `data/louisiana/fact_base.json` — 9 regions, region hubs, all 64
    parish rows (name, region, seat, population, proposed wave,
    districts, industries, narrative world, rural tier), with the
    provenance note that the adopted two-wave plan is computed at
    build time.
  - `data/wlb/institute.json` — org, mission, quote, record, the
    disclaimer (carried verbatim), and the 12 principles with source
    attributions.
  - `tools/extract_fact_bases.py` performed the one-time extraction
    and remains as the documented, deterministic re-extraction path
    should the app's own copy ever be edited.
  - `tools/build_louisiana.py` and `tools/build_states.py` now read
    the canonical files — no builder except the Education OS's own
    evaluates the app template anymore. **Round-trip proven**: with
    the same version, both apps rebuild byte-identical to the
    app-extracted builds; re-running the extractor reproduces the
    canonical files byte-for-byte. (Shrinking the Education OS
    template itself by injecting these layers back is the remaining
    stage of this roadmap item.)

## [0.38.0] — 2026-09-10

### Added
- **Federation v2** (Louisiana Records Office) — the roadmap's named
  remaining federation work:
  - **Record ids & dataset versions**: every newly issued
    cx-credential/1 payload carries a unique `rid` and the dataset
    version it was issued under (`"Cognition.X v0.38.0"`) — additive,
    so v1 records still verify.
  - **Portable trust-list exchange** — `cx-trustlist/1`: export this
    browser's trusted offices as one file; import another hall's.
    Imported entries are stored and displayed as **second-hand**
    ("via X's list — confirm out-of-band"), preserving the rule that
    trust is granted after out-of-band identity confirmation;
    malformed or private-key-bearing entries are skipped.
  - **Revocation** — `cx-revocation/1`: an office revokes a record it
    issued by its `rid` (with a reason shown to verifiers) and
    exports the revocation list **signed with the same key its
    records carry**. Importing verifies the list's signature first —
    an altered or unsigned list is rejected — and replaces any
    earlier list from the same key. Verification gains a fourth
    outcome, **⊘ Revoked by issuing office**, which trumps trust;
    other records from the same office are unaffected. No network:
    lists travel the same out-of-band channel as the keys.
  - Verified headlessly end to end: trust-list round-trip (export →
    cleared registry → import → still verifies by name, now marked
    second-hand), tampered revocation list rejected, revoked grade
    with reason, fresh records unaffected, tamper detection intact,
    everything persists across reload, zero page errors.

## [0.37.0] — 2026-09-10

### Added
- **Cognition.X Platform — the working model** (`apps/platform/`, built
  by the new `tools/build_platform.py`): a single-file capstone app
  that models the whole platform as one system, in four views:
  - **The Model**: live totals from the manifest and a clickable
    ten-node system map — dataset → pipeline → six apps → the working
    models (ledger, flow engine, assessor loop, records office) →
    Network OS → the evidence loop arcing back, dashed, through the
    review board to the dataset ("through people, never
    automatically"). Every node explains what it is and how it is
    verified.
  - **Run the Loop**: the complete learning loop executed in-page
    with the platform's **real mechanics on labeled demo data** —
    six gated stages: enroll a demo learner (seeded at 47/50 on a
    genuine Louisiana OS track), a live flow session on the real
    state machine (overload → shrink, cruise → stretch, the 8-move
    break cadence), witnessed checks where three assessor
    confirmations reach the real 50-check threshold and the
    credential fires only at exactly 50 (not-yet debriefs credit
    nothing), a genuinely signed cx-credential/1 record via the
    browser's own WebCrypto (ECDSA P-256, public key only), the
    three-grade verification (tampered copy ✗, valid-untrusted △,
    trusted-by-name ✓), and the closing cx-evidence/1 aggregate.
    The run lives only in page memory; reset restores a fresh run.
  - **The Apps**: doors into all six apps by relative link.
  - **The Stack**: the full regeneration command list, the eight
    honesty stances in one place, and the documentation record.
  - Verified headlessly end to end: stage gates hold in sequence,
    the credential is absent at 49 and fires at 50, the signature is
    a real 88-character P-256 signature with no private key in the
    record, tamper detection and trust-by-name behave, the evidence
    aggregate carries counts and no names, and the page loads with
    zero errors.

## [0.36.0] — 2026-09-10

### Added
- **The Evidence Loop v1** — the roadmap's last Phase 3 build item,
  consent-first end to end:
  - **Opt-in aggregate export** (Louisiana State Admin): a live
    preview and export of **cx-evidence/1** JSON — per-track counts
    only (checks recorded, witnessed confirmed / not-yet, learners
    as a count), no names, no ids, no per-learner rows. The export
    button stays disabled until the consent box is checked, nothing
    is ever transmitted by the page (the export box is the only
    exit), and the consent object says so in the file itself.
  - **`tools/evidence_triage.py`**: merges collected evidence files
    into a review-board report — tracks with a high witnessed
    not-yet rate (≥40% over ≥5 attempts) are flagged as revision
    priorities ("the check may be mis-pitched, or the theme
    under-taught"), with the explicit rule *evidence proposes; the
    board disposes* — a supersession or teaching note, never an
    automatic edit. A clearly-labeled synthetic sample under
    `data/evidence/` demonstrates the tool.
  - Governance gains the evidence-informed-priorities section; the
    roadmap gains the **path-to-v1.0 operational checklist** (seat
    the board → recruit a named cohort → exchange office keys →
    collect evidence through one full track → cut v1.0).
  - Verified end to end: the consent gate holds, aggregates are
    correct (summed across learners), the export contains zero
    learner names, and the real exported file round-trips through
    the triage tool.

## [0.35.0] — 2026-09-10

### Added
- **Pack Studio — educator authoring** (Flow Hub's new *Author*
  view): a form-driven pack-spec editor — pack name and stance
  notes, tracks with name / 2–3-letter prefix / credential, ten
  themes each with description and a transfer check on real
  material — with live validation mirroring the generator's rules
  (empty fields, duplicate themes, reused prefixes), a live block
  count, a worked example, import-to-edit, browser-local drafts,
  and a **Validate & export** step whose output was verified to
  round-trip through `tools/generate_pack.py` unchanged. Submission
  instructions are built in; honest scope stated: the offline file
  exports the spec — GitHub and the review board carry it from
  there.
- **Governance** (`docs/GOVERNANCE.md`): the curriculum review board
  — composition, the six-point checklist (accuracy, real transfer
  checks, honesty stances intact, respectful terminology,
  shape/provenance, access), the acceptance flow (CI + two board
  approvals), the supersede-never-rewrite breaking-change policy,
  and the standing review queue over the ~9,950 machine-authored
  blocks with its priority order.

## [0.34.0] — 2026-09-10

### Added
- **Federation v1 — trusted offices** (Louisiana Records Office):
  each hall publishes its `{recordsOffice, publicKey}` export;
  another instance adds it to its browser-local **trusted-offices
  registry** after confirming identity out-of-band, once. Verify now
  grades every record three ways: **✗ invalid** (altered or
  mismatched signature), **△ signature valid, key not trusted**
  (unaltered, holder-signed, identity unconfirmed — the v0.29 honest
  gap, now surfaced explicitly), and **✓ signed by trusted office
  "X"** by name. Trusted keys are listed, removable, persisted, and
  stored public-half only.
- **PWA install metadata** in all four interactive apps: a runtime
  blob web-app manifest (name, standalone display, SVG letter-mark
  icon, theme color) plus theme-color and Apple metas, injected at
  load with nothing fetched. Honest scope: installability depends on
  the browser and https serving — the single offline file remains
  the primary packaging.
- Roadmap: the packaging line is closed (workbooks + install
  metadata) and the federation line carries its first slice; the
  remaining federation work (pack-version publishing, trust-list
  exchange, revocation) is named.

## [0.33.0] — 2026-09-10

### Added
- **Complete system review** (`docs/SYSTEM_REVIEW.md`): an honest
  engineering assessment of the platform at v0.32.0 — the dataset and
  pipeline, the six apps, the working models (ledger, flow engine,
  access profiles, assessor loop, credential ledger, Network OS),
  the verification methodology, and the named gaps and risks
  (browser-local state, machine-authored packs awaiting the review
  board, the Education OS baseline error, accessibility). The
  no-network claim was re-verified by auditing every template: zero
  fetch/XHR/WebSocket/beacon code paths; the fonts stylesheet is the
  only external reference, and every app degrades without it.
- **Data review addendum** (`docs/DATA_REVIEW.md`): current-state
  status over the original import findings — backfills complete,
  the foundation library as the standing content debt, and the fact
  bases documented as reviewed content.
- **Roadmap restructured**: a status-at-v0.32.0 summary and a
  recommended order for the remaining work (a11y audit → PWA →
  federation → educator authoring → governance → evidence loop →
  the v1.0 external-cohort gate).
- **Accessibility first pass** (all four interactive apps): skip-to-
  content links (first tab stop, focusing the `main` landmark),
  `document.documentElement.lang = "en"`, a `prefers-reduced-motion`
  guard disabling animations/transitions/smooth scroll, descriptive
  `aria-label`s on icon-only buttons (roster remove, +1 crediting,
  widget reorder arrows), and `aria-live="polite"` on the Flow Hub
  tutor strip. Marked honestly as a first pass — the full WCAG 2.2
  AA audit remains the roadmap's next recommended step.

## [0.32.0] — 2026-09-10

### Added
- **Assessor Mode** (Louisiana) — the seventh role dashboard, closing
  the witnessed-check loop: students send *Request a witnessed check*
  from My standing (self-recorded checks are reframed as the
  practice log; the witnessed record is what the Records Office
  signs), and assessors work **the transfer-check queue** oldest
  first — each request showing the learner's access-profile check
  format, the three-line rubric (*real material · independent at
  band · would transfer*), and an evidence form. **Confirmed**
  credits the ledger (auto-awarding the credential at 50, spoken
  when voice is on); **Not yet** records an honest debrief and no
  credit — a retry costs an attempt, never a record. Duplicate
  requests are blocked; a recent-evidence log and an honest-witness
  rubric widget round out the dashboard. (Roadmap assessor-mode line
  checked.)
- **Printable per-track workbooks** (Flow Hub): a 🖨 Workbook button
  on every tracked track prints a clean paper workbook — the ten
  themes with descriptions and transfer checks, each with five
  band-level witness/date sign-off lines — through the browser's
  print dialog, for zero-device settings. (The packaging roadmap
  line's workbook half is done; PWA install remains open.)

## [0.31.0] — 2026-09-10

### Added
- **Custom curriculum for all 50 states.** Three pieces:
  - **Cognition.X : States OS** (`STATEOS`, 250 blocks) — the
    universal state-curriculum blueprint, the Louisiana OS
    generalized: *Water and the land*, *The working corridor*, *The
    state's table*, *Culture, language and celebration*, *Seasons,
    storms and memory* — every transfer check phrased on the
    learner's own state's real material. Dataset: **16,700 blocks ·
    44 packs · 210 tracks · 1,394 credentials**.
  - **The 50-state fact base** (`data/states/states.json`): every
    state with capital, region, a stylized US tile-grid position and
    five localization anchors (water / corridor / table / culture /
    storm) of public general knowledge — door-openers for local
    study, not exhaustive claims.
  - **The Cognition.X States app** (`apps/states/`, built by
    `tools/build_states.py`): a 50-tile US cartogram, the searchable
    catalog of catalogs, deep-linkable per-state pages rendering the
    five blueprint courses localized by that state's anchors
    ("Water and the land — *the Rio Grande border and the Gulf's
    chest*") plus the Institute Model civic tracks in that state's
    capital and the core spine with Flow Hub links, the blueprint
    and Institute reference views, and an Adoption view mapping the
    Louisiana pattern for any state. Platform-standard styles, voice
    personas and Guide included.
- **Education OS as the seed**: the States build extracts the Willie
  L. Brown Jr. Institute principles, mission and disclaimer directly
  from the Education OS app's fact base at build time (as the
  Louisiana build does) — the Education OS remains the model's
  source, rebuilt on the refreshed pipeline this release.

## [0.30.0] — 2026-09-10

### Added
- **Trades Network expansion — six regions, 222 entries**: three new
  regions join on the fact-base pattern (families × regions,
  councils as front doors): **Baton Rouge – River Region** (the
  Port of Greater Baton Rouge, the petrochemical corridor's grid, a
  Mississippi river-intake…), **Houston – Gulf Coast** (a Port
  Houston terminal on the ship channel, a bayou flood-control
  station, a METRO yard…), and **Los Angeles** (a San Pedro Bay
  berth, an LADWP receiving station, the Aqueduct terminus, a
  Hollywood soundstage…). Each carries its real council front door,
  its districts, nine public training-ground sites, its own
  **stylized city map** (the river through Baton Rouge, the Houston
  Ship Channel, the Pacific under LA), and the coast-correct
  longshore split (ILWU Pacific, ILA Gulf). The network map becomes
  a two-coast, six-node diagram; roster, simulations, flipped and
  district views scale automatically.
- **Baton Rouge hall parishes join the union layer** (Louisiana):
  the parish↔union integration generalizes to every Trade Hall that
  anchors a network region — East Baton Rouge and its hall's
  parishes now get their own matched-trade-family panels with
  River-Region-localized sims, alongside New Orleans.

## [0.29.0] — 2026-09-10

### Added
- **Credential Ledger v1 — signed, portable records** (Louisiana):
  the Parish Admin dashboard gains a **Records Office** — a
  per-browser ECDSA P-256 keypair (WebCrypto; created once, only the
  public key ever leaves), *Issue signed record* for any
  ledger-earned credential producing a portable `cx-credential/1`
  JSON (payload + signature + public key + office label), a *Show
  public key* export, and a *Verify* panel that checks any pasted
  record offline — tampering is detected. Honest scope stated in the
  UI: verification proves the record is unaltered and signed by that
  key's holder; who holds the key is confirmed with the hall, which
  publishes its public key. Graceful fallback where WebCrypto is
  absent. (Roadmap credential-ledger v1 checked; W3C VC / Open
  Badges alignment is follow-on.)
- **Launch budget layer**: a deterministic per-parish budget sketch —
  the five core seats, assessor seats scaled by population, hall
  spaces (with the rural sharing pattern), shared device count, and
  materials posture (printed workbooks by default on the rural
  tier) — on the Parish Admin *Launch team & budget* widget and in
  the `cxla-program/1` export. A scaffold each parish refines, not a
  quote.

## [0.28.0] — 2026-09-10

### Added
- **The Trade Hall Network OS** (Louisiana): the Regions view becomes
  an eight-section operating console — **eight system automations**
  running visibly over the real browser-local state and showing the
  call each is making right now: *Flow Keeper* (channel positions and
  overloads), *Break Caller* (profile cadences due), *Step Tuner*
  (step-down and stretch calls pending), *Credential Clerk*
  (auto-awards and the within-five-checks watch), *Cohort Watch*
  (stall and near-credential alerts), *Readiness Sentinel* (the five
  Wave-1 requirements statewide), *Teacher Relief* (the teacher's own
  load), and *Network Sync* (the eight-hall rollup). A system pulse
  re-runs the board every 20 seconds while the view is open, on
  demand from the pulse button, and fresh on every navigation.
- **Section-OS region cards**: each of the eight Trade Hall cards now
  carries its live section state — parishes Wave-1 ready, parishes
  preparing, and mission rungs logged — beside its Wave-1 launch
  load.
- **Teacher flow**: the Class flow board opens with the teacher's own
  state (*in flow / stretched / overloaded*), computed from class
  size, overload share and pending alerts, with a concrete relief
  automation for each: bank the win, delegate to guild leads, or stop
  triage and run a whole-class bench reset. Keeping the teacher in
  flow is now a first-class automation, not a hope.
- Guide tour gains the Network OS stop.

## [0.27.0] — 2026-09-10

### Added
- **Flow-state engine** (Louisiana): a per-learner flow model —
  *warming up / in flow / cruising / overloaded / break called* —
  computed from recorded pass-struggle events, with the automations
  actually steering the experience: the step shrinks under overload
  (with an alternative check format offered), stretches when
  cruising, and the break is called on the learner's own cadence.
  The student **Flow Session** panel runs it live (channel meter,
  guide line, three buttons — passes also credit the ledger and can
  still auto-award credentials); the teacher gains a **Class flow
  board** (states sorted worst-first with the automation's call and
  each profile's top supports); the parent gains **What helps my
  child**; parish and state rollups show live state distributions.
- **20 learner-type access modules**
  (`data/learners/learner_types.json`): dyslexia, dysgraphia,
  dyscalculia, ADHD, autistic learners, auditory & visual processing,
  speech & language, Deaf/HoH, blind/low-vision, mobility & motor,
  chronic illness & fatigue, anxiety-affected, trauma-affected,
  intellectual disability, gifted & twice-exceptional, multilingual
  learners, executive function & working memory, sensory processing,
  and deliberate processing pace — each with strengths, what-helps,
  home and classroom moves, and flow parameters (break cadence, step
  bias, alternative check formats). **Profiles are chosen supports,
  never diagnoses**: combined, changed or removed anytime,
  browser-local, never gating content; families are pointed to their
  school's own evaluation process for formal services.
- **Learning States & Universal Access pack** (`ACCESS`, 250 blocks):
  reading the learning states, access by design (the capability is
  the constant, the format is the variable), and communication /
  cognitive / whole-body access — the educator curriculum behind the
  modules. Dataset: **16,450 blocks · 43 packs · 205 tracks · 1,389
  credentials**.
- **Flow Hub access profile**: an optional profile select that
  retunes the session automations — focus-interval length and break
  cadence from the profile (ADHD: 15-minute focus, break every 5
  moves), and the Coach easing the band after a single struggle for
  gentler profiles — persisted, removable, never shared.

## [0.26.0] — 2026-09-10

### Added
- **City maps for all 111 union entries** (Trades Network): each
  region card is headed by a stylized, hand-placed city map — the
  Golden Gate, the Bay and the Pacific for San Francisco; the Bay and
  the East Bay hills for Oakland; Lake Pontchartrain and the
  Mississippi crescent for New Orleans — with the nine
  training-ground sites as clickable nodes carrying their
  trade-family counts (the three maps sum to exactly 111 entries).
  Clicking a node opens the Unions roster pre-filtered to that region
  and category.
- **Trades Across School Subjects pack** (`TRADESUBJ`, 250 blocks) —
  the early-pathways curriculum: *Discovering the working world*
  (K–2-up job and skill awareness), *The math on the jobsite*
  (fractions on the cut list, the 3-4-5 triangle, load charts),
  *The science in the craft* (circuits, siphons, heat paths, the
  pendulum), *Reading and writing the working word* (labels, manuals,
  logs, bids), and *Civics and the working city* (union history,
  ports, permits, the apprentice's civic ladder). Dataset: **16,200
  blocks · 42 packs · 200 tracks · 1,384 credentials**.
- **Classroom hooks on every roster entry**: all 37 trade families in
  the unions fact base now carry subject tags and one concrete
  "In class" connection (Ohm's law as ratio, flat patterns as
  unfolded geometry, cold chains as data…), shown on each of the 111
  roster cards — so schools and regions can teach the jobs and
  skills early, inside the subjects they already teach.

## [0.25.0] — 2026-09-10

### Added
- **Working learner ledger** (Louisiana): a browser-local,
  consent-first progress model measured on the 30 core-spine tracks
  (50 blocks / one credential each), with the automations running for
  real — standing recomputes on every change, **a credential is
  awarded automatically at 50 recorded checks**, the next-step
  recommendation derives deterministically (nearest credential →
  most-progressed track → first fresh track), and alerts surface who
  is close to a credential and who hasn't started. Ledger
  export/import via an explicit JSON box; a clearly-labeled,
  deterministic 12-learner **demo cohort** can be seeded and cleared
  in one tap to see the whole model working end to end. Records never
  leave the browser.
- **Comprehensive standing dashboards**: the Student view gains *My
  standing* (standing tiles, per-track meters, suggested next step,
  record-a-check with spoken credential award); the Teacher view
  gains *Class standing* — every student at a glance (per-student
  spine bars, one-tap check crediting on a working unit, a class ×
  track heatmap, live alerts, roster management); Parent gains *Where
  my child stands*; Parish Admin gains the *Learner standing rollup*
  feeding its five honest numbers; and State Admin's overview becomes
  **The complete system** — curriculum, parishes, the adopted
  rollout, readiness, and the live ledger in one nine-tile view.

### Changed
- Roadmap: the Phase 2 "learner state" line is now real —
  browser-local progress store with export/import, no account
  required (IndexedDB migration stays future work).

## [0.24.0] — 2026-09-10

### Added
- **Parish ↔ union integration**: `tools/build_louisiana.py` embeds
  the New Orleans-region slice of the Trades Network fact base, and
  every parish dashboard served by the **New Orleans Trade Hall**
  gains a *Trade unions & training sims* panel listing the trade
  families whose packs sit in that parish's own module plan — each
  with its international union, its New Orleans-localized training
  simulation, and the matching pack chips; the council remains the
  front door and simulation ≠ certification is restated in place.
  Parishes on other halls link across to the full network.

### Changed
- `docs/ROADMAP.md` brought current: v0.20–v0.24 milestones checked
  into Phases 2–3 (visualization layer, tutor swarm/voice, style
  templates, widget dashboards, adopted rollout, launch playbook as
  curriculum, the Trades Network, parish↔union integration), with the
  operational-budgets and network-expansion lines as the next
  Phase 3 work.
- Wiki refreshed: [[Louisiana Platform]] documents the widgetized
  dashboards, the three-persona voice model and the union panel;
  [[Flow Hub]] notes the humanized voice.

## [0.23.0] — 2026-09-10

### Added
- **Cognition.X Trades Network** (`apps/trades-network/`, built by
  `tools/build_trades.py`): 37 trade families × 3 regions (San
  Francisco, Oakland–East Bay, New Orleans) = **111 regional union &
  trade entries**, each naming its real international union (with
  per-coast overrides — ILWU West, ILA Gulf), a training simulation
  set on its region's own publicly known ground, and Flow Hub deep
  links into its backing packs. Views: the three-region network map,
  region cards (training grounds, councils, districts), the
  searchable/filterable 111-entry roster, nine simulation categories,
  the flipped cycle, and the district compact (SFUSD / OUSD / NOLA
  Public Schools). Two hard rules carried throughout: **no union
  local numbers** (the regional council is always the front door) and
  **simulation ≠ certification**.
- **Trades in the Classroom : Flipped & Gamified pack**
  (`TRADESCLASS`, 250 blocks) — the district integration curriculum:
  the flipped lesson, the honest game layer (points map one-to-one to
  passed transfer checks; the boss fight *is* the transfer check),
  union partnerships, the simulation studio and its law, and the
  district compact. Dataset: **15,950 blocks · 41 packs · 195 tracks
  · 1,379 credentials**.
- **Deep customizable role dashboards** (Louisiana): all six
  perspectives (student / teacher / parent / homeschool / parish
  admin / state admin) rebuilt on a widget system — 30 widgets in
  all, each dashboard composable (toggle panels, reorder them),
  persisted per role in the browser. New full-view widgets include
  the student's flow-session launcher and learning journal, the
  teacher's trainer track, flipped-units card and parish readiness
  board, the parent's family ledger and parish/hall card, the
  homeschool co-op guild, the parish admin's five honest numbers and
  launch team of five, and the state admin's per-requirement
  readiness rollup and Trade Hall launch-load chart.
- **Human-like voice model** in all three interactive apps: three
  personas (Warm / Steady / Brisk), a natural-voice preference list
  (Google/natural/neural voices first, graceful fallback),
  sentence-level utterances with slight prosody drift, and warmer
  conversational guide phrasing — still fully on-device, off by
  default, nothing leaves the page.

## [0.22.0] — 2026-09-10

### Added
- **Accelerated two-year adoption plan**: the four-wave proposal is
  superseded by an adopted two-wave rollout — **33 parishes launch in
  Wave 1 (2026–27)**, reaching ~88% of the state's population in year
  one; the remaining 31 follow in Wave 2 (2027–28). Deterministic
  cohort rule in `tools/build_louisiana.py` (original proposal wave,
  then population, then name); the original 4-wave phasing is retained
  on every parish as provenance. Tile map, Voronoi state map, legends,
  cohort timelines, expansion charts, region cards (with per-hall
  Wave-1 launch load) and role dashboards all present the adopted plan
  as primary.
- **Parish Launch & Scale pack** (`LAUNCH`, 250 blocks) — the rollout
  curriculum for the growth: five tracks (the first ninety days /
  standing up the Trade Hall / training the trainers / enrolling the
  community / measure, report, scale), every transfer check performed
  on the learner's own parish. Added to the core spine every parish
  runs, so all 64 parish module plans now carry their own launch
  curriculum.
- **Statewide Wave-1 readiness**: every parish dashboard gains an
  interactive five-requirement readiness board (one requirement per
  Launch & Scale track; browser-local record), the state view rolls
  readiness up across all 64 parishes, the State Admin dashboard
  counts Wave-1-ready parishes, and the parish program export includes
  readiness state — the whole state prepares to the Wave-1 standard
  now.
- **Five style templates** with a professional **Enterprise** default
  (slate ground, corporate blue, toned-down ornament) alongside
  Parade, Classic, Bayou and Gallery — all five carry full light/dark
  variants with WCAG-checked accents; stored style choices are
  validated against the list.
- **SmartCiti.X : New Orleans Trades** (`NOLATRADES`, 250 blocks) — a
  community pack supplementing the Louisiana OS edition as the
  Cognition.X companion to the SmartCiti.X New Orleans Trades Edition.
  Five tracks: the port and the crane, safe ground below the sea, water
  in/water out, power back on, and the craft pathway. Control-discipline
  themes mirror the SmartCiti.X simulator rubrics, and the honesty
  stance is shared: a simulator teaches control discipline and never
  counts as equipment certification. Transfer checks are phrased
  against the learner's own parish and stay observation-safe.

Dataset: **15,700 blocks · 40 packs · 190 tracks · 1,374 credentials.**

## [0.21.0] — 2026-09-10

### Added
- **Tutor swarm for flow-state optimization** (Flow Hub). Four new
  tutor agents — Coach (scaffolds after consecutive struggles),
  Scholar (context on each fresh theme), Examiner (evidence challenge
  on every claimed check), Motivator (flow-streak recognition and the
  break call every ten moves) — join the original four and operate as
  a **swarm**: a shared session blackboard, every tutor proposes each
  move, priority arbitration lets exactly one act. Interventions
  appear in a tutor strip on the block card and in the feed.
- **Voice agents** — on-device speech synthesis (no network): with
  voice on, the acting tutor and the guide speak. Off by default;
  toggle persisted; fully guarded where the API is absent.
- **Active Guide** in both apps: a 🧭 button starts a helper-agent
  walkthrough — 8 stops across Flow Hub, 9 across the Louisiana
  platform — highlighting each feature with Back/Next/End, navigating
  views itself, and narrating aloud when voice is on.
- **System run verified end-to-end** headlessly: a full flow session
  (Scholar on serve → Coach after two struggles → Motivator on a
  three-move flow streak → Examiner on a claimed check), both guides
  walked start to finish, zero page errors in both apps.

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
