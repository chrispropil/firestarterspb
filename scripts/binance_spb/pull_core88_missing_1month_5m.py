import urllib.request
import urllib.parse
import urllib.error
import json
import argparse
import os
import sys
import time
import csv

sys.stdout.reconfigure(encoding="utf-8")

MISSING_SYMBOLS_PATH = "reports/firestarter_core88_missing_symbol_coverage.txt"
TARGET_DIR = "data/research/binance_core88_missing_1month"
MANIFEST_CSV = "reports/firestarter_core88_missing_1month_pull_manifest.csv"
AUDIT_REPORT = "reports/firestarter_core88_missing_1month_pull_audit.md"


def load_missing_symbols():
    if not os.path.exists(MISSING_SYMBOLS_PATH):
        raise FileNotFoundError(f"Missing symbols file not found: {MISSING_SYMBOLS_PATH}")

    with open(MISSING_SYMBOLS_PATH, "r", encoding="utf-8") as f:
        symbols = [line.strip() for line in f if line.strip()]

    # Preserve order while removing accidental duplicates.
    seen = set()
    deduped = []
    for sym in symbols:
        if sym not in seen:
            seen.add(sym)
            deduped.append(sym)

    return deduped


def fetch_active_usdt_perps():
    try:
        req = urllib.request.Request("https://fapi.binance.com/fapi/v1/exchangeInfo")
        with urllib.request.urlopen(req, timeout=30) as response:
            info = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"[ERROR] Failed to fetch exchangeInfo: {e}")
        return set()

    active = set()
    for symbol_info in info.get("symbols", []):
        if (
            symbol_info.get("status") == "TRADING"
            and symbol_info.get("contractType") == "PERPETUAL"
            and symbol_info.get("quoteAsset") == "USDT"
        ):
            active.add(symbol_info.get("symbol"))

    return active


def pull_1month_klines(symbol):
    end_time = int(time.time() * 1000)
    start_time = end_time - (30 * 24 * 60 * 60 * 1000)

    current_start = start_time
    all_klines = []

    while current_start < end_time:
        safe_symbol = urllib.parse.quote(symbol)
        url = (
            "https://fapi.binance.com/fapi/v1/klines"
            f"?symbol={safe_symbol}&interval=5m&limit=1500"
            f"&startTime={current_start}&endTime={end_time}"
        )

        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as response:
                klines = json.loads(response.read().decode("utf-8"))

            if not klines:
                break

            all_klines.extend(klines)
            current_start = klines[-1][0] + 1
            time.sleep(0.1)

        except urllib.error.URLError as e:
            print(f"[ERROR] Network/rate-limit issue on {symbol}: {e}")
            return False, 0, str(e)
        except Exception as e:
            print(f"[ERROR] Unexpected failure on {symbol}: {e}")
            return False, 0, str(e)

    if not all_klines:
        return False, 0, "no_klines_returned"

    os.makedirs(TARGET_DIR, exist_ok=True)
    filepath = os.path.join(TARGET_DIR, f"{symbol}_1month_5m.csv")

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        writer.writerows(all_klines)

    return True, len(all_klines), ""


def write_manifest(rows):
    os.makedirs(os.path.dirname(MANIFEST_CSV), exist_ok=True)

    with open(MANIFEST_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["symbol", "status", "rows", "output_file", "error"]
        )
        writer.writeheader()
        writer.writerows(rows)


def write_audit(symbols, active_symbols, manifest_rows, dry_run):
    success_count = sum(1 for r in manifest_rows if r["status"] == "success")
    skipped_count = sum(1 for r in manifest_rows if r["status"] == "skipped_inactive")
    failed_count = sum(1 for r in manifest_rows if r["status"] == "failed")
    total_rows = sum(int(r["rows"]) for r in manifest_rows if str(r["rows"]).isdigit())

    content = f"""# Firestarter Core88 Missing 1-Month 5m Pull Audit

## Status

| Check | Result |
|---|---|
| Mode | {"DRY_RUN" if dry_run else "LIVE_PULL"} |
| Missing Symbols Requested | {len(symbols)} |
| Active Binance USDT Perps Checked | {len(active_symbols)} |
| Successful Pulls | {success_count} |
| Skipped Inactive Symbols | {skipped_count} |
| Failed Pulls | {failed_count} |
| Total Rows Downloaded | {total_rows} |
| Raw Data Committed | NO |
| Formula Changes | NO |
| Cell 2 / Signal Labels | NO |
| Automation Daemon | NO |

## Output

- Data directory: `{TARGET_DIR}`
- Manifest CSV: `{MANIFEST_CSV}`

## Boundary

This puller only collects public Binance USDT perpetual 5m kline history for the missing Core88 coverage set. It does not alter formulas, scoring logic, labels, execution rules, or live systems.

## Verdict

{"PASS_DRY_RUN_CORE88_MISSING_PULL_READY" if dry_run else "PASS_CORE88_MISSING_1MONTH_5M_PULL_COMPLETE"}
"""

    with open(AUDIT_REPORT, "w", encoding="utf-8") as f:
        f.write(content)


def main(dry_run, approved_live_pull):
    print("======================================================")
    print(" MATRIX ALPHA // FIRESTARTER SPB")
    print(" Core88 Missing 1-Month 5m Binance Puller")
    print("======================================================")

    symbols = load_missing_symbols()
    active_symbols = fetch_active_usdt_perps()

    if not active_symbols:
        print("[ERROR] Could not resolve active Binance USDT perpetual symbols.")
        sys.exit(1)

    print(f"Missing Core88 symbols loaded: {len(symbols)}")
    print(f"Active Binance USDT perpetuals resolved: {len(active_symbols)}")

    manifest_rows = []

    for sym in symbols:
        if sym not in active_symbols:
            manifest_rows.append({
                "symbol": sym,
                "status": "skipped_inactive",
                "rows": 0,
                "output_file": "",
                "error": "symbol_not_active_usdt_perpetual"
            })

    selected = [sym for sym in symbols if sym in active_symbols]

    if dry_run:
        print("\n--- Dry Run Selection ---")
        for i, sym in enumerate(selected, 1):
            print(f"{i:02d}. {sym}")

        skipped = [r["symbol"] for r in manifest_rows if r["status"] == "skipped_inactive"]
        if skipped:
            print("\n--- Skipped Inactive / Unavailable Symbols ---")
            for sym in skipped:
                print(sym)

        print(f"\nProjected live pulls: {len(selected)}")
        print(f"Projected target directory: {TARGET_DIR}")
        write_manifest(manifest_rows)
        write_audit(symbols, active_symbols, manifest_rows, dry_run=True)
        print("\n[GATE] Dry-run complete. Run with --approved-live-pull to ingest.")
        return

    if not approved_live_pull:
        print("\n[ERROR] Live extraction is locked behind manual authorization.")
        print("Run with --approved-live-pull to execute.")
        sys.exit(1)

    os.makedirs(TARGET_DIR, exist_ok=True)

    print(f"\n[LIVE EXECUTION STARTED] Pulling {len(selected)} symbols...")
    for i, sym in enumerate(selected, 1):
        print(f"[{i}/{len(selected)}] Pulling {sym}...", end=" ")
        sys.stdout.flush()

        success, rows, error = pull_1month_klines(sym)
        output_file = os.path.join(TARGET_DIR, f"{sym}_1month_5m.csv") if success else ""

        manifest_rows.append({
            "symbol": sym,
            "status": "success" if success else "failed",
            "rows": rows,
            "output_file": output_file,
            "error": error
        })

        print(f"OK ({rows} rows)" if success else f"FAILED ({error})")

    write_manifest(manifest_rows)
    write_audit(symbols, active_symbols, manifest_rows, dry_run=False)

    success_count = sum(1 for r in manifest_rows if r["status"] == "success")
    failed_count = sum(1 for r in manifest_rows if r["status"] == "failed")
    skipped_count = sum(1 for r in manifest_rows if r["status"] == "skipped_inactive")
    total_rows = sum(int(r["rows"]) for r in manifest_rows if str(r["rows"]).isdigit())

    print(f"\n[DONE] {success_count} success, {failed_count} failed, {skipped_count} skipped. Total rows: {total_rows}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull missing Core88 1-month 5m Binance USDT perpetual klines.")
    parser.add_argument("--dry-run", action="store_true", help="Run strictly in dry-run mode.")
    parser.add_argument("--approved-live-pull", action="store_true", help="Authorize actual raw data ingestion to disk.")
    args = parser.parse_args()

    main(args.dry_run, args.approved_live_pull)
