#!/usr/bin/env node
/* Verify a Cognition.X credential from the command line — offline, no dependencies.
 *
 *   node tools/verify_record.js <file> [--trust trustlist.json] [--revocations list.json ...]
 *
 * <file> is either a native cx-credential/1 record (JSON: {payload, signature,
 * publicKey, issuer}) or an Open Badges 3.0 credential as a compact vc+jwt
 * (three base64url segments, ES256, kid = did:jwk:…) as issued by the
 * Louisiana app's Records Office since v0.60.0.
 *
 * Prints one of the four grades the app prints, for the same reasons:
 *   INVALID      — altered, or the signature does not match the carried key
 *   VALID        — unaltered and signed by the holder of the carried key; the
 *                  key is not on your trust list, so identity is unconfirmed
 *   TRUSTED      — as VALID, and the key matches a named office on --trust
 *   REVOKED      — the issuing office lists this record id on a signed
 *                  cx-revocation/1 document you passed with --revocations
 * Exit code 0 for VALID/TRUSTED, 2 for REVOKED, 1 for INVALID or unreadable.
 *
 * What a signature proves: integrity and possession of the key. Who holds
 * the key is confirmed out-of-band (the hall publishes its public key). */
"use strict";
const fs = require("fs");
const subtle = globalThis.crypto.subtle;
const enc = s => new TextEncoder().encode(s);
const b64d = s => Uint8Array.from(Buffer.from(s, "base64"));
const b64ud = s => Uint8Array.from(Buffer.from(s.replace(/-/g, "+").replace(/_/g, "/"), "base64"));
const jwkEq = (a, b) => !!(a && b && a.kty === b.kty && a.crv === b.crv && a.x === b.x && a.y === b.y);

async function importPub(jwk) {
  return subtle.importKey("jwk", { kty: jwk.kty, crv: jwk.crv, x: jwk.x, y: jwk.y }, { name: "ECDSA", namedCurve: "P-256" }, false, ["verify"]);
}
async function verifyNative(rec) {
  const pub = await importPub(rec.publicKey);
  const ok = await subtle.verify({ name: "ECDSA", hash: "SHA-256" }, pub, b64d(rec.signature), enc(JSON.stringify(rec.payload)));
  return { ok, rid: rec.payload.rid, publicKey: rec.publicKey, issuer: rec.issuer, credential: rec.payload.credential, learner: rec.payload.learner, issuedAt: rec.payload.issuedAt, form: "cx-credential/1" };
}
async function verifyJwt(jwt) {
  const [h, p, s] = jwt.trim().split(".");
  const header = JSON.parse(Buffer.from(b64ud(h)).toString("utf8"));
  const vc = JSON.parse(Buffer.from(b64ud(p)).toString("utf8"));
  if (header.alg !== "ES256" || !/^did:jwk:/.test(header.kid || "")) throw new Error("expected ES256 with a did:jwk kid");
  const jwk = JSON.parse(Buffer.from(b64ud(header.kid.replace(/^did:jwk:/, "").replace(/#.*$/, ""))).toString("utf8"));
  const pub = await importPub(jwk);
  const ok = await subtle.verify({ name: "ECDSA", hash: "SHA-256" }, pub, b64ud(s), enc(h + "." + p));
  const subj = vc.credentialSubject || {};
  const idobj = (subj.identifier || [])[0] || {};
  return { ok, rid: String(vc.id || "").replace(/^urn:(uuid|cx:rid):/, ""), publicKey: jwk, issuer: (vc.issuer || {}).name, credential: vc.name || ((subj.achievement || {}).name), learner: idobj.identityHash, issuedAt: vc.validFrom, form: header.typ || "vc+jwt", witnessed: (vc["cx:record"] || {}).witnessed, demo: (vc["cx:record"] || {}).demo };
}
async function revokedBy(r, lists) {
  for (const doc of lists) {
    try {
      if (!doc || !doc.payload || doc.payload.format !== "cx-revocation/1" || !jwkEq(doc.publicKey, r.publicKey)) continue;
      const pub = await importPub(doc.publicKey);
      const genuine = await subtle.verify({ name: "ECDSA", hash: "SHA-256" }, pub, b64d(doc.signature), enc(JSON.stringify(doc.payload)));
      if (!genuine) continue;
      const hit = (doc.payload.revoked || []).find(x => x.rid === r.rid);
      if (hit) return { office: doc.issuer || doc.payload.office, reason: hit.reason, at: hit.at };
    } catch (e) { /* an unreadable list never revokes */ }
  }
  return null;
}
(async () => {
  const args = process.argv.slice(2);
  const file = args.find(a => !a.startsWith("--") && !args[args.indexOf(a) - 1]?.startsWith("--"));
  if (!file) { console.error("usage: node tools/verify_record.js <record.json|credential.jwt> [--trust trustlist.json] [--revocations list.json ...]"); process.exit(1); }
  const trust = []; const revs = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--trust") { const t = JSON.parse(fs.readFileSync(args[++i], "utf8")); (t.offices || (Array.isArray(t) ? t : [t])).forEach(o => trust.push(o)); }
    if (args[i] === "--revocations") revs.push(JSON.parse(fs.readFileSync(args[++i], "utf8")));
  }
  const text = fs.readFileSync(file, "utf8").trim();
  let r;
  try { r = text.startsWith("{") ? await verifyNative(JSON.parse(text)) : await verifyJwt(text); }
  catch (e) { console.log("UNREADABLE — not a cx-credential/1 record or an ES256 vc+jwt:", e.message); process.exit(1); }
  if (!r.ok) { console.log(`INVALID — altered, or the signature does not match the carried key (${r.form}).`); process.exit(1); }
  const rev = await revokedBy(r, revs);
  if (rev) { console.log(`REVOKED by the issuing office${rev.office ? ` "${rev.office}"` : ""} — ${rev.reason || "no reason given"} (${rev.at || ""}). The signature is genuine; the office withdrew this record id.`); process.exit(2); }
  const who = trust.find(o => jwkEq(o.publicKey, r.publicKey));
  const what = `"${r.credential}" for ${r.learner}, issued ${r.issuedAt}${r.witnessed != null ? ` · ${r.witnessed} of 50 checks witnessed` : ""}${r.demo ? " · DEMO DATA" : ""} (${r.form})`;
  if (who) console.log(`TRUSTED — signed by trusted office "${who.recordsOffice}": ${what}`);
  else console.log(`VALID — unaltered and signed by the holder of the carried key (claims to be "${r.issuer || "unnamed office"}"); confirm the key with the hall out-of-band: ${what}`);
  process.exit(0);
})();
