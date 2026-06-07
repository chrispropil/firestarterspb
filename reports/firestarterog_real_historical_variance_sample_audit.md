# FirestarterOG Real Historical Variance Sample Audit Report

**Run UTC Timestamp:** 2026-06-07T02:50:20.264152Z
**Purpose:** Auditing the generated non-mock historical variance dataset for scoring formula compliance and variance.
**Data Source:** Binance public Futures API historical data.

## 1. Data Integrity and Row Counts

| Symbol | Row Count | Start Timestamp (UTC) | End Timestamp (UTC) | Status |
|---|---:|---|---|---|
| SOLUSDT | 720 | 2026-05-08T03:00:00Z | 2026-05-26T10:00:00Z | **PASS** |
| DOGEUSDT | 720 | 2026-05-08T03:00:00Z | 2026-05-26T10:00:00Z | **PASS** |
| XRPUSDT | 720 | 2026-05-08T03:00:00Z | 2026-05-26T10:00:00Z | **PASS** |
| LINKUSDT | 720 | 2026-05-08T03:00:00Z | 2026-05-26T10:00:00Z | **PASS** |
| AVAXUSDT | 720 | 2026-05-08T03:00:00Z | 2026-05-26T10:00:00Z | **PASS** |
| NEARUSDT | 720 | 2026-05-08T03:00:00Z | 2026-05-26T10:00:00Z | **PASS** |
| BNBUSDT | 720 | 2026-05-08T03:00:00Z | 2026-05-26T10:00:00Z | **PASS** |
| AAVEUSDT | 720 | 2026-05-08T03:00:00Z | 2026-05-26T10:00:00Z | **PASS** |

## 2. Component Score Bounds Verification

- **Expansion Rating (ER) Bounds (0 - 10):** PASS (Observed: 0.0 to 10.0)
- **Funding/Market-Structure (FMLC) Bounds (0 - 10):** PASS (Observed: 4.0 to 10.0)
- **Flowprint Bounds (0 - 8):** PASS (Observed: 3.0 to 8.0)

## 3. Mathematical Score Verification

- **Re-Calculated raw_score Comparison:**
  - Max absolute difference: 0.0
  - Mismatch count (tolerance 0.01): 0
  - Status: PASS

## 4. Time-Series Variance Verification

To verify that the dataset contains true time-series variance (non-constant scores):
- Unique `er` values count: 11 (Expected > 1) -> **PASS**
- Unique `fmlc` values count: 7 (Expected > 1) -> **PASS**
- Unique `flowprint` values count: 6 (Expected > 1) -> **PASS**
- Unique `raw_score` values count: 68 (Expected > 1) -> **PASS**

## 5. Top 10 Symbols by Average raw_score

| Rank | Symbol | Average raw_score |
|---|---|---:|
| 1 | NEARUSDT | 5.0848 |
| 2 | BNBUSDT | 4.7756 |
| 3 | SOLUSDT | 4.4531 |
| 4 | AVAXUSDT | 4.4272 |
| 5 | LINKUSDT | 4.3939 |
| 6 | DOGEUSDT | 4.2051 |
| 7 | XRPUSDT | 4.1587 |
| 8 | AAVEUSDT | 4.1023 |

## 6. Top 10 Hourly Windows by raw_score

| Rank | Symbol | Timestamp (UTC) | Price | 24h Change % | ER | FMLC | Flowprint | raw_score |
|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | NEARUSDT | 2026-05-10T17:00:00Z | 1.597 | 2.11% | 10.0 | 10.0 | 8.0 | **9.40** |
| 2 | NEARUSDT | 2026-05-10T19:00:00Z | 1.621 | 3.91% | 10.0 | 10.0 | 8.0 | **9.40** |
| 3 | SOLUSDT | 2026-05-10T17:00:00Z | 96.47 | 3.56% | 10.0 | 10.0 | 8.0 | **9.40** |
| 4 | XRPUSDT | 2026-05-10T16:00:00Z | 1.4717 | 3.9% | 10.0 | 10.0 | 8.0 | **9.40** |
| 5 | SOLUSDT | 2026-05-10T09:00:00Z | 94.25 | 1.07% | 10.0 | 10.0 | 8.0 | **9.40** |
| 6 | NEARUSDT | 2026-05-08T08:00:00Z | 1.545 | 4.82% | 10.0 | 10.0 | 8.0 | **9.40** |
| 7 | AAVEUSDT | 2026-05-10T17:00:00Z | 99.64 | 4.5% | 10.0 | 10.0 | 8.0 | **9.40** |
| 8 | DOGEUSDT | 2026-05-10T23:00:00Z | 0.11242 | 3.43% | 10.0 | 10.0 | 8.0 | **9.40** |
| 9 | DOGEUSDT | 2026-05-10T22:00:00Z | 0.11186 | 2.61% | 10.0 | 10.0 | 8.0 | **9.40** |
| 10 | AAVEUSDT | 2026-05-10T16:00:00Z | 99.32 | 4.9% | 10.0 | 10.0 | 8.0 | **9.40** |

## 7. Research Observations (Domino Trigger Indicator Analysis)

This section documents instances where an Expansion Rating (ER) spike (ER >= 6) was preceded by deterioration in FMLC (FMLC < 4) or Flowprint (Flowprint < 3) in the prior 12 hours. This is for research observation only.

*No domino trigger setups (ER spikes preceded by FMLC/Flowprint weakness) were detected in this timeframe.*

## 8. Governance and Safety Confirmations

- **Cell 2 Gates Run:** **NO**. No action labels (`SCOUT BUY`, `TRIGGER BUY`, etc.) or neutral candidate gates were executed.
- **Live Notifications / Trading Signals:** **NO**. All processing was completed locally, and no messaging or alerts were broadcasted.
- **Secrets Exposed:** **NO**. Only public REST endpoints were used, and no environment or secret variables were accessed.
- **CSV Staged/Committed:** **NO**. Output CSV `firestarterog_real_historical_variance_sample.csv` remains strictly untracked and excluded from version control.

PASS_FIRESTARTEROG_REAL_HISTORICAL_VARIANCE_SAMPLE_COMPLETE
