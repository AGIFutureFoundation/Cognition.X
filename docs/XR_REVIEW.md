# Cognition.X in AR, VR and the "metaverse fabric" — the review, and what shipped

> A review of what it can honestly mean to put this platform into
> head-mounted and phone-held space, the constraints that decide it, the
> decisions taken, what v0.69.0 built, and what is deliberately not
> built. Not legal advice; the register (`docs/CONTROL_REGISTER.md`,
> PL-21) carries the control.

## 1. What "the metaverse fabric" can mean here

There is no single metaverse. There are:

- **Runtimes on devices** — OpenXR is the Khronos standard every major
  headset runtime speaks (Meta Quest, Pico, Windows Mixed Reality,
  SteamVR, Apple's visionOS through its own layer); it is a native API,
  not a web one.
- **The web's door into those runtimes** — the W3C **WebXR Device API**,
  implemented by the browser itself: Quest Browser, Wolvic, Chrome on
  Android for AR, Chrome and Edge on desktop with an OpenXR runtime. A
  page asks `navigator.xr` for an `immersive-vr` or `immersive-ar`
  session and draws with WebGL. No SDK, no library, nothing downloaded.
- **Interchange formats** — **glTF 2.0** (Khronos) is what Blender,
  Unity, Unreal, Godot, Mozilla Hubs, three.js, Babylon and the OMI
  group's interoperability work all import; USD is the film-and-Apple
  side of the same need.
- **Platforms** — Horizon Worlds, VRChat, Roblox, Rec Room, Spatial,
  Decentraland and the rest, each with its own account, its own SDK, its
  own servers, its own data terms.

Cognition.X has six standing rules that decide which of these it can
join: every app is one offline file; no third-party script ever loads;
the Content-Security-Policy blocks every network connection; nothing
about a person leaves a page unless a person exports it; learners are
often minors; and a simulation is practice — never a check, never a
credential. Those rules rule the platforms out and the standards in.

## 2. Decisions

| Question | Decision | Why |
|---|---|---|
| Which door into headsets and phones? | **WebXR**, the browser's own API | It is the standard, it needs nothing loaded, it works inside the single file, and where it is absent the page still works. OpenXR is reached *through* the browser, never by a native build of our own. |
| Which engine? | **A small WebGL renderer of our own** (`tools/xr/engine.js`, ~460 lines at v0.70.0), not three.js, Babylon or A-Frame | The CSP forbids loading them; bundling one adds 600 KB to six apps for boxes, quads and text. The scenes are simple by design. |
| Which platform? | **None.** No Horizon, VRChat, Roblox, Spatial or Decentraland integration | Each requires accounts, a closed SDK, a server and data terms we could not hold to the consent-first stance, let alone for minors. |
| What goes into a scene? | **A studio run as a room**: the floor, the studio law on a sign, one station per decision point in an arc around the learner, the current decision's options as slabs above its station | The Simulation Studio is the part of the platform that *is* rehearsal; everything else (ledger, records, evidence) has no honest 3D form. |
| Who scores? | **The studio engine, as before.** The XR engine is a view: it listens to the studio's `cxsim` events and calls `choose()`/`next()` when a slab is selected | One source of truth for the run and the record; the honesty lines are not duplicated into a second engine. |
| What about people without a headset, or who cannot use one? | **The magic window**: the same scene drawn in the page, orbit by drag or arrow keys, click a slab — and the studio's HTML buttons keep working beside it, always | WCAG: an immersive session is never the only way; the buttons are the accessible path. |
| What tracking? | **Head/controller pose only, per frame, dropped.** No hand, eye or face tracking is requested; no pose is stored, exported or sent | Minors, the privacy notice, and the register. |
| How does a scene leave, if it must? | **glTF 2.0 export**, geometry embedded, node names and `extras` carrying the scenario and step ids and never a score | The interchange format everything imports. A hall can open its scenario in Blender or Unity, or hand it to any OpenXR world, without us integrating with that world. |
| Camera for AR? | The browser asks the person at that moment; the hosting header allows `xr-spatial-tracking` to the page itself and still denies the camera by policy | An `immersive-ar` session is the browser's own camera use, permitted per session, never granted to a third party. |

## 3. What v0.69.0 built

- **`tools/xr/engine.js` — `CXXR`.** Injected by the shared runtime into
  all six apps after the studio engine. `CXXR.scene(scenario, site,
  plan)` produces a **cx-xrscene/1** document (metres, +Y up).
  `CXXR.gltf(scene)` writes a glTF 2.0 file. `CXXR.attach(controller,
  host, scenario)` draws the room: WebGL magic window; **Enter VR** and
  **Enter AR** appear when `navigator.xr` reports the session is
  supported; controller or gaze `select` picks a slab; pointer click
  picks in the window; arrow keys orbit.
- **The studio offers it everywhere.** `CXSIM.mount` shows *Open in 3D /
  VR* in the brief, on every decision, and in the debrief. Every host
  that mounts the studio — Trades Network, Louisiana (student and teacher
  widgets), States, Flow Hub, Platform, Education OS — has the room with
  no host code changed.
- **A hall's own room (v0.70.0).** *Load your hall's room* opens a glTF 2.0
  or GLB file with embedded buffers — a phone scan exported from any
  scanning app, or a room modelled in Blender — and draws it under the
  stations with its floor set to y = 0 and centred on the learner. The
  page fetches nothing, so a `.gltf` whose buffers are external files is
  refused with the reason; the file stays on the device. *Export scene
  (JSON)* writes the `cx-xrscene/1` document itself.
- **The studio's honesty lists stand in the room (v0.70.0).** Beside the
  law: *Simulated here* and *Practised live, at the bench* from the
  scenario, and the *Under eighteen* hazard line where the scenario
  carries one — signs, never stations, never scored.
- **The honesty lines travel.** The studio law is on the sign in the room;
  the scene document, the glTF `extras` and the panel's own note say a
  scene is practice, never a check, never a credential. Option slabs are
  one colour until chosen; a score is never drawn.
- **Privacy, register, hosting.** The privacy notice's security paragraph
  covers XR sessions; the register gains **PL-21** (met); the hosting
  headers allow `xr-spatial-tracking=(self)`.
- **Tests.** The Python suite holds the engine to no network, no storage,
  no randomness, presence in all six apps, valid scene and glTF output
  (run in node); the browser suite opens the room in Trades Network,
  proves WebGL draws it, mirrors a run step by step through the XR view's
  own `act()`, exports glTF, and confirms the no-WebXR fallback message.

## 4. Trying it

- **Any browser:** open a scenario in the Trades Network (*Simulation
  studio*) or the Louisiana app (student view → *Simulation studio*),
  press **Open in 3D / VR**, drag to look around, click a slab.
- **A headset browser** (Quest Browser, Wolvic, Pico): open the same
  file (copy it to the device or host it per `docs/HOSTING.md`); **Enter
  VR** appears; point and select.
- **A WebXR phone** (Chrome on Android with ARCore): **Enter AR** appears;
  the stations stand on your floor.
- **Another world:** *Export scene (glTF)* and import the file in Blender,
  Unity, Unreal, Godot or Hubs. Names and `extras` tell you which station
  is which decision.

## 5. What is deliberately not built, and what could be next

- **No platform integrations**, for the reasons above. If a district runs
  its own OpenXR world, the glTF export is the handshake.
- **No hand, eye or face tracking**, even where the browser offers it.
  PL-21 says the engine must keep declining them.
- **No avatars, no multi-user rooms, no voice.** A shared room would need
  a server, and this platform has none by design. A hall's shared
  rehearsal is two learners at one bench with one assessor.
- **No 3D content authoring.** Stations are drawn from the scenario's own
  decision points; there is no scene editor, and the specs stay text.
- **Done in v0.70.0** from the earlier list: the room import, the
  youth line and the simulated/live lists as signs.
- **Next, if a hall asks:** placing the stations against the loaded
  room's walls instead of the fixed arc; a QR-style share of the scene
  JSON between two devices in a hall (still a file). Each is a view;
  none changes what a run is.

Not legal advice. A scene is practice.
