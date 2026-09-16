/* Cognition.X Studio in space — the WebXR view of a scenario run (v0.69.0).
 *
 * The Simulation Studio (tools/sim/engine.js) plays a scenario; this file
 * draws the same run as a room: a floor, the studio law on a sign, one
 * station per decision point set in an arc around the learner, and the
 * current decision's options as three slabs above its station. It is a
 * VIEW. Scoring, records and the honesty lines stay in the studio engine;
 * this file only listens to the studio's `cxsim` events and calls back
 * choose()/next() when a slab is selected. The studio's own HTML buttons
 * keep working beside it — they are the accessible path, always.
 *
 * Three ways to be in the room, one code path:
 *   - the magic window: a WebGL canvas in the page, orbit by drag or arrow
 *     keys, click a slab to choose — works in every browser, no headset;
 *   - immersive VR: WebXR `immersive-vr` on a headset browser (Quest, Pico,
 *     Wolvic, Chrome + an OpenXR runtime), controller or gaze `select`;
 *   - immersive AR: WebXR `immersive-ar` on a phone that offers it, the
 *     stations placed on the floor around you.
 *   WebXR is the W3C standard the browser itself implements; no vendor SDK,
 *   no library, nothing loaded from anywhere. When it is absent the magic
 *   window is the whole experience and says so.
 *
 * Interoperability: CXXR.scene() is a cx-xrscene/1 document (metres, +Y up)
 * and CXXR.gltf() turns it into a glTF 2.0 file with the geometry embedded,
 * which Blender, Unity, Unreal, Godot, Hubs, three.js and any OpenXR world
 * can import. Node names and `extras` carry the scenario and step ids and
 * never a score.
 *
 * Privacy: an XR session gives the page the headset's or phone's pose each
 * frame. It is used to draw the frame and dropped. Nothing here is stored,
 * exported or sent; there is no network call and no storage call, and no
 * hand, eye or face tracking is requested. A scene is practice, never a
 * check and never a credential — the studio's law rides on the sign.
 */
(function (global) {
  "use strict";
  const CXXR = { version: "1" };
  const UP = [0, 1, 0];

  /* ---------------- small matrix kit (column-major, like WebGL) */
  const M = {
    ident() { return [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]; },
    mul(a, b) { const o = new Array(16); for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) o[c*4+r] = a[r]*b[c*4] + a[4+r]*b[c*4+1] + a[8+r]*b[c*4+2] + a[12+r]*b[c*4+3]; return o; },
    persp(fovy, aspect, n, f) { const t = 1 / Math.tan(fovy / 2); return [t/aspect,0,0,0, 0,t,0,0, 0,0,(f+n)/(n-f),-1, 0,0,2*f*n/(n-f),0]; },
    lookAt(e, c, u) { const z = norm(sub(e, c)), x = norm(cross(u, z)), y = cross(z, x); return [x[0],y[0],z[0],0, x[1],y[1],z[1],0, x[2],y[2],z[2],0, -dot(x,e),-dot(y,e),-dot(z,e),1]; },
    trs(p, yaw, s) { const c = Math.cos(yaw), si = Math.sin(yaw); return [c*s[0],0,-si*s[0],0, 0,s[1],0,0, si*s[2],0,c*s[2],0, p[0],p[1],p[2],1]; },
    inv(m) { // general 4x4 inverse
      const o = new Array(16), a = m;
      const b00=a[0]*a[5]-a[1]*a[4], b01=a[0]*a[6]-a[2]*a[4], b02=a[0]*a[7]-a[3]*a[4], b03=a[1]*a[6]-a[2]*a[5], b04=a[1]*a[7]-a[3]*a[5], b05=a[2]*a[7]-a[3]*a[6];
      const b06=a[8]*a[13]-a[9]*a[12], b07=a[8]*a[14]-a[10]*a[12], b08=a[8]*a[15]-a[11]*a[12], b09=a[9]*a[14]-a[10]*a[13], b10=a[9]*a[15]-a[11]*a[13], b11=a[10]*a[15]-a[11]*a[14];
      let det = b00*b11 - b01*b10 + b02*b09 + b03*b08 - b04*b07 + b05*b06; if (!det) return M.ident(); det = 1 / det;
      o[0]=(a[5]*b11-a[6]*b10+a[7]*b09)*det; o[1]=(a[2]*b10-a[1]*b11-a[3]*b09)*det; o[2]=(a[13]*b05-a[14]*b04+a[15]*b03)*det; o[3]=(a[10]*b04-a[9]*b05-a[11]*b03)*det;
      o[4]=(a[6]*b08-a[4]*b11-a[7]*b07)*det; o[5]=(a[0]*b11-a[2]*b08+a[3]*b07)*det; o[6]=(a[14]*b02-a[12]*b05-a[15]*b01)*det; o[7]=(a[8]*b05-a[10]*b02+a[11]*b01)*det;
      o[8]=(a[4]*b10-a[5]*b08+a[7]*b06)*det; o[9]=(a[1]*b08-a[0]*b10-a[3]*b06)*det; o[10]=(a[12]*b04-a[13]*b02+a[15]*b00)*det; o[11]=(a[9]*b02-a[8]*b04-a[11]*b00)*det;
      o[12]=(a[5]*b07-a[4]*b09-a[6]*b06)*det; o[13]=(a[0]*b09-a[1]*b07+a[2]*b06)*det; o[14]=(a[13]*b01-a[12]*b03-a[14]*b00)*det; o[15]=(a[8]*b03-a[9]*b01+a[10]*b00)*det;
      return o;
    },
    xf(m, v, w) { return [m[0]*v[0]+m[4]*v[1]+m[8]*v[2]+m[12]*w, m[1]*v[0]+m[5]*v[1]+m[9]*v[2]+m[13]*w, m[2]*v[0]+m[6]*v[1]+m[10]*v[2]+m[14]*w]; }
  };
  function sub(a, b) { return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]; }
  function dot(a, b) { return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]; }
  function cross(a, b) { return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]; }
  function norm(a) { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0]/l, a[1]/l, a[2]/l]; }

  /* ---------------- the scene: cx-xrscene/1 */
  const COL = { floor: [0.16, 0.18, 0.22, 1], station: [0.19, 0.42, 0.55, 1], current: [0.85, 0.64, 0.25, 1], done: [0.33, 0.36, 0.40, 1],
                option: [0.93, 0.93, 0.90, 1], picked: [0.85, 0.64, 0.25, 1], faded: [0.60, 0.60, 0.58, 1], sign: [0.12, 0.13, 0.16, 1], you: [0.85, 0.64, 0.25, 1] };
  function short(s, n) { s = String(s == null ? "" : s); return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, "") + "…" : s; }

  CXXR.scene = function (sc, site, plan) {
    const steps = Array.isArray(plan) && plan.length ? plan : (sc.steps || []);
    const n = steps.length, R = 2.4, arc = Math.min(Math.PI * 1.4, 0.5 * n);
    const nodes = [
      { id: "floor", kind: "floor", name: "Floor", position: [0, -0.02, 0], size: [9, 0.04, 9], color: COL.floor },
      { id: "you", kind: "marker", name: "You (the learner)", position: [0, 0.01, 0], size: [0.5, 0.02, 0.5], color: COL.you },
      { id: "sign", kind: "sign", name: "The studio law", position: [0, 1.9, -3.6], size: [2.6, 0.9, 0.06], color: COL.sign,
        text: (global.CXSIM && global.CXSIM.LAW) || "Simulation ≠ certification." }
    ];
    // v0.70.0: the studio's own honesty lists stand in the room too — what is
    // simulated here, what is practised live at the bench, and the under-18
    // hazard line where the scenario carries one. Signs, never stations.
    if (Array.isArray(sc.simulated) && sc.simulated.length)
      nodes.push({ id: "sign-simulated", kind: "sign", name: "Simulated here", position: [-2.9, 1.5, -2.7], yaw: 0.6, size: [2.0, 0.9, 0.06], color: COL.sign, text: "Simulated here: " + sc.simulated.join(" · ") });
    if (Array.isArray(sc.live) && sc.live.length)
      nodes.push({ id: "sign-live", kind: "sign", name: "Practised live, in the studio", position: [2.9, 1.5, -2.7], yaw: -0.6, size: [2.0, 0.9, 0.06], color: COL.sign, text: "Practised live, at the bench: " + sc.live.join(" · ") });
    if (sc.youth)
      nodes.push({ id: "sign-youth", kind: "sign", name: "Under eighteen", position: [0, 0.95, -3.6], size: [2.6, 0.7, 0.06], color: [0.45, 0.16, 0.12, 1], text: "Under eighteen: " + sc.youth });
    steps.forEach((st, i) => {
      const a = n === 1 ? 0 : -arc / 2 + arc * i / (n - 1);
      const p = [Math.sin(a) * R, 0.55, -Math.cos(a) * R];
      nodes.push({ id: "station-" + i, kind: "station", name: "Decision " + (i + 1) + (st.kind === "complication" ? " (complication)" : ""),
                   position: p, yaw: -a, size: [0.7, 1.1, 0.5], color: COL.station, step: st.id, index: i, text: short(st.prompt, 90) });
    });
    return { format: "cx-xrscene/1", scenario: sc.id, title: sc.title, site: site || sc.site_default || "", units: "metres", up: "+Y",
             law: (global.CXSIM && global.CXSIM.LAW) || "", note: "A scene is practice. It is not a witnessed check and never a credential.", nodes };
  };

  /* ---------------- glTF 2.0 writer: one cube mesh, one node per scene node */
  function cubeGeometry() {
    const P = [], N = [], I = [];
    const faces = [[[0,0,1],[1,0,0],[0,1,0]], [[0,0,-1],[-1,0,0],[0,1,0]], [[1,0,0],[0,0,-1],[0,1,0]], [[-1,0,0],[0,0,1],[0,1,0]], [[0,1,0],[1,0,0],[0,0,-1]], [[0,-1,0],[1,0,0],[0,0,1]]];
    faces.forEach(([nrm, u, v], f) => {
      const c = [nrm[0]*0.5, nrm[1]*0.5, nrm[2]*0.5];
      [[-1,-1],[1,-1],[1,1],[-1,1]].forEach(([su, sv]) => { P.push(c[0]+u[0]*su*0.5+v[0]*sv*0.5, c[1]+u[1]*su*0.5+v[1]*sv*0.5, c[2]+u[2]*su*0.5+v[2]*sv*0.5); N.push(nrm[0], nrm[1], nrm[2]); });
      const b = f * 4; I.push(b, b+1, b+2, b, b+2, b+3);
    });
    return { P: new Float32Array(P), N: new Float32Array(N), I: new Uint16Array(I) };
  }
  function b64(bytes) {
    if (typeof btoa === "function") { let s = ""; for (let i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]); return btoa(s); }
    return Buffer.from(bytes).toString("base64");
  }
  CXXR.gltf = function (scene) {
    const g = cubeGeometry();
    const pb = new Uint8Array(g.P.buffer), nb = new Uint8Array(g.N.buffer), ib = new Uint8Array(g.I.buffer);
    const pad = n => (4 - n % 4) % 4;
    const total = pb.length + pad(pb.length) + nb.length + pad(nb.length) + ib.length + pad(ib.length);
    const buf = new Uint8Array(total); let off = 0;
    const put = a => { buf.set(a, off); const o = off; off += a.length + pad(a.length); return o; };
    const oP = put(pb), oN = put(nb), oI = put(ib);
    const materials = [], matIndex = {};
    const mat = c => { const k = c.join(","); if (!(k in matIndex)) { matIndex[k] = materials.length; materials.push({ name: "cx-" + materials.length, pbrMetallicRoughness: { baseColorFactor: c, metallicFactor: 0, roughnessFactor: 0.9 } }); } return matIndex[k]; };
    const meshes = [], meshIndex = {};
    const meshFor = c => { const m = mat(c); if (!(m in meshIndex)) { meshIndex[m] = meshes.length; meshes.push({ name: "cube-" + m, primitives: [{ attributes: { POSITION: 0, NORMAL: 1 }, indices: 2, material: m }] }); } return meshIndex[m]; };
    const nodes = scene.nodes.map(nd => {
      const yaw = nd.yaw || 0;
      const node = { name: nd.name, translation: nd.position.slice(), scale: nd.size.slice(), mesh: meshFor(nd.color),
                     extras: { cx: { id: nd.id, kind: nd.kind, scenario: scene.scenario, step: nd.step || null, index: nd.index == null ? null : nd.index, text: nd.text || null } } };
      if (yaw) node.rotation = [0, Math.sin(yaw / 2), 0, Math.cos(yaw / 2)];
      return node;
    });
    return {
      asset: { version: "2.0", generator: "Cognition.X CXXR " + CXXR.version, copyright: "Scenario content: Cognition.X; scene: cx-xrscene/1" },
      scene: 0, scenes: [{ name: scene.title, nodes: nodes.map((_, i) => i) }],
      nodes, meshes, materials,
      accessors: [
        { bufferView: 0, componentType: 5126, count: 24, type: "VEC3", min: [-0.5, -0.5, -0.5], max: [0.5, 0.5, 0.5] },
        { bufferView: 1, componentType: 5126, count: 24, type: "VEC3" },
        { bufferView: 2, componentType: 5123, count: 36, type: "SCALAR" }],
      bufferViews: [
        { buffer: 0, byteOffset: oP, byteLength: pb.length, target: 34962 },
        { buffer: 0, byteOffset: oN, byteLength: nb.length, target: 34962 },
        { buffer: 0, byteOffset: oI, byteLength: ib.length, target: 34963 }],
      buffers: [{ byteLength: total, uri: "data:application/octet-stream;base64," + b64(buf) }],
      extras: { format: scene.format, scenario: scene.scenario, site: scene.site, law: scene.law, note: scene.note, units: scene.units }
    };
  };

  /* ---------------- glTF 2.0 / GLB reader (v0.70.0): a hall's own room, offline.
     Accepts an ArrayBuffer (a .glb, or the bytes of a .gltf), a string or a
     parsed document. Buffers must be embedded — a GLB's BIN chunk or data:
     URIs — because this page never fetches. Reads every mesh primitive's
     POSITION (and NORMAL when present; flat normals are computed otherwise),
     resolves indices (8/16/32-bit) into a flat triangle list, composes node
     transforms (matrix or TRS) down the scene graph, takes each material's
     baseColorFactor, and returns the meshes with the room moved so its floor
     sits at y = 0, centred on the learner. Nothing about the file leaves. */
  function b64toBytes(b) {
    if (typeof atob === "function") { const s = atob(b); const o = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) o[i] = s.charCodeAt(i); return o; }
    return new Uint8Array(Buffer.from(b, "base64"));
  }
  CXXR.parseGltf = function (input) {
    let json, bin = null;
    if (input instanceof ArrayBuffer || (typeof ArrayBuffer !== "undefined" && ArrayBuffer.isView(input))) {
      const bytes = input instanceof ArrayBuffer ? new Uint8Array(input) : new Uint8Array(input.buffer, input.byteOffset, input.byteLength);
      const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
      if (bytes.length >= 12 && dv.getUint32(0, true) === 0x46546C67) {       // "glTF" — a GLB container
        let off = 12; while (off < bytes.length) { const len = dv.getUint32(off, true), type = dv.getUint32(off + 4, true); const chunk = bytes.subarray(off + 8, off + 8 + len);
          if (type === 0x4E4F534A) json = JSON.parse(new TextDecoder().decode(chunk)); else if (type === 0x004E4942) bin = chunk; off += 8 + len; }
        if (!json) throw new Error("GLB without a JSON chunk");
      } else json = JSON.parse(new TextDecoder().decode(bytes));
    } else json = typeof input === "string" ? JSON.parse(input) : input;
    if (!json || !json.asset || String(json.asset.version).split(".")[0] !== "2") throw new Error("not glTF 2.0");
    const buffers = (json.buffers || []).map((b, i) => {
      if (b.uri == null) { if (!bin) throw new Error("buffer " + i + " has no data (GLB BIN chunk missing)"); return bin; }
      if (!/^data:/.test(b.uri)) throw new Error("buffer " + i + " is an external file; this page fetches nothing — embed it (data: URI) or use a .glb");
      return b64toBytes(b.uri.slice(b.uri.indexOf(",") + 1));
    });
    const view = i => { const bv = json.bufferViews[i]; const b = buffers[bv.buffer]; return { bytes: b.subarray(bv.byteOffset || 0, (bv.byteOffset || 0) + bv.byteLength), stride: bv.byteStride || 0 }; };
    const comp = { 5120: [Int8Array, 1], 5121: [Uint8Array, 1], 5122: [Int16Array, 2], 5123: [Uint16Array, 2], 5125: [Uint32Array, 4], 5126: [Float32Array, 4] };
    const ncomp = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16 };
    const accessor = i => {
      const a = json.accessors[i]; const [T, sz] = comp[a.componentType]; const n = ncomp[a.type]; const out = new (T === Float32Array ? Float32Array : (T === Uint32Array ? Uint32Array : (T === Uint16Array ? Uint16Array : (T === Int16Array ? Int16Array : (T === Int8Array ? Int8Array : Uint8Array)))))(a.count * n);
      if (a.bufferView == null) return out;
      const v = view(a.bufferView); const base = v.bytes.byteOffset + (a.byteOffset || 0); const stride = v.stride || sz * n;
      const dv = new DataView(v.bytes.buffer);
      const rd = { 5120: o => dv.getInt8(o), 5121: o => dv.getUint8(o), 5122: o => dv.getInt16(o, true), 5123: o => dv.getUint16(o, true), 5125: o => dv.getUint32(o, true), 5126: o => dv.getFloat32(o, true) }[a.componentType];
      for (let k = 0; k < a.count; k++) for (let c = 0; c < n; c++) out[k * n + c] = rd(base + k * stride + c * sz);
      return out;
    };
    const quatMat = q => { const [x, y, z, w] = q; return [1-2*(y*y+z*z), 2*(x*y+z*w), 2*(x*z-y*w), 0, 2*(x*y-z*w), 1-2*(x*x+z*z), 2*(y*z+x*w), 0, 2*(x*z+y*w), 2*(y*z-x*w), 1-2*(x*x+y*y), 0, 0, 0, 0, 1]; };
    const local = nd => { if (nd.matrix) return nd.matrix.slice(); const t = nd.translation || [0, 0, 0], r = nd.rotation || [0, 0, 0, 1], s = nd.scale || [1, 1, 1];
      const R = quatMat(r); const S = [s[0],0,0,0, 0,s[1],0,0, 0,0,s[2],0, 0,0,0,1]; const T = [1,0,0,0, 0,1,0,0, 0,0,1,0, t[0],t[1],t[2],1]; return M.mul(T, M.mul(R, S)); };
    const meshes = []; let triangles = 0;
    const walk = (ni, parent) => {
      const nd = json.nodes[ni]; const model = M.mul(parent, local(nd));
      if (nd.mesh != null) (json.meshes[nd.mesh].primitives || []).forEach(pr => {
        if (pr.mode != null && pr.mode !== 4) return;                              // triangles only
        const pos = accessor(pr.attributes.POSITION); const nrm = pr.attributes.NORMAL != null ? accessor(pr.attributes.NORMAL) : null;
        const idx = pr.indices != null ? accessor(pr.indices) : null; const tri = idx ? idx.length / 3 : pos.length / 9;
        const P = new Float32Array(tri * 9), N = new Float32Array(tri * 9);
        for (let t = 0; t < tri; t++) {
          const ids = [0, 1, 2].map(k => idx ? idx[t * 3 + k] : t * 3 + k);
          ids.forEach((vi, k) => { P.set(pos.subarray(vi * 3, vi * 3 + 3), t * 9 + k * 3); if (nrm) N.set(nrm.subarray(vi * 3, vi * 3 + 3), t * 9 + k * 3); });
          if (!nrm) { const a = P.subarray(t*9, t*9+3), b = P.subarray(t*9+3, t*9+6), c = P.subarray(t*9+6, t*9+9); const n = norm(cross(sub(Array.from(b), Array.from(a)), sub(Array.from(c), Array.from(a)))); for (let k = 0; k < 3; k++) N.set(n, t * 9 + k * 3); }
        }
        const mat = pr.material != null ? json.materials[pr.material] : null;
        const color = (mat && mat.pbrMetallicRoughness && mat.pbrMetallicRoughness.baseColorFactor) ? mat.pbrMetallicRoughness.baseColorFactor.slice(0, 4) : [0.72, 0.70, 0.66, 1];
        meshes.push({ positions: P, normals: N, model, color, name: nd.name || ("node " + ni) }); triangles += tri;
      });
      (nd.children || []).forEach(c => walk(c, model));
    };
    const sceneIdx = json.scene != null ? json.scene : 0; const roots = json.scenes && json.scenes[sceneIdx] ? json.scenes[sceneIdx].nodes : (json.nodes || []).map((_, i) => i);
    roots.forEach(r => walk(r, M.ident()));
    if (!meshes.length) throw new Error("no triangle meshes in the file");
    // world bounds → floor to y = 0, centred in x/z
    let mn = [Infinity, Infinity, Infinity], mx = [-Infinity, -Infinity, -Infinity];
    meshes.forEach(m => { for (let i = 0; i < m.positions.length; i += 3) { const w = M.xf(m.model, [m.positions[i], m.positions[i+1], m.positions[i+2]], 1); for (let k = 0; k < 3; k++) { if (w[k] < mn[k]) mn[k] = w[k]; if (w[k] > mx[k]) mx[k] = w[k]; } } });
    const shift = [-(mn[0] + mx[0]) / 2, -mn[1], -(mn[2] + mx[2]) / 2];
    const T = [1,0,0,0, 0,1,0,0, 0,0,1,0, shift[0], shift[1], shift[2], 1];
    meshes.forEach(m => { m.model = M.mul(T, m.model); });
    return { meshes, triangles, bounds: { min: mn, max: mx, size: [mx[0]-mn[0], mx[1]-mn[1], mx[2]-mn[2]] } };
  };

  /* ---------------- the renderer + the view attached to a studio run */
  const VS = "attribute vec3 aPos;attribute vec3 aNorm;attribute vec2 aUV;uniform mat4 uMVP;uniform mat4 uModel;varying vec3 vN;varying vec2 vUV;void main(){vN=mat3(uModel)*aNorm;vUV=aUV;gl_Position=uMVP*vec4(aPos,1.0);}";
  const FS = "precision mediump float;uniform vec4 uColor;uniform sampler2D uTex;uniform float uUseTex;uniform vec3 uLight;varying vec3 vN;varying vec2 vUV;void main(){vec4 base=mix(uColor,texture2D(uTex,vUV),uUseTex);float d=0.55+0.45*max(dot(normalize(vN),normalize(uLight)),0.0);gl_FragColor=vec4(base.rgb*d,base.a);}";

  CXXR.attach = function (ctl, simHost, sc, opts) {
    opts = opts || {};
    if (typeof document === "undefined") return null;
    const panel = document.createElement("div"); panel.className = "cxxr-panel";
    panel.innerHTML = `<div class="cxxr-bar"><span class="cxxr-status" role="status" aria-live="polite"></span>
        <button type="button" class="cxsim-btn cxxr-vr" hidden>Enter VR</button>
        <button type="button" class="cxsim-btn cxxr-ar" hidden>Enter AR</button>
        <button type="button" class="cxsim-btn cxxr-gltf">Export scene (glTF)</button>
        <button type="button" class="cxsim-btn cxxr-json">Export scene (JSON)</button>
        <label class="cxsim-btn cxxr-roomlab">Load your hall's room <input type="file" class="cxxr-room" accept=".gltf,.glb,model/gltf+json,model/gltf-binary" style="display:none"></label>
        <button type="button" class="cxsim-btn cxxr-close">Close 3D</button></div>
      <canvas class="cxxr-canvas" width="960" height="540" tabindex="0" aria-label="The scenario as a room: drag or use the arrow keys to look around; click a slab to choose. The buttons above this view are the same choices."></canvas>
      <p class="cxsim-note cxxr-note">A scene is practice, never a check, never a credential. The room is drawn from your device's position only while a VR or AR session runs; nothing about where you look or move is recorded or leaves this page. No hand, eye or face tracking is requested.</p>`;
    simHost.insertAdjacentElement("afterend", panel);
    const canvas = panel.querySelector(".cxxr-canvas"), status = panel.querySelector(".cxxr-status");
    const gl = canvas.getContext("webgl", { xrCompatible: true, antialias: true, preserveDrawingBuffer: true }) || canvas.getContext("experimental-webgl");
    if (!gl) { status.textContent = "This browser cannot draw 3D (no WebGL). The buttons above still run the scenario."; return { destroy() { panel.remove(); } }; }

    // program + geometry
    const prog = gl.createProgram();
    [[gl.VERTEX_SHADER, VS], [gl.FRAGMENT_SHADER, FS]].forEach(([t, src]) => { const s = gl.createShader(t); gl.shaderSource(s, src); gl.compileShader(s); gl.attachShader(prog, s); });
    gl.linkProgram(prog); gl.useProgram(prog);
    const A = { pos: gl.getAttribLocation(prog, "aPos"), norm: gl.getAttribLocation(prog, "aNorm"), uv: gl.getAttribLocation(prog, "aUV") };
    const U = { mvp: gl.getUniformLocation(prog, "uMVP"), model: gl.getUniformLocation(prog, "uModel"), color: gl.getUniformLocation(prog, "uColor"), useTex: gl.getUniformLocation(prog, "uUseTex"), light: gl.getUniformLocation(prog, "uLight"), tex: gl.getUniformLocation(prog, "uTex") };
    const cube = cubeGeometry();
    const uvs = new Float32Array(24 * 2); for (let f = 0; f < 6; f++) { uvs.set([0,1, 1,1, 1,0, 0,0], f * 8); }
    const vb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vb); gl.bufferData(gl.ARRAY_BUFFER, cube.P, gl.STATIC_DRAW);
    const nb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, nb); gl.bufferData(gl.ARRAY_BUFFER, cube.N, gl.STATIC_DRAW);
    const ub = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, ub); gl.bufferData(gl.ARRAY_BUFFER, uvs, gl.STATIC_DRAW);
    const ibuf = gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibuf); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, cube.I, gl.STATIC_DRAW);
    gl.enable(gl.DEPTH_TEST); gl.enable(gl.CULL_FACE); gl.cullFace(gl.BACK);
    gl.uniform3f(U.light, 0.4, 1.0, 0.6);
    const white = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, white); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([255,255,255,255]));

    // text textures (canvas 2D → texture), cached by string
    const texCache = new Map();
    function textTex(text, bg, fg) {
      const key = text + "|" + bg; if (texCache.has(key)) return texCache.get(key);
      const c = document.createElement("canvas"); c.width = 512; c.height = 256; const x = c.getContext("2d");
      x.fillStyle = bg; x.fillRect(0, 0, 512, 256); x.fillStyle = fg; x.font = "600 30px 'Instrument Sans', system-ui, sans-serif"; x.textBaseline = "top";
      const words = String(text).split(/\s+/), lines = []; let line = "";
      for (const w of words) { const t = line ? line + " " + w : w; if (x.measureText(t).width > 470 && line) { lines.push(line); line = w; } else line = t; }
      if (line) lines.push(line);
      lines.slice(0, 6).forEach((l, i) => x.fillText(l, 20, 24 + i * 38));
      const tex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tex); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, c); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      texCache.set(key, tex); return tex;
    }

    // the run state this view mirrors (from the studio's events; never scored here)
    const state = { site: opts.site || sc.site_default, plan: [], idx: -1, phase: "intro", options: [], picked: null, xr: null, mode: "window", room: null };
    let scene = CXXR.scene(sc, state.site, []);
    const drawables = () => {
      const out = [];
      scene.nodes.forEach(nd => {
        if (nd.kind === "floor" && state.room) return;   // a loaded room brings its own floor
        let color = nd.color;
        if (nd.kind === "station") color = nd.index === state.idx ? COL.current : (nd.index < state.idx ? COL.done : COL.station);
        out.push({ model: M.trs(nd.position, nd.yaw || 0, nd.size), color, tex: null, pick: null });
        if (nd.kind === "station" || nd.kind === "sign") {
          const yaw = nd.yaw || 0;
          const lp = nd.kind === "sign" ? [nd.position[0] + Math.sin(yaw) * 0.04, nd.position[1], nd.position[2] + Math.cos(yaw) * 0.04] : [nd.position[0], nd.position[1] + 0.9, nd.position[2]];
          const ls = nd.kind === "sign" ? [nd.size[0] - 0.1, nd.size[1] - 0.1, 0.01] : [1.3, 0.45, 0.01];
          const bg = nd.kind === "sign" ? (nd.id === "sign-youth" ? "#5a2119" : "#1f2126") : (nd.index === state.idx ? "#d9a441" : "#2f6b8c");
          out.push({ model: M.trs(lp, yaw, ls), color: [1,1,1,1], tex: textTex(nd.text, bg, nd.kind === "sign" ? "#f3efe6" : "#ffffff"), pick: null });
        }
      });
      // the current decision's option slabs, stacked above its station, facing the learner
      const cur = scene.nodes.find(nd => nd.kind === "station" && nd.index === state.idx);
      if (cur && state.phase !== "intro" && state.phase !== "debrief") {
        state.options.forEach((o, i) => {
          const p = [cur.position[0], 1.55 + i * 0.5, cur.position[2]];
          const col = state.picked == null ? COL.option : (state.picked === i ? COL.picked : COL.faded);
          out.push({ model: M.trs([p[0] - Math.sin(cur.yaw) * 0.55, p[1], p[2] + Math.cos(cur.yaw) * 0.55], cur.yaw, [1.5, 0.44, 0.06]), color: col,
                     tex: textTex((i + 1) + ". " + short(o.t, 110), state.picked == null ? "#f0eee8" : (state.picked === i ? "#d9a441" : "#9a9a96"), "#1a1a1a"), pick: { option: i } });
        });
        if (state.phase === "consequence") out.push({ model: M.trs([cur.position[0] - Math.sin(cur.yaw) * 0.55, 1.15, cur.position[2] + Math.cos(cur.yaw) * 0.55], cur.yaw, [1.5, 0.3, 0.06]), color: COL.picked, tex: textTex("Next →", "#d9a441", "#1a1a1a"), pick: { next: true } });
      }
      return out;
    };

    function drawScene(proj, view) {
      const items = drawables();
      gl.useProgram(prog);
      const bind = (b, loc, n) => { gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, n, gl.FLOAT, false, 0, 0); };
      const vp = M.mul(proj, view);
      if (state.room) {
        gl.disableVertexAttribArray(A.uv); gl.vertexAttrib2f(A.uv, 0, 0);
        gl.uniform1f(U.useTex, 0); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, white); gl.uniform1i(U.tex, 0);
        state.room.gl.forEach(m => {
          bind(m.vb, A.pos, 3); bind(m.nb, A.norm, 3);
          gl.uniformMatrix4fv(U.mvp, false, new Float32Array(M.mul(vp, m.model))); gl.uniformMatrix4fv(U.model, false, new Float32Array(m.model));
          gl.uniform4fv(U.color, m.color); gl.drawArrays(gl.TRIANGLES, 0, m.count);
        });
      }
      bind(vb, A.pos, 3); bind(nb, A.norm, 3); bind(ub, A.uv, 2); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibuf);
      items.forEach(it => {
        gl.uniformMatrix4fv(U.mvp, false, new Float32Array(M.mul(vp, it.model)));
        gl.uniformMatrix4fv(U.model, false, new Float32Array(it.model));
        gl.uniform4fv(U.color, it.color); gl.uniform1f(U.useTex, it.tex ? 1 : 0);
        gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, it.tex || white); gl.uniform1i(U.tex, 0);
        gl.drawElements(gl.TRIANGLES, 36, gl.UNSIGNED_SHORT, 0);
      });
      return items;
    }
    // ray vs unit cube in each pickable's local space
    function pick(origin, dir) {
      let best = null, bt = Infinity;
      drawables().forEach(it => {
        if (!it.pick) return;
        const inv = M.inv(it.model), o = M.xf(inv, origin, 1), d = M.xf(inv, dir, 0);
        let t0 = -Infinity, t1 = Infinity;
        for (let k = 0; k < 3; k++) { if (Math.abs(d[k]) < 1e-9) { if (o[k] < -0.5 || o[k] > 0.5) return; continue; } let a = (-0.5 - o[k]) / d[k], b = (0.5 - o[k]) / d[k]; if (a > b) [a, b] = [b, a]; t0 = Math.max(t0, a); t1 = Math.min(t1, b); }
        if (t1 >= Math.max(t0, 0) && t0 < bt) { bt = t0; best = it.pick; }
      });
      return best;
    }
    function act(p) {
      if (!p) return false;
      if (p.option != null && state.phase === "step" && typeof ctl.choose === "function") { ctl.choose(p.option); return true; }
      if (p.next && state.phase === "consequence" && typeof ctl.next === "function") { ctl.next(); return true; }
      return false;
    }

    // magic window camera
    const cam = { yaw: 0, pitch: -0.12, dist: 3.4, target: [0, 1.2, -1.2] };
    function windowView() { const e = [cam.target[0] + Math.sin(cam.yaw) * Math.cos(cam.pitch) * cam.dist, cam.target[1] - Math.sin(cam.pitch) * cam.dist, cam.target[2] + Math.cos(cam.yaw) * Math.cos(cam.pitch) * cam.dist]; return { eye: e, view: M.lookAt(e, cam.target, UP) }; }
    let dirty = true, raf = 0, destroyed = false;
    function renderWindow() {
      if (destroyed || state.mode !== "window") return;
      if (dirty) {
        dirty = false;
        gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, canvas.width, canvas.height);
        gl.clearColor(0.93, 0.92, 0.89, 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
        drawScene(M.persp(1.05, canvas.width / canvas.height, 0.05, 60), windowView().view);
      }
      raf = global.requestAnimationFrame(renderWindow);
    }
    let drag = null;
    canvas.addEventListener("pointerdown", e => { drag = { x: e.clientX, y: e.clientY, yaw: cam.yaw, pitch: cam.pitch, moved: false }; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener("pointermove", e => { if (!drag) return; const dx = e.clientX - drag.x, dy = e.clientY - drag.y; if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true; cam.yaw = drag.yaw - dx * 0.006; cam.pitch = Math.max(-1.2, Math.min(0.6, drag.pitch - dy * 0.006)); dirty = true; });
    canvas.addEventListener("pointerup", e => {
      if (drag && !drag.moved) {
        const r = canvas.getBoundingClientRect(), nx = (e.clientX - r.left) / r.width * 2 - 1, ny = 1 - (e.clientY - r.top) / r.height * 2;
        const inv = M.inv(M.mul(M.persp(1.05, canvas.width / canvas.height, 0.05, 60), windowView().view));
        const a = M.xf(inv, [nx, ny, -1], 1), b = M.xf(inv, [nx, ny, 1], 1);
        const wA = inv[3]*nx + inv[7]*ny + inv[11]*-1 + inv[15], wB = inv[3]*nx + inv[7]*ny + inv[11] + inv[15];
        const pa = [a[0]/wA, a[1]/wA, a[2]/wA], pb = [b[0]/wB, b[1]/wB, b[2]/wB];
        act(pick(pa, norm(sub(pb, pa))));
      }
      drag = null;
    });
    canvas.addEventListener("keydown", e => { const k = e.key; if (k === "ArrowLeft") cam.yaw += 0.12; else if (k === "ArrowRight") cam.yaw -= 0.12; else if (k === "ArrowUp") cam.pitch = Math.max(-1.2, cam.pitch - 0.08); else if (k === "ArrowDown") cam.pitch = Math.min(0.6, cam.pitch + 0.08); else return; e.preventDefault(); dirty = true; });

    // WebXR sessions
    const xr = global.navigator && global.navigator.xr;
    async function offer() {
      if (!xr) { status.textContent = "WebXR is not available in this browser, so this is the magic-window view: drag or use the arrow keys to look around, click a slab to choose. On a headset or a WebXR phone the same page offers Enter VR / Enter AR."; return; }
      const vr = await xr.isSessionSupported("immersive-vr").catch(() => false), ar = await xr.isSessionSupported("immersive-ar").catch(() => false);
      panel.querySelector(".cxxr-vr").hidden = !vr; panel.querySelector(".cxxr-ar").hidden = !ar;
      status.textContent = vr || ar ? "WebXR is available: enter VR or AR, or stay in the window. Choices work the same in all three." : "WebXR is present but no immersive session is offered here; the magic-window view is the whole experience.";
    }
    async function enter(mode) {
      try {
        const session = await xr.requestSession(mode, { optionalFeatures: ["local-floor"] });
        await gl.makeXRCompatible();
        session.updateRenderState({ baseLayer: new global.XRWebGLLayer(session, gl) });
        const ref = await session.requestReferenceSpace("local-floor").catch(() => session.requestReferenceSpace("local"));
        state.mode = mode; state.xr = { session, ref }; global.cancelAnimationFrame(raf);
        status.textContent = (mode === "immersive-ar" ? "AR" : "VR") + " session running. Look at a slab and select to choose; the page keeps nothing about where you look or move.";
        session.addEventListener("select", ev => {
          const fr = ev.frame, pose = fr.getPose(ev.inputSource.targetRaySpace, ref); if (!pose) return;
          const m = pose.transform.matrix; act(pick([m[12], m[13], m[14]], norm([-m[8], -m[9], -m[10]])));
        });
        session.addEventListener("end", () => { state.mode = "window"; state.xr = null; dirty = true; status.textContent = "Session ended. Back in the window."; raf = global.requestAnimationFrame(renderWindow); });
        const loop = (t, frame) => {
          if (state.mode === "window") return;
          session.requestAnimationFrame(loop);
          const pose = frame.getViewerPose(ref); if (!pose) return;
          const layer = session.renderState.baseLayer; gl.bindFramebuffer(gl.FRAMEBUFFER, layer.framebuffer);
          if (mode === "immersive-ar") { gl.clearColor(0, 0, 0, 0); } else { gl.clearColor(0.93, 0.92, 0.89, 1); }
          gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
          for (const view of pose.views) { const vp = layer.getViewport(view); gl.viewport(vp.x, vp.y, vp.width, vp.height); drawScene(Array.from(view.projectionMatrix), Array.from(view.transform.inverse.matrix)); }
        };
        session.requestAnimationFrame(loop);
      } catch (e) { status.textContent = "Could not start the session (" + (e && e.message ? e.message : e) + "). The window view continues."; }
    }
    panel.querySelector(".cxxr-json").addEventListener("click", () => {
      const text = JSON.stringify(scene, null, 1);
      try { const blob = new Blob([text], { type: "application/json" }); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "cognitionx-" + sc.id.toLowerCase() + ".xrscene.json"; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); } catch (e) {}
      status.textContent = "cx-xrscene/1 exported: " + scene.nodes.length + " nodes in metres, +Y up.";
    });
    // v0.70.0: a hall's own room — a glTF or GLB with EMBEDDED buffers (this page fetches nothing) — drawn under the stations
    function loadRoom(data) {
      try {
        const parsed = CXXR.parseGltf(data);
        if (state.room) state.room.gl.forEach(m => { gl.deleteBuffer(m.vb); gl.deleteBuffer(m.nb); });
        const uploaded = parsed.meshes.map(m => { const vb2 = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vb2); gl.bufferData(gl.ARRAY_BUFFER, m.positions, gl.STATIC_DRAW); const nb2 = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, nb2); gl.bufferData(gl.ARRAY_BUFFER, m.normals, gl.STATIC_DRAW); return { vb: vb2, nb: nb2, count: m.positions.length / 3, model: m.model, color: m.color }; });
        state.room = { gl: uploaded, meshes: parsed.meshes.length, triangles: parsed.triangles, bounds: parsed.bounds };
        dirty = true;
        status.textContent = "Room loaded: " + parsed.meshes.length + " mesh(es), " + parsed.triangles.toLocaleString() + " triangles, floor set to y = 0 and centred. It stays on this device.";
        return state.room;
      } catch (e) { status.textContent = "Could not read that file as glTF 2.0 with embedded buffers (" + (e && e.message ? e.message : e) + "). A .glb, or a .gltf whose buffers are data: URIs, is what this page can open offline."; return null; }
    }
    panel.querySelector(".cxxr-room").addEventListener("change", ev => {
      const f = ev.target.files && ev.target.files[0]; if (!f) return;
      const rd = new FileReader(); rd.onload = () => { loadRoom(rd.result); }; rd.readAsArrayBuffer(f);
    });
    panel.querySelector(".cxxr-vr").addEventListener("click", () => enter("immersive-vr"));
    panel.querySelector(".cxxr-ar").addEventListener("click", () => enter("immersive-ar"));
    panel.querySelector(".cxxr-gltf").addEventListener("click", () => {
      const doc = CXXR.gltf(scene); const text = JSON.stringify(doc, null, 1);
      try { const blob = new Blob([text], { type: "model/gltf+json" }); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "cognitionx-" + sc.id.toLowerCase() + ".gltf"; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); } catch (e) {}
      status.textContent = "glTF 2.0 exported: " + doc.nodes.length + " nodes, one embedded buffer. Opens in Blender, Unity, Unreal, Godot, Hubs or any glTF viewer.";
    });
    const onEvent = ev => {
      const d = ev.detail || {};
      state.phase = d.phase; state.idx = d.idx == null ? -1 : d.idx; state.plan = d.plan || state.plan; state.options = d.options || []; state.picked = d.picked == null ? null : d.picked;
      if (d.plan && d.plan.length && scene.nodes.filter(n => n.kind === "station").length !== d.plan.length) scene = CXXR.scene(sc, state.site, d.plan);
      dirty = true;
    };
    simHost.addEventListener("cxsim", onEvent);
    const destroy = () => { destroyed = true; simHost.removeEventListener("cxsim", onEvent); if (state.xr) { try { state.xr.session.end(); } catch (e) {} } if (state.room) state.room.gl.forEach(m => { gl.deleteBuffer(m.vb); gl.deleteBuffer(m.nb); }); global.cancelAnimationFrame(raf); panel.remove(); };
    const api = { destroy, state, pick, act, loadRoom, get scene() { return scene; }, gltf: () => CXXR.gltf(scene), supported: !!xr, canvas };
    panel.querySelector(".cxxr-close").addEventListener("click", () => api.destroy());   // through the object, so a host's wrapper runs too
    offer(); raf = global.requestAnimationFrame(renderWindow);
    return api;
  };

  global.CXXR = CXXR;
})(typeof window !== "undefined" ? window : globalThis);
