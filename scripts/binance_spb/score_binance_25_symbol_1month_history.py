from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SYMBOL_CONFIG = ROOT / "configs" / "cloud_data_pilot_v1_symbols.json"
INPUT_DIR = ROOT / "data" / "research" / "binance_25_symbol_1month"
OUTPUT_DIR = ROOT / "data" / "research" / "binance_25_symbol_1month_scored"
REPORT_DIR = ROOT / "reports" / "cloud_pattern_watch" / "v1"
SCORED_CSV = OUTPUT_DIR / "binance_25_symbol_1month_firestarter_scored.csv"
SCORED_JSONL = OUTPUT_DIR / "binance_25_symbol_1month_firestarter_scored.jsonl"
MANIFEST_CSV = REPORT_DIR / "binance_25_symbol_1month_scored_manifest.csv"
AUDIT_MD = REPORT_DIR / "binance_25_symbol_1month_scored_audit.md"

OUTPUT_COLUMNS = [
    "symbol",
    "timestamp_utc",
    "source_exchange",
    "scoring_mode",
    "price",
    "price_position",
    "er",
    "fmlc",
    "flowprint",
    "raw_score",
    "rvol_1h",
    "rvol_4h_window",
    "funding",
    "open_interest",
    "range_pos_20",
    "range_pos_50_4h",
    "near_breakout",
    "clean_reclaim",
    "above_4h_trend",
    "er_parent_status",
    "fmlc_parent_status",
    "flowprint_parent_status",
    "raw_score_parent_status",
    "data_quality_flags",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def iso_from_ms(value: int | float | str) -> str:
    return datetime.fromtimestamp(int(float(value)) / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def load_symbols() -> list[str]:
    payload = json.loads(SYMBOL_CONFIG.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("symbol config must be governed object")
    symbols = [str(symbol).strip().upper() for symbol in payload.get("symbols", []) if str(symbol).strip()]
    excluded = {str(symbol).strip().upper() for symbol in payload.get("excluded_symbols", []) if str(symbol).strip()}
    max_symbols = int(payload.get("max_symbols", 25))
    if len(symbols) > max_symbols:
        raise RuntimeError(f"symbol count {len(symbols)} exceeds max_symbols {max_symbols}")
    blocked = sorted(symbol for symbol in symbols if symbol in excluded)
    if blocked:
        raise RuntimeError(f"excluded symbols present: {', '.join(blocked)}")
    return symbols


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def load_klines(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    if df.empty:
        return df
    rename = {
        "open_time": "ts",
        "quote_asset_volume": "volume_quote",
    }
    df = df.rename(columns=rename)
    required = ["ts", "open", "high", "low", "close", "volume", "volume_quote"]
    for column in required:
        if column not in df.columns:
            return pd.DataFrame()
    for column in required:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=required).sort_values("ts").reset_index(drop=True)
    return df


def load_funding(path: Path) -> list[tuple[int, float]]:
    if not path.exists():
        return []
    df = pd.read_csv(path)
    if df.empty or "fundingTime" not in df.columns or "fundingRate" not in df.columns:
        return []
    df["fundingTime"] = pd.to_numeric(df["fundingTime"], errors="coerce")
    df["fundingRate"] = pd.to_numeric(df["fundingRate"], errors="coerce")
    df = df.dropna(subset=["fundingTime", "fundingRate"]).sort_values("fundingTime")
    return [(int(row.fundingTime), float(row.fundingRate)) for row in df.itertuples(index=False)]


def latest_funding_at(funding: list[tuple[int, float]], timestamp_ms: int) -> float | None:
    latest: float | None = None
    for funding_ts, funding_rate in funding:
        if funding_ts <= timestamp_ms:
            latest = funding_rate
        else:
            break
    return latest


def score_er(rvol_1h: float, rvol_4h_window: float, change_24h: float, near_breakout: bool, clean_reclaim: bool) -> float:
    value = 0.0
    if rvol_1h >= 1.25:
        value += 1
    if rvol_1h >= 1.75:
        value += 2
    if rvol_1h >= 2.5:
        value += 2
    if rvol_4h_window >= 1.25:
        value += 1
    if rvol_4h_window >= 1.75:
        value += 1
    if 2 <= change_24h < 4:
        value += 1
    elif 4 <= change_24h <= 12:
        value += 3
    elif 12 < change_24h <= 16:
        value += 2
    elif 16 < change_24h <= 25:
        value += 1
    if near_breakout:
        value += 2
    if clean_reclaim:
        value += 1
    return clamp(value, 0, 10)


def score_fmlc(volume_usd: float, range_pos_50_4h: float, range_pos_20: float, clean_reclaim: bool, above_4h_trend: bool, change_24h: float) -> float:
    value = 0.0
    if volume_usd >= 20_000_000:
        value += 3
    elif volume_usd >= 5_000_000:
        value += 2
    elif volume_usd >= 1_000_000:
        value += 1
    if range_pos_50_4h >= 0.55:
        value += 2
    if range_pos_20 >= 0.65:
        value += 2
    if clean_reclaim:
        value += 2
    if above_4h_trend:
        value += 1
    if change_24h <= 16:
        value += 1
    elif change_24h > 25:
        value -= 3
    return clamp(value, 0, 10)


def score_flowprint(rvol_1h: float, rvol_4h_window: float, current_funding: float, price: float, ema_21: float, near_breakout: bool) -> float:
    value = 0.0
    if rvol_1h >= 1.5:
        value += 2
    if rvol_1h >= 2.5:
        value += 1
    if rvol_4h_window >= 1.25:
        value += 1
    # Historical OI statistics were unavailable from the one-month puller, so no OI point is awarded here.
    if -0.0005 <= current_funding <= 0.0008:
        value += 2
    elif 0.0008 < current_funding <= 0.0015:
        value += 1
    elif current_funding > 0.002:
        value -= 2
    if price > ema_21:
        value += 1
    if near_breakout:
        value += 1
    return clamp(value, 0, 8)


def score_symbol(symbol: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    one_h_path = INPUT_DIR / f"{symbol}_futures_klines_1h.csv"
    four_h_path = INPUT_DIR / f"{symbol}_futures_klines_4h.csv"
    funding_path = INPUT_DIR / f"{symbol}_funding_rate_history.csv"

    one_h = load_klines(one_h_path)
    four_h = load_klines(four_h_path)
    funding = load_funding(funding_path)

    manifest = {
        "symbol": symbol,
        "input_1h_rows": int(len(one_h)),
        "input_4h_rows": int(len(four_h)),
        "input_funding_rows": int(len(funding)),
        "scored_rows": 0,
        "first_scored_utc": "",
        "last_scored_utc": "",
        "status": "HOLD",
        "notes": "",
    }

    if one_h.empty or four_h.empty:
        manifest["status"] = "SKIPPED_MISSING_KLINES"
        manifest["notes"] = "missing or empty 1h/4h kline input"
        return [], manifest
    if len(one_h) < 60 or len(four_h) < 50:
        manifest["status"] = "SKIPPED_INSUFFICIENT_HISTORY"
        manifest["notes"] = "requires at least 60x 1h rows and 50x 4h rows"
        return [], manifest
    if not funding:
        manifest["status"] = "SKIPPED_MISSING_FUNDING"
        manifest["notes"] = "funding history unavailable"
        return [], manifest

    one_h = one_h.copy()
    one_h["ema_9"] = one_h["close"].ewm(span=9).mean()
    one_h["ema_21"] = one_h["close"].ewm(span=21).mean()
    four_h = four_h.copy()
    four_h["ema_50"] = four_h["close"].ewm(span=50).mean()

    rows: list[dict[str, Any]] = []
    for idx in range(59, len(one_h)):
        current = one_h.iloc[idx]
        current_ts = int(current["ts"])
        price = float(current["close"])
        bar_high = float(current["high"])
        bar_low = float(current["low"])
        price_position = (price - bar_low) / (bar_high - bar_low) if (bar_high - bar_low) > 0 else 0.0

        window_20 = one_h.iloc[idx - 19: idx + 1]
        high_20 = float(window_20["high"].max())
        low_20 = float(window_20["low"].min())
        range_20 = high_20 - low_20
        range_pos_20 = (price - low_20) / range_20 if range_20 > 0 else 0.0

        vol_now = float(current["volume_quote"])
        vol_avg_20 = float(window_20["volume_quote"].mean())
        rvol_1h = vol_now / vol_avg_20 if vol_avg_20 > 0 else 0.0
        vol_last_4h = float(one_h.iloc[idx - 3: idx + 1]["volume_quote"].sum())
        vol_prev_4h = float(one_h.iloc[idx - 7: idx - 3]["volume_quote"].sum())
        rvol_4h_window = vol_last_4h / vol_prev_4h if vol_prev_4h > 0 else 0.0

        close_24h = float(one_h.iloc[idx - 24]["close"])
        change_24h = ((price - close_24h) / close_24h) * 100 if close_24h > 0 else 0.0
        volume_usd = float(one_h.iloc[idx - 23: idx + 1]["volume_quote"].sum())
        ema_9 = float(current["ema_9"])
        ema_21 = float(current["ema_21"])
        near_breakout = bool(price >= high_20 * 0.992)
        clean_reclaim = bool(price > ema_21 and ema_9 > ema_21)

        aligned_4h = four_h[four_h["ts"] <= current_ts]
        if len(aligned_4h) < 50:
            continue
        recent_4h = aligned_4h.iloc[-50:]
        high_50_4h = float(recent_4h["high"].max())
        low_50_4h = float(recent_4h["low"].min())
        range_50_4h = high_50_4h - low_50_4h
        range_pos_50_4h = (price - low_50_4h) / range_50_4h if range_50_4h > 0 else 0.0
        ema_50_4h = float(recent_4h["ema_50"].iloc[-1])
        above_4h_trend = bool(price > ema_50_4h)

        current_funding = latest_funding_at(funding, current_ts)
        if current_funding is None:
            continue

        er = score_er(rvol_1h, rvol_4h_window, change_24h, near_breakout, clean_reclaim)
        fmlc = score_fmlc(volume_usd, range_pos_50_4h, range_pos_20, clean_reclaim, above_4h_trend, change_24h)
        flowprint = score_flowprint(rvol_1h, rvol_4h_window, current_funding, price, ema_21, near_breakout)
        raw_score = (er * 0.35) + (fmlc * 0.35) + (flowprint * 0.30)

        rows.append({
            "symbol": symbol,
            "timestamp_utc": iso_from_ms(current_ts),
            "source_exchange": "binance_usdm",
            "scoring_mode": "historical_research_no_oi_history",
            "price": round(price, 8),
            "price_position": round(price_position, 4),
            "er": round(er, 1),
            "fmlc": round(fmlc, 1),
            "flowprint": round(flowprint, 1),
            "raw_score": round(raw_score, 4),
            "rvol_1h": round(rvol_1h, 4),
            "rvol_4h_window": round(rvol_4h_window, 4),
            "funding": round(float(current_funding), 6),
            "open_interest": "",
            "range_pos_20": round(range_pos_20, 4),
            "range_pos_50_4h": round(range_pos_50_4h, 4),
            "near_breakout": near_breakout,
            "clean_reclaim": clean_reclaim,
            "above_4h_trend": above_4h_trend,
            "er_parent_status": "PASS",
            "fmlc_parent_status": "PASS",
            "flowprint_parent_status": "PASS_PROXY_NO_HISTORICAL_OI",
            "raw_score_parent_status": "PASS_PROXY_NO_HISTORICAL_OI",
            "data_quality_flags": "OI_HISTORY_UNAVAILABLE",
        })

    manifest["scored_rows"] = len(rows)
    if rows:
        manifest["first_scored_utc"] = rows[0]["timestamp_utc"]
        manifest["last_scored_utc"] = rows[-1]["timestamp_utc"]
        manifest["status"] = "PASS"
        manifest["notes"] = "scored with historical OI unavailable; Flowprint omits OI component"
    else:
        manifest["status"] = "HOLD_NO_SCORED_ROWS"
        manifest["notes"] = "no rows survived scoring requirements"
    return rows, manifest


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def run() -> None:
    symbols = load_symbols()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    for symbol in symbols:
        rows, manifest = score_symbol(symbol)
        all_rows.extend(rows)
        manifest_rows.append(manifest)

    all_rows.sort(key=lambda row: (row["symbol"], row["timestamp_utc"]))
    write_csv(SCORED_CSV, OUTPUT_COLUMNS, all_rows)
    write_jsonl(SCORED_JSONL, all_rows)
    write_csv(MANIFEST_CSV, list(manifest_rows[0].keys()) if manifest_rows else [], manifest_rows)

    status_counts = Counter(row["status"] for row in manifest_rows)
    symbol_count = len(symbols)
    pass_symbols = status_counts.get("PASS", 0)
    first_ts = min((row["timestamp_utc"] for row in all_rows), default="")
    last_ts = max((row["timestamp_utc"] for row in all_rows), default="")
    pass_marker = "PASS_BINANCE_25_SYMBOL_1MONTH_HISTORY_SCORED_READY_FOR_REVIEW" if all_rows and pass_symbols >= 20 else "HOLD_BINANCE_25_SYMBOL_1MONTH_HISTORY_SCORED_REVIEW"

    lines = [
        "# Binance 25 Symbol 1 Month Historical Firestarter Scoring Audit",
        "",
        f"Run timestamp UTC: `{utc_now()}`",
        f"Symbols attempted: `{symbol_count}`",
        f"Symbols scored/pass: `{pass_symbols}`",
        f"Total scored rows: `{len(all_rows)}`",
        f"First scored UTC: `{first_ts}`",
        f"Last scored UTC: `{last_ts}`",
        "",
        "## Outputs",
        "",
        f"- Scored CSV: `{SCORED_CSV.relative_to(ROOT)}`",
        f"- Scored JSONL: `{SCORED_JSONL.relative_to(ROOT)}`",
        f"- Manifest: `{MANIFEST_CSV.relative_to(ROOT)}`",
        "",
        "## Boundary",
        "",
        "Research/backfill only. This script does not write `state/cloud_pattern_watch/current_metrics.json`, `current_snapshot.json`, Pattern Watch send state, n8n state, or trading state.",
        "",
        "## Scoring Caveat",
        "",
        "Historical open-interest statistics were unavailable from the one-month pull. Historical Flowprint therefore omits the OI component and marks rows with `OI_HISTORY_UNAVAILABLE`.",
        "",
        "## Symbol Manifest",
        "",
        "| Symbol | 1H rows | 4H rows | Funding rows | Scored rows | First scored | Last scored | Status | Notes |",
        "|---|---:|---:|---:|---:|---|---|---|---|",
    ]
    for row in manifest_rows:
        lines.append(
            f"| {row['symbol']} | {row['input_1h_rows']} | {row['input_4h_rows']} | {row['input_funding_rows']} | "
            f"{row['scored_rows']} | {row['first_scored_utc']} | {row['last_scored_utc']} | {row['status']} | {row['notes']} |"
        )
    lines.extend(["", "## Pass Condition", "", pass_marker, ""])
    AUDIT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(pass_marker)
    print(f"Scored rows: {len(all_rows)}")
    print(f"Scored symbols: {pass_symbols}/{symbol_count}")


if __name__ == "__main__":
    run()
