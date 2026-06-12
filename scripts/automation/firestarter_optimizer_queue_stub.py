#!/usr/bin/env python3
"""Create a safe Phase 1 optimizer-prep queue placeholder."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = Path(os.environ.get("FIRESTARTER_CLOUD_STATE_DIR", REPO_ROOT / "state" / "cloud"))
LOG_DIR = Path(os.environ.get("FIRESTARTER_CLOUD_LOG_DIR", REPO_ROOT / "logs" / "cloud"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def append_log(message: str) -> None:
    ensure_dirs()
    with (LOG_DIR / "optimizer_queue_stub.log").open("a", encoding="utf-8") as handle:
        handle.write(f"{utc_now()} {message}\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a no-ML, no-trading optimizer queue stub.")
    parser.add_argument("--dry-run", action="store_true", help="Write status only. Default.")
    parser.add_argument("--execute", action="store_true", help="Create an empty queue stub file.")
    args = parser.parse_args()

    ensure_dirs()
    queue_payload = {
        "timestamp_utc": utc_now(),
        "schema": "firestarter_optimizer_queue_stub_v1",
        "items": [],
        "ml_enabled": False,
        "trading_enabled": False,
        "scoring_changes": False,
        "notes": "Phase 1 placeholder only. No optimizer is active.",
    }
    status = {
        "timestamp_utc": queue_payload["timestamp_utc"],
        "ok": True,
        "mode": "execute" if args.execute else "dry_run",
        "queue_path": str(STATE_DIR / "optimizer_queue_stub.json"),
        "queued_items": 0,
        "raw_data_mutation": False,
        "trading_execution": False,
        "ml_enabled": False,
    }
    if args.execute:
        write_json(STATE_DIR / "optimizer_queue_stub.json", queue_payload)

    write_json(STATE_DIR / "optimizer_queue_stub_status.json", status)
    append_log(f"mode={status['mode']} queued_items=0")
    print(json.dumps(status, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
