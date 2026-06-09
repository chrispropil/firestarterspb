# FirestarterLive — Local Notice-Only Alert System Build Plan

## Mission

Prepare a local FirestarterLive alert framework for `C:\firestarterspb` that can notify Chris when finalized buy-side or short-side research scenarios are met.

This is a research alert system only. It must not trade, place orders, manage positions, use exchange secrets, or provide automated execution.

## Governance flags

Every alert and runtime output must carry:

- `NOTICE_ONLY`
- `RESEARCH_ALERT`
- `NO_AUTO_TRADE`
- `NO_EXCHANGE_KEYS`
- `NO_ORDER_EXECUTION`
- `MANUAL_REVIEW_REQUIRED`

## Hard blocks

Do not implement:

- exchange order routes
- private API key handling
- leverage, margin, position sizing, or portfolio management
- auto buy, sell, or short execution
- Cell 2
- ML training
- unexplained black-box alerting
- raw market data commits
- generated HTML commits
- destructive cleanup
- `git add .`

## Current baseline

Known current repo state before FirestarterLive scaffolding:

- Repo: `chrispropil/firestarterspb`
- Local path: `C:\firestarterspb`
- Core88 viewer: working
- Core88 active discovered symbols: 82
- Missing derivatives context: pulled for 45 symbols
- Derivative files written locally: 315
- Viewer loads both derivative folders
- FMLC missing during first 199 hourly rows is expected warmup, not a bug
- Latest pushed viewer patch before this scaffold: `ffb7e87`

## Target structure

```text
configs/firestarterlive/
  firestarterlive_symbols.yaml
  firestarterlive_scenarios.yaml
  firestarterlive_alert_settings.yaml

scripts/firestarterlive/
  README.md
  run_firestarterlive_watch.py
  compute_firestarterlive_metrics.py
  evaluate_firestarterlive_scenarios.py
  send_firestarterlive_alert.py
  firestarterlive_state.py

reports/firestarterlive/
  firestarterlive_build_plan.md
  firestarterlive_phase_a_scaffold_audit.md
  firestarterlive_alert_events.jsonl
  firestarterlive_daily_audit.md
  firestarterlive_latest_status.json
```

## Runtime design

The watcher should run locally every 5 to 15 minutes through Windows Task Scheduler.

Recommended runtime flow:

1. Load active symbol list.
2. Load latest local market data.
3. Load local derivatives context.
4. Compute existing Firestarter metrics using approved Cell 1 logic.
5. Evaluate enabled scenario rules from config.
6. Write append-only audit events for triggered scenarios.
7. Send notification only if alert delivery is configured and explicitly enabled.
8. Exit cleanly.

No long-running infinite loop in the first build.

## Phase A scope

Phase A is scaffold and planning only.

Allowed files:

- `reports/firestarterlive/firestarterlive_build_plan.md`
- `configs/firestarterlive/firestarterlive_scenarios.yaml`
- `configs/firestarterlive/firestarterlive_alert_settings.yaml`
- `scripts/firestarterlive/README.md`
- `reports/firestarterlive/firestarterlive_phase_a_scaffold_audit.md`

Phase A must not send alerts, compute live alerts, modify formulas, or add trading logic.

## Phase B scope

Add dry-run evaluator only:

- validate scenario config
- load test symbols
- evaluate scenarios in dry-run mode
- print triggered/not-triggered results
- no notifications unless later approved

## Phase C scope

Add local watcher:

```powershell
py .\scripts\firestarterlive\run_firestarterlive_watch.py --dry-run
py .\scripts\firestarterlive\run_firestarterlive_watch.py --write-audit
py .\scripts\firestarterlive\run_firestarterlive_watch.py --send-alerts
```

`--send-alerts` must fail closed unless settings are valid.

## Phase D scope

Add notification adapters after approval:

- console
- local file
- Slack webhook or Slack bot
- email
- Telegram
- Discord
- Windows toast notification

No secrets in repo.

## Phase E scope

Add scheduled local watcher using Windows Task Scheduler after dry-run validation.

## Validation requirements

Every build phase must create a report under `reports/firestarterlive/` with:

- status
- files created
- files modified
- commands run
- raw data commit status
- generated HTML commit status
- safety checklist
- blockers
