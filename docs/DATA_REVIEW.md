# Data Review — imported artifacts (2026-09-09)

Findings from reviewing the five imported files, and what was done about
each. The validator (`tools/validate_blocks.py`) enforces the fixes going
forward.

## What was imported

| Artifact | Verdict | Disposition |
|---|---|---|
| `Cognition.X_all_blocks.csv` (×2 uploads) | Byte-identical duplicates (same MD5) | One copy kept at `data/source/` |
| `Cognition.X_.pdf` (85 pp) | The same CSV rendered as a table — no additional content | Not committed (redundant, 1.6 MB) |
| `affeducationos.html` (7.9 MB) | Education OS app, earlier build | Archived as `apps/education-os/versions/v0.1.0-education-os.html` |
| `gov.html` (8.1 MB) | Same app, later iteration — internal changelog reaches **v227 "Sector Specialization"** (+120 master blocks); Google Fonts dependency removed, so fully offline | Canonical app at `apps/education-os/index.html` |

The two app builds are otherwise structurally identical (same 545 `<h2>`
sections; the only other diff is the fonts `<link>`).

## Dataset findings (6,750 source rows)

1. **Cross-pack code collisions (fixed).** `code` is only unique within a
   pack: track prefixes are reused across packs (`EV-*` in both Housing &
   Tenancy and Sapient OS; `SF-*` in three packs; 450 codes, 550 rows
   affected). Fix: `tools/normalize_blocks.py` prepends a deterministic,
   globally unique `block_id` (`CX-<PACK>-<NNNN>`); the original `code` is
   kept untouched. The validator now allows duplicate codes only across
   packs, never within one.

2. **Two schemas in one file (backfill in progress).** 4,500
   "tracked" source rows carry `track`/`code`/`level`/`description`; 2,250
   "legacy" rows left those empty. *Update (v0.8.0):* the five cleanly
   banded 250-row packs (Basic Life Skills, Preventive Health,
   Water/Land/Climate, Care Across a Life, Making/Repair/Reuse) carried
   their track structure as `(XX)` suffixes in theme names and are now
   promoted to the tracked schema via `data/promotions/*.json` — 1,250
   rows backfilled, source values untouched. *Update (v0.14.0):* the
   1,000 irregular rows (K–12, Trade School, and seven thematic packs)
   received a structural light fill — deterministic `code` (`LB-<n>`)
   and grade-derived `level` on every row, with the validator now
   requiring both dataset-wide. Their shapes are irregular by design
   and are not forced into 10×5; authored `description` (and `track`
   where genuine groupings exist) is the remaining content work — see
   the [roadmap](ROADMAP.md). *Update (v0.90.0):* Future-Work's 111
   rows now carry an authored `description` (one complete sentence per
   theme, since each theme names exactly one row, not five spanning a
   band ladder), filled through a new `"unbanded": true` promotion
   (`tools/normalize_blocks.py`); `track`/`code` are left as they were
   (`LB-<n>` codes), since these packs' natural sub-groupings don't
   form the tracked 50-block shape. *Update (v0.91.0):* Civic &
   Leadership and Language, Culture & Communication (222 more rows)
   filled the same way. Three more foundation packs (Empathy &
   Emotional Intelligence, Community & Relationship Practice, and most
   of Health & Community) fit the same mechanism and are the next
   tranche of `docs/NEXT_STEPS_2.md` prompt 3; K–12, Trade School and
   Regional use single grades or adult bands and need a further
   extension.

2b. **Placeholder transfer checks (found during promotion — resolved
   in v0.13.0).** Most pre-promotion legacy rows carried a generic
   check — "Demonstrate it once, correctly, to somebody who will use
   it" / "Do it once, for real, and show it to somebody who will use
   it" — rather than a per-theme task (217 themes / 1,085 rows across
   the five promoted packs). *Resolution:* real per-theme checks were
   authored in the promotion specs, and the normalizer replaces a
   source check **only** when it is one of the two known placeholder
   sentences — real source checks are never overwritten. Zero
   placeholder checks remain dataset-wide.

3. **Band descriptions are suffixed, not differentiated (in progress
   since v0.65.0).** Within a theme, all five grade bands shared one
   description distinguished only by an "— at {band}" suffix, and the
   transfer check is identical across bands. Since v0.65.0 a pack spec
   or promotion theme may carry `bands` — five sentences in what the
   learner does — and the whole core spine does (five packs, 1,500 rows;
   suffix rows 11,250 → 9,750, a ratchet in the tests). The transfer
   check still does not vary by band; that is a later item.

4. **Minor anomalies (documented).** Two rows have grade `—` (Trade
   School capstones); grades `9–12 · adult` (7 rows) and `11–12 · adult`
   (47 rows) appear only in Trade School; K–12 uses single grades K–12
   plus bridge rows. All legitimate on inspection; the validator treats
   them as legacy-pack shapes.

5. **App data vs. CSV (reconciliation underway).** The app embeds its
   own master-block library, which by v227 had grown past the CSV
   export. *Update (v0.17.0):* the app's uniform sector master-block
   library (`DATA.sectorBlocks` — 5,200 practice blocks, codes
   `T0A…T0Z`, including the app-only **Education OS** edition) is now
   extracted into the dataset by `tools/extract_app_blocks.py`,
   mapped as adult `Lead`-level practice rows (task + outcome joined
   as the transfer check; descriptions deferred with the other
   foundation authoring). Remaining Phase 2 work: the app's
   non-uniform earlier structures (wlb courses, K-12 program layers)
   and rebuilding the app itself from `blocks.csv`.

## Continuation

Following the established shape (5 tracks × 10 themes × 5 bands), a new
community pack **Digital Life, Data & AI** (250 blocks; spec at
`data/pack_specs/digital-life-data-ai.json`) was generated and merged into
the canonical dataset — the domain most conspicuously missing from the 25
existing packs. Canonical totals: **7,000 blocks · 26 packs · 95 tracks ·
402 credentials**, all green under the validator.

---

## Current-state addendum (v0.32.0 review, 2026-09-10)

The findings above cover the original import. As of v0.32.0 the dataset
stands at **16,700 blocks · 44 packs · 210 tracks · 1,394 credentials**;
the full platform assessment now lives in
[`docs/SYSTEM_REVIEW.md`](SYSTEM_REVIEW.md). Data-specific status:

1. **Backfill complete** where it was promised: all tracked-shape gaps
   from finding 2 were closed by v0.14.0 (codes + levels dataset-wide);
   the 217 placeholder transfer checks from finding 3 were replaced
   with authored per-theme checks by v0.13.0 (guarded substitution —
   the two exact generic sentences only). Zero placeholders remain.
2. **Foundation library still deferred**: the 1,000 irregular rows
   (Empathy, Community Practice, Future-Work, Regional, Civic,
   Health, Language) carry structural `LB-<n>` codes and derived
   levels but no authored tracks/descriptions. This is the largest
   remaining content debt, unchanged since v0.14.0 and still honest.
3. **Machine-authored packs await the review board**: everything
   added since import (~9,950 blocks across community, legacy, OS,
   trades, access and states packs) is validator-clean and
   internally consistent but has not been reviewed by subject-matter
   educators. The roadmap's curriculum review board is the intended
   gate before classroom use; in-app scaffold labels (parish
   missions, state anchors) are correct and must stay.
4. **App-reconciled rows**: the 5,200 sector master blocks keep
   task/outcome fidelity through `app-master-blocks.map.json`;
   editing such a row in the dataset intentionally degrades to
   full-check-as-task in the Education OS overlay (dataset wins).
5. **Fact bases are data too**: parishes (from the Education OS app),
   unions (37 families × 6 regions), learner types (20), and states
   (50 × 5 anchors) are reviewed content with the same stance —
   public general knowledge, door-openers not exhaustive claims, no
   union local numbers, profiles never diagnoses.

## Stance — named people in the Makers' Hall (v0.48.0)

`data/louisiana/makers.json` names 63 people. The rule: **public record
only** — published work, recordings, restaurants, exhibitions, awards,
obituaries, institutions that carry their names — as *examples of a
craft*, with the file's own `note` (rendered in the app) stating that
naming is not endorsement, implies no affiliation, and that living
people appear only through what is already public about them. Working
local practitioners are deliberately absent: the parish, the school
board and the trade hall name their own, in person, with consent.
`tests/test_platform.py` holds the note's two sentences, the parish
names, the stage ids and region coverage mechanically. A factual
correction to any entry is a PATCH; removal on a person's or estate's
request is honoured without discussion.

## Finding 6 — level words standing in for credential names (v0.45.0 → corrected v0.52.0, pending board adoption)

Found by the invariant suite in v0.45.0: **1,228 rows — 7% of the
dataset, 24 tracks across five community packs — named their credential
with the bare band level “Practitioner”** instead of an accomplishment.
The defect arrived with the v0.1.0 import and passed through untouched
because the pipeline correctly never overwrites a non-empty source field.

**What v0.52.0 did.** Twenty-four credential names were drafted in the
shape those packs already use — a person and a capability, never a level
word, never a job title the credential cannot confer — and applied
**through the pipeline**: each track in `data/promotions/*.json` now
carries a `credential`, and `tools/normalize_blocks.py` replaces a bare
level word with it as the one deliberate, counted exception to
fill-empty-only (“corrected 1,195 level-word credentials” is printed on
every run; a real credential name is never overwritten). The split track
*The mouth, understood* is unified on *Oral Health Peer*. No `block_id`
changed.

| Pack | Track | Proposed credential |
|---|---|---|
| Basic Life Skills & Self-Reliance | The household that works | Household Keeper |
| | Money that lasts the month | Home Budget Keeper |
| | Getting and holding work | Working Life Navigator |
| | Getting things done in the world | Everyday Navigator |
| | The first minutes of an emergency | First-Minutes Responder |
| Care Across a Life | The first years | Infant Care Companion |
| | Growing up beside them | Childhood Companion |
| | The middle of a life | Adult Life Steward |
| | Later life, lived well | Elder Care Companion |
| | The carer's craft | Family Carer |
| Making, Repair & Reuse | Making something that holds | Workshop Maker |
| | Repair before replace | Everyday Repairer |
| | Reuse and what things are worth | Reuse Steward |
| | Tools and the workshop | Workshop Hand |
| | The trade and the living | Trade Pathfinder |
| Preventive Health & Everyday Care | The mouth, understood | Oral Health Peer (unified) |
| | Eyes and ears in a classroom and a life | Sight and Hearing Peer |
| | Food and water that keep you well | Food and Water Peer |
| | A body and mind that recover | Recovery Peer |
| Water, Land & Climate | Water: source to drain | Water Reader |
| | The ground under you | Land Reader |
| | Climate, read locally | Local Climate Reader |
| | Energy where you live | Home Energy Reader |
| | Resilience when it arrives | Resilience Planner |

**Status: proposed, not adopted.** `docs/GOVERNANCE.md` reserves authored
curriculum content to the review board; these names are drafting for it
and are its first agenda item. Adopting, renaming or rejecting any of
them is a data edit to the promotion file and a PATCH release.

**What remains.** 33 rows — the *Empathy & Emotional Intelligence* pack's
(EW) theme group — still carry “Practitioner”. They have no track to
hang a credential on: eleven themes with three-to-seven bands each, not
the 50-block shape, so the promotion mechanism cannot reach them without
first authoring the missing blocks. The ratchet in `tests/test_platform.py`
now reads **33 rows · 0 tracks · 0 split tracks** and can only go down.
The board's choice: complete the group as a track (17 authored blocks) or
retire the credential field on those rows.
