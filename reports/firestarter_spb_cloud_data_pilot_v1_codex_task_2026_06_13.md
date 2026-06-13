# Codex Task — FirestarterSPB Cloud Data Pilot v1

## Mission

Implement Cloud Data Pilot v1 as a scoped dry-run-first branch/PR.

This task must build the first real cloud baseline collector scaffold for FirestarterSPB without enabling optimizer production, trading, exchange execution, scoring changes, public exposure, or worker execution.

## Required Branch

Create and work on:

```text
feature/cloud-data-pilot-v1
```

Do not commit directly to `main`.

## Source of Truth

Use this scope document as the build contract:

```text
reports/firestarter_spb_cloud_data_pilot_v1_scope_2026_06_13.md
```

## Required Files

Implement or add the following files:

```text
configs/cloud_data_pilot_v1_symbols.json
scripts/automation/cloud_data_pilot_fetch_ohlcv.py
scripts/automation/cloud_data_pilot_audit.py
scripts/automation/cloud_data_pilot_build_manifest.py
scripts/visualization/cloud_data_pilot_viewer.py
automation/n8n_cloud_data_pilot_dryrun.json
reports/firestarter_spb_cloud_data_pilot_v1_build_report.md
```

## Required CLI Behavior

The primary fetcher must support:

```text
python scripts/automation/cloud_data_pilot_fetch_ohlcv.py \
  --dry-run \
  --symbols configs/cloud_data_pilot_v1_symbols.json \
  --timeframe 5m \
  --days 30 \
  --output-dir data/cloud_pilot/v1 \
  --manifest reports/cloud_data_pilot/v1/manifest.json \
  --report reports/cloud_data_pilot/v1/report.md
```

It must also define but not default to:

```text
--execute
```

Dry-run is the default safe mode.

## Pilot Universe

Use a 25-symbol config file. If the exact approved 25-symbol list is not available in the repository, create a conservative placeholder list and mark it clearly as `PENDING_FINAL_SYMBOL_APPROVAL` in the config and build report.

Do not silently invent final production symbols.

## Data Scope

Build for:

- 25 symbols max
- 30-day minimum lookback
- 60-day supported if requested
- 5m OHLCV primary baseline
- optional derived 1h / 4h / daily summaries only if straightforward

Minimum candle fields:

```text
symbol
timestamp_utc
open
high
low
close
volume
source
timeframe
ingested_at_utc
```

## Storage Rules

- Append-only write behavior.
- Never overwrite existing historical data.
- Dedupe by `symbol + timestamp_utc + timeframe`.
- Write failed symbols and gaps to audit output.
- Keep output paths under approved cloud pilot directories.
- No raw data mutation outside `data/cloud_pilot/v1`.

## Manifest Requirements

Every dry-run and execute run must produce or plan a manifest containing:

```text
run_id
started_at_utc
ended_at_utc
mode
symbol_count_requested
symbol_count_completed
row_count_total
row_count_by_symbol
first_candle_by_symbol
last_candle_by_symbol
duplicate_count
gap_count
failed_symbols
output_paths
raw_data_mutation
scoring_changes
trading_execution
```

Safety flags must remain:

```text
raw_data_mutation=false for dry-run
scoring_changes=false
trading_execution=false
```

## Chart / Viewer Scaffold

Implement a first viewer scaffold for the locked chart set:

Must-have charts:

```text
Price + Volume
Price + ER
Price + FMLC
Price + Flowprint
Combined Firestarter State
1H / 4H Trend Context
Outcome Replay
25-Symbol Comparison Board
```

Should-have, if fast and safe:

```text
RVOL / Volume Expansion
Volatility / Range Compression
```

If ER/FMLC/Flowprint/raw_score fields are not available yet in the collected baseline, the viewer must show explicit `PENDING_FEATURE_SOURCE` placeholders rather than fake values.

## n8n Workflow Export

Create:

```text
automation/n8n_cloud_data_pilot_dryrun.json
```

It should follow the Phase 1 fixed-action pattern:

```text
Schedule Trigger -> HTTP Request to fixed worker route
```

The workflow must be inactive by default.

If a new worker route is required, update the fixed-action worker safely and do not allow arbitrary command execution.

## Worker Boundary

Do not enable:

```text
FIRESTARTER_CLOUD_WORKER_EXECUTE=true
```

Do not add any route that accepts arbitrary shell commands or user-supplied script paths.

If adding a fixed route, it must map to exactly one allowlisted script and default to dry-run.

## Explicit Prohibitions

Do not add:

- exchange credentials
- live trading
- order execution
- leverage logic
- optimizer production decisions
- public n8n exposure
- public worker exposure
- public dashboard exposure
- scoring/formula changes
- Cell 2 activation
- raw-data overwrite behavior
- auto-buy/auto-short charts
- PnL/profit prediction charts
- AI confidence chart

## Validation Required

Run and report:

```text
python -m py_compile scripts/automation/cloud_data_pilot_fetch_ohlcv.py
python -m py_compile scripts/automation/cloud_data_pilot_audit.py
python -m py_compile scripts/automation/cloud_data_pilot_build_manifest.py
python -m py_compile scripts/visualization/cloud_data_pilot_viewer.py
python scripts/automation/cloud_data_pilot_fetch_ohlcv.py --help
python scripts/automation/cloud_data_pilot_audit.py --help
python scripts/automation/cloud_data_pilot_build_manifest.py --help
python scripts/visualization/cloud_data_pilot_viewer.py --help
python scripts/automation/cloud_data_pilot_fetch_ohlcv.py --dry-run --symbols configs/cloud_data_pilot_v1_symbols.json --timeframe 5m --days 30 --output-dir data/cloud_pilot/v1 --manifest reports/cloud_data_pilot/v1/manifest.json --report reports/cloud_data_pilot/v1/report.md
```

Also validate JSON exports:

```text
python -m json.tool configs/cloud_data_pilot_v1_symbols.json
python -m json.tool automation/n8n_cloud_data_pilot_dryrun.json
```

## Required Build Report

Create:

```text
reports/firestarter_spb_cloud_data_pilot_v1_build_report.md
```

Include:

- files added/changed
- exact command outputs
- dry-run result
- validation result
- safety boundary confirmation
- any missing dependencies
- whether actual fetch execution was skipped
- whether symbol list is final or placeholder

## Commit / PR Rules

- Work on branch `feature/cloud-data-pilot-v1`.
- Open a PR when complete.
- Do not merge.
- Do not alter existing active cloud Phase 1 runtime config except for a safe fixed-action worker route if required.
- Do not modify optimizer/scoring formulas.

## Expected Result

A reviewable PR that implements a dry-run-first Cloud Data Pilot v1 collector scaffold and viewer scaffold, ready for Bob/Steve review before any VPS deployment or execute-mode collection.
