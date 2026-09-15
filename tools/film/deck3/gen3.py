"""Three-page investor deck (deck3.html + PDF pages) and the eight-slide video edition (video3.html + narration3.json)."""
import json, html
E=html.escape
CSS='''
:root{--paper:#F3F5F8;--paper2:#FFFFFF;--paper3:#E9EEF2;--ink:#0E1E2E;--ink2:#3E5266;--faint:#5F6B7A;--line:#D6DEE5;--gold:#B8871F;--gold-ink:#7F5A00;--gold-wash:#F6EFDF;--teal:#1E7A72;--teal-wash:#E3F1EF;--dark:#0A1622;--red:#B22B2B}
*{box-sizing:border-box} html,body{height:100%}
body{margin:0;background:var(--dark);color:var(--ink);font:400 24px/1.4 "IBM Plex Sans",system-ui,sans-serif;overflow:hidden}
.stage{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform:translate(-50%,-50%) scale(var(--s,1));transform-origin:center}
.slide{position:absolute;inset:0;background:var(--paper);padding:84px 110px 80px;display:none;flex-direction:column;gap:18px}
.slide.on{display:flex}
.slide.dark{background:radial-gradient(1300px 760px at 28% 30%,#16304a 0%,#0A1622 65%);color:#E6EDF3}
.slide.dark .kicker{color:#D9A441} .slide.dark .sub{color:#B8C7D3} .slide.dark .pn{color:#8FA3B4}
.kicker{font:600 19px/1 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.26em;text-transform:uppercase;color:var(--gold-ink);margin:0}
h1{font-family:Fraunces,Georgia,serif;font-variation-settings:"opsz" 144;font-weight:800;font-size:112px;line-height:1;letter-spacing:-.015em;margin:12px 0 0;max-width:16ch;text-wrap:balance}
h1 em{font-style:italic;font-weight:400;color:#D9A441}
.sub{font-family:Fraunces,Georgia,serif;font-variation-settings:"opsz" 30;font-size:34px;line-height:1.35;margin:22px 0 0;max-width:36ch;text-wrap:balance}
h2{font-family:Fraunces,Georgia,serif;font-variation-settings:"opsz" 96;font-weight:600;font-size:52px;line-height:1.08;letter-spacing:-.012em;margin:0;max-width:24ch;text-wrap:balance}
.cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:34px;margin-top:22px}
.col{border-top:4px solid var(--gold);padding-top:14px}
.col b{display:block;font-size:28px;font-weight:600;margin:0 0 8px} .col p{margin:0;font-size:22px;color:var(--ink2);line-height:1.45}
.strip{margin-top:auto;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:16px;border-top:1px solid var(--line);padding-top:18px}
.strip div b{display:block;font-family:Fraunces,Georgia,serif;font-size:44px;line-height:1;color:var(--gold-ink);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.strip div span{display:block;font-size:17px;color:var(--ink2);margin-top:6px;line-height:1.3}
.striplab{font:600 15px/1 "IBM Plex Mono",monospace;letter-spacing:.18em;text-transform:uppercase;color:var(--faint);margin:0 0 -6px}
.split{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:40px;flex:1;min-height:0;margin-top:10px}
.loop{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin:8px 0 6px}
.loop div{background:var(--paper2);border:1px solid var(--line);border-top:4px solid var(--teal);padding:12px 12px 10px;font-size:17px;line-height:1.3;color:var(--ink2)}
.loop b{display:block;font-size:19px;color:var(--ink);margin-bottom:4px}
.loop i{display:block;font:800 26px/1 Fraunces,Georgia,serif;color:var(--teal);font-style:normal;margin-bottom:6px}
.lines{display:grid;gap:10px;margin-top:12px}
.lines div{display:grid;grid-template-columns:200px minmax(0,1fr);gap:16px;padding:10px 0;border-top:1px solid var(--line);font-size:20px;line-height:1.35}
.lines.mid div{font-size:17.5px;padding:7px 0;line-height:1.3} .lines.mid b{font-size:18px}
.lines.tight div{grid-template-columns:110px minmax(0,1fr);padding:6px 0;font-size:15.5px;line-height:1.3} .lines.tight b{font-size:15.5px}
.lines b{font-size:21px} .lines span{color:var(--ink2)}
.shot{margin:0;background:var(--paper2);border:1px solid var(--line);box-shadow:0 22px 56px rgba(14,30,46,.18);overflow:hidden;min-height:0;height:100%;max-height:560px}
.shot img{display:block;width:100%;height:100%;object-fit:cover;object-position:top}
.shots2{display:grid;grid-template-rows:1fr 1fr;gap:16px;min-height:0}
.shots2 .shot{max-height:270px}
.ask{display:grid;grid-template-columns:1fr 1fr;gap:34px;flex:1;min-height:0;margin-top:4px;align-items:start}
.ask table{font-size:16px} .ask td{padding:4px 10px 4px 0} .ask .lines.tight div{font-size:15px;padding:5px 0;gap:12px} .ask .lines.tight b{font-size:15px}
.ask .terms{font-size:14px;line-height:1.28;gap:4px 18px} .ask .box{padding:12px 18px} .ask .box h3{font-size:21px;margin-bottom:4px} .ask .box p{font-size:15.5px;line-height:1.35}
.stack{display:flex;height:54px;border-radius:10px;overflow:hidden;margin:18px 0 8px;font:600 15px/1.2 "IBM Plex Sans",system-ui,sans-serif}
.stack div{display:flex;align-items:center;justify-content:center;color:#fff;padding:0 10px;text-align:center}
.prot{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:16px}
.prot div{border:1px solid var(--line);border-radius:12px;padding:14px 18px;font-size:16px;line-height:1.35;color:var(--ink2);background:#fff}
.prot b{display:block;font:600 13px/1 "IBM Plex Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin-bottom:8px}
table{border-collapse:collapse;width:100%;font-size:17px;line-height:1.25}
th{text-align:left;font:600 13px/1.2 "IBM Plex Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);padding:0 10px 8px 0;border-bottom:2px solid var(--line)}
td{padding:5px 10px 5px 0;border-bottom:1px solid var(--line);color:var(--ink2);vertical-align:top} td b{color:var(--ink);font-weight:600}
td.r,th.r{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.total td{border-bottom:0;border-top:2px solid var(--ink);color:var(--ink);font-weight:600}
.box{background:var(--paper2);border:1px solid var(--line);border-left:6px solid var(--gold);padding:16px 20px;font-size:17px;line-height:1.35;color:var(--ink2)}
.box h3{font-family:Fraunces,Georgia,serif;font-size:23px;margin:0 0 6px;color:var(--ink)}
.box b{color:var(--ink)} .box p{margin:0 0 8px} .box p:last-child{margin:0}
.terms{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 22px;font-size:15.5px;line-height:1.3}
.terms div{padding:6px 0;border-top:1px solid var(--line)} .terms b{display:block;font-size:14px;font:600 13px/1 "IBM Plex Mono",monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin-bottom:5px}
.terms span{color:var(--ink)}
.cta{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:26px;margin-top:30px}
.cta div{border:1.5px solid rgba(217,164,65,.6);border-radius:14px;padding:22px 26px;font-size:24px;line-height:1.35;color:#E6EDF3}
.cta b{display:block;font:600 15px/1 "IBM Plex Mono",monospace;letter-spacing:.2em;text-transform:uppercase;color:#D9A441;margin-bottom:10px}
.fine{font-size:13.5px;line-height:1.35;color:var(--faint);margin:0}
.slide.dark .fine{color:#8FA3B4}
.pn{position:absolute;left:110px;right:110px;bottom:34px;display:flex;justify-content:space-between;font:500 16px/1 "IBM Plex Mono",monospace;letter-spacing:.2em;color:var(--faint)}
.nav{position:fixed;right:18px;bottom:14px;display:flex;gap:6px;z-index:5}
.nav button{font:600 14px "IBM Plex Mono",monospace;background:rgba(14,30,46,.7);color:#fff;border:1px solid rgba(255,255,255,.25);border-radius:6px;padding:8px 12px;cursor:pointer}
.nav button:focus-visible{outline:2px solid #D9A441;outline-offset:2px}
@media (prefers-reduced-motion:no-preference){.slide.on>*{animation:up .5s cubic-bezier(.2,.8,.2,1) both} .slide.on>*:nth-child(2){animation-delay:.07s} .slide.on>*:nth-child(3){animation-delay:.14s} .slide.on>*:nth-child(4){animation-delay:.21s}}
@keyframes up{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
@media print{body{overflow:visible;background:#fff} .stage{position:static;transform:none;width:1920px;height:auto} .slide{display:flex!important;position:relative;height:1080px;page-break-after:always;break-after:page} .slide:last-child{page-break-after:auto;break-after:auto} .slide.on>*{animation:none!important} .nav{display:none}}
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
PROOF=[("54","releases, every one merged green"),("17,450","verifiable blocks · 47 packs"),("6","offline single-file apps"),("64","Louisiana parish dashboards"),("0","WCAG-tagged violations (45 views)"),("50","states: curriculum + compliance")]
ALLOC=[("Cognition.X platform & AI learning infrastructure","$1.20M","24%"),("Robotics simulation & immersive-content studio","$1.00M","20%"),("Robotics lab pilots & partner equipment","$850K","17%"),("Curriculum, SMEs & credential design","$600K","12%"),("Enterprise delivery & customer success","$450K","9%"),("Sales, partnerships & market development","$300K","6%"),("Mission governance, accessibility & public benefit","$250K","5%"),("Legal, security, compliance & operations reserve","$350K","7%")]
MILES=[("0–3 mo","Charter, mission-rights framework, competency framework, first three course blueprints · 3 LOIs"),("3–6 mo","Cognition.X Core; AI-readiness, governance and robot-operator simulations · first paid pilot; two lab/OEM partnerships"),("6–12 mo","Three flagship pathways; xAPI/LRS; simulation analytics · 5–10 paid pilots; $150K–$300K contracted"),("12–18 mo","Cybersecurity and robotics-maintenance tracks; partner-lab model · 10–20 customers; $500K–$1M run-rate"),("18–24 mo","Enterprise integrations, governance layer, skills passport · $1M–$2M ARR; Series A readiness")]

def pn(i,n): return f'<div class="pn"><span>AGI FUTURE FOUNDATION PBC · COGNITION.X · ROBOTICS.X</span><span>{i} / {n}</span></div>'
def strip(): return '<p class="striplab">What exists today — open the repository and click</p><div class="strip">'+''.join(f'<div><b>{E(a)}</b><span>{E(b)}</span></div>' for a,b in PROOF)+'</div>'
def alloc_table():
    return '<table><thead><tr><th>Use of proceeds — $5.0M, 18–24 months</th><th class="r">Amount</th><th class="r">Share</th></tr></thead><tbody>'+''.join(f'<tr><td>{E(a)}</td><td class="r"><b>{E(b)}</b></td><td class="r">{E(c)}</td></tr>' for a,b,c in ALLOC)+'<tr class="total"><td>Total</td><td class="r">$5.0M</td><td class="r">100%</td></tr></tbody></table>'
def miles():
    return '<div class="lines" style="margin-top:6px">'+''.join(f'<div><b>{E(a)}</b><span>{E(b)}</span></div>' for a,b in MILES)+'</div>'
TERMS=[("Total program capitalization","$5.0M blended: $2.5M AGI Corp equity (this instrument) · $1.5–2.0M robotics program capital (grants, leases, strategic) · $0.5–1.5M non-dilutive grants and customer-funded pilots"),
 ("Instrument — standard form","Y Combinator post-money SAFE, valuation-cap only (no discount, no MFN), one form for every investor in the round; cap set with counsel from a fully diluted model. Issuer: AGI Corp, a Delaware C-corporation"),
 ("Side letter","YC pro rata side letter for investors at or above $250K; information rights for the same group; no other special rights"),
 ("At the priced round","NVCA model documents: 1× non-participating preferred · option pool 10–15% pre-money · founder vesting 4 years / 1-year cliff · one investor seat plus an independent director policy · protective provisions limited to major items"),
 ("Securities compliance","Regulation D Rule 506(b) — accredited investors, no general solicitation; Form D within 15 days of first sale; state notice filings; QSBS analysis for a C-corp issuer"),
 ("Mission rights & reporting","Foundation reserved matters limited to public-benefit purpose, safety-policy removal, sale of mission-critical IP and dissolution; quarterly investor report; annual public-benefit report (8 Del. C. §366)")]
def stack():
    return '<p class="striplab" style="margin-top:20px">Blended capital stack — $5.0M program, $2.5M in this instrument</p><div class="stack"><div style="flex:2.5;background:var(--gold)">$2.5M · AGI Corp equity (post-money SAFE)</div><div style="flex:1.75;background:var(--teal)">$1.5–2.0M · robotics program capital</div><div style="flex:1;background:#3D5A73">$0.5–1.5M · grants + customer-funded pilots</div></div><p class="fine">Program capital and grants sit in separate legal entities and capital pools; they do not dilute SAFE holders and SAFE proceeds are not pledged to them.</p>'
def prot():
    P=[("Your protections","Pro rata and information rights at or above $250K; a single SAFE form so no investor holds terms another cannot see; conversion at the cap or the priced-round price, whichever is lower for you."),
       ("Use-of-proceeds discipline","Eight budget lines, board-approved; drawdown by milestone; customer-funded pilots and grants extend runway without dilution; robotics hardware financed off the equity line."),
       ("What you will hear from us","Quarterly investor report (cash, burn, pilots, credentials completed on an unmodified release); annual public-benefit report under 8 Del. C. §366; every product claim traceable to a merged release.")]
    return '<div class="prot">'+''.join(f'<div><b>{E(a)}</b>{E(b)}</div>' for a,b in P)+'</div>'
def terms(): return '<div class="terms">'+''.join(f'<div><b>{E(a)}</b><span>{E(b)}</span></div>' for a,b in TERMS)+'</div>'
RISK="Risk management: AGI operates in early-stage, regulated and technically evolving markets — product execution, AI-model reliability, adoption, enterprise sales cycles, privacy and security, robotics safety, capital availability and mission-governance complexity. Mitigated through a phased roadmap, simulation-first robotics, human oversight, standards-based interoperability, separate legal entities and capital pools, rigorous data controls, customer-funded pilots and board-level governance. Not an offer to sell securities; any offering is made only through definitive documents under an available exemption. Structure and terms are proposals until counsel has papered them."

# ---------- the three pages ----------
P1=f'''<section class="slide on" id="problem"><p class="kicker">1 · The problem</p>
<h2>AI and robotics are advancing faster than workforce readiness and institutional governance.</h2>
<div class="cols">
 <div class="col"><b>Training is completion-based</b><p>Lessons, videos and quizzes measure attendance. A certificate says you sat in the room; nobody can check what a person can actually do.</p></div>
 <div class="col"><b>Robotics is hard to operationalize</b><p>Integration complexity, safety requirements and a shortage of operators and technicians hold adoption back more than the hardware does.</p></div>
 <div class="col"><b>Enterprises need governed adoption</b><p>Before an agent or a robot enters a high-consequence setting, institutions need human oversight, auditability, measurable skills and interoperable evidence.</p></div>
</div>
<div class="box" style="margin-top:34px;border-left-color:var(--teal);font-size:23px"><h3 style="font-size:30px">A certificate says you sat in the room. A record says what you did.</h3><p>The readiness layer is the training, simulation, governance and evidence infrastructure that lets an institution adopt intelligent machines and prove its people can run them.</p></div>
<div style="margin-top:auto">{strip()}</div>{pn(1,3)}</section>'''
P2=f'''<section class="slide" id="solution"><p class="kicker">2 · The solution</p>
<h2>Cognition.X + Robotics.X turn learning into verified capability.</h2>
<div class="loop">'''+''.join(f'<div><i>{i+1}</i><b>{E(a)}</b>{E(b)}</div>' for i,(a,b) in enumerate([("Understand","role-based concepts and policy context"),("Practice","scenario role-play and guided decisions"),("Simulate","digital twin, XR or browser environment"),("Perform","supervised task or workplace evidence"),("Verify","human-reviewed rubric, credential, audit record"),("Improve","remediation and instructor insight")]))+f'''</div>
<div class="split">
 <div class="lines mid">
  <div><b>Cognition.X</b><span>AI-native education and workforce platform — role-based learning, scenario practice, skills verification, governance workflows. Shipped today: the six-stage loop as running code, signed portable credentials, 47 packs, six offline apps.</span></div>
  <div><b>Robotics.X</b><span>Simulation-to-operation environment for embodied AI — operator readiness, human-robot collaboration, maintenance, field operations. Today: the Robotics OS curriculum and the trades simulation studio; the immersive layer is what the raise builds.</span></div>
  <div><b>Mission layer</b><span>AGI Future Foundation PBC protects safety, accessibility, accountability and equitable access through narrow mission rights and public-benefit reporting — the credibility institutions require.</span></div>
  <div><b>Commercial model</b><span>Enterprise licences, paid pilots, learner seats, simulation-module licences, implementation, train-the-trainer, integrations.</span></div>
 </div>
 <div class="shots2"><figure class="shot"><img src="shot-loop.png" alt=""></figure><figure class="shot"><img src="shot-trades.png" alt=""></figure></div>
</div>{pn(2,3)}</section>'''
P3=f'''<section class="slide" id="ask"><p class="kicker">3 · The ask</p>
<h2>Raising $5.0M to build trusted AI and robotics readiness infrastructure.</h2>
<div class="ask">
 <div>{alloc_table()}<p class="striplab" style="margin-top:14px">Milestones</p>{miles().replace('class="lines"','class="lines tight"')}</div>
 <div><div class="box"><h3>The round</h3>{terms()}</div>
  <div class="box" style="margin-top:12px;border-left-color:var(--teal)"><h3>Call to action</h3><p><b>Request the data room</b> — brief, capital-structure and risk memo, and the repository behind every product claim. <br>agifuturefoundation.org · github.com/AGIFutureFoundation/Cognition.X</p></div></div>
</div>
<p class="fine">{E(RISK)}</p>{pn(3,3)}</section>'''
deck=f'''<title>AGI Future Foundation Investor Deck</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>{CSS}</style><div class="stage">{P1}{P2}{P3}</div>
<div class="nav"><button id="prev" aria-label="Previous slide">◀</button><button id="next" aria-label="Next slide">▶</button></div><script>{JS}</script>'''
open('deck3.html','w').write(deck)
open('preview3.html','w').write('<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0">'+deck+'</body></html>')

# ---------- the video edition (eight slides) ----------
V=[]
V.append(dict(id='v-title', say="AGI Future Foundation. Building the readiness layer for safe AI and robotics adoption. This is the investor pitch, and it ends with the round.",
 html=f'<section class="slide dark" id="v-title"><p class="kicker">AGI Future Foundation PBC · investor pitch · September 2026</p><h1>The readiness <em>layer.</em></h1><p class="sub">Cognition.X and Robotics.X turn learning into verified capability — governed AI, workforce training, simulation and embodied-AI readiness for institutions that need proof, not completion.</p>{pn("","")}</section>'))
V.append(dict(id='v-problem', say="The problem. AI and robotics are advancing faster than workforce readiness and institutional governance. Training is completion-based: a certificate says you sat in the room, and nobody can check what a person can actually do. Robotics is hard to operationalize: integration, safety and a shortage of operators hold adoption back more than the hardware does. And enterprises need governed adoption: human oversight, auditability, measurable skills and interoperable evidence before an agent or a robot enters a high-consequence setting.",
 html=P1.replace('class="slide on"','class="slide"').replace('id="problem"','id="v-problem"').replace(pn(1,3),pn("",""))))
V.append(dict(id='v-proof', say="What exists today is not a plan. Fifty-four releases, every one merged with the build green. Seventeen thousand four hundred and fifty verifiable blocks in forty-seven packs. Six offline single-file apps. Sixty-four Louisiana parish dashboards. Zero WCAG-tagged accessibility violations across forty-five audited views. A curriculum and a compliance checklist for all fifty states. Open the repository and click.",
 html=f'<section class="slide" id="v-proof"><p class="kicker">What exists today</p><h2>Evidence an investor can open and click — before the raise.</h2><div class="split"><div>{strip().replace("margin-top:auto","")}<div class="lines" style="margin-top:26px"><div><b>The loop</b><span>Enrol → flow → witnessed checks → credential at fifty → ECDSA-signed record → offline verification with tamper detection: running code, not a diagram.</span></div><div><b>The stances</b><span>Simulation ≠ certification; nothing leaves the page on its own; access profiles are never diagnoses — enforced by 1,318 tests on every push.</span></div><div><b>The flagship</b><span>Cognition.X Louisiana: 64 parishes, 8 Trade Halls, the Legacy Institute curriculum, the Makers\' Hall.</span></div></div></div><div class="shots2"><figure class="shot"><img src="shot-state.png" alt=""></figure><figure class="shot"><img src="shot-makers.png" alt=""></figure></div></div>{pn("","")}</section>'))
V.append(dict(id='v-solution', say="The solution. Cognition.X and Robotics.X turn learning into verified capability. Every module runs the same six stages: understand, practice, simulate, perform, verify, improve. Cognition.X is the education and workforce platform, and its loop already runs as code with signed portable credentials. Robotics.X is the simulation-to-operation environment for embodied AI; today it is a curriculum and a simulation studio, and the immersive layer is what the raise builds. Above both sits the mission layer: the Foundation protects safety, accessibility and equitable access through narrow mission rights, which is exactly the credibility institutional buyers require.",
 html=P2.replace('id="solution"','id="v-solution"').replace(pn(2,3),pn("",""))))
V.append(dict(id='v-portfolio', say="The commercial engine launches three programs first: A I literacy and agentic workflows, for employers, workforce programs and colleges. Responsible A I and governance, for enterprises and public agencies. And robot operator readiness with simulation, for manufacturers, logistics firms and technical schools. Revenue comes from enterprise licences, paid pilots, learner seats, simulation-module licences, implementation and train-the-trainer programs. Cybersecurity and maintenance tracks follow the first pilots.",
 html=f'<section class="slide" id="v-portfolio"><p class="kicker">The commercial engine</p><h2>Three programs first, chosen for demand and for what is already built.</h2><div class="cols"><div class="col"><b>AI Literacy & Agentic Workflows</b><p>Fastest to prototype; broad employer demand; the foundation for every other track. Buyers: employers, workforce programs, colleges.</p></div><div class="col"><b>Responsible AI & Governance</b><p>The Foundation\'s mission in a course: risk, oversight, auditability, procurement, incident response. Buyers: enterprises, public agencies, universities.</p></div><div class="col"><b>Robot Operator Readiness + Simulation</b><p>The differentiated embodied-AI capability. Buyers: manufacturers, logistics, technical schools, workforce boards.</p></div></div><div class="box" style="margin-top:26px"><h3>Revenue model</h3><p>Annual enterprise licences · paid pilots · learner-seat subscriptions · simulation-module licences · implementation and integrations · train-the-trainer. Then cybersecurity and robotics-maintenance tracks, once the first pilots show which buyer converts.</p></div><figure class="shot" style="margin-top:20px;max-height:300px"><img src="shot-roles.png" alt=""></figure>{pn("","")}</section>'))
V.append(dict(id='v-ask', say="The ask. We are raising five million dollars to build trusted A I and robotics readiness infrastructure over eighteen to twenty-four months. One point two million for the Cognition X platform and A I learning infrastructure. One million for the robotics simulation and immersive-content studio. Eight hundred and fifty thousand for lab pilots and partner equipment. Six hundred thousand for curriculum, subject-matter experts and credential design. Four hundred and fifty thousand for enterprise delivery. Three hundred thousand for sales and partnerships. Two hundred and fifty thousand for mission governance, accessibility and public benefit. And three hundred and fifty thousand in legal, security, compliance and reserve.",
 html=f'<section class="slide" id="v-ask"><p class="kicker">The ask</p><h2>Raising $5.0M — an 18–24 month integrated launch plan.</h2><div class="split" style="grid-template-columns:1fr 1fr"><div>{alloc_table()}</div><div><p class="striplab">Milestones</p>{miles()}</div></div>{pn("","")}</section>'))
V.append(dict(id='v-round', say="The round, on standard forms. Five million dollars of total program capitalization as a blended stack: two and a half million of AGI Corp equity through this instrument; one and a half to two million in robotics program capital from grants, leases and strategic partners; and half a million to one and a half million in non-dilutive grants and customer-funded pilots. The instrument is the Y Combinator post-money SAFE, valuation-cap only — no discount, no most-favoured-nation clause — one form for every investor, with the cap set by counsel from a fully diluted model. The issuer is AGI Corp, a Delaware C corporation. Investors at or above two hundred and fifty thousand dollars receive the standard pro rata side letter and information rights. At the priced round, N V C A model documents: one times non-participating preferred, a ten to fifteen percent option pool, four-year founder vesting with a one-year cliff, one investor seat and an independent director. The offering runs under Regulation D, Rule five oh six b, to accredited investors, with Form D filed within fifteen days and state notices made. The Foundation holds narrow mission rights, not commercial control. Quarterly investor reports and an annual public-benefit report. This is not an offer to sell securities; terms are proposals until counsel has papered them.",
 html=f'<section class="slide" id="v-round"><p class="kicker">Round details</p><h2>What you own, what your money funds, who decides.</h2><div class="box">{terms()}</div>{stack()}{prot()}<p class="fine" style="margin-top:auto">{E(RISK)}</p>{pn("","")}</section>'))
V.append(dict(id='v-cta', say="The call to action. Request the data room: the investor brief, the capital-structure and risk memo, and the repository that backs every product claim. Join the first cohort as a design partner, or sponsor a Trade Hall or a robotics lab. Find us at A G I future foundation dot org, and the code at github dot com slash A G I Future Foundation slash Cognition dot X. AGI Future Foundation. The readiness layer.",
 html=f'<section class="slide dark" id="v-cta"><p class="kicker">Call to action</p><h1>Back the <em>readiness layer.</em></h1><div class="cta"><div><b>Investors</b>Request the data room — the brief, the capital-structure and risk memo, and the round documents when counsel has papered them.</div><div><b>Design partners</b>Join the first cohort: one hall, one class, completing credentials on an unmodified release — the v1.0 gate.</div><div><b>Sponsors</b>Fund a Trade Hall, a robotics learning lab, or the fellowship — separate, ring-fenced, reported.</div></div><p class="sub" style="margin-top:36px">agifuturefoundation.org · github.com/AGIFutureFoundation/Cognition.X</p><p class="fine" style="margin-top:22px">Not an offer to sell securities. Any offering is made only through definitive documents under an available exemption; every structure here is a proposal until counsel has papered it.</p>{pn("","")}</section>'))
vid=f'''<title>AGI Future Foundation Investor Pitch</title><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap"><style>{CSS}</style><div class="stage">{''.join(v['html'] for v in V)}</div><div class="nav"><button id="prev">◀</button><button id="next">▶</button></div><script>{JS}</script>'''
open('preview.html','w').write('<!doctype html><html><head><meta charset="utf-8"></head><body style="margin:0">'+vid+'</body></html>')
json.dump([{'id':v['id'],'say':v['say']} for v in V], open('narration.json','w'), ensure_ascii=False, indent=1)
print('deck3 3 pages; video', len(V), 'slides; words', sum(len(v['say'].split()) for v in V))
