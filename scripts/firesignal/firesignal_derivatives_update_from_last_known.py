import os
import sys
import time
import urllib.request
import urllib.parse
import json
import csv
import shutil
from pathlib import Path
from datetime import datetime, timezone

from firesignal_state import load_symbols
from firesignal_validate_derivatives_update import validate_staging_deriv_file, validate_merged_deriv_data, EXPECTED_HEADERS, TIME_KEY_INDICES
from firesignal_update_from_last_known import trigger_viewer_rebuild, STAGING_DIR

DERIV_DIRS = [
    "C:/firestarterspb/data/research/binance_top100_derivatives_context_1month",
    "C:/firestarterspb/data/research/binance_core88_missing_derivatives_context_1month"
]

METRICS = ["fundingRate", "openInterestHist", "takerlongshortRatio", "globalLongShortAccountRatio"]

def find_deriv_file(symbol, metric):
    for d in DERIV_DIRS:
        path = Path(d) / metric / f"{symbol}_{metric}.csv"
        if path.exists():
            return path
    return None

def get_last_timestamp(filepath, metric):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                return None
            rows = list(reader)
            if not rows:
                return None
            
            time_key_idx = TIME_KEY_INDICES.get(metric, 3)
            last_row = rows[-1]
            return int(float(last_row[time_key_idx]))
    except Exception as e:
        print(f"  [ERROR] Parsing last timestamp for {filepath}: {e}")
        return None

def fetch_deriv_data(metric, symbol, start_ms, end_ms, stats):
    """
    Fetches derivatives history from Binance public futures data API.
    """
    if metric == "fundingRate":
        url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&startTime={start_ms}&endTime={end_ms}&limit=500"
    else:
        url = f"https://fapi.binance.com/futures/data/{metric}?symbol={symbol}&period=1h&startTime={start_ms}&endTime={end_ms}&limit=500"
        
    retries = 3
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            code = getattr(e, 'code', None)
            if code == 400:
                # Symbol might not support the metric
                return []
            if attempt == retries - 1:
                print(f"    [ERROR] Binance derivatives pull failed for {symbol} ({metric}): {e}")
                return None
            stats["retries_triggered"] += 1
            time.sleep(2 ** attempt + 0.1)
    return None

def perform_derivatives_update(dry_run=False, max_intervals=None):
    """
    Performs updates on the four derivatives metrics for all active symbols.
    Returns (verdict, reason, stats)
    """
    symbols = load_symbols()
    if not symbols:
        return "HOLD_FIRESIGNAL_DERIVED_FORMULA_SOURCE_MISSING", "Symbol list is empty.", {}
        
    print(f"\n[DERIVATIVES] Auditing files for {len(symbols)} symbols...")
    file_map = {}
    last_timestamps = {m: [] for m in METRICS}
    
    # Audit files first
    for symbol in symbols:
        file_map[symbol] = {}
        for m in METRICS:
            filepath = find_deriv_file(symbol, m)
            if not filepath:
                return "HOLD_FIRESIGNAL_DERIVED_FORMULA_SOURCE_MISSING", f"Derivatives file for {symbol} ({m}) not found.", {}
            file_map[symbol][m] = str(filepath)
            
            ts = get_last_timestamp(filepath, m)
            if ts is not None:
                last_timestamps[m].append(ts)
                
    # Global timestamp limits
    global_limits = {}
    for m in METRICS:
        if last_timestamps[m]:
            global_limits[m] = {
                "min": min(last_timestamps[m]),
                "max": max(last_timestamps[m])
            }
        else:
            global_limits[m] = {"min": None, "max": None}
            
    print("[DERIVATIVES AUDIT RESULT]")
    for m in METRICS:
        lim = global_limits[m]
        min_utc = datetime.fromtimestamp(lim['min']/1000, tz=timezone.utc).isoformat() if lim['min'] else "N/A"
        max_utc = datetime.fromtimestamp(lim['max']/1000, tz=timezone.utc).isoformat() if lim['max'] else "N/A"
        print(f"  Metric {m}: Min last timestamp: {min_utc} | Max last timestamp: {max_utc}")

    # Estimate missing ranges
    now_ms = int(time.time() * 1000)
    max_history_ms = 29 * 24 * 60 * 60 * 1000  # 29 days retention cap
    safe_start_boundary = now_ms - max_history_ms
    
    update_stats = {
        "derivatives_rows_pulled": 0,
        "derivatives_rows_added": 0,
        "derivatives_rows_deduped": 0,
        "derivatives_files_written": 0,
        "derivatives_symbols_updated": [],
        "retries_triggered": 0
    }
    
    if dry_run:
        print("[DRY-RUN] Simulating derivatives pull. No files will be modified.")
        return "PASS_FIRESIGNAL_DERIVATIVES_CONTEXT_UPDATED_FLOWPRINT_SCORE_CURRENT", "Dry run successful.", update_stats

    # Staging dir
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    
    # We do a symbol-by-symbol update
    success_count = 0
    fail_count = 0
    
    for idx, symbol in enumerate(symbols, 1):
        print(f"\n[{idx}/{len(symbols)}] Updating Derivatives for: {symbol}")
        symbol_success = True
        
        for m in METRICS:
            hist_path = file_map[symbol][m]
            last_ts = get_last_timestamp(hist_path, m)
            if last_ts is None:
                # If file is empty, start from 29 days ago
                last_ts = safe_start_boundary
                
            start_ms = last_ts + 1000 # 1 second after last known timestamp
            start_ms = max(start_ms, safe_start_boundary)
            end_ms = now_ms
            
            # Limit bounded max intervals if required
            if max_intervals is not None:
                # 1 interval for derivatives is 1 hour
                target_end_ms = last_ts + (max_intervals * 60 * 60 * 1000)
                end_ms = min(end_ms, target_end_ms)
                
            if start_ms >= end_ms:
                # Already up to date
                continue
                
            # Fetch from API
            data = fetch_deriv_data(m, symbol, start_ms, end_ms, update_stats)
            if data is None:
                print(f"    [ERROR] Fetch failed for {symbol} ({m})")
                symbol_success = False
                break
                
            if not data:
                # Empty but valid response (no new funding intervals or no trade activity)
                continue
                
            update_stats["derivatives_rows_pulled"] += len(data)
            
            # Write to staging
            stage_path = STAGING_DIR / f"{symbol}_{m}_staging.csv"
            cols = EXPECTED_HEADERS[m]
            
            try:
                staged_count = 0
                time_col = "fundingTime" if m == "fundingRate" else "timestamp"
                with open(stage_path, "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(cols)
                    for item in data:
                        ts_val = item.get(time_col)
                        if ts_val is not None:
                            try:
                                if int(float(ts_val)) <= last_ts:
                                    continue
                            except ValueError:
                                pass
                        row = []
                        for col in cols:
                            if col == "symbol":
                                val = item.get("symbol", symbol)
                            else:
                                val = item.get(col, "")
                            row.append(val)
                        writer.writerow(row)
                        staged_count += 1
            except Exception as e:
                print(f"    [ERROR] Staging save error for {symbol} ({m}): {e}")
                symbol_success = False
                break
                
            if staged_count == 0:
                if stage_path.exists():
                    stage_path.unlink()
                continue
                
            # Validate staging file
            val_success, val_info = validate_staging_deriv_file(stage_path, m, last_ts)
            if not val_success:
                print(f"    [ERROR] Staging validation failed for {symbol} ({m}): {val_info}")
                symbol_success = False
                break
                
            # Merge staging with historical
            temp_path = hist_path + ".tmp"
            try:
                # Read historical
                hist_rows = []
                with open(hist_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    for r in reader:
                        hist_rows.append(r)
                        
                # Read staging
                stage_rows = []
                with open(stage_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    for r in reader:
                        stage_rows.append(r)
                        
                # Merge by time key
                time_idx = TIME_KEY_INDICES.get(m, 3)
                merged_dict = {}
                for r in hist_rows:
                    merged_dict[int(float(r[time_idx]))] = r
                for r in stage_rows:
                    merged_dict[int(float(r[time_idx]))] = r
                    
                sorted_keys = sorted(merged_dict.keys())
                
                original_total = len(hist_rows) + len(stage_rows)
                final_total = len(sorted_keys)
                rows_added = final_total - len(hist_rows)
                rows_deduped = original_total - final_total
                
                update_stats["derivatives_rows_added"] += rows_added
                update_stats["derivatives_rows_deduped"] += rows_deduped
                
                # Write merged to temp
                with open(temp_path, "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(cols)
                    for k in sorted_keys:
                        writer.writerow(merged_dict[k])
                        
                # Validate merged file
                merged_val_success, val_count = validate_merged_deriv_data(temp_path, m)
                if not merged_val_success:
                    print(f"    [ERROR] Merged validation failed for {symbol} ({m}): {val_count}")
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    symbol_success = False
                    break
                    
                # Swap files
                shutil.move(temp_path, hist_path)
                update_stats["derivatives_files_written"] += 1
                
            except Exception as e:
                print(f"    [ERROR] Merge failed for {symbol} ({m}): {e}")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                symbol_success = False
                break
                
            finally:
                if os.path.exists(stage_path):
                    os.remove(stage_path)
                    
            time.sleep(0.05)
            
        if symbol_success:
            update_stats["derivatives_symbols_updated"].append(symbol)
            success_count += 1
        else:
            fail_count += 1
            return "HOLD_FIRESIGNAL_DERIVATIVES_ENDPOINT_OR_SCHEMA_ISSUE", f"Failed to update derivatives context for symbol {symbol}", update_stats
            
    print(f"\n[DERIVATIVES DONE] Success count: {success_count}/{len(symbols)}")
    return "PASS_FIRESIGNAL_DERIVATIVES_CONTEXT_UPDATED_FLOWPRINT_SCORE_CURRENT", "Derivatives context updated successfully.", update_stats
