# Firestarter SPB: Binance Top 100 (Excluding Core 5) Pull Audit

## Overview
This document audits the live execution of the dynamic asset ingestion pipeline targeting the top 100 Binance USDT-M perpetual contracts by volume, explicitly excluding the core 5 baselines.

## Execution Metrics
- **Selected Symbol Count:** 100
- **Excluded Symbol Check:** 
  - `[SUCCESS]` Discarded `SOLUSDT`
  - `[SUCCESS]` Discarded `XRPUSDT`
  - `[SUCCESS]` Discarded `DOGEUSDT`
  - `[SUCCESS]` Discarded `LINKUSDT`
  - `[SUCCESS]` Discarded `AVAXUSDT`
- **Success Count:** 100
- **Failed/Skipped Symbols:** 0
- **Total Rows Ingested:** 840,241

## Output Details
- **Output Folder:** `data/research/binance_top100_excluding_existing_5_1month/`
- **File Count Summary:** 101 files total (100 raw symbol CSVs + 1 `manifest.json`)
- **Endpoint Summary:**
  - `fapi/v1/exchangeInfo` (Filter active USDT-M)
  - `fapi/v1/ticker/24hr` (Rank by quoteVolume)
  - `fapi/v1/klines` (1-month chronological 5m paginated chunks)
- **Rate-Limit/Retry Summary:** 0.1s hard sleep delay injected per chunk. Max payload 1500 per chunk (weight=1). 0 HTTP 429/418 limits encountered. 

## Security & Boundary Verification
- **Raw Data Exclusion Confirmation:** Confirmed that `data/research/binance_top100_excluding_existing_5_1month/` is securely bound by `.gitignore`. No raw telemetry was staged or leaked into version control.
- **Blockers:** Encountered Windows console Unicode encode errors with foreign token tickers (e.g., `龙虾USDT`, `币安人生USDT`). Implemented safe URL-encoding patches (`urllib.parse.quote`) and stdout `utf-8` re-configuration. Operations proceeded successfully.
