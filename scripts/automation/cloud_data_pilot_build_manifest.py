#!/usr/bin/env python3
"""Build Cloud Data Pilot v1 manifest payloads."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
REQUIRED_FIELDS = [
    "run_id",
    "started_at_utc",
    "ended_at_utc",
    "mode",
    "symbol_count_requested",
    "symbol_count_completed",
    "row_count_total",
    "row_count_by_symbol",
    "first_candle_by_symbol",
    "last_candle_by_symbol",
    "duplicate_count",
    "gap_count",
    "failed_symbols",
    "output_paths",
    "raw_data_mutation",
    "scoring_changes",
    "trading_execution",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return REPO_ROOT / candidate


def ensure_under_repo(path: Path) -> Path:
    resolved = path.resolve()
    root = REPO_ROOT.resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"Refusing path outside repository: {path}")
    return resolved


def write_json(path: str | Path, payload: dict[str, Any]) -> Path:
    target = ensure_under_repo(repo_path(path))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def build_manifest(
    *,
    run_id: str,
    started_at_utc: str,
    ended_at_utc: str,
    mode: str,
    symbols_requested: list[str],
    completed_symbols: list[str],
    row_count_by_symbol: dict[str, int],
    first_candle_by_symbol: dict[str, str | None],
    last_candle_by_symbol: dict[str, str | None],
    duplicate_count: int,
    gap_count: int,
    failed_symbols: list[dict[str, str]],
    output_paths: dict[str, str],
) -> dict[str, Any]:
    payload = {
        "run_id": run_id,
        "started_at_utc": started_at_utc,
        "ended_at_utc": ended_at_utc,
        "mode": mode,
        "symbol_count_requested": len(symbols_requested),
        "symbol_count_completed": len(completed_symbols),
        "row_count_total": sum(row_count_by_symbol.values()),
        "row_count_by_symbol": row_count_by_symbol,
        "first_candle_by_symbol": first_candle_by_symbol,
        "last_candle_by_symbol": last_candle_by_symbol,
        "duplicate_count": duplicate_count,
        "gap_count": gap_count,
        "failed_symbols": failed_symbols,
        "output_paths": output_paths,
        "raw_data_mutation": mode == "execute",
        "scoring_changes": False,
        "trading_execution": False,
    }
    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    if missing:
        raise ValueError(f"Manifest missing required fields: {missing}")
    if mode == "dry_run":
        payload["raw_data_mutation"] = False
    return payload


def summarize_csv(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"rows": 0, "first": None, "last": None}
    timestamps: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            timestamp = row.get("timestamp_utc")
            if timestamp:
                timestamps.append(timestamp)
    timestamps = sorted(set(timestamps))
    return {
        "rows": len(timestamps),
        "first": timestamps[0] if timestamps else None,
        "last": timestamps[-1] if timestamps else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Cloud Data Pilot v1 manifest from existing CSV files.")
    parser.add_argument("--symbols", required=True, help="Path to Cloud Data Pilot symbol config JSON.")
    parser.add_argument("--data-dir", default="data/cloud_pilot/v1", help="Cloud pilot data directory.")
    parser.add_argument("--timeframe", default="5m", help="Candle timeframe to summarize.")
    parser.add_argument("--manifest", default="reports/cloud_data_pilot/v1/manifest.json", help="Manifest output path.")
    args = parser.parse_args()

    config = json.loads(repo_path(args.symbols).read_text(encoding="utf-8"))
    symbols = [str(symbol).upper() for symbol in config.get("symbols", [])][:25]
    row_counts: dict[str, int] = {}
    first: dict[str, str | None] = {}
    last: dict[str, str | None] = {}
    data_dir = repo_path(args.data_dir) / args.timeframe
    for symbol in symbols:
        summary = summarize_csv(data_dir / f"{symbol}.csv")
        row_counts[symbol] = int(summary["rows"])
        first[symbol] = summary["first"]
        last[symbol] = summary["last"]

    now = utc_now()
    manifest = build_manifest(
        run_id=f"manifest-{now.replace(':', '').replace('-', '')}",
        started_at_utc=now,
        ended_at_utc=now,
        mode="audit",
        symbols_requested=symbols,
        completed_symbols=[symbol for symbol, count in row_counts.items() if count > 0],
        row_count_by_symbol=row_counts,
        first_candle_by_symbol=first,
        last_candle_by_symbol=last,
        duplicate_count=0,
        gap_count=0,
        failed_symbols=[],
        output_paths={"manifest": args.manifest, "data_dir": args.data_dir},
    )
    write_json(args.manifest, manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
