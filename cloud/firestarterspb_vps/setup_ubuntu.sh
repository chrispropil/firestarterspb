#!/usr/bin/env bash
set -euo pipefail

if [[ "$(id -u)" -eq 0 ]]; then
  SUDO=""
else
  SUDO="sudo"
fi

echo "[setup] Installing Docker prerequisites on Ubuntu 24.04"
$SUDO apt-get update
$SUDO apt-get install -y ca-certificates curl git ufw docker.io docker-compose-v2

echo "[setup] Enabling Docker"
$SUDO systemctl enable --now docker

echo "[setup] Preparing FirestarterSPB runtime directories"
mkdir -p ../../logs/cloud ../../state/cloud ../../reports/html backups

echo "[setup] Applying conservative firewall defaults"
$SUDO ufw allow OpenSSH
$SUDO ufw allow "${DASHBOARD_PORT:-8080}/tcp" || true
$SUDO ufw --force enable

echo "[setup] Done. Copy .env.example to .env and replace every placeholder before deploy."
