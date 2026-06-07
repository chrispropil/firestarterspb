import urllib.request
import json
import argparse
import os
import sys
import time
import csv

# Fix Windows cp1252 encoding issue on print
sys.stdout.reconfigure(encoding='utf-8')

CORE_5 = {"SOLUSDT", "XRPUSDT", "DOGEUSDT", "LINKUSDT", "AVAXUSDT"}
TARGET_COUNT = 100
TARGET_DIR = "data/research/binance_top100_excluding_existing_5_1month"

def fetch_active_usdt_perps():
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
            
    try:
        req_ticker = urllib.request.Request("https://fapi.binance.com/fapi/v1/ticker/24hr")
        with urllib.request.urlopen(req_ticker) as response:
            tickers = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Failed to fetch ticker/24hr: {e}")
        return []
        
    valid_tickers = [t for t in tickers if t['symbol'] in active_usdt_perps]
    valid_tickers.sort(key=lambda x: float(x.get('quoteVolume', 0)), reverse=True)
    
    return [t['symbol'] for t in valid_tickers]

def pull_1month_klines(symbol):
    end_time = int(time.time() * 1000)
    start_time = end_time - (30 * 24 * 60 * 60 * 1000)
    
    current_start = start_time
    all_klines = []
    
    # Binance limit is 1500 per request
    while current_start < end_time:
        safe_symbol = urllib.parse.quote(symbol)
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={safe_symbol}&interval=5m&limit=1500&startTime={current_start}&endTime={end_time}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                klines = json.loads(response.read().decode('utf-8'))
                
            if not klines:
                break
                
            all_klines.extend(klines)
            current_start = klines[-1][0] + 1
            
            # Rate limit protection
            time.sleep(0.1)
            
        except urllib.error.URLError as e:
            print(f"[ERROR] Rate limit or network error on {symbol}: {e}")
            return False, 0
            
    if not all_klines:
        return False, 0
        
    os.makedirs(TARGET_DIR, exist_ok=True)
    filepath = os.path.join(TARGET_DIR, f"{symbol}_1month_5m.csv")
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'])
        writer.writerows(all_klines)
        
    return True, len(all_klines)

def execute_live_pull(selected_symbols, discarded_symbols):
    print(f"\n[LIVE EXECUTION STARTED]")
    print(f"Downloading 1-month 5m klines for {len(selected_symbols)} symbols...")
    
    success_count = 0
    fail_count = 0
    total_rows = 0
    
    for i, sym in enumerate(selected_symbols):
        print(f"[{i+1}/{len(selected_symbols)}] Pulling {sym}...", end=" ")
        sys.stdout.flush()
        
        success, rows = pull_1month_klines(sym)
        if success:
            success_count += 1
            total_rows += rows
            print(f"OK ({rows} rows)")
        else:
            fail_count += 1
            print("FAILED")
            
    # Write manifest
    manifest = {
        "run_timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "symbols_requested": len(selected_symbols),
        "excluded_symbols_confirmed": discarded_symbols,
        "success_count": success_count,
        "failed_count": fail_count,
        "total_rows_downloaded": total_rows
    }
    with open(os.path.join(TARGET_DIR, "manifest.json"), 'w') as f:
        json.dump(manifest, f, indent=4)
        
    print(f"\n[DONE] {success_count} success, {fail_count} failed. Total rows: {total_rows}")

def main(dry_run, approved_live_pull):
    print("======================================================")
    print(" MATRIX ALPHA // FIRESTARTER SPB")
    print(" Binance Top 100 (Excluding Core 5) Extraction Tool")
    print("======================================================")
    
    print("\n--- Dynamic Asset Selection ---")
    symbols_by_volume = fetch_active_usdt_perps()
    if not symbols_by_volume:
        print("Failed to resolve symbols. Exiting.")
        return
        
    discarded = []
    selected = []
    
    for sym in symbols_by_volume:
        if sym in CORE_5:
            discarded.append(sym)
        else:
            if len(selected) < TARGET_COUNT:
                selected.append(sym)
                
    if dry_run:
        print(f"Total Active USDT Perpetuals Ranked: {len(symbols_by_volume)}")
        print("\n--- Exclusion Audit Matrix ---")
        for core in CORE_5:
            if core in discarded:
                print(f"[SUCCESS] Discarded baseline symbol: {core}")
            else:
                print(f"[WARNING] Baseline symbol not found in active volume list: {core}")
                
        print(f"\n--- Top {TARGET_COUNT} Selected Target Symbols ---")
        col_width = 15
        for i in range(0, len(selected), 5):
            row = selected[i:i+5]
            print("".join(word.ljust(col_width) for word in row))
        
        print(f"\nTotal Selected: {len(selected)}")
        print("\n--- Dry-Run Mode Active: Zero Disk Footprint ---")
        print(f"Projected Storage Directory: {TARGET_DIR}/")
        print("\n[GATE] Dry-run complete. Run with --approved-live-pull to ingest.")
        return

    if approved_live_pull:
        execute_live_pull(selected, discarded)
    else:
        print("\n[ERROR] Live extraction logic is implemented but strictly locked behind manual authorization.")
        print("Run with --approved-live-pull to execute.")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull Binance Top 100 excluding core 5.")
    parser.add_argument("--dry-run", action="store_true", help="Run strictly in dry-run mode.")
    parser.add_argument("--approved-live-pull", action="store_true", help="Authorize actual raw data ingestion to disk.")
    args = parser.parse_args()
    
    main(args.dry_run, args.approved_live_pull)
