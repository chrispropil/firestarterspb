#!/usr/bin/env python3
"""Collect Phase 1 cloud status files into a small operator summary."""

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
    with (LOG_DIR / "result_collector.log").open("a", encoding="utf-8") as handle:
        handle.write(f"{utc_now()} {message}\n")


def load_status_files() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not STATE_DIR.exists():
        return records

    for path in sorted(STATE_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            records.append({"file": path.name, "ok": payload.get("ok"), "timestamp_utc": payload.get("timestamp_utc")})
        except json.JSONDecodeError as exc:
            records.append({"file": path.name, "ok": False, "error": str(exc)})
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect FirestarterSPB cloud runtime status files.")
    parser.add_argument("--dry-run", action="store_true", help="Write status only. Default.")
    parser.add_argument("--execute", action="store_true", help="Also write a report summary JSON.")
    args = parser.parse_args()

    records = load_status_files()
    payload = {
        "timestamp_utc": utc_now(),
        "ok": all(record.get("ok") is not False for record in records),
        "mode": "execute" if args.execute else "dry_run",
        "status_count": len(records),
        "records": records,
        "raw_data_mutation": False,
        "trading_execution": False,
        "scoring_changes": False,
    }

    ensure_dirs()
    (STATE_DIR / "result_collector_status.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if args.execute:
        reports_dir = REPO_ROOT / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        (reports_dir / "cloud_result_collector_summary.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    append_log(f"collected status_count={len(records)} ok={payload['ok']}")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
