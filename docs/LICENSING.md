# Licensing — recommendation and rationale

Cognition.X mixes two very different kinds of work, and the recommendation
is to license them differently. This is the model used by most open
curriculum projects (e.g. OpenStax, Khan Academy exercises, OER Commons
material).

## Recommended (and applied) model

| Layer | Examples | License | File |
|---|---|---|---|
| **Code** | `tools/*.py`, the Education OS app shell & logic, CI workflows | **Apache License 2.0** | [`/LICENSE`](../LICENSE) |
| **Content & data** | `data/*.csv`, `data/pack_specs/*.json`, block text, themes, transfer checks, docs, wiki | **Creative Commons Attribution 4.0 (CC BY 4.0)** | [`/LICENSE-CONTENT`](../LICENSE-CONTENT) |

Attribution line for content reuse:

> Contains Cognition.X material by AGI Future Foundation, licensed under
> CC BY 4.0 — https://github.com/AGIFutureFoundation/Cognition.X

## Why these two

**Apache-2.0 for code**
- Permissive, so schools, ministries and vendors can embed the tools and
  app without copyleft obligations — important for adoption inside
  government and corporate learning systems.
- Unlike MIT, it carries an **express patent grant** and
  patent-retaliation clause, which matters for a foundation publishing
  education infrastructure that others will build on.

**CC BY 4.0 for content**
- Software licenses are a poor fit for prose and data; CC licenses are
  written for it.
- BY (attribution-only) maximises reuse: a teacher can translate a pack,
  a district can remix blocks into its own scope-and-sequence, a company
  can build a paid product on top — all they owe is credit. That spread
  is the mission of an education foundation.
- 4.0 explicitly covers **database rights**, which matters for
  `blocks.csv`.

## Alternatives considered

- **CC BY-SA 4.0** (share-alike) — keeps derivatives open, but blocks
  integration into mixed-license courseware and deters institutional
  adopters. Choose it only if preventing closed derivatives matters more
  than reach.
- **CC0** — frictionless, but drops the attribution that carries the
  foundation's name with the material.
- **MIT for code** — fine, but no patent grant; Apache-2.0 is the safer
  default at foundation scale.
- **AGPL/GPL for the app** — would prevent ministries and vendors from
  deploying modified private instances; contrary to adoption goals.

## Housekeeping

- Every source file created here is covered by the repo-level licenses;
  per-file headers are optional and not required by either license.
- Contributions are accepted under the same in-bound = out-bound terms
  (see [`CONTRIBUTING.md`](../CONTRIBUTING.md)). If the foundation later
  wants relicensing freedom, adopt a lightweight CLA/DCO before external
  contributions scale up.
- The names "Cognition.X" and "AGI Future Foundation" are not licensed by
  either license; trademark use requires separate permission.
