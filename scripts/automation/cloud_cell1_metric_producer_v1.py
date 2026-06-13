#!/usr/bin/env python3
"""
Cloud Cell 1 Metric Producer v1 for firestarterspb.

This script fetches public market data from Bitget for an approved list of 25 symbols
and computes point-in-time Cell 1 metrics (ER, FMLC, Flowprint, Raw Score) without credentials
or order execution code.
"""

import os
import sys
import json
import csv
import argparse
import time
import urllib.request
import urllib.error
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
APPROVED_OUTPUT_DIR = REPO_ROOT / "state" / "cloud_pattern_watch"
APPROVED_REPORT_DIR = REPO_ROOT / "reports" / "cloud_pattern_watch" / "v1"
MANUAL_BUILD_CONFIRMATION = "CELL1_MANUAL_BUILD_APPROVED"

def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def resolve_repo_path(path_value):
    path = Path(path_value)
    if path.is_absolute():
        return path.resolve()
    return (REPO_ROOT / path).resolve()

def repo_relative(path):
    return str(path.resolve().relative_to(REPO_ROOT)).replace("\\", "/")

def ensure_approved_output_paths(config):
    output_dir = resolve_repo_path(config.get("output_dir", "state/cloud_pattern_watch"))
    report_dir = resolve_repo_path(config.get("report_dir", "reports/cloud_pattern_watch/v1"))
    if output_dir != APPROVED_OUTPUT_DIR.resolve():
        raise ValueError("output_dir must be state/cloud_pattern_watch")
    if report_dir != APPROVED_REPORT_DIR.resolve():
        raise ValueError("report_dir must be reports/cloud_pattern_watch/v1")
    return output_dir, report_dir

def write_manual_build_status(mode, gate_result, symbols, symbol_governance, output_paths, safety_flags, message):
    output_dir = APPROVED_OUTPUT_DIR
    report_dir = APPROVED_REPORT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "timestamp_utc": utc_now(),
        "mode": mode,
        "gate_result": gate_result,
        "message": message,
        "symbol_count": len(symbols),
        "max_symbols": symbol_governance.get("max_symbols"),
        "excluded_symbols": symbol_governance.get("excluded_symbols", []),
        "output_paths": output_paths,
        "safety_flags": safety_flags,
    }
    status_path = output_dir / "cell1_manual_build_gate_status.json"
    manifest_path = report_dir / "cell1_manual_build_gate_manifest.json"
    status_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Manual build status path: {repo_relative(status_path)}")
    print(f"Manual build manifest path: {repo_relative(manifest_path)}")
    return payload

def safety_flags():
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

def load_governed_symbol_config(symbols_file):
    if not os.path.exists(symbols_file):
        raise ValueError(f"Symbols file not found at {symbols_file}")

    with open(symbols_file, "r", encoding="utf-8") as f:
        payload = json.load(f)

    if isinstance(payload, list):
        raise ValueError("Symbols JSON must be the governed object from origin/main, not a bare list")
    if not isinstance(payload, dict):
        raise ValueError("Symbols JSON must be an object")

    required_keys = ["symbols", "max_symbols", "excluded_symbols", "status"]
    missing = [key for key in required_keys if key not in payload]
    if missing:
        raise ValueError(f"Symbols JSON missing required governed keys: {', '.join(missing)}")

    symbols = payload["symbols"]
    max_symbols = payload["max_symbols"]
    excluded_symbols = payload["excluded_symbols"]
    status = payload["status"]

    if not isinstance(symbols, list):
        raise ValueError("Symbols JSON field 'symbols' must be a list")
    if not isinstance(max_symbols, int):
        raise ValueError("Symbols JSON field 'max_symbols' must be an integer")
    if not isinstance(excluded_symbols, list):
        raise ValueError("Symbols JSON field 'excluded_symbols' must be a list")
    if not isinstance(status, str):
        raise ValueError("Symbols JSON field 'status' must be a string")

    normalized_symbols = [str(symbol).strip().upper() for symbol in symbols if str(symbol).strip()]
    normalized_excluded = {str(symbol).strip().upper() for symbol in excluded_symbols if str(symbol).strip()}

    if len(normalized_symbols) != len(symbols):
        raise ValueError("Symbols JSON contains blank or invalid symbol entries")
    if len(normalized_symbols) > max_symbols:
        raise ValueError(f"Symbol count ({len(normalized_symbols)}) exceeds governed max_symbols ({max_symbols})")
    if max_symbols != 25:
        raise ValueError(f"Governed max_symbols must equal 25 for Issue #10, got {max_symbols}")

    blocked = sorted(symbol for symbol in normalized_symbols if symbol in normalized_excluded)
    if blocked:
        raise ValueError(f"Excluded symbols present in governed symbol list: {', '.join(blocked)}")

    return normalized_symbols, {
        "status": status,
        "max_symbols": max_symbols,
        "excluded_symbols": sorted(normalized_excluded),
    }

def safe_float(val):
    try:
        if val is None:
            return 0.0
        return float(val)
    except:
        return 0.0

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))

def calculate_atr(df_1h, period=14):
    if len(df_1h) < period + 1:
        return 0.0
    high = df_1h["high"].astype(float)
    low = df_1h["low"].astype(float)
    close = df_1h["close"].astype(float)
    prev_close = close.shift(1)
    
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return float(tr.rolling(period).mean().iloc[-1])

def fetch_json(url, timeout=10, retries=3):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
                else:
                    raise urllib.error.URLError(f"HTTP Status {response.status}")
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(0.5 * (attempt + 1))

def process_symbol(sym, base_url):
    """
    Fetches public REST data for a symbol and computes all Cell 1 metrics.
    """
    er_parent_status = "PASS"
    fmlc_parent_status = "PASS"
    flowprint_parent_status = "PASS"
    raw_score_parent_status = "PASS"
    
    data_1h = []
    data_4h = []
    funding_data = []
    oi_val = 0.0
    
    # 1. Fetch 1H candles
    try:
        url_1h = f"{base_url}/api/v2/mix/market/candles?symbol={sym}&productType=USDT-FUTURES&granularity=1H&limit=100"
        res_1h = fetch_json(url_1h)
        data_1h = res_1h.get("data", [])
        if len(data_1h) < 50:
            er_parent_status = "FAIL_INSUFFICIENT_1H_HISTORY"
    except Exception as e:
        er_parent_status = f"FAIL_API_1H_ERROR: {str(e)}"
        
    # 2. Fetch 4H candles
    try:
        url_4h = f"{base_url}/api/v2/mix/market/candles?symbol={sym}&productType=USDT-FUTURES&granularity=4H&limit=100"
        res_4h = fetch_json(url_4h)
        data_4h = res_4h.get("data", [])
        if len(data_4h) < 50:
            fmlc_parent_status = "FAIL_INSUFFICIENT_4H_HISTORY"
    except Exception as e:
        fmlc_parent_status = f"FAIL_API_4H_ERROR: {str(e)}"
        
    # 3. Fetch Funding rates
    try:
        url_fund = f"{base_url}/api/v2/mix/market/history-fund-rate?symbol={sym}&productType=USDT-FUTURES&pageSize=100"
        res_fund = fetch_json(url_fund)
        raw_fund = res_fund.get("data", [])
        for item in raw_fund:
            fr = safe_float(item.get("fundingRate"))
            ts = int(item.get("fundingTime", 0))
            funding_data.append((ts, fr))
        funding_data.sort(key=lambda x: x[0])
    except Exception as e:
        flowprint_parent_status = f"FAIL_API_FUNDING_ERROR: {str(e)}"
        
    # 4. Fetch Open Interest
    try:
        url_oi = f"{base_url}/api/v2/mix/market/open-interest?symbol={sym}&productType=USDT-FUTURES"
        res_oi = fetch_json(url_oi)
        oi_list = res_oi.get("data", {}).get("openInterestList", [])
        if oi_list:
            oi_val = safe_float(oi_list[0].get("size", 0))
        else:
            flowprint_parent_status = "FAIL_OI_MISSING"
    except Exception as e:
        flowprint_parent_status = f"FAIL_API_OI_ERROR: {str(e)}"

    # Determine initial validation passes
    if "FAIL" in er_parent_status:
        fmlc_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
        flowprint_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
        raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
    else:
        er_parent_status = "PASS"
        
        if "FAIL" in fmlc_parent_status:
            raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
        else:
            fmlc_parent_status = "PASS"
            
        if "FAIL" in flowprint_parent_status:
            raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
        else:
            flowprint_parent_status = "PASS"
            
        if er_parent_status == "PASS" and fmlc_parent_status == "PASS" and flowprint_parent_status == "PASS":
            raw_score_parent_status = "PASS"
        else:
            raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"

    # Compute if ER parent status is PASS
    if er_parent_status == "PASS":
        try:
            df_1h = pd.DataFrame(data_1h, columns=["ts", "open", "high", "low", "close", "volume", "volume_quote"])
            df_1h["ts"] = df_1h["ts"].astype(int)
            for col in ["open", "high", "low", "close", "volume", "volume_quote"]:
                df_1h[col] = df_1h[col].astype(float)
            df_1h = df_1h.sort_values("ts").reset_index(drop=True)
            
            # Drop current active incomplete candle (last row after sorting)
            df_1h = df_1h.iloc[:-1].reset_index(drop=True)
            
            latest_row = df_1h.iloc[-1]
            current_ts = int(latest_row["ts"])
            price = float(latest_row["close"])
            
            # Format timestamp
            dt = datetime.fromtimestamp(current_ts / 1000.0, tz=timezone.utc)
            timestamp_utc = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # price_position: close location value relative to high/low of latest complete bar
            bar_high = float(latest_row["high"])
            bar_low = float(latest_row["low"])
            price_position = (price - bar_low) / (bar_high - bar_low) if (bar_high - bar_low) > 0 else 0.0
            
            # RVOL 1H
            vol_now = float(latest_row["volume_quote"])
            vol_avg_20 = float(df_1h["volume_quote"].iloc[-20:].mean())
            rvol_1h = vol_now / vol_avg_20 if vol_avg_20 > 0 else 0.0
            
            # RVOL 4H
            vol_last_4h = float(df_1h["volume_quote"].iloc[-4:].sum())
            vol_prev_4h = float(df_1h["volume_quote"].iloc[-8:-4].sum())
            rvol_4h_window = vol_last_4h / vol_prev_4h if vol_prev_4h > 0 else 0.0
            
            # EMAs
            ema_9 = float(df_1h["close"].ewm(span=9).mean().iloc[-1])
            ema_21 = float(df_1h["close"].ewm(span=21).mean().iloc[-1])
            
            # ATR
            atr_1h = calculate_atr(df_1h, 14)
            
            # range_pos_20
            high_20 = float(df_1h["high"].iloc[-20:].max())
            low_20 = float(df_1h["low"].iloc[-20:].min())
            range_20 = high_20 - low_20
            range_pos_20 = (price - low_20) / range_20 if range_20 > 0 else 0.0
            
            # near_breakout, clean_reclaim
            near_breakout = price >= high_20 * 0.992
            clean_reclaim = bool(price > ema_21 and ema_9 > ema_21)
            
            # 24H volume and change
            if len(df_1h) >= 24:
                close_24h = float(df_1h["close"].iloc[-24])
                change_24h = ((price - close_24h) / close_24h) * 100 if close_24h > 0 else 0.0
                volume_usd = float(df_1h["volume_quote"].iloc[-24:].sum())
            else:
                change_24h = 0.0
                volume_usd = float(df_1h["volume_quote"].sum())
                
            # ER formula
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
        except Exception as e:
            er_parent_status = f"FAIL_COMPUTE_ER_ERROR: {str(e)}"
            price = None
            price_position = None
            timestamp_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            rvol_1h = 0.0
            rvol_4h_window = 0.0
            range_pos_20 = 0.0
            near_breakout = False
            clean_reclaim = False
            er = "BLOCKED_PARENT_FIELD_FAILED"
            fmlc_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
            flowprint_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
            raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
    else:
        price = None
        price_position = None
        timestamp_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rvol_1h = 0.0
        rvol_4h_window = 0.0
        range_pos_20 = 0.0
        near_breakout = False
        clean_reclaim = False
        er = "BLOCKED_PARENT_FIELD_FAILED"

    # Compute FMLC if PASS
    if fmlc_parent_status == "PASS" and er_parent_status == "PASS":
        try:
            df_4h = pd.DataFrame(data_4h, columns=["ts", "open", "high", "low", "close", "volume", "volume_quote"])
            df_4h["ts"] = df_4h["ts"].astype(int)
            for col in ["open", "high", "low", "close", "volume", "volume_quote"]:
                df_4h[col] = df_4h[col].astype(float)
            df_4h = df_4h.sort_values("ts").reset_index(drop=True)
            
            # Drop current active 4H candle
            df_4h = df_4h.iloc[:-1].reset_index(drop=True)
            
            # Align 4H up to current_ts
            sub_4h = df_4h[df_4h["ts"] <= current_ts]
            if len(sub_4h) >= 50:
                high_50_4h = float(sub_4h["high"].iloc[-50:].max())
                low_50_4h = float(sub_4h["low"].iloc[-50:].min())
                range_50_4h = high_50_4h - low_50_4h
                range_pos_50_4h = (price - low_50_4h) / range_50_4h if range_50_4h > 0 else 0.0
                
                ema_50_4h = float(sub_4h["close"].ewm(span=50).mean().iloc[-1])
                above_4h_trend = bool(price > ema_50_4h)
                
                # FMLC calculation
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
            else:
                fmlc_parent_status = "FAIL_INSUFFICIENT_ALIGNED_4H_HISTORY"
                range_pos_50_4h = 0.0
                above_4h_trend = False
                fmlc = "BLOCKED_PARENT_FIELD_FAILED"
                raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
        except Exception as e:
            fmlc_parent_status = f"FAIL_COMPUTE_FMLC_ERROR: {str(e)}"
            range_pos_50_4h = 0.0
            above_4h_trend = False
            fmlc = "BLOCKED_PARENT_FIELD_FAILED"
            raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
    else:
        range_pos_50_4h = 0.0
        above_4h_trend = False
        fmlc = "BLOCKED_PARENT_FIELD_FAILED"

    # Compute Flowprint if PASS
    if flowprint_parent_status == "PASS" and er_parent_status == "PASS":
        try:
            # Find latest funding rate <= current_ts
            current_funding = 0.0
            if funding_data:
                valid_fundings = [f for f in funding_data if f[0] <= current_ts]
                if valid_fundings:
                    current_funding = valid_fundings[-1][1]
                else:
                    current_funding = funding_data[0][1]
            else:
                # If funding data from API is completely empty
                flowprint_parent_status = "FAIL_FUNDING_EMPTY"
                raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
            
            if "FAIL" not in flowprint_parent_status:
                # Flowprint formula
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
            else:
                current_funding = 0.0
                flowprint = "BLOCKED_PARENT_FIELD_FAILED"
        except Exception as e:
            flowprint_parent_status = f"FAIL_COMPUTE_FLOWPRINT_ERROR: {str(e)}"
            current_funding = 0.0
            flowprint = "BLOCKED_PARENT_FIELD_FAILED"
            raw_score_parent_status = "BLOCKED_PARENT_FIELD_FAILED"
    else:
        current_funding = 0.0
        flowprint = "BLOCKED_PARENT_FIELD_FAILED"

    # Compute Raw Score if PASS
    if raw_score_parent_status == "PASS":
        try:
            raw_score = (er * 0.35) + (fmlc * 0.35) + (flowprint * 0.30)
        except Exception as e:
            raw_score_parent_status = f"FAIL_COMPUTE_RAW_SCORE_ERROR: {str(e)}"
            raw_score = "BLOCKED_PARENT_FIELD_FAILED"
    else:
        raw_score = "BLOCKED_PARENT_FIELD_FAILED"

    # Assemble row matching exact column order and names
    row = {
        "symbol": sym,
        "timestamp_utc": timestamp_utc,
        "price": round(price, 8) if price is not None else "",
        "price_position": round(price_position, 4) if price_position is not None else "",
        "er": round(er, 1) if isinstance(er, (int, float)) else er,
        "fmlc": round(fmlc, 1) if isinstance(fmlc, (int, float)) else fmlc,
        "flowprint": round(flowprint, 1) if isinstance(flowprint, (int, float)) else flowprint,
        "raw_score": round(raw_score, 4) if isinstance(raw_score, (int, float)) else raw_score,
        "rvol_1h": round(rvol_1h, 4) if rvol_1h is not None else "",
        "rvol_4h_window": round(rvol_4h_window, 4) if rvol_4h_window is not None else "",
        "funding": round(current_funding, 6) if current_funding is not None else "",
        "open_interest": round(oi_val, 2) if oi_val is not None else "",
        "range_pos_20": round(range_pos_20, 4) if range_pos_20 is not None else "",
        "range_pos_50_4h": round(range_pos_50_4h, 4) if range_pos_50_4h is not None else "",
        "near_breakout": near_breakout if near_breakout is not None else "",
        "clean_reclaim": clean_reclaim if clean_reclaim is not None else "",
        "above_4h_trend": above_4h_trend if above_4h_trend is not None else "",
        "er_parent_status": er_parent_status,
        "fmlc_parent_status": fmlc_parent_status,
        "flowprint_parent_status": flowprint_parent_status,
        "raw_score_parent_status": raw_score_parent_status
    }
    
    return row

def run_dry_run(symbols, config, symbol_governance):
    print("--------------------------------------------------")
    print("RUNNING DRY-RUN MODE (No API calls or file writes)")
    print("--------------------------------------------------")
    print(f"Loaded symbols file: {config.get('symbols_file')}")
    print(f"Symbol config status: {symbol_governance.get('status')}")
    print(f"Governed max_symbols: {symbol_governance.get('max_symbols')}")
    print(f"Governed excluded_symbols: {', '.join(symbol_governance.get('excluded_symbols', [])) or '(none)'}")
    print(f"Base API URL: {config.get('base_url')}")
    print(f"Output directory: {config.get('output_dir')}")
    print(f"Report directory: {config.get('report_dir')}")
    print(f"Symbols universe (total {len(symbols)}):")
    for s in symbols:
        print(f" - {s}")
    print("--------------------------------------------------")
    print("Dry-run validation complete. Exiting cleanly.")
    return 0

def run_build(symbols, config):
    print("--------------------------------------------------")
    print("RUNNING BUILD MODE (Fetching active Bitget data)")
    print("--------------------------------------------------")
    
    approved_output_dir, approved_report_dir = ensure_approved_output_paths(config)
    output_dir = approved_output_dir
    report_dir = approved_report_dir
    base_url = config.get("base_url", "https://api.bitget.com")
    if base_url != "https://api.bitget.com":
        raise ValueError("base_url must remain the approved public Bitget endpoint")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    
    output_rows = []
    success_count = 0
    fail_count = 0
    errors = {}
    
    for idx, sym in enumerate(symbols):
        print(f"[{idx+1}/{len(symbols)}] Processing {sym}...")
        try:
            row = process_symbol(sym, base_url)
            # If the calculation failed completely or timed out
            if row["raw_score_parent_status"] == "FAIL" or "FAIL" in row["er_parent_status"]:
                fail_count += 1
                errors[sym] = row["er_parent_status"]
            else:
                success_count += 1
            output_rows.append(row)
        except Exception as e:
            fail_count += 1
            errors[sym] = str(e)
            print(f"Error processing {sym}: {str(e)}")
            # Append empty fallback row with error status
            fallback = {
                "symbol": sym,
                "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
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
                "er_parent_status": f"FAIL_EXCEPTION: {str(e)}",
                "fmlc_parent_status": "BLOCKED_PARENT_FIELD_FAILED",
                "flowprint_parent_status": "BLOCKED_PARENT_FIELD_FAILED",
                "raw_score_parent_status": "BLOCKED_PARENT_FIELD_FAILED"
            }
            output_rows.append(fallback)
        
        # Sleep to respect rate limits
        time.sleep(0.3)
        
    # Order columns matching requirement exactly
    columns = [
        "symbol", "timestamp_utc", "price", "price_position", "er", "fmlc", "flowprint", "raw_score",
        "rvol_1h", "rvol_4h_window", "funding", "open_interest", "range_pos_20",
        "range_pos_50_4h", "near_breakout", "clean_reclaim", "above_4h_trend",
        "er_parent_status", "fmlc_parent_status", "flowprint_parent_status",
        "raw_score_parent_status"
    ]
    
    # 1. Write current_metrics.json
    json_path = output_dir / "current_metrics.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(output_rows, f, indent=2)
    print(f"Saved: {repo_relative(json_path)}")
        
    # 2. Write current_metrics.csv
    csv_path = output_dir / "current_metrics.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"Saved: {repo_relative(csv_path)}")
        
    # 3. Write cell1_metric_producer_status.json
    status_path = output_dir / "cell1_metric_producer_status.json"
    status = {
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "SUCCESS" if fail_count == 0 else "PARTIAL_FAILURE" if success_count > 0 else "FAILURE",
        "symbols_attempted": len(symbols),
        "symbols_successful": success_count,
        "symbols_failed": fail_count,
        "errors": errors,
        "output_files": [repo_relative(json_path), repo_relative(csv_path)]
    }
    with status_path.open("w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)
    print(f"Saved: {repo_relative(status_path)}")
        
    # 4. Write cell1_metric_producer_report.md
    report_path = report_dir / "cell1_metric_producer_report.md"
    report_lines = [
        f"# Cell 1 Metric Producer v1 Execution Report",
        "",
        f"- **Execution Time (UTC):** {status['timestamp_utc']}",
        f"- **Status:** `{status['status']}`",
        f"- **Symbols Processed:** {status['symbols_successful']} / {status['symbols_attempted']} successfully",
        "",
        "## Metrics Table",
        "",
        "| Symbol | Price | ER | FMLC | Flowprint | Raw Score | RVOL 1H | Funding | OI | ER Parent | FMLC Parent | Flowprint Parent |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in output_rows:
        price_str = f"{row['price']:.4f}" if isinstance(row['price'], (int, float)) else ""
        er_str = f"{row['er']:.1f}" if isinstance(row['er'], (int, float)) else str(row['er'])
        fmlc_str = f"{row['fmlc']:.1f}" if isinstance(row['fmlc'], (int, float)) else str(row['fmlc'])
        flow_str = f"{row['flowprint']:.1f}" if isinstance(row['flowprint'], (int, float)) else str(row['flowprint'])
        score_str = f"{row['raw_score']:.4f}" if isinstance(row['raw_score'], (int, float)) else str(row['raw_score'])
        rvol_str = f"{row['rvol_1h']:.2f}" if isinstance(row['rvol_1h'], (int, float)) else ""
        fund_str = f"{row['funding']:.6f}" if isinstance(row['funding'], (int, float)) else ""
        oi_str = f"{row['open_interest']:.2f}" if isinstance(row['open_interest'], (int, float)) else ""
        
        report_lines.append(
            f"| {row['symbol']} | {price_str} | {er_str} | {fmlc_str} | {flow_str} | {score_str} | "
            f"{rvol_str} | {fund_str} | {oi_str} | `{row['er_parent_status']}` | `{row['fmlc_parent_status']}` | `{row['flowprint_parent_status']}` |"
        )
        
    if errors:
        report_lines.extend([
            "",
            "## Execution Errors",
            "",
            "| Symbol | Error Description |",
            "|---|---|",
        ])
        for s, err in errors.items():
            report_lines.append(f"| {s} | {err} |")
            
    with report_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")
    print(f"Saved: {repo_relative(report_path)}")
    print("--------------------------------------------------")
    return 0 if fail_count == 0 else 1

def main():
    parser = argparse.ArgumentParser(description="Cloud Cell 1 Metric Producer v1")
    parser.add_argument("--config", default="configs/cloud_cell1_metric_producer_v1.json", help="Path to config JSON")
    parser.add_argument("--build", action="store_true", help="Rejected for this repair branch; dry-run only")
    parser.add_argument("--dry-run", action="store_true", help="Force dry-run mode")
    parser.add_argument("--manual-build", action="store_true", help="Run controlled manual build only with confirmation token")
    parser.add_argument("--confirm-manual-build", default="", help="Required exact token for controlled manual build")
    args = parser.parse_args()
    
    # 1. Load and validate config file
    if not os.path.exists(args.config):
        print(f"ERROR: Configuration file not found at {args.config}", file=sys.stderr)
        sys.exit(2)
        
    try:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to parse config JSON: {str(e)}", file=sys.stderr)
        sys.exit(2)
        
    # Validate required config keys
    required_keys = ["symbols_file", "base_url", "output_dir", "report_dir", "dry_run"]
    for k in required_keys:
        if k not in config:
            print(f"ERROR: Missing required config key '{k}'", file=sys.stderr)
            sys.exit(2)
            
    if args.build:
        print("ERROR: Legacy --build path is rejected; use the manual build gate only", file=sys.stderr)
        sys.exit(2)
        
    # 2. Load governed symbols object
    symbols_file = config["symbols_file"]
    try:
        symbols, symbol_governance = load_governed_symbol_config(symbols_file)
    except Exception as e:
        print(f"ERROR: Failed governed symbols validation: {str(e)}", file=sys.stderr)
        sys.exit(2)

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
            write_manual_build_status(
                "manual_build",
                "DENIED_CONFIRMATION_REQUIRED",
                symbols,
                symbol_governance,
                output_paths,
                safety_flags(),
                "Manual build denied: missing exact confirmation token.",
            )
            print("ERROR: Manual build requires --confirm-manual-build CELL1_MANUAL_BUILD_APPROVED", file=sys.stderr)
            sys.exit(2)

        print("--------------------------------------------------")
        print("MANUAL BUILD GATE APPROVED")
        print("--------------------------------------------------")
        print(f"Symbol count: {len(symbols)}")
        print(f"Governed max_symbols: {symbol_governance.get('max_symbols')}")
        print(f"Excluded symbols: {', '.join(symbol_governance.get('excluded_symbols', [])) or '(none)'}")
        for label, path in output_paths.items():
            print(f"{label}: {path}")
        write_manual_build_status(
            "manual_build",
            "APPROVED_CONFIRMED",
            symbols,
            symbol_governance,
            output_paths,
            safety_flags(),
            "Manual build approved by exact confirmation token.",
        )
        try:
            result = run_build(symbols, config)
            gate_result = "COMPLETED" if result == 0 else "COMPLETED_WITH_FAILURES"
            write_manual_build_status(
                "manual_build",
                gate_result,
                symbols,
                symbol_governance,
                output_paths,
                safety_flags(),
                f"Manual build finished with exit code {result}.",
            )
            sys.exit(result)
        except Exception as e:
            write_manual_build_status(
                "manual_build",
                "FAILED_EXCEPTION",
                symbols,
                symbol_governance,
                output_paths,
                safety_flags(),
                f"Manual build failed: {str(e)}",
            )
            print(f"ERROR: Manual build failed: {str(e)}", file=sys.stderr)
            sys.exit(1)

    if config["dry_run"] is not True and not args.dry_run:
        print("ERROR: Default behavior must remain dry-run; config dry_run must be true", file=sys.stderr)
        sys.exit(2)

    if args.confirm_manual_build:
        print("ERROR: --confirm-manual-build is only valid with --manual-build", file=sys.stderr)
        sys.exit(2)

    if args.dry_run or not args.manual_build:
        sys.exit(run_dry_run(symbols, config, symbol_governance))

if __name__ == "__main__":
    main()
