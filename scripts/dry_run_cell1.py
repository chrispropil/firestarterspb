import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "research" / "binance_5_token_1month"
OUTPUT_DIR = ROOT / "data" / "research" / "binance_5_token_1month_cell1"
SYMBOLS = ["SOLUSDT", "XRPUSDT", "DOGEUSDT", "LINKUSDT", "AVAXUSDT"]

# Partial-window starts
OI_1H_START = pd.to_datetime("2026-05-06T21:00:00Z").tz_convert('UTC')
OI_4H_START = pd.to_datetime("2026-05-07T00:00:00Z").tz_convert('UTC')

def verify_raw_files():
    files = list(DATA_DIR.glob("*.csv"))
    print(f"Total raw CSV files found in {DATA_DIR}: {len(files)}")
    return len(files) == 50

def align_and_compute_mock_cell1(symbol: str, timeframe: str):
    # Load candles
    candle_file = DATA_DIR / f"{symbol}_futures_klines_{timeframe}.csv"
    df_candles = pd.read_csv(candle_file)
    df_candles['open_time_dt'] = pd.to_datetime(df_candles['open_time_utc'], format='ISO8601').dt.tz_convert('UTC')
    
    # Check row counts & duplicates
    expected_rows = 744 if timeframe == "1h" else 186
    assert len(df_candles) == expected_rows, f"Unexpected row count: {len(df_candles)} (expected {expected_rows})"
    assert df_candles['open_time_dt'].duplicated().sum() == 0, f"Duplicate timestamps found in candles!"
    
    # Sort
    df_candles = df_candles.sort_values('open_time_dt').reset_index(drop=True)
    
    # Load funding
    funding_file = DATA_DIR / f"{symbol}_funding_rate_history.csv"
    df_funding = pd.read_csv(funding_file)
    df_funding['fundingTime_dt'] = pd.to_datetime(df_funding['fundingTime_utc'], format='ISO8601').dt.tz_convert('UTC')
    # Round to nearest 8H to correct the millisecond API offset
    df_funding['fundingTime_norm'] = df_funding['fundingTime_dt'].dt.round('8h')
    df_funding = df_funding.sort_values('fundingTime_norm').reset_index(drop=True)
    
    # Load OI
    oi_file = DATA_DIR / f"{symbol}_open_interest_statistics_{timeframe}.csv"
    df_oi = pd.read_csv(oi_file) if oi_file.exists() else pd.DataFrame()
    if not df_oi.empty:
        df_oi['timestamp_dt'] = pd.to_datetime(df_oi['timestamp_utc'], format='ISO8601').dt.tz_convert('UTC')
        df_oi = df_oi.sort_values('timestamp_dt').reset_index(drop=True)
        
    # Load top long-short account ratio
    acc_file = DATA_DIR / f"{symbol}_top_trader_account_ratio_{timeframe}.csv"
    df_acc = pd.read_csv(acc_file) if acc_file.exists() else pd.DataFrame()
    if not df_acc.empty:
        df_acc['timestamp_dt'] = pd.to_datetime(df_acc['timestamp_utc'], format='ISO8601').dt.tz_convert('UTC')
        df_acc = df_acc.sort_values('timestamp_dt').reset_index(drop=True)
        
    # Load top long-short position ratio
    pos_file = DATA_DIR / f"{symbol}_top_trader_position_ratio_{timeframe}.csv"
    df_pos = pd.read_csv(pos_file) if pos_file.exists() else pd.DataFrame()
    if not df_pos.empty:
        df_pos['timestamp_dt'] = pd.to_datetime(df_pos['timestamp_utc'], format='ISO8601').dt.tz_convert('UTC')
        df_pos = df_pos.sort_values('timestamp_dt').reset_index(drop=True)
        
    # Build output table using open_time_dt as anchors
    rows = []
    partial_start = OI_1H_START if timeframe == "1h" else OI_4H_START
    
    for _, candle in df_candles.iterrows():
        t = candle['open_time_dt']
        
        # Funding join (latest funding rate at or before candle timestamp)
        funding_matches = df_funding[df_funding['fundingTime_norm'] <= t]
        if not funding_matches.empty:
            last_funding = funding_matches.iloc[-1]
            funding_rate = last_funding['fundingRate']
            funding_status = "full_window_available"
        else:
            funding_rate = np.nan
            funding_status = "unavailable"
            
        # Open Interest and Top-Trader Gating check
        if t < partial_start:
            oi_status = "partial_parent_unavailable"
            top_trader_status = "partial_parent_unavailable"
            sum_oi = np.nan
            long_short_acc = np.nan
            long_short_pos = np.nan
        else:
            # Match OI
            oi_match = df_oi[df_oi['timestamp_dt'] == t]
            sum_oi = oi_match.iloc[0]['sumOpenInterest'] if not oi_match.empty else np.nan
            oi_status = "full_window_available" if not np.isnan(sum_oi) else "unavailable"
            
            # Match long/short account
            acc_match = df_acc[df_acc['timestamp_dt'] == t]
            long_short_acc = acc_match.iloc[0]['longShortRatio'] if not acc_match.empty else np.nan
            
            # Match long/short position
            pos_match = df_pos[df_pos['timestamp_dt'] == t]
            long_short_pos = pos_match.iloc[0]['longShortRatio'] if not pos_match.empty else np.nan
            
            top_trader_status = "full_window_available" if (not np.isnan(long_short_acc) and not np.isnan(long_short_pos)) else "unavailable"
            
        # Mock formula computation using placeholder/mock logic
        # Mock ER uses only candle info (rvol mockup)
        mock_er = 5.0
        er_status = "full_window_available"
        
        # Mock FMLC uses OI and top trader
        if oi_status == "partial_parent_unavailable" or top_trader_status == "partial_parent_unavailable":
            mock_fmlc = np.nan
            fmlc_status = "partial_parent_unavailable"
        else:
            mock_fmlc = 5.0
            fmlc_status = "full_window_available"
            
        # Mock Flowprint-proxy
        if oi_status == "partial_parent_unavailable" or top_trader_status == "partial_parent_unavailable":
            mock_flowprint = np.nan
            flowprint_status = "partial_parent_unavailable"
        else:
            mock_flowprint = 4.0
            flowprint_status = "full_window_available"
            
        # Mock raw_score
        if er_status == "full_window_available" and fmlc_status == "full_window_available" and flowprint_status == "full_window_available":
            mock_raw_score = mock_er * 0.35 + mock_fmlc * 0.35 + mock_flowprint * 0.30
            raw_score_status = "full_window_available"
        else:
            mock_raw_score = np.nan
            raw_score_status = "parent_gated_unavailable"
            
        rows.append({
            "symbol": symbol,
            "timeframe": timeframe,
            "timestamp_utc": candle['open_time_utc'],
            "er_value": mock_er,
            "er_parent_status": er_status,
            "fmlc_value": mock_fmlc,
            "fmlc_parent_status": fmlc_status,
            "flowprint_proxy_value": mock_flowprint,
            "flowprint_parent_status": flowprint_status,
            "raw_score": mock_raw_score,
            "raw_score_parent_status": raw_score_status,
            "funding_parent_status": funding_status,
            "oi_parent_status": oi_status,
            "top_trader_parent_status": top_trader_status,
            "partial_window_flag": 1 if t < partial_start else 0
        })
        
    df_out = pd.DataFrame(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUTPUT_DIR / f"{symbol}_{timeframe}_cell1_dry_run.csv"
    df_out.to_csv(out_file, index=False)
    
    # Validation assertions
    assert len(df_out) == expected_rows
    gated_rows = df_out[df_out['partial_window_flag'] == 1]
    expected_gated = 21 if timeframe == "1h" else 6
    assert len(gated_rows) == expected_gated, f"Gated row count mismatch: {len(gated_rows)} vs {expected_gated}"
    assert gated_rows['oi_parent_status'].eq("partial_parent_unavailable").all()
    assert gated_rows['top_trader_parent_status'].eq("partial_parent_unavailable").all()
    assert gated_rows['fmlc_parent_status'].eq("partial_parent_unavailable").all()
    assert gated_rows['flowprint_parent_status'].eq("partial_parent_unavailable").all()
    assert gated_rows['raw_score_parent_status'].eq("parent_gated_unavailable").all()
    
    print(f"[{symbol} {timeframe}] Success! Created {out_file.name} with {len(df_out)} rows. Gated: {len(gated_rows)} rows.")
    return len(df_out), len(gated_rows)

def run_dry_run():
    if not verify_raw_files():
        print("Pre-flight check: raw CSV files count check FAILED!")
        return False
    
    total_processed = 0
    for symbol in SYMBOLS:
        for timeframe in ["1h", "4h"]:
            rows, gated = align_and_compute_mock_cell1(symbol, timeframe)
            total_processed += rows
            
    print(f"\nDry-run completed successfully! Total processed output rows: {total_processed}")
    return True

if __name__ == "__main__":
    run_dry_run()
