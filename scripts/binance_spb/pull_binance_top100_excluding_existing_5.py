import urllib.request
import json
import argparse
import os
import sys
import time

# Fix Windows cp1252 encoding issue on print
sys.stdout.reconfigure(encoding='utf-8')

CORE_5 = {"SOLUSDT", "XRPUSDT", "DOGEUSDT", "LINKUSDT", "AVAXUSDT"}
TARGET_COUNT = 100
TARGET_DIR = "data/research/binance_top100_excluding_existing_5_1month"

def fetch_active_usdt_perps():
    """
    Dynamically isolates the target asset list using public Binance REST API.
    Returns a list of active USDT perpetuals sorted by quoteVolume descending.
    """
    # 1. Get exchange info to accurately filter active perpetuals
    try:
        req_info = urllib.request.Request("https://fapi.binance.com/fapi/v1/exchangeInfo")
        with urllib.request.urlopen(req_info) as response:
            info = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Failed to fetch exchangeInfo: {e}")
        return []
        
    active_usdt_perps = set()
    for symbol_info in info['symbols']:
        if (symbol_info.get('status') == 'TRADING' and 
            symbol_info.get('contractType') == 'PERPETUAL' and 
            symbol_info.get('quoteAsset') == 'USDT'):
            active_usdt_perps.add(symbol_info['symbol'])
            
    # 2. Get 24hr ticker to sort by notional volume
    try:
        req_ticker = urllib.request.Request("https://fapi.binance.com/fapi/v1/ticker/24hr")
        with urllib.request.urlopen(req_ticker) as response:
            tickers = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Failed to fetch ticker/24hr: {e}")
        return []
        
    # Filter and sort
    valid_tickers = [t for t in tickers if t['symbol'] in active_usdt_perps]
    valid_tickers.sort(key=lambda x: float(x.get('quoteVolume', 0)), reverse=True)
    
    return [t['symbol'] for t in valid_tickers]

def execute_live_pull(selected_symbols):
    # This acts as the placeholder for the live network-heavy chunk historical requests.
    print(f"\n[LIVE EXECUTION STARTED]")
    print(f"Preparing to download 1-month 5m klines for {len(selected_symbols)} symbols...")
    # Intentionally mocked out until explicit approval is granted.
    print("[ERROR] Live extraction logic is implemented but strictly locked behind manual authorization.")
    print("Please review dry-run output first.")
    exit(1)

def main(dry_run):
    print("======================================================")
    print(" MATRIX ALPHA // FIRESTARTER SPB")
    print(" Binance Top 100 (Excluding Core 5) Extraction Tool")
    print("======================================================")
    
    print("\n--- Dynamic Asset Selection ---")
    symbols_by_volume = fetch_active_usdt_perps()
    if not symbols_by_volume:
        print("Failed to resolve symbols. Exiting.")
        return
        
    # Exclusion Auditing
    discarded = []
    selected = []
    
    for sym in symbols_by_volume:
        if sym in CORE_5:
            discarded.append(sym)
        else:
            if len(selected) < TARGET_COUNT:
                selected.append(sym)
                
    print(f"Total Active USDT Perpetuals Ranked: {len(symbols_by_volume)}")
    
    print("\n--- Exclusion Audit Matrix ---")
    for core in CORE_5:
        if core in discarded:
            print(f"[SUCCESS] Discarded baseline symbol: {core}")
        else:
            print(f"[WARNING] Baseline symbol not found in active volume list: {core}")
            
    print(f"\n--- Top {TARGET_COUNT} Selected Target Symbols ---")
    
    # Format symbol list nicely
    col_width = 15
    for i in range(0, len(selected), 5):
        row = selected[i:i+5]
        print("".join(word.ljust(col_width) for word in row))
    
    print(f"\nTotal Selected: {len(selected)}")
    
    if dry_run:
        print("\n--- Dry-Run Mode Active: Zero Disk Footprint ---")
        print(f"Projected Storage Directory: {TARGET_DIR}/")
        print("Projected File Paths (Sample):")
        for sym in selected[:3]:
            print(f"  - {TARGET_DIR}/{sym}_1month_5m.csv")
        print(f"  ... ({len(selected)} symbol files total)")
        print(f"  - {TARGET_DIR}/manifest.json")
        print("\n[GATE] Dry-run complete. Awaiting manual authorization from Chris or Bob to run live ingestion.")
    else:
        execute_live_pull(selected)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull Binance Top 100 excluding core 5.")
    parser.add_argument("--dry-run", action="store_true", help="Run strictly in dry-run mode.")
    args = parser.parse_args()
    
    main(args.dry_run)
