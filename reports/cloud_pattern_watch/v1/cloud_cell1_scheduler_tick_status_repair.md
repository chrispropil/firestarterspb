# Cloud Cell 1 Scheduler Tick Status Repair

STATUS: REPAIR_READY

## Issue

The first manual cloud tick refreshed the Pattern Watch snapshot successfully through the metric adapter, but the tick status was marked `FAIL` because the Cell 1 producer returned exit code `1` on a partial-symbol warning.

Observed cloud result:

- producer_exit: `1`
- adapter_exit: `0`
- adapter status: `PASS`
- rows accepted: `24`
- snapshot_written: `true`

## Repair

Update `scripts/local/cloud_cell1_scheduler_tick.sh` so tick success is based on adapter proof of usable snapshot output:

- `adapter_exit_code == 0`
- `adapter_ok == true`
- `adapter_snapshot_written == true`
- `adapter_rows_accepted > 0`

When these are true and producer exit is non-zero, the tick status becomes:

`PASS_WITH_PRODUCER_WARNINGS`

## Safety

- Pattern Watch send remains false.
- Scheduler activation remains false.
- N8N activation remains false.
- Trading execution remains false.
- Scoring changes remain false.
- No cron installation is included.

## Expected Manual Retest

After merge and cloud pull, rerun the tick manually.

Expected status:

`PASS_WITH_PRODUCER_WARNINGS`

Expected adapter fields:

- adapter_exit_code: `0`
- adapter_ok: `true`
- adapter_snapshot_written: `true`
- adapter_rows_accepted: `24` or greater than `0`
