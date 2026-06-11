import os
import json
import csv
from pathlib import Path
from datetime import datetime, timezone

STATE_PATH = Path("C:/firestarterspb/state/firesignal_update_state.json")
INVENTORY_PATH = Path("C:/firestarterspb/reports/firestarter_core88_pulled_symbols_inventory.md")
DATA_DIRS = [
    "C:/firestarterspb/data/research/binance_top100_excluding_existing_5_1month",
    "C:/firestarterspb/data/research/binance_core88_missing_1month"
]

def load_state():
    if not STATE_PATH.exists():
        return None
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load state from {STATE_PATH}: {e}")
        return None

def save_state(state):
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4, sort_keys=True)
        print(f"[STATE] State saved to {STATE_PATH}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to save state to {STATE_PATH}: {e}")
        return False

def load_symbols():
    symbols = []
    if not INVENTORY_PATH.exists():
        print(f"[ERROR] Inventory path not found: {INVENTORY_PATH}")
        return []
    with open(INVENTORY_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                symbols.append(line.replace("- ", "").strip())
    return sorted(symbols)

def find_symbol_files(symbols):
    file_map = {}
    for symbol in symbols:
        found = False
        for d in DATA_DIRS:
            path = Path(d) / f"{symbol}_1month_5m.csv"
            if path.exists():
                file_map[symbol] = str(path)
                found = True
                break
        if not found:
            print(f"[WARNING] File for symbol {symbol} not found in DATA_DIRS")
    return file_map

def infer_last_timestamp(file_map):
    last_timestamps_ms = []
    
    for symbol, filepath in file_map.items():
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if not header:
                    print(f"  [ERROR] {symbol} file is empty (no header)")
                    return None
                
                rows = list(reader)
                if not rows:
                    print(f"  [ERROR] {symbol} file has no data rows")
                    return None
                
                # Check column index for open_time
                if "open_time" not in header:
                    print(f"  [ERROR] {symbol} file lacks open_time header")
                    return None
                
                open_time_idx = header.index("open_time")
                last_row = rows[-1]
                last_ts_ms = int(float(last_row[open_time_idx]))
                last_timestamps_ms.append(last_ts_ms)
        except Exception as e:
            print(f"  [ERROR] Parsing last timestamp for {symbol}: {e}")
            return None
            
    if not last_timestamps_ms:
        return None
        
    # We take the minimum (lowest common denominator) to represent the last successfully unified update
    min_ts_ms = min(last_timestamps_ms)
    return min_ts_ms
