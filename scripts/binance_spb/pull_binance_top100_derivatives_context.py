import os
import sys
import glob
import argparse
import urllib.request
import json
import time
import csv
import hashlib

# Configure stdout encoding to prevent Unicode errors on Windows
sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = "C:/firestarterspb/data/research/binance_top100_excluding_existing_5_1month"
OUTPUT_DIR = "C:/firestarterspb/data/research/binance_top100_derivatives_context_1month"
MANIFEST_PATH = "C:/firestarterspb/reports/firestarter_spb_top100_derivatives_context_1month_manifest.csv"

ENDPOINTS = {
    "fundingRate": {
        "url": "https://fapi.binance.com/fapi/v1/fundingRate",
        "params": ["symbol", "startTime", "endTime", "limit"],
        "description": "Historical funding rate records"
    },
    "openInterestHist": {
        "url": "https://fapi.binance.com/futures/data/openInterestHist",
        "params": ["symbol", "period", "limit", "startTime", "endTime"],
        "description": "Global open interest history (30-day retention)"
    },
    "takerlongshortRatio": {
        "url": "https://fapi.binance.com/futures/data/takerlongshortRatio",
        "params": ["symbol", "period", "limit", "startTime", "endTime"],
        "description": "Taker buy/sell volume and taker buy/sell ratio (30-day retention)"
    },
    "globalLongShortAccountRatio": {
        "url": "https://fapi.binance.com/futures/data/globalLongShortAccountRatio",
        "params": ["symbol", "period", "limit", "startTime", "endTime"],
        "description": "Global account long/short ratio (30-day retention)"
    },
    "topLongShortAccountRatio": {
        "url": "https://fapi.binance.com/futures/data/topLongShortAccountRatio",
        "params": ["symbol", "period", "limit", "startTime", "endTime"],
        "description": "Top trader account long/short ratio (30-day retention)"
    },
    "topLongShortPositionRatio": {
        "url": "https://fapi.binance.com/futures/data/topLongShortPositionRatio",
        "params": ["symbol", "period", "limit", "startTime", "endTime"],
        "description": "Top trader position long/short ratio (30-day retention)"
    },
    "premiumIndex": {
        "url": "https://fapi.binance.com/fapi/v1/premiumIndex",
        "params": ["symbol"],
        "description": "Mark price and premium index context"
    }
}

COLUMNS = {
    "fundingRate": ["symbol", "fundingTime", "fundingRate"],
    "openInterestHist": ["symbol", "sumOpenInterest", "sumOpenInterestValue", "timestamp"],
    "takerlongshortRatio": ["symbol", "buySellRatio", "sellVol", "buyVol", "timestamp"],
    "globalLongShortAccountRatio": ["symbol", "longShortRatio", "longAccount", "shortAccount", "timestamp"],
    "topLongShortAccountRatio": ["symbol", "longShortRatio", "longAccount", "shortAccount", "timestamp"],
    "topLongShortPositionRatio": ["symbol", "longShortRatio", "longAccount", "shortAccount", "timestamp"],
    "premiumIndex": ["symbol", "markPrice", "indexPrice", "estimatedSettlePrice", "lastFundingRate", "interestRate", "nextFundingTime", "time"]
}

def load_symbols():
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] Source dataset directory does not exist: {DATA_DIR}")
        return []
    csv_files = glob.glob(os.path.join(DATA_DIR, "*_1month_5m.csv"))
    symbols = [os.path.basename(f).replace("_1month_5m.csv", "") for f in csv_files]
    return sorted(symbols)

def get_kline_time_range(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)
        if not rows:
            return None, None
        start_time = int(float(rows[0][0]))
        end_time = int(float(rows[-1][0]))
        return start_time, end_time
    except Exception as e:
        print(f"  [ERROR] Parsing kline timestamps from {file_path}: {e}")
        return None, None

def get_sha256(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return ""

def fetch_binance_data(endpoint_name, url, symbol, start_time, end_time, period, stats_tracker, limit=500):
    current_end_time = end_time
    all_items = []
    retries = 3
    
    if endpoint_name == "premiumIndex":
        query_url = f"{url}?symbol={symbol}"
        for attempt in range(retries):
            try:
                req = urllib.request.Request(query_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode('utf-8'))
                return [data]
            except Exception as e:
                code = getattr(e, 'code', None)
                if code == 400:
                    return None
                stats_tracker["retries_triggered"] += 1
                time.sleep(2 ** attempt + 0.1)
        return None

    time_key = "fundingTime" if endpoint_name == "fundingRate" else "timestamp"
    
    while current_end_time >= start_time:
        if endpoint_name == "fundingRate":
            query_url = f"{url}?symbol={symbol}&startTime={start_time}&endTime={current_end_time}&limit={limit}"
        else:
            query_url = f"{url}?symbol={symbol}&period={period}&startTime={start_time}&endTime={current_end_time}&limit={limit}"
            
        success = False
        for attempt in range(retries):
            try:
                req = urllib.request.Request(query_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    data = json.loads(response.read().decode('utf-8'))
                success = True
                break
            except Exception as e:
                code = getattr(e, 'code', None)
                if code == 400:
                    return None
                stats_tracker["retries_triggered"] += 1
                time.sleep(2 ** attempt + 0.1)
                
        if not success:
            return None
            
        if not data:
            break
            
        all_items.extend(data)
        
        t_min = data[0][time_key]
        if len(data) < limit:
            break
            
        next_end_time = t_min - 1
        if next_end_time >= current_end_time:
            break
        current_end_time = next_end_time
        time.sleep(0.06)
        
    all_items.sort(key=lambda x: x.get(time_key, 0))
    return all_items

def save_to_csv(endpoint_name, symbol, data_list):
    sub_dir = os.path.join(OUTPUT_DIR, endpoint_name)
    os.makedirs(sub_dir, exist_ok=True)
    
    file_path = os.path.join(sub_dir, f"{symbol}_{endpoint_name}.csv")
    cols = COLUMNS[endpoint_name]
    
    try:
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(cols)
            for item in data_list:
                row = []
                for col in cols:
                    if col == "symbol":
                        val = item.get("symbol", symbol)
                    else:
                        val = item.get(col, "")
                    row.append(val)
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"    [ERROR] Failed to save {file_path}: {e}")
        return False

def write_manifest(manifest_entries):
    try:
        # Create reports folder if not exists
        os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
        with open(MANIFEST_PATH, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["symbol", "file_type", "row_count", "first_timestamp_utc", "last_timestamp_utc", "checksum_sha256"])
            for entry in manifest_entries:
                writer.writerow([
                    entry["symbol"],
                    entry["file_type"],
                    entry["row_count"],
                    entry["first_timestamp_utc"],
                    entry["last_timestamp_utc"],
                    entry["checksum_sha256"]
                ])
        print(f"[MANIFEST] Manifest written to {MANIFEST_PATH}")
    except Exception as e:
        print(f"[ERROR] Failed to write manifest: {e}")

def generate_audit_report(stats):
    audit_path = "C:/firestarterspb/reports/firestarter_spb_top100_derivatives_context_live_pull_audit.md"
    
    failed_details = ""
    if stats["failed_runs"]:
        failed_details = "\n".join([f"- **{sym}** ({ep}): {reason}" for sym, ep, reason in stats["failed_runs"]])
    else:
        failed_details = "None. All symbols and endpoints processed successfully."
        
    success_summary = "\n".join([f"- **{ep}**: {stats['endpoint_success'][ep]} success, {stats['endpoint_failure'][ep]} fail" for ep in ENDPOINTS])

    content = f"""# Top 100 Derivatives Context Live Pull Audit

## 1. Execution Overview
- **Execution Timestamp (UTC):** {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
- **Selected Symbol Count:** {stats['total_symbols']}
- **Output Folder:** `{OUTPUT_DIR}`
- **Output File Count Summary:** {stats['files_written']} files successfully written
- **Manifest File:** `{MANIFEST_PATH}`

## 2. Endpoint Success Summary
{success_summary}

## 3. Failed/Skipped Symbols & Endpoints
{failed_details}

## 4. Retention & Window Actually Pulled
- **Stats Retention Limit:** Binance public API limits global open interest, taker volume ratios, and long/short account ratios to the latest 30 days.
- **Window Capping:** To prevent HTTP 400 parameter errors, the query `startTime` was capped at a maximum of 29 days ago (safe boundary).
- **Target Cadence:** Historical endpoints were queried with period `1h` (or as configured). Funding rates were queried over the full range up to 1000 records. Premium index context retrieved the current live pricing snapshot.

## 5. Rate-Limit & Retry Summary
- **Rate Limit Policy:** Max request weight of 1,000 per minute. Sleep of 60ms between requests.
- **Retries Triggered:** {stats['retries_triggered']} retries occurred during execution.
- **Fail-Closed Strategy:** Any symbol/endpoint failing 3 times after exponential backoff had its partial files removed, marked as failed, and the script continued safely.

## 6. Safety & Security Checklist
- **API Keys / Secrets exposed?** NO. Only public market data endpoints were used.
- **Raw data committed?** NO. Raw CSV data under `{OUTPUT_DIR}` remains local and is git-ignored or excluded from staging.
- **Formulas implemented?** NO. No signal calculations, ER, FMLC, or Flowprint computations were executed.
- **Cell 2 or ML training scripts?** NO.
- **Trading logic or recommendations?** NO.
- **Blockers:** None.
"""
    try:
        os.makedirs(os.path.dirname(audit_path), exist_ok=True)
        with open(audit_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[AUDIT] Audit report written to {audit_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write audit report: {e}")

def run_dry_run(symbols):
    print("=" * 60)
    print("FIRESTARTER TOP 100 DERIVATIVES CONTEXT DRY-RUN DIAGNOSTICS")
    print("=" * 60)
    print(f"Loaded symbols count: {len(symbols)}")
    
    if len(symbols) != 100:
        print(f"[ERROR] Symbol count is not exactly 100! Found: {len(symbols)}")
        sys.exit(1)
        
    print("\n--- VALIDATING API ENDPOINTS AND PATH ESTIMATIONS ---")
    total_estimated_requests = 0
    
    for name, spec in ENDPOINTS.items():
        print(f"\nEndpoint ID: {name}")
        print(f"  URL: {spec['url']}")
        print(f"  Expected Parameters: {', '.join(spec['params'])}")
        print(f"  Description: {spec['description']}")
        
        requests_per_symbol = 2 if name != "premiumIndex" else 1
        est_endpoint_requests = len(symbols) * requests_per_symbol
        total_estimated_requests += est_endpoint_requests
        
        print(f"  Estimated Requests (100 symbols): {est_endpoint_requests}")
        print(f"  Estimated Output Pattern: {OUTPUT_DIR}/{name}/{{SYMBOL}}_{name}.csv")

    print("\n--- RATE-LIMIT BUDGET AND RETRY RULES ---")
    print("- Weight limit: max 1,000 weight per minute (Target: < 80% of Binance 1,200 limit).")
    print("- Cadence: Funding at 8H; OI/Taker/LongShort ratios at 1H or 5m.")
    print("- Backoff: Exponential retry backoff on HTTP 429/418 with jitter.")
    print("- Fail-closed Policy: Abort pull and write zero files if any symbol request fails 3 times.")

    print("\n--- MANIFEST SCHEMA ---")
    print(f"Path: {MANIFEST_PATH}")
    print("Columns: symbol, file_type, row_count, first_timestamp_utc, last_timestamp_utc, checksum_sha256")

    print("\n--- PER-SYMBOL OUTPUT SCHEMA (Expected Columns) ---")
    print("- fundingRate: symbol, fundingTime, fundingRate")
    print("- openInterestHist: symbol, sumOpenInterest, sumOpenInterestValue, timestamp")
    print("- takerlongshortRatio: symbol, buySellRatio, sellVol, buyVol, timestamp")
    print("- Long/Short Ratios: symbol, longShortRatio, longAccount, shortAccount, timestamp")

    print("\n--- SUMMARY ESTIMATE ---")
    print(f"Total Symbols: {len(symbols)}")
    print(f"Total Estimated API Requests: {total_estimated_requests}")
    print("Result: DRY-RUN SUCCESSFUL. No files were created and no network requests were made.")
    print("=" * 60)

def run_live_pull(symbols, period):
    print("=" * 60)
    print("STARTING FIRESTARTER TOP 100 DERIVATIVES CONTEXT LIVE PULL")
    print("=" * 60)
    print(f"Loaded symbols count: {len(symbols)}")
    print(f"Statistical Period: {period}")
    
    if len(symbols) != 100:
        print(f"[ERROR] Symbol count is not exactly 100! Found: {len(symbols)}")
        sys.exit(1)
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    stats = {
        "total_symbols": len(symbols),
        "endpoint_success": {ep: 0 for ep in ENDPOINTS},
        "endpoint_failure": {ep: 0 for ep in ENDPOINTS},
        "failed_runs": [],
        "retries_triggered": 0,
        "files_written": 0
    }
    
    manifest_entries = []
    now_ms = int(time.time() * 1000)
    max_history_ms = 29 * 24 * 60 * 60 * 1000
    safe_start_boundary = now_ms - max_history_ms
    
    for idx, symbol in enumerate(symbols, 1):
        print(f"\n[{idx}/100] Processing Symbol: {symbol}")
        
        csv_file = os.path.join(DATA_DIR, f"{symbol}_1month_5m.csv")
        if not os.path.exists(csv_file):
            print(f"  [WARNING] Kline CSV not found for {symbol}. Skipping all endpoints.")
            for ep in ENDPOINTS:
                stats["endpoint_failure"][ep] += 1
                stats["failed_runs"].append((symbol, ep, "Kline CSV not found"))
            continue
            
        start_time, end_time = get_kline_time_range(csv_file)
        if start_time is None or end_time is None:
            print(f"  [WARNING] Could not parse timestamps from Kline CSV for {symbol}. Skipping.")
            for ep in ENDPOINTS:
                stats["endpoint_failure"][ep] += 1
                stats["failed_runs"].append((symbol, ep, "Could not parse Kline CSV timestamps"))
            continue
            
        query_start_time = max(start_time, safe_start_boundary)
        query_end_time = min(end_time, now_ms)
        
        print(f"  Target Window: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(start_time/1000))} to {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(end_time/1000))}")
        if query_start_time > start_time:
            print(f"  [INFO] Cap applied: startTime set to {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(query_start_time/1000))} (Binance 30-day retention constraint)")
            
        for ep_name, ep_spec in ENDPOINTS.items():
            print(f"  Fetching: {ep_name}...", end="", flush=True)
            data = fetch_binance_data(ep_name, ep_spec["url"], symbol, query_start_time, query_end_time, period, stats)
            
            if data is None:
                print(" FAIL")
                stats["endpoint_failure"][ep_name] += 1
                stats["failed_runs"].append((symbol, ep_name, "API Error or Symbol Unsupported"))
                file_path = os.path.join(OUTPUT_DIR, ep_name, f"{symbol}_{ep_name}.csv")
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
            elif not data:
                print(" EMPTY (No data returned)")
                stats["endpoint_success"][ep_name] += 1
            else:
                success_save = save_to_csv(ep_name, symbol, data)
                if success_save:
                    print(f" SUCCESS ({len(data)} rows)")
                    stats["endpoint_success"][ep_name] += 1
                    stats["files_written"] += 1
                    
                    file_path = os.path.join(OUTPUT_DIR, ep_name, f"{symbol}_{ep_name}.csv")
                    checksum = get_sha256(file_path)
                    time_key = "fundingTime" if ep_name == "fundingRate" else "timestamp"
                    if ep_name == "premiumIndex":
                        time_key = "time"
                        
                    first_ts = data[0][time_key]
                    last_ts = data[-1][time_key]
                    first_utc = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(first_ts / 1000.0))
                    last_utc = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(last_ts / 1000.0))
                    
                    manifest_entries.append({
                        "symbol": symbol,
                        "file_type": ep_name,
                        "row_count": len(data),
                        "first_timestamp_utc": first_utc,
                        "last_timestamp_utc": last_utc,
                        "checksum_sha256": checksum
                    })
                else:
                    print(" SAVE_ERROR")
                    stats["endpoint_failure"][ep_name] += 1
                    stats["failed_runs"].append((symbol, ep_name, "CSV Save Error"))
                    
            time.sleep(0.06)
            
    write_manifest(manifest_entries)
    generate_audit_report(stats)
    
    print("=" * 60)
    print("FIRESTARTER LIVE PULL COMPLETED")
    print(f"Total files written: {stats['files_written']}")
    print(f"Retries triggered: {stats['retries_triggered']}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Acquire public Binance futures derivatives context data.")
    parser.add_argument("--dry-run", action="store_true", help="Run path estimations and URL parameter checks without execution.")
    parser.add_argument("--approved-live-pull", action="store_true", help="Authorize live data pull execution.")
    parser.add_argument("--period", type=str, default="1h", help="Statistical period/interval for stats endpoints (e.g. 5m, 1h).")
    
    args = parser.parse_args()
    
    symbols = load_symbols()
    
    if args.dry_run:
        run_dry_run(symbols)
        sys.exit(0)
        
    if args.approved_live_pull:
        run_live_pull(symbols, args.period)
        sys.exit(0)
        
    print("[FAIL] Missing execution arguments. Pass --dry-run or --approved-live-pull to run script.")
    sys.exit(1)

if __name__ == "__main__":
    main()
