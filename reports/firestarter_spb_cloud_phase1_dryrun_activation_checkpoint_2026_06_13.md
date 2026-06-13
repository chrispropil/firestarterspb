# FirestarterSPB Cloud Phase 1 Dry-Run Activation Checkpoint — 2026-06-13

## Status

`PASS_PHASE1_DRYRUN_ACTIVATION`

The Phase 1 cloud shell has advanced from smoke-test-only to controlled scheduled dry-run operation.

## Confirmed Active Workflow State

Postgres/n8n workflow table confirmed the final active state:

```text
FirestarterSPB Cloud Auto Viewer Refresh  | t
FirestarterSPB Cloud Health Check         | t
FirestarterSPB Cloud Optimizer Queue Stub | f
FirestarterSPB Cloud Result Collector     | t
```

## Active

- `FirestarterSPB Cloud Health Check`
- `FirestarterSPB Cloud Result Collector`
- `FirestarterSPB Cloud Auto Viewer Refresh`

## Inactive

- `FirestarterSPB Cloud Optimizer Queue Stub`

## Meaning

The cloud system is now scheduled for controlled dry-run status/reporting actions. It remains a research-control shell and does not execute trades.

Current cloud activity:

- worker health check scheduling
- result/status collector scheduling
- auto viewer refresh endpoint scheduling in dry-run mode

Still not active:

- optimizer queue migration
- optimizer production logic
- live trading automation
- exchange execution
- exchange credential use
- raw data mutation
- scoring/formula changes

## Required Safety State

- `FIRESTARTER_CLOUD_WORKER_EXECUTE=false`
- n8n remains localhost-only behind SSH tunnel
- worker remains localhost-only
- dashboard remains localhost-only
- UFW remains SSH-only inbound
- no exchange credentials added
- optimizer queue stub remains inactive

## Operational Boundary

This checkpoint does not mean the cloud is collecting live market data or producing trade signals. It means the approved Phase 1 cloud worker endpoints are being scheduled in dry-run mode.

## Next Valid Actions

1. Observe scheduled runs for Health Check, Result Collector, and Auto Viewer Refresh.
2. Confirm no failures in n8n Executions.
3. Check worker logs/status files after several cycles.
4. Keep Optimizer Queue Stub inactive.
5. Do not enable live execution or optimizer migration without separate approval.

## Do Not Do

- Do not activate Optimizer Queue Stub yet.
- Do not enable `FIRESTARTER_CLOUD_WORKER_EXECUTE=true`.
- Do not open ports 5678, 8090, or 8080 publicly.
- Do not add exchange keys.
- Do not move scoring logic or market-data collection into cloud during this checkpoint.

## Handoff

Cloud Phase 1 scheduled dry-run operation is now active for health, result collection, and auto viewer refresh. The optimizer remains intentionally parked.
