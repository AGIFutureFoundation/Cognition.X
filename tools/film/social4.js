const { run, app } = require('./film');
run('social-4-proof-not-attendance', [
 {card:{kicker:'Cognition.X', title:'Proof, <b>not attendance.</b>', sub:'A certificate says you sat in the room. A record says what you did — and anyone can check it.', lines:['credential at 50 checks','signed records','verified offline']},
  say:"A certificate says you sat in the room. A record says what you did. Watch the whole loop run."},
 {url:app('platform','#/loop'), chapter:'Run the loop', caption:'A demo learner enrolls on a real track.',
  say:"A demo learner enrolls on a real track from the dataset. Each check moves the channel, and the automations answer in real time.",
  steps:[{click:'#s1go', dwell:1200},{click:'#s2p', dwell:900},{click:'#s2p', dwell:900},{click:'#s2s', dwell:900},{click:'#s2p', dwell:1200}]},
 {url:app('platform','#/loop'), chapter:'Witnessed checks', caption:'Confirm — or an honest not-yet with no credit. At exactly fifty, the credential fires.',
  say:"An assessor witnesses the check: confirm, or an honest not-yet with no credit. At exactly fifty checks the credential fires, by name.",
  steps:[{click:'#s1go', dwell:500},{click:'#s2p', dwell:400},{click:'#s2p', dwell:400},{click:'#s2p', dwell:600},{click:'#s3c', dwell:900},{click:'#s3c', dwell:900},{click:'#s3c', dwell:1600}]},
 {url:app('platform','#/loop'), chapter:'The Records Office', caption:'Keys generated in the browser — ECDSA P-256 — sign the record.',
  say:"The Records Office generates its own keys in the browser and signs the record. E C D S A, P two fifty-six. A portable file the learner carries.",
  steps:[{click:'#s1go', dwell:400},{click:'#s2p', dwell:300},{click:'#s2p', dwell:300},{click:'#s2p', dwell:400},{click:'#s3c', dwell:400},{click:'#s3c', dwell:400},{click:'#s3c', dwell:600},{click:'#s4go', dwell:2400}]},
 {url:app('platform','#/loop'), chapter:'Verify', caption:'Valid as-is. A tampered copy fails.',
  say:"Verify it: valid. Now verify a tampered copy: it fails. The signature proves the record is unaltered and signed by that key's holder. Identity is confirmed by people — and that is the point.",
  steps:[{click:'#s1go', dwell:400},{click:'#s2p', dwell:300},{click:'#s2p', dwell:300},{click:'#s2p', dwell:400},{click:'#s3c', dwell:400},{click:'#s3c', dwell:400},{click:'#s3c', dwell:600},{click:'#s4go', dwell:1600},{click:'#s5v', dwell:1600},{click:'#s5t', dwell:1600},{click:'#s5tr', dwell:1600}]},
 {card:{kicker:'Cognition.X', title:'Records people <b>can carry.</b>', sub:'Signed by the hall. Verified by anyone. Owned by the learner. github.com/AGIFutureFoundation/Cognition.X', lines:['cx-credential/1','four verification grades','federation between halls']},
  say:"Records people can carry. Signed by the hall, verified by anyone, owned by the learner. Cognition X."},
]).then(()=>console.log('DONE 4')).catch(e=>{console.error(e);process.exit(1);});
