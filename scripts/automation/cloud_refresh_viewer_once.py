#!/usr/bin/env python3
"""Safely prepare or run approved FirestarterSPB viewer refresh scripts."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = Path(os.environ.get("FIRESTARTER_CLOUD_STATE_DIR", REPO_ROOT / "state" / "cloud"))
LOG_DIR = Path(os.environ.get("FIRESTARTER_CLOUD_LOG_DIR", REPO_ROOT / "logs" / "cloud"))

APPROVED_BUILDERS = {
    "true_og_local_viewer": Path("scripts/firestarterog_binance_1m_local_viewer.py"),
    "core88_evidence_viewer": Path("scripts/visualization/build_core88_evidence_viewer.py"),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def append_log(message: str) -> None:
    ensure_dirs()
    with (LOG_DIR / "viewer_refresh.log").open("a", encoding="utf-8") as handle:
        handle.write(f"{utc_now()} {message}\n")


def write_status(payload: dict[str, Any]) -> None:
    ensure_dirs()
    (STATE_DIR / "viewer_refresh_status.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_builder(name: str) -> dict[str, Any]:
    rel_path = APPROVED_BUILDERS[name]
    script_path = REPO_ROOT / rel_path
    if not script_path.exists():
        return {"builder": name, "ok": False, "error": f"missing {rel_path.as_posix()}"}

    command = [sys.executable, str(script_path)]
    completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True, check=False)
    return {
        "builder": name,
        "ok": completed.returncode == 0,
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout[-2000:],
        "stderr_tail": completed.stderr[-2000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an approved FirestarterSPB viewer refresh once.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Plan the refresh without running builders. Default.")
    mode.add_argument("--execute", action="store_true", help="Run approved builders.")
    parser.add_argument(
        "--builder",
        action="append",
        choices=sorted(APPROVED_BUILDERS),
        help="Approved builder to include. Defaults to true_og_local_viewer.",
    )
    args = parser.parse_args()

    builders = args.builder or ["true_og_local_viewer"]
    execute = bool(args.execute)
    payload: dict[str, Any] = {
        "timestamp_utc": utc_now(),
        "ok": True,
        "mode": "execute" if execute else "dry_run",
        "builders": builders,
        "raw_data_mutation": False,
        "trading_execution": False,
        "scoring_changes": False,
        "results": [],
    }

    append_log(f"start mode={payload['mode']} builders={builders}")
    if execute:
        for builder in builders:
            result = run_builder(builder)
            payload["results"].append(result)
            if not result["ok"]:
                payload["ok"] = False
    else:
        payload["results"] = [
            {
                "builder": builder,
                "ok": (REPO_ROOT / APPROVED_BUILDERS[builder]).exists(),
                "planned_script": APPROVED_BUILDERS[builder].as_posix(),
            }
            for builder in builders
        ]
        payload["ok"] = all(result["ok"] for result in payload["results"])

    write_status(payload)
    append_log(f"end ok={payload['ok']}")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
