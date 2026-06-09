# Firestarter Live Audits — Top100 Review Tracker Template

## Purpose

Track profile-first visual review across the Binance Top100 dataset. This tracker is for setup hypotheses and profile branch review only.

## Active reference cases

| Symbol | Role | Current note |
|---|---|---|
| HYPEUSDT | X2 reference case | FMLC/raw_score persistence with price continuation candidate |
| ONDOUSDT | Original thesis/reference case | X2-style windows and low-flow weakness candidate |
| CCUSDT | Review candidate | Needs comparison against HYPE/ONDO |
| ETHUSDT | Control / possible false positive | Higher-price visual scaling issue; not strong X2 read visually |
| GIGGLEUSDT | Review candidate | Needs FMLC/Flowprint spike persistence review |
| PAXG | Control case | High-price / nonstandard behavior control |

## Visual label definitions

| Label | Meaning |
|---|---|
| X2_VISUAL_CONFIRMED | Visual structure resembles the HYPE/ONDO reference branch and needs metric extraction |
| X2_VISUAL_WEAK | Some structure appears, but continuation/persistence is weak |
| X2_FALSE_POSITIVE | Scanner/profile branch flagged it, but chart does not visually support the branch |
| X2_NEEDS_MORE_DATA | Chart or context is insufficient |
| HOLLOW_BREAKOUT_VISUAL_CONFIRMED | Price expansion appears unsupported by FMLC/Flowprint/raw_score |
| DOMINO_VISUAL_CONFIRMED | Deterioration sequence appears visually coherent |
| INSUFFICIENT_DATA | Missing or incomplete data prevents review |

## Review table

| Symbol | Window | Primary event type | Secondary tags | Data quality flags | Suspected setup hypothesis | Visual label | Classification | Compare against | Next required check | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| HYPEUSDT | 2026-05-17 to 2026-05-22 | X2_CANDIDATE | FAKE_RECOVERY / ENTRY_C_LIKE_RECOVERY / NIF_CATALYST_QUALITY_AUDIT | HIGH_NAN_WARNING | X2 continuation/onset | REFERENCE_CASE | REFERENCE_CASE | ONDO, CC, GIGGLE, ETH | Exact metric extraction | Do not promote beyond reference case |
| ONDOUSDT | TBD | TBD | TBD | TBD | X2 continuation / weakness branch | TBD | TBD | HYPE, CC, ETH | Exact timestamp extraction | Original thesis case |
| CCUSDT | TBD | TBD | TBD | TBD | X2 candidate review | TBD | TBD | HYPE, ONDO, ETH | Visual review | Candidate only |
| ETHUSDT | TBD | TBD | TBD | TBD | False-positive/control review | TBD | TBD | HYPE, ONDO | Scaling-aware review | Control case |
| GIGGLEUSDT | TBD | TBD | TBD | TBD | X2 candidate review | TBD | TBD | HYPE, ONDO, CC | Visual review | Candidate only |
| PAXG | TBD | TBD | TBD | TBD | High-price control case | TBD | TBD | ETH, HYPE | Scaling-aware review | Control case |

## Required next checks before any promotion

- Exact timestamp metric extraction
- Cross-symbol match count using AI match index
- Data quality review
- Symbol concentration review
- Time-window stability review
- False-positive review

## Boundaries

No strategy validation, signal creation, entry/exit language, trade language, Cell 2 label creation, live alerts, or execution logic.
