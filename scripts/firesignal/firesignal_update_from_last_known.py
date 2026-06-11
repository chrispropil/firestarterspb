import os
import sys
import time
import urllib.request
import urllib.parse
import json
import csv
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timezone

from firesignal_state import load_state, save_state, load_symbols, find_symbol_files, infer_last_timestamp
from firesignal_validate_update import validate_staging_file, validate_merged_data, EXPECTED_HEADER

STAGING_DIR = Path("C:/firestarterspb/data/staging")
MANIFEST_DIR = Path("C:/firestarterspb/reports/firesignal")
ACTIVE_VIEWER_PATH = Path("reports/html/pulled_143_evidence_viewer/index.html")

def fetch_symbol_klines(symbol, start_ms, end_ms):
    """
    Fetches 5m klines from Binance futures public API.
    """
    safe_symbol = urllib.parse.quote(symbol)
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={safe_symbol}&interval=5m&limit=1500&startTime={start_ms}&endTime={end_ms}"
    
    retries = 3
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            if attempt == retries - 1:
                print(f"    [ERROR] Binance pull failed for {symbol} after {retries} attempts: {e}")
                return None
            time.sleep(2 ** attempt + 0.1)
    return None

def perform_update_cycle(dry_run=False, max_intervals=None, viewer_only=False, bootstrap_check=False):
    """
    Executes a single update cycle.
    """
    result_manifest = {
        "status": "IN_PROGRESS",
        "last_successful_update_utc": None,
        "last_successful_5m_close_utc": None,
        "symbols_updated": [],
        "files_written": 0,
        "rows_added": 0,
        "rows_deduped": 0,
        "latest_manifest_path": None,
        "latest_viewer_path": str(ACTIVE_VIEWER_PATH),
        "updated_at_utc": datetime.now(timezone.utc).isoformat()
    }
    
    # Load state
    state = load_state()
    symbols = load_symbols()
    
    if not symbols:
        return "HOLD_FIRESIGNAL_BOOTSTRAP_APPROVAL_REQUIRED", "Symbol inventory empty or not found.", result_manifest
        
    file_map = find_symbol_files(symbols)
    if len(file_map) != len(symbols):
        return "HOLD_FIRESIGNAL_BOOTSTRAP_APPROVAL_REQUIRED", f"Missing physical files for some inventory symbols. Found {len(file_map)}/{len(symbols)}.", result_manifest
        
    # Get last known timestamp
    last_close_ms = None
    if state and state.get("last_successful_5m_close_utc"):
        try:
            dt = datetime.fromisoformat(state["last_successful_5m_close_utc"].replace("Z", "+00:00"))
            last_close_ms = int(dt.timestamp() * 1000)
            print(f"[STATE] Loaded last close from state file: {state['last_successful_5m_close_utc']} ({last_close_ms} ms)")
        except Exception as e:
            print(f"[WARNING] Failed to parse last close from state: {e}")
            
    if last_close_ms is None:
        print("[INFO] Inferring last close timestamp from existing files...")
        last_close_ms = infer_last_timestamp(file_map)
        if last_close_ms is None:
            return "HOLD_FIRESIGNAL_BOOTSTRAP_APPROVAL_REQUIRED", "Could not infer last timestamp from local files (bootstrap required).", result_manifest
        print(f"[INFO] Inferred last close: {datetime.fromtimestamp(last_close_ms/1000, tz=timezone.utc).isoformat()} ({last_close_ms} ms)")
        
    # Calculate intervals
    next_start_ms = last_close_ms + (5 * 60 * 1000)
    
    # Latest completed 5m candle close
    now_ms = int(time.time() * 1000)
    latest_completed_close_ms = (now_ms // (5 * 60 * 1000)) * (5 * 60 * 1000)
    
    # Bounded refresh
    if max_intervals is not None:
        target_end_ms = last_close_ms + (max_intervals * 5 * 60 * 1000)
        latest_completed_close_ms = min(latest_completed_close_ms, target_end_ms)
        
    print(f"Update Range: {datetime.fromtimestamp(next_start_ms/1000, tz=timezone.utc).isoformat()} to {datetime.fromtimestamp(latest_completed_close_ms/1000, tz=timezone.utc).isoformat()}")
    
    if next_start_ms > latest_completed_close_ms:
        print("[INFO] No new 5m intervals are completed yet.")
        if viewer_only:
            # Rebuild viewer
            print("[INFO] Rebuilding viewer only...")
            rebuild_success = trigger_viewer_rebuild()
            if rebuild_success:
                return "PASS_FIRESIGNAL_UPDATED_FROM_LAST_KNOWN_AND_VIEWER_REFRESHED", "No new intervals, but viewer rebuilt successfully.", result_manifest
            else:
                return "HOLD_FIRESIGNAL_UPDATE_PATH_AMBIGUOUS", "No new intervals, but viewer rebuild failed.", result_manifest
        return "PASS_FIRESIGNAL_RUN_ONCE_READY", "NO_NEW_5M_INTERVALS", result_manifest
        
    if bootstrap_check:
        print("[BOOTSTRAP CHECK SUCCESSFUL]")
        return "PASS_FIRESIGNAL_RUN_ONCE_READY", f"Bootstrap check successful. Range: {datetime.fromtimestamp(next_start_ms/1000, tz=timezone.utc).isoformat()} to {datetime.fromtimestamp(latest_completed_close_ms/1000, tz=timezone.utc).isoformat()}", result_manifest

    if viewer_only:
        # Rebuild viewer
        print("[INFO] Rebuilding viewer only...")
        rebuild_success = trigger_viewer_rebuild()
        if rebuild_success:
            return "PASS_FIRESIGNAL_UPDATED_FROM_LAST_KNOWN_AND_VIEWER_REFRESHED", "Viewer rebuilt successfully.", result_manifest
        else:
            return "HOLD_FIRESIGNAL_UPDATE_PATH_AMBIGUOUS", "Viewer rebuild failed.", result_manifest

    # If dry-run
    if dry_run:
        print("[DRY-RUN] Simulating live pull. No files will be modified.")
        return "PASS_FIRESIGNAL_RUN_ONCE_READY", f"Dry run successful. Estimated pull: {len(symbols)} symbols, range: {datetime.fromtimestamp(next_start_ms/1000, tz=timezone.utc).isoformat()} to {datetime.fromtimestamp(latest_completed_close_ms/1000, tz=timezone.utc).isoformat()}", result_manifest

    # Pulling data
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    staged_files = {}
    
    print(f"\n[LIVE PULL] Fetching data for {len(symbols)} symbols...")
    success_count = 0
    fail_count = 0
    
    for idx, symbol in enumerate(symbols, 1):
        print(f"  [{idx}/{len(symbols)}] Fetching {symbol}...", end="", flush=True)
        klines = fetch_symbol_klines(symbol, next_start_ms, latest_completed_close_ms)
        
        if klines is None:
            print(" FAIL")
            fail_count += 1
            # Clean up staged files and return HOLD
            cleanup_staging(staged_files.values())
            return "HOLD_FIRESIGNAL_UPDATE_PATH_AMBIGUOUS", f"Failed to pull klines for {symbol}.", result_manifest
            
        staging_file = STAGING_DIR / f"{symbol}_staging.csv"
        try:
            with open(staging_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(EXPECTED_HEADER)
                # Map raw klines fields
                for k in klines:
                    # Raw kline format from binance: [open_time, open, high, low, close, volume, close_time, quote_asset_volume, trades, taker_buy_base, taker_buy_quote, ignore]
                    writer.writerow(k[:len(EXPECTED_HEADER)])
            
            staged_files[symbol] = str(staging_file)
            print(f" SUCCESS ({len(klines)} rows)")
            success_count += 1
        except Exception as e:
            print(f" SAVE_ERROR ({e})")
            fail_count += 1
            cleanup_staging(staged_files.values())
            return "HOLD_FIRESIGNAL_UPDATE_PATH_AMBIGUOUS", f"Failed to save staging file for {symbol}: {e}", result_manifest
            
        # Rate limit protection
        time.sleep(0.05)
        
    # Validation step
    print("\n[VALIDATION] Validating staged files...")
    validated_stats = {}
    for symbol, stage_path in staged_files.items():
        success, info = validate_staging_file(stage_path, last_close_ms)
        if not success:
            print(f"  [ERROR] Staging validation failed for {symbol}: {info}")
            cleanup_staging(staged_files.values())
            return "HOLD_FIRESIGNAL_UPDATE_PATH_AMBIGUOUS", f"Staging validation failed for {symbol}: {info}", result_manifest
        validated_stats[symbol] = info
        
    # Safe Merge step
    print("\n[MERGE] Merging staging files into historical data...")
    total_added = 0
    total_deduped = 0
    merged_files = []
    
    for symbol, stage_path in staged_files.items():
        hist_path = file_map[symbol]
        temp_path = hist_path + ".tmp"
        
        try:
            # Read historical rows
            hist_rows = []
            with open(hist_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None) # skip header
                for r in reader:
                    hist_rows.append(r)
                    
            # Read staging rows
            stage_rows = []
            with open(stage_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None) # skip header
                for r in reader:
                    stage_rows.append(r)
                    
            # Merge and deduplicate
            # We map open_time (index 0) as key to avoid duplicates
            merged_dict = {}
            for r in hist_rows:
                merged_dict[int(float(r[0]))] = r
            for r in stage_rows:
                merged_dict[int(float(r[0]))] = r
                
            sorted_keys = sorted(merged_dict.keys())
            
            # Count added and deduped
            original_total = len(hist_rows) + len(stage_rows)
            final_total = len(sorted_keys)
            rows_added = final_total - len(hist_rows)
            rows_deduped = original_total - final_total
            
            total_added += rows_added
            total_deduped += rows_deduped
            
            # Write to temp file
            with open(temp_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(EXPECTED_HEADER)
                for k in sorted_keys:
                    writer.writerow(merged_dict[k])
                    
            # Validate merged file
            val_success, val_count = validate_merged_data(temp_path)
            if not val_success:
                print(f"  [ERROR] Merged validation failed for {symbol}: {val_count}")
                # clean up temp and abort
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                cleanup_staging(staged_files.values())
                return "HOLD_FIRESIGNAL_UPDATE_PATH_AMBIGUOUS", f"Merged file validation failed for {symbol}: {val_count}", result_manifest
                
            # Rename temp to hist_path (safe swap)
            shutil.move(temp_path, hist_path)
            merged_files.append(hist_path)
            
        except Exception as e:
            print(f"  [ERROR] Failed to merge {symbol}: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            cleanup_staging(staged_files.values())
            return "HOLD_FIRESIGNAL_UPDATE_PATH_AMBIGUOUS", f"Failed to merge {symbol}: {e}", result_manifest
            
    print(f"\n[MERGE SUCCESS] Added {total_added} rows, deduped {total_deduped} rows.")
    
    # Rebuild viewer
    print("\n[VIEWER] Rebuilding FireSignal evidence viewer...")
    rebuild_success = trigger_viewer_rebuild()
    if not rebuild_success:
        print("[ERROR] Viewer rebuild failed.")
        return "HOLD_FIRESIGNAL_UPDATE_PATH_AMBIGUOUS", "Data merged successfully, but viewer rebuild failed.", result_manifest
        
    # Clean up staging directory
    cleanup_staging(staged_files.values())
    
    # Save State
    new_state = {
        "last_successful_update_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "last_successful_5m_close_utc": datetime.fromtimestamp(latest_completed_close_ms/1000, tz=timezone.utc).isoformat().replace("+00:00", "Z"),
        "symbols_updated": symbols,
        "files_written": len(merged_files),
        "rows_added": total_added,
        "rows_deduped": total_deduped,
        "latest_manifest_path": str(MANIFEST_DIR / "firesignal_latest_update_manifest.json"),
        "latest_viewer_path": str(ACTIVE_VIEWER_PATH),
        "status": "SUCCESS",
        "updated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }
    
    save_state(new_state)
    
    # Update result manifest for returning to caller
    result_manifest.update(new_state)
    
    return "PASS_FIRESIGNAL_UPDATED_FROM_LAST_KNOWN_AND_VIEWER_REFRESHED", "Update cycle completed successfully.", result_manifest

def cleanup_staging(file_paths):
    for fp in file_paths:
        if os.path.exists(fp):
            try:
                os.remove(fp)
            except:
                pass

def trigger_viewer_rebuild():
    """
    Subprocesses build_top100_evidence_viewer.py to refresh index.html
    """
    script_path = "scripts/visualization/build_top100_evidence_viewer.py"
    if not os.path.exists(script_path):
        print(f"  [ERROR] Viewer builder script not found: {script_path}")
        return False
        
    try:
        res = subprocess.run([sys.executable, script_path], capture_output=True, text=True, check=False)
        if res.returncode == 0:
            print("  [VIEWER] Rebuild completed successfully.")
            return True
        else:
            print(f"  [VIEWER ERROR] Builder script returned code {res.returncode}")
            print("  Stdout:", res.stdout)
            print("  Stderr:", res.stderr)
            return False
    except Exception as e:
        print(f"  [VIEWER ERROR] Failed to run build script: {e}")
        return False
