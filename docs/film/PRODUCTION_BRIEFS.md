# Cognition.X — film production briefs

> **v0.50.0:** the kit now narrates (piper, offline). Five feature shorts
> (`tools/film/social1.js` … `social5.js`) and the pitch deck
> (`tools/film/deck/`; the three-page investor deck and its eight-slide
> video in `tools/film/deck3/`) ship with their narration in the scene files; the
> two product films below can be narrated the same way by adding `say`
> to their scenes — the scripts under each film are written for that.

Two short films, each delivered two ways:

1. **The product cut** — recorded from the real apps at 1920×1080 by
   `tools/film/` (Playwright drives the actual dashboards; animated
   title cards; captions; H.264). No generated footage, no credits
   spent, every frame is the software as shipped. Re-render any time
   with `node tools/film/scenes1.js` / `scenes2.js`.
2. **The cinematic cut** — the Higgsfield-ready brief below: narration
   script, shot list with generation prompts, timing, and the assembly
   plan. Generate when the workspace has credits (~40–60 credits per
   film at Kling 3.0 / Seedance rates; the narration is one
   `generate_audio` call per film). Every generated shot is a *dramatized*
   illustration of a real screen or scene; the real screens from the
   product cut are intercut so nothing on screen claims a feature the
   platform does not have.

Ground rules for both cuts (they are the platform's own stances):
- Simulation ≠ certification. A credential says exactly what was
  witnessed.
- Nothing leaves a page on its own; export boxes are the only exits.
- The Willie L. Brown Jr. Institute is referenced through its public
  record and published principles; the film carries the same
  disclaimer the app does. No claim of affiliation or endorsement.
- Named makers appear as public-record examples; no living local
  practitioner is named or depicted.
- SmartCiti.X is presented as the VR/AR training center whose
  *curriculum engine* is the Cognition.X Trades Network and the
  SmartCiti.X : New Orleans Trades pack. The films show Cognition.X's
  simulation tracks and records; they do not depict VR hardware as a
  Cognition.X feature.

---

## Film 1 — *The Flow Zone* (education · Louisiana flagship · leadership for educators)

**Length** 2:40 · **Ratio** 16:9 · **Voice** warm, measured, one narrator
(mid-40s, unhurried; the tone of a documentary about a public school
that works) · **Music** low, rhythmic, brass-and-piano undertone that
rises at the Louisiana chapter and settles for the Institute chapter.

### Narration (read at ~140 wpm)

> **[0:00]** Every skill a person ever learns comes down to one moment:
> can you do it, on real material, when it counts?
> **[0:08]** Cognition.X is built on that moment. Seventeen thousand four
> hundred and fifty blocks. Each one: a single capability, at one grade
> band, proven by a transfer check. Forty-seven packs. Two hundred
> twenty-five tracks. Six applications that run from a single file,
> offline, anywhere.
> **[0:26]** This is the Flow Zone.
> **[0:30]** The flagship is Louisiana. Sixty-four parishes, each with its
> own dashboard — its seat, its industries, its story — and a module
> plan earned by its own economy. Thirty-three parishes in year one.
> All sixty-four by year two.
> **[0:50]** Behind every dashboard, a network operating system: eight
> automations on a live pulse, watching the ledger, calling the breaks,
> awarding the credentials — and every call opens to the rows it came
> from. Nothing is a black box.
> **[1:06]** For every seat at the table — student, teacher, assessor,
> parent, homeschool, parish, state — a dashboard with its own crew of
> agents. Agents propose. The person disposes.
> **[1:20]** The classroom is flipped around the jobsite. Quests, guilds,
> honest points. Explorer, Builder, Practitioner, Lead. The credential
> comes at fifty recorded checks, and a witnessed check is what the
> records office signs. Simulation is not certification — and the
> record says exactly what was seen.
> **[1:42]** For educators, the Legacy Institute: leadership, ethics and
> civic duty taught as craft, built on the public record and published
> principles of the Willie L. Brown Jr. Institute of Politics and
> Public Service. Twelve principles. Five strands across five eras. One
> hundred twenty-five courses. Localizable to any state — or any
> country.
> **[2:06]** And now the culture trades: music from the first note to the
> industry, the Louisiana kitchen, art and craft — each taught through
> makers from the public record, parish by parish.
> **[2:20]** One blueprint. Fifty states. A model for a national and global
> program — open source, offline-first, and honest.
> **[2:32]** Cognition.X. The Flow Zone.

### Shot list

| # | Time | Shot | Source | Higgsfield prompt (16:9, 5 s unless noted) |
|---|---|---|---|---|
| 1 | 0:00 | Cold open: a teenager's hands on a workbench, a brass instrument, a knife on a board, a stylus on a tablet — four quick cuts | generated | `Cinematic close-up, natural window light, a teenage student's hands [tightening a valve on a trumpet / dicing an onion on a scarred cutting board / measuring a board with a steel square]; shallow depth of field; documentary realism; no text` |
| 2 | 0:08 | Title over the platform system map | product cut (Platform app, The Model) | — |
| 3 | 0:14 | Numbers kinetic type: 17,450 · 47 · 225 · 6 | title card | — |
| 4 | 0:26 | "The Flow Zone" title | title card | — |
| 5 | 0:30 | Louisiana: drone over the river bend at dawn → tile map | generated → product cut (`#/state`) | `Aerial drone shot at golden hour over the Mississippi River crescent at New Orleans, container port cranes, barges, low mist, warm light; slow forward push; photoreal; no text` |
| 6 | 0:40 | Parish dashboard, St. Landry: plan, then the makers panel | product cut (`#/parish/st-landry`) | — |
| 7 | 0:50 | Network OS board expanding a section | product cut (`#/regions`) | — |
| 8 | 0:58 | A teacher at a laptop in a real classroom, dashboard reflected | generated (8 s) | `A Black woman teacher in her forties at a classroom desk, laptop open, students working in pairs behind her, afternoon light through blinds, calm and focused; slow dolly-in; photoreal; no readable screen text` |
| 9 | 1:06 | Role chips → Teacher dashboard with the swarm panel | product cut (`#/roles`) | — |
| 10 | 1:20 | Flipped classroom: students at a mock rigging plot / banquet-line drill | generated (8 s) | `High-school students in a trades classroom laying out a stage rigging plot on a whiteboard while another group runs a timed kitchen line, instructor watching with a clipboard; energetic, documentary handheld; no text` |
| 11 | 1:28 | Flow Hub session: enter the flow, Breezed / In the flow / Struggled | product cut (Flow) | — |
| 12 | 1:36 | The 50-check credential firing; Records Office signing | product cut (Platform app, Run the loop) | — |
| 13 | 1:42 | Institute: a slow push on the state capitol at dusk; then the twelve principles | generated → product cut (`#/institute`) | `Slow cinematic push toward the Louisiana State Capitol tower at blue hour, warm windows, live oaks in the foreground; photoreal; no text` |
| 14 | 1:56 | Leadership Ladder table, a strand selected | product cut | — |
| 15 | 2:06 | Makers' Hall pathway map; a stage clicked; figure cards | product cut (`#/makers`) | — |
| 16 | 2:14 | A second line brass band on a Tremé street, a roux darkening in a cast-iron pot, beadwork under a lamp — three cuts | generated | `Brass band second line on a New Orleans street, late afternoon, crowd moving with them, handheld documentary; no faces in close-up; no text` · `Macro of a roux darkening in a black cast-iron pot, wooden spoon stirring, steam; overhead; no text` · `Hands sewing beads onto a Mardi Gras Indian suit panel under a desk lamp, close on the needle, no face; no text` |
| 17 | 2:20 | States app cartogram → a state opens → Institute Model | product cut | — |
| 18 | 2:32 | Closing card | title card | — |

### Assembly
- Narration: one `generate_audio` call (the script above), then split at
  the bracketed timestamps.
- Cut the product-cut MP4 at the chapter marks (they are the hard cuts
  in `out/cognitionx-flow-zone.mp4`) and intercut generated shots at 1,
  5, 8, 10, 13, 16.
- Burn the captions from the product cut only where the narration does
  not carry the same sentence.

---

## Film 2 — *Training that proves itself* (non-profit & corporate · SmartCiti.X)

**Length** 2:10 · **Voice** direct, confident, one narrator (corporate
documentary register, never hype) · **Music** electronic pulse under
industrial texture; drops to near-silence for the Records Office beat.

### Narration

> **[0:00]** Most training ends with a certificate that says you sat in
> the room. Cognition.X ends with a record of what you did.
> **[0:10]** Non-profit practice. Corporate operations. Multilateral work.
> Global health in the field. Each one a pack of eleven hundred blocks
> or more — every block a capability, a level, and a check on real
> material.
> **[0:26]** Author your own. Pack Studio validates the spec and generates
> the blocks through the same pipeline the platform runs in CI. A review
> board, a checklist, a supersede policy. Block ids are never reused.
> **[0:42]** And for the trades: SmartCiti.X — a VR and AR training center
> for the trades and unions. Its curriculum engine is the Cognition.X
> Trades Network: two hundred twenty-two union and trade entries, six
> regions on two coasts, thirty-seven trade families — each with a
> localized training simulation, the classroom hook, and the pack behind
> it.
> **[1:04]** Nine control disciplines under the studio law: the rigging
> plot with every point's weight; the banquet line on the two-hundred-
> cover clock; the load-in with the show-stop authority named. The
> jobsite in the classroom, before the jobsite. Simulation is not
> certification.
> **[1:24]** Districts sign a compact: trades on the transcript.
> **[1:30]** In the hall, the Network OS keeps the sections in flow. The
> assessor witnesses the check — confirm, or an honest not-yet with no
> credit.
> **[1:44]** Then the Records Office signs it: a portable credential, your
> own keys, verifiable offline, tamper-evident, with four grades of
> verification and revocation between halls. Your trades. Your record.
> **[2:00]** Cognition.X, powering SmartCiti.X. Open source, offline-first,
> and it proves itself.

### Shot list

| # | Time | Shot | Source | Higgsfield prompt |
|---|---|---|---|---|
| 1 | 0:00 | A framed certificate on a wall, dust in the light — cut to hands doing the work (welding hood flips down) | generated | `Static shot of a generic framed training certificate on a beige office wall, dust motes in a shaft of light; then hard cut: a welder's hood snapping down, sparks; photoreal; no readable text` |
| 2 | 0:10 | Flow Hub packs grid; Non-Profit / Corporate / Multilateral | product cut | — |
| 3 | 0:18 | A field clinic tent, a boardroom, a city hall — three quick establishing shots | generated | `Documentary establishing shots: a field clinic tent at dawn with health workers preparing supplies / a modern nonprofit boardroom with a whiteboard plan / a municipal council chamber; no faces close-up; no text` |
| 4 | 0:26 | Pack Studio: spec → validated → generated | product cut (Author) | — |
| 5 | 0:42 | SmartCiti.X title over a stylized city map; then a trainee in a VR headset in a warehouse-scale training floor | title card → generated (8 s) | `Wide shot of a bright industrial training hall, a trainee in a VR headset with hand controllers standing on a marked floor, instructors at a monitor wall, safety cones, union banners without legible text; photoreal; slow orbit; no readable text` |
| 6 | 0:52 | Trades Network city maps: click a region, click a site | product cut | — |
| 7 | 1:00 | Roster search "electric", then "musicians" | product cut | — |
| 8 | 1:04 | A stage rigging plot being chalked; a banquet line on the clock; a load-in dock at night | generated | `Overhead of a rigging plot chalked on a black stage floor, point loads marked; then a hotel banquet kitchen line at full speed; then a loading dock at night, cases rolling in; documentary; no text` |
| 9 | 1:12 | Simulations view | product cut | — |
| 10 | 1:24 | Districts compact | product cut | — |
| 11 | 1:30 | Network OS board; Assessor Mode queue | product cut | — |
| 12 | 1:44 | Records Office: create keys, show public key | product cut | — |
| 13 | 1:52 | A hand holding a phone with a verified record — abstract, no readable UI | generated | `Close-up of a hand holding a phone at a job-site gate, a green check mark glowing on an otherwise blank dark screen, morning light; shallow focus; no readable text` |
| 14 | 2:00 | Closing card | title card | — |

### Assembly
As Film 1. The product cut is `out/cognitionx-smartciti.mp4`; its chapter
cuts align to the narration timestamps above within ±2 s.
