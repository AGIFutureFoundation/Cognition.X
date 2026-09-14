const { run, app } = require('./film');
run('social-1-sixty-four-parishes', [
 {card:{kicker:'Cognition.X Louisiana', title:'Sixty-four parishes. <b>One platform.</b>', sub:'Every parish gets its own dashboard — its seat, its industries, its story, and a module plan earned from its own economy.', lines:['64 parishes','8 Trade Halls','offline-first'], theme:'gold'},
  say:"Louisiana has sixty-four parishes. Cognition X gives every one of them its own dashboard."},
 {url:app('louisiana','#/state'), chapter:'The state', caption:'Click any parish and its own dashboard opens.',
  say:"This is the state as a tile map. Click any parish and its dashboard opens: its seat, its school systems, its anchor industries, and its narrative world. The two colors are the rollout waves: thirty-three parishes first, all sixty-four the year after.",
  steps:[{scroll:'#mapbox', dwell:800},{hover:'#mapbox g:nth-of-type(12)', dwell:900},{hover:'#mapbox g:nth-of-type(33)', dwell:900},{hover:'#mapbox g:nth-of-type(50)', dwell:900},{cap:'The state as cells — regions by parish, area by population.', dwell:300},{scroll:'#vormap', dwell:2600}]},
 {url:app('louisiana','#/parish/st-landry'), chapter:'Parish dashboards', caption:'St. Landry: the core spine plus the packs its own economy earned.',
  say:"St. Landry Parish. The core spine, plus the packs its own economy earned — each with the phrase that earned it. Rice and ag-tech bring water, land and climate. The makers who came from here bring the music and the culinary trades.",
  steps:[{drift:600, ms:1800},{scroll:'#pplan', dwell:1400},{drift:500, ms:2200}]},
 {url:app('louisiana','#/parish/st-landry'), chapter:'Makers from this parish', caption:'Clifton Chenier · Paul Prudhomme · Tony Chachere · Marc Savoy — from the public record.',
  say:"Clifton Chenier. Paul Prudhomme. Tony Chachere. Marc Savoy. Examples from the public record, for a kid in Opelousas to claim as their own.",
  steps:[{scroll:'#pmakers', dwell:1200},{drift:300, ms:1500}]},
 {url:app('louisiana','#/regions'), chapter:'The Network OS', caption:'Eight automations on a live pulse — every call drillable to its rows.',
  say:"And behind every parish, the Trade Hall Network O S: eight automations on a live pulse, every call drillable to the rows it came from.",
  steps:[{scroll:'#autoboard', dwell:800},{click:'#autoboard button[data-sec]', dwell:2200}]},
 {card:{kicker:'Cognition.X Louisiana', title:'Open. Offline. <b>Yours.</b>', sub:'Nothing leaves the page on its own. github.com/AGIFutureFoundation/Cognition.X', lines:['open source','v0.49.1']},
  say:"Cognition X Louisiana. Open source, offline first. Nothing leaves the page on its own."},
]).then(()=>console.log('DONE 1')).catch(e=>{console.error(e);process.exit(1);});
