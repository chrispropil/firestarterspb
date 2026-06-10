# Firestarter SPB Binance 5-Token 6-Month Expansion Plan

## Objective
Outline the exact data acquisition strategy to expand the Firestarter SPB sandbox from a 1-month to a 6-month historical dataset (2025-12-06 00:00 UTC to 2026-06-06 00:00 UTC) for five core tokens, preserving strict field-source integrity and avoiding look-ahead backfill.

## Target Symbols
- SOLUSDT
- XRPUSDT
- DOGEUSDT
- LINKUSDT
- AVAXUSDT

## Target Window
**Start:** `2025-12-06 00:00:00 UTC`
**End:** `2026-06-06 00:00:00 UTC`

## Data Requirements & Pagination Strategy

### 1. 1H & 4H Futures Candles (OHLCV)
- **Source Endpoint:** Binance `fapi/v1/klines`
- **Pagination Policy:** Retrieve full 6-month window using `startTime` and `endTime` loop pagination (Binance limit is 1500 rows per request, easily covering months of 1H/4H data).
- **Integrity Rule:** Use exact open, high, low, close, volume, and quote asset volume.

### 2. Funding-Rate History
- **Source Endpoint:** Binance `fapi/v1/fundingRate`
- **Pagination Policy:** Retrieve full 6-month window using iterative pagination. Funding occurs every 8 hours (or potentially 4h depending on token volatility phase).
- **Integrity Rule:** Log precise absolute funding rate per timestamp.

### 3. Open Interest (OI) Statistics & Snapshots
- **Source Endpoint (Current Snapshot):** Binance `fapi/v1/openInterest`
- **Source Endpoint (Historical):** Binance `futures/data/openInterestHist`
- **Pagination Policy:** Historical OI may be restricted by Binance's data retention policy (often limited to 30 days via API). 
- **Integrity Rule:** Only pull available recent window. **Do not** attempt to impute, backfill, or interpolate missing OI data for the remaining 5 months.

### 4. Top-Trader Ratios (Account & Position)
- **Source Endpoints:** 
  - `futures/data/topLongShortAccountRatio`
  - `futures/data/topLongShortPositionRatio`
- **Pagination Policy:** Similarly restricted by rolling retention windows.
- **Integrity Rule:** Mark older unavailable historical participation fields strictly as `missing/partial`.

## Governance Boundaries & Field Policies
- **No Data Imputation:** If historical open-interest or top-trader participation data falls outside the Binance API retention window, the fields will remain blank or flagged as `partial` in the dataset.
- **Immutable REST Snapshots:** All pulls must be executed strictly against REST API historical endpoints. No websocket streaming or third-party aggregated data will be used to fill gaps.
- **No Calculation:** This stage only covers data acquisition. No Cell 1 formula execution, Cell 2 labeling, or model training will occur.
- **Secret Isolation:** Do not log or commit API keys during the eventual extraction phase.

## Next Execution Steps
1. Approve this expansion plan.
2. Develop a Python extraction script to securely iterate through the REST endpoints.
3. Output the exact downloaded raw JSON/CSV locally without mutation.
4. Perform data completeness audit.

**PASS: PASS_SPB_6MONTH_EXPANSION_PLAN_READY**
