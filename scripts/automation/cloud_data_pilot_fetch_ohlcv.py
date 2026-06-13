#!/usr/bin/env python3
"""Dry-run-first OHLCV collector scaffold for Cloud Data Pilot v1."""

from __future__ import annotations

import argparse
import csv
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from cloud_data_pilot_build_manifest import build_manifest, write_json


REPO_ROOT = Path(__file__).resolve().parents[2]
APPROVED_OUTPUT_ROOT = REPO_ROOT / "data" / "cloud_pilot" / "v1"
APPROVED_REPORT_ROOT = REPO_ROOT / "reports" / "cloud_data_pilot" / "v1"
TIMEFRAME_MINUTES = {"5m": 5, "1h": 60, "4h": 240, "1d": 1440}
CSV_FIELDS = [
    "symbol",
    "timestamp_utc",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "source",
    "timeframe",
    "ingested_at_utc",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else REPO_ROOT / candidate


def ensure_under(path: Path, root: Path) -> Path:
    resolved = path.resolve()
    resolved_root = root.resolve()
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise ValueError(f"Refusing path outside approved root: {path}")
    return resolved


def load_symbols(path: Path) -> tuple[list[str], str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    symbols = [str(symbol).strip().upper() for symbol in payload.get("symbols", []) if str(symbol).strip()]
    symbols = symbols[:25]
    if not symbols:
        raise ValueError("Symbol config must contain at least one symbol.")
    return symbols, str(payload.get("status", "UNKNOWN"))


def fetch_binance_klines(symbol: str, timeframe: str, days: int) -> list[dict[str, str]]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    end_ms = int(end.timestamp() * 1000)
    next_start_ms = int(start.timestamp() * 1000)
    interval_ms = TIMEFRAME_MINUTES[timeframe] * 60 * 1000
    rows: list[list[Any]] = []
    while next_start_ms < end_ms:
        params = urllib.parse.urlencode(
            {
                "symbol": symbol,
                "interval": timeframe,
                "startTime": next_start_ms,
                "endTime": end_ms,
                "limit": 1000,
            }
        )
        url = f"https://api.binance.com/api/v3/klines?{params}"
        with urllib.request.urlopen(url, timeout=30) as response:
            batch = json.loads(response.read().decode("utf-8"))
        if not batch:
            break
        rows.extend(batch)
        next_start_ms = int(batch[-1][0]) + interval_ms
        if len(batch) < 1000:
            break
    ingested = utc_now()
    candles: list[dict[str, str]] = []
    for row in rows:
        timestamp = datetime.fromtimestamp(row[0] / 1000, tz=timezone.utc).replace(microsecond=0).isoformat()
        candles.append(
            {
                "symbol": symbol,
                "timestamp_utc": timestamp,
                "open": str(row[1]),
                "high": str(row[2]),
                "low": str(row[3]),
                "close": str(row[4]),
                "volume": str(row[5]),
                "source": "binance_public_klines",
                "timeframe": timeframe,
                "ingested_at_utc": ingested,
            }
        )
    return candles


def existing_keys(path: Path, symbol: str, timeframe: str) -> set[tuple[str, str, str]]:
    keys: set[tuple[str, str, str]] = set()
    if not path.exists():
        return keys
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            keys.add((row.get("symbol", ""), row.get("timestamp_utc", ""), row.get("timeframe", "")))
    return {(item_symbol, timestamp, item_timeframe) for item_symbol, timestamp, item_timeframe in keys if item_symbol == symbol and item_timeframe == timeframe}


def append_candles(path: Path, candles: list[dict[str, str]], symbol: str, timeframe: str) -> tuple[int, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    known = existing_keys(path, symbol, timeframe)
    new_rows = [row for row in candles if (row["symbol"], row["timestamp_utc"], row["timeframe"]) not in known]
    duplicate_count = len(candles) - len(new_rows)
    needs_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        if needs_header:
            writer.writeheader()
        for row in new_rows:
            writer.writerow(row)
    return len(new_rows), duplicate_count


def write_report(path: Path, manifest: dict[str, Any], symbol_status: str, execute_skipped: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Cloud Data Pilot v1 Run Report",
        "",
        f"Run ID: `{manifest['run_id']}`",
        f"Mode: `{manifest['mode']}`",
        f"Symbol config status: `{symbol_status}`",
        f"Symbols requested: {manifest['symbol_count_requested']}",
        f"Symbols completed: {manifest['symbol_count_completed']}",
        f"Rows planned/written: {manifest['row_count_total']}",
        f"Duplicate count: {manifest['duplicate_count']}",
        f"Gap count: {manifest['gap_count']}",
        f"Execute skipped: {str(execute_skipped).lower()}",
        "",
        "Safety flags:",
        "",
        f"- raw_data_mutation: `{str(manifest['raw_data_mutation']).lower()}`",
        f"- scoring_changes: `{str(manifest['scoring_changes']).lower()}`",
        f"- trading_execution: `{str(manifest['trading_execution']).lower()}`",
        "",
        "Failed symbols:",
        "",
    ]
    if manifest["failed_symbols"]:
        lines.extend(f"- `{item['symbol']}`: {item['error']}" for item in manifest["failed_symbols"])
    else:
        lines.append("- None")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def planned_count(days: int, timeframe: str) -> int:
    return int(days * 24 * 60 / TIMEFRAME_MINUTES[timeframe])


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch or plan Cloud Data Pilot v1 public OHLCV baseline data.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Plan collection without writing market data. Default.")
    mode.add_argument("--execute", action="store_true", help="Fetch public OHLCV data and append new candles.")
    parser.add_argument("--symbols", required=True, help="Path to Cloud Data Pilot v1 symbols JSON.")
    parser.add_argument("--timeframe", default="5m", choices=sorted(TIMEFRAME_MINUTES), help="OHLCV timeframe.")
    parser.add_argument("--days", type=int, default=30, help="Lookback days. Supports 30 to 60 days.")
    parser.add_argument("--output-dir", default="data/cloud_pilot/v1", help="Approved cloud pilot data directory.")
    parser.add_argument("--manifest", default="reports/cloud_data_pilot/v1/manifest.json", help="Manifest output path.")
    parser.add_argument("--report", default="reports/cloud_data_pilot/v1/report.md", help="Run report output path.")
    args = parser.parse_args()

    if args.days < 30 or args.days > 60:
        raise ValueError("--days must be between 30 and 60 for Cloud Data Pilot v1.")

    symbols_path = repo_path(args.symbols)
    output_dir = ensure_under(repo_path(args.output_dir), APPROVED_OUTPUT_ROOT)
    manifest_path = ensure_under(repo_path(args.manifest), APPROVED_REPORT_ROOT)
    report_path = ensure_under(repo_path(args.report), APPROVED_REPORT_ROOT)
    symbols, symbol_status = load_symbols(symbols_path)
    mode = "execute" if args.execute else "dry_run"
    started = utc_now()
    run_id = f"cloud-data-pilot-v1-{started.replace(':', '').replace('-', '')}"

    row_count_by_symbol: dict[str, int] = {}
    first_candle_by_symbol: dict[str, str | None] = {}
    last_candle_by_symbol: dict[str, str | None] = {}
    failed_symbols: list[dict[str, str]] = []
    completed_symbols: list[str] = []
    duplicate_count = 0
    expected = planned_count(args.days, args.timeframe)

    for symbol in symbols:
        try:
            if mode == "dry_run":
                row_count_by_symbol[symbol] = expected
                first_candle_by_symbol[symbol] = None
                last_candle_by_symbol[symbol] = None
                completed_symbols.append(symbol)
                continue

            candles = fetch_binance_klines(symbol, args.timeframe, args.days)
            target = output_dir / args.timeframe / f"{symbol}.csv"
            written, duplicates = append_candles(target, candles, symbol, args.timeframe)
            duplicate_count += duplicates
            row_count_by_symbol[symbol] = written
            first_candle_by_symbol[symbol] = candles[0]["timestamp_utc"] if candles else None
            last_candle_by_symbol[symbol] = candles[-1]["timestamp_utc"] if candles else None
            completed_symbols.append(symbol)
        except Exception as exc:  # noqa: BLE001 - failure is captured in manifest.
            row_count_by_symbol[symbol] = 0
            first_candle_by_symbol[symbol] = None
            last_candle_by_symbol[symbol] = None
            failed_symbols.append({"symbol": symbol, "error": str(exc)})

    ended = utc_now()
    manifest = build_manifest(
        run_id=run_id,
        started_at_utc=started,
        ended_at_utc=ended,
        mode=mode,
        symbols_requested=symbols,
        completed_symbols=completed_symbols,
        row_count_by_symbol=row_count_by_symbol,
        first_candle_by_symbol=first_candle_by_symbol,
        last_candle_by_symbol=last_candle_by_symbol,
        duplicate_count=duplicate_count,
        gap_count=0,
        failed_symbols=failed_symbols,
        output_paths={
            "output_dir": output_dir.relative_to(REPO_ROOT).as_posix(),
            "manifest": manifest_path.relative_to(REPO_ROOT).as_posix(),
            "report": report_path.relative_to(REPO_ROOT).as_posix(),
        },
    )
    write_json(manifest_path, manifest)
    write_report(report_path, manifest, symbol_status, execute_skipped=mode == "dry_run")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0 if not failed_symbols else 1


if __name__ == "__main__":
    raise SystemExit(main())
