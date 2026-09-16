# Incident response runbook — a hall, school or program office running Cognition.X

*Template. Fill the bracketed fields before the first cohort and keep a printed copy at the hall. Not legal advice; the state's statute and the district's policy govern, and both change — verify the clock with the attorney general's published guidance.*

**Incident lead:** [name, phone] · **Deputy:** [ ] · **District / parish reporting line:** [who, how, within how long] · **Counsel:** [ ] · **State clock:** [from the fifty-state compliance layer — e.g. Louisiana: residents within 60 days of discovery; Attorney General within 10 days of notifying residents]

## What an incident is here

The apps hold data only on the device in use and transmit nothing. An incident is therefore one of:

1. A device that ran the apps is lost, stolen or taken by someone without authority.
2. A device was left unlocked where someone could read or export the ledger.
3. An exported file (ledger, credential record, evidence aggregate) was sent to the wrong recipient or posted where it should not be.
4. A Records Office signed something it should not have (compromised profile, coerced assessor).
5. Someone reports that a file claiming to be a Cognition.X app is not the released file.

## First hour — contain

- Write down the time of discovery. **The clock starts now.**
- For a lost device: use the device-management tool to lock or wipe it if the parish or district has one; change any password that unlocks it.
- For an unlocked device: lock it; note who had access and for how long.
- For a misdirected file: ask the recipient in writing to delete it and confirm; keep the reply.
- For a compromised office: open the Louisiana app on the office's device, *Retire this office* (destroys the private key), create a new office, and publish a **revocation list** for any records signed in the window; publish the new public key to every hall on the trust list.
- For a suspect file: compare its SHA-256 with `apps/CHECKSUMS.sha256` at the same version; if it differs, stop using it and report it under `SECURITY.md`.

## First day — assess

- What was on the device or in the file? The Data & privacy notice lists the keys; the ledger export shows the values. Count the learners named.
- Was the ledger demo data (seeded learners say so on their face) or real people?
- Does the data meet the state statute's definition of personal information? A first name or nickname with progress counts usually does not; a full name with any identifier may. Counsel decides.
- Record every fact in the incident log with times.

## First week — notify

- The district's or parish's own reporting line first, within its internal clock.
- Families of any named learner, plainly and in writing, within the state's outer limit or sooner; say what was in the file, what it was not, what was done, and whom to call.
- The state regulator where the statute requires it (Louisiana: the Attorney General within 10 days of notifying residents, if residents were notified).
- The other halls on the trust list, if an office was retired or a revocation list issued.

## Afterwards — learn

- Add the incident to the hall's session record and the next board packet.
- Fix the control that failed: device encryption and auto-lock, one browser profile per assessor, a weekly export to the parish's secured share and nowhere else.
- Re-run the studio's *Seventy-two hours out* and *The boil-water notice* scenarios with staff — the disciplines are the same: verify, say it out loud, escalate.

## Contacts

| Who | Name | Phone | E-mail |
|---|---|---|---|
| Incident lead | | | |
| District data-privacy officer | | | |
| Parish IT | | | |
| State attorney general (breach notice) | | | |
| Maintainer (security reports only) | AGI Future Foundation | — | security@agifuturefoundation.org |
