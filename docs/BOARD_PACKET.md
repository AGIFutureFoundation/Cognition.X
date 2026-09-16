# The Curriculum Review Board — first-meeting packet

> Everything the board needs for its first sitting, drawn from the repository at the version in `VERSION` and checked by the tests: the checklist as a working form, the standing queue in the order the governance page sets, and the first decision on the agenda. The process itself is [`GOVERNANCE.md`](GOVERNANCE.md); the cohort side is [`COHORT_ONBOARDING.md`](COHORT_ONBOARDING.md); `tools/cohort_report.py` turns a cohort's evidence into the packet for every sitting after this one.

## Sitting one — agenda

1. Seat the board: three to seven reviewers, at minimum a practising educator, a rotating subject-matter reviewer, and an accessibility/equity reviewer; recusals recorded (`GOVERNANCE.md`, *The board*).
2. Adopt the six-point checklist below as the standard and the form.
3. **First decision: the 24 proposed credential names** (Finding 6, `DATA_REVIEW.md`; applied through the pipeline in v0.52.0 as a counted correction, proposed and not yet adopted). Adopt, amend or return each; the names live in `data/promotions/*.json` and a change is a PATCH release.
4. Order the standing queue (below) and assign the first pack to a reviewer pair.
5. Set the cadence: one pack per sitting until the classroom-facing packs are clear; evidence packets from cohorts at every sitting.

## The review checklist — as a form

Pack: ____________________  Reviewer: ____________________  Date: ________

| # | Question | Yes / No | Note |
|---|---|---|---|
| 1 | **Accuracy** — factual claims check out against public sources; the pack claims no expertise it does not carry | | |
| 2 | **Real transfer checks** — every check is a concrete task on real material a learner can reach, and safe: nothing energized, suspended or moving; nothing beyond modest purchases | | |
| 3 | **Honesty stances intact** — simulation ≠ certification; no union local numbers; access profiles are supports, never diagnoses; anchors are door-openers; disclaimers verbatim | | |
| 4 | **Respectful terminology** — communities named as they name themselves; identity-first / person-first per community preference | | |
| 5 | **Shape and provenance** — CI green; no edits to source rows or existing block ids; content arrived through specs, promotions or documented fact bases | | |
| 6 | **Access** — checks admit alternative formats; nothing gates on reading speed, handwriting or a single sensory channel | | |

Outcome: ☐ approved  ☐ approved with teaching notes  ☐ returned (supersession proposed — never an edit to an id)

## First decision — the proposed credential names

Each replaced the bare level word *Practitioner* that arrived with the v0.1.0 import. A credential names a person and a capability, never a level or a job title it cannot confer.

| Pack | Track | Proposed credential |
|---|---|---|
| Basic Life Skills & Self-Reliance | The household that works | **Household Keeper** |
| Basic Life Skills & Self-Reliance | Money that lasts the month | **Home Budget Keeper** |
| Basic Life Skills & Self-Reliance | Getting and holding work | **Working Life Navigator** |
| Basic Life Skills & Self-Reliance | Getting things done in the world | **Everyday Navigator** |
| Basic Life Skills & Self-Reliance | The first minutes of an emergency | **First-Minutes Responder** |
| Care Across a Life | The first years | **Infant Care Companion** |
| Care Across a Life | Growing up beside them | **Childhood Companion** |
| Care Across a Life | The middle of a life | **Adult Life Steward** |
| Care Across a Life | Later life, lived well | **Elder Care Companion** |
| Care Across a Life | The carer's craft | **Family Carer** |
| Making, Repair & Reuse | Making something that holds | **Workshop Maker** |
| Making, Repair & Reuse | Repair before replace | **Everyday Repairer** |
| Making, Repair & Reuse | Reuse and what things are worth | **Reuse Steward** |
| Making, Repair & Reuse | Tools and the workshop | **Workshop Hand** |
| Making, Repair & Reuse | The trade and the living | **Trade Pathfinder** |
| Preventive Health & Everyday Care | The mouth, understood | **Oral Health Peer** |
| Preventive Health & Everyday Care | Eyes and ears in a classroom and a life | **Sight and Hearing Peer** |
| Preventive Health & Everyday Care | Food and water that keep you well | **Food and Water Peer** |
| Preventive Health & Everyday Care | A body and mind that recover | **Recovery Peer** |
| Water, Land & Climate | Water: source to drain | **Water Reader** |
| Water, Land & Climate | The ground under you | **Land Reader** |
| Water, Land & Climate | Climate, read locally | **Local Climate Reader** |
| Water, Land & Climate | Energy where you live | **Home Energy Reader** |
| Water, Land & Climate | Resilience when it arrives | **Resilience Planner** |

## The standing queue

Every pack generated from a spec after the import — **22 packs, 6,160 blocks** — is validator-clean and has **not passed this board**. Until a pack clears review, the in-app scaffold labels stay and adopters treat it as a draft for their own committee. Order per `GOVERNANCE.md`: classroom-facing first, then community packs; the OS editions arrived with the import and are reviewed as source content on request.

### Classroom-facing first

| Order | Pack | Blocks | Tracks | Reviewer pair | Sitting | Outcome |
|---:|---|---:|---:|---|---|---|
| 1 | Learning States & Universal Access (`ACCESS`) | 250 | 5 | | | |
| 2 | Parish Launch & Scale (`LAUNCH`) | 250 | 5 | | | |
| 3 | Trades in the Classroom : Flipped & Gamified (`TRADESCLASS`) | 250 | 5 | | | |
| 4 | Trades Across School Subjects (`TRADESUBJ`) | 250 | 5 | | | |
| 5 | Cognition.X : Louisiana OS (`LAOS`) | 500 | 10 | | | |
| 6 | Cognition.X : States OS (`STATEOS`) | 250 | 5 | | | |
| 7 | Cognition.X : Education OS (`EDUOS`) | 660 | 0 | | | |
| 8 | Emergency Preparedness & First Response (`EMERGENCY`) | 250 | 5 | | | |
| 9 | Civic Leadership Legacy : Louisiana (`LEGACYLA`) | 250 | 5 | | | |
| 10 | Civic Leadership Legacy : The Institute Model (`LEGACYMODEL`) | 250 | 5 | | | |
| 11 | Civic Leadership Legacy : California (`LEGACYCA`) | 250 | 5 | | | |
| 12 | Civic Leadership Legacy : Texas (`LEGACYTX`) | 250 | 5 | | | |

### Community packs

| Order | Pack | Blocks | Tracks | Reviewer pair | Sitting | Outcome |
|---:|---|---:|---:|---|---|---|
| 13 | Digital Life, Data & AI (`DIGITAL`) | 250 | 5 | | | |
| 14 | Energy, Grid & the Home (`ENERGY`) | 250 | 5 | | | |
| 15 | Food, Cooking & Nutrition (`FOOD`) | 250 | 5 | | | |
| 16 | Law, Contracts & Everyday Rights (`LAW`) | 250 | 5 | | | |
| 17 | Transport & Mobility (`TRANSPORT`) | 250 | 5 | | | |
| 18 | Arts, Making Media & Performance (`ARTS`) | 250 | 5 | | | |
| 19 | Arts & Craft Trades : Louisiana Makers (`ARTCRAFT`) | 250 | 5 | | | |
| 20 | Culinary Trades : The Louisiana Kitchen (`CULINARY`) | 250 | 5 | | | |
| 21 | Music : Creation to Industry (`MUSICIND`) | 250 | 5 | | | |
| 22 | SmartCiti.X : New Orleans Trades (`NOLATRADES`) | 250 | 5 | | | |

## What the board receives at every later sitting

- The **cohort packet** from `tools/cohort_report.py` — a cohort's opt-in, aggregate evidence merged into: the cohort summary, per-track witnessed rates, revision priorities (not-yet rate ≥ 40% over ≥ 5 witnessed attempts), unreported tracks, the queue status of the packs the cohort used, and the v1.0 gate status. Evidence proposes; the board disposes.
- Any **supersession** proposed by evidence or a reviewer, as a PR through the acceptance flow.
- The **credential list** to carry to the district's CTE office when transcript recognition is on the table (register DI-03).

## The v1.0 gate, restated

v1.0 is cut when a named external cohort — one hall, one class, one co-op — has completed credentials on an unmodified release, its records office has exchanged keys with at least one other office, its opt-in evidence has been collected through one full track, and this board has reviewed at least the packs that cohort used. `tools/cohort_report.py` prints the gate status from the evidence; the rest is the board's own record.
