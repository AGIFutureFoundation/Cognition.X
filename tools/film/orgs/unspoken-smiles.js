// Promo film — Cognition.X, the Flow Hub app, opened and closed by a real-world
// frame: Unspoken Smiles, the oral-health NGO founded by Jean Paul Laurent in
// 2014. No affiliation, no endorsement, not consulted, no partnership — this
// film only cites their own public record and then shows curriculum that
// already exists in Cognition.X because it happens to teach the same domain.
// It was not written for them and nothing here is presented as being theirs.
//   NODE_PATH=$(npm root -g) node tools/film/orgs/unspoken-smiles.js
const { run, app } = require('../film');

const rowWith = (text) => `(function(){const r=[...document.querySelectorAll('table tr')].find(x=>x.textContent.includes(${JSON.stringify(text)})); if(r) r.scrollIntoView({behavior:'smooth',block:'center'});})()`;
const themeWith = (text) => `(function(){const s=[...document.querySelectorAll('.theme summary')].find(x=>x.textContent.includes(${JSON.stringify(text)})); if(s){s.closest('details').open=true; s.scrollIntoView({behavior:'smooth',block:'center'});}})()`;
const trackHead = (text) => `(function(){const h=[...document.querySelectorAll('.trackhead h3')].find(x=>x.textContent.includes(${JSON.stringify(text)})); if(h) h.closest('.trackhead').scrollIntoView({behavior:'smooth',block:'start'});})()`;

run('org-unspoken-smiles', [
 {card:{kicker:'Cognition.X · a frame, not a partnership', title:'A child who learns to <b>brush</b> can learn to <b>teach it.</b>', sub:'Unspoken Smiles — founded by Jean Paul Laurent in 2014 — trains community oral-health educators and teaches prevention in schools worldwide. It has not seen this film, was not consulted, and has no relationship with this platform.', lines:['no affiliation','not consulted','public record only'], theme:'teal', dur:10},
  say:"Unspoken Smiles is a real organisation, founded by Jean Paul Laurent in twenty fourteen after the Haiti earthquake, working in oral health education and prevention in schools, and training community members as oral health educators. It has not seen this film, has not been asked, and has no relationship with this platform. What follows already exists in Cognition dot X, shown because it happens to teach the same domain — not written for them, and not a partnership."},

 {url:app('flow-hub'), settle:1400, chapter:'One system', caption:'17,450 blocks · 47 packs · 225 tracks · five grade bands, K through adult.',
  say:"This is the Flow Hub, one view onto Cognition X's whole dataset. Seventeen thousand four hundred and fifty blocks, forty seven packs, two hundred and twenty five tracks, five grade bands from kindergarten through adult. Every block is one capability, at one grade, proven by a transfer check on real material — not a quiz.",
  steps:[{drift:260, ms:1600}]},

 {url:app('flow-hub'), settle:1400, chapter:'A peer-educator ladder, already in the dataset', caption:'Brush Captain (K–2) → Prevention Scout (3–5) → Peer Educator I (6–8) → Peer Educator II (9–10) → Community Oral Health Educator (11–12).',
  say:"Search the dataset for oral health, and one foundation pack surfaces a full peer-educator ladder that was authored long before this film: Brush Captain in kindergarten through second grade, Prevention Scout in third through fifth, Peer Educator One in middle school, Peer Educator Two in high school, and Community Oral Health Educator at the top — mapping a two-year and a six-year path with named local programs.",
  steps:[{click:'.navbtn[data-view="packs"]', dwell:600},{type:'#packsearch', text:'oral health', dwell:900},{eval:rowWith('Brush Captain (platform certificate)'), dwell:2200},{drift:260, ms:2200},{eval:rowWith('Prevention Scout'), dwell:1800},{drift:260, ms:2200},{eval:rowWith('Community Oral Health Educator'), dwell:2600},{cap:'Every row carries its own transfer check — a real task, not a multiple-choice question.', dwell:2600}]},

 {url:app('flow-hub'), settle:1400, chapter:'The same domain, a second track', caption:'Oral Health Peer · ten themes · five bands each, from "what a tooth is made of" to "caring for somebody else’s mouth."',
  say:"A second, separate track in the dataset — Oral Health Peer — covers the same ground from a different angle: what a tooth is made of, why gums bleed, fluoride without argument, the dental visit nobody has had, and caring for somebody else's mouth. Ten themes, five grade bands each, the same shape as every other credential on this platform.",
  steps:[{click:'.navbtn[data-view="packs"]', dwell:500},{type:'#packsearch', text:'Preventive Health', dwell:900},{eval:trackHead('The mouth, understood'), dwell:2000},{eval:themeWith('What a tooth is made of'), dwell:2400},{drift:260, ms:2000},{eval:themeWith('Caring for somebody else'), dwell:2400}]},

 {url:app('flow-hub'), settle:1400, chapter:'And forty-six other packs', caption:'Robotics · Global Health OS · Science · trades, civics, languages, the arts — the same block shape, every time.',
  say:"Oral health is two packs out of forty seven. The same shape — a theme, five bands, a real transfer check — runs the trades, the sector operating systems, civics, languages and the arts. Switch the pack in the flow setup, and the machinery underneath is identical.",
  steps:[{click:'.navbtn[data-view="flow"]', dwell:700},{select:'#fs-pack', value:'3', dwell:1400},{cap:'Global Health OS — 1,160 blocks', dwell:1600},{select:'#fs-pack', value:'2', dwell:1400},{cap:'Robotics OS — 1,140 blocks', dwell:1600}]},

 {url:app('flow-hub'), settle:1400, chapter:'Eight agents, one swarm', caption:'One shared blackboard, priority arbitration — exactly one agent intervenes per move, never a chorus.',
  say:"Eight rule-based agents run the session machinery so attention stays on the block in front of a learner, not the interface. Four tutors share one blackboard of the session; each proposes an intervention, and priority arbitration lets exactly one act per move.",
  steps:[{click:'.navbtn[data-view="agents"]', dwell:700},{scroll:'#agentgrid', dwell:1800},{drift:260, ms:1800}]},

 {url:app('flow-hub'), settle:1400, chapter:'The credential rule', caption:'A track’s credential is earned when all ten of its themes have a completed transfer check — witnessed, not self-reported.',
  say:"And the rule that holds the whole platform honest: a track's credential is earned only when all ten of its themes carry a completed, witnessed transfer check. The ledger lives in the learner's own browser; nothing about them leaves the page on its own.",
  steps:[{click:'.navbtn[data-view="ledger"]', dwell:700},{scroll:'.lede', dwell:1800},{drift:260, ms:1600}]},

 {card:{kicker:'A frame, restated', title:'Not their platform. <b>Not their claim.</b>', sub:'Unspoken Smiles was not consulted and has made no endorsement. Cognition.X: open source, offline-first, every check witnessed. github.com/AGIFutureFoundation/Cognition.X', lines:['open source','no affiliation claimed','nothing leaves a page on its own'], theme:'teal', dur:10},
  say:"To be plain a second time: Unspoken Smiles did not ask for this, was not consulted, and has endorsed nothing here. What is real is the platform itself — Cognition X, open source, offline first, every credential backed by a witnessed check. If a program like theirs ever wanted curriculum shaped like this, it is already built, and it is free."},
]).then(()=>console.log('DONE unspoken-smiles')).catch(e=>{console.error(e);process.exit(1);});
