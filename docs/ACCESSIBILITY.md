# Accessibility audit — WCAG 2.2 AA

*Prompt 4 of the first ranked next steps. First full audit: v0.53.0
(2026-09-15); re-run at v0.71.0 (2026-09-17) with the Simulation Studio and
its WebXR room added; round two at v0.113.0 (2026-09-19) — prompt 10 of
`docs/NEXT_STEPS_2.md`. Re-run any time with `node tools/a11y/audit.js`; the
committed result is [`docs/ACCESSIBILITY.json`](ACCESSIBILITY.json) and
`tests/test_platform.py` fails if it carries a WCAG-tagged violation.*

**At v0.113.0: 304 runs — the Education OS's full 149-view route table plus
39 views across the other five apps, each of the 39 audited in all five
styles (149 + 39 × 5 = 304) — 0 WCAG-tagged violations, 42,767 focusable
elements, 0 without a name, 0 click-only controls.** Round two closed three
of the four things the v0.71.0 audit could not do on its own: every
Education OS view, every style, and a pixel measurement of the axe "needs
review" contrast items. The fourth — a screen-reader pass — needs a person
and is not done; see "What remains" below.

## What was tested

- **Automated rules.** axe-core 4.13.0 with the `wcag2a`, `wcag2aa`,
  `wcag21a`, `wcag21aa`, `wcag22aa` and `best-practice` tags, run over
  **304 views**: all 149 Education OS routes (read from the app's own
  `VIEWS` table, `tools/a11y/audit.js`'s `educationOsRoutes()`, so the
  count tracks the app rather than a hand-picked sample), and 39 views
  across Louisiana, States, Trades Network, Flow Hub and the Platform app.
  The 29 of those 39 that carry style variants (14 Louisiana, 8 Trades
  Network, 7 States) were each audited in all five styles — *Enterprise*,
  *Parade*, *Classic*, *Bayou*, *Gallery* — the other 10 (Flow Hub,
  Platform) have none. Light theme for the contrast pass, as before.
- **Keyboard sweep** (same runner): every focusable element per view is
  counted and checked for an accessible name (aria-label, labelledby,
  text, title, placeholder or an associated label); click-only `div`/`span`
  controls are counted. Totals: **42,767 focusable elements, 0 without a
  name, 0 click-only controls.**
- **Pixel-sampled contrast.** `tools/a11y/contrast_sample.js` re-runs
  every recorded view, re-derives each axe "needs review" `color-contrast`
  node's real foreground colour from the live page, screenshots it, and
  samples the actually rendered background pixels around it (up to 5 nodes
  per rule instance) — the same method axe itself cannot use, because it
  cannot compute a single background colour for a gradient, image or
  composited element. **375 nodes measured, 0 below their WCAG threshold**
  after the fixes below; 194 more were unresolved (their bounding box fell
  outside the screenshot — mostly content below the fold on views the
  sampler doesn't scroll, or a node that only appears after one of
  `audit.js`'s in-page `steps` closures, which the sampler cannot replay).
- **Focus survival under re-render.** Unchanged since v0.47.0, held by the
  browser suite.

## What was found, and fixed (round two)

The pixel sampler measured 259 axe "needs review" color-contrast
instances (up to 5 nodes each, 375 nodes) and found **22 below their WCAG
threshold**, all tracing to three root causes:

| Finding | Cause | Fix |
|---|---|---|
| `color-contrast` (Trades Network city-map hint labels, × 15 across 5 styles) | `--faint` text drawn over the water overlay's chart-tinted, 18%-opacity fill reads 3.36–3.73:1 against that composited background, not the 4.6:1+ it gets on plain `surface-2` | new `--faint-ink` token (#3C4658 light; identical to `--faint`'s existing dark value, since dark wasn't measured and isn't changing) for this one use, leaving `--faint`'s many other, already-passing uses alone |
| `color-contrast` (Trades Network flipped-cycle diagram, × 5 across 5 styles) | the white "2" on the `--w2` wave circle measured 4.42:1, just under 4.5 | darkened `--w2` to `#257A55` (light only) — the same value already used for the equivalent token in the sibling Louisiana/States apps |
| `color-contrast` (Education OS state-flag icons, MA) | the simplified-flag `sealLight` renderer draws its two-letter code in whichever colour a state's brand array puts third; Massachusetts's array happened to put its light gold accent there, giving 2.28:1 on white | swapped MA's array order to put its navy in that slot, matching how Illinois's and New Jersey's `sealLight` entries already work |
| `color-contrast` (Education OS state-flag icons, NH) | measured 3.55:1, but the underlying colours (white text on navy) compute to ~14:1 — a synthetic test confirmed the drop was anti-aliasing blending the text with a nearby gold ring at the icon's 14–22px render size, not a colour choice | drew every `flagSVG()` call under 28px at 28px instead (5 call sites); re-measured at 0 below threshold |

Re-sampling after every fix confirmed **0 of 375 measured nodes below
their WCAG threshold.**

## What was found, and fixed (round one, v0.53.0)

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

Result after round one: **0 WCAG-tagged violations across all 45 views**,
light and dark. Extended at v0.71.0 to 47 views (the Simulation Studio and
its WebXR room), same result.

## What remains, and why

- **`heading-order` (162), `empty-table-header` (66), `landmark-unique`
  (1) — all best-practice, not WCAG success criteria.** The heading
  deviation is the same one documented since v0.53.0 (view title `<h1>`,
  panel headings `<h3>`, no `<h2>` between — consistent, not worth
  touching several hundred generated strings for no reading benefit). The
  other two are new at this scale and worth a look in a future pass, but
  neither is a WCAG violation.
- **194 pixel-sample nodes unresolved.** Their bounding box fell outside
  the sampler's screenshot — content below the fold, or a node that only
  appears after an in-page `steps` closure (the Trades Network studio/XR
  views) the sampler cannot replay. Not evidence of a problem; just outside
  what this tool measures. A future pass could scroll each flagged node
  into view before sampling.
- **Screen-reader pass — not done.** This audit is mechanical (axe),
  pixel-based (the contrast sampler) and keyboard (the focusable/name
  sweep). No one has run NVDA, JAWS or VoiceOver against these apps. Live
  regions (`#ro-result`, the toast, the assessor queue) are wired but
  their announcement behaviour has only been checked by reading the
  markup. This needs a person; the checklist below is ready for one to
  run, dated and signed when it happens.
- **Dark theme.** All of the above is light theme, as it always has been;
  round-one's dark-theme token fixes were verified by hand at the time,
  not re-measured by either tool here.
- **The 2024 ADA Title II rule** (WCAG 2.1 AA for public entities from
  April 2026/2027) is met on the automated criteria above; a procurement
  should still commission an external audit — the compliance layer
  budgets one.

### Screen-reader checklist (not yet run)

One pass per app: open the view, navigate by heading and by Tab, and
confirm (a) every heading and landmark announces in a sensible order, (b)
every control's name is read before its role, (c) the app's live region
(where it has one) announces a change without moving focus, (d) no
keyboard trap.

| App | View(s) to check | Live region | Date | Run by |
|---|---|---|---|---|
| Louisiana | Dashboards (each role), Simulation Studio + WebXR | assessor queue toast | — not yet run — | — |
| States | Compliance tab, State Curriculum | — | — not yet run — | — |
| Trades Network | Regions (all 5 styles), Flipped Classroom | — | — not yet run — | — |
| Flow Hub | Studio | — | — not yet run — | — |
| Platform | Simulation Studio + WebXR room | — | — not yet run — | — |
| Education OS | `#/states`, `#/compare` | — | — not yet run — | — |
| Education OS | Robotics sector (`#/ed_rob`) | — | — not yet run — | — |
| Education OS | Records Office / credential issue | `#ro-result` | — not yet run — | — |

## How to re-run

```
node tools/a11y/audit.js               # every app → docs/ACCESSIBILITY.json
node tools/a11y/audit.js louisiana     # one app, prints only — never commit this over the full file
node tools/a11y/contrast_sample.js     # pixel-samples the "needs review" items → docs/ACCESSIBILITY_CONTRAST.json
python3 tests/test_platform.py         # holds: zero WCAG-tagged violations, every control named
```
