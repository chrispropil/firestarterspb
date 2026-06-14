#!/usr/bin/env bash
set -u -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"

STATE_DIR="${REPO_ROOT}/state/cloud_pattern_watch"
LOG_DIR="${REPO_ROOT}/logs/cloud"
TRIAL_STATUS_PATH="${STATE_DIR}/cell1_scheduler_trial_status.json"
TRIAL_COUNTER_PATH="${STATE_DIR}/cell1_scheduler_trial_counter.txt"
TRIAL_LOG_PATH="${LOG_DIR}/cell1_scheduler_trial.log"
TICK_STATUS_PATH="${STATE_DIR}/cell1_scheduler_tick_status.json"
MAX_RUNS="${CELL1_TRIAL_MAX_RUNS:-16}"
INTERVAL_LABEL="${CELL1_TRIAL_INTERVAL_LABEL:-15m}"

mkdir -p "${STATE_DIR}" "${LOG_DIR}"

if [ ! -f "${TRIAL_COUNTER_PATH}" ]; then
  echo "0" > "${TRIAL_COUNTER_PATH}"
fi

RUN_COUNT="$(cat "${TRIAL_COUNTER_PATH}" 2>/dev/null || echo 0)"
case "${RUN_COUNT}" in
  ''|*[!0-9]*) RUN_COUNT=0 ;;
esac

TS_START="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

if [ "${RUN_COUNT}" -ge "${MAX_RUNS}" ]; then
  printf '%s trial_tick skipped: max_runs reached run_count=%s max_runs=%s\n' "${TS_START}" "${RUN_COUNT}" "${MAX_RUNS}" >> "${TRIAL_LOG_PATH}"
  cat > "${TRIAL_STATUS_PATH}" <<JSON
{
  "timestamp_utc": "${TS_START}",
  "status": "TRIAL_COMPLETE_MAX_RUNS_REACHED",
  "run_count": ${RUN_COUNT},
  "max_runs": ${MAX_RUNS},
  "interval_label": "${INTERVAL_LABEL}",
  "tick_executed": false,
  "scheduler_activation": "trial_only",
  "pattern_watch_send": false,
  "n8n_activation": false,
  "trading_execution": false,
  "next_action": "remove trial cron after review"
}
JSON
  exit 0
fi

NEXT_RUN_COUNT=$((RUN_COUNT + 1))
echo "${NEXT_RUN_COUNT}" > "${TRIAL_COUNTER_PATH}"
printf '%s trial_tick start run=%s max_runs=%s\n' "${TS_START}" "${NEXT_RUN_COUNT}" "${MAX_RUNS}" >> "${TRIAL_LOG_PATH}"

TICK_EXIT=0
scripts/local/cloud_cell1_scheduler_tick.sh >> "${TRIAL_LOG_PATH}" 2>&1 || TICK_EXIT=$?

TS_END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TICK_STATUS="UNKNOWN"
COVERAGE_THRESHOLD_MET="false"
ADAPTER_SYMBOLS_ACCEPTED=0
if [ -f "${TICK_STATUS_PATH}" ]; then
  TICK_SUMMARY="$(python - <<'PY'
import json
from pathlib import Path
p = Path('state/cloud_pattern_watch/cell1_scheduler_tick_status.json')
payload = json.loads(p.read_text(encoding='utf-8'))
print(json.dumps({
    'status': str(payload.get('status') or 'UNKNOWN'),
    'coverage_threshold_met': bool(payload.get('coverage_threshold_met')),
    'adapter_symbols_accepted': int(payload.get('adapter_symbols_accepted') or 0),
}))
PY
)"
  TICK_STATUS="$(python -c "import json,sys; print(json.loads(sys.argv[1])['status'])" "${TICK_SUMMARY}")"
  COVERAGE_THRESHOLD_MET="$(python -c "import json,sys; print(str(json.loads(sys.argv[1])['coverage_threshold_met']).lower())" "${TICK_SUMMARY}")"
  ADAPTER_SYMBOLS_ACCEPTED="$(python -c "import json,sys; print(json.loads(sys.argv[1])['adapter_symbols_accepted'])" "${TICK_SUMMARY}")"
fi

if [ "${TICK_EXIT}" -eq 0 ] && { [ "${TICK_STATUS}" = "PASS" ] || [ "${TICK_STATUS}" = "PASS_WITH_PRODUCER_WARNINGS" ]; }; then
  TRIAL_STATUS="TRIAL_TICK_PASS"
else
  TRIAL_STATUS="TRIAL_TICK_FAIL"
fi

cat > "${TRIAL_STATUS_PATH}" <<JSON
{
  "timestamp_utc": "${TS_END}",
  "started_utc": "${TS_START}",
  "status": "${TRIAL_STATUS}",
  "run_count": ${NEXT_RUN_COUNT},
  "max_runs": ${MAX_RUNS},
  "interval_label": "${INTERVAL_LABEL}",
  "tick_executed": true,
  "tick_exit_code": ${TICK_EXIT},
  "tick_status": "${TICK_STATUS}",
  "coverage_threshold_met": ${COVERAGE_THRESHOLD_MET},
  "adapter_symbols_accepted": ${ADAPTER_SYMBOLS_ACCEPTED},
  "scheduler_activation": "trial_only",
  "pattern_watch_send": false,
  "n8n_activation": false,
  "trading_execution": false,
  "log_path": "logs/cloud/cell1_scheduler_trial.log",
  "tick_status_path": "state/cloud_pattern_watch/cell1_scheduler_tick_status.json"
}
JSON

printf '%s trial_tick end status=%s run=%s max_runs=%s tick_status=%s adapter_symbols_accepted=%s\n' "${TS_END}" "${TRIAL_STATUS}" "${NEXT_RUN_COUNT}" "${MAX_RUNS}" "${TICK_STATUS}" "${ADAPTER_SYMBOLS_ACCEPTED}" >> "${TRIAL_LOG_PATH}"
exit 0
