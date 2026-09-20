# SOC 2 and COPPA — enterprise-readiness crosswalk

> **This is not a SOC 2 report, and this document cannot produce one.**
> SOC 2 is an attestation about an *organization's* controls over a
> *system* during an observation period (typically six to twelve months),
> issued by an independent, licensed CPA firm after a Type I or Type II
> engagement. No repository, codebase or vendor can self-certify SOC 2
> compliance; `docs/INVESTOR_BRIEF.md` names "SOC 2 compliant" as a claim
> to avoid before that engagement exists. What this page does instead:
> maps the AICPA's five Trust Services Criteria (TSC, 2017) to what the
> software already does, states plainly which criteria have no scope
> today because there is no operated service, and names exactly what a
> hosted tier would need before an auditor could be engaged. Not legal
> or accounting advice — a CPA firm licensed for SOC 2 engagements makes
> the actual determination. Control ids point at
> [`CONTROL_REGISTER.md`](CONTROL_REGISTER.md).

## Why SOC 2 has no scope today

SOC 2 audits controls over a *system a service organization operates* —
the boundary is normally a hosted application, its infrastructure, and
the company's operational processes around it. Cognition.X ships as six
single HTML files with **no server, no account, no hosting, and no
company-operated system to draw a boundary around**
([`SECURITY.md`](../SECURITY.md)). A school or hall that downloads a file
and opens it locally is not a customer of a service; there is nothing
running that a CPA firm could observe operating correctly over a period
of months, because nothing runs anywhere but the reader's own browser.
This is the same reason the platform has no SOC 2 scope that
`docs/INVESTOR_BRIEF.md` names, stated here in full rather than one line.

That does not mean the underlying intent of the five criteria is
unaddressed — most of it is already met by the software's design, for
the same reason FERPA and COPPA are not triggered
([`COMPLIANCE_REVIEW.md`](COMPLIANCE_REVIEW.md)): a control that protects
data *in a service* is moot when the data never leaves the reader's
device to reach a service in the first place.

## The five Trust Services Criteria, mapped

| Criterion | What it asks of a service organization | Cognition.X today | Register |
|---|---|---|---|
| **Security** (the Common Criteria; required in every SOC 2 report) | Logical and physical access controls, system monitoring, incident response, change management, and risk mitigation over the operated system | No accounts to protect, no server to monitor, no infrastructure to change-manage. What *does* transfer — the release itself — is checksummed, rebuilt byte-for-byte from source in CI, and has a published vulnerability-disclosure channel and response commitment | PL-01, PL-03, PL-05, PL-06, PL-07, PL-08, PL-13 |
| **Availability** | The system is available for operation and use as committed (uptime, capacity, disaster recovery) | No uptime commitment exists because nothing is hosted by the platform; a file either opens in a browser or it doesn't. A district that self-hosts owns its own availability, same as any static file it serves | PL-06, PL-20 |
| **Processing Integrity** | System processing is complete, valid, accurate, timely and authorized | The only "processing" is client-side JavaScript computing from what a person entered; the credential-signing and threshold logic is deterministic and covered by the test suite, but there is no server-side transaction pipeline for a SOC 2 engagement to test | PL-15, PL-18 |
| **Confidentiality** | Information designated confidential is protected from unauthorized disclosure | Nothing designated confidential is transmitted anywhere by the software; it stays in the browser's local storage under a namespaced key until a person exports or erases it | PL-02, PL-09, PL-13 |
| **Privacy** | Personal information is collected, used, retained, disclosed and disposed of per the entity's privacy commitments (this criterion maps closely to FERPA/COPPA intent) | Covered in full by the FERPA and COPPA analysis already in `COMPLIANCE_REVIEW.md`: no online collection, in-app disclosure of every key stored, consent-gated aggregate export, access/correction/erasure all in the reader's own hands | PL-09, PL-10, PL-11, PL-12, FD-01, FD-02 |

## What would actually bring SOC 2 into scope

None of the following is buildable in this repository alone — they are
organizational commitments a company makes once it operates a hosted
service, and they are named here so the gap is honest rather than
implied-away:

1. **A hosted, multi-tenant (or even single-tenant managed) service** —
   the precondition for any SOC 2 scope at all. `docs/HOSTING.md` covers
   a district hosting the static files themselves, which does not create
   this precondition; the district is the operator of its own copy, not
   a customer of a Cognition.X service.
2. **Formal, versioned policies** an auditor tests against: an access
   control policy, a change-management policy, an incident-response
   policy (a runbook template exists for adopters —
   [`docs/templates/INCIDENT_RESPONSE_RUNBOOK.md`](templates/INCIDENT_RESPONSE_RUNBOOK.md)
   — a company running a hosted service needs its own, company-facing
   version), a vendor-management policy, and a business-continuity plan.
3. **An observation period** (Type II) during which the company
   demonstrates the above policies were actually followed — logs,
   tickets, access reviews, a change log with approvals. This cannot
   pre-exist before the service does.
4. **An independent CPA firm licensed for SOC 2 engagements**, engaged
   to test the above and issue the report. Cost and timeline are the
   firm's to quote; this is a commercial engagement, not an engineering
   task.
5. **A defined system boundary and trust-services scope decision** —
   which of the five criteria beyond the mandatory Security category the
   company commits to (most SaaS reports add Availability and
   Confidentiality; Privacy is added when personal data is processed by
   the service itself, which would be new for Cognition.X).

The honest sequencing: item 1 must exist before items 2–5 are anything
but paperwork with no system to test against.

## COPPA, extended: if a hosted tier ever collects data

`COMPLIANCE_REVIEW.md` and control FD-02 already establish that no
operator collects anything online today, so COPPA's
verifiable-parental-consent (VPC) requirement is not triggered. If a
future hosted tier adds
any collection from a user the operator has actual knowledge is under
13 — a login, a hosted ledger, cloud sync — VPC would become a real
requirement before that collection could occur. The FTC's currently
accepted VPC methods (16 CFR 312.5(b)) are, so this is scoped correctly
if that day comes:

| Method | Shape |
|---|---|
| Signed consent form | Parent signs and returns by mail, fax, or scanned upload |
| Government-ID verification | Parent's ID checked against a database, then deleted promptly |
| Trained-staff phone line | Toll-free number, parent calls a trained representative |
| Trained-staff video call | Parent verified over video by a trained representative |
| Payment-system verification | A monetary transaction (even $0) with notice to the payment method's holder |
| Knowledge-based authentication | A dynamic, multi-question identity challenge the parent answers |
| Facial-recognition match to a photo ID | With the same prompt-deletion requirement as ID verification |

Two things narrow this further for a school-facing tool: (1) the FTC's
COPPA guidance recognizes a **school-consent exception** — a school may
consent on a parent's behalf for services used solely for an educational
purpose, in which case the *service agreement with the school* (not
individual VPC per family) is the operative document, closely mirroring
FERPA's "school official" analysis already in `COMPLIANCE_REVIEW.md`;
and (2) COPPA's data-minimization and retention-limit duties (collect
only what's needed, delete when no longer necessary) are already the
platform's stance by design (`PL-12`) and would simply carry forward into
any hosted service that reuses the same schema. Neither point is legal
advice; a hosted tier's actual consent mechanism is a decision for
counsel and the operating company, not this document.

## What to attach when asked "are you SOC 2 compliant?"

1. This page — the honest answer is "not yet in scope; here is exactly
   why, and here is what would bring it into scope."
2. [`CONTROL_REGISTER.md`](CONTROL_REGISTER.md) — the controls that
   already satisfy each criterion's intent by design.
3. [`SECURITY.md`](../SECURITY.md) and
   [`apps/CHECKSUMS.sha256`](../apps/CHECKSUMS.sha256) — the release
   integrity story an auditor or a security-questionnaire reviewer asks
   for first.
4. [`CISA_K12_SUMMARY.md`](CISA_K12_SUMMARY.md) — the same crosswalk
   exercise already done for K–12 cybersecurity guidance.
