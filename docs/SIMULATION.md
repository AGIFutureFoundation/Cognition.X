# The Simulation Studio

> **Simulate what is dangerous, expensive or rare; practice live what is
> safe, cheap and common; debrief every run. Nothing energized, suspended
> or moving is practiced live in a classroom studio, and no simulation
> claims to certify. Simulation ≠ certification.**

The studio is the platform's stage-three answer — *Simulate* — built the
way everything else here is built: a canonical fact base, one shared
engine, six hosts, a validator in CI, and the honesty stance carried
verbatim into every run record. Shipped in v0.54.0; it closes the
roadmap's Phase 2 item "mission simulator: promote from demo to
configurable engine driven by pack data".

## What a run is, and is not

A run is a rehearsal of judgement. A learner reads a brief, meets five
decision points in order (plus one or two seeded complications at higher
difficulty), chooses among three options at each, sees the consequence,
and ends in a debrief with the scenario's three questions and a score by
discipline. The run produces a portable `cx-simrun/1` record.

A run is **not** a witnessed check, **not** evidence of competence and
**never** a credential. Every scenario is tied to a real track in
`data/blocks.csv` and carries that track's witnessed transfer check
verbatim — the check is done live, on real material, with an assessor.
The record says so in its own `note`, and its `transfer.done_here` is
always `false`. In the Louisiana app a kept run attaches to the learner
as *practice*; it never touches progress, evidence or the assessor queue,
and the credential threshold is unchanged at fifty witnessed checks.

## The fact base — `data/simulations/scenarios.json`

Format `cx-simulations/1`. **18 scenarios**, 126 decision points, 378
options. Each scenario carries:

| Field | Meaning |
|---|---|
| `id`, `title`, `role`, `brief` | The situation and who the learner is in it |
| `pack`, `track`, `packName` | The real track this rehearses (slug + name, validated against the dataset) |
| `kind` | One of nine trades kinds (`build elec water port transit service civic mech fire`) — localized by the host to a region's publicly known site via `{site}` — or `null` |
| `localize` | A place anchor for the States app (`water corridor table culture storm`) or `null` |
| `site_default` | The site used when a host has nothing better |
| `simulated`, `live` | The studio law applied: what this scenario simulates, what is practised live on the bench |
| `steps` (5), `complications` (2) | Decision points: a prompt and three options, each with text `t`, discipline `d`, score `s` (exactly one 2, one 1, one 0) and a consequence `c` |
| `debrief` (3) | The questions asked at the end |
| `transfer` | `block_id`, `credential` and the transfer check **quoted verbatim** from the dataset, plus the note that the run never credits the ledger |
| `band` | `9–10` for every scenario in this release |

Six disciplines are scored across every scenario:

- **Verify before you act** — test it, measure it, read the tag, prove the meter.
- **Stop-work authority** — anyone can halt the work; halting is never punished.
- **Say it out loud** — announce, confirm back, hand over, write it down.
- **The order is the safety** — lock, then tag, then test; alarm, then fight, then leave.
- **Escalate, do not improvise** — call the person whose job it is.
- **The person in front of you** — welfare is a control, not a courtesy.

The scenarios: the nine trades kinds (a deck edge, lockout at a
substation, a pump station in the rain, a container that is not square,
a yard crossing, a stage load-in, a school boiler room, a lathe with a
missing guard, a small fire), robotics (entering a robot cell, first run
of a new machine), emergency (the collapse in the corridor, seventy-two
hours out), the kitchen (Friday service and the fryer, the delivery that
is warm), civic (the drainage vote), care (the fall at home) and water
(the boil-water notice at school).

## The engine — `tools/sim/engine.js`

One file, injected by every builder at its template's studio placeholder
through `tools/sim_lib.py`. Its stances are held by the tests:

- **Deterministic.** A seed and a difficulty fully decide the plan
  (mulberry32; no `Math.random`). Complications are injected at seeded
  positions, never first and never last.
- **Three difficulties.** 1 Rehearsal (the five steps), 2 Complications
  (one injected), 3 Full drill (both). After a run the engine
  recommends the next difficulty — 85% or better moves up, under 50%
  moves down, otherwise stay — as advice to the learner and the teacher,
  never a gate. This is the Phase 4 "difficulty model" in first working
  form.
- **No timers.** Every step waits for a choice; access profiles need no
  accommodation because nothing races.
- **Accessible.** Options are real buttons, a live region announces each
  consequence, focus moves to each new prompt, everything works at phone
  width.
- **Nothing leaves the page.** The engine never touches the network or
  storage. The host decides what to keep: the Louisiana app keeps
  practice on the learner; the Trades Network keeps only the last run's
  summary; the others keep nothing.

Host API: `CXSIM.configure(factBase)`, `CXSIM.mount(host, scenario,
{site, difficulty, seed, onRun})`, `CXSIM.mountLibrary(host, scenarios,
{siteFor, autoOpen, onRun})`, and the pure functions `localize`, `plan`,
`score`, `nextDifficulty`.

## The six hosts

| App | Where | Localization | What is kept |
|---|---|---|---|
| Trades Network | Simulations view (category × region); every roster card | The region's site for the kind, from the unions fact base | The last run's summary in this browser |
| Louisiana | Student and teacher role widgets | New Orleans or River Region sites for the trades kinds; the parish itself for the rest | Student runs on the learner as `practice` (sanitized on import) |
| Platform | Between stage 2 and stage 3 of the loop | Orleans Parish; the scenario from the demo track's own pack | Nothing — the status line shows the count unchanged |
| Flow Hub | The flow session, when the track carries a scenario; pack detail marks such tracks | The scenario's default site | A line in the session log |
| States | The state page: the nine anchored scenarios | The state's own water, corridor, table, culture and storm memory | Nothing |
| Education OS | Under the quest simulator | Default sites | Nothing |

## Validation

`tools/validate_simulations.py` runs in CI after the dataset validator.
It checks that every scenario's pack and track exist, that the transfer
block belongs to that track and its check text and credential are quoted
verbatim, that every decision point has exactly one best option and that
every discipline is known and used, and that the law and the run note
carry "Simulation ≠ certification". `tests/test_platform.py` holds the
engine's stances and every app's copy of the law; `tests/browser/smoke.js`
plays a run to the debrief in every host and proves that a kept run in
Louisiana changes nothing but the practice list.

## Authoring a scenario

Add to `data/simulations/scenarios.json`, then run the validator. A
scenario needs a real track; a brief that names the role; five steps and
two complications with three options each (one held, one partial, one
missed — the consequence explains why); three debrief questions; the
`simulated` and `live` lists that apply the studio law; and the transfer
block copied from the dataset, never paraphrased. Scenarios go through
the curriculum review board like any pack.

## The studio in space (v0.69.0)

Every scenario can be opened as a room — **Open in 3D / VR** in the
brief, on any decision, or in the debrief. The room is a view of the same
run: the studio still plans, scores and records; the room draws the floor,
the law on a sign, one station per decision point and the current
decision's options as slabs, and calls the studio's own `choose()` when a
slab is selected. It reaches headsets and phones through WebXR, the
browser's own API, and everything else through a glTF 2.0 export. It
keeps nothing and proves nothing: `docs/XR_REVIEW.md`.
