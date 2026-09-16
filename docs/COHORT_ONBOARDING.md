# Running a cohort — the onboarding path

> For a hall, a class or a co-op that has never seen this repository:
> how to enrol a cohort on an unmodified release, what families are
> asked to agree to (and exactly what the software does), how records
> offices exchange keys, and what evidence leaves, when, and by whose
> hand. Every claim here matches the code and is held by the tests. Not
> legal advice; your district's and state's rules govern — the
> fifty-state layer in the States app lists them, and the hall safety &
> compliance checklist in the Louisiana app tracks the thirteen
> operating controls before enrolment.

## 0. Before the first learner (one afternoon)

1. **Get the release.** Download the apps from the repository at one
   version; verify them: `sha256sum -c apps/CHECKSUMS.sha256`. Do not
   modify a file — the v1.0 gate requires an *unmodified* release, and a
   modified file fails the checksum.
2. **Meet the operating controls.** Open the Louisiana app → Parish
   Admin → *Hall safety & compliance* and work the thirteen controls
   (device sheet, weekly export, incident lead, DPA, records custody,
   background checks, fire marshal, insurance, OSHA 10, youth lines,
   employment certificates, two-adult rule, MOU). The templates for the
   paper are in `docs/templates/`.
3. **Create the Records Office** on one controlled device: Parish Admin
   → *Records Office* → name it → *Create office keys*. The private key
   is non-extractable and lives only in that browser profile; the
   public key is what you publish. Write the office name and the
   device on the custody statement.
4. **Choose the tracks.** A cohort runs one full track to the credential
   (fifty witnessed checks). Pick from the thirty core-spine tracks the
   ledger credits; each carries a rubric an assessor reads in Assessor
   Mode.
5. **Train the assessors** on the three-line rubric and the track
   rubric: *real material · independent at band · would transfer*. The
   honest witness records *not yet*. (Parish Launch & Scale, *Training
   the trainers*.)

## 1. Enrolment (five minutes per learner)

- In the Louisiana app, Student → *My standing* → *Add me — a first name
  or nickname*. That is all the software asks for: no legal name, birth
  date, contact detail or photograph, anywhere.
- Choose the band with the learner (K–2 … 11–12 · adult) and, if the
  learner wants them, the access supports — chosen supports, never
  diagnoses; they change the *format* of a check, never the bar.
- Give the family the consent sheet (`templates/CONSENT_FORM.md`). It
  says what the software does, in plain words, and it is accurate
  because the tests hold the software to it:

  > Everything the app records stays on the hall's device. Nothing is
  > sent anywhere by the app. The only things that ever leave are files
  > a person exports on purpose: a signed credential for your learner,
  > a records-custody copy for the hall's own files, and — only if the
  > hall opts in — an aggregate count per track with no names in it,
  > for the curriculum review board.

- Keep the signed sheet with the hall's records; the ledger does not
  store it and does not need to.

## 2. The cohort runs (one track, eight to twelve weeks)

- Learners work the track in flow sessions; practice checks go in the
  learner's own log; a **witnessed** check is requested from *My
  standing* and confirmed by an assessor in Assessor Mode against the
  rubric. At exactly fifty checks the credential fires; no button awards
  it.
- The studio (*Simulation studio* widget) is rehearsal: a kept run is
  practice, never a check.
- **Weekly:** Parish Admin → *Export records-custody bundle* → the
  hall's secured share. That file is the backup and the public record.
- **If a device is lost or a file is misdirected:** the incident
  runbook, from the first hour.

## 3. Key exchange between records offices (federation)

Two halls that want to verify each other's records by name exchange
public keys **out-of-band** — the software never fetches a key.

1. Hall A: Records Office → *Show public key* → copy the JSON
   (`recordsOffice`, `publicKey`).
2. Hall A sends it to Hall B by a channel the two already trust
   (in person, the district's mail, a phone call to read the first
   twelve characters of `x` aloud).
3. Hall B: Records Office → paste under *Add trusted office* →
   confirm the office name and the first characters of the key with
   Hall A by voice or in person, **then** add. That confirmation is
   the whole security of the trust list; the software cannot do it.
4. Repeat in the other direction. Either hall may *Export trust list*
   for a third hall; imported entries are marked second-hand until
   confirmed the same way.
5. A record signed by a trusted office now grades *trusted by name*.
   Without the exchange it grades *valid, key not trusted* — still
   unaltered and holder-signed, identity unconfirmed.
6. Revocation: an office that issued a record in error revokes it by
   id and exports a signed `cx-revocation/1` list through the same
   channel; verifiers import it and the record grades *revoked*, which
   outranks trusted.

## 4. Issuing the credential

When a learner reaches fifty, the Records Office issues the record:
*Issue signed record* (the native `cx-credential/1` JSON) or *Issue as
Open Badge 3.0* (a `vc+jwt` a wallet can hold). Both state on their
face how many of the fifty checks an assessor witnessed. Hand the file
to the learner; keep a copy with the custody bundle. Anyone can verify
it offline — in the app, or with `node tools/verify_record.js`.

## 5. Evidence for the review board (opt-in, aggregate, by hand)

- At the end of the track: Teacher → *The evidence loop* → read the
  preview → tick *I choose to export this aggregate* → *Export
  cx-evidence/1*. The file holds per-track counts only: checks
  recorded, witnessed confirmed and not-yet, learners as a number. No
  names, no ids, no per-learner rows.
- A person sends the file to the board. The app cannot.
- The board runs `python3 tools/cohort_report.py <files>` and reads
  the packet: revision priorities, unreported tracks, the queue status
  of the packs the cohort used, and the v1.0 gate status.

## 6. The v1.0 gate

The cohort has done its part when: it ran on an unmodified release
(checksums match); at least one learner holds a signed credential for a
full track; the office exchanged keys with at least one other office;
and its opt-in evidence reached the board through one full track. The
board's part is to have reviewed the packs the cohort used
(`BOARD_PACKET.md`). Then v1.0 is cut.
