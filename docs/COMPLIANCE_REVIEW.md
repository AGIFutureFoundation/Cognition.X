# Compliance and regulatory review of the apps

> **This is not legal advice.** It is an engineering review of what the
> six Cognition.X apps do with information, held mechanically by the tests
> that run on every push. A school, hall or program office adopting the
> platform keeps its own duties under FERPA, COPPA, its state's
> student-privacy law and its own policies; the fifty-state layer in
> [`STATE_COMPLIANCE.md`](STATE_COMPLIANCE.md) lists those. Where this
> document says a law "is not triggered", it means *by the software as
> built*; an adopter's own use may still trigger it.

Reviewed at v0.55.0. Scope: the six single-file apps (`apps/*/index.html`)
as built from their templates by `tools/build_*.py`, the shared runtime
(`tools/runtime_lib.py`), and the investor and public documents.

## Method

1. Read every template for storage, network, cryptography, external
   references and inline handlers; grep is in `tests/test_platform.py`.
2. Open every app in a headless browser, record every request the page
   makes and every console message, and try to make a request from
   inside the page (`tests/browser/smoke.js`, *compliance review*).
3. Map the laws and standards an education platform is measured against
   to what the software actually does, and write down the gap.
4. Fix what code can fix in this release; state what remains.

## Findings

| # | Finding | Severity | Status |
|---|---|---|---|
| 1 | Five apps loaded their typefaces from Google Fonts on every open — a third-party request carrying the reader's IP address and user agent, contradicting "nothing leaves the page on its own" and the offline promise | High | **Fixed (v0.55.0).** The latin subsets of the four families (all SIL Open Font License) are committed under `data/fonts/` and embedded into each build as `data:` URIs. No app names a font host; the tests forbid it. |
| 2 | No Content-Security-Policy: the no-network stance rested on code review alone | High | **Fixed.** Every app carries a strict CSP meta (`default-src 'none'`, `connect-src 'none'`, no eval, no frames, no objects, no workers). The browser now refuses any fetch, XHR, WebSocket, beacon or EventSource whatever a script tries; the smoke suite proves it by attempting one. |
| 3 | Outbound links (GitHub, LDOE, the Department of Education) sent the page's URL as a referrer | Medium | **Fixed.** `<meta name="referrer" content="no-referrer">` in every app. |
| 4 | No in-app disclosure of what is stored, and no single erase control | Medium | **Fixed.** A *Data & privacy* control in every app opens a dialog built from one canonical text (`data/policy/privacy.json`): the keys this app has written and their size, what stays, what leaves (nothing, by itself), rights, security, and *Erase everything this app stored in this browser* behind a confirm. Tests hold every app to the canonical text. |
| 5 | Learner names are entered freely into the Louisiana ledger; nothing said that a nickname is enough | Low | **Fixed.** The field asks for a first name or nickname; the notice says nothing here needs a legal name, birth date or contact detail, and none is asked for. |
| 6 | The Education OS's own network self-review still said the page reached `fonts.googleapis.com` | Low | **Fixed.** The claim now reads: one origin, the file itself. |
| 7 | The Louisiana Records Office keypair was stored in `localStorage` in exportable JWK form, so anyone with the browser profile held the signing key | Medium | **Fixed (v0.57.0).** The private key is a non-extractable WebCrypto key in IndexedDB: no script, extension or export can read it and it cannot be copied to another machine; a pre-v0.57.0 office migrates once (same key, private bytes removed); *Retire this office* destroys it. Held by the browser suite. |
| 8 | Chromium treats every `file://` page as one origin, so an app can read another app's `localStorage` keys | Low | **Open, mitigated.** Every app namespaces its keys (`cxla.`, `cxflow.`, `cxst.`, `cxtn.`, `cxpx.`, `aff.`), the notice lists and erases only its own prefix, and imports are sanitized. First-party hosting over https gives each app its own origin. |
| 9 | Federation trust and revocation lists are pasted, not fetched, so identity is confirmed out-of-band | — | **By design.** The signature proves integrity and key possession; identity is confirmed by people. |

## Data map

What each app writes to the browser's `localStorage`, under its prefix.
Nothing is written anywhere else; nothing is sent. Retention is until a
person erases it (one learner, or everything, from the app) or clears the
browser's site data.

| App | Keys | Personal data that may be present |
|---|---|---|
| Louisiana | `cxla.office` (IndexedDB: the non-extractable private key), `cxla.ledger` (learners: name, band, progress counts, access profile ids, flow events, witnessed evidence lines with the assessor's name and note, studio practice runs; the assessor queue), `cxla.roles` (chosen role, current learner id, dashboard layouts, planning notes, assessor name), `cxla.issuer` (the Records Office name and **public** key), `cxla.trust`, `cxla.revoked`, `cxla.revlists` (public keys and record ids of other offices; since v0.62.0 also in IndexedDB `cxla.ledgerdb`, with `cxla.dmeta` holding their save times), `cxla.missions.*`, `cxla.ready.*`, `cxla.theme`, `cxla.style`, `cxla.voice` | Learner names or nicknames; assessor names; free-text notes. Access profiles are chosen supports, never diagnoses. |
| Flow Hub | `cxflow.v1` (per-track skill, completed themes, flow points), `cxflow.draft` (Pack Studio drafts), `cxflow.theme`, `cxflow.voice`, `cxflow.access` | None by design; the session holds no name. |
| Education OS | `aff.*` (the demo learner profile and quest history, view state) | A display name for the demo learner. |
| States | `cxst.state`, `cxst.theme`, `cxst.style`, `cxst.voice` | None. |
| Trades Network | `cxtn.lastrun` (the last studio run's summary), `cxtn.theme`, `cxtn.style`, `cxtn.voice` | None. |
| Platform | `cxpx.theme` | None. The loop runs in page memory only. |

Exports are the only exit and are made by a person: the ledger (JSON),
a `cx-credential/1` record, a `cx-evidence/1` aggregate (consent-gated,
per-track counts, no names), a `cx-simrun/1` studio record, a printed
workbook.

## Regulatory posture

**FERPA (US, 20 U.S.C. §1232g).** The software holds no education record
on behalf of a school: there is no server, no vendor account, no
transmission. A school that keeps the ledger on its own machines holds
its own record under its own policy. The evidence export is aggregate
and consent-gated. The "school official" exception and a data-sharing
agreement are not needed for the software itself; the state layer lists
the agreements a state expects of any tool a district adopts.

**COPPA (US, 15 U.S.C. §§6501–6506; 16 CFR 312).** COPPA governs an
operator's *online collection* of personal information from children
under thirteen. The apps collect nothing online: every keystroke stays in
the browser, and no operator receives it. The notice still asks for a
first name or nickname for younger learners, and nothing asks for a birth
date, contact detail or photograph. An adopter that hosts the apps and
adds any collection of its own takes on COPPA duties at that moment.

**State student-privacy law.** Fifty statutes with differing agreements,
signage and training rules; see the compliance layer per state. The
software's stance — local only, consent-gated aggregate export, no
third-party request — is designed to sit inside every one of them.

**Rights of access, correction and erasure (GDPR-style, and the Education
OS's own rectification-and-erasure stance).** Access: the export box
shows everything. Correction: edit the learner or re-import a corrected
ledger. Erasure: remove one learner, or erase everything the app stored
from the notice. Nobody else can act on the data because nobody else
holds it. A public ledger or on-chain anchor is refused for exactly this
reason (`docs/AGENT_LEARNING.md`, the Education OS's Swarm Architecture
view).

**Accessibility (WCAG 2.2 AA; Section 508; state digital-accessibility
standards).** Audited across 45 views at v0.53.0 and re-run at v0.54.0
with zero WCAG-tagged violations; see [`ACCESSIBILITY.md`](ACCESSIBILITY.md).
The new privacy dialog is a native `<dialog>` with a labelled heading,
keyboard close and focus return.

**Security.** The CSP above; no `eval` or `new Function`; credential
records signed with ECDSA P-256 via WebCrypto with only the public key in
the record; pasted ledgers, trust lists and revocation lists sanitized
before use (`llSanitize`); the studio engine and the notice are shared
code reviewed once and injected everywhere.

**Claims about AI.** No model runs in any app. The "agents", "swarm" and
"tutor" are rule-based automations over the flow state and the ledger;
the Education OS's pages on model-backed coaching and agent
interoperability are design and refusals, and say so. The investor
documents carry the same line (*What the repository proves today*).

**Licensing.** Code Apache-2.0, content CC BY 4.0
([`LICENSING.md`](LICENSING.md)); the four embedded typefaces are SIL
Open Font License 1.1 (`data/fonts/LICENSE-OFL.txt`).

**Securities.** The investor brief, capital-structure memo and deck each
state that nothing in them is an offer to sell securities and that every
term is a proposal until counsel has papered it.

## What remains

- Durable state is complete as of v0.62.0 (ledger, office key, trust and
  revocation lists in IndexedDB with quota failures surfaced; a custody
  bundle restores onto a second device by merge). Two assessor devices
  used at once still reconcile only by exchanging bundles; there is no
  sync service, by design.
- First-party hosting over https, which gives each app its own origin
  (finding 8) and makes the PWA installable; the single file stays the
  primary packaging.
- A written data-processing statement an adopting district can sign, and
  the consent language a family can read — roadmap prompt 10 (the v1.0
  gate materials).
- Counsel's review of this document before any adopter relies on it.
