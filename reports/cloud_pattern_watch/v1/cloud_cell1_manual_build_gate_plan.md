# Cloud Cell 1 Manual Build Gate Plan

Issue: #10
Date: 2026-06-13

## Scope

This branch adds a controlled manual build gate to `scripts/automation/cloud_cell1_metric_producer_v1.py`.

## Command Behavior

- Default remains dry-run:
  `python scripts/automation/cloud_cell1_metric_producer_v1.py`
- Explicit dry-run remains supported:
  `python scripts/automation/cloud_cell1_metric_producer_v1.py --dry-run`
- Legacy build remains rejected:
  `python scripts/automation/cloud_cell1_metric_producer_v1.py --build`
- Manual build without confirmation is rejected and writes only denial manifest/status:
  `python scripts/automation/cloud_cell1_metric_producer_v1.py --manual-build`
- Controlled manual build requires exact confirmation:
  `python scripts/automation/cloud_cell1_metric_producer_v1.py --manual-build --confirm-manual-build CELL1_MANUAL_BUILD_APPROVED`

## Safety Gates

- Governed symbol config must be a JSON object, never a bare list.
- Symbols are read only from `symbols`.
- Maximum symbol count is read only from `max_symbols`.
- Exclusions are read only from `excluded_symbols`.
- Status is read only from `status`.
- Loaded symbol count must be less than or equal to `max_symbols`.
- For Issue #10, `max_symbols` must equal `25`.
- Any excluded symbol in the loaded universe hard-fails.
- Output directory must be exactly `state/cloud_pattern_watch`.
- Report directory must be exactly `reports/cloud_pattern_watch/v1`.
- Base API URL must remain the approved public Bitget endpoint.
- No raw candle history is written.
- No exchange credentials, private endpoints, optimizer changes, scoring changes, trading execution, Cell 2, scheduler activation, n8n activation, or Pattern Watch ntfy send are added.

## Manifest / Status

Every `--manual-build` attempt writes:

- `state/cloud_pattern_watch/cell1_manual_build_gate_status.json`
- `reports/cloud_pattern_watch/v1/cell1_manual_build_gate_manifest.json`

Each manifest/status includes mode, gate result, symbol count, max symbols, excluded symbols, output paths, safety flags, and timestamp UTC.

