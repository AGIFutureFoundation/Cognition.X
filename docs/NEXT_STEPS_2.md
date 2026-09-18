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

## 2 — The community packs' band sentences, by pack importance *(tranche one — SmartCiti.X New Orleans Trades and the States OS — done in v0.79.0; tranche two — Trades in the Classroom and Trades Across School Subjects — done in v0.80.0; tranche three — Music, Culinary Trades and Arts, Making Media & Performance — done in v0.81.0; tranche four — Digital Life and Law — done in v0.82.0; tranche five — Preventive Health & Everyday Care and Care Across a Life — done in v0.83.0; tranche six — Water, Land & Climate and Making, Repair & Reuse — done in v0.84.0; tranche seven — Arts & Craft Trades : Louisiana Makers and Energy, Grid & the Home — done in v0.85.0, 3,750 rows so far; `tools/author_bands.py` for the remaining life-skills packs — the three Civic Leadership Legacy packs, Food Cooking & Nutrition, Learning States & Universal Access, and Transport & Mobility are pack-spec-based and take bands directly with no override, the same as this tranche; Housing & Tenancy, Money Benefits & Entitlements, Reentry & Recovery Pathways and Neighbourhood Safety & Civic Voice will need a new promotion file with the `override: band-suffix` mechanism instead, since their track and description are already non-empty in the raw source)*

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

## 3 — The 6,200 empty descriptions, filled through promotions

**Why.** 36% of rows have no description at all: 5,200 in the sector-OS
packs and 1,000 in the nine foundation packs (K–12, Trade School,
Future-Work, Regional, Civic, Health, Language, Empathy, Community). A
learner opening one sees a code, a level and a transfer check. Filling
empty fields is what promotions are for; no override is needed.

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

## 4 — One shared runtime for the voice and tour helpers

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

## 7 — The Education OS template's second diet

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

## 9 — The board's decisions as data

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
