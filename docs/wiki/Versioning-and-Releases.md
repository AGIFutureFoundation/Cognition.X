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
| **v0.33.0** | Complete system review (docs/SYSTEM_REVIEW.md), data-review addendum, roadmap restructure with recommended order, and the accessibility first pass (skip links, lang, reduced motion, aria labels, live regions) across all four interactive apps |
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
