#!/usr/bin/env python3
"""Hold the release-tag procedure to the changelog (v0.71.0).

docs/wiki/Versioning-and-Releases.md says every release is tagged
`vX.Y.Z` on its merged commit. This checks that it is, and can restore
the tags where it was not:

    python3 tools/release_tags.py --check      # every changelog version below
                                               # the current one has a tag; exit 1 if not
    python3 tools/release_tags.py --backfill   # create the missing annotated tags at the
                                               # first commit on the main line whose VERSION
                                               # file carries that version (prints what it did)
    python3 tools/release_tags.py --backfill --dry-run

The current version (the top changelog entry) is tagged after its pull
request merges, so it is not required. Versions older than the first
commit in the repository (the changelog predates the git history by two
entries) are skipped and named.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# changelog entries older than the first commit in this repository (verified by --backfill)
PREDATES_REPOSITORY = {"0.1.0", "0.2.0"}


def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=check).stdout


def changelog_versions():
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    return re.findall(r"^## \[(\d+\.\d+\.\d+)\]", text, re.M)  # newest first


def existing_tags():
    return set(git("tag", "-l", "v*").split())


def version_commits(rev="HEAD"):
    """First commit (oldest first) at which VERSION reads each version."""
    out, prev = {}, None
    for sha in git("log", "--reverse", "--first-parent", "--format=%H", rev).split():
        r = subprocess.run(["git", "show", f"{sha}:VERSION"], cwd=ROOT, capture_output=True, text=True)
        v = r.stdout.strip() if r.returncode == 0 else None
        if v and v != prev:
            out.setdefault(v, sha)
            prev = v
    return out


def main(argv):
    versions = changelog_versions()
    current, released = versions[0], versions[1:]
    tags = existing_tags()
    if "--check" in argv:
        # no history walk here: CI runs this on a shallow clone with only the tag refs fetched
        before_history = [v for v in released if v in PREDATES_REPOSITORY]
        missing = [v for v in released if f"v{v}" not in tags and v not in PREDATES_REPOSITORY]
        print(f"changelog: {len(versions)} versions; current v{current} (tagged after merge); "
              f"tags present: {len([v for v in released if f'v{v}' in tags])}/{len(released) - len(before_history)}; "
              f"predate the repository: {', '.join(before_history) or 'none'}")
        if missing:
            print("MISSING tags: " + ", ".join(f"v{v}" for v in missing))
            return 1
        print("every released version is tagged")
        return 0
    if "--backfill" in argv:
        dry = "--dry-run" in argv
        commits = version_commits()
        made = 0
        for v in reversed(released):
            if f"v{v}" in tags:
                continue
            sha = commits.get(v)
            if not sha:
                print(f"skip v{v}: no commit on the main line carries it")
                continue
            date = git("log", "-1", "--format=%cI", sha).strip()
            print(f"{'would tag' if dry else 'tag'} v{v} at {sha[:10]} ({date[:10]})")
            if not dry:
                subprocess.run(["git", "tag", "-a", f"v{v}", sha, "-m", f"Cognition.X v{v}"],
                               cwd=ROOT, check=True, env={**__import__('os').environ,
                                                          "GIT_COMMITTER_DATE": date})
            made += 1
        print(f"{made} tags {'to create' if dry else 'created'}; push with: git push origin --tags")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
