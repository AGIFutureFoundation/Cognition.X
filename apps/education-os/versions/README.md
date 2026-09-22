# Education OS — archived builds

The canonical build is always `../index.html`. Superseded builds are kept
here verbatim for provenance.

| Version | File | Notes |
|---|---|---|
| v0.2.0 (current) | `../index.html` | "gov" build; app-internal iteration v227 (Sector Specialization, +120 master blocks); no network dependencies |
| v0.1.0 | `v0.1.0-education-os.html` | "affeducationos" build; loads Inter from Google Fonts |

See the repository `CHANGELOG.md` for the full version history.

## A note on v0.1.0 and the linter

`tools/lint_pages.py` skips this directory by default. Run against it
explicitly, the v0.1.0 archive reports 9 errors: a bare `var DATA = {`
sitting in its body outside any `<script>`, and eight ids its script
addresses — `#toast #nav #crumb #views #stateSel #stateflag #brandchip
#brandstrip` — that its markup never provides.

Those are real, and they are the same faults that were repaired in the
current build on 2026-09-22. They are **not** fixed here, because this
file is kept verbatim: an archive records what shipped, and editing it
to pass a check written afterwards would destroy the only thing it is
for. The faults are listed so the record is legible, not so it is
tidied.

    python3 tools/lint_pages.py apps/education-os/versions
