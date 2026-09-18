/* Cognition.X — the shared voice engine (v0.107.0).
 *
 * `chooseVoice` and `say` were defined verbatim, byte for byte, in four
 * app templates (Flow Hub, Louisiana, States, Trades Network): the same
 * three-persona table, the same speechSynthesis voice preference list,
 * the same sentence-by-sentence utterance drift. One engine now holds
 * that logic; each template keeps a one-line alias so its own inline
 * script is unchanged at the call site.
 *
 * `tourShow`/`tourEnd` were NOT folded in here even though the original
 * prompt named them alongside `say`/`chooseVoice`: each app's guided
 * tour is a genuinely different implementation (own DOM strategy — a
 * div created fresh per step versus one reused box; own navigation —
 * an in-page `go(view)` call versus a `location.hash` change behind a
 * 120/220/240ms `setTimeout`; own CSS class and accent color), not a
 * copy of the others under a shared name. Unifying them would trade a
 * real behavior-preservation risk for a cosmetic line count, so they
 * stay authored per template.
 *
 * Host API:
 *   CXVOICE.PERSONAS            -> the persona table (rate/pitch/drift)
 *   CXVOICE.chooseVoice()       -> the best-matching en-* SpeechSynthesisVoice, or null
 *   CXVOICE.say(text)           -> speaks text in the current mode; no-op if mode is ""
 *   CXVOICE.fromStored(v)       -> normalizes a stored value to "warm"|"steady"|"brisk"|""
 *   CXVOICE.getMode() / setMode(m) -> the current persona name ("" = voice off)
 */
(function (global) {
  "use strict";

  const PERSONAS = { warm: {rate: .97, pitch: 1.03, drift: .05}, steady: {rate: 1.0, pitch: 1.0, drift: .03}, brisk: {rate: 1.12, pitch: 1.02, drift: .02} };
  const VOICE_PREF = [/Google US English/i, /\bNatural\b/i, /\bNeural\b/i, /Samantha/i, /Aria/i, /Jenny/i, /Allison/i, /Karen/i, /Daniel/i];
  let mode = "";
  let picked = null;

  function chooseVoice() {
    try {
      const vs = speechSynthesis.getVoices().filter(v => /^en/i.test(v.lang));
      for (const re of VOICE_PREF) { const v = vs.find(x => re.test(x.name)); if (v) return v; }
      return vs.find(v => v.default) || vs[0] || null;
    } catch (e) { return null; }
  }

  try {
    if (typeof speechSynthesis !== "undefined") {
      picked = chooseVoice();
      speechSynthesis.onvoiceschanged = () => { picked = chooseVoice(); };
    }
  } catch (e) {}

  function say(text) {
    if (!mode) return;
    try {
      if (typeof speechSynthesis === "undefined") return;
      const P = PERSONAS[mode] || PERSONAS.steady;
      speechSynthesis.cancel();
      const parts = String(text).match(/[^.!?…]+[.!?…]*/g) || [String(text)];
      parts.forEach((s, i) => {
        const u = new SpeechSynthesisUtterance(s.trim());
        if (picked) u.voice = picked;
        u.rate = Math.max(.5, P.rate + (i % 2 ? -P.drift : P.drift) / 2);
        u.pitch = Math.max(.5, P.pitch + (i === 0 ? P.drift : 0));
        speechSynthesis.speak(u);
      });
    } catch (e) {}
  }

  function fromStored(v) {
    return ["warm", "steady", "brisk"].includes(v) ? v : (v === "on" ? "warm" : "");
  }

  global.CXVOICE = {
    PERSONAS,
    chooseVoice,
    say,
    fromStored,
    getMode: () => mode,
    setMode: (m) => { mode = m; },
  };
})(typeof window !== "undefined" ? window : globalThis);
