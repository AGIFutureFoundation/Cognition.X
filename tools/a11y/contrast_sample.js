/**
 * Contrast pixel sampler — measures the axe "needs review" color-contrast
 * items a mechanical audit cannot resolve on its own (gradient, image or
 * composited backgrounds axe cannot compute a single background colour
 * for). Re-runs docs/ACCESSIBILITY.json's own runs, re-derives each
 * flagged node's foreground colour from the page, samples the actually
 * rendered background pixels around it from a real screenshot, and
 * computes the WCAG contrast ratio itself instead of leaving the finding
 * "spot-checked by hand".
 *
 *     node tools/a11y/audit.js               # first, to refresh the input
 *     node tools/a11y/contrast_sample.js     # then this, writes
 *                                             # docs/ACCESSIBILITY_CONTRAST.json
 *
 * Up to 5 nodes per flagged rule instance are sampled (instances routinely
 * bundle 50-150 near-identical map-label nodes sharing the same computed
 * colours; sampling all of them measures nothing a handful doesn't already
 * show). Needs Playwright + Chromium + axe-core, same as audit.js.
 *
 * Replays a run's `url`, `style` and `click` (all serialisable data in
 * docs/ACCESSIBILITY.json); it cannot replay audit.js's in-page `steps`
 * closures (the Trades Network studio/XR views), so a flagged instance
 * that only appears after such a step is silently skipped rather than
 * measured against the wrong page state.
 */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const AXE = process.env.AXE_PATH || (() => { try { return require.resolve('axe-core/axe.min.js'); } catch (e) { return path.join(require('child_process').execSync('npm root -g').toString().trim(), 'axe-core', 'axe.min.js'); } })();
const MAX_PER_INSTANCE = 5;

function relLum([r, g, b]) {
  const f = c => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
}
function contrastRatio(a, b) {
  const l1 = relLum(a), l2 = relLum(b);
  const hi = Math.max(l1, l2), lo = Math.min(l1, l2);
  return (hi + 0.05) / (lo + 0.05);
}

(async () => {
  const acc = JSON.parse(fs.readFileSync(path.join(ROOT, 'docs', 'ACCESSIBILITY.json'), 'utf8'));
  const axeSrc = fs.readFileSync(AXE, 'utf8');
  const b = await chromium.launch({ executablePath: process.env.CX_CHROMIUM || '/opt/pw-browsers/chromium' });
  const page = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const results = [];
  let measured = 0, below = 0, unresolved = 0;

  for (const run of acc.runs) {
    if (!run.incomplete) continue;
    const u = 'file://' + path.join(ROOT, run.url.replace(/^\//, ''));
    await page.goto('about:blank'); await page.goto(u);
    await page.waitForTimeout(u.includes('education-os') ? 2500 : 900);
    if (run.style && run.style !== 'enterprise') { await page.evaluate(s => { document.documentElement.dataset.style = s; }, run.style); await page.waitForTimeout(150); }
    if (run.click) { await page.click(run.click); await page.waitForTimeout(700); }
    await page.addScriptTag({ content: axeSrc });
    const targets = await page.evaluate(async (maxPer) => {
      const res = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] }, resultTypes: ['incomplete'] });
      const cc = res.incomplete.filter(v => v.id === 'color-contrast');
      const out = [];
      for (const v of cc) for (const n of v.nodes.slice(0, maxPer)) out.push(n.target[n.target.length - 1]);
      return out;
    }, MAX_PER_INSTANCE);
    if (!targets.length) continue;
    const shot = await page.screenshot();
    const sampled = await page.evaluate(async ({ b64, targets }) => {
      function parseColor(s) { const m = (s || '').match(/[\d.]+/g); return m && m.length >= 3 ? m.slice(0, 3).map(Number) : null; }
      const img = new Image();
      const loaded = new Promise((res, rej) => { img.onload = res; img.onerror = rej; });
      img.src = 'data:image/png;base64,' + b64;
      await loaded;
      const canvas = document.createElement('canvas');
      canvas.width = img.naturalWidth; canvas.height = img.naturalHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0);
      const scale = img.naturalWidth / window.innerWidth;
      const out = [];
      for (const sel of targets) {
        let el;
        try { el = document.querySelector(sel); } catch (e) { out.push({ sel, error: 'unsupported selector' }); continue; }
        if (!el) { out.push({ sel, error: 'not found' }); continue; }
        const cs = getComputedStyle(el);
        const isSvg = el.namespaceURI === 'http://www.w3.org/2000/svg';
        const fg = parseColor(isSvg && cs.fill !== 'none' ? cs.fill : cs.color);
        const rect = el.getBoundingClientRect();
        if (!fg || rect.width < 1 || rect.height < 1) { out.push({ sel, error: 'no geometry or foreground colour' }); continue; }
        const x0 = Math.max(0, Math.floor(rect.left * scale)), y0 = Math.max(0, Math.floor(rect.top * scale));
        const w = Math.min(canvas.width - x0, Math.ceil(rect.width * scale)), h = Math.min(canvas.height - y0, Math.ceil(rect.height * scale));
        let data;
        try { data = w > 0 && h > 0 ? ctx.getImageData(x0, y0, w, h).data : null; } catch (e) { data = null; }
        if (!data) { out.push({ sel, error: 'clip out of bounds' }); continue; }
        // background estimate: the most common pixel colour at least 60
        // (Manhattan, 0-765) away from the known foreground -- close
        // pixels are the glyph/fill itself or its anti-aliasing
        const buckets = new Map();
        for (let i = 0; i < data.length; i += 4) {
          const r = data[i], g = data[i + 1], bl = data[i + 2];
          if (Math.abs(r - fg[0]) + Math.abs(g - fg[1]) + Math.abs(bl - fg[2]) < 60) continue;
          const key = (r >> 4) + ',' + (g >> 4) + ',' + (bl >> 4);
          buckets.set(key, (buckets.get(key) || 0) + 1);
        }
        if (!buckets.size) { out.push({ sel, error: 'no background pixels resolved (element fills its own box)' }); continue; }
        let bestKey = null, bestCount = -1;
        for (const [k, c] of buckets) if (c > bestCount) { bestCount = c; bestKey = k; }
        const bg = bestKey.split(',').map(v => parseInt(v, 10) * 16 + 8);
        const size = parseFloat(cs.fontSize) || 0;
        const weight = parseInt(cs.fontWeight, 10) || 400;
        const large = size >= 24 || (size >= 18.66 && weight >= 700);
        out.push({ sel, fg: fg.map(Math.round), bg, fontSize: Math.round(size * 10) / 10, large });
      }
      return out;
    }, { b64: shot.toString('base64'), targets });
    for (const s of sampled) {
      if (s.error) { unresolved++; results.push({ label: run.label, ...s }); continue; }
      const ratio = Math.round(contrastRatio(s.fg, s.bg) * 100) / 100;
      const threshold = s.large ? 3 : 4.5;
      measured++;
      if (ratio < threshold) below++;
      results.push({ label: run.label, sel: s.sel, fg: s.fg, bg: s.bg, ratio, threshold, pass: ratio >= threshold });
    }
  }
  await b.close();
  const out = { generated: new Date().toISOString().slice(0, 10), maxPerInstance: MAX_PER_INSTANCE, measured, below, unresolved, results };
  fs.writeFileSync(path.join(ROOT, 'docs', 'ACCESSIBILITY_CONTRAST.json'), JSON.stringify(out, null, 1));
  console.log(`measured ${measured} nodes, ${below} below their WCAG threshold, ${unresolved} unresolved (no usable background pixels)`);
  if (below) for (const r of results.filter(r => r.pass === false)) console.log(`  ${r.label} ${r.sel}: ${r.ratio}:1 (needs ${r.threshold}:1) fg=rgb(${r.fg}) bg~rgb(${r.bg})`);
  console.log('wrote docs/ACCESSIBILITY_CONTRAST.json');
})();
