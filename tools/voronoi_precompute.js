#!/usr/bin/env node
/* Precompute the Louisiana app's two Voronoi maps at build time (v0.68.0).
 *
 * The state map (64 parishes in 8 regions, cell area ∝ population) and the
 * curriculum map (packs by family, cell area ∝ blocks) are relaxed power
 * diagrams on a 132×90 grid — deterministic functions of the build data,
 * and the single largest cost of the app's startup (about 240 ms of the
 * 270 ms of script on a laptop). This tool runs the app's OWN code — the
 * region between the @cx-voronoi markers in the template, unmodified — on
 * the build payload, and emits both assignment grids run-length encoded.
 * The app decodes them at load and falls back to computing when they are
 * absent; the browser suite asserts the decoded grids equal a fresh
 * computation, so the two can never drift.
 *
 *   node tools/voronoi_precompute.js apps/louisiana/template.html payload.json
 */
"use strict";
const fs = require("fs");
const [tplPath, payloadPath] = process.argv.slice(2);
if (!tplPath || !payloadPath) { console.error("usage: voronoi_precompute.js <template.html> <payload.json>"); process.exit(2); }
const tpl = fs.readFileSync(tplPath, "utf8");
const region = (a, b) => { const i = tpl.indexOf(a), j = tpl.indexOf(b, i); if (i < 0 || j < 0) throw new Error("marker not found: " + a); return tpl.slice(i + a.length, j); };
const slugFn = (() => { const i = tpl.indexOf("const slug = "); if (i < 0) throw new Error("slug helper not found"); const j = tpl.indexOf("\n", i); return tpl.slice(i, j); })();
const vor = region("/* @cx-voronoi-begin */", "/* @cx-voronoi-end */");
const D = JSON.parse(fs.readFileSync(payloadPath, "utf8"));
const rle = a => { const out = []; let cur = a[0], n = 0; for (const v of a) { if (v === cur) n++; else { out.push([cur, n]); cur = v; n = 1; } } out.push([cur, n]); return out; };
const fn = new Function("D", "rle", slugFn + "\nD.parishes.forEach(p => p.slug = slug(p.name));\n" + vor + `
  const pack = t => ({gw: t.gw, gh: t.gh, g: rle(t.gAssign), m: rle(t.mAssign)});
  return {state: pack(voronoiTessellate(stateVoronoiGroups(), 560, 380, 24)),
          curr: pack(voronoiTessellate(currVoronoiGroups(), 560, 380, 24))};`);
process.stdout.write(JSON.stringify(fn(D, rle)));
