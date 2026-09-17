# White papers and promo films for named organisations

Three modules of the Education OS were written for the needs of three
real organisations, from their public record only, with no affiliation,
endorsement or contact claimed. For each there is a white paper (every
course, session and module, with the module's own refusals and
disclaimer) and a promo film recorded from the app itself.

| Module (Education OS view) | White paper | Film script |
|---|---|---|
| Willie L. Brown Jr. Institute Track (`#/wlb`) | [`willie-brown-institute-track.md`](willie-brown-institute-track.md) | `tools/film/orgs/wlb.js` |
| Tenderloin Pilot · SF (`#/thc`) | [`tenderloin-pilot.md`](tenderloin-pilot.md) | `tools/film/orgs/thc.js` |
| Third Place · Club Edition and Club Administrator Academy (`#/club`, `#/clubadmin`) | [`third-place-club-edition.md`](third-place-club-edition.md) | `tools/film/orgs/club.js` |

The papers' appendices are generated from the built app and the
dataset (`data/blocks.csv`), so a paper says what the module says.

## Regenerate

```bash
# PDF + print HTML for a paper (python-markdown + Chromium via Playwright)
python3 tools/film/orgs/paper.py docs/whitepapers/tenderloin-pilot.md out/

# a film (Playwright records the real app; narration offline with kokoro; ffmpeg encodes)
NODE_PATH=$(npm root -g) CX_KOKORO_DIR=path/to/kokoro node tools/film/orgs/thc.js
# → tools/film/out/org-tenderloin-pilot.mp4
```

Ground rules, which are the modules' own: the disclaimer each page
carries is spoken in the film and printed in the paper, verbatim; no
organisation's marks or programme names are used; nothing is presented
as a partnership; a simulation is practice; nothing leaves a page on its
own. Not legal advice.
