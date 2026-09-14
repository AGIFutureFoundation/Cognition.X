// Captures the real app screens the pitch deck embeds (run from anywhere).
const { chromium } = require('playwright');
const path=require('path');
const A='file://'+path.resolve(__dirname,'..','..','..','apps')+'/';
(async () => {
  const b = await chromium.launch({executablePath: process.env.CX_CHROMIUM || '/opt/pw-browsers/chromium'});
  const page = await b.newPage({viewport:{width:1600,height:1000}, deviceScaleFactor:1});
  const shot = async (name, url, fn) => { await page.goto('about:blank'); await page.goto(url); await page.waitForTimeout(1000); if (fn) await fn(); await page.waitForTimeout(500); await page.screenshot({path: path.join(__dirname, `shot-${name}.png`)}); console.log('shot', name); };
  await shot('state', A+'louisiana/index.html#/state', async()=>{ await page.evaluate(()=>document.querySelector('#mapbox').scrollIntoView({block:'start'})); });
  await shot('parish', A+'louisiana/index.html#/parish/st-landry', async()=>{ await page.evaluate(()=>document.querySelector('#pplan').scrollIntoView({block:'start'})); });
  await shot('makers', A+'louisiana/index.html#/makers', async()=>{ await page.click('#mkpath .mkstage[data-stage="room"]'); await page.evaluate(()=>document.querySelector('#mkpath').scrollIntoView({block:'start'})); });
  await shot('institute', A+'louisiana/index.html#/institute', async()=>{ await page.evaluate(()=>document.querySelector('#arcs').scrollIntoView({block:'start'})); });
  await shot('ladder', A+'louisiana/index.html#/institute', async()=>{ await page.evaluate(()=>document.querySelector('#strandpick').scrollIntoView({block:'start'})); });
  await shot('regions', A+'louisiana/index.html#/regions', async()=>{ await page.evaluate(()=>document.querySelector('#autoboard').scrollIntoView({block:'start'})); await page.click('#autoboard button[data-sec]'); });
  await shot('roles', A+'louisiana/index.html#/roles', async()=>{ await page.click('#rolechips [data-role="teacher"]'); await page.waitForTimeout(800); });
  await shot('trades', A+'trades-network/index.html', async()=>{ await page.evaluate(()=>window.scrollTo(0,260)); });
  await shot('flow', A+'flow-hub/index.html', async()=>{ await page.click('.navbtn[data-view="flow"]'); await page.selectOption('#fs-pack',{label:'Music : Creation to Industry'}); await page.click('#fs-start'); await page.waitForTimeout(800); await page.click('#oc-flow'); });
  await shot('loop', A+'platform/index.html#/loop', async()=>{ for (const s of ['#s1go','#s2p','#s2p','#s2s','#s2p','#s3c','#s3c','#s3c','#s4go']){ const e=await page.$(s); if(e){ await e.click(); await page.waitForTimeout(400);} } await page.waitForTimeout(1500); const e=await page.$('#s5t'); if(e) await e.click(); await page.waitForTimeout(600); await page.evaluate(()=>{ const x=document.querySelector('#s4go, #s5v, #s5t'); if(x) x.scrollIntoView({block:'center'}); }); });
  await shot('states', A+'states/index.html', async()=>{ await page.evaluate(()=>document.querySelector('#usmap').scrollIntoView({block:'start'})); });
  await shot('platform', A+'platform/index.html#/model', async()=>{ await page.evaluate(()=>document.querySelector('#sysmap').scrollIntoView({block:'start'})); });
  await b.close();
})();
