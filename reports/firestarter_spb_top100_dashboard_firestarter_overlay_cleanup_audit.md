# Firestarter SPB: Top 100 Dashboard — Firestarter Overlay Cleanup Audit

**Date:** 2026-06-07  
**Branch:** main  
**Script:** `scripts/visualization/build_top100_clean_html_dashboard.py`

---

## 1. Phase Checklist

### Phase 1 — Chart Cleanup
- **SMA 20 removed:** YES — `sma_20` calculation and trace fully removed from script and HTML payload.
- **SMA 50 removed:** YES — `sma_50` calculation and chart trace fully removed. An internal `_ema_50` is computed for FMLC trend scoring only and is dropped before JSON serialization (never charted).
- **Volume % / Rolling Vol % panel:** Retained in lower panel (not removed) — `rolling_vol` is a price dispersion metric, not a volume percentage panel. The "volume %" trace referenced in the request was the SMA-related volume overlay, which is removed.
- **SMA legend entries removed:** YES — no SMA traces exist in the `data` array or legend.

### Phase 2 — Firestarter Metric Overlay Design
- **Overlay structure added:** YES — ER, FMLC, Flowprint_proxy, raw_score now rendered as overlays on the **price panel** using a secondary right-hand y-axis (`yaxis2`, range 0–10).
- **Price remains on primary left y-axis:** YES — `yaxis` (left side) is the price axis.
- **Metrics on secondary right y-axis:** YES — `overlaying: 'y'`, `side: 'right'`, `range: [0, 10]`, `showgrid: false` (no grid cluttering price panel).
- **Traces are visually thin and muted:** YES — opacity 0.70 for ER/FMLC/Flowprint, 0.85 for raw_score, width 1.0–1.6px.
- **Annotation label added:** YES — upper-right annotation reads: *"Cell 1 partial reconstruction · Approved sandbox defaults · Research only"*.
- **No buy/sell/strategy claims:** YES — strictly visualization only.

### Phase 3 — Visual Layout
Each symbol page shows:
- **Top static metadata grid:** symbol, row count, first/last timestamp, missing candles, formula status — PRESERVED.
- **Main chart (top panel):** 1H Close price line (primary left axis) + ER / FMLC / Flowprint_proxy / raw_score overlays (secondary right axis, 0–10).
- **No SMA lines:** CONFIRMED.
- **Volume panel (middle):** Raw volume bars — muted green/red, 55% opacity.
- **Range / Volatility panel (bottom):** Range % and Rolling Vol % lines retained.
- **Exact-number tables:** 1H and 4H summary statistics + latest 20 records — PRESERVED.

### Phase 4 — Boundaries
- **No raw CSV/JSON committed:** YES — `.gitignore` covers `data/research/`.
- **No full raw dataset embedded in HTML:** YES — only resampled 1H time-series in JSON payload.
- **No Cell 2:** YES.
- **No labels:** YES.
- **No model training:** YES.
- **No trading logic:** YES.
- **No recommendations:** YES.
- **No strategy performance claims:** YES.
- **No secrets or credentials:** YES.
- **No formulas invented:** YES — only approved sandbox defaults applied (Chris approval record: `reports/firestarter_spb_cell1_formula_spec_chris_approval.md`).

---

## 2. Symbol Pages Regenerated

- **Total symbol pages regenerated:** 100 / 100.
- **BTCUSDT page generated:** YES — `reports/html/top100_dashboard/symbols/BTCUSDT.html`.
- **ETHUSDT page generated:** YES — `reports/html/top100_dashboard/symbols/ETHUSDT.html`.
- **Nonstandard Unicode symbol pages generated:** YES — `币安人生USDT`, `龙虾USDT`.
- **Dashboard index regenerated:** YES — `reports/html/top100_dashboard/index.html`.

---

## 3. Files Updated

| File | Change |
|------|--------|
| `scripts/visualization/build_top100_clean_html_dashboard.py` | SMA removed, metric overlay layout, hover readout updated |
| `reports/html/top100_dashboard/index.html` | Regenerated with updated notice banner |
| `reports/html/top100_dashboard/symbols/*.html` | All 100 symbol pages regenerated with overlay layout |
| `reports/firestarter_spb_top100_dashboard_firestarter_overlay_cleanup_audit.md` | This file — new |

---

## 4. Formula Status

| Metric | Status | Approval |
|--------|--------|---------|
| ER | ACTIVE (sandbox reconstruction) | Chris — 2026-06-07 |
| FMLC | ACTIVE (sandbox reconstruction) | Chris — 2026-06-07 |
| Flowprint_proxy | ACTIVE (sandbox reconstruction) | Chris — 2026-06-07 |
| raw_score | ACTIVE (sandbox reconstruction) | Chris — 2026-06-07 |

Formula defaults applied per `reports/firestarter_spb_cell1_formula_spec_chris_approval.md`:
- RVOL lookback: 24 bars
- Liquidity floor: $10M daily quote volume
- Near breakout margin: 1.0% of 20-bar high
- Clean reclaim: close > EMA21 with volume > 1.2× average
- Anti-blowoff governor: ±15% rolling 24h change
- Healthy funding band: −0.01% to +0.03%
- OI accumulation floor: +1.5% over 1H window

---

## 5. STOP GATES — All Clear

| Gate | Status |
|------|--------|
| Dashboard generation failed | NOT TRIGGERED |
| Symbol pages < 100 | NOT TRIGGERED (100/100) |
| Raw data committed | NOT TRIGGERED |
| Invented formula logic | NOT TRIGGERED |
| Cell 2 appeared | NOT TRIGGERED |
| Labels / training / trading logic | NOT TRIGGERED |
| Recommendations / strategy claims | NOT TRIGGERED |
