# Firestarter SPB: Multi-Symbol HTML Viewer Audit

## Overview
This document records the programmatic verification and file structure audit for the standalone multi-symbol local HTML review system built for the Binance Top 100 USDT perpetual dataset.

## 1. File Count & Generation Summary
- **Symbol Index Created:** YES (`reports/html/firestarter_spb_top100_symbol_index.html`)
- **Symbol Directory Created:** YES (`reports/html/top100_symbols/`)
- **Total Symbol Pages Generated:** 100 / 100
- **BTCUSDT Page Created:** YES
- **ETHUSDT Page Created:** YES
- **Non-Standard Symbols Generated:** 2 (币安人生USDT, 龙虾USDT)

## 2. Layout & Styling Checklist
- **Vertical Chart Layout:** Verified.
  1. Price chart on top.
  2. Color-coded Volume bars.
  3. High-Low range %.
  4. 20-period rolling volatility.
- **Exact-Number Data Tables:** Verified. Includes:
  - 20-row preview of 5m klines.
  - resampled 1-hour summary stats.
  - resampled 4-hour summary stats.
- **Index Back Links:** All symbol files contain a valid index back-reference.
- **Notice Banner:** Added:
  *“Firestarter metric panels not enabled yet. Current viewer shows raw OHLCV-derived panels only.”*

## 3. Boundary compliance
- **No Data Commit:** Verified. Local CSV files remain unversioned.
- **No ML/Trading Logic:** Notebook contains no Cell 2, target labels, or predictive parameters.
