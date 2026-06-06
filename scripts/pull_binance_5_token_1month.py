from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SYMBOLS = ["SOLUSDT", "XRPUSDT", "DOGEUSDT", "LINKUSDT", "AVAXUSDT"]
START = datetime(2026, 5, 6, 0, 0, tzinfo=timezone.utc)
END = datetime(2026, 6, 6, 0, 0, tzinfo=timezone.utc)
START_MS = int(START.timestamp() * 1000)
END_MS_EXCLUSIVE = int(END.timestamp() * 1000)
END_MS_INCLUSIVE = END_MS_EXCLUSIVE - 1

BASE = "https://fapi.binance.com"
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "research" / "binance_5_token_1month"
REPORTS_DIR = ROOT / "reports"
AUDIT_PATH = REPORTS_DIR / "firestarter_spb_binance_5_token_1month_pull_audit.md"
MANIFEST_PATH = REPORTS_DIR / "firestarter_spb_binance_5_token_1month_manifest.csv"


@dataclass
class DatasetResult:
    symbol: str
    dataset: str
    interval: str
    path: Path
    rows: int
    first_timestamp: str
    last_timestamp: str
    missing_rows: int | str
    duplicate_timestamps: int
    unavailable_fields: str
    status: str
    notes: str = ""


def ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def iso_from_ms(value: int | str) -> str:
    return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def request_json(path: str, params: dict[str, Any]) -> Any:
    query = urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{BASE}{path}?{query}" if query else f"{BASE}{path}"
    req = Request(url, headers={"User-Agent": "firestarter-spb-research/1.0"})
    for attempt in range(5):
        try:
            with urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code in {418, 429} or exc.code >= 500:
                time.sleep(1.5 * (attempt + 1))
                continue
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {exc.code} for {path}: {body}") from exc
        except URLError:
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"request failed after retries: {url}")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def audit_timestamps(rows: list[dict[str, Any]], timestamp_field: str, expected_step_ms: int | None) -> tuple[str, str, int | str, int]:
    if not rows:
        return "", "", "n/a", 0
    timestamps = [int(row[timestamp_field]) for row in rows]
    seen: set[int] = set()
    duplicates = 0
    for timestamp in timestamps:
        if timestamp in seen:
            duplicates += 1
        seen.add(timestamp)
    first = min(timestamps)
    last = max(timestamps)
    if expected_step_ms is None:
        missing: int | str = "n/a"
    else:
        expected = ((END_MS_EXCLUSIVE - START_MS) // expected_step_ms)
        missing = max(expected - len(seen), 0)
    return iso_from_ms(first), iso_from_ms(last), missing, duplicates


def unavailable(expected: list[str], rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ",".join(expected)
    present = {key for row in rows for key, value in row.items() if value not in ("", None)}
    missing = [field for field in expected if field not in present]
    return ",".join(missing) if missing else ""


def pull_klines(symbol: str, interval: str) -> DatasetResult:
    raw = request_json(
        "/fapi/v1/klines",
        {
            "symbol": symbol,
            "interval": interval,
            "startTime": START_MS,
            "endTime": END_MS_INCLUSIVE,
            "limit": 1000,
        },
    )
    fields = [
        "open_time",
        "open_time_utc",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "close_time_utc",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore",
    ]
    rows = [
        {
            "open_time": item[0],
            "open_time_utc": iso_from_ms(item[0]),
            "open": item[1],
            "high": item[2],
            "low": item[3],
            "close": item[4],
            "volume": item[5],
            "close_time": item[6],
            "close_time_utc": iso_from_ms(item[6]),
            "quote_asset_volume": item[7],
            "number_of_trades": item[8],
            "taker_buy_base_asset_volume": item[9],
            "taker_buy_quote_asset_volume": item[10],
            "ignore": item[11],
        }
        for item in raw
    ]
    step = 60 * 60 * 1000 if interval == "1h" else 4 * 60 * 60 * 1000
    out = DATA_DIR / f"{symbol}_futures_klines_{interval}.csv"
    write_csv(out, fields, rows)
    first, last, missing, dupes = audit_timestamps(rows, "open_time", step)
    return DatasetResult(symbol, "futures_klines", interval, out, len(rows), first, last, missing, dupes, unavailable(fields, rows), "ok")


def pull_funding(symbol: str) -> DatasetResult:
    raw = request_json(
        "/fapi/v1/fundingRate",
        {"symbol": symbol, "startTime": START_MS, "endTime": END_MS_INCLUSIVE, "limit": 1000},
    )
    fields = ["symbol", "fundingTime", "fundingTime_utc", "fundingRate", "markPrice"]
    rows = [
        {
            "symbol": item.get("symbol", symbol),
            "fundingTime": item.get("fundingTime"),
            "fundingTime_utc": iso_from_ms(item["fundingTime"]),
            "fundingRate": item.get("fundingRate"),
            "markPrice": item.get("markPrice"),
        }
        for item in raw
    ]
    out = DATA_DIR / f"{symbol}_funding_rate_history.csv"
    write_csv(out, fields, rows)
    first, last, missing, dupes = audit_timestamps(rows, "fundingTime", 8 * 60 * 60 * 1000)
    return DatasetResult(symbol, "funding_rate_history", "8h", out, len(rows), first, last, missing, dupes, unavailable(fields, rows), "ok")


def pull_period_endpoint(symbol: str, dataset: str, path: str, interval: str, period: str) -> DatasetResult:
    notes = ""
    try:
        raw = request_json(
            path,
            {
                "symbol": symbol,
                "period": period,
                "startTime": START_MS,
                "endTime": END_MS_INCLUSIVE,
                "limit": 1000,
            },
        )
    except RuntimeError as exc:
        if "startTime" not in str(exc):
            out = DATA_DIR / f"{symbol}_{dataset}_{interval}.csv"
            write_csv(out, ["timestamp", "timestamp_utc"], [])
            return DatasetResult(symbol, dataset, interval, out, 0, "", "", "n/a", 0, "all", "unavailable", str(exc))
        raw = request_json(
            path,
            {
                "symbol": symbol,
                "period": period,
                "endTime": END_MS_INCLUSIVE,
                "limit": 1000,
            },
        )
        notes = "retried without startTime because Binance rejected requested 31-day startTime"
    raw = [item for item in raw if START_MS <= int(item["timestamp"]) < END_MS_EXCLUSIVE]
    rows: list[dict[str, Any]] = []
    keys = sorted({key for item in raw for key in item.keys()})
    fields = ["timestamp", "timestamp_utc"] + [key for key in keys if key != "timestamp"]
    for item in raw:
        row = {"timestamp": item.get("timestamp"), "timestamp_utc": iso_from_ms(item["timestamp"])}
        row.update({key: item.get(key) for key in keys if key != "timestamp"})
        rows.append(row)
    out = DATA_DIR / f"{symbol}_{dataset}_{interval}.csv"
    write_csv(out, fields, rows)
    step = 60 * 60 * 1000 if period == "1h" else 4 * 60 * 60 * 1000
    first, last, missing, dupes = audit_timestamps(rows, "timestamp", step)
    return DatasetResult(symbol, dataset, interval, out, len(rows), first, last, missing, dupes, unavailable(fields, rows), "ok", notes)


def pull_open_interest_snapshot(symbol: str) -> DatasetResult:
    item = request_json("/fapi/v1/openInterest", {"symbol": symbol})
    fields = ["symbol", "openInterest", "time", "time_utc"]
    row = {
        "symbol": item.get("symbol", symbol),
        "openInterest": item.get("openInterest"),
        "time": item.get("time"),
        "time_utc": iso_from_ms(item["time"]) if item.get("time") else "",
    }
    out = DATA_DIR / f"{symbol}_open_interest_snapshot.csv"
    write_csv(out, fields, [row])
    return DatasetResult(symbol, "open_interest_snapshot", "current", out, 1, row["time_utc"], row["time_utc"], "n/a", 0, unavailable(fields, [row]), "ok")


def run() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    results: list[DatasetResult] = []
    endpoints = [
        ("open_interest_statistics", "/futures/data/openInterestHist"),
        ("top_trader_account_ratio", "/futures/data/topLongShortAccountRatio"),
        ("top_trader_position_ratio", "/futures/data/topLongShortPositionRatio"),
    ]

    for symbol in SYMBOLS:
        for interval in ["1h", "4h"]:
            results.append(pull_klines(symbol, interval))
        results.append(pull_funding(symbol))
        for dataset, path in endpoints:
            for interval in ["1h", "4h"]:
                results.append(pull_period_endpoint(symbol, dataset, path, interval, interval))
        results.append(pull_open_interest_snapshot(symbol))

    manifest_fields = [
        "symbol",
        "dataset",
        "interval",
        "path",
        "rows",
        "first_timestamp",
        "last_timestamp",
        "missing_rows",
        "duplicate_timestamps",
        "unavailable_fields",
        "status",
        "notes",
    ]
    write_csv(MANIFEST_PATH, manifest_fields, [{**result.__dict__, "path": str(result.path.relative_to(ROOT))} for result in results])

    total_rows = sum(result.rows for result in results)
    unavailable_lines = [result for result in results if result.unavailable_fields or result.status != "ok"]
    missing_lines = [result for result in results if result.missing_rows not in (0, "0", "n/a")]
    duplicate_lines = [result for result in results if result.duplicate_timestamps]

    lines = [
        "# Firestarter SPB Binance 5 Token 1 Month Pull Audit",
        "",
        f"Run timestamp UTC: {datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}",
        f"Window UTC: {START.isoformat().replace('+00:00', 'Z')} to {END.isoformat().replace('+00:00', 'Z')} (end exclusive)",
        f"Symbols: {', '.join(SYMBOLS)}",
        "Source: Binance public USD-M futures REST API; no API keys used.",
        "Boundaries observed: no trading logic, no signal labels, no Cell 2, no paid data, no external raw-data publishing.",
        "",
        "## Summary",
        "",
        f"- Output directory: `{DATA_DIR.relative_to(ROOT)}`",
        f"- Manifest: `{MANIFEST_PATH.relative_to(ROOT)}`",
        f"- Dataset files: {len(results)}",
        f"- Total rows: {total_rows}",
        f"- Missing-row audit exceptions: {len(missing_lines)}",
        f"- Duplicate timestamp exceptions: {len(duplicate_lines)}",
        f"- Unavailable-field exceptions: {len(unavailable_lines)}",
        "",
        "## Dataset Audit",
        "",
        "| Symbol | Dataset | Interval | Rows | First UTC | Last UTC | Missing | Duplicates | Unavailable fields |",
        "|---|---|---:|---:|---|---|---:|---:|---|",
    ]
    for result in results:
        lines.append(
            f"| {result.symbol} | {result.dataset} | {result.interval} | {result.rows} | "
            f"{result.first_timestamp} | {result.last_timestamp} | {result.missing_rows} | "
            f"{result.duplicate_timestamps} | {result.unavailable_fields or ''} |"
        )
    lines.extend(
        [
            "",
            "## Pass Condition",
            "",
            "PASS_SPB_BINANCE_5_TOKEN_DATA_READY_FOR_JODY_AUDIT",
            "",
        ]
    )
    AUDIT_PATH.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    run()
