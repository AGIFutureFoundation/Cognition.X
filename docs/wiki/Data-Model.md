# Data Model

## The block

A **block** is the atomic unit: one capability, one grade band, one
transfer check. It is a row in
[`data/blocks.csv`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/data/blocks.csv):

```
block_id, pack, track, code, grade, level, credential, theme, description, transfer_check
```

`block_id` (`CX-<PACK>-<NNNN>`) is globally unique, deterministic and
permanent — always join on it, never on `code` (source codes reuse
prefixes across packs).

## The hierarchy

```
Pack (26)
└── Track (95) ──────────── 1 credential each
    └── Theme (10 per track)
        └── Block (5 per theme, one per grade band)
```

- A **community pack** = 5 tracks = 250 blocks.
- An **OS edition** = 10 tracks = 500 blocks.
- **Legacy packs** (K–12, Trade School, and seven thematic packs) predate
  this shape; they keep per-grade rows and per-row credentials until the
  Phase 1 backfill.

## Bands and levels

| Grade band | Level |
|---|---|
| K–2 | Explorer |
| 3–5 | Explorer |
| 6–8 | Builder |
| 9–10 | Practitioner |
| 11–12 | Lead |

The same theme recurs at every band; depth, not topic, changes with age.

## Transfer checks

Every block ends in a task performed on **real material** — a real lease,
a real device, a real dataset, a real conversation — with an observable
outcome. This is the assessment philosophy of the whole system: a block
is not "covered", it is *demonstrated*.

Full column reference:
[`data/schema.md`](https://github.com/AGIFutureFoundation/Cognition.X/blob/main/data/schema.md).
