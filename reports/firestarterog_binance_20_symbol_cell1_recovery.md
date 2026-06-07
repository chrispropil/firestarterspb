# FirestarterOG Binance 20-Symbol Cell 1 Recovery Audit Report

**Run UTC Timestamp:** 2026-06-07T02:09:40.310135Z
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
| 1 | PENGUUSDT | 0.006661 | 6.88% | 61,224,153.0 | 0.58 | 7.0 | 8.0 | 6.0 | **7.05** |
| 2 | LINKUSDT | 7.57 | 2.99% | 125,316,948.0 | 0.16 | 6.0 | 8.0 | 6.0 | **6.70** |
| 3 | ETHFIUSDT | 0.2997 | 4.75% | 13,228,403.0 | 0.26 | 7.0 | 7.0 | 6.0 | **6.70** |
| 4 | SHIBUSDT | 0.004642 | 2.16% | 38,236,094.0 | 0.22 | 5.0 | 8.0 | 6.0 | **6.35** |
| 5 | JTOUSDT | 0.5228 | 3.57% | 17,611,419.0 | 0.3 | 5.0 | 7.0 | 6.0 | **6.00** |
| 6 | BNBUSDT | 580.74 | 0.65% | 432,070,151.0 | 0.15 | 4.0 | 8.0 | 6.0 | **6.00** |
| 7 | MANTAUSDT | 0.08887 | 15.36% | 6,969,545.0 | 0.22 | 3.0 | 10.0 | 4.0 | **5.75** |
| 8 | DOGEUSDT | 0.08347 | 2.23% | 524,662,650.0 | 0.07 | 4.0 | 8.0 | 5.0 | **5.70** |
| 9 | INJUSDT | 5.331 | 3.21% | 63,814,850.0 | 0.14 | 4.0 | 8.0 | 5.0 | **5.70** |
| 10 | XRPUSDT | 1.1166 | 1.64% | 811,616,590.0 | 0.13 | 3.0 | 8.0 | 5.0 | **5.35** |

## 6. Full 20-Symbol Grid Results

| Ticker | Price | 24h Change % | Volume USD | RVOL 1H | RVOL 4H | ER | FMLC | Flowprint | raw_score |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| PENGUUSDT | 0.006661 | 6.88% | 61,224,153.0 | 0.58 | 1.7 | 7.0 | 8.0 | 6.0 | 7.05 |
| LINKUSDT | 7.57 | 2.99% | 125,316,948.0 | 0.16 | 1.87 | 6.0 | 8.0 | 6.0 | 6.70 |
| ETHFIUSDT | 0.2997 | 4.75% | 13,228,403.0 | 0.26 | 1.56 | 7.0 | 7.0 | 6.0 | 6.70 |
| SHIBUSDT | 0.004642 | 2.16% | 38,236,094.0 | 0.22 | 1.6 | 5.0 | 8.0 | 6.0 | 6.35 |
| JTOUSDT | 0.5228 | 3.57% | 17,611,419.0 | 0.3 | 1.72 | 5.0 | 7.0 | 6.0 | 6.00 |
| BNBUSDT | 580.74 | 0.65% | 432,070,151.0 | 0.15 | 1.69 | 4.0 | 8.0 | 6.0 | 6.00 |
| MANTAUSDT | 0.08887 | 15.36% | 6,969,545.0 | 0.22 | 0.68 | 3.0 | 10.0 | 4.0 | 5.75 |
| DOGEUSDT | 0.08347 | 2.23% | 524,662,650.0 | 0.07 | 1.11 | 4.0 | 8.0 | 5.0 | 5.70 |
| INJUSDT | 5.331 | 3.21% | 63,814,850.0 | 0.14 | 2.51 | 4.0 | 8.0 | 5.0 | 5.70 |
| XRPUSDT | 1.1166 | 1.64% | 811,616,590.0 | 0.13 | 1.25 | 3.0 | 8.0 | 5.0 | 5.35 |
| TRXUSDT | 0.32401 | 1.32% | 60,348,683.0 | 0.12 | 1.14 | 3.0 | 8.0 | 5.0 | 5.35 |
| CFXUSDT | 0.04496 | 2.37% | 4,554,719.0 | 0.09 | 0.74 | 4.0 | 6.0 | 5.0 | 5.00 |
| NEARUSDT | 1.943 | -1.62% | 273,612,555.0 | 0.17 | 1.75 | 3.0 | 6.0 | 6.0 | 4.95 |
| SOLUSDT | 63.7 | 0.2% | 2,035,902,842.0 | 0.12 | 1.33 | 3.0 | 6.0 | 6.0 | 4.95 |
| AVAXUSDT | 6.785 | 1.24% | 166,953,989.0 | 0.09 | 1.28 | 3.0 | 6.0 | 6.0 | 4.95 |
| ROSEUSDT | 0.00656 | 0.61% | 4,107,825.0 | 0.16 | 1.2 | 3.0 | 6.0 | 5.0 | 4.65 |
| PYTHUSDT | 0.03206 | 1.62% | 4,649,211.0 | 0.12 | 0.97 | 3.0 | 6.0 | 5.0 | 4.65 |
| AAVEUSDT | 62.32 | 2.11% | 70,783,877.0 | 0.51 | 1.2 | 3.0 | 6.0 | 5.0 | 4.65 |
| BERAUSDT | 0.246 | 0.86% | 7,905,185.0 | 0.08 | 0.79 | 1.0 | 7.0 | 4.0 | 4.00 |
| ORCAUSDT | 1.023 | 0.49% | 4,015,758.0 | 0.15 | 0.98 | 2.0 | 4.0 | 5.0 | 3.60 |

## 7. Recovery Conclusion

- **Missing Fields or Proxy Substitutions:** None. All fields (including `open_interest` and `funding` rate) were successfully retrieved from public Binance Futures APIs.
- **Cell 1 Status:** **FULLY RECOVERED** (The original scoring pipeline is perfectly operational on new public data snapshots).

PASS_FIRESTARTEROG_CELL1_BINANCE_20_RECOVERY
