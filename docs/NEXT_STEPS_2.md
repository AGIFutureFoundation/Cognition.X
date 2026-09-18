# Next steps, round two — ten prompts

Ten self-contained sessions, ranked by value, each a complete brief:
what to do, why it matters now, the evidence behind it, the files, the
acceptance criteria, and the commands that prove it. Each stands alone
and assumes only a clone of this repository.

They were written at **v0.71.0**, from the second complete system review
(`SYSTEM_REVIEW_2.md`), after the first ten (`NEXT_STEPS_OPUS5.md`) were
all worked. Where a prompt rests on a finding, the finding is stated
with its file so the next session can confirm it rather than trust it.

## The standing rules every session inherits

Unchanged from the first set, and not style preferences:

1. **Build products are never hand-edited.** Edit `apps/*/template.html`
   or `tools/build_*.py`, then rebuild; CI fails on drift.
2. **`block_id`s are never reused or renumbered.** Supersede; never
   rewrite.
3. **Never overwrite a non-empty source field** — except through a
   designed, counted, visible exception (today: the credential
   correction in `data/promotions/`). Prompt 1 is about designing the
   second one, not about skipping the rule.
4. **A simulation is practice.** Never a check, never a credential.
   A credential is issued at exactly fifty witnessed checks.
5. **Nothing leaves a page on its own.** No fetch, no beacon, no SDK, no
   tracking of hands, eyes or faces. Exports are the person's act.
6. **Access profiles are chosen supports, never diagnoses.** No union
   local numbers. Every compliance document says *not legal advice*.
7. **Every claim in a document is measured, and the tests hold the ones
   that can drift.** Add the test in the same change as the claim.
8. **Both suites green before a push:** `python3 tests/test_platform.py`
   and `NODE_PATH=$(npm root -g) node tests/browser/smoke.js`.

---

## 1 — Design the description override, then author the sector-OS bands *(done — the override in v0.72.0; the seven sector packs authored v0.72.0–v0.78.0: Corporate, Science, Robotics, Global Health, Multilateral, Sapient, Non-Profit Practice — 3,500 rows, the whole sector-OS suffix debt; band-suffix rows 9,750 → 6,250; `tools/author_override.py`)*

**Why.** 9,750 rows carry one sentence per theme with a band suffix.
3,457 of them are in the seven sector-OS packs (Corporate, Science,
Robotics, Global Health, Multilateral, Sapient, Non-Profit Practice:
43% of each pack), whose source descriptions are *non-empty*. The
per-band `bands` mechanism from the first set (`tools/generate_pack.py`
`band_description`, `tools/normalize_blocks.py` `apply_promotions`) can
only fill empty fields, by rule 3. Authoring those 3,457 sentences would
change nothing until an override exists — so the override design is the
prompt, and it has to be as visible and as counted as the credential
correction it resembles.

**Evidence.** `docs/DATA_QUALITY.md` (Band-suffix % column: 43–44% on
the seven packs); `tools/normalize_blocks.py` (the fill-empty rule and
the credential exception); `tests/test_platform.py`
`KNOWN_BAND_SUFFIX_ROWS = 9750`.

**Steps.**
1. Add a `descriptions` override kind to promotions: a promotion may
   replace a non-empty description **only** when the existing text
   matches the band-suffix pattern (`… — at ‹band›`) and the replacement
   is a per-band sentence for the same theme. Anything else is refused
   by the normaliser with the row id.
2. Count the exception the way the credential correction is counted:
   a `description_overrides` line in `docs/DATA_QUALITY.md`, a ratchet in
   the tests, and the CHANGELOG entry naming the number.
3. Author the Corporate OS first (ten tracks, the pack most halls will
   meet), then the others by pack importance; keep the band ladder
   (6–8 smaller scope or with a checker; 9–10 the whole thing for real;
   11–12 for others, for a real body, on the record).
4. Lower `KNOWN_BAND_SUFFIX_ROWS` in the same change as each tranche.

**Acceptance.** The override refuses a non-suffixed target (test); every
overridden row is counted in the dashboard; no block id changes; the
suffix ratchet drops by exactly the authored count; both suites pass.

**Verify.**
```bash
python3 tools/normalize_blocks.py && python3 tools/data_quality.py
python3 tests/test_platform.py
```

---

## 2 — The community packs' band sentences, by pack importance — CLOSED in v0.89.0 *(tranche one — SmartCiti.X New Orleans Trades and the States OS — done in v0.79.0; tranche two — Trades in the Classroom and Trades Across School Subjects — done in v0.80.0; tranche three — Music, Culinary Trades and Arts, Making Media & Performance — done in v0.81.0; tranche four — Digital Life and Law — done in v0.82.0; tranche five — Preventive Health & Everyday Care and Care Across a Life — done in v0.83.0; tranche six — Water, Land & Climate and Making, Repair & Reuse — done in v0.84.0; tranche seven — Arts & Craft Trades : Louisiana Makers and Energy, Grid & the Home — done in v0.85.0; tranche eight — the three Civic Leadership Legacy packs (Institute Model, California, Texas) — done in v0.86.0; tranche nine — Food, Cooking & Nutrition, Learning States & Universal Access, and Transport & Mobility — done in v0.87.0, closing out every pack-spec-based (no-override) community pack; tranche ten — Housing & Tenancy and Money, Benefits & Entitlements — done in v0.88.0, the first override-based tranche, each authored through a brand-new `override: band-suffix` promotion file since neither pack had an existing promotion or pack_spec file; tranche eleven — Reentry & Recovery Pathways and Neighbourhood, Safety & Civic Voice — done in v0.89.0 via the same new-override-promotion mechanism, 6,250 rows across all eleven tranches. Every band-suffix row in the dataset now carries an authored per-band sentence — the dataset-wide band-suffix percentage is 0%)*

**Why.** The remaining 6,293 suffixed rows sit in 25 community and
regional packs of 250 (and the States OS), where the source description
is empty and the `bands` mechanism already works end to end (five packs
done in v0.65.0–v0.67.0). No design decision is needed; it is authoring,
and it is where a learner reads the platform most.

**Evidence.** `docs/DATA_QUALITY.md` (packs at 100% band-suffix);
`data/pack_specs/emergency-preparedness-first-response.json` (the
worked shape); `CONTRIBUTING.md` "Per-band descriptions (`bands`)".

**Steps.** Tranches of two packs (500 rows), in this order: SmartCiti.X
New Orleans Trades and the States OS; Trades in the Classroom and Trades
Across School Subjects; the three culture packs; Digital Life and Law;
then the life-skills family. Each tranche: author `bands` in the spec,
regenerate, add the pack to `BAND_AUTHORED_PACKS`, lower the ratchet.

**Acceptance.** Per tranche: 500 rows with five distinct sentences per
theme, no "— at" suffix, no id change, ratchet lowered by 500.

**Verify.**
```bash
python3 tools/generate_pack.py data/pack_specs/<pack>.json --check
python3 tools/normalize_blocks.py && python3 tests/test_platform.py
```

---

## 3 — The 6,200 empty descriptions, filled through promotions — DONE *(tranche one — Future-Work — done in v0.90.0, 111 rows; tranche two — Civic & Leadership and Language, Culture & Communication — done in v0.91.0, 222 rows; tranche three — Health & Community — done in v0.92.0, 109 of 111 rows; tranche four — a new `partial_bands` mechanism, and Empathy & Emotional Intelligence — done in v0.93.0, 167 rows; tranche five — Community & Relationship Practice — done in v0.94.0, 167 rows, closing every foundation pack reachable by `unbanded`/`partial_bands`; tranche six — the grade filter extended from `BAND_LEVEL` to `GRADE_LEVEL` and K–12's 64 rows filled through `unbanded` — done in v0.95.0; tranche seven — Trade School's 47 rows filled the same way — done in v0.96.0; tranche eight — Regional's 111 rows filled the same way, with the `unbanded` distinctness check scoped to themes rather than rows — done in v0.97.0; close-out — Health & Community's last 2 grade-`—` rows filled, closing every pack reachable by `unbanded`/`partial_bands` — done in v0.98.0; final piece, pilot pack — Sapient OS's 620 rows filled through `unbanded`, `apply_promotions()` fixed to merge multiple promotion files per pack — done in v0.99.0; final piece continued — Robotics OS's 640 rows filled, 120 of 378 themes reused verbatim from Sapient OS's dictionary — done in v0.100.0; final piece continued — Global Health OS's 660 rows filled, 112 of 349 themes reused from the shared dictionary — done in v0.101.0; final piece continued — Multilateral OS's 650 rows filled, 156 of 352 themes reused — done in v0.102.0; final piece continued — Non-Profit Practice's 650 rows filled, 168 of 348 themes reused — done in v0.103.0; final piece continued — Education OS's 660 rows filled, 168 of 336 themes reused — done in v0.104.0; final piece continued — Science OS's 660 rows filled, 185 of 394 themes reused — done in v0.105.0; final piece, last pack — Corporate OS's 660 rows filled, 211 of 415 themes reused — done in v0.106.0, closing prompt 3 entirely: the dataset carries zero empty descriptions, and the shared generic-action dictionary built across the eight `unbanded` sector-OS/Education OS packs holds 1,809 sentences)*

**Wrinkle found in v0.92.0, resolved in v0.93.0.** Empathy & Emotional
Intelligence and Community & Relationship Practice (167 rows each) do
not fit the `unbanded` mechanism used for tranches one through three:
each of their 55 themes recurs across three or four grades in an
irregular, sometimes wrap-around pattern — never all five bands (so
the original `bands` fill doesn't apply) and never exactly one row (so
`unbanded` doesn't either). v0.93.0 added a third promotion kind,
`"partial_bands": true`, filling each grade a theme actually has from
that theme's own per-grade sentence, and used it to author Empathy &
Emotional Intelligence. Community & Relationship Practice (the same
pattern) is the next tranche. K–12, Trade School, Regional, and Health
& Community's two `—`-grade rows remain out of scope until
`apply_promotions()`'s grade filter is extended from `BAND_LEVEL` to
`GRADE_LEVEL`.

**Why.** 36% of rows have no description at all: 5,200 in the sector-OS
packs and 1,000 in the nine foundation packs (K–12, Trade School,
Future-Work, Regional, Civic, Health, Language, Empathy, Community). A
learner opening one sees a code, a level and a transfer check. Filling
empty fields is what promotions are for; no override is needed.

**Wrinkle found in v0.90.0.** Within Future-Work, Civic & Leadership,
Language Culture & Communication, Empathy, Community & Relationship
Practice, and most of Health & Community, each theme names exactly one
row at one grade — not five rows spanning the band ladder like the
community packs from prompt 2. The plain fill-empty fallback would
append a "— at ‹band›" suffix, recreating the exact content debt prompt
2 just eliminated. `tools/normalize_blocks.py` gained a small, tested
extension: a promotion may declare `"unbanded": true`, filling a
one-row theme's description as a single complete sentence with no
suffix, and skipping `track`/`code` fill (those would create a track
shape that fails the 50-block invariant in `tests/test_platform.py`
`test_dataset()`; `light_fill()` still assigns `code` and `level`
structurally, as before). K–12, Trade School, Regional, and Health &
Community's two "—"-grade rows use single grades or adult bands rather
than the five standard bands and are not yet reachable by this
mechanism or the original one — a follow-up tranche.

**Evidence.** `docs/DATA_QUALITY.md` (Desc % = 0% on the foundation
packs; 43% on the sector OS); `data/promotions/basic-life-skills.json`
(a promotion carrying `bands`).

**Steps.** Foundation packs first (1,000 rows, the ones every learner
meets), one promotion file per pack, sentences authored per theme and
band from the transfer check that already exists on the row; then the
sector-OS empties by pack. Never touch a non-empty field.

**Acceptance.** Desc % rises pack by pack; the normaliser reports zero
overwrites; no id changes; both suites pass.

**Verify.**
```bash
python3 tools/normalize_blocks.py --report && python3 tools/data_quality.py
```

---

## 4 — One shared runtime for the voice and tour helpers — DONE in v0.107.0

**Why.** `chooseVoice`, `say`, `tourShow` and `tourEnd` are defined
separately in four templates (Flow Hub, Louisiana, States, Trades
Network; 2.0–3.7 KB each), and `route` in five. The studio and XR
engines already show the pattern: one file under `tools/`, injected by
`tools/runtime_lib.py`. A fix to how the Guide speaks lands in one copy
today.

**Evidence.** `grep -c "function say(" apps/*/template.html`;
`tools/runtime_lib.py` (`body_snippet`).

**Steps.** Move the four helpers to `tools/voice/engine.js` as `CXVOICE`
with the same signatures; inject after the studio engine; each template
keeps a one-line alias. Prove behaviour with the browser suite's
existing voice and tour checks before and after.

**Acceptance.** One definition of each helper in the repository; every
template shrinks; the browser suite's voice and tour assertions pass
unchanged; the footprint budgets hold.

**Finding, v0.107.0.** Only `chooseVoice` and `say` were actually
duplicated — byte-identical logic (the three-persona table, the
speechSynthesis preference list, the sentence-by-sentence utterance
drift) modulo the `localStorage` key each app reads. `tourShow` and
`tourEnd` are not: each app's guided tour is a genuinely different
implementation (own DOM strategy, own navigation — `go(view)` versus
`location.hash` behind a 120/220/240ms `setTimeout`, own CSS class and
accent color) that happens to share a function name. Forcing them into
one shared function would trade real behavior-preservation risk for a
cosmetic line count, so only `chooseVoice`/`say` moved to
`tools/voice/engine.js` as `CXVOICE`, injected after the studio engine
in `tools/runtime_lib.py`'s `body_snippet()`; each template keeps a
one-line alias, and the voice-picker `change` handler now also calls
`CXVOICE.setMode(...)`. Dead, write-only `voiceOn` state (assigned,
never read, in Flow Hub and Louisiana) was dropped in the same change.
Also found: the browser suite has no dedicated voice or tour
assertions to hold unchanged (the acceptance criterion above assumed
some existed) — verified instead with a live-page Playwright check
across all four apps confirming `window.CXVOICE` loads with no page
errors and that driving `#voicepick`'s real `change` event updates
`CXVOICE.getMode()`. Four templates shrink by 140 lines (26 added);
both suites pass unchanged (1,919 Python checks, 223 browser
assertions).

**Verify.**
```bash
for a in flow_hub louisiana states trades; do python3 tools/build_$a.py; done
NODE_PATH=$(npm root -g) node tests/browser/smoke.js
```

---

## 5 — A faster browser suite, evenly spread, with the audit in CI

**Why.** The browser suite is 223 assertions in 135 s, run one page at a
time; the Platform app is opened twice and the Education OS three times
against the Louisiana app's twenty; the accessibility audit (47 views,
~4 min) runs only when someone runs it, so a template regression would
reach `main`.

**Evidence.** `tests/browser/smoke.js` (serial `await` chain);
`grep -c "url('platform')" tests/browser/smoke.js`;
`.github/workflows/validate.yml` (no audit step).

**Steps.** Run the suites per app in parallel contexts of one browser;
add Platform and Education OS suites that exercise their routes and
widgets to the depth the Louisiana suite has; add the audit as a CI job
on changes under `apps/` and `tools/`, comparing to the committed
`docs/ACCESSIBILITY.json`.

**Acceptance.** Browser suite under 60 s with the same assertions;
every app opened at least five times; the audit runs in CI and fails on
a WCAG-tagged violation.

---

## 6 — Signed releases, once a key exists

**Why.** `tools/release_tags.py --backfill` (v0.71.0) recreates the 71
missing release tags, but the automation token cannot push tags (403 on
`refs/tags`), so CI only warns until a maintainer pushes them; checksums
and the SBOM are regenerated per push. None of it is signed: a hall
verifying a download can prove it matches the repository but not who
published it.

**Evidence.** `docs/COMPLIANCE_ROADMAP.md` ("signed release tags once a
signing key is provisioned"); `SECURITY.md`.

**Steps.** A maintainer runs the backfill and pushes the tags, then the
CI step becomes a hard failure. A key ceremony for the foundation (an
SSH signing key or minisign key held offline, public half committed);
`git tag -s` from then on; `tools/checksums.py` writes a detached
signature; the verification steps documented in `SECURITY.md` in a
hall's terms.

**Acceptance.** `git verify-tag` passes on the next release; the
checksum signature verifies with the committed public key; the register
row moves to met.

---

## 7 — The Education OS template's second diet — DONE, v0.108.0–v0.109.0

**Why.** The template is 4.6 MB after v0.63.0 and v0.68.0. Its two
largest remaining literals, `DATA.siteIndex` (296 KB) and
`DATA.platformConformance` (152 KB), are content that should be
canonical files with a round trip, like the eight layers already
injected.

**Evidence.** `docs/PERFORMANCE.md` §"left alone";
`tools/build_education_os.py` `FACT_LAYERS`.

**Steps.** Extract both to `data/education_os/` with
`tools/extract_fact_bases.py`, add placeholders, inject at build,
`--check` in CI; run `tools/view_sweep.js` before and after and require
zero real differences.

**Acceptance.** Template under 4.2 MB; 149 views hash-identical after
normalisation; the extractor round-trips in CI.

**Finding, v0.108.0.** `DATA.platformConformance` no longer exists as a
data literal — somewhere since this prompt was written it was
refactored into a live-computed function
(`function platformConformance(){...}`, a self-check that reads the
DOM, not content). Measuring every top-level `DATA.<name>=` literal by
its actual matched-bracket byte span (not by distance to the next
assignment, which double-counts intervening code) found the real
ranking: `siteIndex` (296 KB, confirmed), then `seEditions` (54 KB,
the Special Editions content — not 152 KB), then `buildStatus` (~50
KB), `fxPack2` (~48 KB), `fxAuthored` (~47 KB). `siteIndex` and
`seEditions` were extracted this tranche via the existing
`__CXFACT:<name>__` mechanism: template 4.62 MB → 4.27 MB (−350 KB),
short of the 4.2 MB target. The next three (~145 KB combined) would
close the gap but are unexamined content whose consuming code wasn't
read this tranche — left for a follow-up rather than extracted
sight-unseen. Verified with `tools/view_sweep.js`: 9 of 149 views
differed at first, but a control sweep (the same unchanged rebuilt
file against itself, twice) reproduced the identical 8 of those 9,
proving pre-existing non-determinism (live timestamps, simulated
data) rather than a regression; the ninth was a one-off timeout in
the baseline run.

**Close-out, v0.109.0.** The remaining three literals — `buildStatus`
(the Release Plan table, 49.8 KB), `fxAuthored` (the authored
Future-Work track content, 47.3 KB) and `fxPack2` (the second
Future-Work pack, 47.9 KB) — read cleanly as pure runtime content
consumed only by client-side JS (a table renderer, and the app's own
`fxPackMerge()`), with no Python build tooling touching them; safe to
extract through the same mechanism as `siteIndex`/`seEditions`. Each
now lives in `data/education_os/` and is injected in place at
`__CXFACT:<name>__`. One dead line was found and removed in the
process: `DATA.fxAuthored=DATA.fxAuthored||{}` inside `fxPackMerge()`
was a defensive fallback for a load order where the literal might not
have run yet — now that the value is always injected before this
script block, the fallback can't fire and was deleted rather than
kept. Template: 4.27 MB → 4.13 MB, under the 4.2 MB target. Verified
with `tools/view_sweep.js`: 8 of 149 views differed before/after, and
a control sweep of the *after* build against itself reproduced the
identical 8 — the same pre-existing non-determinism this prompt found
last tranche, not a regression. Both suites pass (1,934 Python checks,
223 browser assertions); `tools/extract_fact_bases.py --check` round
trips clean for all twelve fact-base layers.

**Verify.**
```bash
node tools/view_sweep.js apps/education-os/index.html before.json
python3 tools/build_education_os.py && node tools/view_sweep.js apps/education-os/index.html after.json
node tools/view_sweep.js --compare before.json after.json
```

---

## 8 — XR round three: stations against the room, AR placement

**Why.** A loaded room (v0.70.0) is drawn under stations that still stand
in the fixed arc; on a phone in AR the stations stand at a fixed
distance rather than on a surface the person chose. Both are views;
neither changes what a run is.

**Evidence.** `tools/xr/engine.js` (`CXXR.scene`, R = 2.4 arc;
`loadRoom`); `docs/XR_REVIEW.md` §5.

**Steps.** From the loaded room's triangles derive the floor extent and
the nearest wall segments; place stations along the walls when a room
is present, arc otherwise; request `hit-test` as an optional feature in
AR sessions only, place the scene at the first `select` hit, and drop
the hit result like the pose. Still no hand, eye or face tracking; the
register's PL-21 text extended.

**Acceptance.** Node test: a room with a known box places stations on
its walls; the no-room path is byte-identical; the privacy paragraph
and PL-21 mention hit-testing as per-frame and dropped.

---

## 9 — The board's decisions as data — DONE, v0.110.0

**Why.** The 24 proposed credential names are applied as a counted
exception and marked *proposed*; the board packet lists them as its
first decision; 33 rows still carry *Practitioner*. Adoption today would
mean editing prose in several documents. It should be one file.

**Evidence.** `docs/BOARD_PACKET.md`; `data/promotions/` (the credential
correction); `docs/DATA_REVIEW.md` Finding 6.

**Steps.** A `cx-boarddecision/1` file (`data/policy/decisions.json`):
decision id, date, motion, outcome, who signed. The normaliser applies
the credential names only when a decision adopts them; the board packet
and the data-quality dashboard read the file; `tools/cohort_report.py`
lists open decisions.

**Acceptance.** With no adopted decision nothing changes; with a fixture
decision the 33 rows resolve and the level-word count is zero; the
packet shows the decision's status.

**Finding, v0.110.0.** The spec's own two acceptance halves turned out to
be in tension: the 24 tracks' correction has been applied *unconditionally*
in the pipeline since v0.52.0, so gating it retroactively on an "adopted"
outcome would silently revert 1,195 rows the moment this shipped (no real
board has met to adopt anything). Resolved by scoping the decision id to
the promotion, not the mechanism: `data/promotions/*.json` tracks may now
name a `"decision"` id; `tools/normalize_blocks.py`'s new
`credential_decision_ready()` gates the correction on that id being
recorded as `"adopted"` in `data/policy/decisions.json` (`cx-boarddecision/1`,
new) — but a track naming no id (all 24 existing ones) is unaffected and
applies exactly as before. `data/policy/decisions.json` records `BD-1`
(the 24-name correction, outcome `proposed`, for-the-record only) and
`BD-2` (the Empathy & Emotional Intelligence "Emotions at Work" group's
33 rows, outcome `open` — the two-way shape choice from Finding 6's "What
remains", not a drafted name: naming it here would pre-empt a curriculum
decision this prompt doesn't own). "With a fixture decision the 33 rows
resolve" is proven the honest way — `tests/test_platform.py` exercises
`credential_decision_ready()` directly with fixture ids, and a live
assertion (`load_decisions()` returns nothing adopted in the committed
file) pins "with no adopted decision nothing changes" as a real, checked
fact rather than a one-time claim. `docs/BOARD_PACKET.md`,
`docs/DATA_QUALITY.md` (new "Board decisions" section) and
`tools/cohort_report.py` (new "Open board decisions" section) all read
the one file instead of carrying their own prose. Both suites pass
(1,946 Python checks, 223 browser assertions); `blocks.csv` is
byte-for-byte unchanged.

---

## 10 — Accessibility round two

**Why.** The automated result is clean at 47 views, and the four things
the audit cannot do are still undone: a screen-reader pass, the four
non-default styles view by view, the Education OS beyond its 8 sampled
views, and the 23 "needs review" contrast items on gradient backgrounds.

**Evidence.** `docs/ACCESSIBILITY.md` "What remains".

**Steps.** Run the audit over every Education OS view (extend
`tools/a11y/audit.js` to read the app's VIEWS table); audit each style;
measure the 23 contrast items with a pixel sampler; script a
screen-reader pass with a checklist per app, recorded by a person.

**Acceptance.** `docs/ACCESSIBILITY.json` covers 149 + 39 views and five
styles with zero WCAG-tagged violations; the 23 items are measured and
either fixed or documented with their ratios; the screen-reader
checklist is in the doc with its date and who ran it.

---

## How these were chosen

Prompts 1–3 are the largest numbers in the repository and the only ones
that need a decision before work can start. Prompts 4–6 are hygiene that
stops drift and cost little. Prompts 7–10 are the next step of work
already begun. None of them is the v1.0 gate; that waits on a named
cohort and an educator who has read the curriculum, and no prompt
substitutes for either.
