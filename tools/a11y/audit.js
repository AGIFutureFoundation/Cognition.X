/**
 * Accessibility audit — axe-core over every view of every app, plus a
 * keyboard sweep. Writes docs/ACCESSIBILITY.json (machine) and prints a
 * summary; docs/ACCESSIBILITY.md is written by hand from the findings.
 *
 *     node tools/a11y/audit.js            # all apps
 *     node tools/a11y/audit.js louisiana  # one app
 *
 * Needs Playwright + Chromium (CX_CHROMIUM) and axe-core (npm i -g axe-core;
 * AXE_PATH overrides). Rules run at WCAG 2.2 A/AA tags. Nothing is fetched.
 */
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const AXE = process.env.AXE_PATH || (() => { try { return require.resolve('axe-core/axe.min.js'); } catch (e) { return path.join(require('child_process').execSync('npm root -g').toString().trim(), 'axe-core', 'axe.min.js'); } })();
const url = (app, hash = '') => 'file://' + path.join(ROOT, 'apps', app, 'index.html') + hash;

// the Education OS's 149 views are a literal `const VIEWS=[[id,title,group,
// section],...]` array in the built app, not a route table this file can
// hand-list; read it directly (was sampled at 8 of 149 through v0.112.0)
function educationOsRoutes() {
  const html = fs.readFileSync(path.join(ROOT, 'apps', 'education-os', 'index.html'), 'utf8');
  const m = html.match(/const VIEWS=(\[\[.*?\]\]);/s);
  if (!m) throw new Error('education-os: could not find the VIEWS array to enumerate routes');
  const arr = JSON.parse(m[1].replace(/'/g, '"')); // safe: no apostrophe appears in any VIEWS string (checked)
  if (arr.length < 100) throw new Error(`education-os: parsed only ${arr.length} views, expected ~149 — an apostrophe may have broken the quote swap`);
  return arr.map(v => '#/' + v[0]);
}
// every route of every app (hash routes)
const VIEWS = {
  'louisiana': ['#/state', '#/parish/east-baton-rouge', '#/regions', '#/roles', '#/institute', '#/makers', '#/machines', '#/curriculum'],
  'flow-hub': ['#'],
  'trades-network': ['#'],
  'states': ['#/nation', '#/states', '#/state/LA', '#/blueprint', '#/institute', '#/adoption', '#/compliance'],
  'platform': ['#/model', '#/loop', '#/apps', '#/stack'],
  'education-os': educationOsRoutes(),
};
// the three Louisiana-family apps carry five visual styles (Enterprise
// default plus Parade, Classic, Bayou, Gallery) as a `data-style` attribute
// on <html>, switched instantly with no reload; the rest ship one style
const STYLE_NAMES = ['parade', 'classic', 'bayou', 'gallery'];
const STYLES = { 'louisiana': STYLE_NAMES, 'states': STYLE_NAMES, 'trades-network': STYLE_NAMES };
// in-app view switches that are not hash routes
const CLICKS = {
  'flow-hub': ['.navbtn[data-view="packs"]', '.navbtn[data-view="flow"]', '.navbtn[data-view="agents"]', '.navbtn[data-view="ledger"]', '.navbtn[data-view="author"]'],
  'trades-network': ['.tab[data-r="regions"]', '.tab[data-r="unions"]', '.tab[data-r="sims"]', '.tab[data-r="flipped"]', '.tab[data-r="districts"]'],
  'louisiana#/roles': ['#rolechips [data-role="teacher"]', '#rolechips [data-role="assessor"]', '#rolechips [data-role="parent"]', '#rolechips [data-role="homeschool"]', '#rolechips [data-role="parishadmin"]', '#rolechips [data-role="stateadmin"]'],
};
// views that need in-page steps first (v0.71.0): the studio open on a scenario, then the WebXR room
const STEPS = {
  'trades-network': [
    ['studio open', async page => { await page.evaluate(() => openSim(Object.keys(simByKind)[0], D.regions[0].id)); }],
    ['studio → Open in 3D / VR', async page => { await page.evaluate(() => openSim(Object.keys(simByKind)[0], D.regions[0].id)); await page.waitForTimeout(300); await page.click('#simhost .cxsim-xr'); }],
  ],
};
const only = process.argv[2];

(async () => {
  const axeSrc = fs.readFileSync(AXE, 'utf8');
  const b = await chromium.launch({ executablePath: process.env.CX_CHROMIUM || '/opt/pw-browsers/chromium' });
  const page = await b.newPage({ viewport: { width: 1280, height: 900 } });
  const report = { generated: new Date().toISOString().slice(0, 10), axe: null, runs: [] };
  async function run(label, u, click, steps, style) {
    await page.goto('about:blank'); await page.goto(u); await page.waitForTimeout(u.includes('education-os') ? 2500 : 900);
    if (style) { await page.evaluate(s => { document.documentElement.dataset.style = s; }, style); await page.waitForTimeout(150); }
    if (click) { await page.click(click); await page.waitForTimeout(700); }
    if (steps) { await steps(page); await page.waitForTimeout(700); }
    await page.addScriptTag({ content: axeSrc });
    const r = await page.evaluate(async () => {
      const res = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] }, resultTypes: ['violations', 'incomplete'] });
      return { version: axe.version, violations: res.violations.map(v => ({ id: v.id, impact: v.impact, tags: v.tags.filter(t => /wcag|best/.test(t)), help: v.help, nodes: v.nodes.length, sample: v.nodes.slice(0, 3).map(n => n.target.join(' ')) })), incomplete: res.incomplete.length };
    });
    // keyboard sweep: tab through up to 400 stops, record focusable elements without a visible focus style or accessible name
    const kb = await page.evaluate(() => {
      const els = [...document.querySelectorAll('a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"]),[role="button"]')].filter(e => e.offsetParent !== null && !e.disabled);
      const noName = els.filter(e => { const n = (e.getAttribute('aria-label') || e.getAttribute('aria-labelledby') || e.textContent || e.getAttribute('title') || e.getAttribute('placeholder') || (e.labels && e.labels.length ? 'labelled' : '') || '').trim(); return !n; }).slice(0, 8).map(e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : ''));
      const clickOnly = [...document.querySelectorAll('div[onclick],span[onclick],div.chip,span.chip')].filter(e => e.offsetParent !== null && !e.hasAttribute('tabindex') && !e.closest('button,a,[role="button"]') && (e.onclick || e.getAttribute('onclick'))).length;
      return { focusable: els.length, noName, clickOnly };
    });
    report.axe = r.version;
    // stored relative to ROOT: an absolute file:// URL bakes in the checkout
    // path, which differs between a local clone and a CI runner and would
    // make every CI re-run diff against the committed file on that alone.
    report.runs.push({ label, url: u.replace('file://' + ROOT, ''), click: click || null, style: style || 'enterprise', violations: r.violations, incomplete: r.incomplete, keyboard: kb });
    const crit = r.violations.filter(v => v.impact === 'critical' || v.impact === 'serious').length;
    console.log(`${label.padEnd(44)} violations ${String(r.violations.length).padStart(2)} (serious+ ${crit}) · focusable ${kb.focusable} · unnamed ${kb.noName.length}`);
  }
  for (const [app, hashes] of Object.entries(VIEWS)) {
    if (only && app !== only) continue;
    for (const h of hashes) {
      await run(`${app} ${h}`, url(app, h));
      for (const c of (CLICKS[app + h] || (h === '#' ? CLICKS[app] : null) || [])) await run(`${app} ${h} → ${c}`, url(app, h), c);
    }
    for (const [name, steps] of (STEPS[app] || [])) await run(`${app} ${name}`, url(app, '#/sims'), null, steps);
    // every route (and its clicks/steps) again under each non-default style
    for (const style of (STYLES[app] || [])) {
      for (const h of hashes) {
        await run(`${app} ${h} [${style}]`, url(app, h), null, null, style);
        for (const c of (CLICKS[app + h] || (h === '#' ? CLICKS[app] : null) || [])) await run(`${app} ${h} → ${c} [${style}]`, url(app, h), c, null, style);
      }
      for (const [name, steps] of (STEPS[app] || [])) await run(`${app} ${name} [${style}]`, url(app, '#/sims'), null, steps, style);
    }
  }
  await b.close();
  const out = path.join(ROOT, 'docs', 'ACCESSIBILITY.json');
  fs.writeFileSync(out, JSON.stringify(report, null, 1));
  const totals = {}; report.runs.forEach(r => r.violations.forEach(v => { totals[v.id] = (totals[v.id] || 0) + v.nodes; }));
  console.log('\nby rule (nodes):', Object.entries(totals).sort((a, b) => b[1] - a[1]).map(([k, v]) => `${k}:${v}`).join('  '));
  console.log('wrote', path.relative(ROOT, out));
})();
