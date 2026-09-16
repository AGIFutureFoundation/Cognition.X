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
| **v0.57.0** | The security and compliance register and roadmap (44 controls across platform, federal, state, parish, local and district levels, evidence checked in CI) and wave one: a non-extractable Records Office key, release checksums and `SECURITY.md`, breach notification for all fifty states, youth hazard orders in the studio, adopter templates |
| v0.56.0 | Standards mapping and transfer-check rubrics: the LSS K–12 codes generated from the program (52 blocks, *cites*), NGSS Engineering Design for four Robotics OS tracks (*touches*), 30 rubrics for the core-spine tracks — in Assessor Mode, Flow Hub pack detail and the printed workbook; `validate_standards.py` in CI |
| v0.55.0 | The compliance and regulatory review of the apps: typefaces embedded so no app makes a third-party request, a strict Content-Security-Policy in every app (the no-network stance browser-enforced), no referrer leakage, a Data & privacy notice with erase-all, `docs/COMPLIANCE_REVIEW.md` (not legal advice) |
| v0.54.0 | The Simulation Studio: `data/simulations/scenarios.json` (18 branching control-discipline scenarios tied to real tracks, each carrying its witnessed transfer check verbatim) played by one shared engine in all six apps — deterministic, three difficulties, no timers, `cx-simrun/1` runs kept as practice and never credentials; `validate_simulations.py` in CI |
| v0.53.2 | The three-page investor deck (`docs/PITCH_DECK.md`, generator in `tools/film/deck3/`) with the round on standard forms — post-money SAFE, NVCA at the priced round, Reg D 506(b) — and its narrated pitch video |
| v0.53.1 | The investor data room: `docs/INVESTOR_BRIEF.md` and `docs/CAPITAL_STRUCTURE.md` with a claim-by-claim bridge to what the repository proves |
| v0.53.0 | The accessibility audit: axe-core over 45 views, every WCAG-tagged finding fixed at the token/component level (0 remaining), keyboard sweep clean, `docs/ACCESSIBILITY.md` with what remains, the audit result held by the tests |
| v0.52.0 | The credential-naming correction: 24 proposed credential names (person + capability) applied through the pipeline as a counted exception, the split track unified, ratchets lowered to 33 rows / 0 tracks — proposed to the review board, not yet adopted; plus the accessibility audit runner |
| v0.51.0 | The compliance layer: for every state, ten domains a program office meets — privacy law and agreement, homeschool forms, nonprofit and charity registration, background checks, mandated reporting, apprenticeship agency, CTE list, accessibility, sales tax — with forms, agencies, fees (as-of, verify) and cost roll-ups; the States app Compliance view, state-page panels, the Louisiana State Admin widget, and a CI-checked report |
| v0.50.1 | A more human narration voice: kokoro-onnx (offline) fronts the film kit's narration via `tools/film/tts.py`, piper kept as fallback; shorts and pitch video re-rendered |
| v0.50.0 | The film kit speaks: offline narration (piper) in the film driver, five narrated feature shorts for social channels, and the 15-slide pitch deck generator with its 7-minute narrated video |
| v0.49.1 | The investor walkthrough (`docs/WALKTHROUGH.md`): the deep features and learning system in one document, every number tied to the dataset |
| v0.49.0 | The film kit: two product films rendered from the apps themselves by `tools/film/` (*The Flow Zone* 3:04 · *Training that proves itself* 2:15) and the production briefs for their cinematic cuts |
| v0.48.0 | The culture trades: three new trade packs — *Music : Creation to Industry* (the whole music trade, ear to industry), *Culinary Trades : The Louisiana Kitchen* and *Arts & Craft Trades : Louisiana Makers* — and the Louisiana app's Makers' Hall: creation→industry pathway maps, 154 industry roles, 63 public-record makers by parish, 42 organisations, parish and role-dashboard maker panels — 17,450 blocks / 47 packs |
| v0.47.0 | The 24 adversarially-verified review findings closed: a dead standing panel, silent save failures, focus theft on every re-render, a credential that asserted unseen witnessing, CI never re-deriving 60% of the dataset, a latent slug collision, half-enforced track shape, three keyboard traps, and validated ledger imports |
| v0.46.0 | The Education OS design system restored — tokens recovered from the app's own documented brand values and vizTok fallbacks, ~35 base component rules generated by its builder, full light/dark, every text pair verified at 4.5:1 |
| v0.45.0 | The Education OS runs for the first time (its HTML shell, missing since the v0.1.0 import, is now generated from the app's own VIEWS array); committed test suites — 121 Python invariants in CI and 60 browser assertions over the working models; the 1,228-row credential-naming defect documented and pinned; documentation corrected against the code; ten ranked next-step briefs |
| v0.44.0 | The Louisiana K–12 program canonicalized (13 grades × 6 LDOE-coded threads + 8 policy threads, rendered grade-by-grade in the Curriculum view) and the CI-generated data-quality dashboard (docs/DATA_QUALITY.md, regenerated and drift-checked on every push) |
| v0.43.0 | The Leadership Ladder: the WLB Institute's full leadership program (5 strands × 5 eras × 125 courses, ten-module method, bridge, standards, graduation seal, Fellowship pattern) canonicalized into the dataset and rendered in the Louisiana and States Institute views |
| v0.42.0 | Dashboard agent swarms: all seven role dashboards open with a blackboard crew of agents (24 in all) computing priority + call from real browser state, with arbitration surfacing the swarm's one call — agents propose; the person disposes |
| v0.41.0 | Reproducible build guaranteed in CI: a fresh clone + Python 3 regenerates the whole platform byte-for-byte, and the new CI apps job rebuilds all six apps on every push, failing on any drift from their sources |
| v0.40.0 | Granular Network OS: every one of the eight section automations expands into a drill-down board with its exact thresholds, the per-learner/per-parish rows it computed from, and a pulse log of recent calls — expansion state kept across the 20-second pulse |
| v0.39.0 | Education OS pipeline stage two: the Louisiana parish fact base and WLB Institute fact base become canonical data files (data/louisiana/, data/wlb/); the Louisiana and States builders read them instead of evaluating the app template — round-trip verified byte-identical |
| v0.38.0 | Federation v2: portable cx-trustlist/1 trust-list exchange (second-hand entries marked until confirmed out-of-band), cx-revocation/1 signed revocation lists with the new ⊘ revoked verification outcome, and record ids + dataset versions in every issued credential payload |
| v0.37.0 | Cognition.X Platform — the capstone working model: a clickable ten-node system map and a six-stage runnable learning loop executing the platform's real mechanics (flow machine, 50-check credential, WebCrypto-signed records, three-grade verification, evidence aggregate) on labeled demo data |
| v0.36.0 | The Evidence Loop v1: opt-in aggregate cx-evidence/1 export (consent-gated, no names, never auto-sent) + evidence_triage.py revision priorities for the review board; the path-to-v1.0 operational checklist |
| v0.35.0 | Pack Studio educator authoring (Flow Hub Author view: validated spec editor with generator round-trip) and the governance process (docs/GOVERNANCE.md: review board, checklist, supersede policy, review queue) |
| v0.34.0 | Federation v1 (trusted-offices registry; three-grade record verification by office name) and PWA install metadata across all four apps |
| v0.33.0 | Complete system review (docs/SYSTEM_REVIEW.md), data-review addendum, roadmap restructure with recommended order, and the accessibility first pass (skip links, lang, reduced motion, aria labels, live regions) across all four interactive apps |
| v0.32.0 | Assessor Mode (witnessed-check queue, rubric, evidence capture, honest confirm/not-yet crediting) and printable per-track workbooks in Flow Hub for zero-device settings |
| v0.31.0 | Custom curriculum for all 50 states: the States OS blueprint pack (250 blocks), the 50-state fact base, and the Cognition.X States app (US tile cartogram, per-state localized courses, Institute Model in every capital) seeded from the Education OS fact base — 16,700 blocks / 44 packs |
| v0.30.0 | Trades Network expansion: Baton Rouge–River Region, Houston–Gulf Coast and Los Angeles join — 37 families × 6 regions = 222 entries, three new city maps, Baton Rouge hall parishes gain union panels |
| v0.29.0 | Credential Ledger v1: per-browser Records Office (ECDSA P-256), signed portable cx-credential/1 records with offline verification and tamper detection; deterministic per-parish launch budget sketches |
| v0.28.0 | The Trade Hall Network OS: eight system automations on a live pulse (flow, breaks, steps, credentials, alerts, readiness, teacher relief, network sync), section-OS region cards, teacher flow state with relief automations |
| v0.27.0 | Flow-state engine driving the experience (profile-aware break calls, shrink/stretch automations, alternative check formats), 20 learner-type access modules (chosen supports, never diagnoses), Learning States & Universal Access pack — 16,450 blocks / 43 packs |
| v0.26.0 | City maps for all 111 union entries (three stylized region maps, click-through to filtered rosters), Trades Across School Subjects pack (250 blocks — trades inside math/science/ELA/civics from K–2), classroom hooks on every roster card — 16,200 blocks / 42 packs |
| v0.25.0 | Working learner ledger (auto credential at 50 checks, recommendations, alerts, export/import, demo cohort) + comprehensive standing dashboards for all six roles |
| v0.24.0 | Parish ↔ union integration (New Orleans-hall parishes surface their matched trade families); roadmap and wiki brought current |
| v0.23.0 | Trades Network app (111 union/trade entries across SF, Oakland & New Orleans, regional training sims, district compacts), Trades in the Classroom pack (flipped & gamified, 250 blocks), widgetized customizable role dashboards, three-persona human-like voice model — 15,950 blocks / 41 packs |
| v0.22.0 | Adopted two-year rollout (33 parishes in Wave 1 2026–27, statewide by 2027–28), Parish Launch & Scale pack (250 blocks), statewide Wave-1 readiness boards, five style templates with an Enterprise default; folds in the SmartCiti.X : New Orleans Trades pack — 15,700 blocks / 40 packs |
| v0.21.0 | Tutor swarm (blackboard + priority arbitration), on-device voice agents, active Guide walkthroughs in both apps — flow loop verified end-to-end |
| v0.20.0 | Recursive Voronoi cell graphics (state + curriculum), expansion-to-Wave-4 timelines, print program template |
| v0.19.0 | Education OS onto the pipeline: index.html built from template + blocks.csv overlay (sector library canonical; duplicate inflation cured) |
| v0.18.0 | Runnable parish missions, the universal Institute Model pack (leadership + civics + EQ, all states), six role dashboards (student/teacher/parent/homeschool/parish/state) |
| v0.17.0 | App reconciliation slice one: 5,200 sector master blocks extracted into the dataset, revealing the Education OS edition — 14,950 blocks / 37 packs |
| v0.16.0 | Parish mission modules (64 × 5 generated capstone ladders from each parish's narrative world), plan customizer, parish program export |
| v0.15.0 | Cognition.X : Louisiana OS (500 blocks, 10 tracks — river, coast, corridor, ports, agriculture, table, music, languages, festivals, storm memory), added to every parish's core spine |
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
