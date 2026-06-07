# Top 100 Derivatives Data Integration Readiness Audit

This audit evaluates the locally pulled public Binance derivatives context dataset for the validated Top 100 symbols to determine whether the dashboard can safely compute partial Cell 1 Firestarter reconstruction metrics (ER, FMLC, Flowprint_proxy, raw_score).

---

## 1. Symbol Availability & Coverage

### 1. Symbols Available in OHLCV Dataset
Exactly **100 symbols** are present in the kline source directory `data/research/binance_top100_excluding_existing_5_1month/`.

### 2. Symbols Available in Derivatives Context
Exactly **98 symbols** are present in the derivatives context directory `data/research/binance_top100_derivatives_context_1month/`.

### 3. Missing Symbols
The following **2 symbols** are missing from the derivatives dataset:
- `币安人生USDT`
- `龙虾USDT`

*Reason:* These are non-standard/custom symbols that are not supported by the public Binance Futures exchange.

### 4. Endpoint Coverage by Symbol
- **98 Standard Symbols:** 100% coverage. All 7 derivatives subdirectories contain a corresponding CSV file for each of these 98 symbols.
- **2 Non-Standard Symbols:** 0% coverage. No derivatives data files were created.

---

## 2. Dataset Usability & Alignment

### 5. Timestamp Coverage by Endpoint
- **fundingRate:** Covers the full 1-month range at an 8-Hour cadence (173 records per symbol, starting on 2026-05-10 00:00:00 UTC).
- **Historical Stats (openInterestHist, takerlongshortRatio, globalLongShortAccountRatio, topLongShortAccountRatio, topLongShortPositionRatio):** Covers the latest 29 days at a 1-Hour cadence (693–694 rows, starting on 2026-05-09 22:00:00 UTC). This represents the safe limit of the Binance 30-day retention constraint.
- **premiumIndex:** Covers a single current snapshot row (retrieved live on 2026-06-07 21:08:43 UTC).

### 6. Usability of Open Interest (OI)
- **Status:** **USABLE** (with a partial-window gate).
- **Notes:** High-quality global open interest values (`sumOpenInterest`, `sumOpenInterestValue`) are available for all 98 standard symbols from 2026-05-09 22:00:00 UTC onwards. Rows prior to this timestamp must be gated as parent unavailable.

### 7. Usability of Funding Rates
- **Status:** **USABLE** (full-window).
- **Notes:** Funding rate history covers the full target range at standard 8-Hour cycle intervals and can be joined to candle rows after normal timestamp offset rounding.

### 8. Usability of Taker Buy/Sell Volume
- **Status:** **USABLE** (with a partial-window gate).
- **Notes:** Taker buy/sell volume and volume ratios are available for the 98 standard symbols starting 2026-05-09 21:00:00 UTC.

### 9. Usability of Long/Short Ratios
- **Status:** **USABLE** (with a partial-window gate).
- **Notes:** Global account ratios, top trader account ratios, and top trader position ratios are available for the 98 standard symbols starting 2026-05-09 22:00:00 UTC.

---

## 3. Cell 1 Formula Readiness

### 10. Data-Available Formula Components
With the local derivatives context dataset successfully pulled and verified, the primary parent fields for the following Cell 1 components are now **available** for the 98 standard symbols (within the 29-day history window):
- **ER:** RVOL 1H/4H candle-only pressure (100% available).
- **FMLC:** Funding rate levels (full window), Open Interest statistics, and Top Trader positioning ratios (last 29 days).
- **Flowprint_proxy:** Candle volume patterns (full window), funding band quality, and open interest presence (last 29 days).
- **raw_score:** The final blended score (ER * 0.35 + FMLC * 0.35 + Flowprint_proxy * 0.30) is computable for rows where all parent fields are present.

### 11. Missing Formula Thresholds & Spec Gaps
Although the parent datasets are now local, **actual metric computation cannot be executed** because the following mathematical specs and parameter thresholds are still missing:
- Exact lookback windows for average volume (RVOL) and price channels.
- Exact numeric thresholds and point allocation tables for scoring ER, FMLC, and Flowprint_proxy.
- Exact equations for FMLC range-positioning scores.
- Gating policies for handling zero-volume candles or missing rows.

---

## 4. Final Decision

> [!WARNING]
> **HOLD DECISION:** `HOLD_FORMULA_SPEC_STILL_INSUFFICIENT`
>
> **Reason:** While the derivatives data integration readiness is complete for the 98 standard symbols, the exact mathematical specs, thresholds, and scoring tables for the Cell 1 Firestarter formulas are still missing in the repository records. To prevent arbitrary signal invention, calculation of ER, FMLC, Flowprint_proxy, and raw_score must remain disabled placeholders on the dashboard until an approved math spec is provided.
