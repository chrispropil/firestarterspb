# Firestarter SPB: Top 100 Dashboard V4 Formula Execution Review

## Overview
This document reviews the implementable formula rules for ER, FMLC, Flowprint_proxy, and raw_score from the available source reports in the repository, and determines whether actual metric computation can be safely enabled.

## 1. Reports Reviewed
1. [firestarter_spb_binance_5_token_formula_spec_confirmation.md](file:///C:/firestarterspb/reports/firestarter_spb_binance_5_token_formula_spec_confirmation.md)
2. [firestarter_spb_binance_5_token_cell1_computation_plan.md](file:///C:/firestarterspb/reports/firestarter_spb_binance_5_token_cell1_computation_plan.md)
3. [reports/firestarter_spb_top100_dashboard_v3_firestarter_metric_source_review.md](file:///C:/firestarterspb/reports/firestarter_spb_top100_dashboard_v3_firestarter_metric_source_review.md)

---

## 2. Review Findings & Gaps

### 1. Exact Formula Components Available
The summary-level components documented in the source reports are:
- **ER:** RVOL 1H, RVOL 4H window, 24h change ranges, `near_breakout`, `clean_reclaim`.
- **FMLC:** liquidity floor, 4H range position, 20-bar range position, `clean_reclaim`, `above_4h_trend`, anti-blowoff governor based on `change_24h`.
- **Flowprint_proxy:** RVOL 1H, RVOL 4H window, OI availability, funding band quality, close above EMA21, `near_breakout`.
- **raw_score:** Weighted blend: `raw_score = ER * 0.35 + FMLC * 0.35 + Flowprint_proxy * 0.30`.

### 2. Exact Weights Available
- `ER`: 35%
- `FMLC`: 35%
- `Flowprint_proxy`: 30%

### 3. Exact Clamp Ranges Available
- `ER`: 0 to 10
- `FMLC`: 0 to 10
- `Flowprint_proxy`: 0 to 8

### 4. Required Input Fields
- **OHLCV Candles:** `open`, `high`, `low`, `close`, `volume` (1H/4H grids)
- **Derivatives & Positioning Data:** `fundingRate`, `markPrice`, `sumOpenInterest`, `sumOpenInterestValue`, `longShortRatio` (account/position)

### 5. Available Fields from Binance Top 100 Dataset
The local Top 100 dataset (`data/research/binance_top100_excluding_existing_5_1month/`) only contains 5m OHLCV files.
- Available fields: `open_time`, `open`, `high`, `low`, `close`, `volume`, `close_time`, `quote_asset_volume`, `number_of_trades`, `taker_buy_base_asset_volume`, `taker_buy_quote_asset_volume`.
- Generated resamples: 1H and 4H aggregates.

### 6. Missing or Approximated Fields & Parameters
The following mathematical details and parameters are **completely missing**:
- Exact RVOL thresholds and scoring weights.
- Exact lookback windows for averages and ranges.
- Exact definitions for `near_breakout`, `clean_reclaim`, and `above_4h_trend`.
- Exact liquidity floor values and range-position equations.
- Gating policies for missing or zero-volume bars.

### 7. Availability of OI/Funding-Dependent Data
- **OI/Funding Data Availability:** COMPLETELY UNAVAILABLE in the Top 100 dataset.
- There are no open interest statistics, funding history, or top-trader ratio CSV files collected for the Top 100 contracts (unlike the Binance 5-token research sandbox).

### 8. Implementable Formulas
- **Safely Implementable Now:** NONE. 
- Attempting to compute any of these metrics would require inventing threshold values, lookbacks, and scoring parameters, which violates strict sandbox integrity.

### 9. Gating Policy
- Because the formula specifications are incomplete and the derivatives parent data is missing, **all components must remain disabled placeholders** labeled as `NOT ENABLED — formula gate required` to prevent arbitrary signal invention.

---

## 3. Stop Gate Triggered

> [!WARNING]
> **HOLD GATE TRIGGERED:** `HOLD_FORMULA_SPEC_INSUFFICIENT`
>
> **Reason:** The source reports confirm summary-level ancestry only and do not provide executable mathematical rules, point allocation tables, or thresholds. Furthermore, required derivatives and position tracking fields (funding, open interest, top-trader ratios) are not collected or present in the Binance Top 100 dataset. Implementing calculations would require arbitrary invention.
