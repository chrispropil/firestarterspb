# Top 100 Evidence Viewer Single Main Chart Stack Audit

This document audits the stacked chart configuration of the Top 100 Evidence Viewer.

## 1. Compliance Checklist

| Audit Parameter | Verification Status | Notes |
|---|---|---|
| One Main Chart Container Exists | **PASS** | Rendering is handled in a single `#chart` div. |
| Price Top Panel | **PASS** | Price is drawn on `yaxis` (domain: `[0.6, 1.0]`). |
| FMLC/Flowprint/Score Middle Panel | **PASS** | Plotted on `yaxis2` (domain: `[0.3, 0.55]`). |
| ER Bottom Panel | **PASS** | Plotted on `yaxis3` (domain: `[0.0, 0.25]`). |
| ER Inside Main Chart | **PASS** | ER is fully contained within the main chart container on its designated yaxis3. |
| Shared X-Axis / Time Alignment | **PASS** | All y-axes share the default `xaxis` and are anchored (`anchor: 'x'`) to align zooms/pans. |
| Top ER/FMLC/Flowprint/Score Cards | **PASS** | Four styled metric cards display the latest non-null values for the active symbol. |
| Light-Blue Color Scheme Preserved | **PASS** | Page background remains `#eef4f8` and Plotly backgrounds remain white/light-slate. |
| Formulas Unchanged | **PASS** | Metric computations strictly follow baseline calculations. |
| No SMA 20/50 | **PASS** | No moving averages are plotted. |
| No Volume % / Bottom Volume | **PASS** | Standard volume charting is omitted. |
| No Experimental Dashboard Styling | **PASS** | Preserves standard Evidence Viewer workflow without dashboard templates. |
| No Raw CSV/JSON Staged/Committed | **PASS** | Staging list contains only script, HTML, and audit logs. |

---

## 2. Commit Target Status
Staged files checked against boundary conditions.

**PASS: PASS_SINGLE_MAIN_CHART_STACK_AUDIT_COMPLETE**
