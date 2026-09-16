# Credential records — the native format and the Open Badges 3.0 envelope

The Louisiana app's Records Office signs a learner's earned credential
into a portable file that verifies offline. Since v0.60.0 it can issue
the same credential in two forms from the same key:

| Form | What it is | Who can read it |
|---|---|---|
| **`cx-credential/1`** (native, canonical) | `{payload, signature, publicKey, issuer}` — the payload states the credential, track, pack, the learner's first name or nickname, band, issue date, **how many of the fifty checks an assessor witnessed**, and whether the learner is demo data; ECDSA P-256 over the payload's JSON | Cognition.X apps, `tools/verify_record.js`, anyone with WebCrypto |
| **Open Badges 3.0 as `vc+jwt`** (envelope) | A W3C Verifiable Credential 2.0 `OpenBadgeCredential` secured as a compact JWS (ES256), the issuer identified by `did:jwk`, the native payload embedded as `cx:record` so nothing is lost | OB 3.0 / VC 2.0 wallets, validators and verifiers that accept JWT-secured credentials; the same tools as above |

Both carry the same `rid` (the native record id; the VC's `id` is
`urn:uuid:<rid>`), so a `cx-revocation/1` list published by the office
revokes both.

## What a verifier learns, and what it does not

A valid signature proves two things: the record is **unaltered**, and it
was signed by whoever holds the **private key** matching the carried
public key. It does not prove who that is. Identity is confirmed
out-of-band: the hall publishes its public key; a verifier adds it to a
trust list; only then does a record grade *trusted by name*. This is the
same design banks arrived at, and the wording travels inside every
record (`verify` in the native form, `criteria.narrative` in the
envelope).

Four grades, in every path (the app, the command line, and any tool
that follows the same rules):

- **Invalid** — altered, or the signature does not match the carried key.
- **Valid, key not trusted** — unaltered and holder-signed; identity unconfirmed.
- **Trusted by name** — valid, and the key matches a named office on the verifier's trust list.
- **Revoked** — valid, but the issuing office lists the record id on a revocation document signed with the same key. Revoked outranks trusted.

The private key is non-extractable (v0.57.0) and never leaves the
browser profile that created it; a retired office cannot sign again, but
everything it signed still verifies against its published public key.

## The envelope, exactly

Header: `{"alg":"ES256","typ":"vc+jwt","kid":"did:jwk:<base64url(public JWK)>#0"}`.
Payload — the credential itself, per *Securing Verifiable Credentials
using JOSE and COSE*:

```json
{
  "@context": ["https://www.w3.org/ns/credentials/v2",
               "https://purl.imsglobal.org/spec/ob/v3p0/context-3.0.3.json",
               {"cx": "https://github.com/AGIFutureFoundation/Cognition.X/blob/main/docs/CREDENTIALS.md#"}],
  "id": "urn:uuid:<rid>",
  "type": ["VerifiableCredential", "OpenBadgeCredential"],
  "issuer": {"id": "did:jwk:…", "type": ["Profile"], "name": "<records office>"},
  "validFrom": "<issue date>T00:00:00Z",
  "name": "<credential>",
  "credentialSubject": {
    "type": ["AchievementSubject"],
    "identifier": [{"type": "IdentityObject", "identityType": "name", "hashed": false, "identityHash": "<first name or nickname>"}],
    "achievement": {"id": "urn:cx:achievement:<pack>:<track>", "type": ["Achievement"], "achievementType": "Competency",
                    "name": "<credential>", "description": "<track> — <pack>: fifty transfer checks on real material",
                    "criteria": {"narrative": "<the witnessed-count sentence and the honest-scope wording>"}}
  },
  "cx:record": { …the native payload… }
}
```

Signature: ES256 over `base64url(header).base64url(payload)`; WebCrypto's
raw `r‖s` output is exactly the JWS form. The learner stays pseudonymous
by design: no subject `id`, no e-mail, no hashed identity — a first name
or nickname as the OB3 `IdentityObject`, unhashed and labelled so.

## Verifying from the command line

```
node tools/verify_record.js record.json
node tools/verify_record.js badge.jwt --trust trustlist.json --revocations revocation.json
```

No dependencies; Node 20 or later (WebCrypto). Exit 0 for valid or
trusted, 2 for revoked, 1 for invalid or unreadable.

## Round-tripping through a third-party validator

The envelope is standard JWT-secured VC 2.0 with the OB 3.0 context and
types; a validator that accepts `vc+jwt` with `did:jwk` issuers will
verify the signature and read the credential. Two honest limits: the
`cx:record` term is this project's own (declared in the context); and
`did:jwk` names a key, not an institution — which is the point.

## What did not change

The native path, the fifty-check threshold, the witnessed count on the
face of every record, the trust list, revocation, the non-extractable
key, and the wording that a signature proves integrity and key
possession while identity is confirmed out-of-band.
