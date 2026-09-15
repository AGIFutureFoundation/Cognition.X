# Simulation Studio

**Simulate what is dangerous, expensive or rare; practice live what is
safe, cheap and common; debrief every run. Simulation ≠ certification.**

The Simulation Studio (v0.54.0) is the platform's *Simulate* stage as
running code: a canonical fact base of **18 branching control-discipline
scenarios** ([`data/simulations/scenarios.json`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/data/simulations/scenarios.json)),
one shared engine ([`tools/sim/engine.js`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/tools/sim/engine.js))
injected into all six apps, and a validator that runs in CI. The full
account is in
[`docs/SIMULATION.md`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/docs/SIMULATION.md).

## What a run is

A learner reads a brief, meets five decision points (plus one or two
seeded complications at higher difficulty), chooses among three options
at each, sees the consequence, and ends in a debrief: three questions and
a score across six disciplines — verify before you act, stop-work
authority, say it out loud, the order is the safety, escalate rather than
improvise, the person in front of you. The run produces a portable
`cx-simrun/1` record.

## What a run is not

Every scenario is tied to a real track and carries that track's
**witnessed transfer check verbatim**. The check is done live, on real
material, with an assessor. A run is practice: it is never a witnessed
check, never evidence of competence, never a credential. In the Louisiana
app a kept run attaches to the learner as *practice* and touches nothing
else — not progress, not evidence, not the assessor queue.

## The engine

Deterministic (seeded; no randomness), three difficulties (rehearsal,
one complication, full drill), a next-difficulty recommendation after
each run (advice, never a gate), no timers, a live region for
consequences, keyboard-complete. The engine never touches the network or
storage; each host decides what to keep.

## Where it runs

- **Trades Network** — the Simulations view runs any of the nine
  categories on any region's own site; every roster card offers its
  scenario.
- **Louisiana** — student and teacher role widgets; the trades kinds run
  on New Orleans or River Region sites, the rest in the parish.
- **Platform** — between stage 2 and stage 3 of the loop, from the demo
  track's own pack; it adds nothing to the count.
- **Flow Hub** — a session on a track with a scenario offers the
  rehearsal; pack detail marks such tracks.
- **States** — the nine anchored scenarios on each state's own water,
  corridor, table, culture and storm memory.
- **Education OS** — the canonical library under the quest simulator.

## Authoring

Scenarios are authored in the fact base and validated by
`tools/validate_simulations.py` (real track, verbatim transfer check,
exactly one best option per decision, every discipline used, the law
present). They go through the curriculum review board like any pack.
