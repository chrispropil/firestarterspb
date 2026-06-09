# FirestarterLive

FirestarterLive is the planned local, notice-only alert layer for FirestarterSPB.

## Status

`PHASE_A_SCAFFOLD_ONLY`

This folder currently contains planning/scaffold documentation only. It must not be treated as a trading system.

## Governance

All future FirestarterLive outputs must carry:

- `NOTICE_ONLY`
- `RESEARCH_ALERT`
- `NO_AUTO_TRADE`
- `NO_EXCHANGE_KEYS`
- `NO_ORDER_EXECUTION`
- `MANUAL_REVIEW_REQUIRED`

## First build target

The first executable phase should be a dry-run evaluator that:

1. Loads scenario config from `configs/firestarterlive/firestarterlive_scenarios.yaml`.
2. Validates the schema.
3. Loads local FirestarterSPB data and approved Cell 1 metrics.
4. Prints whether disabled or enabled scenarios would trigger.
5. Writes no alert logs unless explicitly run with an audit flag.
6. Sends no notifications unless explicitly enabled in a later phase.

## Hard blocks

Do not add:

- exchange private API key handling
- order execution
- auto buy/sell/short logic
- leverage/margin logic
- Cell 2
- ML training
- raw data commits
- generated HTML commits
- secrets

## Runtime design

The eventual watcher should run locally from Windows Task Scheduler every 5 to 15 minutes. It should run once, write audit output if enabled, send configured notifications if enabled, and exit cleanly.
