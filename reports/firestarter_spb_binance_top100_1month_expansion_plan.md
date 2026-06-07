# Firestarter SPB Binance Top 100 One-Month Expansion Plan

## Objective
Outline a safe, reproducible data acquisition strategy to expand the Firestarter SPB sandbox from 5 symbols to the Top 100 Binance USDT Perpetual contracts for a full 1-month profiling window, exclusively using free, public Binance API endpoints.

## 1. Symbol-Selection Method
- **Endpoint:** `fapi/v1/ticker/24hr`
- **Logic:** We will dynamically query the 24hr ticker statistics for all futures contracts.
- **Filters:** 
  1. Symbol must end in `USDT`.
  2. Contract must be currently trading/active (status = `TRADING`).
  3. Exclude delivery contracts, leveraged tokens (e.g., UP/DOWN), or quarterlies.
- **Sorting:** Sort the filtered list by `quoteVolume` (Notional Volume) descending.
- **Selection:** Slice the top 100 symbols from this sorted list to guarantee we are researching highly liquid, actively traded assets.

## 2. Expected File Count
- **Structure:** 1 master CSV file per symbol containing the merged time-series data, plus 1 global manifest file.
- **Count:** 100 symbol CSV files + 1 JSON manifest file = **101 files**.

## 3. Expected Row Count
For a 1-month (30-day) window per symbol:
- 1H Candles: ~720 rows
- 4H Candles: ~180 rows
- Funding Rate (8H): ~90 rows
- Open Interest / Ratios (assuming 1H/daily where retained): ~720 rows
- **Total Expected Rows per Symbol:** ~720 aligned hourly rows.
- **Total Dataset:** ~72,000 to 100,000 rows across all 100 CSVs.

## 4. Storage Estimate
- **Raw Size:** ~10 MB to 20 MB uncompressed text (CSV format).
- **Scale:** Extremely lightweight.

## 5. Rate-Limit Handling
- **Binance Limits:** Free tier allows 2,400 request weight per minute.
- **Strategy:** The script will respect HTTP `429` (Too Many Requests) headers and track `X-MBX-USED-WEIGHT-1M`. A hardcoded `time.sleep(0.5)` will be injected between symbol iterations to ensure we easily float below the ceiling.

## 6. Retry / Fail-Closed Rules
- **Network Timeouts:** Max 3 retries with exponential backoff (e.g., 2s, 4s, 8s).
- **Fail-Closed:** If an endpoint repeatedly fails after 3 retries (or returns a `400`/`403`), the script will log the failure, skip the symbol entirely, and proceed to the next symbol. The missing symbol will be registered in the manifest as `FAILED`.

## 7. Field Availability Policy
- **OHLCV:** Strict preservation. Pagination loop using `startTime` and `endTime`.
- **Derivatives Metrics:** Historical OI and Top-Trader ratios will be queried strictly within Binance's free-tier rolling retention limits (often limited to 30 days via API). 

## 8. Missing-Data Handling
- **No Imputation:** If a field (like OI history) is older than Binance's free-tier retention limit, it will be saved as empty (or `NaN`). 
- **No Backfill:** We will absolutely **not** artificially backfill, forward-fill, or impute missing historical derivative metrics.

## 9. Manifest & Audit Format
- A `manifest.json` will be generated containing:
  - `run_timestamp_utc`
  - `start_window` / `end_window`
  - `symbols_requested`
  - `symbols_succeeded`
  - `symbols_failed` (with error reasons)
  - `total_rows_downloaded`

## 10. ODIN Feasibility
- **Feasibility:** ✅ **High / Trivial.** 
- ODIN can trivially load a 20 MB dataset into memory via Pandas. There are no size, decompression, or hardware limitations for a 1-month, 100-symbol daily/hourly CSV dataset.

## 11. Pass/Hold Gate
We are currently holding at the expansion plan review phase. 
To proceed to the extraction script development and data pull, the user must explicitly approve the plan.

**PASS: PASS_SPB_BINANCE_TOP100_1MONTH_EXPANSION_PLAN_READY**
