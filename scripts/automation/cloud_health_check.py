#!/usr/bin/env python3
"""Phase 1 cloud health check and fixed-action worker for FirestarterSPB."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = Path(os.environ.get("FIRESTARTER_CLOUD_STATE_DIR", REPO_ROOT / "state" / "cloud"))
LOG_DIR = Path(os.environ.get("FIRESTARTER_CLOUD_LOG_DIR", REPO_ROOT / "logs" / "cloud"))

TASKS = {
    "viewer-refresh": ["cloud_refresh_viewer_once.py", "--dry-run"],
    "result-collector": ["cloud_result_collector.py", "--dry-run"],
    "optimizer-queue-stub": ["firestarter_optimizer_queue_stub.py", "--dry-run"],
    "cloud-data-pilot-dryrun": [
        "cloud_data_pilot_fetch_ohlcv.py",
        "--dry-run",
        "--symbols",
        "configs/cloud_data_pilot_v1_symbols.json",
        "--timeframe",
        "5m",
        "--days",
        "30",
        "--output-dir",
        "data/cloud_pilot/v1",
        "--manifest",
        "reports/cloud_data_pilot/v1/manifest.json",
        "--report",
        "reports/cloud_data_pilot/v1/report.md",
    ],
    "cloud-alert-bridge-dryrun": [
        "cloud_alert_bridge.py",
        "--event-type",
        "baseline_audit",
        "--dry-run",
    ],
    "cloud-alert-bridge-send-baseline-audit": [
        "cloud_alert_bridge.py",
        "--event-type",
        "baseline_audit",
        "--send",
    ],
    "cloud-alert-bridge-send-health": [
        "cloud_alert_bridge.py",
        "--event-type",
        "health",
        "--send",
    ],
    "cloud-alert-bridge-send-manual-test": [
        "cloud_alert_bridge.py",
        "--event-type",
        "manual_test",
        "--message",
        "Cloud Alert Bridge v1 manual worker-route test. Research only. No scoring/trading.",
        "--send",
    ],
    "cloud-research-pattern-dryrun": [
        "cloud_pattern_watch_v1.py",
        "--sample",
        "--dry-run",
    ],
    "cloud-research-pattern-send-test": [
        "cloud_pattern_watch_v1.py",
        "--sample",
        "--send",
    ],
    "cloud-metric-snapshot-dryrun": [
        "cloud_metric_snapshot_adapter_v1.py",
        "--dry-run",
    ],
    "cloud-metric-snapshot-build": [
        "cloud_metric_snapshot_adapter_v1.py",
        "--write",
    ],
    "cloud-research-pattern-current-dryrun": [
        "cloud_pattern_watch_v1.py",
        "--dry-run",
    ],
    "cloud-research-pattern-current-send": [
        "cloud_pattern_watch_v1.py",
        "--send",
    ],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def append_log(name: str, message: str) -> None:
    ensure_dirs()
    with (LOG_DIR / name).open("a", encoding="utf-8") as handle:
        handle.write(f"{utc_now()} {message}\n")


def write_status(name: str, payload: dict[str, Any]) -> Path:
    ensure_dirs()
    path = STATE_DIR / name
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def run_health() -> dict[str, Any]:
    checks = {
        "repo_root_exists": REPO_ROOT.exists(),
        "scripts_dir_exists": (REPO_ROOT / "scripts").is_dir(),
        "reports_dir_exists": (REPO_ROOT / "reports").is_dir(),
        "reports_html_dir_exists": (REPO_ROOT / "reports" / "html").is_dir(),
        "logs_dir_ready": LOG_DIR.exists() or LOG_DIR.parent.exists(),
        "state_dir_ready": STATE_DIR.exists() or STATE_DIR.parent.exists(),
    }
    ok = all(value for key, value in checks.items() if key != "reports_html_dir_exists")
    payload = {
        "timestamp_utc": utc_now(),
        "ok": ok,
        "mode": "research_control_only",
        "checks": checks,
        "boundaries": {
            "live_trading": False,
            "exchange_execution": False,
            "cell_2": False,
            "scoring_changes": False,
            "raw_data_mutation": False,
        },
    }
    write_status("health_status.json", payload)
    append_log("health_check.log", f"health ok={ok}")
    return payload


def run_fixed_task(task_name: str) -> dict[str, Any]:
    if task_name not in TASKS:
        return {"timestamp_utc": utc_now(), "ok": False, "error": "unknown fixed task"}

    script_name, *args = TASKS[task_name]
    command = [sys.executable, str(REPO_ROOT / "scripts" / "automation" / script_name), *args]
    append_log("worker.log", f"start task={task_name} command={command}")
    completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    payload = {
        "timestamp_utc": utc_now(),
        "ok": completed.returncode == 0,
        "task": task_name,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
    }
    write_status(f"{task_name.replace('-', '_')}_worker_status.json", payload)
    append_log("worker.log", f"end task={task_name} ok={payload['ok']} returncode={completed.returncode}")
    return payload


class WorkerHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - stdlib callback name
        self._handle_request()

    def do_POST(self) -> None:  # noqa: N802 - stdlib callback name
        self._handle_request()

    def _handle_request(self) -> None:
        if self.path == "/health":
            payload = run_health()
            self._send_json(200 if payload["ok"] else 503, payload)
            return

        prefix = "/run/"
        if self.path.startswith(prefix):
            task = self.path[len(prefix):].split("?", 1)[0].strip("/")
            payload = run_fixed_task(task)
            self._send_json(200 if payload.get("ok") else 500, payload)
            return

        self._send_json(404, {"timestamp_utc": utc_now(), "ok": False, "error": "not found"})

    def log_message(self, fmt: str, *args: Any) -> None:
        append_log("worker_http.log", fmt % args)


def serve(host: str, port: int) -> None:
    ensure_dirs()
    append_log("worker.log", f"serve host={host} port={port}")
    ThreadingHTTPServer((host, port), WorkerHandler).serve_forever()


def main() -> int:
    parser = argparse.ArgumentParser(description="FirestarterSPB cloud health check and fixed-action worker.")
    parser.add_argument("--once", action="store_true", help="Run one health check and exit.")
    parser.add_argument("--serve", action="store_true", help="Run the fixed-action HTTP worker.")
    parser.add_argument("--host", default="127.0.0.1", help="Worker bind host.")
    parser.add_argument("--port", type=int, default=int(os.environ.get("WORKER_PORT", "8090")), help="Worker port.")
    args = parser.parse_args()

    if args.serve:
        serve(args.host, args.port)
        return 0

    payload = run_health()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
