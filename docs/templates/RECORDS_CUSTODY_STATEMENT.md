# Records custody statement — a public body running Cognition.X

*Template for a parish, district or other public body. Not legal advice; the state's public-records law and the body's adopted retention schedule govern. In Louisiana: R.S. 44:1 et seq. and the schedules approved by the State Archives.*

**Custodian:** [office, name] · **Body:** [parish / district] · **Devices and browser profiles that hold ledgers:** [list] · **Secured share for exports:** [path or system] · **Retention schedule applied:** [schedule name and series]

## 1. What is a record here

When a public body's staff record witnessed checks, issue signed credential records or keep a learner ledger in a Cognition.X app on the body's devices, those are the body's records. The software holds nothing on anyone's behalf; the body is the custodian from the first entry.

## 2. Where the records are

- The **ledger** in each device's browser local storage (`cxla.ledger` in the Louisiana app), listed by the app's Data & privacy notice.
- **Issued credential records** wherever the office saved them when issued; each is a signed JSON file that verifies offline.
- **Exports** (ledgers, evidence aggregates, studio run records, compliance checklists, printed workbooks) on the secured share named above.

## 3. Custody practice

1. Export the ledger from every device to the secured share on a fixed schedule: [weekly].
2. Keep issued credential records with the ledger export of the same date.
3. Keep the office's **public** key and every published trust and revocation list with the records; the private key is non-extractable by design and is not a record.
4. Apply the retention series to the exports; when the series expires, erase the device copies from the app's notice and delete the exports under the schedule.
5. On a public-records request, produce from the exports with student information redacted as the district's FERPA policy requires; the export format is plain JSON and prints.
6. On a litigation or audit hold, stop the erase step and note the hold here: [ ].

## 4. What the records do not contain

No legal names are required (first names or nicknames), no birth dates, contact details, photographs, health or disciplinary information. Access supports are chosen supports, not diagnoses. A credential record states how many checks were witnessed by an assessor and how many were the learner's own practice log.

## 5. Integrity

Every credential record carries an ECDSA signature and the issuing office's public key; anyone can verify it offline, and one changed character invalidates it. Release files are verified against `apps/CHECKSUMS.sha256`.

Custodian: ____________________ Date: ________
