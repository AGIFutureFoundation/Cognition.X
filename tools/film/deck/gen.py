"""The pitch deck generator: writes deck.html (15 slides, 16:9, keyboard/click
navigation, the platform's own tokens and faces), preview.html (a full
document for local recording) and narration.json (one `say` per slide).

    python3 tools/film/deck/gen.py        # after `node shots.js` captured the screens
    node tools/film/deck/shots.js         # real app screenshots the slides embed
    node tools/film/deck/rec.js           # record + narrate (piper) + mux -> out/cognitionx-pitch-deck.mp4

Every number on the slides is the dataset's; the opening block is row
CX-MUSICIND-0054 read from data/blocks.csv, unedited."""
import json, html
E=html.escape
import csv, os
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..','..','..'))
rows=list(csv.DictReader(open(os.path.join(ROOT,'data','blocks.csv'),newline='',encoding='utf-8')))
blk=[r for r in rows if r['block_id']=='CX-MUSICIND-0054'][0]  # the block the walkthrough opens with
S=[]  # slides: dict(id, kind, ...) + narration
S.append(dict(id='title', kind='title', kicker='AGI Future Foundation · pitch · v0.49.1', title='Learning you can <em>verify.</em>', sub='Cognition.X — an open, offline learning system that turns education into blocks a person can prove, and hands them a record anyone can check.',
 say="Cognition X. Learning you can verify. An open, offline learning system that turns education into blocks a person can prove, and hands the learner a record anyone can check. This is a walkthrough for investors."))
S.append(dict(id='problem', kind='points', kicker='The problem', title='Most training ends with a certificate that says you sat in the room.',
 points=[('Containers, not proof','Lessons, videos and courses measure attendance. Nobody can check what a person can actually do.'),
         ('Platforms are feeds','Content arrives at one pace for everyone; the learner who is overloaded and the one who is bored get the same next item.'),
         ('Records are locked in','Progress lives in a vendor\'s database, behind an account, on a server the school does not own.'),
         ('The trades and the civic professions are worst served','The jobsite, the kitchen, the council chamber — the places where doing is the whole point — get the least verifiable curriculum of all.')],
 say="Most training ends with a certificate that says you sat in the room. Lessons, videos and courses measure attendance; nobody can check what a person can actually do. Platforms are feeds, delivering the same next item to the overloaded learner and the bored one. Records are locked in a vendor's database. And the trades and the civic professions, where doing is the whole point, get the least verifiable curriculum of all."))
S.append(dict(id='unit', kind='block', kicker='The unit', title='The unit is a block: one capability, one grade band, one transfer check on real material.', blk=blk,
 say="Cognition X chose the smallest thing that can be verified: a block. One capability, at one grade band, described in a sentence, and proven by a transfer check on real material. Here is one, exactly as it sits in the dataset. Collect twenty song ideas in a week, and develop one into a hook with a recorded eight bars. Fifty of these make a track. Ten themes across five grade bands. One named credential at the end."))
S.append(dict(id='manifest', kind='numbers', kicker='What exists today', title='Built, tested and shipped — forty-nine releases in.',
 nums=[('17,450','blocks'),('47','packs'),('225','tracks · credentials'),('64','parish dashboards'),('8','Trade Halls'),('222','union & trade entries'),('50','states localized'),('6','offline apps')],
 say="This is not a plan. Seventeen thousand four hundred and fifty blocks, forty-seven packs, two hundred twenty-five tracks each ending in a named credential. Sixty-four parish dashboards, eight Trade Halls, two hundred twenty-two union and trade entries, all fifty states localized, and six applications that each run from a single file, offline, on any device. Forty-nine releases, every one merged with the build green."))
S.append(dict(id='loop', kind='loop', kicker='The learning loop', title='A loop, not a feed — every stage is running code.',
 steps=[('A block is chosen','the flow engine sizes it to the learner\'s channel'),('Work on real material','the transfer check, not a quiz'),('Felt difficulty reported','breezed it · in the flow · struggled'),('An assessor witnesses','confirm, or an honest not-yet'),('The credential fires at fifty','automatically, by name'),('The record leaves with the learner','signed, portable, verifiable offline')],
 say="Here is what a learner goes through. A block is chosen, sized by the flow engine to where the learner's channel sits. The work happens on real material. The learner reports the felt difficulty, and the engine raises, holds or eases the band. An assessor witnesses the check: confirm, or an honest not yet with no credit. At fifty checks the credential fires automatically, by name. And the record leaves in the learner's hand, signed by the hall's own keys, verifiable offline by anyone."))
S.append(dict(id='flow', kind='shot', kicker='The automated flow system', title='The intelligence lives on the device — and never phones home.', img='shot-roles.png',
 points=[('Flow-state engine','shrinks the step under overload, stretches it when cruising, calls the break on the learner\'s own cadence'),('20 access modules','chosen supports, never diagnoses'),('24-agent dashboard swarms','seven roles, a shared blackboard, priority arbitration — agents propose; the person disposes'),('The Network OS','eight automations on a live pulse across the Trade Halls, every call drillable to its rows')],
 say="The part usually called the A I is, in Cognition X, a set of automations that live inside the page. A flow state engine keeps each learner in their channel. Twenty access modules tune the cadence and the check format, as chosen supports, never diagnoses. Twenty four agents sit behind the seven role dashboards on a shared blackboard; priority arbitration surfaces one call as the swarm's, and every agent's own reasoning stays visible. Agents propose; the person disposes. And the Network O S runs the Trade Halls with eight automations on a live pulse. None of it phones home. That is the product's strongest property."))
S.append(dict(id='louisiana', kind='shot', kicker='The flagship', title='Cognition.X Louisiana: sixty-four parishes, one platform.', img='shot-state.png',
 points=[('An independent dashboard for every parish','seat, school systems, industries, narrative world'),('A module plan earned from each economy','Plaquemines gets energy, port and culinary; St. Landry gets music and the kitchen — with the reason stated'),('A two-year, two-wave rollout','33 parishes in 2026–27, all 64 by 2027–28, with launch curriculum, readiness boards and budget sketches'),('Offline-first','rural parishes get paper-evidence wording; a USB stick is a deployment')],
 say="The flagship is Louisiana: the whole platform modelled onto one state's real structure. Sixty four parishes, each with its own dashboard and a module plan earned from its own economy, with the reason stated in words. A two year, two wave rollout: thirty three parishes in year one, all sixty four by year two, with a launch curriculum, readiness boards and a budget sketch for each. It runs offline, so a rural parish can start with a USB stick and paper evidence."))
S.append(dict(id='makers', kind='shot2', kicker='Parish dashboards · the Makers\' Hall', title='Every parish sees its own plan — and its own makers.', imgs=['shot-parish.png','shot-makers.png'],
 say="Every parish dashboard shows the plan it earned, its five rung mission module, and now the Makers' Hall: music from the first note to the industry's every role, the professional kitchen from knife to ownership, the art and craft trades from seeing to the working studio. Each is a pathway whose stages are the tracks of its pack, taught through sixty three makers from the public record spread across every region, so a learner in any parish can claim one."))
S.append(dict(id='institute', kind='shot2', kicker='The flagship curriculum', title='The Legacy Institute: leadership, ethics and civic duty, taught as craft.', imgs=['shot-institute.png','shot-ladder.png'],
 foot='Built on the public record and published principles of the Willie L. Brown Jr. Institute of Politics and Public Service. Not affiliated with, endorsed by, or reviewed by the Institute; a named track would be offered under a partnership agreement and the Institute\'s review of every course.',
 say="The civic cornerstone of every edition is the Legacy Institute: a leadership program built on the public record and published principles of the Willie L. Brown Junior Institute of Politics and Public Service. Twelve principles, each traced to its source. Five strands across five eras, one hundred twenty five courses, a ten module method, bridge projects, a graduation seal, and the Fellowship pattern of paid public agency placements at the top. For educators, the Leadership Ladder is the training track, and one template localizes it to any state or country. We carry the Institute's disclaimer verbatim: this is a proposal, not an affiliation. The partnership is the opportunity."))
S.append(dict(id='trades', kind='shot', kicker='Trades · unions · SmartCiti.X', title='The same block model, pointed at work.', img='shot-trades.png',
 points=[('222 entries · 37 trade families · 6 regions on two coasts','San Francisco, Oakland, New Orleans, Baton Rouge, Houston, Los Angeles'),('A localized training sim for every family','the rigging plot with every point\'s weight, the banquet line on the 200-cover clock'),('The curriculum engine behind SmartCiti.X','the VR/AR training center for the trades and unions'),('Simulation ≠ certification','the hall certifies; the platform proves practice — and never a local number')],
 say="The Trades Network is the same block model pointed at work: thirty seven trade families across six regions on two coasts, two hundred twenty two entries, each with a training simulation localized to a real site and a classroom hook into math, science, English and civics. This is the curriculum engine behind SmartCiti X, the V R and A R training center for the trades and unions. Simulation is not certification: the hall certifies, the platform proves practice."))
S.append(dict(id='records', kind='shot', kicker='Records people can carry', title='Signed by the hall. Verified by anyone. Owned by the learner.', img='shot-loop.png',
 points=[('ECDSA P-256 in the browser','the Records Office signs portable cx-credential/1 files'),('Four verification grades','invalid · unknown key · signed by trusted office “X” · revoked'),('Federation between halls','signed trust lists and revocation lists, confirmed out of band'),('Standards next','W3C Verifiable Credentials / Open Badges 3.0 is an envelope change on the roadmap')],
 say="A hall's Records Office is a key pair in the browser that signs ledger earned credentials into portable files. Verification is offline and graded four ways: invalid, unknown key, signed by a trusted office by name, or revoked. Halls federate by exchanging signed trust lists, confirmed out of band. The signature proves integrity and key possession; identity is confirmed by people. Alignment to W three C verifiable credentials is an envelope change, already on the roadmap."))
S.append(dict(id='states', kind='shot', kicker='Scale', title='One state is the pattern. Fifty are data. Any country is a template.', img='shot-states.png',
 points=[('The States OS blueprint','250 blocks localized for all fifty states from a fact base'),('The Institute Model in every capital','one localizer, any state or country'),('Adding a state is a data file, not a rebuild','three legacy localizations already exist'),('Organisations too','non-profit, corporate, multilateral and global-health packs; Pack Studio for authoring your own')],
 say="Louisiana is the pattern. The States O S blueprint localizes for all fifty states from a fact base, with the Institute Model in every capital, and the same template reaches any country. Adding a state is a data file, not a rebuild. Organisations get the same engine: non profit, corporate, multilateral and global health packs, and a Pack Studio to author their own."))
S.append(dict(id='trust', kind='points', kicker='Built to be trusted', title='Reproducible, tested, and honest about what it does not claim.',
 points=[('Byte-for-byte from a fresh clone','every pack from its spec, every app from its template — proven in CI on every push'),('452 mechanical checks · 89 browser assertions','the stances are tests, not slogans'),('Nothing leaves the page on its own','no server, no account, no telemetry; export is a deliberate act'),('Open by design','MIT code · CC BY 4.0 curriculum — a district can adopt without asking')],
 say="Everything ships as six single files that open anywhere. A fresh clone plus Python regenerates the entire platform byte for byte, and the build proves it on every push, alongside four hundred fifty two mechanical checks and eighty nine browser assertions that drive the working models for real. The honesty stances are tests, not slogans: simulation is not certification; access profiles are never diagnoses; nothing leaves the page on its own. And it is open by design, so a district can adopt it without asking."))
S.append(dict(id='ask', kind='points', kicker='Where it stands · what comes next', title='The road to v1.0 is operational, not code.',
 points=[('The v1.0 gate, as the roadmap states it','a named external cohort — one hall, one class — completes credentials on an instance and holds verifiable records'),('A first parish cohort and its assessor network','the loop run by real teachers on real material'),('The curriculum review board, seated','working the evidence loop into block revisions'),('The first named Trade Hall with SmartCiti.X','the Network OS on a live floor'),('The Institute partnership, on the Institute\'s terms',''),('The credential envelope aligned to W3C','so the records interoperate beyond our own halls')],
 say="Forty nine releases in, the foundation and data phases are complete and the platform phase nearly so. The remaining road to version one is operational: a named external cohort, one hall, one class, completing credentials and holding verifiable records. That is what the next stage funds. A first parish cohort and its assessor network. The curriculum review board seated. The first named Trade Hall running the Network O S with SmartCiti X. The Institute partnership, on the Institute's terms. And the credential envelope aligned to the W three C standard. The software to do all of it exists today, in one repository, and every claim in this deck can be opened and clicked."))
S.append(dict(id='close', kind='title', kicker='Cognition.X · AGI Future Foundation', title='Open. Offline. <em>Honest.</em>', sub='github.com/AGIFutureFoundation/Cognition.X — the dataset, the six apps, the roadmap, the tests. Nothing leaves the page on its own.',
 say="Cognition X. Open, offline, and honest. The dataset, the six apps, the roadmap and the tests are all at github dot com slash A G I Future Foundation slash Cognition dot X. Thank you."))

def block_html(b):
    return f'''<div class="blk"><div class="bid">{E(b['block_id'])} <span>· {E(b['pack'])}</span></div>
 <div class="grid2"><div><i>Track</i>{E(b['track'])} · {E(b['code'])}</div><div><i>Theme</i>{E(b['theme'])}</div><div><i>Band · level</i>{E(b['grade'])} · {E(b['level'])}</div><div><i>Credential</i>{E(b['credential'])}</div></div>
 <div class="desc"><i>Description</i>{E(b['description'])}</div>
 <div class="check"><i>Transfer check</i>{E(b['transfer_check'])}</div></div>'''

def slide(s,i,n):
    k=s['kind']; head=f'<p class="kicker">{E(s["kicker"])}</p>'
    if k=='title':
        inner=f'<div class="center"><p class="kicker">{E(s["kicker"])}</p><h1>{s["title"]}</h1><p class="sub">{E(s["sub"])}</p></div>'
    elif k=='points':
        inner=head+f'<h2>{E(s["title"])}</h2><ul class="pts">'+''.join(f'<li><b>{E(a)}</b>{("<span>"+E(b)+"</span>") if b else ""}</li>' for a,b in s['points'])+'</ul>'
    elif k=='block':
        inner=head+f'<h2>{E(s["title"])}</h2>'+block_html(s['blk'])
    elif k=='numbers':
        inner=head+f'<h2>{E(s["title"])}</h2><div class="nums">'+''.join(f'<div><b>{E(a)}</b><span>{E(b)}</span></div>' for a,b in s['nums'])+'</div>'
    elif k=='loop':
        inner=head+f'<h2>{E(s["title"])}</h2><ol class="steps">'+''.join(f'<li><span class="n">{j+1}</span><b>{E(a)}</b><span>{E(b)}</span></li>' for j,(a,b) in enumerate(s['steps']))+'</ol>'
    elif k=='shot':
        inner=head+f'<h2>{E(s["title"])}</h2><div class="split"><ul class="pts small">'+''.join(f'<li><b>{E(a)}</b><span>{E(b)}</span></li>' for a,b in s['points'])+f'</ul><figure class="shot"><img src="{s["img"]}" alt=""></figure></div>'
    elif k=='shot2':
        inner=head+f'<h2>{E(s["title"])}</h2><div class="two">'+''.join(f'<figure class="shot"><img src="{im}" alt=""></figure>' for im in s['imgs'])+'</div>'+(f'<p class="foot">{E(s["foot"])}</p>' if s.get('foot') else '')
    return f'<section class="slide k-{k}" id="{s["id"]}" data-i="{i}">{inner}<div class="pn"><span>COGNITION.X</span><span>{i+1} / {n}</span></div></section>'

n=len(S)
slides=''.join(slide(s,i,n) for i,s in enumerate(S))
CSS='''
:root{--paper:#F3F5F8;--paper2:#FFFFFF;--paper3:#E9EEF2;--ink:#0E1E2E;--ink2:#3E5266;--faint:#6F8195;--line:#D6DEE5;--gold:#B8871F;--gold-ink:#8A6210;--gold-wash:#F6EFDF;--teal:#1E7A72;--teal-wash:#E3F1EF;--dark:#0A1622}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--paper:#0E1E2E;--paper2:#122536;--paper3:#18304A;--ink:#E6EDF3;--ink2:#B8C7D3;--faint:#8FA3B4;--line:#26405A;--gold:#D9A441;--gold-ink:#E2B860;--gold-wash:#2A2610;--teal:#4FC3B6;--teal-wash:#0F3733}}
:root[data-theme="dark"]{--paper:#0E1E2E;--paper2:#122536;--paper3:#18304A;--ink:#E6EDF3;--ink2:#B8C7D3;--faint:#8FA3B4;--line:#26405A;--gold:#D9A441;--gold-ink:#E2B860;--gold-wash:#2A2610;--teal:#4FC3B6;--teal-wash:#0F3733}
*{box-sizing:border-box} html,body{height:100%}
body{margin:0;background:var(--dark);color:var(--ink);font:400 26px/1.4 "IBM Plex Sans",system-ui,sans-serif;overflow:hidden}
.stage{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform:translate(-50%,-50%) scale(var(--s,1));transform-origin:center}
.slide{position:absolute;inset:0;background:var(--paper);padding:96px 120px 90px;display:none;flex-direction:column;gap:22px}
.slide.on{display:flex} .slide.k-points,.slide.k-numbers,.slide.k-loop,.slide.k-block{justify-content:center;padding-bottom:140px} .slide.k-title{background:radial-gradient(1200px 700px at 30% 30%,#16304a 0%,#0A1622 65%);color:#E6EDF3;justify-content:center}
.slide.k-title .kicker{color:#D9A441} .slide.k-title .sub{color:#B8C7D3}
.kicker{font:600 20px/1 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.26em;text-transform:uppercase;color:var(--gold-ink);margin:0}
h1{font-family:Fraunces,Georgia,serif;font-variation-settings:"opsz" 144;font-weight:800;font-size:132px;line-height:.98;letter-spacing:-.015em;margin:14px 0 0;max-width:15ch;text-wrap:balance}
h1 em{font-style:italic;font-weight:400;color:#D9A441}
.sub{font-family:Fraunces,Georgia,serif;font-variation-settings:"opsz" 30;font-size:36px;line-height:1.35;margin:26px 0 0;max-width:34ch;text-wrap:balance}
h2{font-family:Fraunces,Georgia,serif;font-variation-settings:"opsz" 96;font-weight:600;font-size:62px;line-height:1.1;letter-spacing:-.012em;margin:0;max-width:22ch;text-wrap:balance}
.center{max-width:1500px}
.pts{list-style:none;margin:18px 0 0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 48px}
.pts li{border-top:3px solid var(--gold);padding-top:14px;font-size:27px;line-height:1.35}
.pts li b{display:block;font-weight:600;margin:0 0 6px;font-size:30px} .pts li span{color:var(--ink2)}
.pts.small{grid-template-columns:minmax(0,1fr);gap:16px;font-size:23px;align-content:start} .pts.small li{padding-top:10px} .pts.small li b{font-size:25px;margin-bottom:3px} .pts.small li span{font-size:22px}
.split{display:grid;grid-template-columns:660px minmax(0,1fr);gap:48px;align-items:start;flex:1;min-height:0;margin-top:10px}
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:36px;flex:1;min-height:0;margin-top:14px}
.shot{margin:0;background:var(--paper2);border:1px solid var(--line);box-shadow:0 24px 60px rgba(14,30,46,.18);overflow:hidden;min-height:0;height:100%;max-height:700px}
.shot img{display:block;width:100%;height:100%;object-fit:cover;object-position:top}
.foot{font-size:19px;line-height:1.4;color:var(--faint);margin:6px 0 0;max-width:120ch}
.nums{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:28px;margin-top:30px}
.nums div{background:var(--paper2);border:1px solid var(--line);border-top:5px solid var(--gold);padding:28px 30px 24px}
.nums b{display:block;font-family:Fraunces,Georgia,serif;font-variation-settings:"opsz" 96;font-weight:800;font-size:78px;line-height:1;color:var(--gold-ink);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.nums span{display:block;margin-top:10px;font-size:25px;color:var(--ink2)}
.steps{list-style:none;margin:26px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px 40px;counter-reset:s}
.steps li{display:grid;grid-template-columns:64px minmax(0,1fr);gap:0 16px;border-top:1px solid var(--line);padding-top:18px;font-size:24px;line-height:1.35}
.steps .n{grid-row:1/3;font-family:Fraunces,Georgia,serif;font-weight:800;font-size:60px;line-height:1;color:var(--teal);font-variant-numeric:tabular-nums}
.steps b{font-size:28px;font-weight:600} .steps span:not(.n){color:var(--ink2)}
.blk{margin-top:26px;background:var(--paper2);border:1px solid var(--line);border-left:8px solid var(--gold);padding:28px 36px;display:grid;gap:18px;font-size:26px}
.blk .bid{font:600 22px/1 "IBM Plex Mono",monospace;letter-spacing:.06em;color:var(--gold-ink)} .blk .bid span{font-weight:400;color:var(--faint)}
.blk i{display:block;font:600 15px/1 "IBM Plex Mono",monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--faint);font-style:normal;margin-bottom:6px}
.blk .grid2{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px 30px}
.blk .check{font-family:Fraunces,Georgia,serif;font-variation-settings:"opsz" 30;font-size:34px;line-height:1.35}
.pn{position:absolute;left:120px;right:120px;bottom:40px;display:flex;justify-content:space-between;font:500 17px/1 "IBM Plex Mono",monospace;letter-spacing:.2em;color:var(--faint)}
.k-title .pn{color:#8FA3B4}
.nav{position:fixed;right:18px;bottom:14px;display:flex;gap:6px;z-index:5}
.nav button{font:600 14px "IBM Plex Mono",monospace;background:rgba(14,30,46,.7);color:#fff;border:1px solid rgba(255,255,255,.25);border-radius:6px;padding:8px 12px;cursor:pointer}
.nav button:focus-visible{outline:2px solid #D9A441;outline-offset:2px}
@media (prefers-reduced-motion:no-preference){.slide.on>*{animation:up .55s cubic-bezier(.2,.8,.2,1) both} .slide.on>*:nth-child(2){animation-delay:.08s} .slide.on>*:nth-child(3){animation-delay:.16s} .slide.on>*:nth-child(4){animation-delay:.24s}}
@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
'''
JS='''
const slides=[...document.querySelectorAll('.slide')]; let cur=0;
function fit(){ const s=Math.min(innerWidth/1920, innerHeight/1080); document.documentElement.style.setProperty('--s', s); }
function show(i){ cur=Math.max(0,Math.min(slides.length-1,i)); slides.forEach((s,j)=>s.classList.toggle('on', j===cur)); history.replaceState(null,'','#'+slides[cur].id); }
function fromHash(){ const i=slides.findIndex(s=>'#'+s.id===location.hash); show(i<0?0:i); }
addEventListener('resize', fit); fit(); fromHash(); addEventListener('hashchange', fromHash);
addEventListener('keydown', e=>{ if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown'){e.preventDefault();show(cur+1);} if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(cur-1);} if(e.key==='Home')show(0); if(e.key==='End')show(slides.length-1); });
document.querySelector('#prev').addEventListener('click',()=>show(cur-1)); document.querySelector('#next').addEventListener('click',()=>show(cur+1));
document.querySelector('.stage').addEventListener('click', e=>{ if(e.target.closest('.nav')) return; show(cur+1); });
'''
page=f'''<title>Cognition.X Pitch Deck</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>{CSS}</style>
<div class="stage">{slides}</div>
<div class="nav"><button id="prev" aria-label="Previous slide">◀</button><button id="next" aria-label="Next slide">▶</button></div>
<script>{JS}</script>
'''
open(os.path.join(HERE,'deck.html'),'w').write(page)
open(os.path.join(HERE,'preview.html'),'w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head><body style="margin:0">'+page+'</body></html>')
json.dump([{'id':s['id'],'say':s['say']} for s in S], open(os.path.join(HERE,'narration.json'),'w'), ensure_ascii=False, indent=1)
print(n,'slides; narration words', sum(len(s['say'].split()) for s in S))
