# Cloud Cell 1 Scheduler Tick Gate Plan

STATUS: PLANNED_TICK_GATE_READY

## Purpose

Create a guarded cloud scheduler tick script that can refresh Cell 1 metrics and the Pattern Watch snapshot when manually run or later attached to cron.

This does not activate cron by itself.

## Scope

Added file:

- `scripts/local/cloud_cell1_scheduler_tick.sh`

## Tick Sequence

1. Enter repository root.
2. Acquire non-overlap lock.
3. Activate `.venv` when present.
4. Run Cell 1 metric producer through the existing manual-build confirmation gate.
5. Run metric snapshot adapter write to refresh `state/cloud_pattern_watch/current_snapshot.json`.
6. Write tick status to `state/cloud_pattern_watch/cell1_scheduler_tick_status.json`.
7. Append logs to `logs/cloud/cell1_scheduler_tick.log`.

## Safety Lock

- Pattern Watch send remains false.
- N8N activation remains false.
- Trading execution remains false.
- Scoring changes remain false.
- Raw data mutation beyond approved current metric/snapshot state remains false.
- Cron activation is not included in this PR.

## Manual Verification Gate

After merge and cloud pull, run the tick manually once from `/opt/firestarterspb`.

Pass condition:

- tick status JSON exists
- adapter exit code is `0`
- current snapshot remains writable and readable
- Pattern Watch send remains inactive

## Future Gate

Only after manual tick passes should cron installation be considered.
