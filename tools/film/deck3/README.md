# The three-page investor deck

`gen3.py` writes `deck3.html` (clickable, three pages), `preview3.html`
(print edition — `check3.js` exports it as the PDF) and `preview.html`
(the eight-slide video edition) plus `narration.json`. The app screenshots
the pages embed (`shot-*.png`) are taken by `../deck/shots.js` and are not
committed; `shots3.js` takes the page previews.

    python3 gen3.py                       # pages + narration
    NODE_PATH=$(npm root -g) node check3.js   # overflow/overlap measure + PDF
    python3 synth.py                      # narration via ../tts.py (kokoro)
    NODE_PATH=$(npm root -g) node rec.js  # record slides to the narration timings
    python3 mux.py                        # align clips, loudnorm, H.264 MP4

Canonical text: `docs/PITCH_DECK.md`. Not an offer to sell securities.
