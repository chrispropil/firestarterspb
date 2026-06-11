import os
import csv
import time

EXPECTED_HEADERS = {
    "fundingRate": ["symbol", "fundingTime", "fundingRate"],
    "openInterestHist": ["symbol", "sumOpenInterest", "sumOpenInterestValue", "timestamp"],
    "takerlongshortRatio": ["symbol", "buySellRatio", "sellVol", "buyVol", "timestamp"],
    "globalLongShortAccountRatio": ["symbol", "longShortRatio", "longAccount", "shortAccount", "timestamp"]
}

TIME_KEY_INDICES = {
    "fundingRate": 1,
    "openInterestHist": 3,
    "takerlongshortRatio": 4,
    "globalLongShortAccountRatio": 4
}


def validate_staging_deriv_file(filepath, metric_name, last_known_ts_ms=None):
    if not os.path.exists(filepath):
        return False, "Staging file does not exist"
        
    expected_header = EXPECTED_HEADERS.get(metric_name)
    if not expected_header:
        return False, f"Unknown metric name: {metric_name}"
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if not header:
                return False, "File is empty"
                
            if header != expected_header:
                return False, f"Header mismatch. Expected {expected_header}, got {header}"
                
            rows = list(reader)
            if not rows:
                return True, {"row_count": 0, "first_ts": None, "last_ts": None}
                
            time_key_idx = TIME_KEY_INDICES.get(metric_name, 3)
            now_ms = int(time.time() * 1000)
            prev_ts = None
            
            for idx, r in enumerate(rows):
                if len(r) != len(expected_header):
                    return False, f"Row {idx} has invalid column count: {len(r)}"
                    
                try:
                    ts = int(float(r[time_key_idx]))
                except ValueError:
                    return False, f"Row {idx} has unparseable timestamp: {r[time_key_idx]}"
                    
                if ts > now_ms:
                    return False, f"Row {idx} has a future timestamp: {ts} > now {now_ms}"
                    
                if prev_ts is not None and ts <= prev_ts:
                    return False, f"Row {idx} violates monotonicity: ts={ts} <= prev={prev_ts}"
                    
                if last_known_ts_ms is not None and ts <= last_known_ts_ms:
                    return False, f"Row {idx} overlaps with historical data: ts={ts} <= last_known={last_known_ts_ms}"
                    
                prev_ts = ts
                
            first_ts = int(float(rows[0][time_key_idx]))
            last_ts = int(float(rows[-1][time_key_idx]))
            
            return True, {
                "row_count": len(rows),
                "first_ts": first_ts,
                "last_ts": last_ts
            }
    except Exception as e:
        return False, f"Unexpected parsing error: {e}"

def validate_merged_deriv_data(filepath, metric_name):
    if not os.path.exists(filepath):
        return False, "Merged file does not exist"
        
    expected_header = EXPECTED_HEADERS.get(metric_name)
    if not expected_header:
        return False, f"Unknown metric name: {metric_name}"
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header != expected_header:
                return False, f"Header mismatch in merged file: {header}"
                
            time_key_idx = TIME_KEY_INDICES.get(metric_name, 3)
            prev_ts = None
            now_ms = int(time.time() * 1000)
            seen_ts = set()
            
            for idx, r in enumerate(reader):
                ts = int(float(r[time_key_idx]))
                
                if ts > now_ms:
                    return False, f"Merged row {idx} has a future timestamp: {ts} > now {now_ms}"
                    
                if ts in seen_ts:
                    return False, f"Merged row {idx} has a duplicate timestamp: {ts}"
                    
                if prev_ts is not None and ts <= prev_ts:
                    return False, f"Merged row {idx} violates monotonicity: ts={ts} <= prev={prev_ts}"
                    
                prev_ts = ts
                seen_ts.add(ts)
                
        return True, len(seen_ts)
    except Exception as e:
        return False, f"Unexpected error during merged validation: {e}"
