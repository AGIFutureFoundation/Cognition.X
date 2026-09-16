# Data-processing statement — Cognition.X apps

*A statement an adopting district, hall or program office can attach to its own data-privacy agreement (for example as the technical exhibit of an SDPC-style agreement). It describes the software as built and tested at the version in the footer of each app. Not legal advice; the district's own policy and its state's statute govern. Fill the bracketed fields.*

**Adopter:** [district / parish / program office] · **Contact:** [name, role] · **Apps in use:** [Louisiana / Flow Hub / States / Trades Network / Platform / Education OS] · **Version:** [from the app footer] · **Date:** [ ]

## 1. What the software is

Single-file HTML applications that run in a web browser on the adopter's own devices. There is no vendor server, no account, no login, no synchronisation and no telemetry. The maintainer (AGI Future Foundation) receives nothing from any deployment.

## 2. What data exists, and where

| Data | Where it lives | Who can reach it |
|---|---|---|
| Learner ledger (first name or nickname, band, progress counts, chosen access supports, witnessed-check evidence lines with the assessor's name and note, studio practice runs) | The browser's local storage on the device in use, under the app's namespaced keys | Whoever can use that device and browser profile |
| Records Office keys | The public key in local storage; the private key as a non-extractable key in the browser's IndexedDB — it cannot be read, exported or copied to another machine | Signing only, from that browser profile |
| Trust and revocation lists (other offices' public keys and record ids) | Local storage | As above |
| Exports (ledger JSON, signed credential records, aggregate evidence, studio run records, printed workbooks) | Wherever the person who exported them puts them | The people they are sent to |

No data element is a legal name, a date of birth, a contact detail, a photograph, a government identifier or a disciplinary or health record. Access supports are chosen supports, never diagnoses.

## 3. Transmission

None occurs. Every app carries a Content-Security-Policy that instructs the browser to refuse every connection; typefaces are embedded; no referrer is sent on outbound links. This is verified by automated tests on every release and can be verified by the adopter by opening an app with the browser's network panel visible.

## 4. Disclosure, access, correction and erasure

- **Disclosure** happens only when a person exports a file and sends it. Aggregate evidence exports are behind a consent step and carry per-track counts, never names.
- **Access:** the export box shows every stored value; the Data & privacy notice in each app lists every key and its size.
- **Correction:** edit the learner in the app, or re-import a corrected ledger.
- **Erasure:** remove one learner, or *Erase everything this app stored in this browser* from the notice; the private key of a Records Office is destroyed by *Retire this office*.

## 5. Security measures

Content-Security-Policy (no connections, no eval, no frames, no workers); no third-party code or resources; ECDSA P-256 signatures on credential records with offline verification and tamper detection; non-extractable signing key; sanitisation of any pasted data; reproducible builds and SHA-256 release checksums (`apps/CHECKSUMS.sha256`); a published vulnerability-disclosure policy (`SECURITY.md`); WCAG 2.2 AA with zero tagged violations across audited views.

## 6. Subprocessors

None. There is no hosting, no analytics and no support tooling that touches data.

## 7. Retention and deletion

Data persists on the device until erased by a person or by clearing the browser's site data. The adopter's own retention schedule governs any exported file; see the records custody statement.

## 8. Breach

Because nothing is transmitted or hosted, a breach is a lost or stolen device, an unlocked screen, or an export sent to the wrong recipient. The adopter's incident runbook (template provided) names the incident lead, the district's reporting line and the state's notification clock.

## 9. Changes

The software changes only by versioned release; the changelog and this statement are updated together. The adopter is not notified automatically, because the software has no channel to do so; check the repository or the footer version.

Signed for the adopter: ____________________ Date: ________
