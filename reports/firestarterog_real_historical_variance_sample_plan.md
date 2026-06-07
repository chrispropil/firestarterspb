# FirestarterOG Real Historical Variance Sample Plan

**Date:** 2026-06-07  
**Status:** PLAN PROPOSED  
**Lineage:** Historical Variance Generation Lane  

---

## 1. Objectives

The goal of this plan is to construct a non-mock historical sample dataset using public market data from Binance Futures. This dataset will feature realistic, time-varying values for Expansion Rating (`ER`), Funding/Market-Structure Rating (`FMLC`), Derivatives/Volume Participation (`Flowprint`), and the combined `raw_score`. 

This historical variance is critical for testing structural shifts, market regimes, and validating the **SPB / Domino Trigger** hypothesis (where deterioration in FMLC and Flowprint precedes ER spikes).

---

## 2. Target Settings & Symbols

### 2.1 Target Symbols (8 Symbols)
- `SOLUSDT`
- `DOGEUSDT`
- `XRPUSDT`
- `LINKUSDT`
- `AVAXUSDT`
- `NEARUSDT`
- `BNBUSDT`
- `AAVEUSDT`

### 2.2 Timeframe
- **Target Period:** 30 days (e.g., May 1, 2026 to May 31, 2026)
- **Resolution:** 1-hour interval candles.
- **Expected Data Points:** ~720 rows per symbol, totaling ~5,760 records.

---

## 3. Required Binance Futures Endpoints

To retrieve the historical inputs without private API credentials, we will poll the following public endpoints:

1. **OHLCV Candles (1h and 4h):**
   - Endpoint: `GET https://fapi.binance.com/fapi/v1/klines`
   - Parameters: `symbol`, `interval` (1h, 4h), `startTime`, `endTime`, `limit` (max 1500)
2. **Historical Open Interest:**
   - Endpoint: `GET https://fapi.binance.com/fapi/v1/openInterestHist`
   - Parameters: `symbol`, `period=1h`, `startTime`, `endTime`, `limit` (max 500)
3. **Funding Rate History:**
   - Endpoint: `GET https://fapi.binance.com/fapi/v1/fundingRate`
   - Parameters: `symbol`, `startTime`, `endTime`, `limit` (max 1000)

---

## 4. Exact Feature Construction Plan

For every timestamp $t$ (on a 1-hour grid):

1. **Windowed High/Low Indicators:**
   - `high_20`: Maximum of high price over the preceding 20 hours ($t-19$ to $t$).
   - `low_20`: Minimum of low price over the preceding 20 hours ($t-19$ to $t$).
   - `high_50_4h`: Maximum of 4h high price over the preceding 50 bars.
   - `low_50_4h`: Minimum of 4h low price over the preceding 50 bars.
2. **Moving Averages (1h and 4h):**
   - `ema_9`: Exponential Moving Average (span 9) of 1h close prices.
   - `ema_21`: Exponential Moving Average (span 21) of 1h close prices.
   - `ema_50_4h`: Exponential Moving Average (span 50) of 4h close prices.
3. **Volume-Based Indicators:**
   - `rvol_1h`: Current 1h volume divided by the average 1h volume of the past 20 hours.
   - `rvol_4h_window`: Total volume over the last 4 hours divided by the total volume of the preceding 4-hour window.
   - `change_24h`: 24h percentage change in price: $\frac{\text{close}_t - \text{close}_{t-24}}{\text{close}_{t-24}} \times 100$.
4. **Range Positions:**
   - `range_pos_20`: $\frac{\text{close}_t - \text{low\_20}}{\text{high\_20} - \text{low\_20}}$.
   - `range_pos_50_4h`: $\frac{\text{close}_t - \text{low\_50\_4h}}{\text{high\_50\_4h} - \text{low\_50\_4h}}$.
5. **Logic Flags:**
   - `near_breakout`: Boolean flag indicating if $\text{close}_t \ge \text{high\_20} \times 0.992$.
   - `clean_reclaim`: Boolean flag indicating if $\text{close}_t > \text{ema\_21}_t$ and $\text{ema\_9}_t > \text{ema\_21}_t$.
   - `above_4h_trend`: Boolean flag indicating if $\text{close}_t > \text{ema\_50\_4h}_t$.
6. **Join Alignment:**
   - Align `open_interest` and `funding` rate entries matching timestamp $t$.

---

## 5. Raw-Data Isolation & Governance Policy

To preserve repository safety and prevent accidental checkin of private tokens or large datasets:
- **Local Data Only:** All raw JSON payloads and temporary CSV files downloaded from Binance must be saved in the git-ignored `data/research/` directory.
- **Untracked Target Outputs:** The generated outputs (`reports/firestarterog_real_historical_variance_sample.csv` or `.parquet`) must be added to `.gitignore` or kept strictly untracked.
- **Secrets Isolation:** No API keys are required for these endpoints; the collection script will not access environment files containing Slack tokens or other credentials.
- **No Cell 2 Logic:** Gating and active trading candidate labels are excluded from this phase. No active alarms or notifications will be executed.

---

## 6. Expected Output Schema

The generated time-series CSV file will include the following columns for each hourly row:

- `ticker` (string)
- `timestamp_utc` (string, ISO8601 format)
- `price` (float)
- `change_24h_%` (float)
- `volume_usd` (float)
- `rvol_1h` (float)
- `rvol_4h_window` (float)
- `er` (float/int)
- `fmlc` (float/int)
- `flowprint` (float/int)
- `raw_score` (float)
- `near_breakout` (boolean)
- `clean_reclaim` (boolean)
- `above_4h_trend` (boolean)
- `range_pos_20` (float)
- `range_pos_50_4h` (float)
- `open_interest` (float)
- `funding` (float)
- `ema_21` (float)
- `is_stock_token` (boolean, constant `False` for crypto assets)

---

## 7. Validation Checks

Upon script execution, the output dataset will be audited against the following validation rules:
1. **Row Count Check:** Verify that rows exist for all 8 symbols across the 30-day period (~5,760 total rows).
2. **Formula Integrity Check:** Validate that `raw_score` values match:
   $$\text{raw\_score} = \text{ER} \times 0.35 + \text{FMLC} \times 0.35 + \text{Flowprint} \times 0.30$$
3. **Score Bounds Check:** Validate that component scores fall within expected bounds (ER: 0–10, FMLC: 0–10, Flowprint: 0–8).
4. **Time-Series Variance Check:** Confirm that standard deviations of score columns (`ER`, `FMLC`, `Flowprint`, `raw_score`) are greater than $0.0$, verifying that the data is not constant.

---

## 8. Status Markers

- **Pass Condition:** `PASS_FIRESTARTEROG_REAL_HISTORICAL_VARIANCE_SAMPLE_PLAN_READY`
- **Hold Condition:** `HOLD_FIRESTARTEROG_HISTORICAL_VARIANCE_PLAN_FIELD_GAP`

The real historical variance generation plan is ready for review:  
`PASS_FIRESTARTEROG_REAL_HISTORICAL_VARIANCE_SAMPLE_PLAN_READY`
