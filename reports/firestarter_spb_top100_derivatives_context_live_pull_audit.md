# Top 100 Derivatives Context Live Pull Audit

## 1. Execution Overview
- **Execution Timestamp (UTC):** 2026-06-07T21:16:27Z
- **Selected Symbol Count:** 100
- **Output Folder:** `C:/firestarterspb/data/research/binance_top100_derivatives_context_1month`
- **Output File Count Summary:** 686 files successfully written
- **Manifest File:** `C:/firestarterspb/reports/firestarter_spb_top100_derivatives_context_1month_manifest.csv`

## 2. Endpoint Success Summary
- **fundingRate**: 98 success, 2 fail
- **openInterestHist**: 98 success, 2 fail
- **takerlongshortRatio**: 98 success, 2 fail
- **globalLongShortAccountRatio**: 98 success, 2 fail
- **topLongShortAccountRatio**: 98 success, 2 fail
- **topLongShortPositionRatio**: 98 success, 2 fail
- **premiumIndex**: 98 success, 2 fail

## 3. Failed/Skipped Symbols & Endpoints
- **币安人生USDT** (fundingRate): API Error or Symbol Unsupported
- **币安人生USDT** (openInterestHist): API Error or Symbol Unsupported
- **币安人生USDT** (takerlongshortRatio): API Error or Symbol Unsupported
- **币安人生USDT** (globalLongShortAccountRatio): API Error or Symbol Unsupported
- **币安人生USDT** (topLongShortAccountRatio): API Error or Symbol Unsupported
- **币安人生USDT** (topLongShortPositionRatio): API Error or Symbol Unsupported
- **币安人生USDT** (premiumIndex): API Error or Symbol Unsupported
- **龙虾USDT** (fundingRate): API Error or Symbol Unsupported
- **龙虾USDT** (openInterestHist): API Error or Symbol Unsupported
- **龙虾USDT** (takerlongshortRatio): API Error or Symbol Unsupported
- **龙虾USDT** (globalLongShortAccountRatio): API Error or Symbol Unsupported
- **龙虾USDT** (topLongShortAccountRatio): API Error or Symbol Unsupported
- **龙虾USDT** (topLongShortPositionRatio): API Error or Symbol Unsupported
- **龙虾USDT** (premiumIndex): API Error or Symbol Unsupported

## 4. Retention & Window Actually Pulled
- **Stats Retention Limit:** Binance public API limits global open interest, taker volume ratios, and long/short account ratios to the latest 30 days.
- **Window Capping:** To prevent HTTP 400 parameter errors, the query `startTime` was capped at a maximum of 29 days ago (safe boundary).
- **Target Cadence:** Historical endpoints were queried with period `1h` (or as configured). Funding rates were queried over the full range up to 1000 records. Premium index context retrieved the current live pricing snapshot.

## 5. Rate-Limit & Retry Summary
- **Rate Limit Policy:** Max request weight of 1,000 per minute. Sleep of 60ms between requests.
- **Retries Triggered:** 42 retries occurred during execution.
- **Fail-Closed Strategy:** Any symbol/endpoint failing 3 times after exponential backoff had its partial files removed, marked as failed, and the script continued safely.

## 6. Safety & Security Checklist
- **API Keys / Secrets exposed?** NO. Only public market data endpoints were used.
- **Raw data committed?** NO. Raw CSV data under `C:/firestarterspb/data/research/binance_top100_derivatives_context_1month` remains local and is git-ignored or excluded from staging.
- **Formulas implemented?** NO. No signal calculations, ER, FMLC, or Flowprint computations were executed.
- **Cell 2 or ML training scripts?** NO.
- **Trading logic or recommendations?** NO.
- **Blockers:** None.
