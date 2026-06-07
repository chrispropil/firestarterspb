# FirestarterOG Recovery 4h–8h Entry/Exit Refinement 001 Plan

**Date:** 2026-06-07  
**Status:** PLAN PROPOSED  
**Lineage:** Historical Verification Lane  

---

## 1. Executive Summary & Purpose

This plan establishes a research-only framework to study the entry and exit dynamics of the **bearish-regime inverse SPB recovery impulse**. 

Prior audits ([Bearish Regime Sensitivity Audit 001](file:///C:/firestarterspb/reports/firestarterog_bearish_regime_sensitivity_audit_001.md) and the [Expanded Sample Run 001](file:///C:/firestarterspb/reports/firestarterog_inverse_spb_expanded_sample_run_001.md)) verified that structural and participation recoveries behave as highly reliable short-term mean-reversion events when the overall market basket is bearish. However, these setups suffer from severe decay and reversal by the 12h–24h mark. 

This test aims to evaluate whether specific entry triggers combined with dynamic exit rules can preserve the peak 4h–8h return impulse while successfully avoiding the subsequent decay.

### 1.1 Model Shift & Framing Lock
To prevent misinterpretation and alignment risks, we establish a strict model framing lock:
* **CORRECT FRAMING:** Bearish-regime recovery = a short-window mean-reversion impulse (transient relative strength).
* **REJECTED FRAMING:** Recovery = a multi-day trend-following long-side continuation event.

---

## 2. Test Configuration Families

We will evaluate the combination of four entry triggers and six exit rules against the 30-symbol out-of-sample dataset.

### 2.1 Entry Trigger Tests

All entry conditions are strictly gated by the bearish market regime (prior 24h average basket return < 0.0%):

1. **`Entry A` (Baseline Recovery):**
   - Bearish regime basket condition.
   - FMLC rise over 4h or 8h $\ge 2$.
   - Flowprint rise over 4h or 8h $\ge 1$.
2. **`Entry B` (Stricter Structure - Structural Snapback):**
   - Bearish regime basket condition.
   - FMLC rise over 4h or 8h $\ge 3$.
   - Flowprint rise over 4h or 8h $\ge 1$.
3. **`Entry C` (Stricter Participation - Flow Confirmation):**
   - Bearish regime basket condition.
   - FMLC rise over 4h or 8h $\ge 2$.
   - Flowprint rise over 4h or 8h $\ge 2$.
4. **`Entry D` (Maximum Gating - Profound Recovery Candidate):**
   - Bearish regime basket condition.
   - FMLC rise over 4h or 8h $\ge 3$.
   - Flowprint rise over 4h or 8h $\ge 2$.
   - Current Expansion Rating (ER) $\ge 7$.

### 2.2 Exit Rule Tests

Once an entry is triggered, the trade position is tracked to evaluate the following exit rules:

* **`Exit A` (Fixed 4h):** Exit the position exactly 4 hours after entry.
* **`Exit B` (Fixed 6h):** Exit the position exactly 6 hours after entry.
* **`Exit C` (Fixed 8h):** Exit the position exactly 8 hours after entry.
* **`Exit D` (Flowprint Rollover):** Exit the position immediately when Flowprint begins to decay or falls below standard levels.
  - *Mathematical Definition:* $\text{Flowprint}_T < \text{Flowprint}_{T-1}$ (1-hour drop) **OR** $\text{Flowprint}_T < 4$ (participation exhaustion).
* **`Exit E` (FMLC Rollover):** Exit the position immediately when structural momentum rolls over.
  - *Mathematical Definition:* $\text{FMLC}_T < \text{FMLC}_{T-1}$ (1-hour drop) **OR** $\text{FMLC}_T < 5$ (structural breakdown).
* **`Exit F` (Hybrid Exit):** Whichever occurs first: Fixed 8-hour horizon **OR** Flowprint Rollover trigger.

---

## 3. Analytics & Measurement Metrics

For each of the 24 Entry-Exit combinations (Entry A–D crossed with Exit A–F), the script will calculate and compile the following metrics:

1. **Sample Size:** Total number of triggered occurrences.
2. **Average Return:** Mean percentage price change from entry to exit.
3. **Positive Return Rate:** Percentage of trades resulting in positive returns.
4. **Max Favorable Excursion (MFE):** Peak percentage gain observed during the trade holding window.
5. **Max Adverse Excursion (MAE):** Peak percentage loss observed during the trade holding window.
6. **False-Positive Rate:** Percentage of setups resulting in negative returns at the exit point.
7. **Symbol Consistency:** Ratio of symbols displaying positive average returns vs. total symbol coverage.
8. **Regime Sensitivity:** Validation checks confirming performance behavior under Bearish vs. Neutral vs. Bullish market-wide conditions.
9. **Decay After Exit Window:** Forward return from the exit timestamp to $T+24$ hours (verifying if the exit rule successfully avoided the downward reversion curve).
10. **Comparison Versus Baseline Bearish Rows:** Comparison of the average return and positive rate against a simple holding baseline of all bearish regime rows.

---

## 4. Key Questions to Answer in the Report

The final audit report must address the following questions:
1. Which entry condition is cleanest (highest positive rate and lowest MAE) in bearish regimes?
2. Which exit rule preserves most of the 4h–8h impulse before reversion?
3. Does Flowprint rollover improve exits compared to fixed holding windows?
4. Does FMLC rollover improve exits compared to fixed holding windows?
5. Does Entry D remain too strict (resulting in insufficient sample size) or overfit?
6. Is 8h still the maximum useful hold window for bearish mean reversion?
7. Should this strategy remain research-only, or has it demonstrated enough stability to advance to a larger-sample out-of-sample validation?

---

## 5. Governance, Safety, & Boundaries

To ensure complete alignment with data and safety standards:
- **Research-Only Scope:** No order execution, buy/sell recommendations, action labels, or live alerts will be generated.
- **Formula Integrity:** No modifications will be made to canonical Cell 1 indicators (`ER`, `FMLC`, `Flowprint`, `raw_score`).
- **CSV Data Exclusion:** No raw database outputs or generated datasets will be committed to version control.
- **Verification Commit Lock:** Only this plan document is staged for commit. Execution scripts and CSV runs remain strictly untracked.

---

`PASS_FIRESTARTEROG_RECOVERY_4H_8H_ENTRY_EXIT_REFINEMENT_PLAN_READY`
