# Authoring Packs

New packs are written as **specs**, not spreadsheets. A spec is a JSON
file in `data/pack_specs/` declaring tracks and themes; tooling expands it
across the five grade bands deterministically.

## Shape of a community pack

- **5 tracks**, each with:
  - `name` — reads like a journey: *"Privacy and the trail you leave"*
  - `prefix` — two letters, unique within the pack
  - `credential` — the name earned: *"Data Steward"*
  - **10 themes**, each with:
    - `theme` — concrete and human: *"Keys, locks and who else holds one"*
    - `description` — one sentence of what is taught
    - `transfer_check` — imperative, on real material, observable

Expansion: every theme × 5 bands (K–2/3–5 Explorer, 6–8 Builder, 9–10
Practitioner, 11–12 Lead) → 250 blocks.

## Workflow

```bash
python3 tools/generate_pack.py data/pack_specs/my-pack.json > data/generated/my-pack.csv
```

A theme may carry `bands` — the five band labels each to a sentence
that says what the learner does at that band — instead of letting the
generator suffix one shared sentence with "— at ‹band›". All five must
be present and distinct (see `CONTRIBUTING.md`, *Per-band descriptions*;
`parish-launch-scale.json` shows the shape).

```
python3 tools/normalize_blocks.py     # rebuild blocks.csv + manifest.json
python3 tools/validate_blocks.py      # must pass; CI enforces it
```

Then pin the pack's `block_id` slug in `PACK_SLUGS`
(`tools/normalize_blocks.py`), note the pack in `CHANGELOG.md`, and open
a PR. Reference example:
[`digital-life-data-ai.json`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/data/pack_specs/digital-life-data-ai.json).

## Writing transfer checks that survive review

Bad: "Understand password security."
Good: "Turn on a second factor for a real account and explain what attack
it just blocked."

The test: could an assessor watch the artifact or performance and say yes
or no without asking a quiz question?

## Candidate packs wanted

The original Phase 1 candidate list (Food, Energy, Transport, Emergency
Preparedness, Arts, Law) has shipped. Ideas that would extend coverage —
open an issue proposing tracks before writing a full spec:

Parenting & Early Years · Grief, Loss & Endings · Sport, Movement &
Coaching · Faith, Meaning & Pluralism · Rural Skills & Land Craft ·
Entrepreneurship & the Small Trade

## The Pack Studio (v0.35.0)

Flow Hub's **Author** view is a form-driven spec editor: tracks of ten
themes with live generator-grade validation, a worked example,
import-to-edit, browser-local drafts, and a validated JSON export that
round-trips through `tools/generate_pack.py` unchanged. Export the spec,
save it under `data/pack_specs/`, and open a pull request — CI validates
mechanically and the [curriculum review board](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/docs/GOVERNANCE.md)
reviews for accuracy, safety, honest transfer checks and respectful
terminology before merge.
