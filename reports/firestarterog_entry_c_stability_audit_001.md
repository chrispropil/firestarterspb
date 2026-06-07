# FirestarterOG Entry C Stability Audit 001 Plan

**Date:** 2026-06-07  
**Status:** PLAN PROPOSED  
**Lineage:** Historical Verification Lane  

---

## 1. Objectives & Executive Summary

This document presents a research-only plan to execute a **stability audit** on the current best-performing inverse SPB recovery trigger and exit pair: **Entry C combined with a Fixed 8h Exit**.

In our entry/exit refinement backtest ([Refinement Execution 001](file:///C:/firestarterspb/reports/firestarterog_recovery_4h_8h_entry_exit_refinement_execution_001.md)), the combination of Entry C and Exit C emerged as the strongest candidate. This plan details the testing methodology, metrics, and criteria to determine if this edge is mathematically stable and consistent, or if it suffers from concentration risks, clustering, or overfitting.

### 1.1 Candidate Configuration to Audit
* **Entry Trigger (Entry C):**
  - Basket regime is Bearish (prior 24h average return of the basket < 0.0%).
  - FMLC rises by $\ge 2$ over a 4h or 8h window.
  - Flowprint rises by $\ge 2$ over the same window.
* **Exit Trigger (Exit C):**
  - Fixed 8h holding window.
* **Baseline Baseline Target Results to Preserve/Validate:**
  - Sample size: **139**
  - Mean 8h return: **+1.56%**
  - 8h False Positive Rate (FPR): **23.7%**

---

## 2. Stability Audit Checks & Methodology

The audit script will perform the following checks on the local time-series dataset:

### 2.1 Symbol Concentration Audit
To confirm the return is not driven by 1–2 highly volatile or outlying assets:
* **Metrics:** Compute sample size, mean return, and positive rate grouped by symbol (e.g. SOL, DOGE, XRP, LINK, AVAX, NEAR, BNB, AAVE).
* **Concentration Check:** Calculate the proportion of total cumulative return contributed by each symbol.
* **Consistency Check:** Verify if at least 70% of individual symbols achieve positive average returns.

### 2.2 Date/Time Clustering Audit
To check if the edge is driven by a single macro event or day (e.g. a market-wide capitulation snapback day):
* **Metrics:** Group trade triggers by day/date and calculate the daily trigger count and average return.
* **Clustering Check:** Identify the top 3 days by sample size. Calculate their contribution to the total trade returns.
* **Macro Robustness:** Determine if the strategy remains profitable when excluding the single most active day.

### 2.3 Intra-Window Risk & Excursion Profile
To audit the intra-trade risk and path efficiency:
* **Excursion Metrics:** Audit maximum adverse excursion (MAE) and maximum favorable excursion (MFE) distribution.
* **Drawdown Audit:** Measure the distribution of paper drawdowns during the 8h hold window.
* **Time-to-MFE Check:** Find the average hour $h \in [1, 8]$ where MFE is achieved. Verify if the price typically peaks before the 8h exit.

### 2.4 Horizon Sensitivity: 6h vs. 8h Hold
To determine if the extra exposure of the last 2 hours is justified:
* **Comparison Matrix:** Compare return, positive rate, MFE, and MAE of Exit B (Fixed 6h, mean return **+1.13%**, FPR **26.6%**) versus Exit C (Fixed 8h, mean return **+1.56%**, FPR **23.7%**).
* **Efficiency Ratio:** Assess whether the 8h return improvement is proportional to the increased risk (worse MAE).

### 2.5 Volatility Sensitivity
To evaluate how Entry C behaves in different market volatility regimes:
* **Volatility Gating:** Group rows into High-Volatility (above median hourly ATR/RVOL) and Low-Volatility (below median) conditions.
* **Comparative Stats:** Compare sample size, return, MFE, MAE, and false-positive rates across both volatility pools.

### 2.6 BTC-Led vs. Alt-Led Leadership Gating
To verify the influence of market leadership:
* **Leadership Gate:** Classify trades by whether BTC or the Altcoin basket led the initial FMLC/Flowprint recovery:
  - *BTC-Led:* BTCUSDT 24h return exceeds Altcoin basket 24h return by $\ge 1.0\%$ at trigger.
  - *Alt-Led:* Altcoin basket 24h return exceeds BTCUSDT 24h return by $\ge 1.0\%$ at trigger.
* **Comparative Metrics:** If data is insufficient or unavailable, clearly note the field gap. Otherwise, report the split performance.

### 2.7 Regime Isolation Check
* **Regime Gating:** Confirm that 100% of tested rows are bearish-regime only (basket average 24h change < 0.0%).
* **Baseline Comparison:** Compare overall statistics against the bearish all-row baseline (all rows under bearish regime, regardless of recovery signals).

---

## 3. Stability Verdict Criteria

Based on the audit metrics, the strategy will be assigned one of the following verdicts:
1. **Stable:** Returns are broadly distributed across symbols/dates, MAE is bounded, and the 8h window shows structural efficiency.
2. **Promising but Under-sampled:** Edge appears real but suffers from sample sparsity, requiring a larger out-of-sample partition.
3. **Symbol-Concentrated:** Rejection state. Profitability is driven by 1–2 symbols (e.g. only NEAR or AVAX).
4. **Date-Clustered:** Rejection state. Triggers are clustered on a single day or macro event.
5. **Rejected / Unstable:** Return profile is highly volatile, drawdown is excessive, or alts fail to outperform baselines.

---

## 4. Governance & Safety Guidelines

- **Research Boundary:** Local, offline simulation only. No live trading, order submission, or alerts.
- **Formula Gating:** Canonical Cell 1 formulas will not be modified or tuned to fit the dataset.
- **Data Boundaries:** Raw CSV data and generated evaluation matrices will not be added to version control.
- **Lock Commit Only:** Stage and commit this plan report only.

---

`PASS_FIRESTARTEROG_ENTRY_C_STABILITY_AUDIT_001_COMPLETE`
