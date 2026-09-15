/* Cognition.X — the Data & privacy notice (v0.55.0).
 *
 * Injected into every app with the shared runtime. Adds one small fixed
 * control ("Data & privacy") that opens an accessible dialog built from
 * the canonical text in data/policy/privacy.json (window.CX_PRIVACY) and
 * the app's own storage prefixes (window.CX_APP.prefixes):
 *
 *   - lists every localStorage key this app has written, with its size;
 *   - states what stays, what leaves (nothing, by itself) and the rights
 *     a person has over what is stored;
 *   - offers one erase-all control for this app's keys, behind a confirm.
 *
 * No network, no timers, no third-party code. Styles use the host's
 * tokens with fallbacks. The dialog is a real <dialog> with a labelled
 * heading, Escape closes it, and focus returns to the control.
 */
(function () {
  "use strict";
  if (typeof document === "undefined") return;
  const P = window.CX_PRIVACY, A = window.CX_APP || {};
  if (!P || !Array.isArray(A.prefixes)) return;
  const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

  const CSS = `
  #cx-privbtn{position:fixed;right:12px;bottom:12px;z-index:80;font:600 .74rem/1 system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:.02em;
    border:1px solid var(--line,#c9d1d9);background:var(--surface,#fff);color:var(--ink,#1c2430);border-radius:999px;padding:9px 13px;cursor:pointer;box-shadow:0 2px 10px rgba(0,0,0,.12)}
  #cx-privbtn:focus-visible{outline:2px solid var(--gold,#7f5a00);outline-offset:2px}
  #cx-privdlg{max-width:min(720px,94vw);border:1px solid var(--line,#c9d1d9);border-radius:14px;padding:0;background:var(--surface,#fff);color:var(--ink,#1c2430);font:.9rem/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
  #cx-privdlg::backdrop{background:rgba(10,16,24,.55)}
  #cx-privdlg .in{padding:20px 22px 18px;max-height:82vh;overflow:auto}
  #cx-privdlg h2{margin:0 0 10px;font-size:1.15rem}
  #cx-privdlg h3{margin:14px 0 4px;font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--faint,#5f6b7a)}
  #cx-privdlg p{margin:0 0 8px}
  #cx-privdlg table{width:100%;border-collapse:collapse;font-size:.8rem;margin:4px 0 8px}
  #cx-privdlg td,#cx-privdlg th{text-align:left;padding:4px 8px 4px 0;border-bottom:1px solid var(--line,#e3e8ee);vertical-align:top}
  #cx-privdlg td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
  #cx-privdlg .row{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
  #cx-privdlg button{font:inherit;border:1px solid var(--line,#c9d1d9);background:var(--surface-2,var(--bg,#f4f6f8));color:var(--ink,#1c2430);border-radius:9px;padding:8px 14px;cursor:pointer}
  #cx-privdlg button.danger{border-color:var(--w4,#a83a3a);color:var(--w4,#a83a3a)}
  #cx-privdlg button:focus-visible{outline:2px solid var(--gold,#7f5a00);outline-offset:2px}
  #cx-privdlg .fine{font-size:.76rem;color:var(--faint,#5f6b7a)}
  #cx-privdlg code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.78rem}
  @media print{#cx-privbtn{display:none}}`;

  function keys() {
    const out = [];
    try {
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (A.prefixes.some(p => k.startsWith(p))) out.push({k, n: (localStorage.getItem(k) || "").length});
      }
    } catch (e) { /* storage unavailable: the table simply shows nothing */ }
    return out.sort((a, b) => a.k.localeCompare(b.k));
  }
  function fmt(n) { return n < 1024 ? n + " B" : (n / 1024).toFixed(1) + " KB"; }

  function build() {
    const st = document.createElement("style"); st.setAttribute("data-cx-privacy", "1"); st.textContent = CSS; document.head.appendChild(st);
    const btn = document.createElement("button"); btn.id = "cx-privbtn"; btn.type = "button"; btn.textContent = "Data & privacy";
    btn.setAttribute("aria-haspopup", "dialog");
    const dlg = document.createElement("dialog"); dlg.id = "cx-privdlg"; dlg.setAttribute("aria-labelledby", "cx-privttl");
    document.body.appendChild(btn); document.body.appendChild(dlg);
    btn.addEventListener("click", () => { render(); if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", ""); });
    function render() {
      const ks = keys(); const total = ks.reduce((s, x) => s + x.n, 0);
      dlg.innerHTML = `<div class="in">
        <h2 id="cx-privttl">${esc(P.title)}</h2>
        <h3>What stays here</h3><p>${esc(P.stays)}</p>
        <table aria-label="Keys this app has stored in this browser"><thead><tr><th>Key</th><th class="n">Size</th></tr></thead><tbody>
        ${ks.length ? ks.map(x => `<tr><td><code>${esc(x.k)}</code></td><td class="n">${fmt(x.n)}</td></tr>`).join("") : `<tr><td colspan="2" class="fine">Nothing stored yet under ${A.prefixes.map(p => "<code>" + esc(p) + "…</code>").join(", ")}.</td></tr>`}
        </tbody></table>
        <p class="fine">${ks.length} key${ks.length === 1 ? "" : "s"} · ${fmt(total)} · app ${esc(A.name || "")} v${esc(A.version || "")}</p>
        <h3>What leaves</h3><p>${esc(P.leaves)}</p><p>${esc(P.exports)}</p>
        <h3>Learners under thirteen</h3><p>${esc(P.minors)}</p>
        <h3>Your rights over it</h3><p>${esc(P.rights)}</p>
        <h3>Security</h3><p>${esc(P.security)}</p>
        <p class="fine">${esc(P.not_advice)} ${esc(P.docs)}</p>
        <div class="row"><button type="button" class="danger" id="cx-priverase" ${ks.length ? "" : "disabled"}>${esc(P.erase_label)}</button>
        <button type="button" id="cx-privclose">Close</button></div>
        <p class="fine" id="cx-privmsg" aria-live="polite"></p></div>`;
      dlg.querySelector("#cx-privclose").addEventListener("click", () => { dlg.close ? dlg.close() : dlg.removeAttribute("open"); btn.focus(); });
      dlg.querySelector("#cx-priverase").addEventListener("click", () => {
        if (!window.confirm(P.erase_confirm)) return;
        try { keys().forEach(x => localStorage.removeItem(x.k)); } catch (e) {}
        dlg.querySelector("#cx-privmsg").textContent = P.erased;
        dlg.querySelector("#cx-priverase").disabled = true;
        setTimeout(() => location.reload(), 900);
      });
    }
    dlg.addEventListener("close", () => btn.focus());
  }
  if (document.body) build(); else document.addEventListener("DOMContentLoaded", build);
})();
