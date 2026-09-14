/**
 * Film kit — records the platform's own apps into short product films.
 *
 * Every frame is the software as shipped: Playwright drives the real
 * dashboards at 1920x1080 (title cards are generated HTML, captions and
 * the cursor are injected overlays), then ffmpeg encodes H.264. No
 * generated footage, no external service, no credits.
 *
 *     node tools/film/scenes1.js     # The Flow Zone (education · Louisiana · Institute)
 *     node tools/film/scenes2.js     # Training that proves itself (organisations · SmartCiti.X)
 *
 * Needs Playwright + a Chromium build (CX_CHROMIUM, default the project
 * environment's /opt/pw-browsers/chromium) and ffmpeg (CX_FFMPEG, else the
 * imageio-ffmpeg wheel, else PATH). Output lands in tools/film/out/ (git-
 * ignored). Render one film at a time: two concurrent recorders starve the
 * screencast and drop black frames. The cinematic cuts that intercut
 * generated footage are specified in docs/film/PRODUCTION_BRIEFS.md.
 */
// Film driver: records a scene list from the real apps into one 1920x1080 webm,
// then ffmpeg encodes an H.264 MP4. Scenes: {card:{...},dur} or {url, caption, chapter, steps:[...]}
const { chromium } = require('playwright');
const { card } = require('./card');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const ROOT = path.resolve(__dirname, '..', '..', 'apps');
const app = (a, hash='') => `file://${ROOT}/${a}/index.html${hash}`;
// ffmpeg: CX_FFMPEG, else the imageio-ffmpeg wheel's binary, else whatever is on PATH
const FF = process.env.CX_FFMPEG || (()=>{ try { return require('child_process').execSync('python3 -c "import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())"', {stdio:['ignore','pipe','ignore']}).toString().trim(); } catch(e){ return 'ffmpeg'; } })();
const CHROME = process.env.CX_CHROMIUM || '/opt/pw-browsers/chromium';

const OVERLAY = `
(function(){
  // a hash-only navigation keeps the previous scene's document (and its opaque fade) — clear it
  document.querySelectorAll('#cx-fade,#cx-cap,#cx-cur,style[data-cx]').forEach(e=>e.remove());
  const s=document.createElement('style'); s.dataset.cx='1'; s.textContent=\`
  #cx-cap{pointer-events:none;position:fixed;left:72px;bottom:72px;max-width:1100px;padding:22px 34px;background:rgba(10,22,34,.94);color:#fff;font:600 34px/1.25 Georgia,serif;border-left:8px solid #D9A441;z-index:2147483000;border-radius:8px;box-shadow:0 18px 50px rgba(0,0,0,.35);opacity:0;transform:translateY(20px);transition:opacity .5s,transform .5s}
  #cx-cap.on{opacity:1;transform:none}
  #cx-cap small{display:block;font:600 20px/1 ui-monospace,Menlo,monospace;letter-spacing:.28em;color:#D9A441;margin:0 0 10px;text-transform:uppercase}
  #cx-fade{position:fixed;inset:0;background:#000;z-index:2147483001;opacity:1;transition:opacity .6s;pointer-events:none}
  #cx-cur{position:fixed;width:26px;height:26px;border-radius:50%;background:rgba(217,164,65,.9);border:3px solid #fff;z-index:2147483002;pointer-events:none;transform:translate(-50%,-50%);transition:left .55s cubic-bezier(.2,.8,.2,1),top .55s cubic-bezier(.2,.8,.2,1);box-shadow:0 0 0 8px rgba(217,164,65,.25);display:none}
  #cx-cur.click{animation:cxclick .35s ease-out}
  @keyframes cxclick{50%{transform:translate(-50%,-50%) scale(.6)}}
  html{scroll-behavior:smooth}\`;
  document.head.appendChild(s);
  const f=document.createElement('div'); f.id='cx-fade'; document.body.appendChild(f);
  const c=document.createElement('div'); c.id='cx-cap'; document.body.appendChild(c);
  const k=document.createElement('div'); k.id='cx-cur'; document.body.appendChild(k);
  window.cxFade=(on)=>{ f.style.opacity=on?1:0; };
  window.cxCap=(chapter,text)=>{ c.classList.remove('on'); setTimeout(()=>{ c.innerHTML=(chapter?'<small>'+chapter+'</small>':'')+text; c.classList.add('on'); }, 250); };
  window.cxCur=(x,y,click)=>{ k.style.display='block'; k.style.left=x+'px'; k.style.top=y+'px'; if(click){ k.classList.remove('click'); void k.offsetWidth; k.classList.add('click'); } };
})();`;

async function moveClick(page, sel, {click=true, dwell=700}={}){
  const el = await page.$(sel); if (!el) { console.log('  (missing', sel+')'); return false; }
  await el.evaluate(e=>e.scrollIntoView({block:'center', inline:'nearest'})); await page.waitForTimeout(450);
  const b = await el.boundingBox(); if (!b) return false;
  const x = b.x + Math.min(b.width/2, 200), y = b.y + b.height/2;
  await page.evaluate(([x,y])=>window.cxCur(x,y,false), [x,y]);
  await page.waitForTimeout(650);
  if (click){ await page.evaluate(([x,y])=>window.cxCur(x,y,true), [x,y]); await page.mouse.click(x,y); }
  await page.waitForTimeout(dwell);
  return true;
}
async function scrollTo(page, sel, dwell=1200){
  const ok = await page.evaluate(s=>{ const e=document.querySelector(s); if(!e) return false; e.scrollIntoView({behavior:'smooth',block:'start'}); return true; }, sel);
  if (!ok) console.log('  (missing scroll target', sel+')');
  await page.waitForTimeout(dwell);
}
async function drift(page, px, ms){ // slow scroll over ms
  const steps = Math.max(1, Math.round(ms/40));
  for (let i=0;i<steps;i++){ await page.mouse.wheel(0, px/steps); await page.waitForTimeout(40); }
}

async function run(name, scenes){
  const outdir = path.resolve(__dirname, 'out', name); fs.rmSync(outdir, {recursive:true, force:true}); fs.mkdirSync(outdir, {recursive:true});
  const b = await chromium.launch({executablePath: CHROME});
  const ctx = await b.newContext({viewport:{width:1920,height:1080}, recordVideo:{dir:outdir, size:{width:1920,height:1080}}, reducedMotion:'no-preference'});
  const page = await ctx.newPage();
  page.on('pageerror', e=>console.log('  pageerror', e.message.slice(0,80)));
  let i=0;
  for (const sc of scenes){
    i++;
    if (sc.card){
      const file = path.join(outdir, `card${i}.html`);
      const u = card(file, {...sc.card, dur: sc.dur||5});
      console.log(`[${i}] card ${sc.card.title.replace(/<[^>]+>/g,'')}`);
      await page.goto(u); await page.waitForTimeout((sc.dur||5)*1000);
      continue;
    }
    console.log(`[${i}] ${sc.url.split('/apps/')[1]} — ${sc.caption}`);
    await page.goto('about:blank'); // every scene starts from a fresh document
    await page.goto(sc.url); await page.waitForTimeout(sc.settle||900);
    await page.evaluate(OVERLAY);
    await page.evaluate(()=>window.cxFade(false));
    await page.evaluate(([c,t])=>window.cxCap(c,t), [sc.chapter||'', sc.caption||'']);
    await page.waitForTimeout(600);
    for (const st of (sc.steps||[])){
      if (st.click) await moveClick(page, st.click, {dwell: st.dwell||900});
      else if (st.hover) await moveClick(page, st.hover, {click:false, dwell: st.dwell||900});
      else if (st.scroll) await scrollTo(page, st.scroll, st.dwell||1200);
      else if (st.drift) await drift(page, st.drift, st.ms||1800);
      else if (st.type){ await page.fill(st.type, ''); await page.type(st.type, st.text, {delay:70}); await page.waitForTimeout(st.dwell||900); }
      else if (st.select){ try { await page.selectOption(st.select, st.value); const e=await page.$(st.select); if(e) await e.dispatchEvent('change'); } catch(e){ console.log('  (select failed', st.select+')'); } await page.waitForTimeout(st.dwell||900); }
      else if (st.cap){ await page.evaluate(([c,t])=>window.cxCap(c,t), [st.chapter||sc.chapter||'', st.cap]); await page.waitForTimeout(st.dwell||1500); }
      else if (st.wait) await page.waitForTimeout(st.wait);
      else if (st.eval){ await page.evaluate(st.eval); await page.waitForTimeout(st.dwell||600); }
    }
    await page.waitForTimeout(sc.hold||1200);
    await page.evaluate(()=>window.cxFade(true)); await page.waitForTimeout(650);
  }
  await page.close(); await ctx.close(); await b.close();
  const webm = fs.readdirSync(outdir).find(f=>f.endsWith('.webm'));
  const mp4 = path.resolve(__dirname, 'out', name + '.mp4');
  execFileSync(FF, ['-y','-hide_banner','-loglevel','error','-i', path.join(outdir, webm), '-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart','-r','25', mp4]);
  console.log('wrote', mp4, (fs.statSync(mp4).size/1e6).toFixed(1)+' MB');
  return mp4;
}
module.exports = { run, app, OVERLAY };
