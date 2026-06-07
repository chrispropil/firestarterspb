# Firestarter SPB: Top 100 Dashboard V3 Firestarter Metric Source Review

## Overview
This document audits and locks the approved Firestarter-style metric sources for the Top 100 V3 dashboard rebuild.

## 1. Reports Inspected
The following Cell 1 formula/reconstruction reports in the repository were read and analyzed:
1. [firestarter_spb_binance_5_token_formula_spec_confirmation.md](file:///C:/firestarterspb/reports/firestarter_spb_binance_5_token_formula_spec_confirmation.md)
2. [firestarter_spb_binance_5_token_cell1_computation_plan.md](file:///C:/firestarterspb/reports/firestarter_spb_binance_5_token_cell1_computation_plan.md)

## 2. Approved Metrics & Formulas Available
The ancestor summary specifications outline the following metric structure components:
- **ER (Ignition/Momentum Pressure):** RVOL 1H, RVOL 4H window, 24h change ranges, near_breakout, clean_reclaim, clamped 0-10.
- **FMLC (Anti-Blowoff Governor):** Liquidity floor, 4H range position, 20-bar range position, clean_reclaim, above_4h_trend, anti-blowoff governor, clamped 0-10.
- **Flowprint-proxy (Participation Proxy):** RVOL 1H, RVOL 4H window, OI presence, funding band quality, close above EMA21, near_breakout, clamped 0-8.
- **raw_score:** `raw_score = ER * 0.35 + FMLC * 0.35 + Flowprint * 0.30`

## 3. Ambiguities & Blockers (Specification Gaps)
As documented in the Cell 1 spec confirmation reports, the following executable details are missing:
- Exact RVOL thresholds, point allocation tables, and lookback windows for ER/Flowprint.
- Exact range-position formulas, liquidity floors, and trend/reclaim thresholds for FMLC.
- Clamp/reject policies and null handling rules for out-of-bounds metrics.
- Gating and fallback behavior when partial Open Interest (OI) or top-trader data is unavailable.

## 4. Computation Status
- **Metric Computation Allowed in this Build:** NO.
- **Reason:** An approved executable formula spec has not been finalized (gated by `HOLD_SPB_FORMULA_COMPUTATION_PENDING_EXECUTABLE_SPEC`).
- **Dashboard Action:** Standardized placeholder panels will be rendered in the charts and top summaries, labeled clearly as `NOT ENABLED — formula gate required` to avoid inventing metric rules.
