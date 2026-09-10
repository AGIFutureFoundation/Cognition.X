# Agent & Robot Learning — architecture and data principles

Every Cognition.X block ends with a human doing something real. This
document defines how those interactions can — **with consent, and only
with consent** — also train learning agents and robots, and how the
flow-state engine doubles as a machine curriculum scheduler.

## One block, two learners

```
Human learner → Transfer check (real material)
             → Consented trace (CX-Trace v1, local first)
             → Agent / robot curriculum (flow-paced)
             → Assistance returned in class & Trade Hall → …
```

The human earns the credential. The machine, when a trace is
deliberately exported, learns from how it was done. Any machine trained
on community traces must serve back into the same community's
classrooms and Trade Halls — the learner is paid in capability.

## Machine-learnable signals per module

| Signal | What it is | Learning use |
|---|---|---|
| Demonstration | Step order, manipulation, phrasing on real material | Imitation learning |
| Correction | "Not like that" moments from learners and assessors | Negative examples / preference data |
| Pacing | Real time-per-band for humans | Curriculum difficulty ground truth |
| Boundaries | Steps humans refuse or escalate | Safety limits from practice |
| Flow telemetry | Breezed / in-flow / struggled on the skill–challenge plane | Reward shaping |

## Flow state as machine curriculum

Curriculum learning is the flow channel by another name: serve tasks
just above demonstrated competence (challenge within `skill −0.6 …
+1.1`), ease off on failure, advance on mastery. A robot trained on
module traces climbs the human ladder: **Explorer** (observe &
classify) → **Builder** (assist on subtasks) → **Practitioner**
(perform under supervision) → **Lead** (teach back, flag exceptions).

## CX-Trace v1

The export format the Flow Hub Archivist produces (Ledger → *Copy
training trace*):

```json
{
  "format": "cx-trace/1",
  "version": "0.10.0",
  "sessions": [{"track": "HOUSING/HS",
                "moves": [{"skill": 2.4, "challenge": 3.0}]}],
  "checks":   [{"track": "HOUSING/HS", "theme": 2, "band": "6–8"}],
  "consent":  {"share": false, "anonymized": true}
}
```

Rules: no identity fields, ever; `consent.share` defaults to `false`
and is flipped only by the person exporting; the ledger (credentials)
and the trace (skill signals) are separable documents.

## Ecosystem options (candidates, not integrations)

Named for evaluation only — **no affiliation, partnership or data flow
exists or is implied**. Every candidate is judged on four questions:
open weights? consent controls? on-device option? who owns the trace?

- **Sentient Foundation** — community-built open-source AGI; candidate
  destination for anonymized traces contributed to open training
  commons, if its consent and ownership terms verify.
- **Virtuals Protocol** (virtuals.io) — tokenized agent ecosystem;
  candidate for publishing credentialed skill agents, with explicit
  caution on data-rights terms and financial-speculation exposure
  before any learner data is involved.
- **Hugging Face LeRobot** — open robot-learning stack and datasets;
  strong fit for demonstration traces from Making/Repair and Robotics
  OS modules under a contributor licence.
- **ROS 2** — robot middleware the Robotics OS pack already teaches
  around; traces replayed on real rigs in Trade Halls stay entirely
  local.

## Data principles (non-negotiable)

1. **Local first** — traces are recorded and stored only in the
   learner's browser; the apps make no network calls.
2. **Opt-in export** — data reaches any pipeline only when the learner
   exports it themselves, per session, eyes open.
3. **Anonymized by default** — exports carry skill signals, never
   identity.
4. **Capability returned** — machines trained on community traces
   serve that community.

Any future integration that cannot satisfy all four is out, whatever
its other merits.
