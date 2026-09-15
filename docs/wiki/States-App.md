# States App

**Cognition.X States** ([`apps/states/`](https://github.com/AGIFutureFoundation/Cognition.X/tree/main/apps/states))
is the 50-state curriculum layer: the Louisiana pattern generalized so
**every U.S. state gets a custom course catalog** from one shared
blueprint.

Built by [`tools/build_states.py`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/tools/build_states.py)
from three sources — never hand-edit `index.html`:

1. **The 50-state fact base**
   ([`data/states/states.json`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/data/states/states.json)):
   every state with its capital, region, a stylized US tile-grid
   position, and five localization anchors — *water, working corridor,
   table, culture, storm memory* — of public general knowledge.
2. **The Cognition.X : States OS blueprint pack** (250 blocks, five
   universal tracks whose transfer checks are phrased on *your state's*
   real material). The blueprint is the constant; the state is the
   variable.
3. **The Education OS app's Institute fact base** — the Willie L.
   Brown Jr. Institute principles and mission are extracted from
   `apps/education-os/template.html` at build time (exactly as the
   Louisiana build does), so the Education OS remains the seed of the
   state model. Its disclaimer is carried verbatim.

## Surfaces

- **The Nation** — a 50-tile US cartogram colored by region; click any
  state for its curriculum.
- **All 50 States** — the searchable catalog of catalogs.
- **State Curriculum** (`#/state/TX`, deep-linkable) — the five
  blueprint courses localized by that state's anchors ("Water and the
  land — *the Rio Grande border and the Gulf's chest*"), the Institute
  Model civic tracks placed in that state's capital, the core spine
  (K–12, life skills, emergency, launch, universal access), and Flow
  Hub deep links.
- **The Blueprint / The Institute Model** — the two universal layers in
  full, with the twelve principles.
- **Compliance (v0.51.0)** — what each state asks of a program office:
  ten domains per state (student data privacy law and the agreement a
  district will ask for, homeschool notice and assessment forms, foreign
  nonprofit qualification, charitable-solicitation registration,
  background checks, mandated reporting, apprenticeship agency, the CTE
  credential list, digital accessibility, sales-tax exemption) with the
  agency, the form, the fee (as-of year, `verify` flag) and a cost
  roll-up. A lens map of the nation (homeschool tier, charity
  registration, operator law, SAA/OA, sales tax, universal reporting,
  cost band), a per-state checklist that exports as
  `cxstate-compliance/1` JSON and prints, and the national baseline.
  Every state page carries the short list. Not legal advice — the data
  says so, and CI regenerates
  [`docs/STATE_COMPLIANCE.md`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/docs/STATE_COMPLIANCE.md)
  from it.
- **Adoption** — how a state goes from blueprint to running system on
  the Louisiana reference: fact base → spine → two waves → halls with
  the Network OS → ledger and signed credentials.

Anchors are door-openers for local study, not exhaustive claims;
communities named are the keepers of their own stories. Standards and
civic-seal names are verified with each state's education department.
