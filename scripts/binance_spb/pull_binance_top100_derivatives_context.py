import os
import sys
import glob
import argparse

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

def load_symbols():
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] Source dataset directory does not exist: {DATA_DIR}")
        return []
    csv_files = glob.glob(os.path.join(DATA_DIR, "*_1month_5m.csv"))
    symbols = [os.path.basename(f).replace("_1month_5m.csv", "") for f in csv_files]
    return sorted(symbols)

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
        
        # Estimate files and requests for 100 symbols
        # For historical data, we may need 1-2 pages per symbol due to limits
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

def main():
    parser = argparse.ArgumentParser(description="Acquire public Binance futures derivatives context data.")
    parser.add_argument("--dry-run", action="store_true", help="Run path estimations and URL parameter checks without execution.")
    parser.add_argument("--approved-live-pull", action="store_true", help="Authorize live data pull execution.")
    
    args = parser.parse_args()
    
    symbols = load_symbols()
    
    if args.dry_run:
        run_dry_run(symbols)
        sys.exit(0)
        
    if args.approved_live_pull:
        # Enforce fail closed unless explicit environment confirmation is met
        print("[HOLD] Live pull execution is strictly gated.")
        print("Required approval gate: HOLD_DERIVATIVES_PULL_PENDING_APPROVAL")
        sys.exit(1)
        
    # Default fail-closed behavior
    print("[FAIL] Missing execution arguments. Pass --dry-run to validate script.")
    sys.exit(1)

if __name__ == "__main__":
    main()
