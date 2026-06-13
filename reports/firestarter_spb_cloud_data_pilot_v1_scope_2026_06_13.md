# FirestarterSPB Cloud Data Pilot v1 Scope — 2026-06-13

## Status

`READY_FOR_BUILD_PLANNING`

This document locks the next approved cloud phase after Phase 1 dry-run activation.

## Phase Name

`Cloud Data Pilot v1`

## Purpose

Build the first real cloud data baseline collector for FirestarterSPB without enabling optimizer production, trading, exchange execution, or scoring changes.

The goal is to prove that cloud can safely pull, store, dedupe, audit, and visualize a small baseline universe before any optimizer logic is activated.

## Approved Maximum Scope

- 25-symbol pilot universe
- 30-day historical backfill minimum
- 60-day preferred historical backfill if API/storage load is acceptable
- 5m candles as primary baseline
- optional derived 1h / 4h / daily context views
- append-only storage
- dedupe by symbol + timestamp
- manifest/audit report for every pull
- chart/dashboard preparation only
- no production optimizer decisions
- no live trade signals
- no exchange order execution
- no raw data overwrite

## Hard Boundaries

Do not add or enable:

- exchange credentials
- live trading
- order execution
- leverage logic
- auto-buy / auto-short logic
- optimizer production decisions
- public n8n access
- public worker access
- public dashboard access
- `FIRESTARTER_CLOUD_WORKER_EXECUTE=true`
- scoring/formula changes
- Cell 2 activation
- raw-data mutation or overwrite

## Data Requirements

### Primary Dataset

5m OHLCV candles for each pilot symbol.

Minimum fields:

- `symbol`
- `timestamp_utc`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `source`
- `timeframe`
- `ingested_at_utc`

### Audit Metadata

Every pull must produce a manifest containing:

- run ID
- start timestamp
- end timestamp
- symbol count requested
- symbol count completed
- row count per symbol
- first candle timestamp per symbol
- last candle timestamp per symbol
- duplicate count
- gap count
- failed symbols
- output paths
- mode
- raw-data mutation flag
- scoring change flag
- trading execution flag

### Storage Rules

- append-only write path
- no overwrite of historical data
- dedupe by `symbol + timestamp_utc + timeframe`
- write gaps to a separate audit file
- failed pulls must not corrupt prior completed data
- all output paths must stay under approved cloud data directories

## Chart Set

### Must Have

1. Price + Volume
2. Price + ER Panel
3. Price + FMLC Panel
4. Price + Flowprint Panel
5. Combined Firestarter State Chart
6. 1H / 4H Trend Context Chart
7. Outcome Replay Chart
8. 25-Symbol Comparison Board

### Should Have

9. RVOL / Volume Expansion Chart
10. Volatility / Range Compression Chart

### Later Only

- Funding / Open Interest Chart
- BTC / Market Regime Overlay
- Narrative / NIF Overlay
- Whale / Orderbook / Taker Flow

### Rejected for Phase 2A

- Auto-buy chart
- Auto-short chart
- PnL projection chart
- Leverage sizing chart
- AI confidence chart
- Profit prediction chart

## Build Objects Required

Recommended implementation objects:

1. `configs/cloud_data_pilot_v1_symbols.json`
2. `scripts/automation/cloud_data_pilot_fetch_ohlcv.py`
3. `scripts/automation/cloud_data_pilot_audit.py`
4. `scripts/automation/cloud_data_pilot_build_manifest.py`
5. `scripts/visualization/cloud_data_pilot_viewer.py`
6. `automation/n8n_cloud_data_pilot_dryrun.json`
7. `reports/firestarter_spb_cloud_data_pilot_v1_build_report.md`

## Acceptance Criteria

A build candidate is acceptable only if it proves:

- runs in dry-run mode without network writes
- can fetch 25 symbols when explicitly approved
- writes append-only candle data
- dedupes cleanly
- generates per-symbol row counts
- reports gaps and failed symbols
- writes a manifest
- produces at least the locked starter chart set or a viewer scaffold proving chart readiness
- has no exchange credentials
- has no trading execution
- has no scoring/formula changes
- has no optimizer production activation
- has no public service exposure

## First Build Mode

The first implementation should support:

```text
--dry-run
--symbols configs/cloud_data_pilot_v1_symbols.json
--timeframe 5m
--days 30
--output-dir data/cloud_pilot/v1
--manifest reports/cloud_data_pilot/v1/manifest.json
--report reports/cloud_data_pilot/v1/report.md
```

Dry-run must report planned actions without writing market data.

## Second Build Mode

Only after dry-run review:

```text
--execute
```

Execute mode may fetch and append data, but still must not score, trade, or activate optimizer decisions.

## Current Cloud Dependency

Phase 1 cloud shell is already active with:

- Health Check active
- Result Collector active
- Auto Viewer Refresh active in dry-run mode
- Optimizer Queue Stub inactive

Cloud Data Pilot v1 should integrate only after repo review and explicit activation.

## Handoff

Next valid action is a scoped implementation branch/PR for Cloud Data Pilot v1. Do not modify active scoring, optimizer, exchange integrations, or public exposure settings.
