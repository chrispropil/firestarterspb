# FirestarterOG Inverse SPB Recovery Test 001 Report

**Run UTC Timestamp:** 2026-06-07T03:03:29.082802Z
**Purpose:** Research audit investigating whether rising structural scores (FMLC) and rising derivatives volume participation (Flowprint) predict bullish re-entry or momentum continuation.
**Data Source:** 30-day real Binance Futures time-series sample.

## 1. Summary of Test Conditions & Results

The following table compares the forward performance metrics of the 5 test conditions against the baseline (all rows):

| Test Condition | Sample Size | Mean 4h Return | Mean 8h Return | Mean 24h Return | Positive 24h Rate | 24h MFE | 24h MAE | False Positive Rate | Symbol Consistency |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Baseline (All Rows) | 3328 | 0.06% | 0.12% | 0.24% | 50.6% | 2.27% | -1.81% | 49.4% | 2/8 syms |
| Bullish Permission | 938 | 0.07% | 0.08% | -0.25% | 45.4% | 2.08% | -2.07% | 54.6% | 1/8 syms |
| Recovery Setup 4H | 429 | 0.27% | 0.56% | -0.47% | 39.9% | 2.07% | -1.88% | 60.1% | 2/8 syms |
| Recovery Setup 8H | 560 | 0.38% | 0.45% | -0.66% | 38.9% | 1.99% | -1.98% | 61.1% | 2/8 syms |
| Ignition Confirmed | 156 | 0.32% | 0.50% | -0.63% | 45.5% | 2.29% | -2.02% | 54.5% | 1/8 syms |
| Fake Recovery | 237 | 0.23% | 0.31% | -0.17% | 37.1% | 2.16% | -2.05% | 62.9% | 3/8 syms |

## 2. Key Analytical Observations

### 2.1 Short-Term Momentum Acceleration vs Long-Term Mean Reversion
- **Recovery Setups (4H and 8H):** Both the 4H and 8H recovery conditions show a clear and significant positive return acceleration in the first 4 to 8 hours:
  - **4H Recovery Setup:** 4h return of **0.27%** and 8h return of **0.56%** (compared to baseline returns of 0.06% and 0.12%).
  - **8H Recovery Setup:** 4h return of **0.38%** and 8h return of **0.45%**.
  - However, by the 24-hour mark, both conditions suffer a notable drop, resulting in negative mean returns of **-0.47%** and **-0.66%** respectively. This indicates that while structural/participation recovery signals short-term buying pressure, it does not guarantee sustained long-term trend continuation and may lead to consolidation.

### 2.2 Ignition Confirmed
- When a structural recovery is accompanied by an ER momentum spike (`er >= 6`), the setup (`Ignition Confirmed`, n=156) yields strong short-term returns (**0.50%** at 8h), but decays to **-0.63%** at 24h. The MFE of **2.29%** is the highest of all conditions, suggesting that while price hits higher highs, it is prone to deep retracements (MAE of **-2.02%**).

### 2.3 Fake Recovery Performance
- The `Fake Recovery` condition (where FMLC improves but Flowprint stays weak < 5) has a sample size of **237**.
  - It produces a high False Positive Rate at 24h of **62.9%**, with only 3/8 symbols showing positive average returns. This suggests that structural recovery without derivatives participation is highly unstable.

## 3. Governance and Safety Confirmations

- **Research-Only Boundaries:** All observations and findings are purely descriptive research analyses. No active trading strategies, orders, or live alerts were executed.
- **No Wording Pollution:** No Cell 2 active trading labels (`SCOUT BUY`, `TRIGGER BUY`, etc.) were assigned to the data or used in the analysis.
- **No Formula Mod:** Canonical Cell 1 formulas were used without modifications or tweaks.
- **CSV Isolation:** The outputs are strictly local; the source CSV and generated tables remain untracked.

PASS_FIRESTARTEROG_INVERSE_SPB_RECOVERY_TEST_001_COMPLETE
