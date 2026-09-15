/* Cognition.X Simulation Studio — the shared scenario engine (v0.54.0).
 *
 * One engine, injected by every builder at its template's studio placeholder, run
 * inside each single-file app. It plays a branching control-discipline
 * scenario from data/simulations/scenarios.json:
 *
 *   - deterministic: a seed and a difficulty fully decide which
 *     complications are injected and where (mulberry32, no randomness);
 *   - difficulty 1–3 (rehearsal / one complication / full drill), with a
 *     next-difficulty recommendation after each run — advice, never a gate;
 *   - no timers, no autoplay: every step waits for a choice (access profiles);
 *   - accessible: a live region announces consequences, options are real
 *     buttons, focus moves to each new prompt;
 *   - a run ends in a portable cx-simrun/1 record that a host may store as
 *     PRACTICE. It is never a witnessed check and never a credential. The
 *     run note is carried verbatim inside every record.
 *
 * Host API:
 *   CXSIM.mount(hostElement, scenario, {site, difficulty, seed, onRun, compact})
 *     -> controller {start(), destroy(), record()}
 *   CXSIM.localize(scenario, site)   -> a copy with every {site} filled in
 *   CXSIM.plan(scenario, difficulty, seed) -> the ordered decision points
 *   CXSIM.score(plan, choices)       -> {score, max, pct, byDiscipline}
 *   CXSIM.nextDifficulty(pct, difficulty)
 *   CXSIM.LAW / CXSIM.RUN_NOTE / CXSIM.DISCIPLINES (set by CXSIM.configure)
 *
 * Nothing here touches the network or storage; the host decides what to
 * keep. Styles use the host app's tokens with plain fallbacks.
 */
(function (global) {
  "use strict";
  const CXSIM = {};
  CXSIM.LAW = "";
  CXSIM.RUN_NOTE = "A simulation run is practice. It is not a witnessed check, it is not evidence of competence, and it is never a credential. Simulation ≠ certification.";
  CXSIM.DISCIPLINES = [];
  CXSIM.DIFFICULTY = [{level:1,name:"Rehearsal"},{level:2,name:"Complications"},{level:3,name:"Full drill"}];

  CXSIM.configure = function (fb) {
    if (!fb) return CXSIM;
    if (fb.law) CXSIM.LAW = fb.law;
    if (fb.run_note) CXSIM.RUN_NOTE = fb.run_note;
    if (Array.isArray(fb.disciplines)) CXSIM.DISCIPLINES = fb.disciplines;
    if (Array.isArray(fb.difficulty)) CXSIM.DIFFICULTY = fb.difficulty;
    return CXSIM;
  };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  }
  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function hashSeed(s) {
    let h = 2166136261;
    for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  function fill(text, site) { return String(text).split("{site}").join(site); }

  CXSIM.localize = function (sc, site) {
    const s = site || sc.site_default || "the site";
    const copy = JSON.parse(JSON.stringify(sc));
    copy.site = s;
    copy.brief = fill(copy.brief, s);
    (copy.steps || []).concat(copy.complications || []).forEach(st => {
      st.prompt = fill(st.prompt, s);
      st.options.forEach(o => { o.t = fill(o.t, s); o.c = fill(o.c, s); });
    });
    return copy;
  };

  /* The plan: the scenario's decision points in order, with complications
     injected at seeded positions (never first, never last). */
  CXSIM.plan = function (sc, difficulty, seed) {
    const d = Math.max(1, Math.min(3, Number(difficulty) || 1));
    const steps = (sc.steps || []).map(st => ({...st, kind: "step"}));
    const comps = (sc.complications || []).slice(0, d - 1).map(st => ({...st, kind: "complication"}));
    const rng = mulberry32(hashSeed(String(seed == null ? "" : seed) + "|" + sc.id + "|" + d));
    comps.forEach(c => {
      const pos = 1 + Math.floor(rng() * Math.max(1, steps.length - 1));
      steps.splice(pos, 0, c);
    });
    return steps;
  };

  CXSIM.score = function (plan, choices) {
    const by = {};
    let score = 0, max = 0;
    plan.forEach((st, i) => {
      const best = Math.max(...st.options.map(o => o.s));
      const pick = choices[i] == null ? null : st.options[choices[i]];
      const d = pick ? pick.d : st.options.find(o => o.s === best).d;
      by[d] = by[d] || {got: 0, max: 0};
      by[d].max += best; max += best;
      if (pick) { by[d].got += pick.s; score += pick.s; }
    });
    return {score, max, pct: max ? Math.round(100 * score / max) : 0, byDiscipline: by};
  };

  CXSIM.nextDifficulty = function (pct, difficulty) {
    const d = Math.max(1, Math.min(3, Number(difficulty) || 1));
    if (pct >= 85 && d < 3) return d + 1;
    if (pct < 50 && d > 1) return d - 1;
    return d;
  };

  const CSS = `
  .cxsim{border:1px solid var(--line,#d9dee4);border-radius:12px;padding:16px 18px;background:var(--surface,#fff);color:var(--ink,#1c2430);font-size:.92rem;line-height:1.45}
  .cxsim *{box-sizing:border-box}
  .cxsim .cxsim-law{font-size:.78rem;color:var(--faint,#5f6b7a);border-left:3px solid var(--gold,#7f5a00);padding:6px 10px;margin:8px 0 12px}
  .cxsim .cxsim-head{display:flex;gap:10px;flex-wrap:wrap;align-items:baseline}
  .cxsim h4{margin:0;font-size:1.05rem}
  .cxsim .cxsim-role{font-size:.78rem;color:var(--muted,#4b5563)}
  .cxsim .cxsim-brief{margin:8px 0 10px}
  .cxsim .cxsim-lists{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;font-size:.8rem;margin:0 0 12px}
  .cxsim .cxsim-lists b{display:block;font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint,#5f6b7a);margin-bottom:3px}
  .cxsim ul{margin:0;padding-left:18px}
  .cxsim .cxsim-controls{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:6px 0 4px}
  .cxsim select,.cxsim button{font:inherit}
  .cxsim .cxsim-btn{border:1px solid var(--line,#d9dee4);background:var(--surface-2,var(--bg,#f4f6f8));color:var(--ink,#1c2430);border-radius:9px;padding:8px 14px;cursor:pointer;min-height:36px}
  .cxsim .cxsim-btn.gold{background:var(--gold,#7f5a00);border-color:var(--gold,#7f5a00);color:var(--on-gold,#fff)}
  .cxsim .cxsim-btn:focus-visible{outline:2px solid var(--gold,#7f5a00);outline-offset:2px}
  .cxsim .cxsim-btn[disabled]{opacity:.55;cursor:default}
  .cxsim .cxsim-prog{font-size:.74rem;color:var(--faint,#5f6b7a);font-variant-numeric:tabular-nums;margin:10px 0 4px}
  .cxsim .cxsim-prompt{font-weight:600;margin:6px 0 10px}
  .cxsim .cxsim-prompt.comp::before{content:"Complication · ";color:var(--gold,#7f5a00);font-size:.74rem;letter-spacing:.08em;text-transform:uppercase}
  .cxsim .cxsim-opts{display:grid;gap:8px}
  .cxsim .cxsim-opt{text-align:left;border:1px solid var(--line,#d9dee4);background:var(--surface,#fff);color:var(--ink,#1c2430);border-radius:10px;padding:10px 12px;cursor:pointer;line-height:1.4}
  .cxsim .cxsim-opt:hover{border-color:var(--gold,#7f5a00)}
  .cxsim .cxsim-opt:focus-visible{outline:2px solid var(--gold,#7f5a00);outline-offset:2px}
  .cxsim .cxsim-opt[disabled]{cursor:default;opacity:.7}
  .cxsim .cxsim-opt.picked{border-width:2px;border-color:var(--gold,#7f5a00);opacity:1}
  .cxsim .cxsim-cons{margin:10px 0 6px;padding:10px 12px;border-radius:10px;background:var(--surface-2,var(--bg,#f4f6f8));border:1px solid var(--line,#d9dee4)}
  .cxsim .cxsim-cons .s2{color:var(--green,#1f7a4d);font-weight:600}
  .cxsim .cxsim-cons .s1{color:var(--gold,#7f5a00);font-weight:600}
  .cxsim .cxsim-cons .s0{color:var(--w4,var(--red,#a83a3a));font-weight:600}
  .cxsim .cxsim-bars{display:grid;gap:6px;margin:10px 0}
  .cxsim .cxsim-bar{display:grid;grid-template-columns:190px minmax(0,1fr) 54px;gap:10px;align-items:center;font-size:.8rem}
  .cxsim .cxsim-bar i{display:block;height:9px;border-radius:5px;background:var(--line,#d9dee4);overflow:hidden}
  .cxsim .cxsim-bar i b{display:block;height:100%;background:var(--gold,#7f5a00)}
  .cxsim .cxsim-bar span:last-child{text-align:right;font-variant-numeric:tabular-nums}
  .cxsim .cxsim-debrief{margin:10px 0}
  .cxsim .cxsim-debrief label{display:block;font-size:.84rem;margin:8px 0 4px}
  .cxsim textarea{width:100%;min-height:52px;font:inherit;font-size:.84rem;border:1px solid var(--line,#d9dee4);border-radius:8px;padding:8px;background:var(--surface,#fff);color:var(--ink,#1c2430)}
  .cxsim .cxsim-note{font-size:.78rem;color:var(--faint,#5f6b7a);margin:8px 0}
  .cxsim .cxsim-json{display:none;width:100%;min-height:120px;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.72rem;margin-top:8px}
  .cxsim .cxsim-json.show{display:block}
  .cxsim .cxsim-live{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
  .cxsim .cxsim-transfer{font-size:.8rem;border-top:1px dashed var(--line,#d9dee4);padding-top:10px;margin-top:12px}
  @media (max-width:640px){.cxsim .cxsim-bar{grid-template-columns:1fr 60px;grid-template-rows:auto auto}.cxsim .cxsim-bar i{grid-column:1/-1}}
  `;
  let cssInjected = false;
  function injectCSS() {
    if (cssInjected || typeof document === "undefined") return;
    const st = document.createElement("style"); st.setAttribute("data-cxsim", "1"); st.textContent = CSS;
    document.head.appendChild(st); cssInjected = true;
  }

  CXSIM.mount = function (host, scenario, opts) {
    injectCSS();
    opts = opts || {};
    const site = opts.site || scenario.site_default || "the site";
    const sc = CXSIM.localize(scenario, site);
    let difficulty = Math.max(1, Math.min(3, Number(opts.difficulty) || 1));
    let seed = opts.seed != null ? String(opts.seed) : String(Date.now());
    let plan = [], choices = [], idx = 0, phase = "intro", debrief = [], lastRecord = null;
    const discName = id => (CXSIM.DISCIPLINES.find(d => d.id === id) || {name: id}).name;

    host.classList.add("cxsim");
    host.setAttribute("data-scenario", sc.id);

    function announce(t) { const l = host.querySelector(".cxsim-live"); if (l) l.textContent = t; }
    function focusPrompt() { const p = host.querySelector(".cxsim-prompt, .cxsim-result h4"); if (p) { p.setAttribute("tabindex", "-1"); p.focus({preventScroll: false}); } }

    function renderIntro() {
      phase = "intro";
      host.innerHTML = `
        <div class="cxsim-live" aria-live="polite"></div>
        <div class="cxsim-head"><h4>${esc(sc.title)}</h4><span class="cxsim-role">${esc(sc.role)} · ${esc(sc.packName)} · ${esc(sc.track)}</span></div>
        <p class="cxsim-brief">${esc(sc.brief)}</p>
        <div class="cxsim-law">${esc(CXSIM.LAW)}</div>
        <div class="cxsim-lists">
          <div><b>Simulated here</b><ul>${(sc.simulated || []).map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>
          <div><b>Practised live, in the studio</b><ul>${(sc.live || []).map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>
        </div>
        <div class="cxsim-controls">
          <label for="cxsim-diff-${esc(sc.id)}" style="font-size:.8rem">Difficulty</label>
          <select id="cxsim-diff-${esc(sc.id)}" class="cxsim-diff" aria-label="Difficulty">${CXSIM.DIFFICULTY.map(d => `<option value="${d.level}"${d.level === difficulty ? " selected" : ""}>${d.level} · ${esc(d.name)}</option>`).join("")}</select>
          <button class="cxsim-btn gold cxsim-start" type="button">Start the run</button>
          <span class="cxsim-note" style="margin:0">No timer. Every step waits for you.</span>
        </div>
        <div class="cxsim-transfer"><b>What this run is not:</b> the witnessed check for “${esc(sc.track)}” — <i>${esc(sc.transfer.check)}</i> — is done live with an assessor on real material (${esc(sc.transfer.block_id)}, credential “${esc(sc.transfer.credential)}”). ${esc(CXSIM.RUN_NOTE)}</div>`;
      host.querySelector(".cxsim-start").addEventListener("click", () => {
        difficulty = Number(host.querySelector(".cxsim-diff").value) || 1;
        start();
      });
    }

    function start() {
      plan = CXSIM.plan(sc, difficulty, seed);
      choices = new Array(plan.length).fill(null); idx = 0; debrief = []; lastRecord = null;
      renderStep();
    }

    function renderStep() {
      phase = "step";
      const st = plan[idx];
      host.innerHTML = `
        <div class="cxsim-live" aria-live="polite"></div>
        <div class="cxsim-head"><h4>${esc(sc.title)}</h4><span class="cxsim-role">${esc(site)} · difficulty ${difficulty} · seed ${esc(seed)}</span></div>
        <p class="cxsim-prog">Decision ${idx + 1} of ${plan.length}</p>
        <p class="cxsim-prompt${st.kind === "complication" ? " comp" : ""}">${esc(st.prompt)}</p>
        <div class="cxsim-opts" role="group" aria-label="Your options">
          ${st.options.map((o, i) => `<button type="button" class="cxsim-opt" data-i="${i}">${esc(o.t)}</button>`).join("")}
        </div>
        <div class="cxsim-after"></div>`;
      host.querySelectorAll(".cxsim-opt").forEach(b => b.addEventListener("click", () => choose(Number(b.dataset.i))));
      focusPrompt();
    }

    function choose(i) {
      if (phase !== "step") return;
      const st = plan[idx]; const o = st.options[i];
      choices[idx] = i; phase = "consequence";
      host.querySelectorAll(".cxsim-opt").forEach(b => { b.disabled = true; if (Number(b.dataset.i) === i) b.classList.add("picked"); });
      const label = o.s === 2 ? "Held" : (o.s === 1 ? "Partly" : "Missed");
      const after = host.querySelector(".cxsim-after");
      after.innerHTML = `<div class="cxsim-cons"><span class="s${o.s}">${label} · ${esc(discName(o.d))}</span> — ${esc(o.c)}</div>
        <div class="cxsim-controls"><button type="button" class="cxsim-btn gold cxsim-next">${idx + 1 < plan.length ? "Next decision" : "Debrief"}</button></div>`;
      announce(label + ". " + o.c);
      const nb = after.querySelector(".cxsim-next");
      nb.addEventListener("click", () => { idx++; if (idx < plan.length) renderStep(); else renderDebrief(); });
      nb.focus();
    }

    function renderDebrief() {
      phase = "debrief";
      const r = CXSIM.score(plan, choices);
      host.innerHTML = `
        <div class="cxsim-live" aria-live="polite"></div>
        <div class="cxsim-result"><h4>Debrief — ${esc(sc.title)}</h4>
        <p class="cxsim-prog">${r.score} of ${r.max} · ${r.pct}% · difficulty ${difficulty} · ${plan.filter(p => p.kind === "complication").length} complication(s)</p>
        <div class="cxsim-bars">${Object.entries(r.byDiscipline).map(([d, v]) => `<div class="cxsim-bar"><span>${esc(discName(d))}</span><i><b style="width:${v.max ? Math.round(100 * v.got / v.max) : 0}%"></b></i><span>${v.got}/${v.max}</span></div>`).join("")}</div>
        <div class="cxsim-debrief">${(sc.debrief || []).map((q, i) => `<label for="cxsim-db-${esc(sc.id)}-${i}">${esc(q)}</label><textarea id="cxsim-db-${esc(sc.id)}-${i}" data-i="${i}" placeholder="Say it out loud first, then write it — or leave it for the conversation with your teacher."></textarea>`).join("")}</div>
        <p class="cxsim-note"><b>Next:</b> ${nextText(r.pct)}</p>
        <p class="cxsim-note">${esc(CXSIM.RUN_NOTE)}</p>
        <div class="cxsim-controls">
          <button type="button" class="cxsim-btn gold cxsim-finish">Keep this run as practice</button>
          <button type="button" class="cxsim-btn cxsim-export">Show the run record</button>
          <button type="button" class="cxsim-btn cxsim-again">Run again</button>
          <button type="button" class="cxsim-btn cxsim-back">Back to the brief</button>
        </div>
        <textarea class="cxsim-json" readonly aria-label="cx-simrun/1 record"></textarea></div>`;
      host.querySelectorAll(".cxsim-debrief textarea").forEach(t => t.addEventListener("input", () => { debrief[Number(t.dataset.i)] = t.value; }));
      host.querySelector(".cxsim-export").addEventListener("click", () => {
        const ta = host.querySelector(".cxsim-json"); ta.value = JSON.stringify(record(), null, 1); ta.classList.add("show"); ta.focus(); ta.select();
      });
      host.querySelector(".cxsim-again").addEventListener("click", () => { seed = String(Number(seed) + 1 || Date.now()); start(); });
      host.querySelector(".cxsim-back").addEventListener("click", renderIntro);
      host.querySelector(".cxsim-finish").addEventListener("click", () => {
        lastRecord = record();
        const b = host.querySelector(".cxsim-finish"); b.disabled = true; b.textContent = "Kept as practice";
        announce("Run kept as practice. It is not a check and not a credential.");
        if (typeof opts.onRun === "function") opts.onRun(lastRecord);
      });
      focusPrompt();
    }
    function nextText(pct) {
      const n = CXSIM.nextDifficulty(pct, difficulty);
      const name = l => (CXSIM.DIFFICULTY.find(d => d.level === l) || {name: ""}).name;
      if (n > difficulty) return `a clean run — try difficulty ${n} (${name(n)}) next, or take the same scenario to the bench and the witnessed check.`;
      if (n < difficulty) return `run difficulty ${n} (${name(n)}) again before adding complications.`;
      return `run this difficulty once more with a new seed; the complications land somewhere else.`;
    }
    function record() {
      const r = CXSIM.score(plan, choices);
      return {
        format: "cx-simrun/1",
        scenario: sc.id, title: sc.title, pack: sc.pack, track: sc.track, site,
        difficulty, seed, at: new Date().toISOString().slice(0, 10),
        decisions: plan.map((st, i) => ({id: st.id, kind: st.kind, choice: choices[i], score: choices[i] == null ? null : st.options[choices[i]].s, discipline: choices[i] == null ? null : st.options[choices[i]].d})),
        score: r.score, max: r.max, pct: r.pct, byDiscipline: r.byDiscipline,
        next: CXSIM.nextDifficulty(r.pct, difficulty),
        debrief: (sc.debrief || []).map((q, i) => ({q, a: debrief[i] || ""})),
        transfer: {block_id: sc.transfer.block_id, credential: sc.transfer.credential, done_here: false},
        note: CXSIM.RUN_NOTE
      };
    }

    renderIntro();
    return {
      start, record, destroy() { host.innerHTML = ""; host.classList.remove("cxsim"); },
      get plan() { return plan; }, get phase() { return phase; }
    };
  };

  /* A picker + host pair for apps that list several scenarios. */
  CXSIM.mountLibrary = function (host, scenarios, opts) {
    injectCSS();
    opts = opts || {};
    const siteFor = opts.siteFor || (sc => sc.site_default);
    host.innerHTML = `<div class="cxsim-controls" style="margin-bottom:10px">
      <label for="${esc(opts.id || "cxsim-pick")}" style="font-size:.8rem">Scenario</label>
      <select id="${esc(opts.id || "cxsim-pick")}" class="cxsim-pick" aria-label="Scenario">${scenarios.map((s, i) => `<option value="${i}">${esc(s.title)} — ${esc(s.track)}</option>`).join("")}</select>
      <button type="button" class="cxsim-btn gold cxsim-open">Open</button></div><div class="cxsim-host"></div>`;
    const open = () => {
      const s = scenarios[Number(host.querySelector(".cxsim-pick").value) || 0];
      CXSIM.mount(host.querySelector(".cxsim-host"), s, {site: siteFor(s), difficulty: opts.difficulty, seed: opts.seed, onRun: opts.onRun});
    };
    host.querySelector(".cxsim-open").addEventListener("click", open);
    if (opts.autoOpen !== false) open();
    return {open};
  };

  global.CXSIM = CXSIM;
})(typeof window !== "undefined" ? window : globalThis);
