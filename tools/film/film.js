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
 *     node tools/film/social1.js … social5.js   # the five narrated feature shorts
 *
 * Narration: a scene's `say` text is rendered offline by tools/film/tts.py —
 * kokoro-onnx by default (pip install kokoro-onnx soundfile; kokoro-v1.0.onnx +
 * voices-v1.0.bin in tools/film/kokoro/ or CX_KOKORO_DIR; voice via CX_TTS_VOICE,
 * default af_heart) or piper (CX_TTS=piper, CX_PIPER_VOICE). The scene is held
 * at least as long as its clip, the track is assembled from the recorded scene
 * start times, and ffmpeg muxes it. Scenes without `say` record silent.
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

// Narration: piper (offline neural TTS) renders each scene's `say` to a wav;
// the scene is held at least as long as its clip, and the track is assembled
// from the recorded scene start times so voice and picture stay aligned.
function wavInfo(file){
  const b = fs.readFileSync(file); let off = 12, byteRate = 0, dataLen = 0;
  while (off + 8 <= b.length){ const id = b.toString('ascii', off, off+4), len = b.readUInt32LE(off+4);
    if (id === 'fmt ') byteRate = b.readUInt32LE(off+16); if (id === 'data'){ dataLen = len; break; } off += 8 + len + (len % 2); }
  return {dur: dataLen / byteRate, sampleRate: b.readUInt32LE(24), channels: b.readUInt16LE(22), bits: b.readUInt16LE(34)};
}
function synth(text, file){
  // tts.py: kokoro (default, CX_TTS_VOICE e.g. af_heart / am_michael / bm_george) or piper (CX_TTS=piper)
  if (!fs.existsSync(file)) execFileSync('python3', [path.join(__dirname, 'tts.py'), '--out', file], {input: text, stdio:['pipe','ignore','pipe'], env: {...process.env}});
  return wavInfo(file).dur;
}
function buildTrack(clips, out){ // clips: [{file, at}] seconds; writes a 16-bit PCM wav with silence between
  const info = wavInfo(clips[0].file), sr = info.sampleRate, bps = info.channels * info.bits / 8;
  const parts = []; let pos = 0;
  for (const c of clips){ const start = Math.round(c.at * sr) * bps; if (start > pos){ parts.push(Buffer.alloc(start - pos)); pos = start; }
    const b = fs.readFileSync(c.file); let off = 12; while (off + 8 <= b.length){ const id = b.toString('ascii', off, off+4), len = b.readUInt32LE(off+4); if (id === 'data'){ const d = b.subarray(off+8, off+8+len); parts.push(d); pos += d.length; break; } off += 8 + len + (len % 2); } }
  const data = Buffer.concat(parts); const h = Buffer.alloc(44);
  h.write('RIFF',0); h.writeUInt32LE(36+data.length,4); h.write('WAVE',8); h.write('fmt ',12); h.writeUInt32LE(16,16); h.writeUInt16LE(1,20); h.writeUInt16LE(info.channels,22); h.writeUInt32LE(sr,24); h.writeUInt32LE(sr*bps,28); h.writeUInt16LE(bps,32); h.writeUInt16LE(info.bits,34); h.write('data',36); h.writeUInt32LE(data.length,40);
  fs.writeFileSync(out, Buffer.concat([h, data]));
}

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
  // narration first, so every scene knows how long it must hold
  scenes.forEach((sc, i) => { if (sc.say){ sc.audio = path.join(outdir, `say${i+1}.wav`); sc.sayDur = synth(sc.say, sc.audio); } });
  const b = await chromium.launch({executablePath: CHROME});
  const ctx = await b.newContext({viewport:{width:1920,height:1080}, recordVideo:{dir:outdir, size:{width:1920,height:1080}}, reducedMotion:'no-preference'});
  const page = await ctx.newPage();
  page.on('pageerror', e=>console.log('  pageerror', e.message.slice(0,80)));
  const T0 = Date.now(), clips = [];
  const holdFor = async (sc, started) => { if (!sc.sayDur) return; const left = (sc.sayDur + 0.6) * 1000 - (Date.now() - started); if (left > 0) await page.waitForTimeout(left); };
  let i=0;
  for (const sc of scenes){
    i++;
    if (sc.card){
      const file = path.join(outdir, `card${i}.html`);
      const dur = Math.max(sc.dur||5, sc.sayDur ? sc.sayDur + 0.8 : 0);
      const u = card(file, {...sc.card, dur});
      console.log(`[${i}] card ${sc.card.title.replace(/<[^>]+>/g,'')}`);
      await page.goto(u); if (sc.audio) clips.push({file: sc.audio, at: (Date.now()-T0)/1000 + 0.35});
      await page.waitForTimeout(dur*1000);
      continue;
    }
    console.log(`[${i}] ${sc.url.split('/apps/')[1]} — ${sc.caption}`);
    await page.goto('about:blank'); // every scene starts from a fresh document
    await page.goto(sc.url); await page.waitForTimeout(sc.settle||900);
    await page.evaluate(OVERLAY);
    const started = Date.now(); if (sc.audio) clips.push({file: sc.audio, at: (started-T0)/1000 + 0.3});
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
    await holdFor(sc, started);
    await page.evaluate(()=>window.cxFade(true)); await page.waitForTimeout(650);
  }
  await page.close(); await ctx.close(); await b.close();
  const webm = fs.readdirSync(outdir).find(f=>f.endsWith('.webm'));
  const mp4 = path.resolve(__dirname, 'out', name + '.mp4');
  const vargs = ['-c:v','libx264','-preset','slow','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart','-r','25'];
  if (clips.length){
    const track = path.join(outdir, 'track.wav'); buildTrack(clips, track);
    execFileSync(FF, ['-y','-hide_banner','-loglevel','error','-i', path.join(outdir, webm), '-i', track, ...vargs, '-c:a','aac','-b:a','128k','-af','highpass=f=80,loudnorm=I=-18:TP=-1.5:LRA=9','-shortest', mp4]);
  } else {
    execFileSync(FF, ['-y','-hide_banner','-loglevel','error','-i', path.join(outdir, webm), ...vargs, mp4]);
  }
  console.log('wrote', mp4, (fs.statSync(mp4).size/1e6).toFixed(1)+' MB');
  return mp4;
}
module.exports = { run, app, OVERLAY };
