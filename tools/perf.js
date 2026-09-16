#!/usr/bin/env node
/* Measure every app the way a hall's browser experiences it: bytes on disk,
 * gzip bytes (what a hosted copy sends), time from navigation to `load`,
 * time to the first rendered content, script evaluation time, and JS heap
 * after settle. Chromium via Playwright, file:// URLs, three runs each,
 * the median reported. Prints a Markdown table; --json writes the numbers.
 *
 *   NODE_PATH=$(npm root -g) node tools/perf.js [--json out.json] [--runs 3]
 *
 * Numbers are one machine's; the budget the tests hold is on bytes, which
 * do not vary. docs/PERFORMANCE.md carries the last measured table. */
"use strict";
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), zlib = require("zlib");
const ROOT = path.resolve(__dirname, "..");
const APPS = [
  ["education-os", () => document.querySelector(".view.active") && document.querySelector(".view.active").textContent.trim().length > 500],
  ["flow-hub", () => document.body.textContent.trim().length > 2000],
  ["louisiana", () => document.body.textContent.trim().length > 2000],
  ["platform", () => document.body.textContent.trim().length > 1500],
  ["states", () => document.body.textContent.trim().length > 1500],
  ["trades-network", () => document.body.textContent.trim().length > 1500],
];
const median = a => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; };
(async () => {
  const args = process.argv.slice(2);
  const runs = args.includes("--runs") ? +args[args.indexOf("--runs") + 1] : 3;
  const jsonOut = args.includes("--json") ? args[args.indexOf("--json") + 1] : null;
  const browser = await chromium.launch({ executablePath: process.env.CX_CHROMIUM || "/opt/pw-browsers/chromium" });
  const rows = [];
  for (const [app, ready] of APPS) {
    const file = path.join(ROOT, "apps", app, "index.html");
    const buf = fs.readFileSync(file);
    const bytes = buf.length, gz = zlib.gzipSync(buf, { level: 9 }).length;
    const samples = { load: [], first: [], script: [], heap: [] };
    for (let r = 0; r < runs; r++) {
      const page = await browser.newPage();
      const client = await page.context().newCDPSession(page);
      await client.send("Performance.enable");
      const t0 = Date.now();
      await page.goto("file://" + file, { waitUntil: "load" });
      const tLoad = Date.now() - t0;
      await page.waitForFunction(ready, null, { timeout: 30000 });
      const tFirst = Date.now() - t0;
      await page.waitForTimeout(600);
      const m = (await client.send("Performance.getMetrics")).metrics;
      const get = n => (m.find(x => x.name === n) || {}).value || 0;
      samples.load.push(tLoad); samples.first.push(tFirst);
      samples.script.push(Math.round(get("ScriptDuration") * 1000));
      samples.heap.push(Math.round(get("JSHeapUsedSize") / 1048576));
      await page.close();
    }
    rows.push({ app, bytes, gzip: gz, load_ms: median(samples.load), first_ms: median(samples.first), script_ms: median(samples.script), heap_mb: median(samples.heap) });
    process.stderr.write(`  ${app}: ${(bytes / 1e6).toFixed(2)} MB, gzip ${(gz / 1e6).toFixed(2)} MB, load ${median(samples.load)} ms, first content ${median(samples.first)} ms, script ${median(samples.script)} ms, heap ${median(samples.heap)} MB\n`);
  }
  await browser.close();
  console.log("| App | Bytes | Gzip | Load | First content | Script eval | JS heap |");
  console.log("|---|---:|---:|---:|---:|---:|---:|");
  for (const r of rows) console.log(`| ${r.app} | ${(r.bytes / 1e6).toFixed(2)} MB | ${(r.gzip / 1e6).toFixed(2)} MB | ${r.load_ms} ms | ${r.first_ms} ms | ${r.script_ms} ms | ${r.heap_mb} MB |`);
  if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify({ runs, measured: new Date().toISOString().slice(0, 10), rows }, null, 1));
})();
