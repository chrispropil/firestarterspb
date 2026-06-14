#!/usr/bin/env python3
"""Cloud Cell 1 Metric Producer using Binance public USD-M REST data.

Manual-gated producer. Writes the same Cell 1 current_metrics files consumed by the
existing snapshot adapter. No credentials and no order/execution code.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
APPROVED_OUTPUT_DIR = REPO_ROOT / "state" / "cloud_pattern_watch"
APPROVED_REPORT_DIR = REPO_ROOT / "reports" / "cloud_pattern_watch" / "v1"
MANUAL_BUILD_CONFIRMATION = "CELL1_MANUAL_BUILD_APPROVED"
BINANCE_BASE_URL = "https://fapi.binance.com"

COLUMNS = [
    "symbol", "timestamp_utc", "price", "price_position", "er", "fmlc", "flowprint", "raw_score",
    "rvol_1h", "rvol_4h_window", "funding", "open_interest", "range_pos_20",
    "range_pos_50_4h", "near_breakout", "clean_reclaim", "above_4h_trend",
    "er_parent_status", "fmlc_parent_status", "flowprint_parent_status", "raw_score_parent_status",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_repo_path(path_value: str) -> Path:
    path = Path(path_value)
    return path.resolve() if path.is_absolute() else (REPO_ROOT / path).resolve()


def repo_relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT)).replace("\\", "/")


def ensure_approved_output_paths(config: dict[str, Any]) -> tuple[Path, Path]:
    output_dir = resolve_repo_path(config.get("output_dir", "state/cloud_pattern_watch"))
    report_dir = resolve_repo_path(config.get("report_dir", "reports/cloud_pattern_watch/v1"))
    if output_dir != APPROVED_OUTPUT_DIR.resolve():
        raise ValueError("output_dir must be state/cloud_pattern_watch")
    if report_dir != APPROVED_REPORT_DIR.resolve():
        raise ValueError("report_dir must be reports/cloud_pattern_watch/v1")
    return output_dir, report_dir


def atomic_replace_text(path: Path, text: str) -> None:
    tmp_path = path.with_name(path.name + ".tmp")
    tmp_path.write_text(text, encoding="utf-8")
    os.replace(tmp_path, path)


def safety_flags() -> dict[str, bool]:
    return {
        "raw_candle_history_written": False,
        "exchange_credentials": False,
        "private_endpoints": False,
        "optimizer_changes": False,
        "scoring_changes": False,
        "trading_execution": False,
        "cell_2": False,
        "scheduler_activation": False,
        "n8n_activation": False,
        "pattern_watch_ntfy_send": False,
    }


def write_manual_build_status(
    mode: str,
    gate_result: str,
    symbols: list[str],
    symbol_governance: dict[str, Any],
    output_paths: dict[str, str],
    message: str,
) -> dict[str, Any]:
    APPROVED_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    APPROVED_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp_utc": utc_now(),
        "mode": mode,
        "gate_result": gate_result,
        "message": message,
        "source_exchange": "binance_usdm",
        "symbol_count": len(symbols),
        "max_symbols": symbol_governance.get("max_symbols"),
        "excluded_symbols": symbol_governance.get("excluded_symbols", []),
        "output_paths": output_paths,
        "safety_flags": safety_flags(),
    }
    status_path = APPROVED_OUTPUT_DIR / "cell1_manual_build_gate_status.json"
    manifest_path = APPROVED_REPORT_DIR / "cell1_manual_build_gate_manifest.json"
    status_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Manual build status path: {repo_relative(status_path)}")
    print(f"Manual build manifest path: {repo_relative(manifest_path)}")
    return payload


def load_governed_symbol_config(symbols_file: str) -> tuple[list[str], dict[str, Any]]:
    path = resolve_repo_path(symbols_file)
    if not path.exists():
        raise ValueError(f"Symbols file not found at {repo_relative(path)}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        raise ValueError("Symbols JSON must be the governed object, not a bare list")
    if not isinstance(payload, dict):
        raise ValueError("Symbols JSON must be an object")
    for key in ["symbols", "max_symbols", "excluded_symbols", "status"]:
        if key not in payload:
            raise ValueError(f"Symbols JSON missing required governed key: {key}")

    symbols = payload["symbols"]
    max_symbols = payload["max_symbols"]
    excluded = payload["excluded_symbols"]
    status = payload["status"]
    if not isinstance(symbols, list):
        raise ValueError("symbols must be a list")
    if not isinstance(max_symbols, int):
        raise ValueError("max_symbols must be an integer")
    if not isinstance(excluded, list):
        raise ValueError("excluded_symbols must be a list")
    if not isinstance(status, str):
        raise ValueError("status must be a string")

    normalized_symbols = [str(symbol).strip().upper() for symbol in symbols if str(symbol).strip()]
    normalized_excluded = {str(symbol).strip().upper() for symbol in excluded if str(symbol).strip()}
    if len(normalized_symbols) != len(symbols):
        raise ValueError("Symbols JSON contains blank or invalid symbol entries")
    if len(normalized_symbols) > max_symbols:
        raise ValueError(f"Symbol count ({len(normalized_symbols)}) exceeds governed max_symbols ({max_symbols})")
    if max_symbols != 25:
        raise ValueError(f"Governed max_symbols must equal 25, got {max_symbols}")
    blocked = sorted(symbol for symbol in normalized_symbols if symbol in normalized_excluded)
    if blocked:
        raise ValueError(f"Excluded symbols present in governed symbol list: {', '.join(blocked)}")

    return normalized_symbols, {
        "status": status,
        "max_symbols": max_symbols,
        "excluded_symbols": sorted(normalized_excluded),
    }


def safe_float(value: Any) -> float:
    try:
        if value is None:
            return 0.0
        return float(value)
    except Exception:
        return 0.0


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def fetch_json(base_url: str, path: str, params: dict[str, Any], timeout: int = 10, retries: int = 3) -> Any:
    query = urllib.parse.urlencode({key: value for key, value in params.items() if value is not None})
    url = f"{base_url}{path}?{query}" if query else f"{base_url}{path}"
    request = urllib.request.Request(url, headers={"User-Agent": "firestarter-cell1-binance/1.0"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                if response.status == 200:
                    return json.loads(response.read().decode("utf-8"))
                raise urllib.error.URLError(f"HTTP Status {response.status}")
        except Exception as exc:
            if attempt == retries - 1:
                raise exc
            time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(f"request failed after retries: {url}")


def calculate_atr(df_1h: pd.DataFrame, period: int = 14) -> float:
    if len(df_1h) < period + 1:
        return 0.0
    high = df_1h["high"].astype(float)
    low = df_1h["low"].astype(float)
    close = df_1h["close"].astype(float)
    prev_close = close.shift(1)
    tr = pd.concat([(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1).max(axis=1)
    return float(tr.rolling(period).mean().iloc[-1])


def klines_to_df(raw: list[list[Any]]) -> pd.DataFrame:
    rows = []
    for item in raw:
        rows.append({
            "ts": int(item[0]),
            "open": float(item[1]),
            "high": float(item[2]),
            "low": float(item[3]),
            "close": float(item[4]),
            "volume": float(item[5]),
            "volume_quote": float(item[7]),
        })
    return pd.DataFrame(rows).sort_values("ts").reset_index(drop=True)


def blocked_row(symbol: str, status: str) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "timestamp_utc": utc_now(),
        "price": "",
        "price_position": "",
        "er": "BLOCKED_PARENT_FIELD_FAILED",
        "fmlc": "BLOCKED_PARENT_FIELD_FAILED",
        "flowprint": "BLOCKED_PARENT_FIELD_FAILED",
        "raw_score": "BLOCKED_PARENT_FIELD_FAILED",
        "rvol_1h": "",
        "rvol_4h_window": "",
        "funding": "",
        "open_interest": "",
        "range_pos_20": "",
        "range_pos_50_4h": "",
        "near_breakout": "",
        "clean_reclaim": "",
        "above_4h_trend": "",
        "er_parent_status": status,
        "fmlc_parent_status": "BLOCKED_PARENT_FIELD_FAILED",
        "flowprint_parent_status": "BLOCKED_PARENT_FIELD_FAILED",
        "raw_score_parent_status": "BLOCKED_PARENT_FIELD_FAILED",
    }


def process_symbol(symbol: str, base_url: str) -> dict[str, Any]:
    er_parent_status = "PASS"
    fmlc_parent_status = "PASS"
    flowprint_parent_status = "PASS"
    raw_score_parent_status = "PASS"
    funding_data: list[tuple[int, float]] = []
    oi_val = 0.0

    try:
        data_1h = fetch_json(base_url, "/fapi/v1/klines", {"symbol": symbol, "interval": "1h", "limit": 100})
        if not isinstance(data_1h, list) or len(data_1h) < 50:
            er_parent_status = "FAIL_INSUFFICIENT_1H_HISTORY"
    except Exception as exc:
        er_parent_status = f"FAIL_API_1H_ERROR: {exc}"
        data_1h = []

    try:
        data_4h = fetch_json(base_url, "/fapi/v1/klines", {"symbol": symbol, "interval": "4h", "limit": 100})
        if not isinstance(data_4h, list) or len(data_4h) < 50:
            fmlc_parent_status = "FAIL_INSUFFICIENT_4H_HISTORY"
    except Exception as exc:
        fmlc_parent_status = f"FAIL_API_4H_ERROR: {exc}"
        data_4h = []

    try:
        raw_funding = fetch_json(base_url, "/fapi/v1/fundingRate", {"symbol": symbol, "limit": 100})
        for item in raw_funding if isinstance(raw_funding, list) else []:
            funding_data.append((int(item.get("fundingTime", 0)), safe_float(item.get("fundingRate"))))
        funding_data.sort(key=lambda row: row[0])
    except Exception as exc:
        flowprint_parent_status = f"FAIL_API_FUNDING_ERROR: {exc}"

    try:
        raw_oi = fetch_json(base_url, "/fapi/v1/openInterest", {"symbol": symbol})
        oi_val = safe_float(raw_oi.get("openInterest")) if isinstance(raw_oi, dict) else 0.0
        if oi_val <= 0:
            flowprint_parent_status = "FAIL_OI_MISSING"
    except Exception as exc:
        flowprint_parent_status = f"FAIL_API_OI_ERROR: {exc}"

    if "FAIL" in er_parent_status:
        return blocked_row(symbol, er_parent_status)
    er_parent_status = "PASS"
    if "FAIL" in fmlc_parent_status:
        raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
    else:
        fmlc_parent_status = "PASS"
    if "FAIL" in flowprint_parent_status:
        raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
    else:
        flowprint_parent_status = "PASS"

    try:
        df_1h = klines_to_df(data_1h)
        df_1h = df_1h.iloc[:-1].reset_index(drop=True)
        latest = df_1h.iloc[-1]
        current_ts = int(latest["ts"])
        price = float(latest["close"])
        timestamp_utc = datetime.fromtimestamp(current_ts / 1000.0, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        bar_high = float(latest["high"])
        bar_low = float(latest["low"])
        price_position = (price - bar_low) / (bar_high - bar_low) if (bar_high - bar_low) > 0 else 0.0
        vol_now = float(latest["volume_quote"])
        vol_avg_20 = float(df_1h["volume_quote"].iloc[-20:].mean())
        rvol_1h = vol_now / vol_avg_20 if vol_avg_20 > 0 else 0.0
        vol_last_4h = float(df_1h["volume_quote"].iloc[-4:].sum())
        vol_prev_4h = float(df_1h["volume_quote"].iloc[-8:-4].sum())
        rvol_4h_window = vol_last_4h / vol_prev_4h if vol_prev_4h > 0 else 0.0
        ema_9 = float(df_1h["close"].ewm(span=9).mean().iloc[-1])
        ema_21 = float(df_1h["close"].ewm(span=21).mean().iloc[-1])
        _atr_1h = calculate_atr(df_1h, 14)
        high_20 = float(df_1h["high"].iloc[-20:].max())
        low_20 = float(df_1h["low"].iloc[-20:].min())
        range_20 = high_20 - low_20
        range_pos_20 = (price - low_20) / range_20 if range_20 > 0 else 0.0
        near_breakout = price >= high_20 * 0.992
        clean_reclaim = bool(price > ema_21 and ema_9 > ema_21)
        if len(df_1h) >= 24:
            close_24h = float(df_1h["close"].iloc[-24])
            change_24h = ((price - close_24h) / close_24h) * 100 if close_24h > 0 else 0.0
            volume_usd = float(df_1h["volume_quote"].iloc[-24:].sum())
        else:
            change_24h = 0.0
            volume_usd = float(df_1h["volume_quote"].sum())
        er_val = 0.0
        if rvol_1h >= 1.25: er_val += 1
        if rvol_1h >= 1.75: er_val += 2
        if rvol_1h >= 2.5: er_val += 2
        if rvol_4h_window >= 1.25: er_val += 1
        if rvol_4h_window >= 1.75: er_val += 1
        if 2 <= change_24h < 4: er_val += 1
        elif 4 <= change_24h <= 12: er_val += 3
        elif 12 < change_24h <= 16: er_val += 2
        elif 16 < change_24h <= 25: er_val += 1
        if near_breakout: er_val += 2
        if clean_reclaim: er_val += 1
        er = clamp(er_val, 0, 10)
    except Exception as exc:
        return blocked_row(symbol, f"FAIL_COMPUTE_ER_ERROR: {exc}")

    if fmlc_parent_status == "PASS":
        try:
            df_4h = klines_to_df(data_4h)
            df_4h = df_4h.iloc[:-1].reset_index(drop=True)
            sub_4h = df_4h[df_4h["ts"] <= current_ts]
            if len(sub_4h) < 50:
                fmlc_parent_status = "FAIL_INSUFFICIENT_ALIGNED_4H_HISTORY"
                raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
                range_pos_50_4h = 0.0
                above_4h_trend = False
                fmlc = "BLOCKED_PARENT_FIELD_FAILED"
            else:
                high_50_4h = float(sub_4h["high"].iloc[-50:].max())
                low_50_4h = float(sub_4h["low"].iloc[-50:].min())
                range_50_4h = high_50_4h - low_50_4h
                range_pos_50_4h = (price - low_50_4h) / range_50_4h if range_50_4h > 0 else 0.0
                ema_50_4h = float(sub_4h["close"].ewm(span=50).mean().iloc[-1])
                above_4h_trend = bool(price > ema_50_4h)
                fmlc_val = 0.0
                if volume_usd >= 20_000_000: fmlc_val += 3
                elif volume_usd >= 5_000_000: fmlc_val += 2
                elif volume_usd >= 1_000_000: fmlc_val += 1
                if range_pos_50_4h >= 0.55: fmlc_val += 2
                if range_pos_20 >= 0.65: fmlc_val += 2
                if clean_reclaim: fmlc_val += 2
                if above_4h_trend: fmlc_val += 1
                if change_24h <= 16: fmlc_val += 1
                elif change_24h > 25: fmlc_val -= 3
                fmlc = clamp(fmlc_val, 0, 10)
        except Exception as exc:
            fmlc_parent_status = f"FAIL_COMPUTE_FMLC_ERROR: {exc}"
            raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
            range_pos_50_4h = 0.0
            above_4h_trend = False
            fmlc = "BLOCKED_PARENT_FIELD_FAILED"
    else:
        range_pos_50_4h = 0.0
        above_4h_trend = False
        fmlc = "BLOCKED_PARENT_FIELD_FAILED"

    if flowprint_parent_status == "PASS":
        try:
            valid_funding = [row for row in funding_data if row[0] <= current_ts]
            current_funding = valid_funding[-1][1] if valid_funding else (funding_data[-1][1] if funding_data else 0.0)
            if not funding_data:
                flowprint_parent_status = "FAIL_FUNDING_EMPTY"
                raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
                flowprint = "BLOCKED_PARENT_FIELD_FAILED"
            else:
                flow = 0.0
                if rvol_1h >= 1.5: flow += 2
                if rvol_1h >= 2.5: flow += 1
                if rvol_4h_window >= 1.25: flow += 1
                if oi_val > 0: flow += 1
                if -0.0005 <= current_funding <= 0.0008: flow += 2
                elif 0.0008 < current_funding <= 0.0015: flow += 1
                elif current_funding > 0.002: flow -= 2
                if price > ema_21: flow += 1
                if near_breakout: flow += 1
                flowprint = clamp(flow, 0, 8)
        except Exception as exc:
            flowprint_parent_status = f"FAIL_COMPUTE_FLOWPRINT_ERROR: {exc}"
            raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
            current_funding = 0.0
            flowprint = "BLOCKED_PARENT_FIELD_FAILED"
    else:
        current_funding = 0.0
        flowprint = "BLOCKED_PARENT_FIELD_FAILED"

    if er_parent_status == "PASS" and fmlc_parent_status == "PASS" and flowprint_parent_status == "PASS":
        raw_score_parent_status = "PASS"
    else:
        raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"

    if raw_score_parent_status == "PASS":
        raw_score = (er * 0.35) + (fmlc * 0.35) + (flowprint * 0.30)
    else:
        raw_score = "BLOCKED_PARENT_FIELD_FAILED"

    return {
        "symbol": symbol,
        "timestamp_utc": timestamp_utc,
        "price": round(price, 8),
        "price_position": round(price_position, 4),
        "er": round(er, 1),
        "fmlc": round(fmlc, 1) if isinstance(fmlc, (int, float)) else fmlc,
        "flowprint": round(flowprint, 1) if isinstance(flowprint, (int, float)) else flowprint,
        "raw_score": round(raw_score, 4) if isinstance(raw_score, (int, float)) else raw_score,
        "rvol_1h": round(rvol_1h, 4),
        "rvol_4h_window": round(rvol_4h_window, 4),
        "funding": round(current_funding, 6),
        "open_interest": round(oi_val, 2),
        "range_pos_20": round(range_pos_20, 4),
        "range_pos_50_4h": round(range_pos_50_4h, 4),
        "near_breakout": near_breakout,
        "clean_reclaim": clean_reclaim,
        "above_4h_trend": above_4h_trend,
        "er_parent_status": er_parent_status,
        "fmlc_parent_status": fmlc_parent_status,
        "flowprint_parent_status": flowprint_parent_status,
        "raw_score_parent_status": raw_score_parent_status,
    }


def run_dry_run(symbols: list[str], config: dict[str, Any], symbol_governance: dict[str, Any]) -> int:
    print("--------------------------------------------------")
    print("BINANCE CELL 1 DRY-RUN MODE")
    print("--------------------------------------------------")
    print(f"Loaded symbols file: {config.get('symbols_file')}")
    print(f"Symbol config status: {symbol_governance.get('status')}")
    print(f"Governed max_symbols: {symbol_governance.get('max_symbols')}")
    print(f"Base API URL: {config.get('base_url')}")
    print(f"Output directory: {config.get('output_dir')}")
    print(f"Report directory: {config.get('report_dir')}")
    print(f"Symbols universe total: {len(symbols)}")
    print("Dry-run validation complete. Exiting cleanly.")
    return 0


def write_outputs(output_rows: list[dict[str, Any]], output_dir: Path, report_dir: Path, success_count: int, fail_count: int, errors: dict[str, str]) -> int:
    json_path = output_dir / "current_metrics.json"
    csv_path = output_dir / "current_metrics.csv"
    snapshot_output_files: list[str] = []
    if success_count > 0:
        atomic_replace_text(json_path, json.dumps(output_rows, indent=2) + "\n")
        csv_tmp = csv_path.with_name(csv_path.name + ".tmp")
        with csv_tmp.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(output_rows)
        os.replace(csv_tmp, csv_path)
        print(f"Saved: {repo_relative(json_path)}")
        print(f"Saved: {repo_relative(csv_path)}")
        snapshot_output_files = [repo_relative(json_path), repo_relative(csv_path)]
    else:
        print("Skipped snapshot write: success_count is 0; existing current_metrics.json/csv preserved.")

    status_path = output_dir / "cell1_metric_producer_status.json"
    status = {
        "timestamp_utc": utc_now(),
        "source_exchange": "binance_usdm",
        "status": "SUCCESS" if fail_count == 0 else "PARTIAL_FAILURE" if success_count > 0 else "FAILURE",
        "symbols_attempted": len(output_rows),
        "symbols_successful": success_count,
        "symbols_failed": fail_count,
        "errors": errors,
        "output_files": snapshot_output_files,
        "snapshot_write_skipped": success_count == 0,
        "snapshot_skip_reason": "success_count is 0; existing current_metrics.json/csv preserved" if success_count == 0 else "",
    }
    status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(f"Saved: {repo_relative(status_path)}")

    report_path = report_dir / "cell1_metric_producer_report.md"
    lines = [
        "# Binance Cell 1 Metric Producer v1 Execution Report",
        "",
        f"- Execution Time UTC: `{status['timestamp_utc']}`",
        "- Source: `binance_usdm`",
        f"- Status: `{status['status']}`",
        f"- Symbols Processed: `{success_count} / {len(output_rows)}` successfully",
        "",
        "## Metrics Table",
        "",
        "| Symbol | Price | ER | FMLC | Flowprint | Raw Score | RVOL 1H | Funding | OI | ER Parent | FMLC Parent | Flowprint Parent |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for row in output_rows:
        price = f"{row['price']:.4f}" if isinstance(row.get("price"), (int, float)) else ""
        er = f"{row['er']:.1f}" if isinstance(row.get("er"), (int, float)) else str(row.get("er", ""))
        fmlc = f"{row['fmlc']:.1f}" if isinstance(row.get("fmlc"), (int, float)) else str(row.get("fmlc", ""))
        flow = f"{row['flowprint']:.1f}" if isinstance(row.get("flowprint"), (int, float)) else str(row.get("flowprint", ""))
        score = f"{row['raw_score']:.4f}" if isinstance(row.get("raw_score"), (int, float)) else str(row.get("raw_score", ""))
        rvol = f"{row['rvol_1h']:.2f}" if isinstance(row.get("rvol_1h"), (int, float)) else ""
        funding = f"{row['funding']:.6f}" if isinstance(row.get("funding"), (int, float)) else ""
        oi = f"{row['open_interest']:.2f}" if isinstance(row.get("open_interest"), (int, float)) else ""
        lines.append(
            f"| {row['symbol']} | {price} | {er} | {fmlc} | {flow} | {score} | {rvol} | {funding} | {oi} | "
            f"`{row['er_parent_status']}` | `{row['fmlc_parent_status']}` | `{row['flowprint_parent_status']}` |"
        )
    if errors:
        lines.extend(["", "## Execution Errors", "", "| Symbol | Error |", "|---|---|"])
        for symbol, error in sorted(errors.items()):
            lines.append(f"| {symbol} | {error} |")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved: {repo_relative(report_path)}")
    return 0 if fail_count == 0 else 1


def run_build(symbols: list[str], config: dict[str, Any]) -> int:
    print("--------------------------------------------------")
    print("RUNNING BINANCE CELL 1 MANUAL BUILD")
    print("--------------------------------------------------")
    output_dir, report_dir = ensure_approved_output_paths(config)
    base_url = config.get("base_url", BINANCE_BASE_URL)
    if base_url != BINANCE_BASE_URL:
        raise ValueError("base_url must remain the approved public Binance USD-M endpoint")
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    output_rows: list[dict[str, Any]] = []
    errors: dict[str, str] = {}
    success_count = 0
    fail_count = 0
    for index, symbol in enumerate(symbols):
        print(f"[{index + 1}/{len(symbols)}] Processing {symbol}...")
        try:
            row = process_symbol(symbol, base_url)
            if "FAIL" in str(row.get("er_parent_status")):
                fail_count += 1
                errors[symbol] = str(row.get("er_parent_status"))
            else:
                success_count += 1
            output_rows.append(row)
        except Exception as exc:
            fail_count += 1
            errors[symbol] = str(exc)
            output_rows.append(blocked_row(symbol, f"FAIL_EXCEPTION: {exc}"))
        time.sleep(0.2)
    return write_outputs(output_rows, output_dir, report_dir, success_count, fail_count, errors)


def main() -> None:
    parser = argparse.ArgumentParser(description="Binance Cloud Cell 1 Metric Producer v1")
    parser.add_argument("--config", default="configs/cloud_cell1_metric_producer_binance_v1.json")
    parser.add_argument("--build", action="store_true", help="Rejected legacy path; use --manual-build")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--manual-build", action="store_true")
    parser.add_argument("--confirm-manual-build", default="")
    args = parser.parse_args()

    if args.build:
        print("ERROR: Legacy --build path is rejected; use the manual build gate only", file=sys.stderr)
        sys.exit(2)
    if not Path(args.config).exists():
        print(f"ERROR: Configuration file not found at {args.config}", file=sys.stderr)
        sys.exit(2)
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    for key in ["symbols_file", "base_url", "output_dir", "report_dir", "dry_run"]:
        if key not in config:
            print(f"ERROR: Missing required config key '{key}'", file=sys.stderr)
            sys.exit(2)
    symbols, symbol_governance = load_governed_symbol_config(config["symbols_file"])
    output_dir, report_dir = ensure_approved_output_paths(config)
    output_paths = {
        "output_dir": repo_relative(output_dir),
        "report_dir": repo_relative(report_dir),
        "metrics_json": repo_relative(output_dir / "current_metrics.json"),
        "metrics_csv": repo_relative(output_dir / "current_metrics.csv"),
        "producer_status": repo_relative(output_dir / "cell1_metric_producer_status.json"),
        "producer_report": repo_relative(report_dir / "cell1_metric_producer_report.md"),
        "manual_gate_status": repo_relative(output_dir / "cell1_manual_build_gate_status.json"),
        "manual_gate_manifest": repo_relative(report_dir / "cell1_manual_build_gate_manifest.json"),
    }

    if args.manual_build:
        if args.confirm_manual_build != MANUAL_BUILD_CONFIRMATION:
            write_manual_build_status("manual_build", "DENIED_CONFIRMATION_REQUIRED", symbols, symbol_governance, output_paths, "Manual build denied: missing exact confirmation token.")
            print("ERROR: Manual build requires --confirm-manual-build CELL1_MANUAL_BUILD_APPROVED", file=sys.stderr)
            sys.exit(2)
        write_manual_build_status("manual_build", "APPROVED_CONFIRMED", symbols, symbol_governance, output_paths, "Manual build approved by exact confirmation token.")
        try:
            result = run_build(symbols, config)
            write_manual_build_status("manual_build", "COMPLETED" if result == 0 else "COMPLETED_WITH_FAILURES", symbols, symbol_governance, output_paths, f"Manual build finished with exit code {result}.")
            sys.exit(result)
        except Exception as exc:
            write_manual_build_status("manual_build", "FAILED_EXCEPTION", symbols, symbol_governance, output_paths, f"Manual build failed: {exc}")
            print(f"ERROR: Manual build failed: {exc}", file=sys.stderr)
            sys.exit(1)

    if config["dry_run"] is not True and not args.dry_run:
        print("ERROR: Default behavior must remain dry-run; config dry_run must be true", file=sys.stderr)
        sys.exit(2)
    if args.confirm_manual_build:
        print("ERROR: --confirm-manual-build is only valid with --manual-build", file=sys.stderr)
        sys.exit(2)
    sys.exit(run_dry_run(symbols, config, symbol_governance))


if __name__ == "__main__":
    main()
