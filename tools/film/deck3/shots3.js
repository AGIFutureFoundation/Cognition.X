const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const page = await b.newPage({viewport:{width:1920,height:1080}});
  for (const id of ['problem','solution','ask']){ await page.goto('file://'+process.cwd()+'/preview3.html#'+id); await page.waitForTimeout(1200); await page.screenshot({path:`p-${id}.png`}); }
  // PDF: three 16:9 pages
  await page.goto('file://'+process.cwd()+'/preview3.html'); await page.waitForTimeout(1200);
  await page.emulateMedia({media:'print'});
  await page.pdf({path:'AGI-Future-Foundation-Investor-Deck.pdf', width:'1920px', height:'1080px', printBackground:true, margin:{top:0,right:0,bottom:0,left:0}, preferCSSPageSize:false});
  for (const id of ['v-proof','v-round','v-cta']){ await page.emulateMedia({media:'screen'}); await page.goto('file://'+process.cwd()+'/preview.html#'+id); await page.waitForTimeout(1200); await page.screenshot({path:`p-${id}.png`}); }
  await b.close();
})();
