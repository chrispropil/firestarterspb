# FirestarterOG Binance 20-Symbol Cell 1 Recovery Audit Report

**Run UTC Timestamp:** 2026-06-07T02:23:59.737480Z
**Purpose:** Live recovery validation of original Firestarter Cell 1 formulas on a 20-symbol Binance snapshot.
**Data Source:** Binance public USD-M Futures REST API (no private keys used).

## 1. Symbols Scanned & Replacements

Total requested symbols: 20
Total successfully scanned: 20

### Replacements Made:
- `SHIBUSDT` was not directly available and was replaced with active contract: `1000SHIBUSDT`

## 2. Required Schema Verification

The output CSV contains exactly the following columns, complying with the recovery spec:
- `ticker`, `price`, `change_24h_%`, `volume_usd`, `rvol_1h`, `rvol_4h_window`
- `er`, `fmlc`, `flowprint`, `raw_score`
- `near_breakout`, `clean_reclaim`, `above_4h_trend`
- `range_pos_20`, `range_pos_50_4h`, `open_interest`, `funding`, `ema_21`
- `is_stock_token`, `risk_pct`, `invalidation_distance`, `ignition_momentum`, `ignition_participation`

### Verification Checklists:
- New CSV contains all Cell 2-required fields: PASS
- Cell 2 (action label assignment/gating) was NOT run: PASS (Cell 1 patch only)
- CSV remains locally untracked: PASS (git ignored or local untracked file)

## 3. Score Bounds Check

- **ER Bounds (0 - 10):** PASS
- **FMLC Bounds (0 - 10):** PASS
- **Flowprint Bounds (0 - 8):** PASS

## 4. raw_score Formula Verification

Calculated raw_score formula matches:
- Mathematical Verification: PASS
  `raw_score = ER * 0.35 + FMLC * 0.35 + Flowprint * 0.30` (rounded to 2 decimals)

## 5. Top 10 Symbols by raw_score

| Rank | Ticker | Price | 24h Change % | Volume USD | RVOL 1H | ER | FMLC | Flowprint | raw_score |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | PENGUUSDT | 0.006691 | 7.54% | 62,124,313.0 | 1.2 | 8.0 | 8.0 | 6.0 | **7.40** |
| 2 | SHIBUSDT | 0.004624 | 1.76% | 38,261,128.0 | 0.44 | 4.0 | 8.0 | 6.0 | **6.00** |
| 3 | MANTAUSDT | 0.08679 | 12.22% | 7,045,855.0 | 0.74 | 3.0 | 10.0 | 4.0 | **5.75** |
| 4 | INJUSDT | 5.304 | 2.73% | 63,762,808.0 | 0.3 | 4.0 | 8.0 | 5.0 | **5.70** |
| 5 | ETHFIUSDT | 0.2974 | 4.13% | 13,297,639.0 | 0.52 | 5.0 | 7.0 | 5.0 | **5.70** |
| 6 | LINKUSDT | 7.531 | 2.6% | 125,093,930.0 | 0.34 | 4.0 | 8.0 | 5.0 | **5.70** |
| 7 | TRXUSDT | 0.32395 | 1.44% | 60,107,396.0 | 0.28 | 3.0 | 8.0 | 5.0 | **5.35** |
| 8 | JTOUSDT | 0.5157 | 2.83% | 17,723,044.0 | 0.66 | 4.0 | 7.0 | 5.0 | **5.35** |
| 9 | XRPUSDT | 1.1094 | 1.31% | 812,410,549.0 | 0.37 | 2.0 | 8.0 | 5.0 | **5.00** |
| 10 | AAVEUSDT | 61.99 | 1.76% | 70,643,270.0 | 0.76 | 3.0 | 6.0 | 6.0 | **4.95** |

## 6. Full 20-Symbol Grid Results

| Ticker | Price | 24h Change % | Volume USD | RVOL 1H | RVOL 4H | ER | FMLC | Flowprint | raw_score |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| PENGUUSDT | 0.006691 | 7.54% | 62,124,313.0 | 1.2 | 2.29 | 8.0 | 8.0 | 6.0 | 7.40 |
| SHIBUSDT | 0.004624 | 1.76% | 38,261,128.0 | 0.44 | 1.73 | 4.0 | 8.0 | 6.0 | 6.00 |
| MANTAUSDT | 0.08679 | 12.22% | 7,045,855.0 | 0.74 | 0.77 | 3.0 | 10.0 | 4.0 | 5.75 |
| INJUSDT | 5.304 | 2.73% | 63,762,808.0 | 0.3 | 2.63 | 4.0 | 8.0 | 5.0 | 5.70 |
| ETHFIUSDT | 0.2974 | 4.13% | 13,297,639.0 | 0.52 | 1.64 | 5.0 | 7.0 | 5.0 | 5.70 |
| LINKUSDT | 7.531 | 2.6% | 125,093,930.0 | 0.34 | 1.95 | 4.0 | 8.0 | 5.0 | 5.70 |
| TRXUSDT | 0.32395 | 1.44% | 60,107,396.0 | 0.28 | 1.2 | 3.0 | 8.0 | 5.0 | 5.35 |
| JTOUSDT | 0.5157 | 2.83% | 17,723,044.0 | 0.66 | 1.89 | 4.0 | 7.0 | 5.0 | 5.35 |
| XRPUSDT | 1.1094 | 1.31% | 812,410,549.0 | 0.37 | 1.34 | 2.0 | 8.0 | 5.0 | 5.00 |
| AAVEUSDT | 61.99 | 1.76% | 70,643,270.0 | 0.76 | 1.3 | 3.0 | 6.0 | 6.0 | 4.95 |
| BNBUSDT | 578.72 | 0.36% | 427,364,969.0 | 0.44 | 1.84 | 3.0 | 6.0 | 5.0 | 4.65 |
| DOGEUSDT | 0.08291 | 1.94% | 524,666,848.0 | 0.26 | 1.19 | 1.0 | 8.0 | 4.0 | 4.35 |
| NEARUSDT | 1.932 | -1.93% | 274,270,049.0 | 0.52 | 1.92 | 2.0 | 6.0 | 5.0 | 4.30 |
| SOLUSDT | 63.31 | -0.16% | 2,039,338,676.0 | 0.4 | 1.43 | 1.0 | 6.0 | 5.0 | 3.95 |
| AVAXUSDT | 6.736 | 0.58% | 166,681,169.0 | 0.28 | 1.36 | 1.0 | 6.0 | 5.0 | 3.95 |
| CFXUSDT | 0.0446 | 1.46% | 4,559,253.0 | 0.34 | 0.82 | 1.0 | 6.0 | 4.0 | 3.65 |
| PYTHUSDT | 0.03182 | 0.89% | 4,622,592.0 | 0.23 | 1.01 | 1.0 | 6.0 | 4.0 | 3.65 |
| ROSEUSDT | 0.0065 | -0.15% | 4,092,202.0 | 0.34 | 1.26 | 1.0 | 4.0 | 5.0 | 3.25 |
| BERAUSDT | 0.244 | 0.12% | 7,903,408.0 | 0.33 | 0.86 | 0.0 | 5.0 | 4.0 | 2.95 |
| ORCAUSDT | 1.015 | -0.39% | 4,022,129.0 | 0.54 | 1.1 | 0.0 | 2.0 | 4.0 | 1.90 |

## 7. Recovery Conclusion

- **Missing Fields or Proxy Substitutions:** None. All fields (including `open_interest` and `funding` rate) were successfully retrieved from public Binance Futures APIs.
- **Cell 1 Status:** **FULLY RECOVERED** (The original scoring pipeline is perfectly operational on new public data snapshots).

PASS_FIRESTARTEROG_CELL1_BINANCE_20_RECOVERY
