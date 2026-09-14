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
  await page.evaluate(() => {
    const d = llLoad();
    d.learners = [{ id: 'rec', name: 'Record Learner', band: 4, prog: { [LTRACKS[0].key]: 50 } }];
    d.queue = []; llSave(d);
    try { localStorage.removeItem('cxla.trust'); localStorage.removeItem('cxla.revlists'); } catch (e) {}
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
      ['platform loop', testPlatformLoop],
      ['review regressions', testReviewRegressions],
      ['education os boots', testEducationOsBoots],
      ['other apps', testOtherApps],
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
