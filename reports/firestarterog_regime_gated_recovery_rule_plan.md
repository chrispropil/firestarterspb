# FirestarterOG Regime-Gated Recovery Rule Plan

**Date:** 2026-06-07  
**Status:** PLAN PROPOSED  
**Lineage:** Historical Verification Lane  

---

## 1. Objectives

This document presents a research-only plan to isolate and formalize regime-gated inverse SPB recovery rules. Following the findings of our Bears/Bulls sensitivity audit, it is clear that market-wide regime indicators completely invert the performance profile of structural recoveries. 

This plan details the rulesets and validation criteria necessary to test these behaviors over a larger scope before any thresholds are considered validated or overfit-resistant.

---

## 2. Core Empirical Findings to Preserve

1. **Bearish Mean-Reversion Edge:** In Bearish regimes (prior 24h basket return < 0%), recovery setups display very strong performance, peaking in the 4h–8h window (e.g. `Recovery Setup 4H` average 8h return of **+1.38%** with a **78.3%** positive rate).
2. **Bullish Distribution Trap:** In Bullish regimes (prior 24h basket return > 2%), recoveries decay immediately and produce deep negative returns (e.g. `Recovery Setup 4H` 24h return of **-2.09%** with a **77.6%** false-positive rate).
3. **Transient Nature:** Validated that the edge is concentrated within the 4h–8h window, turning negative or reverting by the 24h window across all regimes except Bearish.

---

## 3. Isolated Ruleset Definitions

We define three distinct candidate classifications for testing in the next expansion phase:

### 3.1 Bearish Recovery Candidate (Re-Entry Signal)
Designed to isolate high-probability mean-reversion buying pressure in oversold environments.
- **Regime Gate:** Prior 24h basket average return < 0.0%.
- **Structural Gate:** FMLC rises by $\ge 2$ over a 4h or 8h window.
- **Participation Gate:** Flowprint rises by $\ge 1$ over the same window.
- **Momentum Confirmation:** Expansion Rating (ER) $\ge 6$.
- **Target Evaluation Window:** 4h to 8h forward return.

### 3.2 Bullish Trap Candidate (Distribution Warning)
Designed to flag late-cycle breakout traps where retail buy liquidity is absorbed by distribution.
- **Regime Gate:** Prior 24h basket average return > 2.0%.
- **Trigger event:** FMLC/Flowprint recovery setup occurs (FMLC rise $\ge 2$, Flowprint rise $\ge 1$).
- **Deterioration Horizon:** 12h to 24h forward returns.
- **Risk Indicator:** High expected false-positive rate (exceeding 70%).

### 3.3 Fake Recovery Warning (Liquidity Trap)
Designed to flag structural spikes that lack derivatives/volume participation.
- **Trigger Event:** FMLC rises by $\ge 2$ over 4h or 8h.
- **Lacking Participation:** Flowprint remains weak (below 5) at T-0 (now).
- **Risk Profile:** High false-positive rate across all regimes (observed at 62.9% in initial audit).

---

## 4. Validation & Expanded Sample Requirements

To avoid overfitting risks, no rules will be promoted to active trading systems based on the 30-day sample. The following expansion criteria are required:
- **Sample Expansion:** Implement these rulesets against a 30-symbol, 90-day historical dataset (utilizing local archives to bypass the REST API's 30-day open interest lookback limit).
- **Out-of-Sample Partition:** Divide the expanded dataset into a 60-day train partition (for threshold optimization) and a 30-day out-of-sample test partition (for validation).
- **Regime Robustness Check:** Verify that the Bearish Recovery Candidate outperforms the baseline in at least 80% of the tested symbols.

---

## 5. Governance, Safety, & Boundaries

- **Research-Only Scope:** All metrics and candidate classifications are purely descriptive research tools.
- **Profound Recovery Candidate:** Will remain strictly research-only and segregated from production pipelines.
- **No Cell 2 Integration:** These rules are isolated from the Cell 2 action-label engine. No live alerts, buy/sell recommendations, or slack updates will be generated.
- **CSV Data Control:** No raw market data or generated evaluation databases will be checked into version control.

---

`PASS_FIRESTARTEROG_REGIME_GATED_RECOVERY_RULE_PLAN_READY`
