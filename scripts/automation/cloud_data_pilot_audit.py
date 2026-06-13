#!/usr/bin/env python3
"""Audit Cloud Data Pilot v1 append-only candle files."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
TIMEFRAME_MINUTES = {"5m": 5, "1h": 60, "4h": 240, "1d": 1440}


def repo_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else REPO_ROOT / candidate


def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def audit_symbol(path: Path, timeframe: str) -> dict[str, Any]:
    timestamps: list[str] = []
    duplicate_count = 0
    seen: set[str] = set()
    if path.exists():
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                key = row.get("timestamp_utc", "")
                if key in seen:
                    duplicate_count += 1
                elif key:
                    seen.add(key)
                    timestamps.append(key)

    timestamps = sorted(timestamps)
    gap_count = 0
    if len(timestamps) > 1:
        step = timedelta(minutes=TIMEFRAME_MINUTES.get(timeframe, 5))
        parsed = [parse_ts(value) for value in timestamps]
        for before, after in zip(parsed, parsed[1:]):
            missing = int((after - before) / step) - 1
            if missing > 0:
                gap_count += missing

    return {
        "file": str(path.relative_to(REPO_ROOT)) if path.exists() else str(path),
        "exists": path.exists(),
        "row_count": len(timestamps),
        "first_candle": timestamps[0] if timestamps else None,
        "last_candle": timestamps[-1] if timestamps else None,
        "duplicate_count": duplicate_count,
        "gap_count": gap_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Cloud Data Pilot v1 candle files for duplicates and gaps.")
    parser.add_argument("--symbols", default="configs/cloud_data_pilot_v1_symbols.json", help="Symbol config JSON.")
    parser.add_argument("--data-dir", default="data/cloud_pilot/v1", help="Cloud pilot data directory.")
    parser.add_argument("--timeframe", default="5m", choices=sorted(TIMEFRAME_MINUTES), help="Timeframe to audit.")
    parser.add_argument("--output", default="reports/cloud_data_pilot/v1/audit.json", help="Audit JSON output path.")
    args = parser.parse_args()

    config = json.loads(repo_path(args.symbols).read_text(encoding="utf-8"))
    symbols = [str(symbol).upper() for symbol in config.get("symbols", [])][:25]
    data_dir = repo_path(args.data_dir) / args.timeframe
    records = {symbol: audit_symbol(data_dir / f"{symbol}.csv", args.timeframe) for symbol in symbols}
    payload = {
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "mode": "audit",
        "symbol_count": len(symbols),
        "duplicate_count": sum(record["duplicate_count"] for record in records.values()),
        "gap_count": sum(record["gap_count"] for record in records.values()),
        "failed_symbols": [symbol for symbol, record in records.items() if not record["exists"]],
        "records": records,
        "raw_data_mutation": False,
        "scoring_changes": False,
        "trading_execution": False,
    }
    output = repo_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
