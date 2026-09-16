# XR and the "metaverse" — the studio in space

Since v0.69.0 every scenario in the Simulation Studio can be opened as a
room: **Open in 3D / VR** in the brief, on any decision, or in the debrief.

- **What you see.** The floor, the studio law on a sign, one station per
  decision point in an arc around you, and the current decision's three
  options as slabs above its station. Pick a slab to choose; the studio's
  own buttons keep working beside the room and remain the accessible path.
- **How it reaches a headset or a phone.** WebXR, the browser's own
  standard: on Quest Browser, Wolvic or Chrome with an OpenXR runtime the
  page offers **Enter VR**; on a WebXR phone it offers **Enter AR**. In any
  other browser the same room is a *magic window* — drag or use the arrow
  keys to look around, click a slab. Nothing is loaded from anywhere; no
  SDK, no library, no platform account.
- **How it reaches other worlds.** *Export scene (glTF)* writes a glTF 2.0
  file that Blender, Unity, Unreal, Godot, Hubs and any OpenXR world
  import. Node names and `extras` carry the scenario and step ids, never
  a score. The scene document itself is `cx-xrscene/1` (metres, +Y up).
- **What it keeps.** Nothing. The device's position is read to draw each
  frame and dropped; no hand, eye or face tracking is requested; the
  privacy notice says so and the register holds it (PL-21).
- **What it proves.** Nothing. A scene is practice, never a witnessed
  check and never a credential; the law is on the sign in the room.

The full review — what the "metaverse fabric" can and cannot mean for a
consent-first, offline platform used by minors, the decisions taken and
what is deliberately not built — is
[`docs/XR_REVIEW.md`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/docs/XR_REVIEW.md).
