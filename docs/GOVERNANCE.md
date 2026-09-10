# Governance — the Curriculum Review Board

How curriculum enters, changes and leaves the Cognition.X dataset. This
process is the quality gate the [system review](SYSTEM_REVIEW.md) calls
for; GitHub is the pipeline, CI is the mechanical gate, and the board is
the human one.

## The board

Three to seven reviewers, appointed by the repository maintainers,
covering at minimum: a practicing educator, a subject-matter reviewer
for the pack under review (rotating), and an accessibility/equity
reviewer. Reviewers recuse themselves from packs they authored. Until a
board is seated, the maintainers act as the board and this document is
the standard they review against.

## What the board reviews

Every pull request that adds or changes curriculum content — pack specs
(`data/pack_specs/`), promotions (`data/promotions/`), fact bases
(`data/unions/`, `data/states/`, `data/learners/`), and any change to
source rows. Tooling and app changes need CI plus one maintainer, not
the board — unless they change what a learner is told.

## The review checklist

A pack is approved when every reviewer can answer yes:

1. **Accuracy** — factual claims check out against public sources; the
   pack claims no expertise it doesn't carry.
2. **Real transfer checks** — every check is a concrete task on real
   material a learner can actually reach, and safe: observation from
   public ground, rated tags and paper trails, nothing energized,
   suspended or moving, nothing requiring purchases beyond the modest.
3. **Honesty stances intact** — simulation ≠ certification; no union
   local numbers (councils are the front door); access profiles are
   supports, never diagnoses; anchors are door-openers, not exhaustive
   claims; independence disclaimers preserved verbatim where they
   apply (the Willie L. Brown Jr. Institute disclaimer above all).
4. **Respectful terminology** — communities are named as they name
   themselves and honored as the keepers of their own stories;
   identity-first/person-first language follows community preference.
5. **Shape and provenance** — CI green (tracked shape, unique codes);
   no edits to source rows or existing `block_id`s; new content arrives
   only through specs, promotions or documented fact bases.
6. **Access** — checks admit alternative formats (the capability is the
   constant, the format is the variable); nothing gates on reading
   speed, handwriting, or a single sensory channel.

## Acceptance flow

1. Author the spec — the Flow Hub **Pack Studio** (Author view)
   validates and exports it — and open a PR adding it under
   `data/pack_specs/` with the generated CSV.
2. CI must pass (`validate_blocks.py`).
3. Two board approvals (one maintainer suffices while the board is
   unseated), checklist in the review comments.
4. Squash-merge; the release notes name the pack and its block count.

## Breaking changes

- `block_id`s are never reused, renumbered or deleted — a wrong block
  is **superseded** by a new block and noted in the changelog, never
  rewritten away. Fixing typos and factual errors in place is a PATCH
  and allowed; changing what a block *teaches* is a supersession.
- Removing a pack is a MAJOR change requiring board consensus and a
  migration note for anyone holding its credentials.

## The standing review queue

The ~9,950 machine-authored blocks (everything post-import) are
validator-clean but **have not passed this board**. They are the
standing queue, to be reviewed pack-by-pack in this order: the packs in
classroom-facing use first (K–12 spine adjacents, Access, Launch), then
community packs, then OS editions. Until a pack clears review, the
in-app scaffold labels stay, and adopters should treat its content as a
draft for their own committee.
