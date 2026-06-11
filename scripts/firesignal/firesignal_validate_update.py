import os
import csv
from pathlib import Path
import time

EXPECTED_HEADER = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'trades', 'taker_buy_base', 'taker_buy_quote', 'ignore']

def validate_staging_file(filepath, last_known_ts_ms=None):
    """
    Validates a staged CSV file.
    Returns (success, reason_or_stats_dict)
    """
    if not os.path.exists(filepath):
        return False, "Staging file does not exist"
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                return False, "File is empty"
                
            if header != EXPECTED_HEADER:
                return False, f"Header mismatch. Expected {EXPECTED_HEADER}, got {header}"
                
            rows = list(reader)
            if not rows:
                # If there are truly no new intervals, it is valid to have an empty file, but we should handle it
                return True, {"row_count": 0, "first_ts": None, "last_ts": None}
                
            # Validate timestamps
            now_ms = int(time.time() * 1000)
            prev_ts = None
            
            for idx, r in enumerate(rows):
                if len(r) != len(EXPECTED_HEADER):
                    return False, f"Row {idx} has invalid column count: {len(r)}"
                    
                try:
                    open_time = int(float(r[0]))
                    close_time = int(float(r[6]))
                except ValueError:
                    return False, f"Row {idx} has unparseable timestamps: open_time={r[0]}, close_time={r[6]}"
                    
                # No future timestamps
                if open_time > now_ms:
                    return False, f"Row {idx} has a future timestamp: {open_time} > now {now_ms}"
                    
                # Monotonicity check in staging
                if prev_ts is not None and open_time <= prev_ts:
                    return False, f"Row {idx} violates monotonicity: open_time={open_time} <= prev={prev_ts}"
                    
                # Monotonicity check against existing last known timestamp
                if last_known_ts_ms is not None and open_time <= last_known_ts_ms:
                    return False, f"Row {idx} overlaps with historical data: open_time={open_time} <= last_known={last_known_ts_ms}"
                    
                prev_ts = open_time
                
            first_ts = int(float(rows[0][0]))
            last_ts = int(float(rows[-1][0]))
            
            return True, {
                "row_count": len(rows),
                "first_ts": first_ts,
                "last_ts": last_ts
            }
    except Exception as e:
        return False, f"Unexpected parsing error: {e}"

def validate_merged_data(filepath):
    """
    Validates the merged historical file.
    Checks monotonicity, duplicates, and future dates.
    """
    if not os.path.exists(filepath):
        return False, "Merged file does not exist"
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header != EXPECTED_HEADER:
                return False, f"Header mismatch in merged file: {header}"
                
            prev_ts = None
            now_ms = int(time.time() * 1000)
            seen_ts = set()
            
            for idx, r in enumerate(reader):
                open_time = int(float(r[0]))
                
                if open_time > now_ms:
                    return False, f"Merged row {idx} has a future timestamp: {open_time} > now {now_ms}"
                    
                if open_time in seen_ts:
                    return False, f"Merged row {idx} has a duplicate timestamp: {open_time}"
                    
                if prev_ts is not None and open_time <= prev_ts:
                    return False, f"Merged row {idx} violates monotonicity: open_time={open_time} <= prev={prev_ts}"
                    
                prev_ts = open_time
                seen_ts.add(open_time)
                
        return True, len(seen_ts)
    except Exception as e:
        return False, f"Unexpected error during merged validation: {e}"
