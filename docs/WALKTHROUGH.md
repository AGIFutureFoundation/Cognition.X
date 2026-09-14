# Cognition.X — a walkthrough for investors

*Learning you can verify.* Cognition.X breaks education into blocks a person can prove, runs them through a flow system that lives on the device, and hands the learner a record anyone can check. Louisiana is where it is built out first — sixty-four parishes, eight Trade Halls, and a leadership curriculum in the Willie L. Brown Jr. Institute model.

AGI Future Foundation · open source (MIT code, CC BY 4.0 curriculum) · v0.49.0 · https://github.com/AGIFutureFoundation/Cognition.X

The published page: this document, designed — see the artifact link in the release notes. Every number below is checked against the dataset by `tests/test_platform.py` on every push.

## The unit is a block
`CX-UNIT-0001`

Every learning platform has a unit. Most choose the lesson, the video, the course — containers, not proof. Cognition.X chose the smallest thing that can be verified: a block. One capability, at one grade band, described in a sentence, and proven by a transfer check on real material. Here is one, exactly as it sits in the dataset:

| Field | Value |
|---|---|
| Block id | CX-MUSICIND-0054 |
| Pack | Music : Creation to Industry |
| Track | The song: writing and arranging |
| Code | SW-4 |
| Band | 9–10 |
| Level | Practitioner |
| Credential | Songwriter |
| Theme | Where songs come from |
| Description | The hook, the title and the line you cannot shake: catching an idea and keeping it before it leaves. — at 9–10 |
| Transfer check | Collect twenty song ideas in a week — titles, lines, hummed phrases — and develop one into a hook with a recorded eight bars. |

*Row CX-MUSICIND-0054 of `data/blocks.csv`, unedited. Fifty of these make a track; ten themes across five bands; one credential at the end.*

## The manifest
`CX-MANIFEST-0002`

Blocks roll up into themes, themes into tracks, tracks into credentials, credentials into packs. The whole system is one CSV with permanent ids, one manifest, one validator — and it regenerates deterministically from authored specs on every push. These are the current numbers, and the tests fail if the documentation drifts from them.

| | |
|---:|---|
| **17,450** | blocks — each one capability, one grade band, one transfer check |
| **47** | packs, from K–12 mathematics to the music industry |
| **225** | tracks, each a 50-block ladder to one named credential |
| **64** | Louisiana parishes with their own dashboard |
| **8** | Trade Halls running the Network OS |
| **222** | union and trade entries across six regions on two coasts |
| **50** | states with a localized curriculum from one blueprint |
| **6** | offline single-file apps, rebuilt byte-for-byte in CI |

## The learning loop
`CX-LOOP-0003`

Here is what a learner actually goes through. It is a loop, not a feed, and every stage is executable code the Platform app runs on labeled demo data in front of you.

1. **A block is chosen** — The flow engine looks at where the learner's channel sits — warming up, in flow, cruising, overloaded — and picks the next block at a step it can hold. One capability, one band.
2. **The work happens on real material** — A block's transfer check is never a quiz. It is a thing done in the world: twenty song ideas in a week, a roux to three named colors, a rigging plot with every point's weight.
3. **The learner reports the felt difficulty** — Breezed it, in the flow, or struggled. The engine raises, holds or eases the band; on the learner's own cadence it calls the break.
4. **An assessor witnesses the check** — Three lines: real material · independent at band · would transfer. Confirm, or an honest not-yet with no credit. Witnessed checks are what the records office signs.
5. **At fifty checks the credential fires** — Not before. The ledger awards it automatically, by name — Songwriter, Louisiana Cook, Working Draftsperson — and tells every dashboard at once.
6. **The record leaves in the learner's hand** — The hall's Records Office signs a portable cx-credential/1 file with its own ECDSA key. Anyone can verify it offline; a tampered copy fails; a revoked one says so.

## The automated flow system
`CX-FLOW-0004`

The part investors usually call the AI is, in Cognition.X, a set of automations that live inside the page and never phone home. We say that plainly because it is the product's strongest property, not a limitation.

The flow-state engine keeps a per-learner channel — the felt difficulty of the last dozen moves — and steers the next block into it: shrink the step under overload, stretch it when cruising, call the break on the learner's own cadence. Twenty access modules tune that cadence, the step bias and the check format for different kinds of minds. They are chosen supports, never diagnoses, and the platform will not let them be used as one.

The agent swarms sit behind every one of the seven role dashboards — student, teacher, assessor, parent, homeschool, parish admin, state admin. Twenty-four agents in all, on a shared blackboard: each computes a priority and a concrete call from the browser's real state — the ledger, the witness queue, readiness boards, budgets, missions — and priority arbitration surfaces one call as the swarm's. Every agent's own reasoning stays listed beneath it. Agents propose; the person disposes. A voice model speaks the call on demand, on the device.

The Network OS runs the Trade Halls the same way: eight automations on a twenty-second pulse — Flow Keeper, Break Caller, Step Tuner, Credential Clerk, Cohort Watch, Readiness Sentinel, Teacher Relief, Network Sync — and every one of them opens into the exact thresholds and the per-learner rows it computed from. Teachers, not just learners, are kept in the channel: the Class flow board reads the teacher's own state and proposes relief.

With consent, the same loop teaches machines: every completed block can be exported as a CX-Trace — how a human did it, step by step — so agents and robots learn from a curriculum that was written for people. Nothing is exported unless someone chooses to.

## Louisiana, the flagship
`CX-LAOS-0005`

Cognition.X Louisiana is the whole platform modelled onto one state's real structure — sixty-four parishes, eight regions, eight Trade Halls — with an independent dashboard for every parish. Each one carries its seat, its school systems, its anchor industries, its narrative world, and a module plan the rules engine earned from its own economy: Plaquemines gets energy, transport and the culinary trade because of LNG, the river port and the seafood; St. Landry gets the music and culinary trades because Clifton Chenier, Paul Prudhomme and Tony Chachere came from there, and the plan says so in words.

The state's own 500-block edition — river, coast, energy corridor, ports, agriculture, the Louisiana table, music, heritage languages, krewes and festivals, storm memory — sits in every parish's core spine. Every parish also gets a five-rung mission module generated from its narrative world, and a program export a school board can print.

The adopted rollout is two years and two waves: thirty-three parishes carrying about 88% of the population in 2026–27, all sixty-four by 2027–28, with a launch-team curriculum, a readiness board and a deterministic budget sketch for each. Rural parishes get offline-evidence wording; paper logs count.

The newest layer is the Makers' Hall: music from the first note to the industry's every role, the professional kitchen from knife to ownership, and the art and craft trades from seeing to the working studio — each drawn as a pathway whose five stages are the five tracks of its pack, with 154 job titles, 42 schools and programs, and 63 makers from the public record spread across all eight regions so that a learner in any parish can claim one. Naming is not endorsement, and the living practitioner two streets over is left for the parish to name.

## The flagship curriculum: the Legacy Institute
`CX-LEGACY-0006`

The civic cornerstone of every Cognition.X edition is a leadership program built on the public record and published principles of the Willie L. Brown Jr. Institute of Politics and Public Service. Twelve principles, each traced to its source and taught as craft. Five strands — public service and civic leadership; democracy, law and rights; economic development and opportunity; community health and wellbeing; equity, inclusion and access — across five eras from K–2 to the last years of high school: 125 courses, a ten-module teaching method, bridge projects at grades 5 and 8, five standards, a graduation seal, and the Fellowship pattern of paid public-agency placements at the top of the ladder.

> “Public service is the most noble of professions. It provides the opportunity to give back to your community, to ensure the next generation has opportunities to lead better lives.” — Willie L. Brown Jr., Institute vision statement

For educators this is the training track: the Leadership Ladder is what a teacher or a parish administrator works through to run the program, and the whole curriculum is canonical data — data/wlb/institute.json — rendered in the Louisiana and States apps and localizable through one template to any state or country.

We carry the Institute's own words as our disclaimer, verbatim, on every page that names it: “This track is a proposal built from the Institute's public mission and the Willie L. Brown Jr. Fellowship Program at San Francisco State University. It is not affiliated with, endorsed by, or reviewed by the Institute, SF State, or Mayor Brown; the "Willie Brown Foundation" name in the brief refers to this Institute. A named track would be offered under a partnership agreement and the Institute's review of every course.” A partnership is the opportunity; we have not claimed it.

## Trades, halls and SmartCiti.X
`CX-TRADES-0007`

The Trades Network is the same block model pointed at work: 37 trade families across six regions on two coasts — San Francisco, Oakland, New Orleans, Baton Rouge, Houston, Los Angeles — 222 entries in all, each naming the international union, a training simulation localized to a real site, a classroom hook into math, science, ELA or civics, and the pack behind it. Never a local number: the regional council is always the front door.

The classroom is flipped around the jobsite — quests, guilds, honest points; Explorer, Builder, Practitioner, Lead — and nine control disciplines run under the studio law: the rigging plot with every point's weight and the show-stop authority named, the banquet line on the 200-cover clock, the load-in. This is the curriculum engine behind SmartCiti.X, the VR/AR training center for the trades and unions: the scenarios a headset renders are these simulations, and the record a trainee walks out with is a Cognition.X credential that says exactly what was witnessed. Simulation is not certification, and every card says so.

## Records people can carry
`CX-RECORDS-0008`

A hall's Records Office is a keypair in the browser — ECDSA P-256, WebCrypto — that signs ledger-earned credentials into portable cx-credential/1 files carrying a record id, the dataset version, and an honest note of what was and was not witnessed. Verification is offline and graded four ways: invalid; valid but from an unknown key; signed by trusted office “X” by name; or ⊘ revoked, against a signed cx-revocation/1 list. Halls exchange their trust lists as cx-trustlist/1 files, second-hand entries marked until confirmed out of band.

The design principle is the one banks eventually arrived at: the signature proves integrity and key possession; identity is confirmed by people. The path to W3C Verifiable Credentials and Open Badges 3.0 is an envelope change, already on the roadmap.

## From one state to fifty, and to any country
`CX-STATEOS-0009`

The Louisiana build is a pattern, not a one-off. The States OS blueprint — 250 blocks — localizes for all fifty states from a fact base of each one's geography, economy and civic structure, with the Institute Model rendered in every capital; the States app is a tile cartogram you can click. The Institute localizer takes the same template to any country. Three legacy-track localizations (Louisiana, California, Texas) already exist; adding a state is a data file, not a rebuild.

## Built to be trusted
`CX-BUILD-0010`

Everything here ships as six single HTML files that open from a USB stick. There is no server, no account, no telemetry: nothing leaves a page on its own, and export boxes are the only exits. A fresh clone plus Python 3 regenerates the entire platform byte-for-byte, and CI proves it on every push — every pack from its spec, every fact base from its source, every app from its template — alongside 452 mechanical checks on the stances above and 89 browser assertions that drive the working models for real. The 149-view Education OS, the first app in the lineage, boots and renders under a generated shell and a recovered design system.

Licensing is dual by design: MIT for the code, CC BY 4.0 for the curriculum. A school district can adopt it without asking; a partner can build on it without fear.

## What we do not claim
`CX-STANCE-0011`

Investors are used to decks that round up. This platform is built around not doing that, and it is the reason a school board or a union hall can trust it:

- **Simulation ≠ certification.** Every training sim says so; the union hall certifies, the platform proves practice.
- **No union local or chapter numbers, ever.** The regional council is the front door.
- **Access profiles are chosen supports, never diagnoses.** The code and the tests hold that line.
- **Nothing leaves a page on its own.** Records live in the browser; export is a deliberate act; evidence export is consent-gated and aggregate-only.
- **A signature proves integrity and key possession — not identity.** Identity is confirmed by people, out of band.
- **Named people appear through the public record only.** Naming is not endorsement; living local practitioners are the community's to name.
- **Block ids are never reused or renumbered.** Supersede, never rewrite.
- **Every number in every document must match the code,** and CI fails when it does not.

## Where it stands, and what comes next
`CX-NEXT-0012`

Version 0.49.0. Forty-nine releases in, every one merged with CI green; the roadmap's foundation and data phases are complete, the platform phase nearly so, deployment well underway. The remaining road to v1.0 is operational, not code, and the roadmap states the gate plainly: v1.0 is cut when a named external cohort — one hall, one class — has completed credentials on an instance and holds verifiable records.

That is what the next stage is for: a first parish cohort and its assessor network; the curriculum review board seated and working the evidence loop; the first named Trade Hall running the Network OS with SmartCiti.X; the Institute partnership pursued on the Institute's terms; the credential envelope aligned to the W3C standard so the records interoperate beyond our own halls. The software to do all of it exists today, in one repository, and you can open every claim in this document and click it.
