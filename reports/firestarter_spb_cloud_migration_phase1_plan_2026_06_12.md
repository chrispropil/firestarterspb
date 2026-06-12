# FirestarterSPB Cloud Migration Phase 1 Plan - 2026-06-12

## Summary

This package prepares FirestarterSPB for a low-cost Ubuntu VPS using Docker Compose. Phase 1 is control, research automation, viewer refresh orchestration, dashboard hosting, logs, health checks, and optimizer-prep only.

It does not add live trading, exchange order execution, Cell 2, scoring changes, raw data mutation, secrets, recursive n8n workflows, or arbitrary shell execution from webhooks.

## Recommended VPS

- Ubuntu 24.04 LTS
- 2 vCPU
- 4 GB RAM
- 40 to 80 GB disk
- Docker Compose
- Cost class: approximately 20 USD per month before optional backups or monitoring add-ons

## What Moves To Cloud

- n8n control workflows with Schedule Trigger cadence.
- Postgres-backed n8n persistence.
- Fixed-action Firestarter worker for health checks, viewer-refresh dry runs, result collection, and optimizer queue stubbing.
- Read-only dashboard hosting from `reports/html`.
- Persistent runtime logs under `logs/cloud`.
- Persistent status files under `state/cloud`.

## What Stays Local

- Active trading decisions.
- Exchange credentials and any private keys.
- Raw local research data unless separately approved.
- FireSignal 5-minute updater ownership.
- Active OG symbol expansion decisions.
- Formula/scoring research lanes.

## Service Architecture

- `postgres`: n8n database.
- `n8n`: scheduler/operator UI, with basic-auth placeholders and Postgres.
- `firestarter-worker`: Python standard-library HTTP worker with fixed routes only.
- `dashboard`: nginx serving generated dashboards read-only.

The worker exposes `/health`, `/run/viewer-refresh`, `/run/result-collector`, and `/run/optimizer-queue-stub`. These routes ignore webhook payloads and call fixed local scripts only.

## n8n Workflow List

- `automation/n8n_cloud_auto_viewer_refresh.json`
- `automation/n8n_cloud_health_check.json`
- `automation/n8n_cloud_result_collector.json`
- `automation/n8n_cloud_optimizer_queue_stub.json`

All workflows use Schedule Trigger nodes. None call themselves. None accept arbitrary shell commands from payloads.

## Deployment Commands

```bash
cd cloud/firestarterspb_vps
cp .env.example .env
nano .env
./setup_ubuntu.sh
./deploy.sh
```

Import the workflow JSON files into n8n after the stack is running.

## Security Checklist

- Replace all `.env` placeholders before deploy.
- Keep `.env` out of git.
- Use long random values for Postgres, n8n basic auth, and n8n encryption key.
- Keep n8n on localhost unless a TLS reverse proxy is configured.
- Keep worker routes internal and fixed-action only.
- Do not import recursive workflows.
- Do not add webhook payload command execution.
- Keep raw data and generated HTML out of commits unless separately approved.

## Secrets Handling

Only `.env.example` is committed. Real secrets belong in `.env` on the VPS or a provider secret store. No API keys, exchange keys, or production passwords are included.

## Backup Plan

Use `cloud/firestarterspb_vps/backup.sh` to export the n8n Postgres database and archive logs, state, workflow exports, and cloud config templates. The script excludes `.env`.

## Rollback Plan

Stop the Docker Compose stack, checkout the previous git revision, restore the previous n8n database dump, and redeploy. Generated dashboards are served read-only and can be restored from approved backups.

## Acceptance Tests

- Docker Compose config validates with `.env.example` where Docker is available.
- Python automation scripts expose `--help` and default to dry-run or status-only behavior.
- n8n workflow exports parse as JSON.
- No secrets are committed.
- No raw data files are committed.
- No trading, scanner, or scoring mutation is introduced.
- No workflow calls itself.

## 25-Symbol Pilot Note

The 25-symbol pilot is locally feasible. `SHIBUSDT` and `POLUSDT` are missing from the exact preferred list. Available local replacements are `1000SHIBUSDT` and `1000PEPEUSDT`.

The active OG lane currently uses the existing 8-symbol path. This cloud package does not update the active symbol list. Symbol expansion remains pending user approval of the final list.

## Known Risks

- VPS disk can fill if generated reports or logs are not rotated.
- n8n must be protected by basic auth and ideally TLS before any public exposure.
- Enabling worker execution before reviewing approved builders could refresh generated reports unexpectedly.
- Dashboard hosting is read-only, but generated HTML should still remain outside commits unless separately approved.

## Future Phase 2 Optimizer Path

Phase 2 can replace the queue stub with a reviewed optimizer-prep service that reads approved summaries, writes explainable proposals, and remains blocked from exchange execution. Any ML, scoring, or execution change should require a separate design review.
