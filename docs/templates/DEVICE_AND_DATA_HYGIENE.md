# Device and data hygiene for hall staff — one page

*Template for a Trade Hall, school or co-op running Cognition.X. Read it, sign the line at the bottom, keep the sheet with the hall's records. It is the software-side answer to register item ST-03 (state and local cybersecurity training) and the practice behind PA-01 (the device sheet); a parish employee also takes the parish's own annual course, and that course governs where the two differ. Not legal advice.*

**Hall:** [ ] · **Device sheet owner:** [name] · **Incident lead:** [name, phone] · **Version of the apps:** [from the footer]

## What is on the device, and why it matters

The apps keep everything on the device: learners' first names or nicknames, bands, progress counts, witnessed evidence lines with the assessor's name and note, the Records Office public key, and the trust and revocation lists. Nothing is sent anywhere by the app and the browser blocks it. That means the device *is* the record. Lose the device and you have lost the hall's records since the last export; let someone else use your browser profile and they can read every learner's line and sign records in the office's name.

## Ten rules, in the order they come up

1. **Encryption on, lock in five.** Full-disk encryption switched on; auto-lock at five minutes; a passcode or password, never a shared one. Lock it when you step away, every time.
2. **One profile per assessor.** Your browser profile is your signature. Never assess from someone else's profile and never lend yours. The Records Office key lives in one profile on one device and cannot be copied; that is by design.
3. **No accounts, no sync.** Do not sign the browser into a cloud account that syncs site data, and do not install browser extensions on a hall device. An extension can read any page it likes.
4. **Export weekly, to the parish share.** Parish Admin → *Export records-custody bundle* → the hall's secured share. The bundle is the backup and the public record. Verify the file opened. Never e-mail it to a personal address.
5. **Restore only by merge.** A second device takes up the records through Records Office → *Restore (merge)* from the latest bundle. Nothing else copies records between devices; do not try.
6. **What leaves, leaves by hand.** The only files that ever leave are a learner's signed credential, the custody bundle, and (only if the hall opts in) the aggregate evidence count with no names in it. Check the recipient before you send any of them; send the bundle only to the parish share.
7. **Keys change hands out-of-band.** Another office's public key is added to the trust list only after you confirm the office name and the first characters of the key with that office by voice or in person. A key in an e-mail is not confirmed. The software cannot do this step for you.
8. **Learners' lines are the learners'.** A learner or family may ask to see, correct or erase what is recorded; the Data & privacy control in the app shows every value and erases one learner or everything. Do it while they watch; do not export a learner's data to answer the request.
9. **Screens face the room.** Assessment happens with the device visible to the learner, never with a screen turned away; nothing about a learner is recorded that the learner cannot see.
10. **Lost, stolen, misdirected: the first hour.** A missing device, a bundle sent to the wrong address, a profile used by the wrong person: tell the incident lead now and open the incident runbook (`INCIDENT_RESPONSE_RUNBOOK.md`). The state's breach clock starts at discovery, and the runbook says who must be told and by when.

## Once a year

- Re-read this sheet and re-sign. Confirm encryption and auto-lock on every hall device. Rotate any device passcode that more than one person has known.
- Parish employees: complete the parish's annual cybersecurity course as well; where its rules are stricter, they win.
- Check `sha256sum -c apps/CHECKSUMS.sha256` on the release the hall runs, and update the version in the header of this sheet.

## Sign-off

I have read the ten rules and I run the hall's devices this way.

Name: ____________________ Role: ____________ Date: ________

Device sheet owner: ____________________ Date: ________

*From the security and compliance register (`docs/CONTROL_REGISTER.md`, ST-03, PA-01, ST-02) and the CISA K–12 summary (`docs/CISA_K12_SUMMARY.md`, training and awareness). Not legal advice.*
