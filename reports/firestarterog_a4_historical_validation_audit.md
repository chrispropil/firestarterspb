# FirestarterOG A4 Historical Validation Audit Report

**Date:** 2026-06-07  
**Status:** VALIDATION COMPLETE  
**Lineage:** Historical Verification Lane  

---

## 1. Executive Summary

We have completed the historical validation checks against the recovered A4 10,000-row replay artifact located at [firestarter_lane_a4_25_symbol_cell1_replay_output.csv](file:///C:/Users/User/fastlane/data/firestarter_lane_a4_25_symbol_cell1_replay_output.csv).

All 10,000 rows were loaded and checked mathematically against the original scoring model. The formulas verified with 100% precision.

---

## 2. Check Results Table

| Check # | Check Description | Value / Result | Status |
|---|---|---|---|
| 1 | Row count = 10,000 | 10,000 | **PASS** |
| 2 | Symbol count = 25 | 25 | **PASS** |
| 3 | Rows per symbol = 400 | 400 (all symbols) | **PASS** |
| 4 | ER/FMLC/Flowprint/raw_score exist | Present | **PASS** |
| 5 | ER bounds (0 - 10) | Min: 0.55, Max: 0.55 | **PASS** |
| 6 | FMLC bounds (0 - 10) | Min: 0.65, Max: 0.65 | **PASS** |
| 7 | Flowprint bounds (0 - 8) | Min: 0.80, Max: 0.80 | **PASS** |
| 8 | raw_score recalculation check | Checked | **PASS** |
| 9 | raw_score vs raw_score_check comparison | Verified | **PASS** |
| 10 | Max absolute difference | 0.0 | **PASS** |
| 11 | Mismatch count (tolerance 0.01) | 0 | **PASS** |

---

## 3. Score Summary & Top Symbols

Because the A4 replay artifact is a mock / sandbox verification file, all rows in the dataset contain constant score metrics:
- **ER:** 0.55
- **FMLC:** 0.65
- **Flowprint:** 0.80
- **raw_score:** 0.66

Mathematically:
$$\text{raw\_score} = 0.55 \times 0.35 + 0.65 \times 0.35 + 0.80 \times 0.30 = 0.1925 + 0.2275 + 0.2400 = 0.66$$
This confirms perfect mathematical consistency.

### 3.1 Top 10 Symbols by Average raw_score
Since all symbols have constant values, they all share an identical average of **0.6600**:
1. BTCUSDT (0.6600)
2. ETHUSDT (0.6600)
3. SOLUSDT (0.6600)
4. XRPUSDT (0.6600)
5. ADAUSDT (0.6600)
6. DOGEUSDT (0.6600)
7. LINKUSDT (0.6600)
8. DOTUSDT (0.6600)
9. MATICUSDT (0.6600)
10. BNBUSDT (0.6600)

### 3.2 Top 10 Symbols by Average FMLC
All symbols share an identical average FMLC of **0.6500**:
1. BTCUSDT (0.6500)
2. ETHUSDT (0.6500)
3. SOLUSDT (0.6500)
4. XRPUSDT (0.6500)
5. ADAUSDT (0.6500)
6. DOGEUSDT (0.6500)
7. LINKUSDT (0.6500)
8. DOTUSDT (0.6500)
9. MATICUSDT (0.6500)
10. BNBUSDT (0.6500)

---

## 4. Research Observations & Caveats

- **ER Spikes & Divergences:** Since the scores in this particular artifact are constant, no active ER spikes or leading indicator divergences (such as FMLC or Flowprint weakness preceding a momentum spike) could be observed or documented in this test run.
- **Sandbox Tweaks:** Checked for experimental variables (`conviction_score`, `fakeout`, `hard_fakeout`, and `raw_score_no_4h_trend`). These remain segregated from the core production-ready scoring pipeline as research-only parameters.
- **Action/Gating Safety:** No Cell 2 active trading labels were assigned to this validation set.

---

`PASS_FIRESTARTEROG_A4_HISTORICAL_VALIDATION_COMPLETE`
