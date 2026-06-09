"""Build a compact Firestarter Live Audits AI match index.

Research-only utility.

This script is intended to create a compact, derived, AI-readable table from the
local Binance Top100 FirestarterOG research dataset. It does not modify source
market data, scanner files, dashboard HTML, or existing raw artifacts.

IMPORTANT:
- No trading signals.
- No strategy validation.
- No Cell 2 labels.
- No live execution.
- No raw 5-minute export in the output index.

The first implementation pass should reuse metric logic from:
    scripts/visualization/build_top100_clean_html_dashboard.py

Default output:
    reports/firestarter_live_audits/ai_match_index.csv
    reports/firestarter_live_audits/ai_match_index_summary.md
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


DEFAULT_CANDLES_DIR = Path(
    r"C:\firestarterspb\data\research\binance_top100_excluding_existing_5_1month"
)
DEFAULT_DERIVATIVES_DIR = Path(
    r"C:\firestarterspb\data\research\binance_top100_derivatives_context_1month"
)
DEFAULT_OUTPUT = Path("reports/firestarter_live_audits/ai_match_index.csv")

REQUIRED_COLUMNS = [
    "timestamp",
    "symbol",
    "close",
    "er",
    "fmlc",
    "flowprint",
    "raw_score",
    "x2_candidate",
    "hollow_breakout",
    "fake_recovery",
    "domino_deterioration",
    "entry_c_recovery",
    "primary_event_type",
    "secondary_tags",
    "data_quality_flags",
    "nan_pct_score",
    "deriv_available",
]


@dataclass(frozen=True)
class BuildSummary:
    run_timestamp_utc: str
    source_candle_dir: str
    source_derivatives_dir: str
    output_path: str
    symbols_seen: int
    symbols_written: int
    row_count: int
    first_timestamp: str
    last_timestamp: str
    notes: list[str]


@dataclass(frozen=True)
class BuildResult:
    rows: list[dict[str, object]]
    symbols_written: int
    first_timestamp: str
    last_timestamp: str
    notes: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Firestarter Live Audits compact AI match index."
    )
    parser.add_argument("--candles-dir", type=Path, default=DEFAULT_CANDLES_DIR)
    parser.add_argument("--derivatives-dir", type=Path, default=DEFAULT_DERIVATIVES_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Inspect inputs and report intended output without writing CSV.",
    )
    return parser.parse_args()


def discover_symbols(candles_dir: Path) -> list[str]:
    """Discover symbols from local Top100 candle CSV filenames.

    Expected filename pattern:
        <SYMBOL>_1month_5m.csv
    """
    if not candles_dir.exists():
        return []

    symbols: list[str] = []
    for path in sorted(candles_dir.glob("*_1month_5m.csv")):
        symbol = path.name.replace("_1month_5m.csv", "")
        if symbol:
            symbols.append(symbol)
    return symbols


def load_derivatives_data(symbol: str, derivatives_dir: Path) -> dict[str, pd.DataFrame]:
    data: dict[str, pd.DataFrame] = {}
    subdirs = [
        "fundingRate",
        "openInterestHist",
        "takerlongshortRatio",
        "globalLongShortAccountRatio",
        "topLongShortAccountRatio",
        "topLongShortPositionRatio",
        "premiumIndex",
    ]

    for subdir in subdirs:
        file_path = derivatives_dir / subdir / f"{symbol}_{subdir}.csv"
        if not file_path.exists():
            continue

        try:
            df_temp = pd.read_csv(file_path)
            if df_temp.empty:
                continue

            time_col = (
                "fundingTime"
                if subdir == "fundingRate"
                else ("time" if subdir == "premiumIndex" else "timestamp")
            )
            if time_col not in df_temp.columns:
                continue

            df_temp["datetime"] = pd.to_datetime(df_temp[time_col], unit="ms", utc=True)
            data[subdir] = df_temp
        except Exception:
            continue

    return data


def merge_derivatives(
    df_1h: pd.DataFrame, deriv_data: dict[str, pd.DataFrame]
) -> pd.DataFrame:
    df_merged = df_1h.copy().sort_index()

    if "fundingRate" in deriv_data:
        df_f = (
            deriv_data["fundingRate"][["datetime", "fundingRate"]]
            .dropna()
            .sort_values("datetime")
        )
        df_merged = pd.merge_asof(
            df_merged,
            df_f.set_index("datetime"),
            left_index=True,
            right_index=True,
            direction="backward",
        )
    else:
        df_merged["fundingRate"] = np.nan

    if "openInterestHist" in deriv_data:
        df_oi = (
            deriv_data["openInterestHist"][
                ["datetime", "sumOpenInterest", "sumOpenInterestValue"]
            ]
            .dropna()
            .sort_values("datetime")
        )
        df_merged = pd.merge_asof(
            df_merged,
            df_oi.set_index("datetime"),
            left_index=True,
            right_index=True,
            direction="backward",
            tolerance=pd.Timedelta("15Min"),
        )
    else:
        df_merged["sumOpenInterest"] = np.nan
        df_merged["sumOpenInterestValue"] = np.nan

    if "takerlongshortRatio" in deriv_data:
        df_t = (
            deriv_data["takerlongshortRatio"][["datetime", "buySellRatio"]]
            .dropna()
            .sort_values("datetime")
        )
        df_merged = pd.merge_asof(
            df_merged,
            df_t.set_index("datetime"),
            left_index=True,
            right_index=True,
            direction="backward",
            tolerance=pd.Timedelta("15Min"),
        )
    else:
        df_merged["buySellRatio"] = np.nan

    if "globalLongShortAccountRatio" in deriv_data:
        df_gls = (
            deriv_data["globalLongShortAccountRatio"][["datetime", "longShortRatio"]]
            .dropna()
            .sort_values("datetime")
        )
        df_merged = pd.merge_asof(
            df_merged,
            df_gls.set_index("datetime"),
            left_index=True,
            right_index=True,
            direction="backward",
            tolerance=pd.Timedelta("15Min"),
        )
    else:
        df_merged["longShortRatio"] = np.nan

    return df_merged


def compute_cell1_metrics(df_merged: pd.DataFrame) -> pd.DataFrame:
    df_merged["ema_21"] = df_merged["close"].ewm(span=21, adjust=False).mean()
    df_merged["vol_avg_10"] = df_merged["volume"].rolling(10).mean()
    df_merged["_ema_50"] = df_merged["close"].ewm(span=50, adjust=False).mean()

    df_merged["rvol_1h"] = df_merged["volume"] / df_merged["volume"].rolling(24).mean()
    df_merged["vol_4h"] = df_merged["volume"].rolling(4).sum()
    df_merged["rvol_4h"] = df_merged["vol_4h"] / df_merged["vol_4h"].rolling(96).mean()

    df_merged["change_24h"] = (
        (df_merged["close"] - df_merged["close"].shift(24))
        / df_merged["close"].shift(24)
        * 100
    )

    high_20 = df_merged["high"].rolling(20).max()
    rvol = df_merged["rvol_1h"]

    rvol_score = np.zeros(len(df_merged))
    rvol_score[rvol > 2.5] = 4
    rvol_score[(rvol > 1.8) & (rvol <= 2.5)] = 3
    rvol_score[(rvol > 1.2) & (rvol <= 1.8)] = 2
    rvol_score[(rvol > 0.8) & (rvol <= 1.2)] = 1

    near_breakout = np.zeros(len(df_merged))
    near_breakout[df_merged["close"] >= 0.99 * high_20] = 3
    near_breakout[
        (df_merged["close"] >= 0.975 * high_20)
        & (df_merged["close"] < 0.99 * high_20)
    ] = 1

    clean_reclaim = np.zeros(len(df_merged))
    clean_reclaim[
        (df_merged["close"] > df_merged["ema_21"])
        & (df_merged["volume"] > 1.2 * df_merged["vol_avg_10"])
    ] = 3

    er_raw = rvol_score + near_breakout + clean_reclaim
    df_merged["er"] = np.clip(er_raw, 0, 10)

    er_na = df_merged["close"].isna() | df_merged["rvol_1h"].isna() | high_20.isna()
    df_merged.loc[er_na, "er"] = np.nan

    df_merged["quote_volume"] = df_merged["volume"] * df_merged["close"]
    df_merged["quote_volume_24h"] = df_merged["quote_volume"].rolling(24).sum()

    high_200 = df_merged["high"].rolling(200).max()
    low_200 = df_merged["low"].rolling(200).min()
    rp_200 = (df_merged["close"] - low_200) / (high_200 - low_200) * 10

    low_20 = df_merged["low"].rolling(20).min()
    rp_20 = (df_merged["close"] - low_20) / (high_20 - low_20) * 10

    composite_rp = 0.5 * rp_200 + 0.5 * rp_20
    composite_rp_score = composite_rp / 2.0

    trend_score = np.zeros(len(df_merged))
    trend_score[df_merged["close"] > df_merged["_ema_50"]] = 3
    trend_score[
        (df_merged["close"] <= df_merged["_ema_50"])
        & (df_merged["close"] > df_merged["ema_21"])
    ] = 1

    funding_score = np.zeros(len(df_merged))
    funding_score[df_merged["fundingRate"] <= 0.0001] = 2
    funding_score[
        (df_merged["fundingRate"] > 0.0001)
        & (df_merged["fundingRate"] <= 0.0005)
    ] = 1

    governor_penalty = np.zeros(len(df_merged))
    governor_penalty[
        (df_merged["change_24h"] >= 15) | (df_merged["change_24h"] <= -15)
    ] = 4

    fmlc_raw = composite_rp_score + trend_score + funding_score - governor_penalty
    df_merged["fmlc"] = np.clip(fmlc_raw, 0, 10)
    df_merged.loc[df_merged["quote_volume_24h"] < 10000000, "fmlc"] = 0

    fmlc_na = (
        df_merged["fundingRate"].isna()
        | df_merged["change_24h"].isna()
        | high_200.isna()
        | low_20.isna()
    )
    df_merged.loc[fmlc_na, "fmlc"] = np.nan

    df_merged["oi_change_1h"] = (
        (df_merged["sumOpenInterest"] - df_merged["sumOpenInterest"].shift(1))
        / df_merged["sumOpenInterest"].shift(1)
        * 100
    )

    funding_quality = np.zeros(len(df_merged))
    funding_quality[
        (df_merged["fundingRate"] >= -0.0001)
        & (df_merged["fundingRate"] <= 0.0003)
    ] = 2

    taker_ratio = df_merged["buySellRatio"] / (df_merged["buySellRatio"] + 1)
    taker_score = np.zeros(len(df_merged))
    taker_score[taker_ratio >= 0.52] = 2
    taker_score[(taker_ratio >= 0.48) & (taker_ratio < 0.52)] = 1

    rvol_fp_score = np.zeros(len(df_merged))
    rvol_fp_score[rvol > 1.5] = 2
    rvol_fp_score[(rvol > 1.0) & (rvol <= 1.5)] = 1

    oi_score = np.zeros(len(df_merged))
    oi_score[df_merged["oi_change_1h"] > 1.5] = 2
    oi_score[
        (df_merged["oi_change_1h"] > 0) & (df_merged["oi_change_1h"] <= 1.5)
    ] = 1

    flowprint_raw = funding_quality + taker_score + rvol_fp_score + oi_score
    df_merged["flowprint"] = np.clip(flowprint_raw, 0, 8)

    flowprint_na = (
        df_merged["volume"].isna()
        | df_merged["buySellRatio"].isna()
        | df_merged["sumOpenInterest"].isna()
        | df_merged["fundingRate"].isna()
        | df_merged["oi_change_1h"].isna()
    )
    df_merged.loc[flowprint_na, "flowprint"] = np.nan

    raw_score = (
        df_merged["er"] * 0.35
        + df_merged["fmlc"] * 0.35
        + df_merged["flowprint"] * 0.30
    )
    df_merged["raw_score"] = np.clip(raw_score / 0.94, 0, 10)

    raw_score_na = (
        df_merged["er"].isna()
        | df_merged["fmlc"].isna()
        | df_merged["flowprint"].isna()
    )
    df_merged.loc[raw_score_na, "raw_score"] = np.nan

    df_merged.drop(columns=["_ema_50"], errors="ignore", inplace=True)
    return df_merged


def resample_symbol_candles(candle_path: Path) -> tuple[pd.DataFrame, list[str]]:
    notes: list[str] = []
    df = pd.read_csv(candle_path)
    required = {"open_time", "open", "high", "low", "close", "volume"}
    missing = sorted(required - set(df.columns))
    if missing:
        notes.append(f"{candle_path.name}: missing columns {','.join(missing)}")
        return pd.DataFrame(), notes

    df["open_datetime"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df = df.sort_values("open_datetime")
    df_resample = df.set_index("open_datetime")
    df_1h = (
        df_resample.resample("1h")
        .agg(
            {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",
            }
        )
        .dropna()
    )
    return df_1h, notes


def _compact_bool(value: object) -> str:
    if pd.isna(value):
        return ""
    return "1" if bool(value) else "0"


def _compact_float(value: object, digits: int = 6) -> str:
    if pd.isna(value):
        return ""
    return f"{float(value):.{digits}f}".rstrip("0").rstrip(".")


def _event_fields(row: pd.Series) -> tuple[str, str]:
    events = []

    if row["x2_candidate"]:
        events.append("x2_candidate")
    if row["hollow_breakout"]:
        events.append("hollow_breakout")
    if row["fake_recovery"]:
        events.append("fake_recovery")
    if row["domino_deterioration"]:
        events.append("domino_deterioration")
    if row["entry_c_recovery"]:
        events.append("entry_c_recovery")

    primary = events[0] if events else "none"
    secondary = "|".join(events[1:])
    return primary, secondary


def _quality_flags(row: pd.Series) -> str:
    flags = []
    if row["nan_pct_score"] > 0:
        flags.append("metric_nan")
    if not row["deriv_available"]:
        flags.append("no_derivatives")
    if row["close"] <= 0:
        flags.append("nonpositive_close")
    if row["symbol_nonstandard"]:
        flags.append("nonstandard_symbol")
    return "|".join(flags) if flags else "ok"


def build_symbol_frame(
    symbol: str, candles_dir: Path, derivatives_dir: Path
) -> tuple[pd.DataFrame, list[str]]:
    candle_path = candles_dir / f"{symbol}_1month_5m.csv"
    df_1h, notes = resample_symbol_candles(candle_path)
    if df_1h.empty:
        return pd.DataFrame(), notes

    deriv_data = load_derivatives_data(symbol, derivatives_dir)
    df_merged = merge_derivatives(df_1h, deriv_data)
    df_merged = compute_cell1_metrics(df_merged)

    df_merged["symbol"] = symbol
    df_merged["timestamp"] = df_merged.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    df_merged["deriv_available"] = bool(deriv_data)
    df_merged["symbol_nonstandard"] = not symbol.isascii()
    df_merged["return_1h_pct"] = df_merged["close"].pct_change() * 100
    df_merged["raw_score_delta_3h"] = df_merged["raw_score"] - df_merged["raw_score"].shift(3)
    df_merged["fmlc_delta_3h"] = df_merged["fmlc"] - df_merged["fmlc"].shift(3)
    df_merged["close_delta_3h_pct"] = df_merged["close"].pct_change(3) * 100
    df_merged["close_gt_ema21"] = df_merged["close"] > df_merged["ema_21"]
    df_merged["prior_close_lte_ema21"] = df_merged["close"].shift(1) <= df_merged[
        "ema_21"
    ].shift(1)
    df_merged["near_high_20"] = df_merged["close"] >= 0.99 * df_merged[
        "high"
    ].rolling(20).max()

    return df_merged, notes


def add_research_flags(df_all: pd.DataFrame) -> pd.DataFrame:
    if df_all.empty:
        return df_all

    df_all = df_all.copy()
    df_all["return_rank_1h"] = df_all.groupby("timestamp")["return_1h_pct"].rank(
        pct=True
    )
    df_all["nan_pct_score"] = (
        df_all[["er", "fmlc", "flowprint", "raw_score"]].isna().mean(axis=1) * 100
    )

    df_all["x2_candidate"] = (
        (df_all["return_rank_1h"] < 0.90)
        & (df_all["rvol_4h"] < 1.5)
        & df_all["raw_score"].notna()
    )
    df_all["hollow_breakout"] = (
        df_all["near_high_20"]
        & (df_all["rvol_1h"] < 1.0)
        & df_all["flowprint"].fillna(0).le(2)
    )
    df_all["fake_recovery"] = (
        df_all["close_gt_ema21"]
        & df_all["prior_close_lte_ema21"]
        & df_all["raw_score"].fillna(0).lt(4)
    )
    df_all["domino_deterioration"] = (
        df_all["raw_score_delta_3h"].lt(-2)
        & df_all["fmlc_delta_3h"].lt(-1)
        & df_all["close_delta_3h_pct"].lt(0)
    )
    df_all["entry_c_recovery"] = (
        df_all["close_gt_ema21"]
        & df_all["raw_score_delta_3h"].gt(1)
        & df_all["fmlc_delta_3h"].gt(0)
        & df_all["flowprint"].fillna(0).ge(3)
    )

    event_values = df_all.apply(_event_fields, axis=1, result_type="expand")
    df_all["primary_event_type"] = event_values[0]
    df_all["secondary_tags"] = event_values[1]
    df_all["data_quality_flags"] = df_all.apply(_quality_flags, axis=1)

    return df_all


def build_rows(
    symbols: Iterable[str], candles_dir: Path, derivatives_dir: Path
) -> BuildResult:
    frames: list[pd.DataFrame] = []
    notes: list[str] = []

    for symbol in symbols:
        frame, symbol_notes = build_symbol_frame(symbol, candles_dir, derivatives_dir)
        notes.extend(symbol_notes)
        if not frame.empty:
            frames.append(frame)

    if not frames:
        return BuildResult([], 0, "N/A", "N/A", notes)

    df_all = pd.concat(frames, axis=0, ignore_index=False)
    df_all = add_research_flags(df_all)
    df_all = df_all.sort_values(["timestamp", "symbol"])

    rows: list[dict[str, object]] = []
    for _, row in df_all.iterrows():
        rows.append(
            {
                "timestamp": row["timestamp"],
                "symbol": row["symbol"],
                "close": _compact_float(row["close"]),
                "er": _compact_float(row["er"]),
                "fmlc": _compact_float(row["fmlc"]),
                "flowprint": _compact_float(row["flowprint"]),
                "raw_score": _compact_float(row["raw_score"]),
                "x2_candidate": _compact_bool(row["x2_candidate"]),
                "hollow_breakout": _compact_bool(row["hollow_breakout"]),
                "fake_recovery": _compact_bool(row["fake_recovery"]),
                "domino_deterioration": _compact_bool(row["domino_deterioration"]),
                "entry_c_recovery": _compact_bool(row["entry_c_recovery"]),
                "primary_event_type": row["primary_event_type"],
                "secondary_tags": row["secondary_tags"],
                "data_quality_flags": row["data_quality_flags"],
                "nan_pct_score": _compact_float(row["nan_pct_score"], digits=2),
                "deriv_available": _compact_bool(row["deriv_available"]),
            }
        )

    first_timestamp = str(df_all["timestamp"].iloc[0])
    last_timestamp = str(df_all["timestamp"].iloc[-1])
    symbols_written = int(df_all["symbol"].nunique())
    return BuildResult(rows, symbols_written, first_timestamp, last_timestamp, notes)


def write_csv(output_path: Path, rows: Iterable[dict[str, object]]) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    row_count = 0
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in REQUIRED_COLUMNS})
            row_count += 1
    return row_count


def write_summary(summary_path: Path, summary: BuildSummary) -> None:
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    notes = "\n".join(f"- {note}" for note in summary.notes) if summary.notes else "- None"
    content = f"""# Firestarter Live Audits — AI Match Index Summary

## Status

Research-only derived index summary.

## Run

| Field | Value |
|---|---|
| run_timestamp_utc | `{summary.run_timestamp_utc}` |
| source_candle_dir | `{summary.source_candle_dir}` |
| source_derivatives_dir | `{summary.source_derivatives_dir}` |
| output_path | `{summary.output_path}` |
| symbols_seen | `{summary.symbols_seen}` |
| symbols_written | `{summary.symbols_written}` |
| row_count | `{summary.row_count}` |
| first_timestamp | `{summary.first_timestamp}` |
| last_timestamp | `{summary.last_timestamp}` |

## Notes

{notes}

## Boundary

This index is research-only. It is not a strategy table, signal table, Cell 2 label table, alert source, or execution artifact.
"""
    summary_path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    run_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    symbols = discover_symbols(args.candles_dir)
    notes: list[str] = []

    if not symbols:
        notes.append("No symbols discovered from candle directory.")

    build = build_rows(symbols, args.candles_dir, args.derivatives_dir)

    if args.dry_run:
        print("DRY RUN - no files written")
        print(f"candles_dir={args.candles_dir}")
        print(f"derivatives_dir={args.derivatives_dir}")
        print(f"symbols_seen={len(symbols)}")
        print(f"symbols_written={build.symbols_written}")
        print(f"row_count={len(build.rows)}")
        print(f"first_timestamp={build.first_timestamp}")
        print(f"last_timestamp={build.last_timestamp}")
        print(f"output={args.output}")
        if build.notes:
            print("notes=" + " | ".join(build.notes[:10]))
        return 0

    row_count = write_csv(args.output, build.rows)
    summary = BuildSummary(
        run_timestamp_utc=run_timestamp,
        source_candle_dir=str(args.candles_dir),
        source_derivatives_dir=str(args.derivatives_dir),
        output_path=str(args.output),
        symbols_seen=len(symbols),
        symbols_written=build.symbols_written,
        row_count=row_count,
        first_timestamp=build.first_timestamp,
        last_timestamp=build.last_timestamp,
        notes=notes + build.notes,
    )
    write_summary(args.output.with_name("ai_match_index_summary.md"), summary)

    print(f"Wrote {args.output}")
    print(f"Wrote {args.output.with_name('ai_match_index_summary.md')}")
    print(f"row_count={row_count}")
    print(f"symbols_seen={len(symbols)}")
    print(f"symbols_written={build.symbols_written}")
    print(f"first_timestamp={build.first_timestamp}")
    print(f"last_timestamp={build.last_timestamp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
