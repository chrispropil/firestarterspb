# Top 100 Evidence Viewer One-Screen Stacked Recovery Audit

This document audits the layout and configurations of the compact one-screen vertically stacked Top 100 Evidence Viewer.

## 1. Compliance Checklist

| Audit Parameter | Verification Status | Notes |
|---|---|---|
| Bad Side-by-Side Layout Removed | **PASS** | Visual layouts are fully stacked vertically. No side-by-side elements. |
| CSS-Grid Chart Split Removed | **PASS** | Layout uses a single, unified main `#chart` Plotly container. |
| Focus Mode Removed | **PASS** | Focus Mode and HUD toggles are completely absent. |
| Floating HUD Removed | **PASS** | No floating UI elements are configured. |
| One Main Plotly Container | **PASS** | A single `#chart` container handles all panels. |
| Three Stacked Panels Restored | **PASS** | Price, Metrics, and ER are stacked vertically inside the container. |
| Price Top Panel | **PASS** | Plotted at the top using yaxis domain `[0.58, 1.00]`. |
| FMLC/Flowprint/Score Middle Panel | **PASS** | Plotted in the middle using yaxis2 domain `[0.28, 0.54]`. |
| ER Bottom Panel | **PASS** | Plotted at the bottom using yaxis3 domain `[0.00, 0.22]`. |
| ER Y-Axis Restored to 0–10 | **PASS** | Y-axis range is set to fixed `[0, 10]`. |
| Chart Height Reduced to One-Screen | **PASS** | Main chart container height is restricted to `820px` to fit on one screen. |
| Time Buttons Preserved | **PASS** | 1D, 3D, 6D, and Full controls are available. |
| Default 3D View | **PASS** | Default time window set to 3D. |
| Cursor Readouts Preserved | **PASS** | Enlarged dynamic cursor readout boxes are present. |
| Candlesticks Preserved | **PASS** | OHLC candlesticks are plotted over the white price line in Panel 1. |
| Light-Blue Theme Preserved | **PASS** | Outer theme is light-blue `#eef4f8`. |
| Dark Grey Backdrop Preserved | **PASS** | Chart areas use dark grey `#18181b` plot backgrounds. |
| Formulas Unchanged | **PASS** | Metric computations remain completely unaltered. |
| No Raw Data Committed | **PASS** | Staged files do not include raw research datasets. |
| No Cell 2 / Action Labels | **PASS** | No model training, execution rules, or labels are introduced. |

---

## 2. Layout Specifications
- **Total Chart Height:** 820px
- **Price Domain:** `[0.58, 1.00]`
- **Metrics Domain:** `[0.28, 0.54]`
- **ER Domain:** `[0.00, 0.22]`
- **ER Range:** `[0, 10]`

**STATUS: Successful One-Screen Stacked Recovery**
