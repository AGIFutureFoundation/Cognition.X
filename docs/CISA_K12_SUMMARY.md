# CISA K–12 cybersecurity — the vendor summary

> A one-page answer for a district that asks a vendor how its tool sits
> against CISA's *Protecting Our Future: Partnering to Safeguard K–12
> Organizations from Cybersecurity Threats* (January 2023) and the K–12
> Cybersecurity Act guidance. The guidance is voluntary and written for
> districts; this table says which of its recommendations the software
> answers, which the district answers, and where the evidence is.
> Not legal advice. Control ids point at [`CONTROL_REGISTER.md`](CONTROL_REGISTER.md).

## The shape of the answer

Cognition.X apps are single files that run in the browser with **no
server, no account, no network request and no telemetry**. Most of
CISA's recommendations address systems the district operates; for this
tool the district's own device and identity controls are the perimeter,
and the software's contribution is to give the district nothing to
defend beyond the device. The register is the full account.

## CISA's highest-priority steps

| CISA recommendation | Who answers | How | Register |
|---|---|---|---|
| Deploy multi-factor authentication | district | There is no login in the software to protect; MFA applies to the device and any SSO the district puts in front of a hosted copy | PA-01, PL-20 |
| Prioritize patching known exploited vulnerabilities | both | No runtime dependencies to patch; the browser is the runtime and the district patches it; releases are versioned, checksummed and rebuilt from source in CI | PL-05, PL-06, PL-08 |
| Perform and test backups | both | The weekly records-custody bundle is the backup; the district's secured share holds it under its retention schedule | PL-16, ST-07 |
| Minimize exposure to common attacks | software | Browser-enforced CSP (no connection, no eval, no frames, no objects, no workers), no third-party resources, sanitized imports, non-extractable signing key | PL-01, PL-02, PL-03, PL-04, PL-13 |
| Develop and exercise a cyber incident response plan | district | The incident runbook template keyed to the state breach clock; a tabletop run before the first cohort | ST-02 |
| Create a training and awareness campaign | district | Device and data hygiene for hall staff; the parish's or state's annual training where it applies | ST-03 |

## Other recommendations districts commonly ask about

| Topic | Who answers | How | Register |
|---|---|---|---|
| Secure configuration / hardening | software | The same CSP as an HTTP header, HSTS, no cookies, no analytics — the hosting guide; the hosted copy is tested to behave like the file | PL-20 |
| Encryption at rest | district | Full-disk encryption on hall devices (device sheet); the software holds data only in the browser's storage on that device | PA-01 |
| Encryption in transit | software / district | Nothing is transmitted by the software; a hosted copy is served over TLS | PL-01, PL-20 |
| Software bill of materials | software | CycloneDX SBOM generated from the build: the six apps, the four embedded typefaces, the build and test toolchains | PL-08 |
| Vulnerability disclosure | software | `SECURITY.md`: channel, response times, threat model | PL-07 |
| Data minimisation and student privacy | software | First names or nicknames, no identifiers, consent-gated aggregate exports, in-app disclosure and erase | PL-09 to PL-12, FD-01, FD-02 |
| Accessibility | software | WCAG 2.2 AA, zero tagged violations across audited views | PL-14, FD-05 |
| Logging and monitoring | district | The software emits nothing to log; the host's access log (paths and status only) and the device's own logs apply | PL-20 |
| Third-party risk | software | No subprocessors, no hosting, no support tooling that touches data | PL-02 |
| Asset inventory | district | The device sheet lists every hall device and browser profile | PA-01 |

## What to attach when a district asks

1. This page.
2. `docs/CONTROL_REGISTER.md` (the full register with evidence).
3. `SECURITY.md` and `apps/CHECKSUMS.sha256`.
4. `docs/templates/DATA_PROCESSING_STATEMENT.md`, filled in.
5. The SBOM (`sbom/cognitionx.cdx.json`).
