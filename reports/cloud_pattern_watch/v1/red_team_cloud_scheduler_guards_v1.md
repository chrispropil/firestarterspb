# Red Team Cloud Scheduler Guards v1

STATUS: REPAIR_READY

## Trigger

Red Team identified two immediate blockers before active cloud scheduling:

1. The Cell 1 scheduler tick accepted any positive adapter output, which could hide major producer/API degradation.
2. Cloud Pattern Watch notifications were not visually distinct from local/n8n notifications.

## Fix 1 — Minimum Viable Universe Threshold

Updated `scripts/local/cloud_cell1_scheduler_tick.sh` to require a minimum viable snapshot universe before reporting a pass-class status.

Default thresholds:

- `CELL1_MIN_ACCEPTED_ROWS`: `20`
- `CELL1_MIN_ACCEPTED_SYMBOLS`: `20`

Pass-class status now requires:

- `adapter_exit_code == 0`
- `adapter_ok == true`
- `adapter_snapshot_written == true`
- `adapter_rows_accepted >= 20`
- `adapter_symbols_accepted >= 20`

Status behavior:

- `PASS`: producer exit `0` and coverage threshold met
- `PASS_WITH_PRODUCER_WARNINGS`: producer exit non-zero, but coverage threshold met
- `FAIL_UNDER_MINIMUM_UNIVERSE`: adapter wrote a snapshot, but accepted rows/symbols are below threshold
- `FAIL`: adapter did not produce a valid written snapshot

## Fix 2 — Cloud Notification Origin Tag

Updated `scripts/automation/cloud_pattern_watch_v1.py` so cloud-origin notifications include:

`[CLOUD]`

Cloud ntfy title example:

`[CLOUD] FMLC Hanger`

Cloud ntfy message example:

`[CLOUD] FMLC Hanger — BTCUSDT ...`

The event log now also records:

- `origin: cloud`
- `origin_tag: [CLOUD]`
- `notification_title: [CLOUD] FMLC Hanger`

## Safety

- No cron activation.
- No Pattern Watch scheduler activation.
- No n8n activation.
- No trading execution.
- No scoring changes.
- No local notification router changes.

## Remaining Governance Rule

Before permanent scheduler activation, require time-decay evidence from a limited scheduled trial window, not just one manual pass.
