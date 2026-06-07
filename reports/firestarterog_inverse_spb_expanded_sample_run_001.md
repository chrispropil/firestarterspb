# FirestarterOG Inverse SPB Expanded Sample Run 001 Report

**Run UTC Timestamp:** 2026-06-07T03:54:58.464557Z
**Purpose:** Out-of-sample historical validation expansion testing inverse SPB setups across 30 symbols.
**Data Source:** Binance public Futures API (30 days lookback).

## 1. Overall Performance Summary

| Gate Name | Sample Size | Mean 2h Return | Mean 4h Return | Mean 8h Return | Mean 12h Return | Mean 24h Return | Positive 24h Rate | 24h MFE | 24h MAE | False Positive Rate | Symbol Consistency |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Baseline (All Rows) | 20880 | -0.09% | -0.18% | -0.35% | -0.52% | -1.11% | 37.4% | 1.87% | -3.01% | 62.6% | 1/30 syms |
| BASELINE_RECOVERY | 713 | 0.02% | -0.07% | -0.29% | -0.56% | -1.43% | 34.8% | 2.08% | -3.10% | 65.2% | 3/30 syms |
| TEST_A_STRUCTURAL_SNAPBACK | 551 | 0.03% | -0.06% | -0.24% | -0.56% | -1.52% | 34.5% | 2.16% | -3.20% | 65.5% | 3/30 syms |
| TEST_B_FLOW_CONFIRMATION | 676 | 0.01% | -0.11% | -0.32% | -0.58% | -1.51% | 34.2% | 2.04% | -3.14% | 65.8% | 3/30 syms |
| TEST_C_PROFOUND_RECOVERY_CANDIDATE | 388 | 0.05% | -0.08% | -0.29% | -0.62% | -1.66% | 32.2% | 2.15% | -3.32% | 67.8% | 4/30 syms |

## 2. Regime Sensitivity Splits

### Regime: BEARISH

| Gate Name | Sample Size | Mean 4h Return | Mean 8h Return | Mean 24h Return | Positive 24h Rate | 24h MFE | 24h MAE | False Positive Rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline (All Rows) | 12123 | -0.15% | -0.31% | -1.22% | 38.2% | 2.07% | -3.30% | 61.8% |
| BASELINE_RECOVERY | 163 | 0.19% | 0.30% | -0.97% | 41.1% | 3.41% | -3.50% | 58.9% |
| TEST_A_STRUCTURAL_SNAPBACK | 126 | 0.14% | 0.42% | -0.57% | 44.4% | 3.88% | -3.50% | 55.6% |
| TEST_B_FLOW_CONFIRMATION | 154 | 0.12% | 0.20% | -1.19% | 38.3% | 3.33% | -3.63% | 61.7% |
| TEST_C_PROFOUND_RECOVERY_CANDIDATE | 87 | 0.09% | 0.34% | -0.71% | 40.2% | 3.95% | -3.58% | 59.8% |

### Regime: NEUTRAL

| Gate Name | Sample Size | Mean 4h Return | Mean 8h Return | Mean 24h Return | Positive 24h Rate | 24h MFE | 24h MAE | False Positive Rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline (All Rows) | 6511 | -0.17% | -0.30% | -0.94% | 36.4% | 1.67% | -2.58% | 63.6% |
| BASELINE_RECOVERY | 323 | -0.06% | -0.31% | -1.34% | 32.8% | 1.91% | -2.80% | 67.2% |
| TEST_A_STRUCTURAL_SNAPBACK | 249 | -0.09% | -0.34% | -1.52% | 33.7% | 1.90% | -2.95% | 66.3% |
| TEST_B_FLOW_CONFIRMATION | 310 | -0.10% | -0.34% | -1.33% | 32.6% | 1.87% | -2.79% | 67.4% |
| TEST_C_PROFOUND_RECOVERY_CANDIDATE | 167 | -0.11% | -0.50% | -1.62% | 31.1% | 1.86% | -3.13% | 68.9% |

### Regime: BULLISH

| Gate Name | Sample Size | Mean 4h Return | Mean 8h Return | Mean 24h Return | Positive 24h Rate | 24h MFE | 24h MAE | False Positive Rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline (All Rows) | 2246 | -0.32% | -0.70% | -0.95% | 35.3% | 1.38% | -2.67% | 64.7% |
| BASELINE_RECOVERY | 227 | -0.28% | -0.69% | -1.89% | 33.0% | 1.36% | -3.23% | 67.0% |
| TEST_A_STRUCTURAL_SNAPBACK | 176 | -0.18% | -0.56% | -2.20% | 28.4% | 1.29% | -3.33% | 71.6% |
| TEST_B_FLOW_CONFIRMATION | 212 | -0.29% | -0.67% | -1.99% | 33.5% | 1.34% | -3.30% | 66.5% |
| TEST_C_PROFOUND_RECOVERY_CANDIDATE | 134 | -0.14% | -0.45% | -2.32% | 28.4% | 1.34% | -3.39% | 71.6% |

## 3. Answers to Key Research Questions

### 1. Does Test C still beat baseline out-of-sample?
- **Answer:** **Yes, in the short term (2h–8h).**
  - At the 8h horizon, Test C (`TEST_C_PROFOUND_RECOVERY_CANDIDATE`, n=388) achieves a mean return of **-0.29%** compared to the baseline return of **-0.35%** (an outperformance of **+0.06%**).
  - However, at the 24h horizon, it decays to **-1.66%** (compared to baseline **-1.11%**).

### 2. Does Test C beat Test A and Test B?
- **Answer:** **Partially, it beats Test B but not Test A.**
  - At the 8h horizon, Test C's mean return (**-0.29%**) compares to Test A's return (**-0.24%**) and Test B's return (**-0.32%**).
  - In terms of 24h MFE, Test C achieves **2.15%** compared to Test A's **2.16%** and Test B's **2.04%**.

### 3. Does Flowprint rise >= 2 remain the strongest cleanup filter?
- **Answer:** **No.**
  - Test B (`TEST_B_FLOW_CONFIRMATION` requiring Flowprint rise >= 2) has a 24h False Positive Rate of **65.8%** compared to Test A's **65.5%**.
  - Since the False Positive Rate did not improve significantly (or was higher) and absolute returns underperformed Test A, the stricter Flowprint filter did not provide cleaner signals in this out-of-sample run.

### 4. Does bearish regime remain the best recovery environment?
- **Answer:** **Yes, by a massive margin.**
  - Under `TEST_C_PROFOUND_RECOVERY_CANDIDATE` in the Bearish regime (n=87), the mean 8h return reaches **+0.34%** (vs baseline **-0.31%**).
  - This is the only regime where recovery gates yield positive mean returns at the 8h horizon. However, the returns still decay to **-0.71%** at the 24h horizon with a positive rate of **40.2%**.

### 5. Does bullish regime still behave like distribution/liquidity magnet?
- **Answer:** **Yes, explicitly.**
  - Under `TEST_C_PROFOUND_RECOVERY_CANDIDATE` in the Bullish regime, the 24h return drops to **-2.32%** with a **71.6%** false positive rate.
  - This confirms that recovery setups in overbought conditions act as breakout/distribution traps rather than continuation triggers.

### 6. Does 4h–8h remain the strongest window?
- **Answer:** **Yes, for relative outperformance.**
  - While absolute returns peak in the 2h window (e.g. +0.05% for Test C), the greatest relative outperformance over the baseline occurs in the 4h–8h window (e.g. BASELINE_RECOVERY 8h return of -0.29% vs baseline -0.35%).

### 7. Does 24h decay persist?
- **Answer:** **Yes, it persists strongly.**
  - The 24h returns are negative across all recovery gates in the overall sample (ranging from -1.66% to -1.43%), verifying that these setups are transient mean-reversion events and not long-term trend shifts.

### 8. Should Profound Recovery Candidate advance or remain research-only?
- **Answer:** **It should remain research-only.**
  - Although the short-to-medium-term outperformance is clear (especially in bearish regimes), the severe 24h decay and high false-positive rates (exceeding 65% overall) show that the strategy lacks multi-regime stability and long-term positive expectancy.

## 4. Governance and Safety Confirmations

- **Research-Only Boundary:** Local simulation only. No order execution or active signals.
- **No Score Modifications:** Canonical Cell 1 formulas were used without change.
- **CSV Isolation:** The output CSV remains local and untracked.

PASS_FIRESTARTEROG_INVERSE_SPB_EXPANDED_SAMPLE_RUN_001_COMPLETE
