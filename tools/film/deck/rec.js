// Records the deck slide by slide to the narration timings; see gen.py for the pipeline.
// Narration clips are synthesized first: python3 -m piper (see ../film.js) into audio/, then this
// script records, builds the aligned track and muxes with ffmpeg.
const { chromium } = require('playwright');
const path=require('path'); process.chdir(__dirname);
const fs=require('fs'); const idx=JSON.parse(fs.readFileSync('audio/index.json'));
const PAD=0.5;
(async () => {
  fs.rmSync('out',{recursive:true,force:true});
  const b = await chromium.launch({executablePath: process.env.CX_CHROMIUM || '/opt/pw-browsers/chromium'});
  const ctx = await b.newContext({viewport:{width:1920,height:1080}, recordVideo:{dir:'out', size:{width:1920,height:1080}}});
  const page = await ctx.newPage();
  await page.goto('file://'+process.cwd()+'/preview.html#title'); await page.waitForTimeout(1200);
  await page.addStyleTag({content:'.nav{display:none!important}'});
  const t0=Date.now(); const marks=[];
  for (const s of idx){
    await page.evaluate(id=>{ location.hash='#'+id; }, s.id);
    marks.push({id:s.id, at:(Date.now()-t0)/1000});
    await page.waitForTimeout(Math.round((s.dur+PAD)*1000));
  }
  await page.waitForTimeout(800);
  const lead=(marks[0].at); fs.writeFileSync('out/marks.json', JSON.stringify({lead, marks}));
  await page.close(); await ctx.close(); await b.close();
  console.log('recorded; lead-in', lead.toFixed(2),'s; total', ((Date.now()-t0)/1000).toFixed(1),'s');
})();
