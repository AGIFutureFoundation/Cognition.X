# Cognition.X

**Flow Zone — education-based learning, as modular frameworks.**

Cognition.X is an open curriculum system built from small, verifiable units
called **blocks**. A block names one thing a learner can do, at one grade
band, and pairs it with a **transfer check** — a concrete task performed on
real material that proves the skill transferred. Blocks roll up into
**themes**, themes into **tracks**, tracks into **credentials**, and
credential families into **packs** that cover life from K–12 mathematics to
tenancy law, reentry after incarceration, global health field practice, and
working alongside AI systems.

The repository carries three things:

| What | Where | Format |
|---|---|---|
| The blocks dataset (7,000 blocks, 26 packs) | [`data/`](data/) | CSV + JSON manifest |
| The Education OS app (single-file, offline-capable) | [`apps/education-os/`](apps/education-os/) | HTML |
| Docs, roadmap and wiki source | [`docs/`](docs/) | Markdown |

## Quick start

```bash
# Explore the canonical dataset
python3 -c "import csv; rows=list(csv.DictReader(open('data/blocks.csv'))); print(len(rows), 'blocks')"

# Validate it
python3 tools/validate_blocks.py

# Open the app (no server or network needed)
open apps/education-os/index.html        # macOS
xdg-open apps/education-os/index.html    # Linux
```

## The data model in one paragraph

Every row of [`data/blocks.csv`](data/blocks.csv) is a block with a globally
unique `block_id` (`CX-<PACK>-<NNNN>`). Tracked packs follow a fixed shape:
each **track** contains **10 themes**, and each theme is taught at **5 grade
bands** — K–2 and 3–5 at *Explorer* level, 6–8 at *Builder*, 9–10 at
*Practitioner*, 11–12 at *Lead* — so a track is 50 blocks and one
credential. Earlier "legacy" packs (K–12, Trade School, and the
grade-banded community packs) predate that shape and are kept verbatim.
Full details: [`data/schema.md`](data/schema.md) and the
[wiki](docs/wiki/Home.md).

## Packs at a glance

Seven **Cognition.X OS editions** (Corporate, Science, Robotics, Global
Health, Multilateral, Sapient, Non-Profit — 500 blocks each), ten
**community packs** (250 each — housing, money, reentry, neighbourhood,
preventive health, life skills, water/land/climate, care, making/repair,
and the new *Digital Life, Data & AI* pack), plus the legacy K–12, Trade
School and thematic packs. The generated
[`data/manifest.json`](data/manifest.json) is the machine-readable index.

## Regenerating and extending the data

```bash
# 1. Author a pack spec: 5 tracks x 10 themes (see data/pack_specs/)
# 2. Expand it across the five grade bands
python3 tools/generate_pack.py data/pack_specs/my-pack.json > data/generated/my-pack.csv
# 3. Rebuild the canonical dataset + manifest, then validate
python3 tools/normalize_blocks.py
python3 tools/validate_blocks.py
```

CI runs the validator on every push and pull request
([`.github/workflows/validate.yml`](.github/workflows/validate.yml)).

## Versioning

Releases follow [Semantic Versioning](https://semver.org) and are recorded
in [`CHANGELOG.md`](CHANGELOG.md); the current version is in
[`VERSION`](VERSION). Superseded builds of the app are archived under
[`apps/education-os/versions/`](apps/education-os/versions/).

## Roadmap · Wiki · Contributing

- Deep roadmap: [`docs/ROADMAP.md`](docs/ROADMAP.md)
- Wiki source (publishable to the GitHub wiki): [`docs/wiki/`](docs/wiki/)
- Data review and known issues: [`docs/DATA_REVIEW.md`](docs/DATA_REVIEW.md)
- How to contribute: [`CONTRIBUTING.md`](CONTRIBUTING.md)

## License

Dual-licensed by design (rationale in [`docs/LICENSING.md`](docs/LICENSING.md)):

- **Code** (tools, app shell, CI): [Apache License 2.0](LICENSE)
- **Curriculum content and data** (blocks, packs, docs): [CC BY 4.0](LICENSE-CONTENT)

© AGI Future Foundation.
