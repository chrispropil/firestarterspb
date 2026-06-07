# Firestarter SPB: Top 100 Dashboard — Main Chart Firestarter Metric Overlay Audit

**Date:** 2026-06-07  
**Branch:** main  
**Script:** `scripts/visualization/build_top100_clean_html_dashboard.py`  
**Approval basis:** Chris visual review directives (session 2026-06-07 18:22 ET)

---

## 1. Phase Checklist

### Phase 1 — Axis Restructure

| Check | Status |
|---|---|
| **Price moved to RIGHT y-axis** | YES — `yaxis2`, `side: 'right'`, `overlaying: 'y'`, `showgrid: false` |
| **Price line is white** | YES — `color: '#ffffff'`, `width: 1.5` |
| **LEFT y-axis = Firestarter Metrics** | YES — `yaxis`, `title: 'Firestarter Metrics'`, `range: [0, 10]`, `side: 'left'` |
| **FMLC moved to main chart** | YES — `traceFMLC` on `yaxis: 'y'` (LEFT, 0–10 scale) |
| **Flowprint_proxy moved to main chart** | YES — `traceFlowprint` on `yaxis: 'y'` (LEFT, 0–10 scale) |
| **raw_score moved to main chart** | YES — `traceRawScore` on `yaxis: 'y'` (LEFT, 0–10 scale) |
| **Bottom Firestarter graph removed** | YES — the yaxis3 FMLC/FP/Score panel from previous build is fully removed |
| **No SMA 20** | YES — confirmed absent |
| **No SMA 50** | YES — confirmed absent |
| **Volume % removed** | YES — no vol% trace |
| **Volume bars removed** | YES — `traceVolume` deleted; `volume` not loaded in JS |

---

### Phase 2 — FMLC Styling

| Property | Value |
|---|---|
| Type | `scatter`, `mode: 'lines'` |
| Color | `rgba(239,68,68,0.82)` — muted red |
| Line width | 1.2 |
| Axis | LEFT (`yaxis: 'y'`) |
| Range | 0–10 (fixed left axis) |
| Styling | Professional, muted; no neon |

---

### Phase 3 — Flowprint Styling

| Property | Value |
|---|---|
| Type | `scatter`, `mode: 'lines'` |
| Color | `rgba(52,211,153,0.55)` — light green, 55% opacity |
| Line width | 0.9 (very thin) |
| Markers | None |
| Axis | LEFT (`yaxis: 'y'`) |

---

### Phase 4 — raw_score Styling

| Property | Value |
|---|---|
| Type | `scatter`, `mode: 'markers'` |
| Color | `rgba(167,139,250,0.78)` — purple |
| Marker size | 3.5 |
| No connecting line | YES — `mode: 'markers'` only |
| Label in legend | `Score` |
| Axis | LEFT (`yaxis: 'y'`) |

---

### Phase 5 — Panel Layout (top → bottom)

| Panel | Content | Y-Domain | Y-Range |
|---|---|---|---|
| **Main chart** | White price (RIGHT) + FMLC/Flowprint/Score (LEFT) | `[0.44, 1.0]` | LEFT: 0–10 fixed; RIGHT: auto (price) |
| **ER panel** | Amber vertical bars | `[0.24, 0.40]` | Fixed `0–10` |
| **Range / Vol % panel** | Range % + Rolling Vol % lines | `[0.0, 0.20]` | Auto |

**Bottom Firestarter graph removed:** YES — the dedicated yaxis3 metric panel (FMLC/FP/Score) that existed in the previous build is gone. These traces are now in the main chart.

---

### Phase 6 — Top Output Cards

Four compact cards rendered side-by-side in a `flex` row, directly below the metadata grid:

| Card | Label | Color | Value source |
|---|---|---|---|
| ER | ER — Expansion Readiness | Amber `#f59e0b` | Last non-null `er` value from 1H resampled series |
| FMLC | FMLC — Momentum / Liquidity | Red `#ef4444` | Last non-null `fmlc` value |
| Flowprint proxy | Flowprint proxy | Green `#34d399` | Last non-null `flowprint` value |
| raw_score | raw_score — blended | Purple `#a78bfa` | Last non-null `raw_score` value |

Card properties:
- Monospaced number font (Consolas/Menlo)
- 20px bold value display
- Dark background `#0e1014`, `1px solid #1e222b` border
- No sticky/floating — static HTML position
- Values computed per-symbol from `df_merged` before HTML generation

---

### Phase 7 — Symbol Pages Regenerated

- **Total symbol pages regenerated:** 100 / 100
- **BTCUSDT page generated:** YES
- **ETHUSDT page generated:** YES
- **Nonstandard Unicode pages:** YES — `币安人生USDT`, `龙虾USDT`
- **Dashboard index regenerated:** YES — `reports/html/top100_dashboard/index.html`
- **Static metadata preserved:** YES — symbol, row count, first/last timestamps, missing candles, formula status

---

### Phase 8 — Boundaries

| Boundary | Status |
|---|---|
| No raw CSV/JSON committed | YES |
| No full raw dataset embedded in HTML | YES |
| No Cell 2 | YES |
| No labels | YES |
| No model training | YES |
| No trading logic | YES |
| No recommendations | YES |
| No strategy performance claims | YES |
| No secrets or credentials | YES |
| No formulas invented | YES — only Chris-approved sandbox defaults |

---

## 2. Files Updated

| File | Change |
|---|---|
| `scripts/visualization/build_top100_clean_html_dashboard.py` | Full chart axis restructure; metric cards CSS + HTML injected; volume removed from payload |
| `reports/html/top100_dashboard/index.html` | Regenerated |
| `reports/html/top100_dashboard/symbols/*.html` | All 100 regenerated with new chart layout and metric cards |
| `reports/firestarter_spb_top100_dashboard_main_chart_metric_overlay_audit.md` | This file — new |

---

## 3. STOP GATES — All Clear

| Gate | Status |
|---|---|
| Dashboard generation failed | NOT TRIGGERED |
| Symbol pages < 100 | NOT TRIGGERED (100/100) |
| Raw data committed | NOT TRIGGERED |
| Price remained on left axis | NOT TRIGGERED — price on RIGHT |
| FMLC/Flowprint/Score not on main chart | NOT TRIGGERED — all three on main chart LEFT axis |
| Bottom Firestarter graph remains | NOT TRIGGERED — removed |
| Cell 2 / labels / training / trading logic | NOT TRIGGERED |
| Recommendation language | NOT TRIGGERED |
