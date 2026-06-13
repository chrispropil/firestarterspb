# Cloud Metric Snapshot Adapter v1 Build Report

DATE: 2026-06-13
STATUS: READY_FOR_REVIEW
BRANCH: `feature/cloud_snapshot_v1`

## Scope

Adds a manual-only adapter that converts existing precomputed metric files into the Pattern Watch `current_snapshot.json` format.

## Files

Added:
- `scripts/automation/cloud_metric_snapshot_adapter_v1.py`
- `configs/cloud_metric_snapshot_adapter_v1.json`

Updated:
- `configs/cloud_pattern_watch_v1.json`
- `scripts/automation/cloud_pattern_watch_v1.py`
- `scripts/automation/cloud_health_check.py`

## Worker routes

- `/run/cloud-metric-snapshot-dryrun`
- `/run/cloud-metric-snapshot-build`
- `/run/cloud-research-pattern-current-dryrun`
- `/run/cloud-research-pattern-current-send`

## Behavior

The adapter searches local precomputed metric files, filters to the approved 25-symbol pilot universe, rejects excluded or unapproved symbols, keeps the latest valid row per symbol, and writes `state/cloud_pattern_watch/current_snapshot.json` only when explicitly run with the build route.

## Required fields

- `symbol`
- `price_position`
- `er`
- `fmlc`
- `flowprint`
- `raw_score`

Common Cell 1 aliases such as `er_value`, `fmlc_value`, and `flowprint_proxy_value` are accepted.

## Safety

- No schedule activation.
- No market data fetch.
- No production score change.
- No exchange credentials.
- No order execution.
- No symbol expansion.

STATUS: READY_FOR_REVIEW
