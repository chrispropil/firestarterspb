# Core88 Missing Derivatives Context Live Pull Audit

## 1. Execution Overview
- **Execution Timestamp (UTC):** 2026-06-09T11:33:16Z
- **Selected Symbol Count:** 45
- **Output Folder:** `C:/firestarterspb/data/research/binance_core88_missing_derivatives_context_1month`
- **Output File Count Summary:** 315 files successfully written
- **Manifest File:** `C:/firestarterspb/reports/firestarter_core88_missing_derivatives_context_manifest.csv`

## 2. Endpoint Success Summary
- **fundingRate**: 45 success, 0 fail
- **openInterestHist**: 45 success, 0 fail
- **takerlongshortRatio**: 45 success, 0 fail
- **globalLongShortAccountRatio**: 45 success, 0 fail
- **topLongShortAccountRatio**: 45 success, 0 fail
- **topLongShortPositionRatio**: 45 success, 0 fail
- **premiumIndex**: 45 success, 0 fail

## 3. Failed/Skipped Symbols & Endpoints
None. All symbols and endpoints processed successfully.

## 4. Retention & Window Actually Pulled
- **Stats Retention Limit:** Binance public API limits global open interest, taker volume ratios, and long/short account ratios to the latest 30 days.
- **Window Capping:** To prevent HTTP 400 parameter errors, the query `startTime` was capped at a maximum of 29 days ago (safe boundary).
- **Target Cadence:** Historical endpoints were queried with period `1h` (or as configured). Funding rates were queried over the full range up to 1000 records. Premium index context retrieved the current live pricing snapshot.

## 5. Rate-Limit & Retry Summary
- **Rate Limit Policy:** Max request weight of 1,000 per minute. Sleep of 60ms between requests.
- **Retries Triggered:** 0 retries occurred during execution.
- **Fail-Closed Strategy:** Any symbol/endpoint failing 3 times after exponential backoff had its partial files removed, marked as failed, and the script continued safely.

## 6. Safety & Security Checklist
- **API Keys / Secrets exposed?** NO. Only public market data endpoints were used.
- **Raw data committed?** NO. Raw CSV data under `C:/firestarterspb/data/research/binance_core88_missing_derivatives_context_1month` remains local and is git-ignored or excluded from staging.
- **Formulas implemented?** NO. No signal calculations, ER, FMLC, or Flowprint computations were executed.
- **Cell 2 or ML training scripts?** NO.
- **Trading logic or recommendations?** NO.
- **Blockers:** None.
