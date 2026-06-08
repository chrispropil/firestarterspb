# Top 100 Evidence Viewer Cell 1 Formula Numeric Audit

This report validates the numerical correctness of the Cell 1 formula calculations applied in the Top 100 Evidence Viewer.

## 1. Audit Scope & Sources
- **Viewer Script:** `scripts/visualization/build_top100_evidence_viewer.py`
- **Data Directory:** `C:/firestarterspb/data/research/binance_top100_excluding_existing_5_1month`
- **Derivatives Directory:** `C:/firestarterspb/data/research/binance_top100_derivatives_context_1month`

## 2. Validation Symbol Table

| Symbol | Metric | Latest Value | Min | Max | Null Count | Clamp Pass | Recomp Pass |
|---|---|---|---|---|---|---|---|
| BTCUSDT | ER | 1.0000 | 0.0000 | 10.0000 | 23 | PASS | PASS |
| | FMLC | 3.5164 | 2.0087 | 9.3917 | 199 | PASS | |
| | Flowprint_proxy | N/A | 2.0000 | 8.0000 | 32 | PASS | |
| | RAW_SCORE | N/A | 1.5246 | 8.8805 | 201 | PASS | |
| | | | | | | | |
| ETHUSDT | ER | 1.0000 | 0.0000 | 10.0000 | 23 | PASS | PASS |
| | FMLC | 7.1260 | 2.0535 | 9.0051 | 199 | PASS | |
| | Flowprint_proxy | N/A | 0.0000 | 7.0000 | 32 | PASS | |
| | RAW_SCORE | N/A | 1.6041 | 8.9457 | 201 | PASS | |
| | | | | | | | |
| BNBUSDT | ER | 1.0000 | 0.0000 | 10.0000 | 23 | PASS | PASS |
| | FMLC | 7.2275 | 1.7192 | 9.9770 | 199 | PASS | |
| | Flowprint_proxy | N/A | 2.0000 | 8.0000 | 32 | PASS | |
| | RAW_SCORE | N/A | 1.6027 | 9.6191 | 201 | PASS | |
| | | | | | | | |
| HYPEUSDT | ER | 0.0000 | 0.0000 | 10.0000 | 23 | PASS | PASS |
| | FMLC | 3.4620 | 0.0000 | 9.9781 | 199 | PASS | |
| | Flowprint_proxy | N/A | 0.0000 | 8.0000 | 32 | PASS | |
| | RAW_SCORE | N/A | 1.3298 | 9.5901 | 201 | PASS | |
| | | | | | | | |
| ZECUSDT | ER | 0.0000 | 0.0000 | 10.0000 | 23 | PASS | PASS |
| | FMLC | 3.4951 | 0.0000 | 9.8241 | 199 | PASS | |
| | Flowprint_proxy | N/A | 0.0000 | 8.0000 | 32 | PASS | |
| | RAW_SCORE | N/A | 0.1675 | 9.2556 | 201 | PASS | |
| | | | | | | | |

## 3. Formula Implementation Verification Details

### ER Calculation
- **RVOL average lookback:** 24h rolling average. Threshold points match lock sheet specifications (Max 4 points).
- **Breakout logic:** Close within 1% of 20-bar high gets 3 points; within 2.5% gets 1 point.
- **Clean reclaim:** Close above EMA21 with volume > 1.2x average gets 3 points.
- **Clamp & Gating:** Score clamped cleanly between 0 and 10. Missing-data handling confirmed (returns NaN when parents are missing).

### FMLC Calculation
- **Liquidity Floor:** Daily rolling volume < $10,000,000 gates FMLC to 0 points.
- **Range Position:** Composite of 50-bar (200-bar 1H) and 20-bar range position (Max 5 points).
- **Trend/Reclaim:** Close above EMA50 gets 3 points; below EMA50 but above EMA21 gets 1 point.
- **Anti-Blowoff:** penalized by 4 points if rolling 24h change exceeds +/-15%.
- **Clamp & Gating:** Score clamped cleanly between 0 and 10. Missing-data handling confirmed.

### Flowprint_proxy Calculation
- **Inputs:** Uses open interest change, funding rate, taker buy/sell ratio (buySellRatio), and relative volume.
- **Clamp & Gating:** Clamped between 0 and 8 inclusive. Missing-data handling confirmed.

### Raw Score Blend Verification
- **Formula:** `raw_score = ER * 0.35 + FMLC * 0.35 + Flowprint_proxy * 0.30`
- **Normalization:** Divided by `0.94` to scale back to 0-10 range.
- **Recomputation Check:** All validation symbols achieved 100% mathematical parity (zero delta deviation) between stored `raw_score` and recomputed score.

## 4. Decision
**PASS_CELL1_NUMBERS_CONFIRMED**
