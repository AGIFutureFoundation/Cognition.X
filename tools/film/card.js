// Title-card generator for the film kit: a self-contained 1920x1080 page with kinetic type.
const fs = require('fs');
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
function card(file, {kicker='', title='', sub='', lines=[], dur=5, theme='ink'}) {
  const bg = theme==='gold' ? 'radial-gradient(1200px 700px at 30% 20%, #3a2a08 0%, #0E1E2E 60%)'
           : theme==='teal' ? 'radial-gradient(1200px 700px at 70% 80%, #0f3f3a 0%, #0E1E2E 60%)'
           : 'radial-gradient(1200px 700px at 50% 40%, #16304a 0%, #0A1622 65%)';
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
  html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#0A1622}
  .stage{position:relative;width:1920px;height:1080px;background:${bg};color:#E6EDF3;font-family:Georgia,'Times New Roman',serif}
  .grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:96px 96px;animation:drift ${dur+2}s linear both}
  @keyframes drift{from{transform:translate(0,0) scale(1.06)}to{transform:translate(-40px,-24px) scale(1)}}
  .cells{position:absolute;inset:0;opacity:.35}
  .cells i{position:absolute;border:1px solid rgba(184,135,31,.55);border-radius:50% 40% 55% 45%;animation:pulse 6s ease-in-out infinite}
  @keyframes pulse{0%,100%{transform:scale(1);opacity:.5}50%{transform:scale(1.06);opacity:.9}}
  .wrap{position:absolute;left:160px;right:160px;top:50%;transform:translateY(-50%)}
  .kicker{font:700 26px/1 'IBM Plex Mono',ui-monospace,Menlo,monospace;letter-spacing:.32em;text-transform:uppercase;color:#D9A441;opacity:0;animation:up .8s .2s ease-out forwards}
  h1{font:800 118px/1.02 Georgia,serif;margin:22px 0 0;letter-spacing:-.01em;opacity:0;animation:up .9s .5s cubic-bezier(.2,.8,.2,1) forwards}
  h1 b{color:#D9A441;font-weight:800}
  .sub{font:400 40px/1.3 Georgia,serif;color:#B8C7D3;margin:28px 0 0;max-width:1400px;opacity:0;animation:up .9s 1s ease-out forwards}
  .lines{display:flex;gap:28px;margin:54px 0 0;flex-wrap:wrap}
  .lines span{font:600 27px/1 ui-monospace,Menlo,monospace;color:#E6EDF3;border:1.5px solid rgba(217,164,65,.7);border-radius:999px;padding:16px 26px;opacity:0;animation:up .7s ease-out forwards}
  .rule{position:absolute;left:160px;bottom:120px;height:4px;width:0;background:#D9A441;animation:rule ${dur}s .3s linear forwards}
  @keyframes rule{to{width:1600px}}
  .brand{position:absolute;right:160px;bottom:96px;font:600 26px ui-monospace,Menlo,monospace;color:#8FA3B4;letter-spacing:.14em}
  @keyframes up{from{opacity:0;transform:translateY(36px)}to{opacity:1;transform:none}}
  .fade{position:absolute;inset:0;background:#000;animation:fin .6s ease-out forwards, fout .6s ${dur-0.6}s ease-in forwards}
  @keyframes fin{from{opacity:1}to{opacity:0}} @keyframes fout{from{opacity:0}to{opacity:1}}
  </style></head><body><div class="stage"><div class="grid"></div><div class="cells">
  ${[...Array(9)].map((_,i)=>`<i style="left:${(i*211)%1800+40}px;top:${(i*397)%900+60}px;width:${180+(i*53)%240}px;height:${140+(i*71)%200}px;animation-delay:${i*.7}s"></i>`).join('')}
  </div><div class="wrap">${kicker?`<div class="kicker">${esc(kicker)}</div>`:''}<h1>${title}</h1>${sub?`<p class="sub">${esc(sub)}</p>`:''}
  ${lines.length?`<div class="lines">${lines.map((l,i)=>`<span style="animation-delay:${1.3+i*.18}s">${esc(l)}</span>`).join('')}</div>`:''}</div>
  <div class="rule"></div><div class="brand">COGNITION.X</div><div class="fade"></div></div></body></html>`;
  fs.writeFileSync(file, html);
  return 'file://' + require('path').resolve(file);
}
module.exports = { card };
