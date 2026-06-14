# Cloud Cell 1 Limited Scheduler Trial Plan

STATUS: TRIAL_WRAPPER_READY

## Purpose

Run a limited Cloud Cell 1 scheduled-pull trial before permanent activation.

This trial is designed to satisfy the Red Team time-decay rule: do not treat one manual pass as production health.

## Scope

Added file:

- `scripts/local/cloud_cell1_scheduler_trial_tick.sh`

## Trial Behavior

The trial wrapper:

1. Tracks run count in `state/cloud_pattern_watch/cell1_scheduler_trial_counter.txt`.
2. Runs `scripts/local/cloud_cell1_scheduler_tick.sh` only while run count is below the configured maximum.
3. Writes trial state to `state/cloud_pattern_watch/cell1_scheduler_trial_status.json`.
4. Appends trial logs to `logs/cloud/cell1_scheduler_trial.log`.
5. Stops executing work after `CELL1_TRIAL_MAX_RUNS` is reached.

Default trial values:

- `CELL1_TRIAL_MAX_RUNS`: `16`
- intended interval: `15 minutes`
- approximate observation window: `4 hours`

## Safety

- Pattern Watch send remains false.
- N8N activation remains false.
- Trading execution remains false.
- The wrapper does not install cron by itself.
- The wrapper does not activate permanent scheduling.

## Pass Conditions

A trial tick is pass-class when the underlying Cell 1 tick status is either:

- `PASS`
- `PASS_WITH_PRODUCER_WARNINGS`

The underlying Cell 1 tick already enforces the Red Team minimum viable universe guard:

- accepted rows >= `20`
- accepted symbols >= `20`
- adapter wrote a valid snapshot

## Review Gate After Trial

Before any permanent scheduler activation, review:

- `state/cloud_pattern_watch/cell1_scheduler_trial_status.json`
- `state/cloud_pattern_watch/cell1_scheduler_tick_status.json`
- `logs/cloud/cell1_scheduler_trial.log`
- `logs/cloud/cell1_scheduler_tick.log`

Required evidence:

- no repeated lock collisions
- no under-threshold universe failures
- no adapter write failures
- no Pattern Watch send activation
- no n8n activation
- no trading execution
