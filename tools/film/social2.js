const { run, app } = require('./film');
run('social-2-the-flow-zone', [
 {card:{kicker:'Cognition.X', title:'Not a feed. <b>A flow system.</b>', sub:'Every block arrives sized to the learner\'s channel — and the intelligence lives on the device.', lines:['flow-state engine','20 access modules','24-agent swarms'], theme:'teal'},
  say:"Most learning platforms are feeds. Cognition X is a flow system."},
 {url:app('flow-hub','#'), chapter:'Flow Hub', caption:'Pick a track, say where your skill is today, and enter the flow.',
  say:"A flow session. Pick a pack and a track, say where your skill is today, and enter the flow. Each block arrives sized to your channel.",
  steps:[{click:'.navbtn[data-view="flow"]', dwell:900},{select:'#fs-pack', value:{label:'Music : Creation to Industry'}, dwell:900},{click:'#fs-start', dwell:1800}]},
 {url:app('flow-hub','#'), chapter:'The engine', caption:'Breezed it · in the flow · struggled — the band moves with you.',
  say:"Breezed it, in the flow, or struggled. The engine raises the band, holds it, or eases off — and calls the break on your own cadence, not a timer's.",
  steps:[{click:'.navbtn[data-view="flow"]', dwell:600},{click:'#fs-start', dwell:1000},{click:'#oc-flow', dwell:1300},{click:'#oc-breezed', dwell:1300},{click:'#oc-struggled', dwell:1300},{click:'#oc-flow', dwell:1200}]},
 {url:app('louisiana','#/roles'), chapter:'Dashboard swarms', caption:'Agents propose; the person disposes.',
  say:"Every dashboard runs a crew of agents on a shared blackboard. Each one computes a priority and a concrete call from real state — the ledger, the witness queue, the readiness boards — and arbitration surfaces one call as the swarm's. Agents propose. The person disposes.",
  steps:[{click:'#rolechips [data-role="teacher"]', dwell:1500},{drift:700, ms:2400},{drift:400, ms:1500}]},
 {url:app('louisiana','#/roles'), chapter:'Access modules', caption:'Twenty learner-type supports — chosen, never diagnosed.',
  say:"Twenty access modules tune the cadence, the step and the check format for different kinds of minds. They are chosen supports, never diagnoses, and the platform will not let them be used as one.",
  steps:[{click:'#rolechips [data-role="student"]', dwell:1400},{drift:900, ms:2600}]},
 {card:{kicker:'Cognition.X', title:'The <b>Flow Zone.</b>', sub:'On the device. Never phoning home. github.com/AGIFutureFoundation/Cognition.X', lines:['open source','offline-first'], theme:'teal'},
  say:"The Flow Zone. On the device, never phoning home. Cognition X."},
]).then(()=>console.log('DONE 2')).catch(e=>{console.error(e);process.exit(1);});
