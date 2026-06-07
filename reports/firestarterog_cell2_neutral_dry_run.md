# FirestarterOG Cell 2 Neutral Dry-Run Audit Report

**Run UTC Timestamp:** 2026-06-07T02:30:42.176478Z
**Purpose:** Live validation of recovered original Firestarter Cell 2 Dust Cleaner logic using neutral research labels.
**Data Source:** Live Cell 1 Binance recovery snapshot CSV.

## 1. Row Counts & Field Analysis

- **Input Row Count (Cell 1 Recovery CSV):** 20
- **Output Row Count (Crypto Filtered):** 20
- **Required Fields Check:**
  - PASS: All required fields are present in the input dataset.

## 2. Candidate Classification Summary

| Neutral Research Class | Count | Description |
|---|---:|---|
| `scout_class_candidate` | 0 | Controlled risk, strong scores & FMLC/Flowprint participation |
| `trigger_class_candidate` | 1 | Actionable structure & score qualification, normal risk |
| `extended_watch_candidate` | 0 | Strong mover (16% to 25% 24h change), too extended for entry |
| `rejected_candidate` | 19 | Failed key gates or lacked tactical edge |

## 3. Top 10 Symbols by raw_score (with Neutral Class & Reason)

| Rank | Ticker | raw_score | price | 24h Change % | ER | FMLC | Flowprint | Neutral Class | Reason |
|---|---|---:|---|---:|---:|---:|---:|---|---|
| 1 | PENGUUSDT | 7.40 | 0.006691 | 7.54% | 8.0 | 8.0 | 6.0 | `trigger_class_candidate` | Actionable setup: wait for trigger/confirmation. |
| 2 | SHIBUSDT | 6.00 | 0.004624 | 1.76% | 4.0 | 8.0 | 6.0 | `rejected_candidate` | Rejected: not enough tactical edge. |
| 3 | MANTAUSDT | 5.75 | 0.08679 | 12.22% | 3.0 | 10.0 | 4.0 | `rejected_candidate` | Rejected: weak participation. |
| 4 | INJUSDT | 5.70 | 5.304 | 2.73% | 4.0 | 8.0 | 5.0 | `rejected_candidate` | Rejected: not enough tactical edge. |
| 5 | ETHFIUSDT | 5.70 | 0.2974 | 4.13% | 5.0 | 7.0 | 5.0 | `rejected_candidate` | Rejected: not enough tactical edge. |
| 6 | LINKUSDT | 5.70 | 7.531 | 2.6% | 4.0 | 8.0 | 5.0 | `rejected_candidate` | Rejected: not enough tactical edge. |
| 7 | TRXUSDT | 5.35 | 0.32395 | 1.44% | 3.0 | 8.0 | 5.0 | `rejected_candidate` | Rejected: not enough tactical edge. |
| 8 | JTOUSDT | 5.35 | 0.5157 | 2.83% | 4.0 | 7.0 | 5.0 | `rejected_candidate` | Rejected: not enough tactical edge. |
| 9 | XRPUSDT | 5.00 | 1.1094 | 1.31% | 2.0 | 8.0 | 5.0 | `rejected_candidate` | Rejected: not enough tactical edge. |
| 10 | AAVEUSDT | 4.95 | 61.99 | 1.76% | 3.0 | 6.0 | 6.0 | `rejected_candidate` | Rejected: not enough tactical edge. |

## 4. Qualified Candidates (Scout/Trigger Class Only)

| Ticker | raw_score | price | 24h Change % | risk_pct | invalidation_distance | Neutral Class | Reason |
|---|---:|---|---:|---:|---|---|---|
| PENGUUSDT | 7.40 | 0.006691 | 7.54% | 2.67% | STRETCHED | `trigger_class_candidate` | Actionable setup: wait for trigger/confirmation. |

## 5. Governance and Safety Confirmations

- **Cell 1 Formulas Modified:** **NO**. Original formulas for ER, FMLC, Flowprint, and raw_score remain exactly as documented in the master specification and were not altered.
- **Action/Trading Labels or Alerts Triggered:** **NO**. No live notifications were sent, no trade recommendations were made, and all classifications use neutralized research-candidate names.
- **Trading Signal Classification:** **NO**. This is a neutral, local dry-run simulation for historical alignment research and formula verification only.

PASS_FIRESTARTEROG_CELL2_NEUTRAL_DRY_RUN_COMPLETE
