#!/usr/bin/env node
/* Render every view of the Education OS and hash what each one draws.
 *
 * The claim behind v0.63.0 and v0.68.0 — "every one of the 149 views renders
 * identically before and after" — was made with a script that lived outside
 * the repository. This is that script, so the claim can be re-run from a
 * clone. Two modes:
 *
 *   node tools/view_sweep.js apps/education-os/index.html out.json
 *       walks every route in the app's own VIEWS table, records the length
 *       and SHA-256 of each view's innerHTML, page errors and timeouts
 *   node tools/view_sweep.js --compare before.json after.json [--show]
 *       reports which views differ; known nondeterminism (random gradient
 *       ids, the live-feed lines, the accessibility marker's timing) is
 *       normalised before hashing so only real changes show
 *
 * Playwright + Chromium (CX_CHROMIUM). Nothing is fetched. A view that
 * blocks the page for 8 s is recorded as a timeout and the page reopened. */
"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const T = ms => new Promise((_, rej) => setTimeout(() => rej(new Error("timeout")), ms));
// strip what legitimately differs between two renders of the same view
const normalise = h => h
  .replace(/ha\w*?\d+[sg]\b/g, "ha#")                       // random gradient ids
  .replace(/\s*tabindex="0" aria-label="Scrollable content"/g, "") // a11y marker, applied after a timer
  .replace(/\d{1,2}:\d{2}(:\d{2})?\s*(AM|PM)?/g, "hh:mm");     // live clocks and feed timestamps
const sha = s => crypto.createHash("sha256").update(s).digest("hex").slice(0, 16);

async function sweep(file, outFile) {
  const { chromium } = require("playwright");
  const html = fs.readFileSync(file, "utf8");
  const i = html.indexOf("const VIEWS=["); const j = html.indexOf("];", i);
  if (i < 0 || j < 0) throw new Error("no VIEWS table in " + file);
  const VIEWS = eval("(" + html.slice(i + 12, j + 1) + ")").map(v => v[0]);
  const browser = await chromium.launch({ executablePath: process.env.CX_CHROMIUM || "/opt/pw-browsers/chromium" });
  const errs = [], out = {}; let page = null; const t0 = Date.now();
  const fresh = async () => {
    if (page) { try { await Promise.race([page.close(), T(3000)]); } catch (e) { /* stuck page */ } }
    page = await browser.newPage(); page.on("pageerror", e => errs.push(e.message.slice(0, 120)));
    await page.goto("file://" + path.resolve(file)); await page.waitForTimeout(1200);
  };
  await fresh();
  for (let k = 0; k < VIEWS.length; k++) {
    const id = VIEWS[k];
    if (k && k % 20 === 0) await fresh();
    try {
      const h = await Promise.race([(async () => {
        await page.evaluate(id => { location.hash = "#/" + id; }, id);
        await page.waitForTimeout(150);
        return page.evaluate(id => { const v = document.getElementById("v-" + id); return v ? v.innerHTML : null; }, id);
      })(), T(8000)]);
      out[id] = h == null ? null : { len: h.length, sha: sha(normalise(h)) };
    } catch (e) { out[id] = { error: e.message }; await fresh(); }
    process.stderr.write(`  ${k + 1}/${VIEWS.length} ${id} ${out[id] ? (out[id].error || out[id].len) : "null"} ${((Date.now() - t0) / 1000).toFixed(1)}s\n`);
  }
  await browser.close();
  const empty = Object.values(out).filter(v => v && !v.error && v.len < 40).length;
  fs.writeFileSync(outFile, JSON.stringify({ file: path.basename(file), views: out, errs }, null, 1));
  console.log(`${path.basename(file)}: ${VIEWS.length} views, ${errs.length} page errors, ${Object.values(out).filter(v => v && v.error).length} timeouts, ${empty} empty`);
  return errs.length || empty ? 1 : 0;
}

function compare(a, b, show) {
  const A = JSON.parse(fs.readFileSync(a, "utf8")), B = JSON.parse(fs.readFileSync(b, "utf8"));
  let same = 0; const diff = [];
  for (const id of Object.keys(A.views)) { const x = A.views[id], y = B.views[id]; if (x && y && x.sha === y.sha) same++; else diff.push(id); }
  console.log(`same ${same}, different ${diff.length}${diff.length ? ": " + diff.join(", ") : ""}`);
  if (show) for (const id of diff) console.log(`  ${id}: ${JSON.stringify(A.views[id])} → ${JSON.stringify(B.views[id])}`);
  return diff.length ? 1 : 0;
}

(async () => {
  const args = process.argv.slice(2);
  if (args[0] === "--compare") process.exit(compare(args[1], args[2], args.includes("--show")));
  if (args.length < 2) { console.error("usage: view_sweep.js <app.html> <out.json> | --compare <before.json> <after.json> [--show]"); process.exit(2); }
  process.exit(await sweep(args[0], args[1]));
})();
