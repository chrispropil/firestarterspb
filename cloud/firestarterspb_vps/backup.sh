#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  echo "[backup] Missing .env. Cannot read database settings." >&2
  exit 2
fi

set -a
# shellcheck disable=SC1091
. ./.env
set +a

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_DIR="backups/${STAMP}"
mkdir -p "${BACKUP_DIR}"

echo "[backup] Exporting Postgres database"
docker compose --env-file .env exec -T postgres pg_dump -U "${POSTGRES_USER:-n8n}" "${POSTGRES_DB:-n8n}" > "${BACKUP_DIR}/n8n_postgres.sql"

echo "[backup] Archiving logs, state, cloud config templates, and workflow exports"
tar -czf "${BACKUP_DIR}/firestarterspb_cloud_runtime.tgz" \
  --exclude='cloud/firestarterspb_vps/.env' \
  ../../logs \
  ../../state \
  ../../automation \
  ../../cloud/firestarterspb_vps

echo "[backup] Created ${BACKUP_DIR}"
