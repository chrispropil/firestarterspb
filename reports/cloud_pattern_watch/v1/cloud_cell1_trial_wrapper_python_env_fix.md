# Cloud Cell 1 Trial Wrapper Python Environment Fix

STATUS: REPAIR_READY

## Trigger

The limited cron trial produced a failed wrapper entry with blank parsed fields:

- `tick_status`: blank
- `adapter_symbols_accepted`: blank

The underlying Cell 1 scheduler tick still completed successfully afterward:

- `status=PASS_WITH_PRODUCER_WARNINGS`
- `adapter_symbols_accepted=24`
- `coverage_threshold_met=true`

## Assessment

This points to a trial wrapper parser/environment issue, not a Cell 1 data-pull failure.

Likely cause:

- manual shell had access to a Python interpreter
- cron environment did not inherit the same Python/venv path
- wrapper used `python` directly when parsing the tick status JSON

## Fix

Updated `scripts/local/cloud_cell1_scheduler_trial_tick.sh` to:

1. Prefer `${REPO_ROOT}/.venv/bin/python`.
2. Fall back to `python3` or `python` if the repo venv is unavailable.
3. Hard-fail visibly if no Python interpreter is available.
4. Add `parser_ok` to the trial status JSON.
5. Add `python_bin` to the trial status JSON.
6. Prevent blank parser fields from being treated as pass-class.

## Safety

- No cron activation added.
- Existing paused cron file remains operator-controlled.
- Pattern Watch send remains false.
- N8N activation remains false.
- Trading execution remains false.
