# Security and compliance roadmap — state, parish/county, local and district

> **Not legal advice.** This is an engineering review of the Cognition.X
> apps and the deployment they imply (a parish Trade Hall, a school
> classroom, a program office), measured against the security and
> compliance expectations those bodies actually apply, with a phased
> roadmap and a begin-now checklist. Sources are cited as commonly
> published; verify each with the agency or counsel. The live register of
> controls with status and evidence is
> [`CONTROL_REGISTER.md`](CONTROL_REGISTER.md), generated from
> [`data/policy/controls.json`](../data/policy/controls.json) and checked
> in CI so no control can point at proof that is not there.

Reviewed at v0.57.0. Builds on the app-level review of v0.55.0
([`COMPLIANCE_REVIEW.md`](COMPLIANCE_REVIEW.md)) and the fifty-state
deployment layer of v0.51.0 ([`STATE_COMPLIANCE.md`](STATE_COMPLIANCE.md)).

## 1. What was reviewed, and how

Four layers, because that is how a public body will ask the question:

| Layer | Who asks | What they ask |
|---|---|---|
| **The software** | a district IT office, a vendor-risk questionnaire | does data leave, can it be altered, who can sign, is the file what you shipped, who do we call |
| **State** | the state education agency, the attorney general, the labor department, the fire marshal | student-privacy statute and agreement, breach notification, child-labor hazardous occupations, background checks, mandated reporting, public records, accessibility |
| **Parish / county** | parish IT, risk management, the fire marshal, the council | device and acceptable-use policy, encryption and backup, occupancy and egress, insurance, an MOU |
| **Local and district** | the school board, the principal, the city clerk | data-governance policy and the DPA, the security questionnaire, supervision ratios, facility permits, transcript recognition |

Method: the software was read and exercised (every network path, every
storage key, every signing path, every input that accepts pasted data);
each law or policy was mapped to what the software does and to what an
adopter must do; every claim the register makes about the software is
tied to a test, a browser check, a CI step or a file that the register
generator confirms exists.

## 2. Findings — where the system stands

**The software's posture is strong and mechanically held.** No egress
(browser-enforced CSP), no third-party resource, no eval, local-only
storage with an in-app disclosure and erase control, consent-gated
aggregate exports, signed offline-verifiable records, sanitized imports,
WCAG 2.2 AA, reproducible builds. As of this release: a **non-extractable
signing key** (the one medium finding left open by v0.55.0), **release
checksums** an adopter can verify, a **vulnerability-disclosure policy**,
and **youth hazard-order lines** on every trades scenario.

**The gaps are on the adopter's side of the line, and the software did
not yet help enough with them.** A hall or district must still: sign the
state's data agreement and a DPA; name an incident lead and know the
state's breach clock; keep records under a retention schedule; keep
minors off hazardous-occupation tasks and hold the student-learner
agreements; run background checks and mandated-reporter training; get
the room past the fire marshal; confirm insurance; put an MOU on an
agenda. Until this release, none of that had a template, a checklist or
a number in the software. Now the fifty-state layer carries the breach
statute for every state, three templates exist (data-processing
statement, incident runbook, records custody), and the register names
each item with an owner and a next step.

**What remains open in the software itself** (register status *partial*
or *open*): signed release tags once a signing key is provisioned; trust
and revocation lists still in local storage. Wave 2 is otherwise
complete: the durable ledger, the custody bundle and the hall checklist
(v0.58.0); the hosting guide with a hosted-copy test, the CycloneDX SBOM
and the CISA K–12 vendor summary (v0.59.0).

Counts from the register at v0.59.0: 44 controls — 28 met, 13 partial,
3 open. Every open item has a wave and an owner below.

## 3. Recommendations

Ordered by how much risk they retire per unit of work.

1. **Treat the device as the perimeter.** Everything the software
   protects can be undone by an unlocked, unencrypted, shared laptop.
   Parish or district device policy — full-disk encryption, auto-lock,
   one browser profile per assessor, no shared logins — is the single
   most valuable control and costs nothing in code.
2. **Make the weekly export the backup and the record.** Local storage
   is not a system of record. Export the ledger and the issued records to
   the body's secured share on a schedule; that export is also the
   records-custody mechanism and the answer to a public-records request.
3. **Name the incident lead before the first cohort, and learn the
   state clock.** The realistic incident is a lost device or a
   misdirected file. Fill the runbook; the fifty-state layer gives the
   statute, the deadline and the regulator line for every state.
4. **Sign the paper the district already uses.** Attach the
   data-processing statement to the district's own DPA (the SDPC national
   form in most states) rather than inventing a new agreement; the
   statement answers its exhibits.
5. **Post the youth line at every station.** The hazardous-occupation
   orders are federal law; the studio law already keeps energized,
   suspended and moving work out of the room. The station sheet should
   say which HO applies and whether a written student-learner agreement
   exists.
6. **Keep the honest claims honest in procurement.** Simulation is not
   certification; credentials are recognised on a transcript by district
   decision; the union hall certifies. The register's *governance* rows
   are the vendor's answer when a buyer asks.
7. **Do not host until the hardening guide exists.** The single file is
   the primary packaging and is safest. When a district wants a URL, the
   same CSP as an HTTP header, TLS, HSTS and no analytics, with a check
   that the hosted copy behaves like the file.
8. **Ask counsel to read the register once.** Everything here is
   engineering; a one-hour review by the district's or foundation's
   counsel turns it into something a board can rely on.

## 4. The roadmap

### Wave 1 — this release (v0.57.0): the register and the first controls

| Item | Owner | Artifact | Status |
|---|---|---|---|
| Control register with checked evidence | software | `data/policy/controls.json`, `docs/CONTROL_REGISTER.md`, CI | done |
| Non-extractable Records Office key with migration and *Retire this office* | software | Louisiana app; `testOfficeKeyNonExtractable` | done |
| Release checksums and a security policy | software | `apps/CHECKSUMS.sha256`, `SECURITY.md`, CI | done |
| Breach-notification domain for all fifty states | software | `data/states/compliance.json`, States app lens and checklist, Louisiana State Admin, `STATE_COMPLIANCE.md` | done |
| Youth hazard-order lines on every trades scenario, shown in the studio | software | `data/simulations/scenarios.json`, engine | done |
| Adopter templates: data-processing statement, incident runbook, records custody | software | `docs/templates/` | done |

### Wave 2 — next two releases: durable state, hosting, provenance

| Item | Owner | Acceptance |
|---|---|---|
| Ledger and queue in IndexedDB behind the existing accessors, one-time migration, quota errors surfaced (roadmap prompt 9) | software | **done, v0.58.0** — a 400-learner ledger saves and reloads; a simulated quota failure is reported and the ledger reloads from IndexedDB; `testDurableLedger` |
| One-click records-custody bundle (ledger + office public key + trust and revocation lists + checklists, dated) | software | **done, v0.58.0** — exports from the Records Office and Parish Admin; never the private key; the custody statement names it |
| Trust and revocation lists on the same durable path; restore from the custody bundle on a second device (roadmap prompt 9, close-out) | software | **done, v0.62.0** — the lists migrate once and survive a quota failure; *Restore (merge)* in the Records Office merges learners by id, trusted offices second-hand, revocation lists re-verified, an office by name and public key only; `testDurableListsAndRestore` |
| `docs/HOSTING.md` with header examples; a Playwright check against a hosted copy | software | **done, v0.59.0** — nginx, Apache and Caddy examples; `testHostedCopy` serves the apps over HTTP and runs the same CSP, no-request and font checks, or `CX_HOSTED_BASE` for a real host |
| CycloneDX SBOM from the build; signed release tags | software | **SBOM done, v0.59.0** — `tools/sbom.py`, `sbom/cognitionx.cdx.json`, CI-diffed; signed tags wait on a signing key |
| Hall safety & compliance checklist: the thirteen wave-3 operating controls per parish, exported with the bundle | software | **done, v0.58.0** — in the parish dashboard and Parish Admin; the register's adopter controls carry it as evidence and move from *open* to *partial* |
| CISA K–12 vendor summary table | software | **done, v0.59.0** — `docs/CISA_K12_SUMMARY.md` |

### Wave 3 — the adopter's operating controls (first cohort)

| Item | Owner | Acceptance |
|---|---|---|
| Device sheet adopted: encryption, auto-lock, one profile per assessor, weekly export | parish / district IT | signed device sheet on file; first export on the share |
| DPA signed with the data-processing statement attached; apps listed as approved offline tools | district | the district's approved-tools list names the apps |
| Incident runbook filled; incident lead named; state clock recorded | program office | printed copy at the hall; one tabletop run with staff |
| Records custody statement signed; retention series mapped | custodian | statement on file; first scheduled erase date set |
| Background checks and mandated-reporter training logged for every assessor and mentor | hall | check log complete before the first session |
| Fire-marshal walkthrough; occupancy posted; extinguishers matched to stations; insurance confirmed in writing | parish | walkthrough report on file; certificate of insurance |
| MOU between program office, parish and district on the room, the schedule, custody and the incident line | all three | signed MOU; on the council and board agendas |
| Youth lines posted at every station; student-learner agreements held where an exemption is used | hall | station sheets posted; agreements in the hall file |

### Wave 4 — recognition and review

| Item | Owner |
|---|---|
| Credential list to the review board and the district's CTE office together (transcript recognition) | board / district |
| Counsel's review of this document and the register | foundation / district counsel |
| Annual re-run of the accessibility audit, the app compliance review and this register; PATCH release for any corrected fee, statute or deadline | software |

## 5. Begin now — a Louisiana parish pilot in ten steps

1. Open the States app → Compliance → Louisiana, export the checklist, and read the breach row with the incident lead.
2. Print the three templates; fill the bracketed fields at one sitting with the parish IT contact and the district's data-privacy officer.
3. Adopt the device sheet (recommendation 1) for every hall laptop; verify encryption and auto-lock on each.
4. Create the Records Office on one controlled device; publish its public key to the trust list; read the message that the key cannot be copied.
5. Verify the hall's app files against `apps/CHECKSUMS.sha256`.
6. Post the studio law and the youth line at every station; file any student-learner agreements.
7. Log background checks and mandated-reporter training for every adult.
8. Fire-marshal walkthrough; occupancy posted; insurance confirmed in writing.
9. Put the MOU on the next parish and board agendas with the register attached.
10. Run one tabletop incident from the runbook with staff, then enrol the first cohort.

## 6. Keeping it current

The register is data. When a statute, fee or deadline changes, correct
the JSON, run `tools/controls_report.py` and `tools/compliance_report.py`,
and ship a PATCH release; the tests hold the shape, and CI refuses a
register whose evidence is missing.
