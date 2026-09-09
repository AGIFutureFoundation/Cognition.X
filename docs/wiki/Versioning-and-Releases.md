# Versioning and Releases

Cognition.X follows [Semantic Versioning](https://semver.org). The current
version is in [`VERSION`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/VERSION);
history is in [`CHANGELOG.md`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/CHANGELOG.md).

## What bumps what

| Change | Bump |
|---|---|
| Fixing typos, correcting a transfer check, doc edits | **PATCH** |
| New pack, new app feature, new tooling | **MINOR** |
| Dataset schema change, `block_id` format change, removing a pack | **MAJOR** |

## Invariants

- `block_id`s are never reused or renumbered — a MAJOR bump does not
  license breaking them; supersede blocks instead.
- Superseded app builds are archived under
  `apps/education-os/versions/`, never silently overwritten.
- Every release tag `vX.Y.Z` points at a commit where CI (the dataset
  validator) is green.

## History

| Version | Summary |
|---|---|
| **v0.4.0** | *Food, Cooking & Nutrition* pack (250 blocks) — dataset at 7,250 blocks / 27 packs |
| v0.3.0 | First repo release: structure, CI, canonical dataset (7,000 blocks) with stable ids, *Digital Life, Data & AI* pack, docs/roadmap/wiki, dual licensing |
| v0.2.0 | Imported "gov" app build (internal v227, Sector Specialization, offline fonts) |
| v0.1.0 | Imported "affeducationos" app build + 6,750-block CSV export |

## Cutting a release

1. Update `VERSION` and move `CHANGELOG.md` *Unreleased* items under the
   new version heading.
2. Merge to `main` with CI green.
3. `git tag -a vX.Y.Z -m "Cognition.X vX.Y.Z" && git push origin vX.Y.Z`
4. Optionally publish a GitHub Release pointing at the tag, attaching the
   app HTML as a downloadable asset.
