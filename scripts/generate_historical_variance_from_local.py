from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
CSV_OUTPUT = REPORTS_DIR / "firestarterog_real_historical_variance_sample.csv"
AUDIT_OUTPUT = REPORTS_DIR / "firestarterog_real_historical_variance_sample_audit.md"

DATA_ROOT_CANDIDATES = [
    ROOT / "data",
    Path(r"C:\firestarterspb\data"),
]

SYMBOLS = [
    "1000SHIBUSDT",
    "AAVEUSDT",
    "ADAUSDT",
    "APTUSDT",
    "ARBUSDT",
    "ATOMUSDT",
    "AVAXUSDT",
    "BCHUSDT",
    "BNBUSDT",
    "BTCUSDT",
    "DOGEUSDT",
    "DOTUSDT",
    "ETHUSDT",
    "INJUSDT",
    "LINKUSDT",
    "LTCUSDT",
    "NEARUSDT",
    "OPUSDT",
    "RENDERUSDT",
    "SOLUSDT",
    "SUIUSDT",
    "TIAUSDT",
    "TRXUSDT",
    "UNIUSDT",
    "XRPUSDT",
    "FILUSDT",
    "ICPUSDT",
    "SEIUSDT",
    "FETUSDT",
    "ALGOUSDT",
    "XLMUSDT",
    "HBARUSDT",
    "ETCUSDT",
    "STXUSDT",
    "VETUSDT",
    "RUNEUSDT",
    "SANDUSDT",
    "MANAUSDT",
    "AXSUSDT",
    "WLDUSDT",
    "JUPUSDT",
    "PYTHUSDT",
    "DYDXUSDT",
    "LDOUSDT",
    "ENAUSDT",
    "ORDIUSDT",
    "WIFUSDT",
    "1000BONKUSDT",
    "1000PEPEUSDT",
    "EGLDUSDT"
]

TOP100_5M_SYMBOLS = {"TRXUSDT", "ETCUSDT", "ALGOUSDT", "RUNEUSDT", "TIAUSDT", "FILUSDT", "1000BONKUSDT", "XLMUSDT", "APTUSDT", "SEIUSDT", "LTCUSDT", "OPUSDT", "SUIUSDT", "ETHUSDT", "BNBUSDT", "BCHUSDT", "ARBUSDT", "AAVEUSDT", "DOTUSDT", "WLDUSDT", "INJUSDT", "RENDERUSDT", "ICPUSDT", "1000PEPEUSDT", "ADAUSDT", "ENAUSDT", "ORDIUSDT", "WIFUSDT", "UNIUSDT", "1000SHIBUSDT", "HBARUSDT", "FETUSDT", "ATOMUSDT", "NEARUSDT", "BTCUSDT"}
TOP100_DERIV_SYMBOLS = {"TRXUSDT", "ETCUSDT", "ALGOUSDT", "RUNEUSDT", "TIAUSDT", "FILUSDT", "1000BONKUSDT", "XLMUSDT", "APTUSDT", "SEIUSDT", "LTCUSDT", "OPUSDT", "SUIUSDT", "ETHUSDT", "BNBUSDT", "BCHUSDT", "ARBUSDT", "AAVEUSDT", "DOTUSDT", "WLDUSDT", "INJUSDT", "RENDERUSDT", "ICPUSDT", "1000PEPEUSDT", "ADAUSDT", "ENAUSDT", "ORDIUSDT", "WIFUSDT", "UNIUSDT", "1000SHIBUSDT", "HBARUSDT", "FETUSDT", "ATOMUSDT", "NEARUSDT", "BTCUSDT"}

CANDLE_SUBDIR_BY_SYMBOL = {
    symbol: (
        "binance_top100_excluding_existing_5_1month"
        if symbol in TOP100_5M_SYMBOLS
        else "binance_core88_missing_1month"
    )
    for symbol in SYMBOLS
}
DERIV_SUBDIR_BY_SYMBOL = {
    symbol: (
        "binance_top100_derivatives_context_1month"
        if symbol in TOP100_DERIV_SYMBOLS
        else "binance_core88_missing_derivatives_context_1month"
    )
    for symbol in SYMBOLS
}


def pick_first_existing(candidates: list[Path]) -> Path:
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError("No local source file found in any expected location.")


def resolve_source_file(symbol: str, kind: str) -> Path:
    candidates: list[Path] = []
    for data_root in DATA_ROOT_CANDIDATES:
        if not data_root.exists():
            continue
        if kind == "candle":
            candidates.append(data_root / "research" / CANDLE_SUBDIR_BY_SYMBOL[symbol] / f"{symbol}_1month_5m.csv")
        elif kind == "funding":
            candidates.append(data_root / "research" / DERIV_SUBDIR_BY_SYMBOL[symbol] / "fundingRate" / f"{symbol}_fundingRate.csv")
        elif kind == "oi":
            candidates.append(data_root / "research" / DERIV_SUBDIR_BY_SYMBOL[symbol] / "openInterestHist" / f"{symbol}_openInterestHist.csv")
        else:
            raise ValueError(f"Unknown source kind: {kind}")
    return pick_first_existing(candidates)


def read_5m_candles(symbol: str) -> tuple[pd.DataFrame, Path]:
    path = resolve_source_file(symbol, "candle")
    df = pd.read_csv(path)
    df["open_time_dt"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    numeric_cols = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "trades",
        "taker_buy_base",
        "taker_buy_quote",
        "ignore",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.sort_values("open_time_dt").set_index("open_time_dt")
    hourly = df.resample("1h", label="left", closed="left").agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
            "close_time": "last",
            "quote_asset_volume": "sum",
            "trades": "sum",
            "taker_buy_base": "sum",
            "taker_buy_quote": "sum",
            "ignore": "last",
        }
    )
    hourly = hourly.dropna(subset=["open", "high", "low", "close"]).reset_index()
    hourly = hourly.rename(columns={"quote_asset_volume": "quote_volume"})
    return hourly, path


def read_funding(symbol: str) -> tuple[pd.DataFrame, Path]:
    path = resolve_source_file(symbol, "funding")
    df = pd.read_csv(path)
    df["fundingTime_dt"] = pd.to_datetime(df["fundingTime"], unit="ms", utc=True)
    df["fundingRate"] = pd.to_numeric(df["fundingRate"], errors="coerce")
    return df.sort_values("fundingTime_dt").reset_index(drop=True), path


def read_open_interest(symbol: str) -> tuple[pd.DataFrame, Path]:
    path = resolve_source_file(symbol, "oi")
    df = pd.read_csv(path)
    df["open_time_dt"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df["sumOpenInterest"] = pd.to_numeric(df["sumOpenInterest"], errors="coerce")
    df["sumOpenInterestValue"] = pd.to_numeric(df["sumOpenInterestValue"], errors="coerce")
    return df.sort_values("open_time_dt").reset_index(drop=True), path


def clamp(val: float, low: float, high: float) -> float:
    return max(low, min(high, val))


def compute_cell1_row(row: pd.Series) -> tuple[float, float, float, float]:
    er = 0.0
    r1 = row["rvol_1h"]
    if r1 >= 1.25:
        er += 1
    if r1 >= 1.75:
        er += 2
    if r1 >= 2.5:
        er += 2

    r4 = row["rvol_4h_window"]
    if r4 >= 1.25:
        er += 1
    if r4 >= 1.75:
        er += 1

    c24 = row["change_24h"]
    if 2 <= c24 < 4:
        er += 1
    elif 4 <= c24 <= 12:
        er += 3
    elif 12 < c24 <= 16:
        er += 2
    elif 16 < c24 <= 25:
        er += 1

    if row["near_breakout"]:
        er += 2
    if row["clean_reclaim"]:
        er += 1

    er = clamp(er, 0, 10)

    fmlc = 0.0
    v_usd = row["volume_usd"]
    if v_usd >= 20_000_000:
        fmlc += 3
    elif v_usd >= 5_000_000:
        fmlc += 2
    elif v_usd >= 1_000_000:
        fmlc += 1

    if row["range_pos_50_4h"] >= 0.55:
        fmlc += 2
    if row["range_pos_20"] >= 0.65:
        fmlc += 2
    if row["clean_reclaim"]:
        fmlc += 2
    if row["above_4h_trend"]:
        fmlc += 1
    if c24 <= 16:
        fmlc += 1
    elif c24 > 25:
        fmlc -= 3

    fmlc = clamp(fmlc, 0, 10)

    flow = 0.0
    if r1 >= 1.5:
        flow += 2
    if r1 >= 2.5:
        flow += 1
    if r4 >= 1.25:
        flow += 1
    if row["open_interest"] > 0:
        flow += 1

    fnd = row["funding"]
    if -0.0005 <= fnd <= 0.0008:
        flow += 2
    elif 0.0008 < fnd <= 0.0015:
        flow += 1
    elif fnd > 0.002:
        flow -= 2

    if row["close"] > row["ema_21"]:
        flow += 1
    if row["near_breakout"]:
        flow += 1

    flow = clamp(flow, 0, 8)
    raw_score = round(er * 0.35 + fmlc * 0.35 + flow * 0.30, 2)
    return er, fmlc, flow, raw_score


def enrich_symbol(symbol: str) -> tuple[pd.DataFrame, dict]:
    candles_1h, candle_path = read_5m_candles(symbol)
    funding_df, funding_path = read_funding(symbol)
    oi_df, oi_path = read_open_interest(symbol)

    df = candles_1h.copy().sort_values("open_time_dt").reset_index(drop=True)
    df["high_20"] = df["high"].rolling(20).max()
    df["low_20"] = df["low"].rolling(20).min()
    df["vol_avg_20"] = df["quote_volume"].rolling(20).mean()
    df["rvol_1h"] = df["quote_volume"] / df["vol_avg_20"]

    df["vol_last_4h"] = df["quote_volume"].rolling(4).sum()
    df["vol_prev_4h"] = df["quote_volume"].shift(4).rolling(4).sum()
    df["rvol_4h_window"] = df["vol_last_4h"] / df["vol_prev_4h"]

    df["change_24h"] = df["close"].pct_change(24) * 100
    denom_20 = (df["high_20"] - df["low_20"]).replace(0, np.nan)
    df["range_pos_20"] = (df["close"] - df["low_20"]) / denom_20
    df["near_breakout"] = df["close"] >= (df["high_20"] * 0.992)

    df["ema_9"] = df["close"].ewm(span=9, adjust=False).mean()
    df["ema_21"] = df["close"].ewm(span=21, adjust=False).mean()
    df["clean_reclaim"] = (df["close"] > df["ema_21"]) & (df["ema_9"] > df["ema_21"])
    df["volume_usd"] = df["quote_volume"].rolling(24).sum()

    df_4h = df.set_index("open_time_dt")[["open", "high", "low", "close", "quote_volume"]].resample("4h", label="left", closed="left").agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "quote_volume": "sum",
        }
    )
    df_4h["high_50_4h"] = df_4h["high"].rolling(50).max()
    df_4h["low_50_4h"] = df_4h["low"].rolling(50).min()
    denom_50 = (df_4h["high_50_4h"] - df_4h["low_50_4h"]).replace(0, np.nan)
    df_4h["range_pos_50_4h"] = (df_4h["close"] - df_4h["low_50_4h"]) / denom_50
    df_4h["ema_50_4h"] = df_4h["close"].ewm(span=50, adjust=False).mean()
    df_4h = df_4h.reset_index().rename(columns={"open_time_dt": "dt_4h"})

    df["dt_4h"] = df["open_time_dt"].dt.floor("4h")
    df = df.merge(
        df_4h[["dt_4h", "range_pos_50_4h", "ema_50_4h"]],
        on="dt_4h",
        how="left",
    )
    df["above_4h_trend"] = df["close"] > df["ema_50_4h"]

    oi_df = oi_df.copy().sort_values("open_time_dt")
    df = pd.merge_asof(
        df.sort_values("open_time_dt"),
        oi_df[["open_time_dt", "sumOpenInterest", "sumOpenInterestValue"]],
        on="open_time_dt",
        direction="backward",
    )
    df["open_interest"] = df["sumOpenInterest"]

    funding_df = funding_df.copy().sort_values("fundingTime_dt")
    df = pd.merge_asof(
        df.sort_values("open_time_dt"),
        funding_df[["fundingTime_dt", "fundingRate"]],
        left_on="open_time_dt",
        right_on="fundingTime_dt",
        direction="backward",
    )
    df["funding"] = df["fundingRate"]

    df["open_interest"] = df["open_interest"].ffill().fillna(0.0)
    df["funding"] = df["funding"].ffill().fillna(0.0)
    df["range_pos_50_4h"] = df["range_pos_50_4h"].ffill().fillna(0.5)
    df["ema_50_4h"] = df["ema_50_4h"].ffill().fillna(df["close"])
    df["above_4h_trend"] = df["close"] > df["ema_50_4h"]

    df_final = df.tail(720).copy().reset_index(drop=True)

    ers: list[float] = []
    fmlcs: list[float] = []
    flows: list[float] = []
    raw_scores: list[float] = []
    for _, row in df_final.iterrows():
        er, fmlc, flow, raw_score = compute_cell1_row(row)
        ers.append(er)
        fmlcs.append(fmlc)
        flows.append(flow)
        raw_scores.append(raw_score)

    df_final["er"] = ers
    df_final["fmlc"] = fmlcs
    df_final["flowprint"] = flows
    df_final["raw_score"] = raw_scores
    df_final["is_stock_token"] = False

    export_df = pd.DataFrame({
        "ticker": symbol,
        "timestamp_utc": df_final["open_time_dt"].dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "price": df_final["close"].round(8),
        "change_24h_%": df_final["change_24h"].round(2),
        "volume_usd": df_final["volume_usd"].round(0),
        "rvol_1h": df_final["rvol_1h"].round(2),
        "rvol_4h_window": df_final["rvol_4h_window"].round(2),
        "er": df_final["er"],
        "fmlc": df_final["fmlc"],
        "flowprint": df_final["flowprint"],
        "raw_score": df_final["raw_score"],
        "near_breakout": df_final["near_breakout"],
        "clean_reclaim": df_final["clean_reclaim"],
        "above_4h_trend": df_final["above_4h_trend"],
        "range_pos_20": df_final["range_pos_20"].round(2),
        "range_pos_50_4h": df_final["range_pos_50_4h"].round(2),
        "open_interest": df_final["open_interest"].round(2),
        "funding": df_final["funding"].round(6),
        "ema_21": df_final["ema_21"].round(8),
        "is_stock_token": df_final["is_stock_token"],
    })

    source_meta = {
        "symbol": symbol,
        "candle_path": str(candle_path),
        "funding_path": str(funding_path),
        "open_interest_path": str(oi_path),
        "source_latest_timestamp": str(df_final["open_time_dt"].dt.strftime("%Y-%m-%dT%H:%M:%SZ").max()),
        "source_rows": len(export_df),
    }
    return export_df, source_meta


def read_existing_latest_timestamp(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        df = pd.read_csv(path, usecols=["timestamp_utc"])
        if df.empty:
            return None
        return str(df["timestamp_utc"].max())
    except Exception:
        return None


def build_audit_report(
    df_all: pd.DataFrame,
    source_meta: list[dict],
    existing_latest: str | None,
    previous_mtime: str | None,
    new_mtime: str | None,
    status: str,
    reason: str,
) -> None:
    symbol_counts = df_all["ticker"].value_counts().sort_index()
    latest_by_symbol = df_all.groupby("ticker")["timestamp_utc"].max().to_dict()
    latest_overall = df_all["timestamp_utc"].max()
    lines = [
        "# FirestarterOG Real Historical Variance Sample Audit Report",
        "",
        f"**Run UTC Timestamp:** {datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}",
        "**Mode:** Local-only source refresh from existing repository data.",
        f"**Status:** {status}",
        f"**Reason:** {reason}",
        "",
        "## Output Summary",
        "",
        f"- **Current Latest Timestamp:** {latest_overall}",
        f"- **Previous CSV Latest Timestamp:** {existing_latest or 'N/A'}",
        f"- **Source File MTime Before:** {previous_mtime or 'N/A'}",
        f"- **Source File MTime After:** {new_mtime or 'N/A'}",
        f"- **Symbols Processed:** {len(SYMBOLS)}",
        f"- **Total Rows:** {len(df_all)}",
        "",
        "## Symbol Coverage",
        "",
        "| Symbol | Rows | Latest Timestamp (UTC) |",
        "|---|---:|---|",
    ]
    for symbol in SYMBOLS:
        lines.append(f"| {symbol} | {int(symbol_counts.get(symbol, 0))} | {latest_by_symbol.get(symbol, 'N/A')} |")

    lines.extend([
        "",
        "## Local Source Files Used",
        "",
        "| Symbol | Candle CSV | Funding CSV | Open Interest CSV |",
        "|---|---|---|---|",
    ])
    for meta in source_meta:
        lines.append(
            f"| {meta['symbol']} | `{meta['candle_path']}` | `{meta['funding_path']}` | `{meta['open_interest_path']}` |"
        )

    lines.extend([
        "",
        "## Governance and Safety",
        "",
        "- Research-only local refresh lane.",
        "- No Binance network calls were used.",
        "- No trading recommendations were generated.",
        "- No scoring formula changes were made.",
        "- No generated HTML was committed.",
        "- No raw data was committed.",
        "- Cell 2 was not used.",
        "- ML was not used.",
        "",
        status,
        "",
    ])
    AUDIT_OUTPUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    existing_latest = read_existing_latest_timestamp(CSV_OUTPUT)
    previous_mtime = None
    if CSV_OUTPUT.exists():
        previous_mtime = datetime.fromtimestamp(CSV_OUTPUT.stat().st_mtime, timezone.utc).isoformat().replace("+00:00", "Z")

    all_frames: list[pd.DataFrame] = []
    source_meta: list[dict] = []

    for symbol in SYMBOLS:
        print(f"Processing local OG symbol: {symbol}")
        df_sym, meta = enrich_symbol(symbol)
        all_frames.append(df_sym)
        source_meta.append(meta)

    df_all = pd.concat(all_frames, ignore_index=True)
    df_all = df_all.sort_values(["ticker", "timestamp_utc"]).reset_index(drop=True)
    new_latest = str(df_all["timestamp_utc"].max())
    new_mtime = None

    if existing_latest is not None and new_latest <= existing_latest:
        reason = (
            f"Local refresh did not advance the source sample. Existing latest={existing_latest}, "
            f"new latest={new_latest}."
        )
        build_audit_report(df_all, source_meta, existing_latest, previous_mtime, new_mtime, "HOLD_TRUE_OG_SOURCE_REFRESH_SOURCE_NOT_NEWER", reason)
        print(reason)
        return 1

    df_all.to_csv(CSV_OUTPUT, index=False)
    new_mtime = datetime.fromtimestamp(CSV_OUTPUT.stat().st_mtime, timezone.utc).isoformat().replace("+00:00", "Z")
    build_audit_report(
        df_all,
        source_meta,
        existing_latest,
        previous_mtime,
        new_mtime,
        "PASS_TRUE_OG_SOURCE_REFRESH_AND_VIEWER_UPDATED",
        "Local source sample refreshed from existing repository data and advanced successfully.",
    )
    print(f"Saved source sample: {CSV_OUTPUT}")
    print(f"Saved audit report: {AUDIT_OUTPUT}")
    print(f"Latest timestamp: {new_latest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
