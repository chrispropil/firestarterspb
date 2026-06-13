# FirestarterSPB VPS Phase 1

This package prepares FirestarterSPB for a low-cost Ubuntu VPS running Docker Compose. It is for cloud control, research automation, viewer refresh orchestration, dashboard hosting, logs, health checks, and optimizer-prep only.

It does not enable live trading, exchange order execution, Cell 2, private keys, scoring changes, or raw data mutation.

## Target VPS

- Ubuntu 24.04 LTS
- 2 vCPU
- 4 GB RAM
- 40 to 80 GB disk
- Docker Engine with Docker Compose
- Approximate cost class: about 20 USD per month, depending on provider and backups

## Services

- `postgres`: durable n8n database.
- `n8n`: workflow scheduler and operator UI, protected by basic auth placeholders in `.env`.
- `firestarter-worker`: Python standard-library worker with fixed, allowlisted internal endpoints.
- `dashboard`: read-only nginx hosting for `reports/html`.

The worker exposes only fixed internal actions. It does not run arbitrary commands from webhook payloads.

## Quick Start

```bash
cd cloud/firestarterspb_vps
cp .env.example .env
nano .env
chmod +x setup_ubuntu.sh deploy.sh backup.sh
./setup_ubuntu.sh
./deploy.sh
```

Then import the workflow exports from `automation/` into n8n:

- `n8n_cloud_auto_viewer_refresh.json`
- `n8n_cloud_health_check.json`
- `n8n_cloud_result_collector.json`
- `n8n_cloud_optimizer_queue_stub.json`

The workflows use Schedule Trigger nodes and fixed worker URLs. They do not call themselves and do not expose arbitrary shell execution.

## Safe Defaults

`FIRESTARTER_CLOUD_WORKER_EXECUTE=false` keeps worker actions in dry-run mode by default. Runtime status files are written under `state/cloud`, and logs are appended under `logs/cloud`.

Viewer execution can be enabled later only after reviewing the approved builder list in `scripts/automation/cloud_refresh_viewer_once.py`.

## Dashboard

nginx serves `reports/html` read-only. Keep generated HTML out of commits unless a separate review approves it.

## 25-Symbol Pilot Note

The 25-symbol pilot is locally feasible, but it is not activated by this package. The exact preferred list is missing `SHIBUSDT` and `POLUSDT` locally. Available local replacements are `1000SHIBUSDT` and `1000PEPEUSDT`.

The active OG lane still uses the existing 8-symbol path. Symbol expansion remains pending user approval of the final list.

## Boundaries

- No live trading automation.
- No exchange order execution.
- No Cell 2 unlock.
- No unapproved scoring changes.
- No raw data mutation.
- No secrets committed.
- No recursive n8n workflows.
- No arbitrary shell from webhooks.
