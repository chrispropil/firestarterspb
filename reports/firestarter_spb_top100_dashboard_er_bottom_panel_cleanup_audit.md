# Firestarter SPB: Top 100 Dashboard — ER Bottom Panel + White Price Line Cleanup Audit

**Date:** 2026-06-07  
**Branch:** main  
**Script:** `scripts/visualization/build_top100_clean_html_dashboard.py`  
**Approval basis:** Chris visual review directives (session 2026-06-07 18:06 ET)

---

## 1. Phase Checklist

### Phase 1 — Chart Structure

| Check | Status |
|---|---|
| **Price line is white** | YES — `color: '#ffffff'`, `width: 1.4` |
| **ER removed from price overlay** | YES — ER no longer uses `overlaying: 'y'` on the price axis |
| **ER in own panel directly below price** | YES — `yaxis2`, domain `[0.43, 0.60]` |
| **ER uses bar/vertical style** | YES — Plotly `type: 'bar'` with amber gradient colouring (opacity stepped by score band) |
| **ER y-axis fixed 0–10** | YES — `range: [0, 10]`, `fixedrange: true` |
| **ER axis label** | YES — `'ER  (0–10)'` + panel annotation: `ER — Expansion Readiness | bars | 0–10` |
| **Bottom volume panel removed** | YES — `traceVolume` deleted; `volumeArr` not loaded in JS |
| **Volume % panel/trace removed** | YES — no volume % trace anywhere in script |
| **SMA 20 removed** | YES — already removed in prior session; confirmed absent from script |
| **SMA 50 removed** | YES — already removed in prior session; `_ema_50` is internal-only (never charted) |
| **No SMA legend entries** | YES — confirmed |
| **FMLC / Flowprint / raw_score** | Retained in `yaxis3` panel below ER, domain `[0.22, 0.39]`, fixed range 0–10 |
| **Range % / Rolling Vol %** | Retained in `yaxis4` panel at bottom, domain `[0.0, 0.18]` |
| **Static top metadata preserved** | YES — symbol, row count, first/last timestamp, missing candles, formula status unchanged |

---

### Phase 2 — Panel Layout (top → bottom)

| Panel | Content | Y-Domain | Y-Range |
|---|---|---|---|
| 1 — Price | White price line only | `[0.64, 1.0]` | Auto (price) |
| 2 — ER | Amber vertical bars | `[0.43, 0.60]` | Fixed `0–10` |
| 3 — Metrics | FMLC / Flowprint_proxy / raw_score lines | `[0.22, 0.39]` | Fixed `0–10` |
| 4 — Volatility | Range % + Rolling Vol % lines | `[0.0, 0.18]` | Auto |

---

### Phase 3 — Symbol Pages Regenerated

- **Total symbol pages regenerated:** 100 / 100
- **BTCUSDT page generated:** YES — `reports/html/top100_dashboard/symbols/BTCUSDT.html`
- **ETHUSDT page generated:** YES — `reports/html/top100_dashboard/symbols/ETHUSDT.html`
- **Nonstandard Unicode pages generated:** YES — `币安人生USDT`, `龙虾USDT`
- **Dashboard index regenerated:** YES — `reports/html/top100_dashboard/index.html`

---

### Phase 4 — Boundaries

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
| No formulas invented | YES — only Chris-approved sandbox defaults applied |

---

## 2. Files Updated

| File | Change |
|---|---|
| `scripts/visualization/build_top100_clean_html_dashboard.py` | JS chart block rewritten: white price, ER bar panel, no volume, no SMA |
| `reports/html/top100_dashboard/index.html` | Regenerated |
| `reports/html/top100_dashboard/symbols/*.html` | All 100 symbol pages regenerated |
| `reports/firestarter_spb_top100_dashboard_er_bottom_panel_cleanup_audit.md` | This file — new |

---

## 3. STOP GATES — All Clear

| Gate | Status |
|---|---|
| Dashboard generation failed | NOT TRIGGERED |
| Symbol pages < 100 | NOT TRIGGERED (100/100) |
| Raw data committed | NOT TRIGGERED |
| ER remains overlaid on price | NOT TRIGGERED — ER is in own separate bar panel |
| Bottom volume panel remains | NOT TRIGGERED — volume panel fully removed |
| SMA traces remain | NOT TRIGGERED |
| Cell 2 / labels / training / trading logic | NOT TRIGGERED |
| Recommendation language | NOT TRIGGERED |
