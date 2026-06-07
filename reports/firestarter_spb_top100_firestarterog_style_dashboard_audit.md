# Firestarter SPB: Top 100 FirestarterOG-Style Dashboard Audit

## Overview
This document audits the design, layout, and compilation metrics for the local Top 100 HTML dashboard, which has been rebuilt to match the visual features and interactive capabilities of the original FirestarterOG local research viewer.

## 1. Dashboard Structure and Layout
- **Design Inspiration:** Sourced strictly from the styling and structure of `reports/firestarterog_binance_1m_local_viewer.html`.
- **Interactive Capabilities:** Integrates Plotly client-side interactive rendering for high-resolution navigation:
  - Synchronized zoom across price, volume, range, and volatility panels.
  - Multi-panel stacked grid chart (Price + trend overlays, Volume bars, Range % spread, Rolling Vol % returns).
  - Hover readout container dynamically displaying timestamp metrics (`[UTC TIME] // Price // Volume // Spread // Volatility`).
- **Easy Symbol Switching:** Every symbol detail page contains a `<select>` dropdown populated with all 100 symbols, enabling fast client-side redirection.
- **Exact-Number Data Tables:** Features three distinct HTML summary tables beneath the chart card:
  - 20-row preview of raw 5m klines.
  - resampled 1-hour statistics summary.
  - resampled 4-hour statistics summary.

## 2. Directory Verification
- **Dashboard Index:** `reports/html/top100_dashboard/index.html` (Created)
- **Symbol Detail Folder:** `reports/html/top100_dashboard/symbols/` (Created)
- **Symbol Pages Created:** 100 / 100 (Created)
- **BTCUSDT Page:** `reports/html/top100_dashboard/symbols/BTCUSDT.html` (Created)
- **ETHUSDT Page:** `reports/html/top100_dashboard/symbols/ETHUSDT.html` (Created)
- **Non-Standard symbols:** 2 (币安人生USDT, 龙虾USDT) (Created)

## 3. Boundaries and Policies
- **No Old Raw Data Copied:** Checked. No telemetry from the old FirestarterOG viewer was duplicated.
- **No Raw CSV/JSON committed:** Checked. Dataset files remain unversioned.
- **No ML/Trading/Recommendations:** Checked. Standard disclaimer added:
  *“Firestarter metric panels (ER/FMLC/Flowprint) not enabled yet. Current viewer shows raw OHLCV-derived panels only.”*
