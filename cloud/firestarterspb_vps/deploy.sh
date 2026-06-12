#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  echo "[deploy] Missing .env. Copy .env.example to .env and replace placeholders." >&2
  exit 2
fi

echo "[deploy] Validating Docker Compose"
docker compose --env-file .env config >/tmp/firestarterspb_compose_config.yml

echo "[deploy] Pulling images"
docker compose --env-file .env pull

echo "[deploy] Starting services"
docker compose --env-file .env up -d

echo "[deploy] Service status"
docker compose --env-file .env ps
