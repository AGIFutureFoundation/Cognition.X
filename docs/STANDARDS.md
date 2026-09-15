# Standards mapping and transfer-check rubrics

> Every code in this repository names an **intended alignment**, never a
> certification of one. Verify each code against the current document
> before classroom use. No external body has reviewed these mappings.

Shipped in v0.56.0 as roadmap step ⑤ (prompt 5 of
[`NEXT_STEPS_OPUS5.md`](NEXT_STEPS_OPUS5.md)). Two things an assessor and a
curriculum office asked for and did not have: a shared anchor for "would
transfer", and the codes a block was designed against.

## Standards — `data/standards/*.json` (`cx-standards/1`)

Two frameworks, two scopes, two honest strengths:

| File | Framework | Scope | Strength | Coverage |
|---|---|---|---|---|
| `lss-k12.json` | Louisiana Student Standards — Mathematics (LSSM, CCSS-numbered), ELA, Science (NGSS-style codes), as cited by the Louisiana K–12 program | block | **cites** — the block's author named these codes as the design target | 52 K–12 blocks, 299 citations. **Generated** by `tools/generate_standards.py` from `data/louisiana/k12_program.json`; CI regenerates and diffs. |
| `ngss-ets-robotics.json` | NGSS Engineering Design (K-2-ETS1, 3-5-ETS1, MS-ETS1, HS-ETS1; 2013) | track-band | **touches** — the track's blocks at this band practise the expectation's core activity | 4 Robotics OS tracks × 5 bands = 20 entries, 200 blocks. Authored, each entry with a one-line *why*. |

Strength words are deliberate. *cites* and *touches* are claims the
repository can stand behind; *aligns* (an external alignment review)
appears in the schema so the validator accepts it, and nowhere in the
data, because nobody has done one.

Every framework carries `publisher`, `documents`, `as_of` and a `caveat`
that tells the reader to verify. The validator refuses a file without
them.

## Rubrics — `data/rubrics/core_spine.json` (`cx-rubrics/1`)

Thirty rubrics, one per core-spine track — the tracks the Louisiana
ledger credits and the Records Office signs (Louisiana OS, Civic
Leadership Legacy : Louisiana, Basic Life Skills, Emergency Preparedness,
Parish Launch & Scale). Each sits under the three-line rubric every
assessor already uses (real material · independent at band · would
transfer) and gives:

- **Pass evidence** — three lines; any one met on real material at the
  learner's band is a confirmed check.
- **Common failure modes** — three; a check that matches one is recorded
  *not yet*, with the smaller step and the retry date.
- **An assessor note** — the one thing to watch for on this track.

The theme-level specific is the block's own transfer check, quoted at
check time; the rubric never replaces it. The bar never moves for an
access profile; the format does.

## Where they appear

- **Louisiana, Assessor Mode.** Opening a witnessed-check request shows
  the three lines and, beneath them, the track's rubric. *The honest
  witness* panel reports the coverage.
- **Flow Hub, pack detail.** A track with a rubric opens it above its
  themes; a band with codes shows them as chips with the framework and
  the caveat on hover; the K–12 rows carry a *Standards (as cited)*
  column.
- **Flow Hub, printed workbook.** The rubric prints under the track
  header and the codes print in each band's row, so the paper an
  assessor signs carries both.

## Validation and coverage

`tools/validate_standards.py` runs in CI: every block id, track and band
exists; a block-scope entry's theme and grade match the dataset; no
empty code; every framework has its metadata and a verifying caveat;
every rubric names a real track with exactly three pass lines, three
failure modes and a note. `docs/DATA_QUALITY.md` reports the coverage:
252 of 17,450 blocks carry a code; 30 of 225 tracks carry a rubric.

## Extending

A new framework is a new file in the schema above with its own `as_of`
and `caveat`; a generated one gets a generator and a CI diff step, an
authored one gets a *why* per entry. A new rubric names a real track and
goes through the curriculum review board like any pack. Frameworks and
rubrics that would require an external alignment review are not added
until one exists.
