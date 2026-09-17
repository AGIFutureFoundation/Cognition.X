# Accessibility audit — WCAG 2.2 AA

*Prompt 4 of the ranked next steps. First full audit: v0.53.0 (2026-09-15);
re-run at v0.71.0 (2026-09-17) with the Simulation Studio and its WebXR
room added as views. Re-run any time with `node tools/a11y/audit.js`; the
committed result is [`docs/ACCESSIBILITY.json`](ACCESSIBILITY.json) and
`tests/test_platform.py` fails if it carries a WCAG-tagged violation.*

**At v0.71.0: 47 views, 0 WCAG-tagged violations, 5,309 focusable
elements, 0 without a name, 0 click-only controls.** The two views added
are the studio open on a scenario and the same studio with *Open in 3D /
VR* pressed: the 3D panel's buttons, file input and canvas all carry
names, the canvas is described, and the only finding on either is the
documented `heading-order` deviation below (38 nodes across the run).

## What was tested

- **Automated rules.** axe-core 4.13.0 with the `wcag2a`, `wcag2aa`,
  `wcag21a`, `wcag21aa`, `wcag22aa` and `best-practice` tags, run over
  **45 views**: every hash route of the Louisiana, States and Platform apps
  (the Louisiana *Dashboards* view once per role, seven times), every
  in-app view of Flow Hub and the Trades Network, and eight sampled views
  of the 149-view Education OS. Default style (*Enterprise*), light and
  dark themes for the contrast pass.
- **Keyboard sweep** (same runner): every focusable element per view is
  counted and checked for an accessible name (aria-label, labelledby,
  text, title, placeholder or an associated label); click-only `div`/`span`
  controls are counted. Totals: **4,849 focusable elements, 0 without a
  name, 0 click-only controls.**
- **Focus survival under re-render.** Verified in v0.47.0 and held by the
  browser suite: `focusMark()/focusRestore()` around every full
  re-render; the Network OS (20 s) and swarm (10 s) pulses skip any board
  containing `document.activeElement`.

## What was found, and fixed

The first run reported **1,182 colour-contrast nodes, 82 target-size, 16
nested-interactive, 12 select-name, 4 scrollable-region-focusable and 36
heading-order** findings. Almost all of the contrast failures traced to a
handful of tokens, so the fixes are token-level in the templates (build
products are never edited):

| Finding | Cause | Fix |
|---|---|---|
| `color-contrast` × ~1,000 | `--faint` (#7E8898 light / #768290 dark) at 3.3–4.2:1 on the page grounds, in the four platform-standard apps | `--faint` → #5F6B7A light (≥4.6:1 on white, bg and surface-2) / #8B97A6 dark (≥4.8:1); the Classic/Bayou style variants likewise |
| `color-contrast` (chips, eyebrows) | `--gold` #946900 as text on gold-soft at 4.3:1 | `--gold` → #7F5A00 (≥5.4:1); Classic gold → #9A6210 |
| `color-contrast` (dark Guide button, dark badges) | white text on the dark theme's light gold (#C9A24B, 2.4:1) | `--on-gold` token: gold buttons take ink text in dark themes |
| `color-contrast` (wave chips, region badges) | white on region colours `--w1..w4` at 3.5–4.4:1 | region colours darkened until white reads ≥4.6:1 in both themes (`#2A835B`, `#BA5637` light; `#4970BC #32815F #9460B0 #B05C42` dark); same palette in Flow Hub |
| `color-contrast` (Flow Hub) | `--faint`, `--accent` #B87514 as text (3.1–3.8:1) | `--faint` → #5F6A85 / #8C96AB; `--accent` → #9A6210 (accent buttons keep white text at 5.1:1) |
| `color-contrast` (States compliance tiers) | white on the lens colours for *moderate*, *baseline*, *exempt* | tier colours → #8A6210, #5F6B7A, #257A54 (≥5.3:1) |
| `color-contrast` (Education OS) | the app's own CSS paints ids and codes `#b8860b` (3.0:1) | the generated shell overrides that colour with the brand's `--gold-ink` for `.mono` in tables, summaries and cards |
| `color-contrast` (Makers' Hall chips) | `opacity:.75` on the maker count | opacity removed |
| `target-size` × 82 | the dashboard ◀ ▶ reorder buttons had no minimum size | `min-width/height: 24px` (WCAG 2.2 · 2.5.8) |
| `nested-interactive` × 16 | tile maps and city maps were `role="img"` while containing `role="button"` tiles; Louisiana module-plan `<summary>` held buttons | maps are `role="group"` with the same label; set-aside / remove buttons moved out of the summary into the details body |
| `select-name` × 12 | selects generated inside widget `innerHTML` without labels (`ppick`, `custpick`, `ls-me`, `ls-track`, `fs-track`, `lc-band`, `lc-track`, `rt-unit`, `lp-child`, `ro-pick`, `rh-band`; Trades `uregion`/`ukind`; States `sregion`) | `aria-label` on each; the shared `parishSelect()`/`bandSelect()` helpers name every select they emit |
| `scrollable-region-focusable` × 4 | Platform `.artifact` output boxes; Education OS `.tablewrap` and `#fg-out` | Platform boxes are `tabindex="0" role="region"`; the Education OS shell marks any region that actually scrolls focusable after each render |

Result after the fixes: **0 WCAG-tagged violations across all 45 views**,
light and dark.

## What remains, and why

- **`heading-order` (36, best-practice, not a WCAG success criterion).**
  Every view is one `<h1>` followed by panels whose headings are `<h3>`
  (and `<h4>` on state cards); axe expects an `<h2>` in between. The
  outline is consistent — view title, then component headings — and
  changing the component heading level would touch several hundred
  generated strings for no reading benefit. Left as a documented
  deviation; a future pass could restyle `.panel h3` as `h2`.
- **axe “needs review” items (23).** Mostly `color-contrast` on elements
  with gradient or image backgrounds (title cards, the Voronoi canvas)
  that axe cannot compute. Spot-checked by hand in v0.46.0 (≥4.5:1);
  not re-measured mechanically here.
- **Non-default styles.** The Parade, Classic, Bayou and Gallery style
  variants were token-fixed for `--faint` and `--gold` but not audited
  view by view; the audit runs the Enterprise default.
- **Screen-reader pass.** This audit is mechanical plus a keyboard
  sweep. A human pass with NVDA/VoiceOver has not been done; live regions
  (`#ro-result`, the toast, the assessor queue) are wired but their
  announcement behaviour has only been checked by reading the markup.
- **The Education OS** was sampled (8 of 149 views); the shell fixes
  apply everywhere, but the unsampled views may carry their own
  app-CSS colours.
- **The 2024 ADA Title II rule** (WCAG 2.1 AA for public entities from
  April 2026/2027) is met on the automated criteria above; a procurement
  should still commission an external audit — the compliance layer
  budgets one.

## How to re-run

```
node tools/a11y/audit.js            # every app → docs/ACCESSIBILITY.json
node tools/a11y/audit.js louisiana  # one app (does not replace the committed file — commit only full runs)
python3 tests/test_platform.py      # holds: zero WCAG-tagged violations, every control named
```
