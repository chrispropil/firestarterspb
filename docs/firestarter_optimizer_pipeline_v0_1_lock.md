# Firestarter Optimizer Pipeline v0.1 Lock

## Status

LOCKED FOR BUILD PREP.

## Doctrine

Firestarter Optimizer v0.1 is an evidence and monitoring pipeline, not a trading bot.

Core flow:

```text
Incoming derived Firestarter data
→ Cell 2 incoming cleaner
→ candidate ticket memory
→ candidate state monitor
→ Slack notice formatter
→ hourly monitor summary
→ scheduled Steve/Bob/Jody review
→ later symbol behavior memory
```

## Proof-of-concept anchor

ESPORT short-hanger persistence around approximately 0.35 followed by collapse toward approximately 0.15 is treated as a major proof-of-concept anchor case for the pipeline.

Anchor label:

```text
PERSISTENT_SHORT_HANGER_THEN_COLLAPSE
```

Governance note: this is proof-of-concept evidence, not a validated edge claim. Preserve it as an anchor case and collect more cases.

## Build order

1. Complete-source validation of `scripts/firestarter_optimizer/build_candidate_tickets.py`.
2. Incoming Cell 2 cleaner wrapper.
3. Candidate state monitor.
4. Slack notice formatter.
5. Hourly monitor summary writer.
6. Scheduler review loop.
7. Later symbol behavior profile memory.

## Immediate next build

Create:

```text
scripts/firestarter_optimizer/update_candidate_states.py
```

Purpose:

- read candidate-ticket output
- track first seen / last seen
- track persistence count and age
- track first price / latest price
- track favorable and adverse movement by direction bias
- detect observation states only
- write append-only state events and current active snapshot

Outputs:

```text
reports/firestarter_optimizer/active_candidates.jsonl
reports/firestarter_optimizer/candidate_state_events.jsonl
reports/firestarter_optimizer/expired_or_changed_candidates.jsonl
reports/firestarter_optimizer/update_candidate_states_report.md
```

## Observation states

Use observation states only. Do not use them as exclusion rules.

```text
NEW
ACTIVE_VALID
PERSISTENT_HANGER
PERSISTENT_GRIND
PERSISTENT_REAWAKENING
PERSISTENT_THEN_COLLAPSE
PERSISTENT_THEN_BREAKOUT
PERSISTENT_THEN_CHOP
ADVERSE_FIRST
MICRO_MOVE_HIT
GRIND_BROKE
HANGER_CONFIRMED
DATA_GAP
```

## Direction bias

Track behavior by direction bias.

```text
LONG
SHORT_REVIEW
AVOID_LONG
WATCH_ONLY
DATA_GAP
```

Short-hanger persistence may be useful warning pressure. Long persistence may be stale, active, or broken. Do not treat persistence as automatically good or bad.

## Candidate state monitor required fields

The monitor should track at minimum:

```text
candidate_id
symbol
direction_bias
signal_family
action_label
first_seen_utc
last_seen_utc
persistence_count
persistence_minutes
first_seen_price
latest_price
price_change_since_first_seen_pct
max_favorable_pct
max_adverse_pct
current_state
previous_state
state_change_reason
source_ticket_count
last_updated_utc
```

## X1 micro-move observation

Track but do not trade:

```text
time_to_0_3pct_move
time_to_0_5pct_move
time_to_0_75pct_move
time_to_1pct_move
time_to_1_5pct_move
time_to_2pct_move
adverse_before_favorable_flag
x1_micro_move_hit
```

## Short-hanger observation

Track but do not trade:

```text
hanger_first_seen_utc
hanger_last_seen_utc
hanger_persistence_count
hanger_age_minutes
first_hanger_price
latest_hanger_price
lowest_price_after_hanger
short_mfe_pct
short_mae_pct
hanger_confirmed_breakdown_flag
```

## Hard boundaries

Do not:

- create live trading logic
- create exchange/order logic
- create ML
- create `signal_discovery.py`
- create automatic rule mutation
- create automatic exclusion rules
- create new composite master scores
- mutate raw scanner files
- mutate raw JSONL/parquet/OHLCV/Tardis/history files
- write active outputs directly to Google Drive
- claim proven edge

## Required validation later

Before any rule promotion, later audit must include:

- effective sample size correction
- block bootstrap
- shuffle/random-label test
- inverted-filter test
- symbol concentration
- leave-one-symbol-out
- time-slice stability
- threshold sensitivity
- alpha-adjusted labels
- triple-barrier labels
- purged/embargoed validation where feasible

## Acceptance for next build

Candidate state monitor passes if:

- it reads candidate-ticket JSONL safely
- it writes only isolated/derived outputs
- it preserves existing ticket history
- it creates stable candidate state records
- it detects persistence and directional movement without rule mutation
- report documents counts, paths, state distributions, and missing fields
- no raw/scanner/history files are modified

## Board lock

```text
BOB: Buildable.
JODY: Scientifically acceptable as evidence-only observation pipeline.
STEVE: Locked with boundaries.
CHRIS: Final approval received.
```
