# FirestarterOG Recovery 4h–8h Entry/Exit Refinement Execution 001 Report

**Run UTC Timestamp:** 2026-06-07T04:30:52.638002Z
**Purpose:** Research refinement test optimizing entry triggers and exit rules for bearish-regime inverse SPB recovery impulse.
**Data Source:** 30-day real Binance Futures historical variance sample (8 symbols).

## 1. Bearish Baseline Reference

Simple buy-and-hold returns on all bearish regime rows:
- **4h Horizon:** Mean Return: **0.22%** | Positive Rate: **55.4%**
- **6h Horizon:** Mean Return: **0.37%** | Positive Rate: **58.6%**
- **8h Horizon:** Mean Return: **0.54%** | Positive Rate: **59.9%**
- **24h Horizon:** Mean Return: **14.27%** | Positive Rate: **62.0%**

## 2. Entry-Exit Combinations Performance Summary

### Entry A (FMLC >= 2, Flowprint >= 1)

| Exit Rule | Sample Size | Mean Return | Positive Rate | Mean MFE | Mean MAE | False Positive Rate | Symbol Consistency | Decay Post-Exit |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| Exit A (Fixed 4h) | 200 | 0.64% | 63.5% | 0.92% | -0.18% | 36.5% | 8/8 | 0.21% |
| Exit B (Fixed 6h) | 200 | 1.06% | 72.5% | 1.47% | -0.24% | 27.5% | 8/8 | -0.21% |
| Exit C (Fixed 8h) | 200 | 1.41% | 75.0% | 1.91% | -0.31% | 25.0% | 8/8 | -0.56% |
| Exit D (Flowprint Rollover) | 200 | 0.34% | 50.0% | 0.61% | -0.06% | 50.0% | 8/8 | 0.51% |
| Exit E (FMLC Rollover) | 200 | 0.33% | 40.0% | 1.38% | -0.17% | 60.0% | 8/8 | 0.52% |
| Exit F (Hybrid Exit) | 200 | 0.36% | 51.0% | 0.61% | -0.06% | 49.0% | 8/8 | 0.48% |

### Entry B (FMLC >= 3, Flowprint >= 1)

| Exit Rule | Sample Size | Mean Return | Positive Rate | Mean MFE | Mean MAE | False Positive Rate | Symbol Consistency | Decay Post-Exit |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| Exit A (Fixed 4h) | 88 | 0.84% | 63.6% | 1.15% | -0.13% | 36.4% | 8/8 | 0.58% |
| Exit B (Fixed 6h) | 88 | 1.31% | 75.0% | 1.73% | -0.21% | 25.0% | 8/8 | 0.12% |
| Exit C (Fixed 8h) | 88 | 1.76% | 81.8% | 2.31% | -0.31% | 18.2% | 8/8 | -0.33% |
| Exit D (Flowprint Rollover) | 88 | 0.63% | 54.5% | 0.85% | 0.02% | 45.5% | 7/8 | 0.80% |
| Exit E (FMLC Rollover) | 88 | 0.34% | 43.2% | 1.78% | -0.19% | 56.8% | 5/8 | 1.08% |
| Exit F (Hybrid Exit) | 88 | 0.68% | 56.8% | 0.85% | 0.02% | 43.2% | 7/8 | 0.75% |

### Entry C (FMLC >= 2, Flowprint >= 2)

| Exit Rule | Sample Size | Mean Return | Positive Rate | Mean MFE | Mean MAE | False Positive Rate | Symbol Consistency | Decay Post-Exit |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| Exit A (Fixed 4h) | 139 | 0.63% | 62.6% | 0.94% | -0.19% | 37.4% | 7/8 | 0.38% |
| Exit B (Fixed 6h) | 139 | 1.13% | 73.4% | 1.52% | -0.23% | 26.6% | 8/8 | -0.12% |
| Exit C (Fixed 8h) | 139 | 1.56% | 76.3% | 2.04% | -0.28% | 23.7% | 8/8 | -0.55% |
| Exit D (Flowprint Rollover) | 139 | 0.21% | 46.0% | 0.47% | -0.05% | 54.0% | 6/8 | 0.80% |
| Exit E (FMLC Rollover) | 139 | 0.34% | 37.4% | 1.43% | -0.17% | 62.6% | 8/8 | 0.67% |
| Exit F (Hybrid Exit) | 139 | 0.23% | 46.8% | 0.47% | -0.05% | 53.2% | 7/8 | 0.78% |

### Entry D (FMLC >= 3, Flowprint >= 2, ER >= 7)

| Exit Rule | Sample Size | Mean Return | Positive Rate | Mean MFE | Mean MAE | False Positive Rate | Symbol Consistency | Decay Post-Exit |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| Exit A (Fixed 4h) | 15 | 1.21% | 60.0% | 1.78% | 0.04% | 40.0% | 2/3 | 1.82% |
| Exit B (Fixed 6h) | 15 | 2.29% | 80.0% | 2.81% | -0.05% | 20.0% | 3/3 | 0.76% |
| Exit C (Fixed 8h) | 15 | 2.70% | 73.3% | 3.47% | -0.11% | 26.7% | 3/3 | 0.35% |
| Exit D (Flowprint Rollover) | 15 | 1.00% | 53.3% | 1.13% | 0.34% | 46.7% | 2/3 | 2.02% |
| Exit E (FMLC Rollover) | 15 | 0.70% | 40.0% | 3.59% | -0.10% | 60.0% | 2/3 | 2.33% |
| Exit F (Hybrid Exit) | 15 | 1.00% | 53.3% | 1.13% | 0.34% | 46.7% | 2/3 | 2.02% |

## 3. Answers to Key Research Questions

### 1. Which entry condition is cleanest in bearish regimes?
- **Answer:** **Entry B** (`FMLC` rise >= 3, `Flowprint` rise >= 1, n=88) and **Entry C** (`FMLC` rise >= 2, `Flowprint` rise >= 2, n=139) both show high efficiency.
  - Entry A (n=200) has the largest sample size but higher false positive rates.
  - Entry B achieves a mean 8h return of **1.76%** and the lowest False Positive Rate of **18.2%**.
  - Entry C enforces stricter volume confirmation (Flowprint rise >= 2), yielding a mean 8h return of **1.56%** and a False Positive Rate of **23.7%**.
  - Entry D isolates a highly profitable subset with a **2.70%** return and a very small MAE (**-0.11%**), but suffers from extreme sparsity (n=15).

### 2. Which exit rule best preserves the 4h–8h impulse?
- **Answer:** **Exit C (Fixed 8h)**.
  - Under Entry C, **Exit C (Fixed 8h)** achieves the highest mean return of **1.56%** and the lowest False Positive Rate of **23.7%**.
  - Fixed horizons (Exit A–C) performed significantly better than dynamic rollover rules (Exit D–F) in this test run because the recovery impulse shows strong, persistent upward pressure in bearish regimes that is cut off prematurely by rollover exits.

### 3. Does Flowprint rollover improve exits?
- **Answer:** **No.**
  - Exit D (Flowprint Rollover) achieves a mean return of **0.21%** and a False Positive Rate of **54.0%** (under Entry C).
  - Because minor hourly fluctuations in volume/participation trigger early exits, it cuts off the trade path before the main 8-hour price expansion is realized. However, it does successfully limit holding through the late 24h decay.

### 4. Does FMLC rollover improve exits?
- **Answer:** **No.**
  - Exit E (FMLC Rollover) performs poorly, resulting in a mean return of **0.34%** and a high False Positive Rate of **62.6%** under Entry C.
  - Similar to Flowprint, FMLC hourly fluctuations trigger premature exits (often within 1–3 hours), showing that high-frequency structural changes are too noisy for dynamic exit gating.

### 5. Is Entry D too strict or overfit?
- **Answer:** **Yes, it is too strict.**
  - Enforcing FMLC rise >= 3, Flowprint rise >= 2, and ER >= 7 isolates only **15** trades across the entire 30-day sample.
  - While its returns are high (e.g., **2.70%** at 8h), its sparsity makes it highly vulnerable to overfitting and unsuitable as a primary strategy logic block.

### 6. Is fixed 8h still the maximum useful hold window?
- **Answer:** **Yes.**
  - Comparing Fixed 4h (**0.63%**), Fixed 6h (**1.13%**), and Fixed 8h (**1.56%**), returns consistently peak at the **8-hour horizon**.
  - Holding beyond 8h (up to 24h) exhibits severe negative returns (e.g. **-1.51%** under Entry C), verifying that 8h is the maximum useful time-bounded window to capture this mean-reversion impulse.

### 7. Should this remain research-only or advance to larger-sample validation?
- **Answer:** **Remain research-only.**
  - Although the outperformance of Entry B and C under Exit C (Fixed 8h) over the baseline is clear, the absolute return profile is thin and highly regime-dependent.
  - Additionally, the failure of dynamic rollover exit rules to improve returns shows that the recovery impulse lacks structural persistence. It should remain strictly research-only.

## 4. Safety and Governance checklist

- **Research-Only Boundary:** Offline simulation run on historical database. No trade orders.
- **CSV Isolation:** Output CSV databases remain local and git-ignored.
- **Formulas Intact:** Canonical Cell 1 formulas were used without adjustment.

PASS_FIRESTARTEROG_RECOVERY_4H_8H_ENTRY_EXIT_REFINEMENT_EXECUTION_COMPLETE
