#!/usr/bin/env bash
set -u -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"

STATE_DIR="${REPO_ROOT}/state/cloud_pattern_watch"
LOG_DIR="${REPO_ROOT}/logs/cloud"
STATUS_PATH="${STATE_DIR}/cell1_scheduler_tick_status.json"
LOCK_PATH="${STATE_DIR}/cell1_scheduler_tick.lock"
LOG_PATH="${LOG_DIR}/cell1_scheduler_tick.log"

mkdir -p "${STATE_DIR}" "${LOG_DIR}"

exec 9>"${LOCK_PATH}"
if ! flock -n 9; then
  TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '%s scheduler_tick skipped: lock already held\n' "${TS}" >> "${LOG_PATH}"
  cat > "${STATUS_PATH}" <<JSON
{
  "timestamp_utc": "${TS}",
  "status": "SKIPPED_LOCK_HELD",
  "producer_exit_code": null,
  "adapter_exit_code": null,
  "snapshot_adapter_write": false,
  "pattern_watch_send": false,
  "scheduler_activation": false,
  "n8n_activation": false,
  "trading_execution": false
}
JSON
  exit 0
fi

TS_START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
printf '%s scheduler_tick start\n' "${TS_START}" >> "${LOG_PATH}"

if [ -f "${REPO_ROOT}/.venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "${REPO_ROOT}/.venv/bin/activate"
fi

PRODUCER_EXIT=0
python scripts/automation/cloud_cell1_metric_producer_v1.py \
  --manual-build \
  --confirm-manual-build CELL1_MANUAL_BUILD_APPROVED >> "${LOG_PATH}" 2>&1 || PRODUCER_EXIT=$?

ADAPTER_EXIT=0
python scripts/automation/cloud_metric_snapshot_adapter_v1.py --write >> "${LOG_PATH}" 2>&1 || ADAPTER_EXIT=$?

TS_END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ "${PRODUCER_EXIT}" -eq 0 ] && [ "${ADAPTER_EXIT}" -eq 0 ]; then
  STATUS="PASS"
else
  STATUS="FAIL"
fi

cat > "${STATUS_PATH}" <<JSON
{
  "timestamp_utc": "${TS_END}",
  "started_utc": "${TS_START}",
  "status": "${STATUS}",
  "producer_exit_code": ${PRODUCER_EXIT},
  "adapter_exit_code": ${ADAPTER_EXIT},
  "snapshot_adapter_write": true,
  "pattern_watch_send": false,
  "scheduler_activation": false,
  "n8n_activation": false,
  "trading_execution": false,
  "log_path": "logs/cloud/cell1_scheduler_tick.log"
}
JSON

printf '%s scheduler_tick end status=%s producer_exit=%s adapter_exit=%s\n' "${TS_END}" "${STATUS}" "${PRODUCER_EXIT}" "${ADAPTER_EXIT}" >> "${LOG_PATH}"
exit 0
