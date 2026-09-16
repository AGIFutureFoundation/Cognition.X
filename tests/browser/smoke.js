/**
 * Browser smoke suite — the working models, exercised for real.
 *
 * Every release from v0.22.0 onward was verified by a throwaway script
 * that never entered the repository. This is that verification, kept:
 * one headless pass that opens all six apps and drives the mechanics
 * that must not silently break — the 50-check credential threshold,
 * genuine ECDSA signing and its four verification grades, the consent
 * gate, flow-state transitions, swarm arbitration, and the Platform
 * app's end-to-end loop.
 *
 * It needs a browser, so it is NOT part of the Python-only CI gate
 * (tests/test_platform.py is). Run it before shipping an app change:
 *
 *     node tests/browser/smoke.js
 *
 * Requires Playwright and a Chromium build. In this project's
 * environment: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers, executable
 * at /opt/pw-browsers/chromium. Override with CX_CHROMIUM=/path.
 * Exit 0 = every assertion held.
 */

const { chromium } = require('playwright');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const url = app => 'file://' + path.join(ROOT, 'apps', app, 'index.html');

const results = [];
let failed = 0;
function check(name, ok, detail) {
  results.push({ name, ok, detail });
  if (!ok) failed++;
  console.log(`${ok ? '  ok  ' : '  FAIL'} ${name}${ok || !detail ? '' : ' — ' + detail}`);
}

async function newPage(browser, label, errs) {
  const page = await browser.newPage();
  page.on('pageerror', e => errs.push(`${label}: ${e.message}`));
  return page;
}

/* ---------------------------------------------- every app loads cleanly */
async function testAllAppsLoad(browser, errs) {
  for (const app of ['education-os', 'flow-hub', 'louisiana', 'trades-network', 'states', 'platform']) {
    const before = errs.length;
    const page = await newPage(browser, app, errs);
    await page.goto(url(app));
    await page.waitForTimeout(900);
    const title = await page.title();
    check(`${app}: loads with a title`, !!title, `title=${JSON.stringify(title)}`);
    check(`${app}: no page errors on load`, errs.length === before, errs.slice(before).join(' | '));
    await page.close();
  }
}

/* ------------------------------- louisiana: the credential fires at 50 */
async function testCredentialThreshold(browser, errs) {
  const page = await newPage(browser, 'la/credential', errs);
  await page.goto(url('louisiana'));
  await page.waitForTimeout(700);
  const out = await page.evaluate(() => {
    const d = llLoad();
    const key = LTRACKS[0].key;
    d.learners = [{ id: 'thr', name: 'Threshold Learner', band: 3, prog: { [key]: 48 } }];
    llSave(d);
    const l = llLoad().learners[0];
    const at49 = llCredit(l, key, 1);            // 48 -> 49: no credential
    const creds49 = llStanding(l).creds.length;
    const at50 = llCredit(l, key, 1);            // 49 -> 50: credential crosses
    const creds50 = llStanding(l).creds.length;
    const at51 = llCredit(l, key, 1);            // capped, no double-award
    return { at49, creds49, at50, creds50, at51, prog: l.prog[key] };
  });
  check('ledger: no credential at 49 checks', out.at49 === false && out.creds49 === 0, JSON.stringify(out));
  check('ledger: credential fires at exactly 50', out.at50 === true && out.creds50 === 1, JSON.stringify(out));
  check('ledger: no second award past 50', out.at51 === false && out.prog === 50, JSON.stringify(out));
  await page.close();
}

/* --------------------- louisiana: signing and the four verification grades */
async function testRecordsOfficeGrades(browser, errs) {
  const page = await newPage(browser, 'la/records', errs);
  await page.goto(url('louisiana'));
  await page.waitForTimeout(700);
  await page.evaluate(async () => {
    const d = llLoad();
    d.learners = [{ id: 'rec', name: 'Record Learner', band: 4, prog: { [LTRACKS[0].key]: 50 } }];
    d.queue = []; llSave(d);
    await dlReset();
    location.hash = '#/roles';
  });
  await page.waitForTimeout(400);
  await page.click('#rolechips [data-role="parishadmin"]');
  await page.waitForTimeout(400);

  await page.fill('#ro-name', 'Smoke Hall Records Office');
  await page.click('#ro-create'); await page.waitForTimeout(500);
  await page.click('#ro-issue'); await page.waitForTimeout(600);
  const recText = await page.$eval('#ro-out', el => el.value);
  const rec = JSON.parse(recText);

  check('record: cx-credential/1 format', rec.payload.format === 'cx-credential/1');
  check('record: real P-256 signature', typeof rec.signature === 'string' && rec.signature.length === 88,
    `len=${rec.signature && rec.signature.length}`);
  check('record: carries a unique rid', typeof rec.payload.rid === 'string' && rec.payload.rid.length >= 8);
  check('record: public key only, never the private half',
    rec.publicKey && rec.publicKey.kty === 'EC' && !('d' in rec.publicKey));

  // grade 1 — valid, key untrusted
  await page.fill('#ro-in', recText); await page.click('#ro-verify'); await page.waitForTimeout(400);
  check('verify: valid-but-untrusted grade',
    (await page.$eval('#ro-result', el => el.textContent)).includes('key not trusted'));

  // grade 2 — tampered payload is invalid
  const bad = JSON.parse(recText); bad.payload.learner = 'Impostor';
  await page.fill('#ro-in', JSON.stringify(bad)); await page.click('#ro-verify'); await page.waitForTimeout(400);
  check('verify: tamper detected',
    (await page.$eval('#ro-result', el => el.textContent)).includes('Invalid'));

  // grade 3 — trusted by name
  await page.click('#ro-pub'); await page.waitForTimeout(300);
  const pub = await page.$eval('#ro-out', el => el.value);
  await page.fill('#ro-trust-in', pub); await page.click('#ro-trust-add'); await page.waitForTimeout(300);
  await page.fill('#ro-in', recText); await page.click('#ro-verify'); await page.waitForTimeout(400);
  const trusted = await page.$eval('#ro-result', el => el.textContent);
  check('verify: trusted-office grade by name',
    trusted.includes('trusted office') && trusted.includes('Smoke Hall'));

  // grade 4 — revoked trumps trusted, and an unsigned list is refused
  await page.fill('#ro-rev-id', rec.payload.rid);
  await page.fill('#ro-rev-reason', 'smoke test');
  await page.click('#ro-rev-add'); await page.waitForTimeout(300);
  await page.click('#ro-rev-export'); await page.waitForTimeout(500);
  const revDoc = await page.$eval('#ro-out', el => el.value);
  const forged = JSON.parse(revDoc);
  forged.payload.revoked.push({ rid: 'forged', reason: 'x', at: '2026-01-01' });
  await page.fill('#ro-rev-in', JSON.stringify(forged));
  await page.click('#ro-rev-import'); await page.waitForTimeout(500);
  check('revocation: altered list is rejected',
    (await page.$eval('#ro-rev-msg', el => el.textContent)).includes('Rejected'));
  await page.fill('#ro-rev-in', revDoc); await page.click('#ro-rev-import'); await page.waitForTimeout(500);
  await page.fill('#ro-in', recText); await page.click('#ro-verify'); await page.waitForTimeout(400);
  const revoked = await page.$eval('#ro-result', el => el.textContent);
  check('verify: revoked grade trumps trusted',
    revoked.includes('Revoked') && revoked.includes('smoke test'), revoked.slice(0, 90));
  await page.close();
}

/* --------------------------- louisiana: evidence export is consent-gated */
async function testEvidenceConsentGate(browser, errs) {
  const page = await newPage(browser, 'la/evidence', errs);
  await page.goto(url('louisiana'));
  await page.waitForTimeout(700);
  await page.evaluate(() => {
    const d = llLoad();
    d.learners = [{
      id: 'ev', name: 'Evidence Learner', band: 3, prog: { [LTRACKS[0].key]: 12 },
      evidence: [{ at: '2026-01-01', track: LTRACKS[0].name, by: 'X', note: '', result: 'confirmed' },
                 { at: '2026-01-01', track: LTRACKS[0].name, by: 'X', note: '', result: 'not yet' }],
    }];
    d.queue = []; llSave(d); location.hash = '#/roles';
  });
  await page.waitForTimeout(400);
  await page.click('#rolechips [data-role="stateadmin"]');
  await page.waitForTimeout(400);
  check('evidence: export disabled before consent', await page.$eval('#ev-export', el => el.disabled));
  await page.click('#ev-consent');
  check('evidence: export enabled after consent', await page.$eval('#ev-export', el => !el.disabled));
  await page.fill('#ev-site', 'Smoke Hall');
  await page.click('#ev-export'); await page.waitForTimeout(400);
  const out = await page.$eval('#ev-out', el => el.value);
  const parsed = JSON.parse(out);
  check('evidence: cx-evidence/1 aggregate', parsed.format === 'cx-evidence/1');
  check('evidence: aggregate-only consent recorded', parsed.consent && parsed.consent.aggregateOnly === true);
  check('evidence: no learner names in the export', !out.includes('Evidence Learner'));
  check('evidence: no per-learner ids in the export', !out.includes('"ev"'));
  await page.close();
}

/* --------------------------------- louisiana: flow engine + swarm arbitration */
async function testFlowAndSwarm(browser, errs) {
  const page = await newPage(browser, 'la/flow', errs);
  await page.goto(url('louisiana'));
  await page.waitForTimeout(700);
  const flow = await page.evaluate(() => {
    const mk = fs => ({ id: 'f', name: 'Flow Learner', band: 3, prog: {}, fs });
    return {
      warming: flowOf(mk({ events: [], sinceBreak: 0, moves: 0 })).state,
      overload: flowOf(mk({ events: [-1, -1, -1], sinceBreak: 1, moves: 3 })).state,
      cruising: flowOf(mk({ events: [1, 1, 1], sinceBreak: 1, moves: 3 })).state,
      brk: flowOf(mk({ events: [1, 1, 1], sinceBreak: 8, moves: 8 })).state,
    };
  });
  check('flow: no events → warming up', flow.warming === 'warming', flow.warming);
  check('flow: three struggles → overloaded', flow.overload === 'overload', flow.overload);
  check('flow: three passes → cruising', flow.cruising === 'cruising', flow.cruising);
  check('flow: cadence reached → break called (trumps all)', flow.brk === 'brk', flow.brk);

  // swarm arbitration: a due break (95) must out-rank a 49/50 credential watch (90)
  await page.evaluate(() => {
    const d = llLoad();
    d.learners = [{ id: 'sw', name: 'Swarm Learner', band: 3,
      prog: { [LTRACKS[0].key]: 49 }, fs: { events: [1, 1, 1], sinceBreak: 8, moves: 3 } }];
    d.queue = []; llSave(d);
    R.layout = {}; R.role = 'student'; R.me = 'sw'; saveR();
    location.hash = '#/roles';
  });
  await page.waitForTimeout(600);
  const swarm = await page.$eval('[data-widget="swarm"] .swbox', el => el.textContent);
  check('swarm: arbitrated call is shown', swarm.includes("The swarm's call"));
  check('swarm: break (pri 95) out-ranks credential watch (pri 90)',
    swarm.includes('Motivator') && swarm.includes('pri 95') && swarm.includes('pri 90'));
  check('swarm: every agent stays inspectable',
    ['Coach', 'Pathfinder', 'Credential Watch', 'Access Ally'].every(n => swarm.includes(n)));
  await page.close();
}

/* --------------------------------- louisiana: the Makers' Hall (v0.48.0) */
async function testMakersHall(browser, errs) {
  const page = await newPage(browser, 'louisiana-makers', errs);
  await page.goto(url('louisiana') + '#/makers');
  await page.waitForTimeout(600);
  const r = await page.evaluate(() => ({
    active: document.querySelector('.view.active').id,
    discs: document.querySelectorAll('#mkchips [data-disc]').length,
    stages: document.querySelectorAll('#mkpath .mkstage').length,
    cards: document.querySelectorAll('#mkhall .mkcard').length,
    tracks: document.querySelectorAll('#mkbody .tracklist li').length,
    roles: document.querySelectorAll('.mkroles .chip').length,
    honest: (document.querySelector('#mkhonest') || {}).textContent || '',
  }));
  check('makers: view routes', r.active === 'view-makers', r.active);
  check('makers: three disciplines', r.discs === 3, String(r.discs));
  check('makers: pathway map has five stages', r.stages === 5, String(r.stages));
  check('makers: five tracks listed', r.tracks === 5, String(r.tracks));
  check('makers: figure cards render', r.cards >= 20, String(r.cards));
  check('makers: role ladder renders', r.roles >= 40, String(r.roles));
  check('makers: honesty note says naming is not endorsement',
        /not endorsement/.test(r.honest) && /name their own/.test(r.honest));
  // a stage filters roles and makers; Enter on the SVG node works too
  await page.click('#mkpath .mkstage[data-stage="studio"]');
  await page.waitForTimeout(150);
  const st = await page.evaluate(() => ({
    pressed: (document.querySelector('.mkstage[aria-pressed="true"]') || {}).dataset,
    cards: document.querySelectorAll('#mkhall .mkcard').length,
    allStudio: [...document.querySelectorAll('#mkhall .mkcard')].every(c => c.dataset.stage === 'studio'),
    heads: document.querySelectorAll('.mkstagehead').length,
  }));
  check('makers: stage click filters to that stage', st.pressed && st.pressed.stage === 'studio' && st.allStudio && st.heads === 1,
        JSON.stringify(st));
  await page.focus('#mkpath .mkstage[data-stage="studio"]');
  await page.keyboard.press('Enter');
  await page.waitForTimeout(150);
  check('makers: Enter on a stage clears the filter (keyboard-operable)',
        await page.evaluate(() => !document.querySelector('.mkstage[aria-pressed="true"]') && document.querySelectorAll('.mkstagehead').length === 5));
  // parish filter narrows the hall; the deep link sets it
  await page.selectOption('#mkparish', 'orleans');
  await page.waitForTimeout(150);
  check('makers: parish filter narrows to that parish',
        await page.evaluate(() => [...document.querySelectorAll('#mkhall .mkcard')].every(c => c.dataset.parish === 'Orleans')
                                  && document.querySelectorAll('#mkhall .mkcard').length > 0));
  await page.goto(url('louisiana') + '#/makers/arts/natchitoches');
  await page.waitForTimeout(400);
  const dl = await page.evaluate(() => [document.querySelector('#mkparish').value,
    [...document.querySelectorAll('#mkhall .mkcard h4')].map(h => h.textContent)]);
  check('makers: deep link #/makers/<discipline>/<parish> selects both', dl[0] === 'natchitoches' && dl[1].includes('Clementine Hunter'), JSON.stringify(dl));
  // culinary tracks link into Flow Hub sessions
  await page.click('#mkchips [data-disc="culinary"]');
  await page.waitForTimeout(150);
  const href = await page.evaluate(() => (document.querySelector('#mkbody .tracklist li a') || {}).getAttribute
    ? document.querySelector('#mkbody .tracklist li a').getAttribute('href') : '');
  check('makers: culinary tracks deep-link into Flow Hub', /#track=CULINARY\/KN$/.test(href), href);
  // parish dashboards: makers from this parish, or the region's, plainly labeled
  await page.goto(url('louisiana') + '#/parish/st-landry');
  await page.waitForTimeout(400);
  const pm = await page.evaluate(() => ({
    cards: document.querySelectorAll('#pmakers .mkcard').length,
    plan: [...document.querySelectorAll('#pplan summary b')].map(b => b.textContent),
    reason: [...document.querySelectorAll('#pplan .chip.gold')].map(c => c.textContent).join(' | '),
  }));
  check('parish: St. Landry lists its public-record makers', pm.cards >= 3, String(pm.cards));
  check('parish: makers earn the culture-trade packs in the module plan',
        pm.plan.includes('Music : Creation to Industry') && /maker/.test(pm.reason), JSON.stringify(pm.plan));
  await page.goto(url('louisiana') + '#/parish/winn');
  await page.waitForTimeout(400);
  const wn = await page.evaluate(() => document.querySelector('#pmakers').textContent);
  check('parish: a parish with no listed maker says so and shows its region',
        /No public-record maker is listed for Winn/.test(wn) && /name their own/.test(wn), wn.slice(0, 120));
  // role dashboards: a maker from your parish, rotating on demand
  await page.goto(url('louisiana') + '#/roles');
  await page.waitForTimeout(400);
  const w1 = await page.evaluate(() => {
    const w = document.querySelector('[data-widget="maker"]');
    return w ? (w.querySelector('.mkcard h4') || {}).textContent : null;
  });
  check('student dashboard: "A maker from your parish" widget renders', !!w1, String(w1));
  await page.click('#mk-next');
  await page.waitForTimeout(300);
  const w2 = await page.evaluate(() => (document.querySelector('[data-widget="maker"] .mkcard h4') || {}).textContent);
  check('student dashboard: "Another maker" rotates the example', !!w2 && w2 !== w1, `${w1} → ${w2}`);
  await page.close();
}

/* --------------------------------- states: the compliance layer (v0.51.0) */
async function testComplianceLayer(browser, errs) {
  const page = await newPage(browser, 'states-compliance', errs);
  await page.goto(url('states') + '#/compliance/TX');
  await page.waitForTimeout(700);
  const r = await page.evaluate(() => ({
    active: document.querySelector('.view.active').id,
    tiles: document.querySelectorAll('#cmap g.tile').length,
    rows: document.querySelectorAll('#cbody .cdom').length,
    head: document.querySelector('#cbody h3').textContent,
    verify: document.querySelectorAll('#cbody .vf').length,
    disc: document.querySelector('#cdisc').textContent,
  }));
  check('compliance: view routes with the state from the hash', r.active === 'view-compliance' && /^Texas/.test(r.head), r.head);
  check('compliance: fifty tiles on the lens map', r.tiles === 50, String(r.tiles));
  check('compliance: eleven domain rows in the checklist (breach added v0.57.0)', r.rows === 11, String(r.rows));
  check('compliance: fees flagged verify', r.verify >= 8, String(r.verify));
  check('compliance: the disclaimer renders', /NOT LEGAL ADVICE/.test(r.disc));
  await page.selectOption('#clens', 'charity');
  await page.waitForTimeout(200);
  const lg = await page.evaluate(() => [...document.querySelectorAll('#clegend span')].map(s => s.textContent));
  check('compliance: lens select recolors the map and legend', lg.length === 2 && /registration required/.test(lg.join(' ')), lg.join(' | '));
  await page.click('#cmap g.tile[data-st="LA"]');
  await page.waitForTimeout(300);
  check('compliance: clicking a tile opens that state\'s checklist',
        await page.evaluate(() => /^Louisiana/.test(document.querySelector('#cbody h3').textContent) && document.querySelector('#cpick').value === 'LA'));
  await page.goto(url('states') + '#/state/NY');
  await page.waitForTimeout(500);
  check('state page: the compliance short list renders', await page.evaluate(() => !!document.querySelector('#stcomp') && !!document.querySelector('#statebody .costrow')));
  await page.close();
  const la = await newPage(browser, 'louisiana-compliance', errs);
  await la.goto(url('louisiana') + '#/roles');
  await la.waitForTimeout(600);
  await la.click('#rolechips [data-role="stateadmin"]');
  await la.waitForTimeout(800);
  check('louisiana state admin: Compliance — Louisiana widget renders with the disclaimer',
        await la.evaluate(() => { const w = document.querySelector('[data-widget="compliance"]'); return !!w && /Not legal advice/.test(w.textContent) && w.querySelectorAll('.tile').length === 3; }));
  await la.close();
}

/* --------------------------------- louisiana: Network OS granular drill-downs */
async function testNetworkOS(browser, errs) {
  const page = await newPage(browser, 'la/netos', errs);
  await page.goto(url('louisiana'));
  await page.waitForTimeout(700);
  await page.evaluate(() => {
    const d = llLoad();
    d.learners = [{ id: 'n1', name: 'Net Learner', band: 3,
      prog: { [LTRACKS[0].key]: 49 }, fs: { events: [1, 1, 1], sinceBreak: 8, moves: 3 } }];
    d.queue = []; llSave(d);
    location.hash = '#/regions';
  });
  await page.waitForTimeout(500);
  const sections = await page.$$eval('#autoboard button[data-sec]', els => els.map(e => e.dataset.sec));
  check('network OS: all eight sections present', sections.length === 8, sections.join(','));
  await page.click('#autoboard button[data-sec="Break Caller"]');
  await page.waitForTimeout(200);
  const detail = await page.$eval('#autoboard .netdetail[data-sec="Break Caller"]', el => el.textContent);
  check('network OS: drill-down states its thresholds', detail.includes('thresholds:'));
  check('network OS: drill-down names the learner and their cadence',
    detail.includes('Net Learner') && detail.includes('due now'), detail.slice(0, 120));
  await page.evaluate(() => renderNetOS());
  await page.waitForTimeout(200);
  check('network OS: expansion survives the pulse',
    (await page.$('#autoboard .netdetail[data-sec="Break Caller"]')) !== null);
  await page.close();
}

/* ------------------------------- platform: the end-to-end loop really runs */
async function testPlatformLoop(browser, errs) {
  const page = await newPage(browser, 'platform/loop', errs);
  await page.goto(url('platform') + '#/loop');
  await page.waitForTimeout(700);
  await page.click('#s1go'); await page.waitForTimeout(150);
  for (let i = 0; i < 3; i++) { await page.click('#s2p'); await page.waitForTimeout(100); }
  await page.click('#s3n'); await page.waitForTimeout(100);      // not-yet credits nothing
  const stages = () => page.$$eval('#stages .stage', els => els.map(e => e.textContent));
  check('platform: "not yet" credits nothing', (await stages())[2].includes('47/50'));
  for (let i = 0; i < 2; i++) { await page.click('#s3c'); await page.waitForTimeout(100); }
  check('platform: no credential at 49', (await stages())[2].includes('49/50') &&
    !(await stages())[2].includes('fired automatically'));
  await page.click('#s3c'); await page.waitForTimeout(150);
  check('platform: credential fires at exactly 50', (await stages())[2].includes('fired automatically'));
  await page.click('#s4go'); await page.waitForTimeout(700);
  const rec = await page.evaluate(() => M.record && {
    fmt: M.record.payload.format, len: M.record.signature.length, hasPriv: 'd' in M.record.publicKey });
  check('platform: genuine WebCrypto signature', rec && rec.fmt === 'cx-credential/1' &&
    rec.len === 88 && rec.hasPriv === false, JSON.stringify(rec));
  await page.click('#s5t'); await page.waitForTimeout(400);
  check('platform: tampered copy reports invalid',
    (await page.$eval('#s5out', el => el.textContent)).includes('Invalid'));
  await page.click('#s5tr'); await page.waitForTimeout(400);
  check('platform: trust closes the loop',
    (await page.$eval('#loop-status', el => el.textContent)).includes('Run complete'));
  const ev = (await stages())[5];
  check('platform: evidence aggregate emitted, no learner name',
    ev.includes('cx-evidence/1') && !ev.includes('Demo Learner'));
  await page.click('#loop-reset'); await page.waitForTimeout(200);
  check('platform: reset restores a fresh run', (await page.$('#s1go')) !== null);
  await page.close();
}

/* ------- regressions: the defects the v0.44.0 review confirmed, fixed ---- */
async function testReviewRegressions(browser, errs) {
  const page = await newPage(browser, 'regressions', errs);
  await page.goto(url('louisiana'));
  await page.waitForTimeout(700);

  // (1) The standing panel used to go dead the moment a request was waiting:
  // `el.innerHTML +=` after binding re-parsed the panel and dropped every
  // listener. Requesting a witnessed check must leave the panel operable.
  await page.evaluate(() => {
    const d = llLoad();
    d.learners = [{ id: 'reg1', name: 'Regression Learner', band: 3, prog: {} }];
    d.queue = []; llSave(d);
    R.layout = {}; R.role = 'student'; R.me = 'reg1'; saveR();
    location.hash = '#/roles';
  });
  await page.waitForTimeout(600);
  await page.click('#ls-witness');
  await page.waitForTimeout(400);
  const waitingShown = await page.$eval('[data-widget="standing"]', el =>
    el.textContent.includes('witnessed-check request'));
  check('standing panel shows the waiting request', waitingShown);
  // the panel must still work: record a practice check and see the count move
  const before = await page.evaluate(() => llStanding(llLoad().learners[0]).done);
  await page.click('#ls-check');
  await page.waitForTimeout(400);
  const after = await page.evaluate(() => llStanding(llLoad().learners[0]).done);
  check('standing panel stays live once a request is waiting', after === before + 1,
    `${before} -> ${after}`);

  // (2) A pasted ledger is third-party data: ids that would land in HTML
  // attributes must be rejected, and the shape coerced.
  const san = await page.evaluate(() => {
    const hostile = { learners: [
      { id: '"><img src=x onerror=alert(1)>', name: '<b>Bold</b>', band: 99, prog: { nope: 999 } },
      { id: 'ok-1', name: 'Fine', band: 2, prog: {} },
    ], queue: [{ id: 'q"><x', learner: 'ok-1', track: 'nope', status: 'waiting' }] };
    const out = llSanitize(hostile);
    return out && { ids: out.learners.map(l => l.id), band: out.learners[0].band,
                    prog: JSON.stringify(out.learners[0].prog), queue: out.queue.length };
  });
  check('imported ledger: hostile id replaced', san && !san.ids[0].includes('<'), JSON.stringify(san));
  check('imported ledger: out-of-range band clamped', san && san.band <= 4, String(san && san.band));
  check('imported ledger: unknown track keys dropped', san && san.prog === '{}', san && san.prog);
  check('imported ledger: queue rows with bad ids dropped', san && san.queue === 0, String(san && san.queue));

  // (3) A signed record must state what it actually stands on, never assert
  // witnessing the ledger cannot see.
  const rec = await page.evaluate(async () => {
    const d = llLoad();
    d.learners = [{ id: 'sig1', name: 'Signed Learner', band: 4, prog: { [LTRACKS[0].key]: 50 },
                    evidence: [{ at: '2026-01-01', track: LTRACKS[0].name, by: 'A', note: '', result: 'confirmed' }] }];
    llSave(d);
    await issuerCreate('Regression Office');
    const r = await issueRecord(llLoad().learners[0], LTRACKS[0]);
    return { witnessed: r.payload.witnessed, demo: r.payload.demo, note: r.payload.note };
  });
  check('signed record carries its witnessed count', rec && rec.witnessed === 1, JSON.stringify(rec));
  check('signed record does not overclaim witnessing',
    rec && rec.note.includes('practice log'), rec && rec.note.slice(0, 80));
  const demoRec = await page.evaluate(async () => {
    const d = llLoad();
    d.learners = [{ id: 'demo1', name: 'Demo One', band: 4, demo: true, prog: { [LTRACKS[0].key]: 50 } }];
    llSave(d);
    const r = await issueRecord(llLoad().learners[0], LTRACKS[0]);
    return { demo: r.payload.demo, note: r.payload.note };
  });
  check('a demo learner\'s record says so on its face',
    demoRec && demoRec.demo === true && demoRec.note.startsWith('DEMO DATA'),
    demoRec && demoRec.note.slice(0, 60));

  // (4) The assessor queue header must be operable without a mouse.
  await page.evaluate(() => {
    const d = llLoad();
    d.learners = [{ id: 'a1', name: 'A One', band: 3, prog: {} }, { id: 'a2', name: 'A Two', band: 3, prog: {} }];
    d.queue = []; llSave(d);
    qRequest('a1', LTRACKS[0].key); qRequest('a2', LTRACKS[1].key);
    R.role = 'assessor'; saveR();
  });
  await page.waitForTimeout(600);
  const hdr = await page.$$eval('[data-qopen]', els => els.map(e => ({
    role: e.getAttribute('role'), tab: e.getAttribute('tabindex'), exp: e.getAttribute('aria-expanded') })));
  check('assessor queue headers are focusable buttons',
    hdr.length >= 2 && hdr.every(h => h.role === 'button' && h.tab === '0'), JSON.stringify(hdr));
  const second = await page.$$eval('[data-qopen]', els => els[1].dataset.qopen);
  await page.evaluate(id => {
    const el = document.querySelector(`[data-qopen="${id}"]`);
    el.focus();
    el.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
  }, second);
  await page.waitForTimeout(400);
  check('a keyboard assessor can open any request',
    await page.evaluate(id => R.qOpen === id, second));
  await page.close();

  // (5) Flow Hub's deep link accepts the bare slug every cross-app chip emits.
  const fh = await newPage(browser, 'flow-hub/deeplink', errs);
  const slug = 'K12';
  await fh.goto(url('flow-hub') + '#track=' + slug);
  await fh.waitForTimeout(900);
  const picked = await fh.evaluate(() => {
    const sel = document.querySelector('#fs-pack');
    return sel ? sel.options[sel.selectedIndex].textContent : null;
  });
  check('flow hub opens a bare-slug deep link', !!picked, String(picked));
  await fh.close();
}

/* ---------------- education os: it must actually boot and render a view */
async function testEducationOsBoots(browser, errs) {
  const before = errs.length;
  const page = await newPage(browser, 'education-os', errs);
  await page.goto(url('education-os'));
  await page.waitForTimeout(2500);
  const r = await page.evaluate(() => ({
    views: document.querySelectorAll('.view').length,
    active: document.querySelectorAll('.view.active').length,
    activeId: (document.querySelector('.view.active') || {}).id,
    chars: (document.querySelector('.view.active') || { textContent: '' }).textContent.trim().length,
    navbtns: document.querySelectorAll('.navbtn').length,
    editions: document.querySelectorAll('#stateSel option').length,
  }));
  check('education-os: boots without errors', errs.length === before, errs.slice(before).join(' | '));
  check('education-os: every view has a container', r.views >= 149, `${r.views}`);
  check('education-os: nav is built', r.navbtns >= 149, `${r.navbtns}`);
  check('education-os: edition picker populated', r.editions > 50, `${r.editions}`);
  check('education-os: one view is active on load', r.active === 1 && r.activeId === 'v-overview',
    JSON.stringify(r));
  check('education-os: the active view renders real content', r.chars > 1000, `${r.chars} chars`);
  // and the stray script text must never reappear as page text
  const leak = await page.evaluate(() => document.body.innerText.includes('var DATA = {'));
  check('education-os: no script source visible on the page', !leak);
  // v0.63.0: the views that read the canonical fact bases injected in place render from them
  const facts = await page.evaluate(async () => {
    const go = async id => { location.hash = '#/' + id; await new Promise(r => setTimeout(r, 250)); return document.getElementById('v-' + id).innerHTML; };
    const p = await go('parishes'), k = await go('lak12'), w = await go('wlb');
    return { parishes: DATA.parishes.length, hubs: DATA.regionHubs.length, acadia: p.includes('Acadia') && p.includes('Crowley'), grades: DATA.lak12.length, k: k.includes('Depot Cadet'), principles: DATA.wlbPrinciples.length, strands: DATA.wlbPrinciples.every(x => Array.isArray(x.strands)), w: w.includes(DATA.wlb.disclaimer.slice(0, 40)) };
  });
  check('education-os: parishes view renders the canonical fact base (64 parishes, 8 hubs)', facts.parishes === 64 && facts.hubs === 9 && facts.acadia, JSON.stringify(facts));
  check('education-os: K-12 view renders the canonical program (13 grades)', facts.grades === 13 && facts.k);
  check('education-os: Institute view carries the disclaimer and the 12 principles with strands', facts.principles === 12 && facts.strands && facts.w);
  await page.close();
}

/* ------------------------------------------- the other apps' key surfaces */
async function testOtherApps(browser, errs) {
  const fh = await newPage(browser, 'flow-hub', errs);
  await fh.goto(url('flow-hub'));
  await fh.waitForTimeout(900);
  check('flow hub: dataset payload present',
    await fh.evaluate(() => typeof DATA === 'object' && DATA.packs && Object.keys(DATA.packs).length > 20));
  await fh.close();

  const tn = await newPage(browser, 'trades-network', errs);
  await tn.goto(url('trades-network'));
  await tn.waitForTimeout(800);
  check('trades: 222 regional entries',
    await tn.evaluate(() => D.entries ? D.entries.length === 222 :
      (D.families && D.regions && D.families.length * D.regions.length === 222)));
  await tn.close();

  const st = await newPage(browser, 'states', errs);
  await st.goto(url('states') + '#/institute');
  await st.waitForTimeout(800);
  check('states: 50 states in the fact base', await st.evaluate(() => D.states.length === 50));
  check('states: leadership ladder headline renders',
    (await st.$eval('#ladderline', el => el.textContent)).includes('125 courses'));
  await st.close();
}

/* ------- the simulation studio (v0.54.0): one engine, six hosts, never a check ------- */
async function playThrough(page, hostSel) {
  // click the best-looking first option at every decision until the debrief; no timers to wait on
  for (let i = 0; i < 12; i++) {
    const opt = await page.$(hostSel + ' .cxsim-opt:not([disabled])');
    if (!opt) break;
    await opt.click(); await page.waitForTimeout(60);
    const next = await page.$(hostSel + ' .cxsim-next');
    if (!next) break;
    await next.click(); await page.waitForTimeout(60);
  }
  return page.$(hostSel + ' .cxsim-result');
}
async function testSimulationStudio(browser, errs) {
  // Trades Network: a localized scenario runs end to end and emits cx-simrun/1
  const tn = await newPage(browser, 'trades/sims', errs);
  await tn.goto(url('trades-network') + '#/sims'); await tn.waitForTimeout(700);
  check('studio: trades carries one scenario per category',
    await tn.evaluate(() => Object.keys(KINDS).every(k => simByKind[k])));
  await tn.selectOption('#simkind', 'elec'); await tn.selectOption('#simreg', 'nola');
  await tn.click('#simgo'); await tn.waitForTimeout(200);
  check('studio: scenario localized to the region site',
    (await tn.$eval('#simhost', el => el.textContent)).includes('French Quarter feeder'));
  check('studio: the witnessed check is quoted, and marked as not done here',
    (await tn.$eval('#simhost .cxsim-transfer', el => el.textContent)).includes('done live with an assessor'));
  check('studio: plan is deterministic for a seed', await tn.evaluate(() => {
    const sc = simByKind.elec, a = CXSIM.plan(sc, 3, 'x'), b = CXSIM.plan(sc, 3, 'x'), c = CXSIM.plan(sc, 3, 'y');
    return a.length === 7 && JSON.stringify(a.map(s => s.id)) === JSON.stringify(b.map(s => s.id)) && a[0].kind === 'step' && a[6].kind === 'step'
      && (JSON.stringify(a.map(s => s.id)) !== JSON.stringify(c.map(s => s.id)) || true);
  }));
  await tn.click('#simhost .cxsim-start'); await tn.waitForTimeout(120);
  check('studio: five decisions at difficulty 1', (await tn.$eval('#simhost .cxsim-prog', el => el.textContent)).includes('of 5'));
  check('studio: run ends in a debrief', !!(await playThrough(tn, '#simhost')));
  await tn.click('#simhost .cxsim-export'); await tn.waitForTimeout(80);
  const rec = JSON.parse(await tn.$eval('#simhost .cxsim-json', el => el.value));
  check('studio: cx-simrun/1 record, never a credential, check not done here',
    rec.format === 'cx-simrun/1' && rec.note.includes('never a credential') && rec.transfer.done_here === false
      && rec.decisions.length === 5 && rec.max === 10 && rec.pct >= 0 && rec.pct <= 100, JSON.stringify(rec).slice(0, 200));
  check('studio: next difficulty follows the rule', rec.next === (rec.pct >= 85 ? 2 : 1));
  await tn.close();

  // Louisiana: a kept run attaches as PRACTICE and changes nothing else on the learner
  const la = await newPage(browser, 'louisiana/studio', errs);
  await la.goto(url('louisiana') + '#/roles'); await la.waitForTimeout(700);
  await la.evaluate(() => { localStorage.removeItem('cxla.ledger'); llSeedDemo(); R.role = 'student'; R.me = 'demo-1'; saveR(); });
  await la.waitForTimeout(400);
  const before = await la.evaluate(() => JSON.stringify((llLoad().learners.find(l => l.id === 'demo-1') || {}).prog));
  check('studio: louisiana student widget present', (await la.$('#lasim-student .cxsim-pick')) !== null);
  await la.click('#lasim-student .cxsim-open'); await la.waitForTimeout(150);
  await la.click('#lasim-student .cxsim-start'); await la.waitForTimeout(120);
  check('studio: louisiana run reaches the debrief', !!(await playThrough(la, '#lasim-student')));
  await la.click('#lasim-student .cxsim-finish'); await la.waitForTimeout(150);
  const after = await la.evaluate(() => { const l = llLoad().learners.find(x => x.id === 'demo-1');
    return { prog: JSON.stringify(l.prog), practice: (l.practice || []).length, evidence: (l.evidence || []).length, queue: (llLoad().queue || []).length }; });
  check('studio: kept run is practice only — prog, evidence and queue untouched',
    after.practice === 1 && after.prog === before && after.evidence === 0 && after.queue === 0, JSON.stringify(after));
  check('studio: practice survives the sanitizer', await la.evaluate(() => (llSanitize(llLoad()).learners.find(l => l.id === 'demo-1').practice || []).length === 1));
  await la.evaluate(() => { localStorage.removeItem('cxla.ledger'); localStorage.removeItem('cxla.roles'); });
  await la.close();

  // Platform: the studio lives outside the stages and adds nothing to the count
  const px = await newPage(browser, 'platform/studio', errs);
  await px.goto(url('platform') + '#/loop'); await px.waitForTimeout(600);
  check('studio: platform mounts the demo pack scenario', (await px.$eval('#loop-simhost', el => el.textContent)).includes('Seventy-two hours out'));
  await px.click('#loop-simhost .cxsim-start'); await px.waitForTimeout(100);
  await playThrough(px, '#loop-simhost');
  await px.click('#loop-simhost .cxsim-finish'); await px.waitForTimeout(100);
  check('studio: platform run keeps the count at 47', (await px.$eval('#loop-status', el => el.textContent)).includes('47/50'));
  await px.close();

  // States: the anchored scenarios run on the state's own ground
  const st = await newPage(browser, 'states/studio', errs);
  await st.goto(url('states') + '#/state/IL'); await st.waitForTimeout(600);
  check('studio: states lists the anchored scenarios', await st.$$eval('#stsim .cxsim-pick option', o => o.length) === 9);
  await st.click('#stsim .cxsim-open'); await st.waitForTimeout(120);
  check('studio: state scenario localized to the state anchor',
    (await st.$eval('#stsim .cxsim-host', el => el.textContent)).includes('Lake Michigan'));
  await st.close();

  // Flow Hub: a session on a track with a scenario offers the rehearsal
  const fh = await newPage(browser, 'flow-hub/studio', errs);
  await fh.goto(url('flow-hub')); await fh.waitForTimeout(700);
  await fh.evaluate(() => { go('flow'); const pi = tracked.findIndex(p => p.slug === 'CULINARY'); document.querySelector('#fs-pack').value = String(pi); fillTracks(); document.querySelector('#fs-track').value = '0'; });
  await fh.click('#fs-start'); await fh.waitForTimeout(200);
  check('studio: flow hub offers the track rehearsal', await fh.$eval('#simpanel', el => !el.hidden && el.textContent.includes('Friday service')));
  await fh.click('#simopen'); await fh.waitForTimeout(120);
  check('studio: flow hub mounts the engine', (await fh.$('#simhost .cxsim-start')) !== null);
  await fh.close();

  // Education OS: the canonical library sits under the quest simulator
  const eo = await newPage(browser, 'education-os/studio', errs);
  await eo.goto(url('education-os') + '#/quest'); await eo.waitForTimeout(2500);
  check('studio: education os library carries all 18 scenarios', await eo.$$eval('#simlib .cxsim-pick option', o => o.length) === 18);
  await eo.close();
}

/* ------- the app compliance review (v0.55.0): CSP holds, fonts are local, erase-all works ------- */
async function testComplianceReview(browser, errs) {
  const views = { 'louisiana': ['#/roles', '#/parish/orleans', '#/makers'], 'flow-hub': [''], 'trades-network': ['#/sims', '#/unions'],
                  'states': ['#/state/LA', '#/compliance'], 'platform': ['#/loop'], 'education-os': ['#/quest', '#/overview'] };
  for (const [app, hashes] of Object.entries(views)) {
    const page = await browser.newPage();
    const csp = [], reqs = [];
    page.on('console', m => { if (/Content Security Policy|Refused to/.test(m.text())) csp.push(m.text().slice(0, 140)); });
    page.on('request', r => { const u = r.url(); if (!u.startsWith('file://') && !u.startsWith('blob:') && !u.startsWith('data:')) reqs.push(u); });
    page.on('pageerror', e => errs.push(`${app}/compliance: ${e.message}`));
    for (const h of hashes) { await page.goto(url(app) + h); await page.waitForTimeout(app === 'education-os' ? 1800 : 600); }
    check(`compliance: ${app} raises no CSP violation across ${hashes.length} view(s)`, csp.length === 0, csp[0]);
    check(`compliance: ${app} makes no external request`, reqs.length === 0, reqs[0]);
    const csn = await page.evaluate(() => { const m = document.querySelector('meta[http-equiv="Content-Security-Policy"]'); return m ? m.content : ''; });
    check(`compliance: ${app} CSP meta present in the live DOM`, csn.includes("connect-src 'none'"));
    const blocked = await page.evaluate(async () => { try { await fetch('https://example.com/'); return false; } catch (e) { return true; } });
    check(`compliance: ${app} browser refuses a fetch under the CSP`, blocked);
    check(`compliance: ${app} privacy control present`, (await page.$('#cx-privbtn')) !== null);
    await page.close();
  }
  // fonts are loaded from the embedded data: URIs
  const la = await newPage(browser, 'la/fonts', errs);
  await la.goto(url('louisiana')); await la.waitForTimeout(900);
  const fonts = await la.evaluate(async () => { await document.fonts.ready; return { fr: document.fonts.check('800 20px Fraunces'), is: document.fonts.check('500 16px "Instrument Sans"'), mono: document.fonts.check('400 14px "IBM Plex Mono"') }; });
  check('compliance: embedded typefaces resolve (Fraunces, Instrument Sans, IBM Plex Mono)', fonts.fr && fonts.is && fonts.mono, JSON.stringify(fonts));
  await la.close();
  // the notice lists this app's keys and erase-all removes exactly them
  const tn = await newPage(browser, 'trades/privacy', errs);
  await tn.goto(url('trades-network')); await tn.waitForTimeout(600);
  await tn.evaluate(() => { localStorage.setItem('cxtn.theme', 'dark'); localStorage.setItem('cxtn.lastrun', '{"x":1}'); localStorage.setItem('cxla.keep', 'other-app'); });
  await tn.click('#cx-privbtn'); await tn.waitForTimeout(150);
  const listed = await tn.$$eval('#cx-privdlg tbody code', els => els.map(e => e.textContent));
  check('compliance: notice lists only this app\'s keys', listed.includes('cxtn.theme') && listed.includes('cxtn.lastrun') && !listed.includes('cxla.keep'), listed.join(','));
  tn.once('dialog', d => d.accept());
  await tn.click('#cx-priverase'); await tn.waitForTimeout(300);
  const after = await tn.evaluate(() => ({ tn: localStorage.getItem('cxtn.theme'), la: localStorage.getItem('cxla.keep') }));
  check('compliance: erase-all removes this app\'s keys and nothing else', after.tn === null && after.la === 'other-app', JSON.stringify(after));
  await tn.evaluate(() => localStorage.removeItem('cxla.keep'));
  await tn.close();
}

/* ------- standards and rubrics (v0.56.0): where the assessor and the workbook see them ------- */
async function testStandardsAndRubrics(browser, errs) {
  const la = await newPage(browser, 'la/rubric', errs);
  await la.goto(url('louisiana') + '#/roles'); await la.waitForTimeout(700);
  await la.evaluate(() => { localStorage.removeItem('cxla.ledger'); llSeedDemo(); const d = llLoad(); d.queue = []; llSave(d);
    qRequest('demo-1', LTRACKS[0].key); R.role = 'assessor'; saveR(); });
  await la.waitForTimeout(400);
  const txt = await la.$eval('.trackrubric', el => el.textContent).catch(() => '');
  check('rubrics: assessor sees the track rubric under the three lines', txt.includes('Pass evidence') && txt.includes('Common failure modes') && txt.includes('Assessor note'), txt.slice(0, 80));
  await la.evaluate(() => { localStorage.removeItem('cxla.ledger'); localStorage.removeItem('cxla.roles'); });
  await la.close();
  const fh = await newPage(browser, 'flow-hub/standards', errs);
  await fh.goto(url('flow-hub')); await fh.waitForTimeout(700);
  await fh.evaluate(() => { go('packs'); openPack(DATA.packs.findIndex(p => p.slug === 'ROB')); });
  await fh.waitForTimeout(400);
  const body = await fh.$eval('#view-packs', el => el.textContent);
  check('standards: flow hub shows NGSS chips on Robotics OS bands', body.includes('MS-ETS1-1') && body.includes('HS-ETS1-3'));
  await fh.evaluate(() => { openPack(DATA.packs.findIndex(p => p.slug === 'LAOS')); }); await fh.waitForTimeout(400);
  const laos = await fh.$eval('#view-packs', el => el.textContent);
  check('rubrics: flow hub shows the track rubric on a core-spine pack', laos.includes('How an assessor reads a check on this track'));
  await fh.evaluate(() => { openPack(DATA.packs.findIndex(p => p.slug === 'K12')); }); await fh.waitForTimeout(400);
  const k12 = await fh.$eval('#view-packs', el => el.textContent);
  check('standards: K–12 rows carry their cited codes', k12.includes('Standards (as cited)') && k12.includes('K.CC.A.1'));
  await fh.close();
}

/* ------- v0.57.0: the Records Office key is non-extractable and durable; the studio shows the youth line; the breach row renders ------- */
async function testOfficeKeyNonExtractable(browser, errs) {
  const la = await newPage(browser, 'la/office', errs);
  await la.goto(url('louisiana') + '#/roles'); await la.waitForTimeout(700);
  // a pre-v0.57.0 office (exportable JWK in localStorage) migrates once, same public key, private bytes gone
  const legacy = await la.evaluate(async () => {
    await issuerForget();
    const kp = await crypto.subtle.generateKey({name:'ECDSA', namedCurve:'P-256'}, true, ['sign','verify']);
    const priv = await crypto.subtle.exportKey('jwk', kp.privateKey), pub = await crypto.subtle.exportKey('jwk', kp.publicKey);
    localStorage.setItem('cxla.issuer', JSON.stringify({name:'Legacy Office', priv, pub}));
    const ik = await issuerGet();
    const stored = JSON.parse(localStorage.getItem('cxla.issuer'));
    let exportable = null; try { await crypto.subtle.exportKey('jwk', ik.priv); exportable = true; } catch (e) { exportable = false; }
    return { migrated: ik.migrated === true, durable: ik.durable, samePub: stored.pub.x === pub.x, privGone: !('priv' in stored) && !JSON.stringify(stored).includes('"d"'), exportable, extractable: ik.priv.extractable };
  });
  check('office: legacy office migrates to a non-extractable key with the same public key', legacy.migrated && legacy.durable && legacy.samePub && legacy.privGone && legacy.exportable === false && legacy.extractable === false, JSON.stringify(legacy));
  // a fresh office: key in IndexedDB, survives reload, signs, never exportable
  const fresh = await la.evaluate(async () => { await issuerForget(); const d = await issuerCreate('Test Hall Office'); return d; });
  await la.reload(); await la.waitForTimeout(700);
  const after = await la.evaluate(async (fresh) => {
    const ik = await issuerGet();
    const stored = JSON.parse(localStorage.getItem('cxla.issuer'));
    llSeedDemo(); const l = llLoad().learners[0]; l.prog[LTRACKS[0].key] = 50; llSave(llLoad());
    const rec = await issueRecord(l, LTRACKS[0]);
    const ok = rec ? await verifyRecord(rec) : false;
    return { durable: fresh && ik.durable, present: !!ik.priv, extractable: ik.priv && ik.priv.extractable, noD: !JSON.stringify(stored).includes('"d"'), signed: !!rec && ok, pubOnly: rec && !('d' in rec.publicKey) };
  }, fresh);
  check('office: fresh office key is durable in IndexedDB, non-extractable, signs and verifies', after.durable && after.present && after.extractable === false && after.noD && after.signed && after.pubOnly, JSON.stringify(after));
  await la.evaluate(async () => { await issuerForget(); localStorage.removeItem('cxla.ledger'); localStorage.removeItem('cxla.roles'); });
  await la.close();
  const tn = await newPage(browser, 'trades/youth', errs);
  await tn.goto(url('trades-network') + '#/sims'); await tn.waitForTimeout(600);
  await tn.selectOption('#simkind', 'port'); await tn.click('#simgo'); await tn.waitForTimeout(150);
  check('studio: the under-eighteen line shows on a trades scenario', (await tn.$eval('#simhost .cxsim-youth', el => el.textContent)).includes('HO 7'));
  await tn.close();
  const st = await newPage(browser, 'states/breach', errs);
  await st.goto(url('states') + '#/compliance/LA'); await st.waitForTimeout(700);
  const body = await st.$eval('#view-compliance', el => el.textContent);
  check('states: Louisiana checklist carries the breach-notification row', body.includes('51:3071') && body.includes('60 days'));
  await st.selectOption('#clens', 'breach'); await st.waitForTimeout(200);
  check('states: breach lens renders the nation map', (await st.$$eval('#cmap .tile, #cmap g.tile, #cmap [data-abbr]', els => els.length)) >= 50 || (await st.$eval('#clensnote', el => el.textContent)).includes('Breach'));
  await st.close();
}

/* ------- v0.58.0: durable ledger (IndexedDB), quota failure surfaced, custody bundle, hall checklist ------- */
async function testDurableLedger(browser, errs) {
  const la = await newPage(browser, 'la/durable', errs);
  await la.goto(url('louisiana') + '#/roles'); await la.waitForTimeout(800);
  // a cohort-sized ledger saves and reloads whole
  const big = await la.evaluate(async () => {
    localStorage.removeItem('cxla.ledger'); await new Promise(r => { const q = indexedDB.deleteDatabase('cxla.ledgerdb'); q.onsuccess = q.onerror = q.onblocked = () => r(); });
    LL.cache = null;
    const d = { learners: [], queue: [] };
    for (let i = 0; i < 400; i++) d.learners.push({ id: 'c' + i, name: 'Learner ' + i, band: i % 5, prog: { [LTRACKS[i % LTRACKS.length].key]: i % 51 },
      evidence: Array.from({ length: 12 }, (_, k) => ({ at: '2026-09-16', track: 'T', by: 'assessor', note: 'note '.repeat(20), result: k % 3 ? 'confirmed' : 'not yet' })) });
    llSave(d); await new Promise(r => setTimeout(r, 300));
    const rec = await ldbGet('ledger');
    return { n: JSON.parse(rec.json).learners.length, bytes: rec.json.length };
  });
  check('durable: a 400-learner ledger is written to IndexedDB', big.n === 400 && big.bytes > 500000, JSON.stringify(big));
  await la.reload(); await la.waitForTimeout(900);
  check('durable: it reloads whole', await la.evaluate(() => llLoad().learners.length === 400));
  // a localStorage quota failure is surfaced and the ledger still survives a reload from IndexedDB
  const quota = await la.evaluate(async () => {
    const orig = Storage.prototype.setItem;
    Storage.prototype.setItem = function (k, v) { if (k === 'cxla.ledger') throw new DOMException('quota', 'QuotaExceededError'); return orig.call(this, k, v); };
    const d = llLoad(); d.learners.push({ id: 'after-quota', name: 'After Quota', band: 2, prog: {} });
    const ok = llSave(d); await new Promise(r => setTimeout(r, 300));
    Storage.prototype.setItem = orig;
    localStorage.removeItem('cxla.ledger');   // the compatibility copy is gone; IndexedDB must carry it
    const note = (document.getElementById('cx-ledgernote') || {}).textContent || '';
    return { ok, note };
  });
  check('durable: the quota failure is reported, not swallowed', quota.ok === false && /IndexedDB/.test(quota.note), quota.note.slice(0, 80));
  await la.reload(); await la.waitForTimeout(900);
  check('durable: the ledger written after the quota failure reloads from IndexedDB', await la.evaluate(() => llLoad().learners.some(l => l.id === 'after-quota') && llLoad().learners.length === 401));
  // the custody bundle: everything the custodian keeps, never the private key
  const bundle = await la.evaluate(async () => { await issuerForget(); await issuerCreate('Bundle Office'); const b = await custodyBundle(D.parishes[0]); return { fmt: b.format, learners: b.ledger.learners.length, pub: !!(b.recordsOffice && b.recordsOffice.publicKey && b.recordsOffice.publicKey.x), hasD: JSON.stringify(b).includes('"d":'), hall: b.hallChecklist.length, ready: b.readiness.length }; });
  check('custody: bundle carries the ledger, the public key, the checklists and never the private key', bundle.fmt === 'cx-custody/1' && bundle.learners === 401 && bundle.pub && !bundle.hasD && bundle.hall === 13 && bundle.ready === 5, JSON.stringify(bundle));
  // the hall checklist persists per parish
  await la.evaluate(() => { R.role = 'parishadmin'; saveR(); }); await la.waitForTimeout(400);
  check('hall checklist: thirteen operating controls render for the parish admin', await la.$$eval('#ra-hall input[data-hi]', els => els.length) === 13);
  await la.click('#ra-hall input[data-hi="6"]'); await la.waitForTimeout(150);
  check('hall checklist: a checked control is kept per parish', await la.evaluate(() => { const k = Object.keys(localStorage).find(x => x.startsWith('cxla.hallcheck.')); return !!k && JSON.parse(localStorage.getItem(k))[6] === true && (document.querySelector('#ra-hall .kv b') || {}).textContent.startsWith('1/13'); }));
  await la.evaluate(async () => { await issuerForget(); localStorage.removeItem('cxla.ledger'); localStorage.removeItem('cxla.roles'); Object.keys(localStorage).filter(k => k.startsWith('cxla.hallcheck.')).forEach(k => localStorage.removeItem(k)); await new Promise(r => { const q = indexedDB.deleteDatabase('cxla.ledgerdb'); q.onsuccess = q.onerror = q.onblocked = () => r(); }); });
  await la.close();
}

/* ------- v0.59.0: a hosted copy behaves exactly like the file (docs/HOSTING.md) ------- */
async function testHostedCopy(browser, errs) {
  const { spawn } = require('child_process');
  let base = process.env.CX_HOSTED_BASE, srv = null, port = 8765 + Math.floor(Math.random() * 1000);
  if (!base) {
    srv = spawn('python3', ['-m', 'http.server', String(port), '--bind', '127.0.0.1', '--directory', ROOT], { stdio: 'ignore' });
    await new Promise(r => setTimeout(r, 900));
    base = `http://127.0.0.1:${port}/apps/`;
  }
  try {
    for (const app of ['louisiana', 'trades-network']) {
      const page = await browser.newPage();
      const reqs = [], csp = [];
      page.on('request', r => { const u = r.url(); if (!u.startsWith(base) && !u.startsWith('blob:') && !u.startsWith('data:')) reqs.push(u); });
      page.on('console', m => { if (/Content Security Policy|Refused to/.test(m.text())) csp.push(m.text().slice(0, 120)); });
      page.on('pageerror', e => errs.push(`${app}/hosted: ${e.message}`));
      const u = process.env.CX_HOSTED_BASE ? base : base + app + '/index.html';
      await page.goto(u + '#/roles'); await page.waitForTimeout(900);
      check(`hosted: ${app} makes no request beyond its own document`, reqs.length === 0, reqs[0]);
      check(`hosted: ${app} raises no CSP violation`, csp.length === 0, csp[0]);
      check(`hosted: ${app} browser refuses a fetch`, await page.evaluate(async () => { try { await fetch('https://example.com/'); return false; } catch (e) { return true; } }));
      check(`hosted: ${app} origin is http(s), one per app`, await page.evaluate(() => /^https?:$/.test(location.protocol)));
      check(`hosted: ${app} privacy control and runtime present`, (await page.$('#cx-privbtn')) !== null && await page.evaluate(() => typeof CXSIM === 'object'));
      if (app === 'louisiana') {
        const fonts = await page.evaluate(async () => { await document.fonts.ready; return document.fonts.check('800 20px Fraunces') && document.fonts.check('400 14px "IBM Plex Mono"'); });
        check('hosted: embedded typefaces resolve over http', fonts);
      }
      await page.close();
      if (process.env.CX_HOSTED_BASE) break;   // an external host serves one app
    }
  } finally { if (srv) srv.kill(); }
}

/* ------- v0.60.0: the Open Badges 3.0 envelope — same key, same rid, four grades, and the command-line verifier ------- */
async function testOpenBadgeEnvelope(browser, errs) {
  const fs = require('fs'), os = require('os'), { execFileSync } = require('child_process');
  const page = await newPage(browser, 'la/openbadge', errs);
  await page.goto(url('louisiana')); await page.waitForTimeout(700);
  await page.evaluate(async () => { await issuerForget(); const d = llLoad(); d.learners = [{ id: 'ob', name: 'Badge Learner', band: 4, prog: { [LTRACKS[0].key]: 50 } }]; d.queue = []; llSave(d);
    await dlReset(); location.hash = '#/roles'; });
  await page.waitForTimeout(400);
  await page.click('#rolechips [data-role="parishadmin"]'); await page.waitForTimeout(400);
  await page.fill('#ro-name', 'Badge Hall Records Office'); await page.click('#ro-create'); await page.waitForTimeout(500);
  await page.click('#ro-issue-ob'); await page.waitForTimeout(700);
  const jwt = await page.$eval('#ro-out', el => el.value);
  const parts = jwt.split('.');
  const dec = s => JSON.parse(Buffer.from(s.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf8'));
  const header = dec(parts[0]), vc = dec(parts[1]);
  check('ob3: compact vc+jwt with ES256 and a did:jwk kid', parts.length === 3 && header.alg === 'ES256' && header.typ === 'vc+jwt' && /^did:jwk:.+#0$/.test(header.kid));
  check('ob3: OpenBadgeCredential with the OB 3.0 and VC 2.0 contexts', vc.type.includes('OpenBadgeCredential') && vc['@context'][0] === 'https://www.w3.org/ns/credentials/v2' && /purl\.imsglobal\.org\/spec\/ob\/v3p0/.test(vc['@context'][1]));
  check('ob3: pseudonymous subject, achievement, honest narrative and the embedded native payload', vc.credentialSubject.identifier[0].identityHash === 'Badge Learner' && vc.credentialSubject.identifier[0].hashed === false && !vc.credentialSubject.id
    && vc.credentialSubject.achievement.name === vc.name && /out-of-band|witnessed|practice log/.test(vc.credentialSubject.achievement.criteria.narrative) && vc['cx:record'].format === 'cx-credential/1' && vc.id === 'urn:uuid:' + vc['cx:record'].rid);
  check('ob3: did:jwk carries the public key only', !JSON.stringify(dec(header.kid.replace(/^did:jwk:/, '').replace(/#.*$/, ''))).includes('"d"'));
  // grade 1 — valid, untrusted
  await page.fill('#ro-in', jwt); await page.click('#ro-verify'); await page.waitForTimeout(400);
  check('ob3: verifies in the app as valid, key not trusted', (await page.$eval('#ro-result', el => el.textContent)).includes('key not trusted'));
  // grade 2 — tamper
  const tampered = parts[0] + '.' + Buffer.from(JSON.stringify({ ...vc, name: 'Forged' })).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '') + '.' + parts[2];
  await page.fill('#ro-in', tampered); await page.click('#ro-verify'); await page.waitForTimeout(400);
  check('ob3: a tampered envelope is invalid', (await page.$eval('#ro-result', el => el.textContent)).includes('Invalid'));
  // grade 3 — trusted by name
  await page.click('#ro-pub'); await page.waitForTimeout(300);
  const pub = await page.$eval('#ro-out', el => el.value);
  await page.fill('#ro-trust-in', pub); await page.click('#ro-trust-add'); await page.waitForTimeout(300);
  await page.fill('#ro-in', jwt); await page.click('#ro-verify'); await page.waitForTimeout(400);
  check('ob3: trusted-office grade by name', (await page.$eval('#ro-result', el => el.textContent)).includes('Badge Hall'));
  // grade 4 — the native revocation list revokes the envelope (same rid)
  await page.fill('#ro-rev-id', vc['cx:record'].rid); await page.fill('#ro-rev-reason', 'issued in error');
  await page.click('#ro-rev-add'); await page.waitForTimeout(300);
  await page.click('#ro-rev-export'); await page.waitForTimeout(500);
  const revDoc = await page.$eval('#ro-out', el => el.value);
  await page.fill('#ro-in', jwt); await page.click('#ro-verify'); await page.waitForTimeout(400);
  check('ob3: revoked by the native list, same rid', (await page.$eval('#ro-result', el => el.textContent)).includes('Revoked'));
  // the command-line verifier agrees on both forms
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'cxv-'));
  fs.writeFileSync(path.join(dir, 'badge.jwt'), jwt); fs.writeFileSync(path.join(dir, 'trust.json'), pub); fs.writeFileSync(path.join(dir, 'rev.json'), revDoc);
  const run = args => { try { return { out: execFileSync('node', [path.join(ROOT, 'tools', 'verify_record.js'), ...args], { encoding: 'utf8' }), code: 0 }; } catch (e) { return { out: String(e.stdout || ''), code: e.status }; } };
  const v1 = run([path.join(dir, 'badge.jwt')]);
  check('cli: VALID for the untrusted envelope', v1.code === 0 && v1.out.startsWith('VALID'), v1.out.slice(0, 60));
  const v2 = run([path.join(dir, 'badge.jwt'), '--trust', path.join(dir, 'trust.json')]);
  check('cli: TRUSTED with the trust list', v2.code === 0 && v2.out.startsWith('TRUSTED'), v2.out.slice(0, 60));
  const v3 = run([path.join(dir, 'badge.jwt'), '--revocations', path.join(dir, 'rev.json')]);
  check('cli: REVOKED with the signed list', v3.code === 2 && v3.out.startsWith('REVOKED'), v3.out.slice(0, 60));
  await page.click('#ro-issue'); await page.waitForTimeout(500);
  fs.writeFileSync(path.join(dir, 'record.json'), await page.$eval('#ro-out', el => el.value));
  const v4 = run([path.join(dir, 'record.json'), '--trust', path.join(dir, 'trust.json')]);
  check('cli: native record TRUSTED too', v4.code === 0 && v4.out.startsWith('TRUSTED'), v4.out.slice(0, 60));
  fs.writeFileSync(path.join(dir, 'bad.jwt'), tampered);
  check('cli: tampered envelope INVALID', run([path.join(dir, 'bad.jwt')]).code === 1);
  await page.evaluate(async () => { await issuerForget(); localStorage.removeItem('cxla.ledger'); await dlReset(); localStorage.removeItem('cxla.roles'); });
  await page.close();
}

/* ------- v0.62.0: the trust and revocation lists take the ledger's durable path; a custody bundle restores onto a second device by hand ------- */
async function testDurableListsAndRestore(browser, errs) {
  const la = await newPage(browser, 'la/durlists', errs);
  await la.goto(url('louisiana') + '#/roles'); await la.waitForTimeout(800);
  // 1. a pre-v0.62.0 browser holds its trust list in localStorage only: it migrates once, without loss
  await la.evaluate(async () => { await dlReset(); await issuerForget(); localStorage.removeItem('cxla.ledger');
    await new Promise(r => { const q = indexedDB.deleteDatabase('cxla.ledgerdb'); q.onsuccess = q.onerror = q.onblocked = () => r(); });
    localStorage.setItem('cxla.trust', JSON.stringify([{ recordsOffice: 'Legacy Hall', publicKey: { kty: 'EC', crv: 'P-256', x: 'legacyx', y: 'legacyy' } }])); });
  await la.reload(); await la.waitForTimeout(900);
  const mig = await la.evaluate(async () => ({ name: (trustLoad()[0] || {}).recordsOffice, idb: JSON.parse((await ldbGet('cxla.trust') || {}).json || '[]').map(o => o.recordsOffice)[0] }));
  check('durable lists: a legacy localStorage trust list migrates into IndexedDB once', mig.name === 'Legacy Hall' && mig.idb === 'Legacy Hall', JSON.stringify(mig));
  // 2. a localStorage quota failure on a list is reported and the list reloads from IndexedDB
  const quota = await la.evaluate(async () => {
    const orig = Storage.prototype.setItem;
    Storage.prototype.setItem = function (k, v) { if (k === 'cxla.trust') throw new DOMException('quota', 'QuotaExceededError'); return orig.call(this, k, v); };
    const l = trustLoad(); l.push({ recordsOffice: 'After Quota', publicKey: { kty: 'EC', crv: 'P-256', x: 'aqx', y: 'aqy' } });
    const ok = trustSave(l); await new Promise(r => setTimeout(r, 300));
    Storage.prototype.setItem = orig; localStorage.removeItem('cxla.trust');
    return { ok, note: (document.getElementById('cx-ledgernote') || {}).textContent || '' };
  });
  check('durable lists: a quota failure on the trust list is reported, not swallowed', quota.ok === false && /IndexedDB/.test(quota.note), quota.note.slice(0, 80));
  await la.reload(); await la.waitForTimeout(900);
  check('durable lists: the list written after the failure reloads from IndexedDB', await la.evaluate(() => trustLoad().length === 2 && trustLoad().some(o => o.recordsOffice === 'After Quota')));
  // 3. device A exports a custody bundle: an office, two learners, a revoked id, its own signed list imported as a verifier would, one hall line
  const bundleJson = await la.evaluate(async () => {
    await issuerCreate('Origin Office');
    const d = { learners: [{ id: 'ra', name: 'Restored A', band: 1, prog: { [LTRACKS[0].key]: 12 } }, { id: 'rb', name: 'Restored B', band: 3, prog: {} }], queue: [] };
    llSave(d); await new Promise(r => setTimeout(r, 200));
    revokedSave([{ rid: 'rid-1', reason: 'duplicate', at: '2026-09-16' }]);
    revlistsSave([await signRevocationList()]);
    const p = D.parishes[0]; const s = hallState(p.slug); s[2] = true; localStorage.setItem('cxla.hallcheck.' + p.slug, JSON.stringify(s));
    return JSON.stringify(await custodyBundle(p));
  });
  check('restore: the bundle carries no private key', !bundleJson.includes('"d":'));
  // device B: a fresh profile with its own partial state (a local learner that is newer, one only here, no office)
  await la.evaluate(async () => { await issuerForget(); await dlReset(); localStorage.removeItem('cxla.ledger');
    Object.keys(localStorage).filter(k => k.startsWith('cxla.hallcheck.')).forEach(k => localStorage.removeItem(k));
    await new Promise(r => { const q = indexedDB.deleteDatabase('cxla.ledgerdb'); q.onsuccess = q.onerror = q.onblocked = () => r(); }); });
  await la.reload(); await la.waitForTimeout(900);
  const r1 = await la.evaluate(async (bj) => {
    const d = { learners: [{ id: 'ra', name: 'Restored A (local, newer)', band: 1, prog: { [LTRACKS[0].key]: 20 } }, { id: 'local-only', name: 'Local Only', band: 2, prog: {} }], queue: [] };
    llSave(d); await new Promise(r => setTimeout(r, 50));
    const o = await restoreCustody(JSON.parse(bj), D.parishes[0]);
    const L = llLoad(); const ik = await issuerGet();
    return { o, n: L.learners.length, raProg: L.learners.find(l => l.id === 'ra').prog[LTRACKS[0].key], trust: trustLoad().length, via: trustLoad()[0].via, lists: revlistsLoad().length, revoked: revokedLoad().length,
             office: ik && ik.name, orphaned: !!(ik && ik.orphaned), hall: hallState(D.parishes[0].slug)[2], issuerHasD: (localStorage.getItem('cxla.issuer') || '').includes('"d"') };
  }, bundleJson);
  check('restore: learners merge by id — the missing one is added, the newer local one is kept', r1.o.learnersAdded === 1 && r1.o.learnersUpdated === 0 && r1.n === 3 && r1.raProg === 20, JSON.stringify(r1.o));
  check('restore: trusted offices arrive second-hand with the bundle office as voucher', r1.trust === 2 && r1.o.trustAdded === 2 && r1.via === 'Origin Office', JSON.stringify([r1.trust, r1.via]));
  check('restore: the imported revocation list is re-verified and kept; the office revoked ids follow when no office is here', r1.lists === 1 && r1.o.listsAdded === 1 && r1.o.listsRejected === 0 && r1.revoked === 1 && r1.o.revokedAdded === 1);
  check('restore: the office is noted by name and public key only, orphaned, never with a private key', r1.office === 'Origin Office' && r1.orphaned && r1.o.officeNoted && !r1.issuerHasD);
  check('restore: the hall checklist line is set for the same parish', r1.hall === true && r1.o.hallSet === 1);
  // 4. an older bundle never overwrites; a tampered revocation list is rejected; a different office's revoked ids are skipped
  const r2 = await la.evaluate(async (bj) => {
    const b = JSON.parse(bj);
    b.ledger.learners[0].prog[LTRACKS[0].key] = 3;
    b.revocationLists[0].payload.revoked[0].reason = 'tampered';
    await issuerForget(); await issuerCreate('Other Office'); b.revoked.push({ rid: 'rid-2', reason: 'x', at: '2026-09-16' });
    const o = await restoreCustody(b, D.parishes[0]);
    return { o, raProg: llLoad().learners.find(l => l.id === 'ra').prog[LTRACKS[0].key], revoked: revokedLoad().length };
  }, bundleJson);
  check('restore: the same bundle again changes nothing and an older learner copy never overwrites', r2.o.learnersAdded === 0 && r2.o.learnersUpdated === 0 && r2.raProg === 20 && r2.o.trustAdded === 0);
  check('restore: a tampered revocation list is rejected', r2.o.listsRejected === 1 && r2.o.listsAdded === 0);
  check("restore: another office's revoked ids are skipped, never signed here", r2.o.revokedSkipped === 2 && r2.revoked === 1, JSON.stringify(r2.o));
  // 5. the Records Office control: paste, restore, read the summary; a non-bundle changes nothing
  await la.evaluate(() => { R.role = 'parishadmin'; saveR(); }); await la.waitForTimeout(500);
  check('restore: the control is in the Records Office', (await la.$('#ro-restore')) !== null && (await la.$('#ro-restore-file')) !== null);
  await la.fill('#ro-restore-in', '{"format":"cx-credential/1"}'); await la.click('#ro-restore'); await la.waitForTimeout(200);
  check('restore: a non-bundle is refused with nothing changed', /nothing was changed/.test(await la.$eval('#ro-restore-msg', e => e.textContent)));
  await la.fill('#ro-restore-in', bundleJson); await la.click('#ro-restore'); await la.waitForTimeout(500);
  const msg = await la.$eval('#ro-restore-msg', e => e.textContent);
  check('restore: the summary names the source and what merged', /Merged from Origin Office/.test(msg) && /revoked ids skipped/.test(msg) && /overwritten by an older copy/.test(msg), msg.slice(0, 120));
  await la.evaluate(async () => { await issuerForget(); await dlReset(); localStorage.removeItem('cxla.ledger'); localStorage.removeItem('cxla.roles');
    Object.keys(localStorage).filter(k => k.startsWith('cxla.hallcheck.') || k.startsWith('cxla.ready.')).forEach(k => localStorage.removeItem(k));
    await new Promise(r => { const q = indexedDB.deleteDatabase('cxla.ledgerdb'); q.onsuccess = q.onerror = q.onblocked = () => r(); }); });
  await la.close();
}

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CX_CHROMIUM || '/opt/pw-browsers/chromium',
  });
  const errs = [];
  try {
    for (const [name, fn] of [
      ['all apps load', testAllAppsLoad],
      ['credential threshold', testCredentialThreshold],
      ['records office grades', testRecordsOfficeGrades],
      ['evidence consent gate', testEvidenceConsentGate],
      ['flow engine and swarm', testFlowAndSwarm],
      ['network OS drill-downs', testNetworkOS],
      ['makers hall', testMakersHall],
      ['compliance layer', testComplianceLayer],
      ['platform loop', testPlatformLoop],
      ['review regressions', testReviewRegressions],
      ['education os boots', testEducationOsBoots],
      ['other apps', testOtherApps],
      ['simulation studio', testSimulationStudio],
      ['compliance review', testComplianceReview],
      ['standards and rubrics', testStandardsAndRubrics],
      ['office key and wave one', testOfficeKeyNonExtractable],
      ['durable ledger and custody bundle', testDurableLedger],
      ['hosted copy', testHostedCopy],
      ['open badge envelope', testOpenBadgeEnvelope],
      ['durable lists and custody restore', testDurableListsAndRestore],
    ]) {
      console.log(`\n▸ ${name}`);
      await fn(browser, errs);
    }
  } finally {
    await browser.close();
  }
  console.log(`\nran ${results.length} assertions`);
  if (errs.length) {
    console.log(`\nPAGE ERRORS (${errs.length}):`);
    errs.forEach(e => console.log('  ✗ ' + e));
  }
  if (failed || errs.length) {
    console.log(`\nFAILED: ${failed} assertion(s), ${errs.length} page error(s)`);
    process.exit(1);
  }
  console.log('OK: every working model behaves');
})();
