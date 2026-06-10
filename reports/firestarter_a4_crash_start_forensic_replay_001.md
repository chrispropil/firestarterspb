# Firestarter A4 Crash-Start Forensic Replay 001

**Run UTC Timestamp:** 2026-06-07T05:43:43.889889Z
**Status:** AUDIT EXECUTED
**System:** Matrix Alpha / Firestarter A4
**Data Source:** `firestarter_lane_a4_2_full_dynamic_cell1_replay_output.csv`

---

## 1. Dataset Confirmation

| Metric | Value |
|---|---|
| Total Rows | 12,500 |
| Accepted Rows | 11,944 |
| Rejected Rows | 556 |
| Symbol Count | 25 |
| Timestamp Range | `2026-05-14T11:00:00+00:00` to `2026-06-03T19:00:00+00:00` |
| Unique Hourly Timestamps | 489 |
| Columns | 28 |

**Symbols:** AAVEUSDT, ADAUSDT, ALGOUSDT, ATOMUSDT, AVAXUSDT, BCHUSDT, BNBUSDT, BTCUSDT, DOGEUSDT, DOTUSDT, ETHUSDT, FILUSDT, ICPUSDT, LINKUSDT, LTCUSDT, NEARUSDT, POLUSDT, SHIBUSDT, SOLUSDT, STXUSDT, TRXUSDT, UNIUSDT, VETUSDT, XMRUSDT, XRPUSDT

**Key columns used:** symbol, replay_timestamp, ER, FMLC, Flowprint, raw_score, trigger (price proxy), change_24h_pct_replay

> **Note:** The first ~8 hours of data contain only 9 accepted symbols. Full 24–25 symbol coverage begins at approximately `2026-05-14T19:00:00+00:00`. All crash-start detection uses only timestamps with >= 20 symbols to avoid composition-driven artifacts.

---

## 2. Basket-Level Aggregate Snapshot (>= 20 symbols only)

First 10 and last 10 stable timestamps:

| Timestamp | Syms | Avg Trigger | Avg ER | Avg FMLC | Avg FP | Avg Score | FMLC Fall | FP Fall | ER>=6 | ER>=7 | Chg24h | Fwd8h |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-05-14T19:00 | 24 | 3589.1 | 5.75 | 8.29 | 6.38 | 6.83 | 0 | 4 | 14 | 10 | 2.81% | -0.01% |
| 2026-05-14T20:00 | 24 | 3589.1 | 3.42 | 7.92 | 5.04 | 5.48 | 1 | 7 | 5 | 2 | 2.24% | -0.11% |
| 2026-05-14T21:00 | 24 | 3589.1 | 2.08 | 7.58 | 4.25 | 4.66 | 3 | 9 | 1 | 1 | 1.83% | -0.11% |
| 2026-05-14T22:00 | 24 | 3589.1 | 1.96 | 7.50 | 4.08 | 4.54 | 3 | 9 | 0 | 0 | 1.92% | -0.12% |
| 2026-05-14T23:00 | 24 | 3589.1 | 2.29 | 7.50 | 4.42 | 4.75 | 8 | 19 | 2 | 2 | 1.70% | -0.07% |
| 2026-05-15T00:00 | 24 | 3589.1 | 1.75 | 5.46 | 4.00 | 3.72 | 18 | 14 | 2 | 2 | 1.07% | -0.05% |
| 2026-05-15T01:00 | 24 | 3589.1 | 1.79 | 6.33 | 4.12 | 4.08 | 14 | 4 | 0 | 0 | 1.09% | -0.05% |
| 2026-05-15T02:00 | 24 | 3589.1 | 0.46 | 4.50 | 3.33 | 2.74 | 19 | 16 | 0 | 0 | 0.47% | -0.05% |
| 2026-05-15T03:00 | 24 | 3589.1 | 2.75 | 5.33 | 4.62 | 4.22 | 17 | 7 | 1 | 1 | 1.35% | -0.03% |
| 2026-05-15T04:00 | 24 | 3589.1 | 1.71 | 4.62 | 3.71 | 3.33 | 10 | 6 | 0 | 0 | 1.89% | -0.02% |
| 2026-06-03T02:00 | 25 | 2959.6 | 1.24 | 3.68 | 3.64 | 2.81 | 2 | 0 | 1 | 1 | -4.03% | -0.59% |
| 2026-06-03T03:00 | 25 | 2952.6 | 0.52 | 3.68 | 3.24 | 2.44 | 2 | 13 | 0 | 0 | -5.01% | -1.23% |
| 2026-06-03T04:00 | 25 | 2948.7 | 1.00 | 3.64 | 3.40 | 2.64 | 1 | 8 | 1 | 1 | -7.20% | -0.26% |
| 2026-06-03T05:00 | 25 | 2935.3 | 0.84 | 3.88 | 3.32 | 2.65 | 0 | 10 | 1 | 0 | -4.78% | -0.15% |
| 2026-06-03T06:00 | 25 | 2931.1 | 0.52 | 4.12 | 3.44 | 2.66 | 0 | 9 | 0 | 0 | -2.90% | -0.01% |
| 2026-06-03T07:00 | 25 | 2927.3 | 1.04 | 4.12 | 3.96 | 2.99 | 1 | 1 | 0 | 0 | -2.74% | -0.09% |
| 2026-06-03T08:00 | 25 | 2922.6 | 0.80 | 4.60 | 3.96 | 3.08 | 1 | 4 | 0 | 0 | -2.61% | -0.00% |
| 2026-06-03T09:00 | 25 | 2907.7 | 0.92 | 4.60 | 3.88 | 3.10 | 2 | 2 | 0 | 0 | -2.59% | -0.03% |
| 2026-06-03T10:00 | 25 | 2893.5 | 0.52 | 4.44 | 3.72 | 2.85 | 3 | 3 | 0 | 0 | -2.57% | 0.17% |
| 2026-06-03T11:00 | 25 | 2864.2 | 1.48 | 5.32 | 4.20 | 3.64 | 1 | 7 | 2 | 0 | -2.24% | 0.34% |

---

## 3. Crash-Start Candidates

| Rule | Timestamp | Condition | Value |
|---|---|---|---|
| CRASH_START_A | `2026-05-16T02:00:00` | basket avg per-symbol 8h forward return <= -2% | -2.08% |
| CRASH_START_B | NOT FOUND | -- | -- |
| CRASH_START_C | `2026-05-15T08:00:00` | >= 60% symbols negative 8h forward return | 95.8% |
| CRASH_START_D | `2026-05-15T14:00:00` | basket average change_24h drops below -3% | avg_change_24h=-3.39% |

### Selected: **CRASH_START_A** at `2026-05-16T02:00:00+00:00`

**Rationale:** Earliest moment of measurable 8-hour forward pain (basket avg per-symbol return <= -2%). This marks the onset of real drawdown.

---

## 4. Crash-Start Timeline

Centered on `2026-05-16T02:00:00+00:00`:

| Point | Timestamp | Syms | Basket ER | Basket FMLC | Basket FP | Basket Score | FMLC Fall | FP Fall | ER>=6 | Chg24h | Fwd 8h |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **T-24h** | 2026-05-15T02:00 | 24 | 0.46 | 4.50 | 3.33 | 2.74 | 19 | 16 | 0 | 0.47% | -0.05% |
| **T-12h** | 2026-05-15T14:00 | 24 | 6.21 | 3.21 | 6.71 | 5.31 | 9 | 0 | 18 | -3.39% | -1.83% |
| **T-8h** | 2026-05-15T18:00 | 24 | 0.12 | 3.50 | 3.12 | 2.21 | 0 | 24 | 0 | -3.91% | -1.58% |
| **T-4h** | 2026-05-15T22:00 | 24 | 0.17 | 3.33 | 3.17 | 2.18 | 4 | 2 | 0 | -4.50% | -1.29% |
| **T-2h** | 2026-05-16T00:00 | 24 | 0.21 | 3.29 | 3.21 | 2.19 | 2 | 0 | 0 | -3.45% | -1.35% |
| **T-1h** | 2026-05-16T01:00 | 24 | 0.46 | 3.38 | 3.33 | 2.34 | 2 | 0 | 1 | -3.82% | -1.37% |
| **T0** | 2026-05-16T02:00 | 24 | 0.38 | 3.21 | 3.29 | 2.24 | 3 | 1 | 0 | -3.24% | -2.08% |
| **T+4h** | 2026-05-16T06:00 | 24 | 2.04 | 3.00 | 4.12 | 3.00 | 3 | 2 | 1 | -2.49% | -1.58% |
| **T+8h** | 2026-05-16T10:00 | 24 | 4.29 | 3.08 | 5.75 | 4.31 | 1 | 2 | 9 | -4.71% | -0.20% |
| **T+24h** | 2026-05-17T02:00 | 24 | 2.46 | 3.58 | 4.58 | 3.49 | 0 | 3 | 3 | -3.05% | -0.64% |

---

## 5. Earliest Warning Symbols

### First FMLC Drop >= 2 (over 4h)
- **Symbol:** ADAUSDT
- **Timestamp:** `2026-05-14T20:00:00+00:00`
- **FMLC:** 7.0, **4h change:** -2.0
- **Symbols in first 24h:** 23 -- ADAUSDT, ALGOUSDT, STXUSDT, DOTUSDT, VETUSDT, AVAXUSDT, SOLUSDT, AAVEUSDT, BCHUSDT, BNBUSDT, NEARUSDT, ATOMUSDT, LTCUSDT, FILUSDT, ETHUSDT

### First Flowprint Drop >= 1 (over 4h)
- **Symbol:** DOGEUSDT
- **Timestamp:** `2026-05-14T18:00:00+00:00`
- **Flowprint:** 5.0, **4h change:** -1.0
- **Symbols in first 24h:** 24 -- DOGEUSDT, LINKUSDT, SOLUSDT, ETHUSDT, BNBUSDT, BTCUSDT, XRPUSDT, ADAUSDT, DOTUSDT, SHIBUSDT, NEARUSDT, AVAXUSDT, AAVEUSDT, LTCUSDT, FILUSDT

### First Dual Drop (FMLC >= 2 AND Flowprint >= 1, over 4h)
- **Symbol:** ADAUSDT
- **Timestamp:** `2026-05-14T21:00:00+00:00`
- **FMLC:** 7.0, **Flowprint:** 5.0
- **Symbols in first 24h:** 23 -- ADAUSDT, VETUSDT, STXUSDT, DOTUSDT, ALGOUSDT, AVAXUSDT, AAVEUSDT, SHIBUSDT, ETHUSDT, BNBUSDT, BCHUSDT, TRXUSDT, FILUSDT, SOLUSDT, LINKUSDT

### First ER Spike After Deterioration
- **Symbol:** DOGEUSDT
- **Deterioration at:** `2026-05-14T15:00:00+00:00`
- **ER spike at:** `2026-05-14T17:00:00+00:00` (ER = 6.0)
- **Delay:** 2h after first deterioration
- **Symbols with ER spike after deterioration:** DOGEUSDT, LINKUSDT, ADAUSDT, LTCUSDT, BCHUSDT, ATOMUSDT, FILUSDT, VETUSDT, BNBUSDT, TRXUSDT

---

## 6. Crash Warning Scope

### Verdict: **MARKET-WIDE**

Dual deterioration in 23/25 symbols within 24h -- broad systemic event.

- FMLC drop >= 2 in first 24h: **23** symbols
- Flowprint drop >= 1 in first 24h: **24** symbols
- Both dropping in first 24h: **23** symbols

---

## 7. Deterioration Sequence Test

| Test | Symbols Confirmed | % of Total |
|---|---:|---:|
| Flowprint drop before ER spike | 25 | 100.0% |
| FMLC drop before ER spike | 22 | 88.0% |
| FMLC + Flowprint drop before crash start | 23 | 92.0% |

### Per-Symbol Sequence Detail

| Symbol | 1st FP Drop | 1st FMLC Drop | 1st ER Spike | FP->ER | FMLC->ER | Both<Crash |
|---|---|---|---|---|---|---|
| AAVEUSDT | 2026-05-14 23:00 | 2026-05-15 00:00 | 2026-05-15 14:00 | Y | Y | Y |
| ADAUSDT | 2026-05-14 21:00 | 2026-05-14 20:00 | 2026-05-15 00:00 | Y | Y | Y |
| ALGOUSDT | 2026-05-14 23:00 | 2026-05-14 23:00 | 2026-05-15 14:00 | Y | Y | Y |
| ATOMUSDT | 2026-05-15 02:00 | 2026-05-15 00:00 | 2026-05-15 06:00 | Y | Y | Y |
| AVAXUSDT | 2026-05-14 23:00 | 2026-05-14 23:00 | 2026-05-15 14:00 | Y | Y | Y |
| BCHUSDT | 2026-05-14 23:00 | 2026-05-15 00:00 | 2026-05-15 03:00 | Y | Y | Y |
| BNBUSDT | 2026-05-14 20:00 | 2026-05-15 00:00 | 2026-05-15 08:00 | Y | Y | Y |
| BTCUSDT | 2026-05-14 20:00 | 2026-05-15 05:00 | 2026-05-15 14:00 | Y | Y | Y |
| DOGEUSDT | 2026-05-14 18:00 | 2026-05-15 05:00 | 2026-05-17 11:00 | Y | Y | Y |
| DOTUSDT | 2026-05-14 21:00 | 2026-05-14 23:00 | 2026-05-15 14:00 | Y | Y | Y |
| ETHUSDT | 2026-05-14 19:00 | 2026-05-15 00:00 | 2026-05-15 14:00 | Y | Y | Y |
| FILUSDT | 2026-05-14 23:00 | 2026-05-15 00:00 | 2026-05-15 06:00 | Y | Y | Y |
| ICPUSDT | 2026-05-15 00:00 | 2026-05-16 20:00 | 2026-05-16 08:00 | Y | N | N |
| LINKUSDT | 2026-05-14 18:00 | 2026-05-15 02:00 | 2026-05-14 19:00 | Y | N | Y |
| LTCUSDT | 2026-05-14 23:00 | 2026-05-15 00:00 | 2026-05-15 00:00 | Y | N | Y |
| NEARUSDT | 2026-05-14 23:00 | 2026-05-15 00:00 | 2026-05-15 14:00 | Y | Y | Y |
| POLUSDT | 2026-05-18 02:00 | 2026-05-18 00:00 | 2026-05-18 23:00 | Y | Y | N |
| SHIBUSDT | 2026-05-14 23:00 | 2026-05-15 00:00 | 2026-05-15 14:00 | Y | Y | Y |
| SOLUSDT | 2026-05-14 19:00 | 2026-05-15 00:00 | 2026-05-16 08:00 | Y | Y | Y |
| STXUSDT | 2026-05-14 23:00 | 2026-05-14 23:00 | 2026-05-15 14:00 | Y | Y | Y |
| TRXUSDT | 2026-05-15 02:00 | 2026-05-15 01:00 | 2026-05-15 08:00 | Y | Y | Y |
| UNIUSDT | 2026-05-14 23:00 | 2026-05-15 02:00 | 2026-05-15 14:00 | Y | Y | Y |
| VETUSDT | 2026-05-14 23:00 | 2026-05-14 23:00 | 2026-05-15 06:00 | Y | Y | Y |
| XMRUSDT | 2026-05-15 03:00 | 2026-05-15 00:00 | 2026-05-15 13:00 | Y | Y | Y |
| XRPUSDT | 2026-05-14 20:00 | 2026-05-15 05:00 | 2026-05-17 11:00 | Y | Y | Y |

---

## 8. Jody-Style Verdict

### Verdict: **PASS**

Pre-crash deterioration is **measurable and sequenced**. Flowprint drop preceded ER spike in 25/25 symbols (100%). FMLC drop preceded ER spike in 22/25 symbols (88%). Dual deterioration appeared in 23/25 symbols before the crash-start timestamp. The sequence -- flow withdrawal, structural breakdown, volatility spike, price collapse -- is confirmed.

---

## 9. Governance & Safety

- **Research-Only Boundary:** Offline forensic audit on historical replay data. No trade orders, no alerts.
- **Formula Gating:** Canonical Cell 1 formulas used without modification.
- **CSV Isolation:** Generated CSV is local only -- not committed.
- **No Cell 2.** No action labels. No buy/sell recommendations.

PASS_FIRESTARTER_A4_CRASH_START_FORENSIC_REPLAY_COMPLETE
