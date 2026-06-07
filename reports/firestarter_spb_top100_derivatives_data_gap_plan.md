# Top 100 Derivatives Data Gap and Pull Plan

## 1. Public Binance USDⓈ-M Futures Endpoints
The following public endpoints can provide the missing derivatives context:
- **Funding Rate History:** `GET /fapi/v1/fundingRate`  
  Returns funding rate history for a symbol (weight: 1).
- **Open Interest Statistics (Global):** `GET /futures/data/openInterestHist`  
  Returns global open interest statistics over time (weight: 1).
- **Taker Long/Short Ratio:** `GET /futures/data/takerlongshortRatio`  
  Returns taker buy/sell volume and taker buy/sell ratio (weight: 1).
- **Long/Short Account Ratio (Global):** `GET /futures/data/globalLongShortAccountRatio`  
  Returns global long/short account ratio (weight: 1).
- **Top Trader Account Long/Short Ratio:** `GET /futures/data/topLongShortAccountRatio`  
  Returns top trader account long/short ratio (weight: 1).
- **Top Trader Position Long/Short Ratio:** `GET /futures/data/topLongShortPositionRatio`  
  Returns top trader position long/short ratio (weight: 1).
- **Mark Price / Premium Index:** `GET /fapi/v1/premiumIndex`  
  Returns premium index, funding rate, and mark price (weight: 1).

## 2. Retention Limits
- **Derivatives Data Endpoints:** Global open interest, taker volume ratios, and top trader ratios only retain **retained latest 30 days** of history for public API requests.
- **Funding History:** Returns historical data up to 1000 records per request; goes back further depending on start/end timestamp parameters.

## 3. Expected Cadence
- **Funding rate:** 8-Hour cadence (standard funding cycle).
- **Open interest stats:** 1-Hour or 5-Minute interval.
- **Taker buy/sell volume:** 1-Hour or 5-Minute interval.
- **Long/short account ratio:** 1-Hour or 5-Minute interval.
- **Top trader ratios:** 1-Hour or 5-Minute interval.

## 4. Mapping to Firestarter ER/FMLC/Flowprint
- **ER (Ignition Pressure):** RVOL 1H and RVOL 4H (candle-only). If derivatives are added, open interest presence is used as a participation gate.
- **FMLC (Governor):** `fundingRate` maps to premium state. `sumOpenInterest` and `sumOpenInterestValue` map to leverage/range positions. `longShortRatio` (top trader accounts and positions) maps to the positioning governor.
- **Flowprint (Participation):** Taker buy/sell ratio maps to flow quality. Funding rate and Open interest statistics map to participation bands.

## 5. Fields Not Available via Binance Public API
- **Institutional Identity:** Detailed breakdown of institutional vs. retail market participants.
- **L3 Order Book History:** Full historical order books with order ID tracking.
- **Off-exchange Liquidations:** OTC and off-exchange liquidation events.

## 6. Proposed Local Output Directory
`data/research/binance_top100_derivatives_context_1month/`  
(Ensure this folder is added to `.gitignore` to prevent raw data tracking).

## 7. Manifest Schema
The manifest `reports/firestarter_spb_top100_derivatives_context_1month_manifest.csv` will contain:
`symbol, file_type, row_count, first_timestamp_utc, last_timestamp_utc, checksum_sha256`

## 8. Dry-Run Selection Logic
- Test pull on 3 target symbols: `BTCUSDT`, `ETHUSDT`, and `SOLUSDT` over a 24-hour window first.
- Verify timestamp joins and API endpoint responsiveness.

## 9. Rate Limits & Retry Rules
- Limit request weight to 1000 per minute (well below standard 1200 weight limit).
- Implement exponential backoff with jitter on 429/418 responses.

## 10. Fail-Closed Handling
- If any single query fails 3 times, abort the entire pull process, write no partial files to the directory, and raise `HOLD_DERIVATIVES_PULL_FAIL`.

## 11. Approval Gate
- **No data pull is authorized by this plan.** 
- Execution is strictly gated until Chris or Jody explicitly confirms with:
  `PASS_TOP100_DERIVATIVES_PULL_START`
