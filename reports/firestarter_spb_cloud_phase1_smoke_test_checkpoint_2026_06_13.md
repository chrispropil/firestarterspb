# FirestarterSPB Cloud Phase 1 Smoke Test Checkpoint — 2026-06-13

## Status

`PASS_PHASE1_CLOUD_SMOKE_TEST`

Cloud Phase 1 is deployed and verified as a private-first control shell. It is not collecting market data, not running optimizer production logic, and not executing trades.

## Confirmed Scope

- GitHub PR #3 merged into `main`.
- Follow-up hardening patch committed to `main` for dashboard localhost binding.
- Ubuntu 24.04 VPS connected by SSH.
- Docker and Docker Compose installed.
- FirestarterSPB repository cloned to `/opt/firestarterspb`.
- Cloud stack started from `cloud/firestarterspb_vps/docker-compose.yml`.
- No exchange credentials added.
- No live trading automation enabled.
- `FIRESTARTER_CLOUD_WORKER_EXECUTE=false` remains the required safe default.

## Important Commits

- PR #3 merge commit: `ba81535b4def855829a6b019973d2d438f16f4b6`
- Dashboard localhost hardening commit: `536c3033a0cfea10b4af6ec4e308c87c85addedd`

## Security Posture

- UFW firewall active.
- Incoming traffic denied by default.
- SSH is the only allowed inbound service.
- n8n bound to `127.0.0.1:5678`.
- Firestarter worker bound to `127.0.0.1:8090`.
- Dashboard bound to `127.0.0.1:8080`.
- n8n access is through SSH tunnel only.
- Worker access is internal/local only.
- Dashboard is private/local only.
- `.env` credentials were generated locally on the VPS and were not pasted into chat or committed to the repository.

## Runtime Validation

Docker stack services verified:

- `postgres`: healthy
- `firestarter-worker`: healthy
- `n8n`: running and reachable through SSH tunnel
- `dashboard`: running; returns expected nginx response while no dashboard index is present

Worker endpoint checks:

- `GET /health`: PASS
- `POST /run/viewer-refresh`: PASS, dry-run only
- `POST /run/result-collector`: PASS, dry-run only
- `POST /run/optimizer-queue-stub`: PASS, dry-run only

Observed safety flags from worker responses:

- `raw_data_mutation=false`
- `trading_execution=false`
- `ml_enabled=false` for optimizer stub
- `mode=dry_run` for non-health actions

## n8n Workflow State

Four workflow exports were imported into n8n:

- `FirestarterSPB Cloud Health Check`
- `FirestarterSPB Cloud Auto Viewer Refresh`
- `FirestarterSPB Cloud Result Collector`
- `FirestarterSPB Cloud Optimizer Queue Stub`

Manual workflow tests:

- Health Check: PASS
- Auto Viewer Refresh: PASS
- Result Collector: PASS
- Optimizer Queue Stub: PASS

Final active-state correction:

- Health Check: active
- Auto Viewer Refresh: inactive
- Result Collector: inactive
- Optimizer Queue Stub: inactive

Scheduled health-check execution succeeded after activation.

## Correction Made During Deployment

Initial Docker Compose dashboard binding exposed the dashboard on all interfaces:

```text
0.0.0.0:8080->80/tcp
```

This was corrected locally and then patched in the repository to:

```text
127.0.0.1:8080->80/tcp
```

This keeps the dashboard private-first and aligned with the Phase 1 security model.

## Current Capability

The cloud system is now alive and monitoring itself.

It currently collects:

- cloud worker health status
- scheduled health-check execution status
- dry-run status artifacts from manual endpoint tests

It does not yet collect:

- live coin data
- scanner data
- optimizer candidates
- trade signals
- market history
- viewer refresh outputs as active production data

## Known Non-Blocking Warnings

n8n emitted warnings during workflow import:

- settings file permission warning for `/home/node/.n8n/config`
- task runner deprecation warning recommending `N8N_RUNNERS_ENABLED=true`

These did not block import, manual tests, or scheduled health-check execution. They should be handled in a future maintenance patch, not during the smoke-test checkpoint.

## Next Valid Actions

Recommended next sequence:

1. Leave only Health Check active for stability observation.
2. Let the VPS run through several scheduled health-check cycles.
3. Add a small cloud status/audit report command if needed.
4. Patch n8n environment warnings in a separate repo commit.
5. Only after stability: activate Result Collector in dry-run mode.
6. Do not activate viewer refresh or optimizer queue until explicitly approved.

## Do Not Do

- Do not expose n8n publicly.
- Do not open ports 5678, 8090, or 8080 to the internet.
- Do not enable `FIRESTARTER_CLOUD_WORKER_EXECUTE=true` yet.
- Do not add exchange credentials.
- Do not move optimizer scoring logic into cloud yet.
- Do not activate Auto Viewer Refresh, Result Collector, or Optimizer Queue Stub without explicit approval.
- Do not treat this as market-data collection or signal production.

## Handoff

Cloud Phase 1 is now a working private control shell. The next phase is controlled observation and maintenance hardening, not optimizer migration.
