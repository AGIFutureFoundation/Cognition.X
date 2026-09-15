const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const page = await b.newPage({viewport:{width:1920,height:1080}});
  for (const [f,ids] of [['preview3.html',['problem','solution','ask']],['preview.html',['v-proof','v-portfolio','v-ask','v-round','v-cta']]]){
    for (const id of ids){ await page.goto('file://'+process.cwd()+'/'+f+'#'+id); await page.waitForTimeout(900);
      const o = await page.evaluate(id=>{ const s=document.getElementById(id); const r=s.getBoundingClientRect(); let over=0; s.querySelectorAll('*').forEach(e=>{ const b=e.getBoundingClientRect(); if(b.bottom>r.bottom-70 && b.height>0 && !e.closest('.pn')) over++; }); let overlap=0; const fs=s.querySelectorAll('.fine'); const fine=fs[fs.length-1]; if(fine){ const ft=fine.getBoundingClientRect().top; s.querySelectorAll('.ask *, .box, .prot, .stack').forEach(e=>{ if(e.closest('.fine'))return; const b=e.getBoundingClientRect(); if(b.height>0 && b.bottom>ft+1) overlap++; }); } return {over, overlap, sh:s.scrollHeight}; }, id);
      console.log(f, id, 'past footer:', o.over, 'overlapping fine print:', o.overlap, 'scrollHeight', o.sh);
      await page.screenshot({path:`p-${id}.png`}); }
  }
  await page.goto('file://'+process.cwd()+'/preview3.html'); await page.waitForTimeout(1000); await page.emulateMedia({media:'print'});
  await page.pdf({path:'AGI-Future-Foundation-Investor-Deck.pdf', width:'1920px', height:'1080px', printBackground:true, margin:{top:0,right:0,bottom:0,left:0}});
  await b.close();
})();
