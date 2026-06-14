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
ADAPTER_STATUS_PATH="${STATE_DIR}/metric_snapshot_adapter_status.json"

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
  "adapter_ok": null,
  "adapter_snapshot_written": null,
  "adapter_rows_accepted": null,
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

ADAPTER_SUMMARY_JSON="$(python - <<'PY'
import json
from pathlib import Path

path = Path('state/cloud_pattern_watch/metric_snapshot_adapter_status.json')
if not path.exists():
    print(json.dumps({
        'adapter_ok': False,
        'adapter_snapshot_written': False,
        'adapter_rows_accepted': 0,
        'adapter_symbols_accepted': 0,
        'adapter_status': 'MISSING_STATUS_FILE',
    }))
else:
    payload = json.loads(path.read_text(encoding='utf-8'))
    print(json.dumps({
        'adapter_ok': bool(payload.get('ok')),
        'adapter_snapshot_written': bool(payload.get('snapshot_written')),
        'adapter_rows_accepted': int(payload.get('rows_accepted') or 0),
        'adapter_symbols_accepted': int(payload.get('symbols_accepted') or 0),
        'adapter_status': str(payload.get('status') or 'UNKNOWN'),
    }))
PY
)"

ADAPTER_OK="$(python -c "import json,sys; print(str(json.loads(sys.argv[1])['adapter_ok']).lower())" "${ADAPTER_SUMMARY_JSON}")"
ADAPTER_SNAPSHOT_WRITTEN="$(python -c "import json,sys; print(str(json.loads(sys.argv[1])['adapter_snapshot_written']).lower())" "${ADAPTER_SUMMARY_JSON}")"
ADAPTER_ROWS_ACCEPTED="$(python -c "import json,sys; print(json.loads(sys.argv[1])['adapter_rows_accepted'])" "${ADAPTER_SUMMARY_JSON}")"
ADAPTER_SYMBOLS_ACCEPTED="$(python -c "import json,sys; print(json.loads(sys.argv[1])['adapter_symbols_accepted'])" "${ADAPTER_SUMMARY_JSON}")"
ADAPTER_STATUS="$(python -c "import json,sys; print(json.loads(sys.argv[1])['adapter_status'])" "${ADAPTER_SUMMARY_JSON}")"

TS_END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ "${ADAPTER_EXIT}" -eq 0 ] && [ "${ADAPTER_OK}" = "true" ] && [ "${ADAPTER_SNAPSHOT_WRITTEN}" = "true" ] && [ "${ADAPTER_ROWS_ACCEPTED}" -gt 0 ]; then
  if [ "${PRODUCER_EXIT}" -eq 0 ]; then
    STATUS="PASS"
  else
    STATUS="PASS_WITH_PRODUCER_WARNINGS"
  fi
else
  STATUS="FAIL"
fi

cat > "${STATUS_PATH}" <<JSON
{
  "timestamp_utc": "${TS_END}",
  "started_utc": "${TS_START}",
  "status": "${STATUS}",
  "producer_exit_code": ${PRODUCER_EXIT},
  "producer_partial_allowed": true,
  "adapter_exit_code": ${ADAPTER_EXIT},
  "adapter_ok": ${ADAPTER_OK},
  "adapter_snapshot_written": ${ADAPTER_SNAPSHOT_WRITTEN},
  "adapter_rows_accepted": ${ADAPTER_ROWS_ACCEPTED},
  "adapter_symbols_accepted": ${ADAPTER_SYMBOLS_ACCEPTED},
  "adapter_status": "${ADAPTER_STATUS}",
  "snapshot_adapter_write": true,
  "pattern_watch_send": false,
  "scheduler_activation": false,
  "n8n_activation": false,
  "trading_execution": false,
  "log_path": "logs/cloud/cell1_scheduler_tick.log"
}
JSON

printf '%s scheduler_tick end status=%s producer_exit=%s adapter_exit=%s adapter_ok=%s adapter_snapshot_written=%s adapter_rows_accepted=%s\n' "${TS_END}" "${STATUS}" "${PRODUCER_EXIT}" "${ADAPTER_EXIT}" "${ADAPTER_OK}" "${ADAPTER_SNAPSHOT_WRITTEN}" "${ADAPTER_ROWS_ACCEPTED}" >> "${LOG_PATH}"
exit 0
