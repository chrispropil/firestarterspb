# FirestarterOG Inverse SPB Validation Expansion Plan

**Date:** 2026-06-07  
**Status:** PLAN PROPOSED  
**Lineage:** Historical Verification Lane  

---

## 1. Executive Summary & Core Context

This document outlines the validation expansion plan to study the **Inverse SPB Recovery** effect. In our initial test (Test 001, 30 days, 8 symbols), we discovered a distinct short-term return acceleration following structural (FMLC) and participation (Flowprint) recoveries, which decayed by the 24-hour mark.

This expansion aims to test whether this effect is stable, consistent across different market conditions, and replicable over a larger scope of assets and timeframes.

### 1.1 Summary of Initial Findings to Preserve:
1. **Short-Term Acceleration:** Both `Recovery Setup 4H` (0.56% return at 8h) and `Recovery Setup 8H` (0.45% return at 8h) significantly outperformed the baseline (0.12% at 8h).
2. **24h Decay/Reversal:** The return advantage decayed by 24h, reverting to negative mean returns (-0.47% and -0.66% respectively) compared to a positive baseline (+0.24%).
3. **Fake Recovery Instability:** The `Fake Recovery` setup (where FMLC improves but Flowprint stays weak < 5) resulted in a high 24h False Positive Rate of **62.9%**.
4. **Flowprint Gating:** Derivatives volume participation confirmation (Flowprint) is required to prevent chasing low-volume/illiquid structural moves.
5. **Scoring Formula Lock:** No modifications to the original Cell 1 score formulas (`ER`, `FMLC`, `Flowprint`, `raw_score`) are approved or will be made.

---

## 2. Expanded Validation Parameters

### 2.1 Asset Universe (20 to 50 Symbols)
We will expand symbol coverage to include **30 major futures assets** from Binance, capturing a broader range of market capitalizations and sectors:
- *Core candidates:* SOL, DOGE, XRP, LINK, AVAX, NEAR, BNB, AAVE, BTC, ETH, ADA, DOT, MATIC, LTC, BCH, UNI, ATOM, FIL, ICP, VET, STX, SHIB, TRX, XMR, ALGO, OP, ARB, APT, SUI, PEPE.

### 2.2 Timeframe and API Limitations (60 to 120 Days)
- **Resolution:** 1-Hour interval candles.
- **Lookback Target:** 60 to 120 days.
- **API Constraint Note:** The public REST endpoint `/futures/data/openInterestHist` is restricted to the most recent **30 days** of data. To achieve a 60–120 day backtest, the collection script will:
  1. Retrieve standard OHLCV and funding rate data via REST (which supports longer histories).
  2. For open interest, join with local historical database archives (e.g. from `C:\Users\User\fastlane\data\` or daily CSV downloads from `data.binance.vision`) to bypass the REST lookback limit.
  3. If historical archives are unavailable for specific symbols, cap REST collection to 30 days.

### 2.3 Target Forward Windows
We will measure forward performance across five distinct horizons:
- **2 Hours**
- **4 Hours**
- **8 Hours**
- **12 Hours**
- **24 Hours**

---

## 3. Test Condition Families

We will evaluate the following six research conditions:

1. **`bullish_permission`:**
   $$\text{FMLC} \ge 7 \quad \text{AND} \quad \text{Flowprint} \ge 5$$
2. **`recovery_4h`:**
   $$\text{FMLC rise over 4h} \ge 2 \quad \text{AND} \quad \text{Flowprint rise over 4h} \ge 1$$
3. **`recovery_8h`:**
   $$\text{FMLC rise over 8h} \ge 2 \quad \text{AND} \quad \text{Flowprint rise over 8h} \ge 1$$
4. **`ignition_confirmed`:**
   $$\text{recovery\_4h or recovery\_8h} \quad \text{AND} \quad \text{ER} \ge 6$$
5. **`fake_recovery`:**
   $$\text{FMLC rise} \ge 2 \quad \text{AND} \quad \text{Flowprint} < 5 \text{ (at T-0)}$$
6. **`spb_breakdown`:**
   $$\text{ER} \ge 6 \quad \text{AND} \quad \text{FMLC} < 5 \quad \text{AND} \quad \text{Flowprint} < 4 \quad \text{AND} \quad \text{FMLC/Flowprint falling (over 4h)}$$

---

## 4. Measurement & Analytics Metrics

For each test condition, the validation script will compute:
- **Sample Size:** Total occurrences.
- **Average Forward Returns:** Mean percentage return for the 2h, 4h, 8h, 12h, and 24h horizons.
- **Positive Return Rate:** Percentage of positive returns at each horizon.
- **Max Favorable Excursion (MFE):** Peak percentage gain within the 24h forward window.
- **Max Adverse Excursion (MAE):** Peak percentage loss within the 24h forward window.
- **False Positive Rate:** Percentage of setups resulting in negative returns at 24h.
- **Symbol Consistency:** Ratio of symbols displaying positive average returns vs total symbol coverage.
- **Regime Sensitivity:** Analysis of forward returns grouped by market regime (Bull vs Bear vs Range/Chop, classified using a 24h baseline index return).

---

## 5. Governance, Safety, & Staging Policy

- **No Formula Promotion:** Findings will not be used to propose or deploy adjustments to the core FirestarterOG scoring logic.
- **No Cell 2 Actions:** Active buy/sell recommendations, alerts, and trading logs are strictly barred. All outputs will use research-only candidate classes.
- **Data Exclusion:** All collected raw files and generated CSV summary matrices will remain untracked locally and excluded from git commits.
- **Execution Guard:** This document is the plan only. Execution will not begin until the plan is formally approved.

---

`PASS_FIRESTARTEROG_INVERSE_SPB_VALIDATION_EXPANSION_PLAN_READY`
