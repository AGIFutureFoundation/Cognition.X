# Complete System Review, round two — Cognition.X at v0.70.0

*Reviewed 2026-09-17, covering releases v0.33.0 → v0.70.0 (38 releases,
73 merged pull requests, every one CI-green). The first review
(`SYSTEM_REVIEW.md`, v0.32.0) and its ten prompts
(`NEXT_STEPS_OPUS5.md`, all complete) are the baseline. This review says
what was measured, what it found, what was fixed in v0.71.0 because it
was cheap and verified, and what goes to the next ten prompts
(`NEXT_STEPS_2.md`). Every number below was produced in the review; the
ones that can drift are held by `tests/test_platform.py`.*

---

## 1. The dataset and pipeline — sound, with its debt named and counted

**17,450 blocks · 47 packs · 225 tracks · 1,430 credentials** (1,431
distinct strings; one is the level word *Practitioner* on 33 trackless
rows, awaiting the board's decision on the 24 proposed names).

- **Every invariant from the first review still holds:** block ids never
  reused, non-empty source fields never overwritten (the credential
  correction is the one counted exception), every app rebuilt in CI and
  compared byte for byte, `docs/DATA_QUALITY.md` regenerated on every
  push.
- **The content debt, exactly:** 6,200 rows (36%) have no description —
  5,200 in the seven sector-OS packs and 1,000 in the nine foundation
  packs — and 9,750 rows (56%) carry one sentence per theme with a
  band suffix, across 32 packs. Prompt 6 of the first set authored the
  core spine (1,500 rows, five packs, distinct sentences per band); the
  ratchets `KNOWN_BAND_SUFFIX_ROWS = 9750` and `BAND_AUTHORED_PACKS`
  stop either number going the wrong way.
- **Finding, fixed:** the data-quality headline counted distinct strings
  (1,431) where the wiki counted real credentials (1,430). It now counts
  real credentials.
- **Finding, deferred to prompt 1:** 3,457 of the suffixed rows are in
  the sector-OS packs, whose source descriptions are *non-empty*. The
  fill-empty rule that protects the dataset means authored band
  sentences cannot reach them without a designed, counted override —
  the same shape as the credential correction, but 100× larger. That
  design decision is the prompt, not the authoring.

## 2. The six apps — build products, verified, budgeted

| App | Bytes | Budget | First content | Runtime injected |
|---|---:|---:|---:|---|
| education-os | 6.15 MB | 6.5 MB | 459 ms | studio + XR engines, 8 canonical layers |
| flow-hub | 2.44 MB | 2.6 MB | 178 ms | studio + XR |
| louisiana | 0.93 MB | 1.0 MB | 233 ms | studio + XR, precomputed Voronoi |
| platform | 0.26 MB | 0.3 MB | 99 ms | studio + XR |
| states | 0.60 MB | 0.65 MB | 129 ms | studio + XR |
| trades-network | 0.46 MB | 0.5 MB | 143 ms | studio + XR |

(Bytes at v0.70.0; times from `docs/PERFORMANCE.md` at v0.68.0 plus the
25 KB XR engine, inside every budget.)

- **Reproducible:** `tools/build_*.py` from `template.html` + `data/`,
  compared in CI. A strict Content-Security-Policy in every app; fonts
  embedded; no request leaves any page. The Education OS is built from
  eight canonical layers injected in place (`__CXFACT:*__`) and the
  extractor round-trips them in CI.
- **Finding, fixed:** the claim that "every one of the 149 views renders
  identically" (v0.63.0, v0.68.0) was made with a sweep script that
  lived outside the repository. It is now `tools/view_sweep.js`, with
  the nondeterminism it must ignore written into it.
- **Finding, deferred to prompt 4:** four templates (Flow Hub,
  Louisiana, States, Trades Network) each carry their own copy of the
  voice and tour helpers (`chooseVoice`, `say`, `tourShow`, `tourEnd`:
  2.0–3.7 KB per app) and five carry `route`. The cost is not bytes; it
  is that a fix lands in one copy. The studio and XR engines already
  show the shape of the answer: one file under `tools/`, injected by
  `tools/runtime_lib.py`.
- **Finding, deferred to prompt 7:** the Education OS template is still
  4.6 MB, of which `DATA.siteIndex` (296 KB) and
  `DATA.platformConformance` (152 KB) are the two largest literals not
  yet canonical files.

## 3. Tests and CI — broad, fast, unevenly distributed

| Suite | Checks | Time | In CI |
|---|---:|---:|---|
| `tests/test_platform.py` | 1,640 | 8 s | yes |
| `tests/browser/smoke.js` | 223 | 135 s | yes |
| `tools/a11y/audit.js` | 47 views | ~4 min | no — committed result checked |
| Validators, extractors, reports | — | < 30 s | yes (23 steps) |

- **Finding, deferred to prompt 5:** the browser suite runs one page at a
  time; a per-app parallel run would cut it to ~40 s. Its coverage per
  app is uneven — the Louisiana app is opened 20 times, the Platform app
  twice and the Education OS three times — and the accessibility audit
  runs only when someone runs it.
- **What the tests now hold that they did not at v0.32.0:** the byte
  budgets, the accessibility result, the register's counts, the
  simulation and XR engines' no-network / no-storage / no-randomness
  properties, the credential at exactly 50 witnessed checks, the
  per-band ratchets, the canonical round trip, and (from v0.71.0) the
  review's own numbers and the release-tag procedure.

## 4. Security, privacy and the register

**45 controls — 29 met, 16 partial, 0 open.** Every partial control is
one whose evidence is an act by a hall or a district (a signed sheet, a
permit, a fire inspection, a data agreement) that the software carries
on the hall checklist and exports in the custody bundle, and that no
release can close from the repository. That is the honest ceiling for
software, and the register says so on each row.

- **Held by test:** CSP in every app, no third-party request, the
  Records Office key non-extractable, checksums and the CycloneDX SBOM
  regenerated in CI, the privacy notice's XR paragraph, the hosting
  headers, no hand, eye or face tracking requested.
- **Finding, half fixed:** `docs/wiki/Versioning-and-Releases.md` step 3
  says every release is tagged `vX.Y.Z` on its merged commit. One tag
  existed (v0.3.0) for 70 releases. `tools/release_tags.py --backfill`
  now recreates the 71 missing annotated tags on the commits that
  introduced each version, and `--check` runs in CI. Pushing the tags
  needs a maintainer: the automation token that ships releases is
  refused (HTTP 403) on `refs/tags`, so CI warns rather than fails
  until they are pushed. Signing them waits on a key (prompt 6).
- **Unchanged by design:** single-browser state with export, restore and
  the custody bundle; no server; no sync. Continuity across devices is
  the bundle carried by hand.

## 5. Accessibility

Re-run in this review over **47 views** (the 45 of v0.53.0 plus the
Simulation Studio open on a scenario and the same studio with its WebXR
room open): **0 WCAG-tagged violations, 5,309 focusable elements, 0
without a name, 0 click-only controls.** The 3D panel's controls, file
input and canvas are all named; the only finding anywhere is the
documented `heading-order` best-practice deviation (38 nodes).

What remains is unchanged and written down in `docs/ACCESSIBILITY.md`:
no screen-reader pass, the four non-default styles not audited view by
view, the Education OS sampled at 8 of 149 views, 23 axe "needs review"
items on gradient backgrounds. Prompt 10.

**Update, v0.113.0 (prompt 10).** Re-run over the Education OS's full
route table and all five styles: **304 views**, 0 WCAG-tagged violations,
42,767 focusable elements, 0 without a name, 0 click-only controls. A new
pixel sampler measured the "needs review" contrast items mechanically
(375 nodes across 259 flagged instances) instead of leaving them
spot-checked by hand; it found 22 genuinely below threshold, all three
token- or icon-size-level bugs, all fixed. What remains, unchanged: no
screen-reader pass — it needs a person, and `docs/ACCESSIBILITY.md` now
carries a dated, unsigned checklist rather than a fabricated result.

## 6. Performance

Measured and budgeted in v0.68.0 (`docs/PERFORMANCE.md`); nothing has
moved since beyond the XR engine's 25 KB. The Education OS went from
9.54 MB to 6.12 MB and the Louisiana app's first content from 468 ms to
233 ms. The tests hold every app under its budget. The next real gains
are the Education OS literals in §2 and nothing else worth its risk.

## 7. Documentation

- **Findings, fixed:** `docs/ROADMAP.md` still listed as open the WCAG
  audit (done v0.53.0), the Education OS design restoration (v0.46.0),
  the canonical-layer injection (v0.63.0) and the VC envelopes (v0.60.0);
  `docs/XR_REVIEW.md` gave the engine as ~400 lines (it is ~460);
  `docs/COMPLIANCE_REVIEW.md` and the investor brief cited the 45-view
  audit without the re-run. All corrected. `docs/NEXT_STEPS_OPUS5.md` is
  marked complete.
- **Structure holds:** every generated document says it is generated and
  CI fails on drift; every compliance document carries *not legal
  advice*; the wiki's numbers line is held to the dataset by test.

## 8. Cross-cutting risks

1. **The v1.0 gate waits on people, not code.** The board packet, the
   consent sheet, the key exchange and `tools/cohort_report.py` exist;
   no named external cohort has yet completed credentials on an
   unmodified release, and no educator has read the curriculum end to
   end. Nothing in the next ten prompts substitutes for that.
2. **The board has not decided.** The 24 credential names are proposed;
   until adopted, 33 rows carry a level word and the pipeline's counted
   exception stays open. Prompt 9 makes the decision a data file so that
   adoption is a commit, not a rewrite.
3. **Content debt is the largest number in the repository** (6,200 empty,
   9,750 suffixed), and the fill-empty rule means the largest part of it
   needs a design decision before authoring can start (§1).
4. **Duplicated helpers drift silently** (§2). Not a user-facing defect
   today; the class of defect the first review warned about.
5. **The audit is manual** (§3). A regression in a template would reach
   `main` and be caught only when someone re-runs it.

## 9. Verdict

The platform does more than it did at v0.32.0 and claims nothing it
does not do: one validated dataset, six regenerable and budgeted apps,
a shared studio and XR runtime, offline signed credentials in two
formats, a register with no open software controls, an accessibility
result held by test, and a documented, executable gate to v1.0. The
scaffolding is still labelled as scaffolding. The recommended order of
work is in `NEXT_STEPS_2.md`: the override design and the description
debt first, because they are the largest numbers and the only ones that
need a decision; the runtime, suite and tag hygiene next, because they
are cheap and stop drift; the Education OS diet, XR round three, the
board's decisions as data, and accessibility round two after that.

Not legal advice. A simulation is practice. A credential is issued at
exactly fifty witnessed checks and nothing else.
