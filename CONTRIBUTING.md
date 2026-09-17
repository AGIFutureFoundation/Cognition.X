# Contributing to Cognition.X

## Ground rules

- **`block_id`s are forever.** Never renumber, reuse or delete an id;
  supersede a block by adding a replacement and noting it in the PR.
- **Specs are the source for new packs.** Author new content as a pack
  spec (`data/pack_specs/*.json`), not by editing `blocks.csv` by hand —
  `blocks.csv` and `manifest.json` are build outputs.
- **The validator is the contract.** `python3 tools/validate_blocks.py`
  must pass; CI runs it on every PR.

## Adding a pack

1. Copy an existing spec (e.g. `data/pack_specs/digital-life-data-ai.json`).
   A community pack is 5 tracks; each track has a unique-in-pack two-letter
   `prefix`, one `credential`, and exactly 10 themes with a `description`
   and a concrete, real-material `transfer_check`.
2. `python3 tools/generate_pack.py data/pack_specs/<spec>.json > data/generated/<spec>.csv`
3. `python3 tools/normalize_blocks.py && python3 tools/validate_blocks.py`
4. Add the pack's slug to `PACK_SLUGS` in `tools/normalize_blocks.py`
   (pins its `block_id` prefix), update `CHANGELOG.md` under *Unreleased*,
   and open a PR.

### Per-band descriptions (`bands`)

A theme's `description` is the sentence every band shares; on its own,
each block gets that sentence with an "— at ‹band›" suffix, which is the
documented content debt (`docs/DATA_QUALITY.md`, band-suffix column). To
pay it down, give the theme a `bands` map — the five band labels
(`K–2`, `3–5`, `6–8`, `9–10`, `11–12`) each to one sentence that says
what the learner **does** at that band. The band is already in the
`level` column, so the five must differ in the doing, not in adjectives:
a K–2 sentence is the child's honest version of the task with an adult,
an 11–12 sentence is the real deliverable for a real office. All five
must be present, non-empty and distinct; the generator refuses anything
less, and the suffix count in the tests only ever falls. The whole core
spine carries them (Emergency Preparedness & First Response and Parish
Launch & Scale since v0.65.0; Civic Leadership Legacy : Louisiana and, as
a promotion, Basic Life Skills & Self-Reliance since v0.66.0; the
Louisiana OS since v0.67.0) — copy their shape. The band ladder they
follow: 6–8 does the task on a smaller scope or with a checker; 9–10
does the whole thing for real; 11–12 does it for others, for a real
body, or on the record.

### Overriding a suffixed source description (`override`)

Some packs — the seven sector OS packs — arrived with their suffixed
sentences already in the *source*, so the fill-empty rule keeps `bands`
out. For those, and only those, a promotion may declare
`"override": "band-suffix"` (see `data/promotions/corporate-os.json`).
The normaliser then replaces a description **only** when it is the
shared sentence with its "— at ‹band›" suffix for the row's own band,
and only with that theme's authored sentence for that band; an authored
source sentence, an empty one, a wrong band or malformed `bands` is
refused with the row id. It is the second counted exception to
fill-empty-only (the first is the credential correction): the
normaliser prints the count, `docs/DATA_QUALITY.md` reports it, and the
tests hold it. Nothing else on the row — track, code, credential,
transfer check — is touched.

### Writing style (match the corpus)

- Track names read like a journey: *"Privacy and the trail you leave"*.
- Themes are concrete and human: *"Keys, locks and who else holds one"* —
  not "Unit 3: Security".
- Transfer checks are imperative, performed on **real material**, and
  observable: "Restore one real file from a backup you made yourself."

## App and tooling changes

- The Education OS app stays a single, offline-capable file — no
  runtime network dependencies. Since v0.19.0 `index.html` is a build
  product: edit `apps/education-os/template.html` (or the dataset) and
  run `python3 tools/build_education_os.py` — never edit `index.html`
  directly.
- Superseded app builds move to `apps/education-os/versions/` rather than
  being overwritten silently; record the change in `CHANGELOG.md`.

## Releases

Maintainers cut releases from `main`: update `VERSION` and
`CHANGELOG.md`, tag `vX.Y.Z`. MINOR for new packs/features, PATCH for
corrections, MAJOR for schema or id-format changes.

## Licensing of contributions

In-bound = out-bound: code contributions are accepted under Apache-2.0 and
content/data contributions under CC BY 4.0 (see `docs/LICENSING.md`).
