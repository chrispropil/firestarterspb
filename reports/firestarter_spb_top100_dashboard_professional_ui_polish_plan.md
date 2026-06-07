# Firestarter SPB: Top 100 Dashboard Professional UI Polish Plan

This document outlines the professional UI/UX design updates to transform the Binance Top 100 dashboard into a high-density, serious quantitative research terminal.

## 1. Identified Visual Limitations
- **Color Styling:** Remove overly bright rainbow color selections and emoji from warnings/titles. Use a restrained dark-mode palette.
- **Oversized Layout elements:** Card size and grid spacing are currently too loose. We will decrease margin sizes, padding values, and text sizes to achieve high information density.
- **Chart Visual Clutter:** Standardize SMA trend lines to neutral and muted colors. Align plot border highlights.
- **Tabular presentation:** Use monospaced numbers in tables to prevent visual alignment jitter. Shrink table fonts to `12px` for compact tabular rendering.

## 2. Quantitative Terminal Theme Specs
- **Color System:**
  - Base Background: `#08090b` (Deep matte black)
  - Card/Panel Background: `#0e1014` (Dense charcoal)
  - Muted Borders: `#1e222b` (Charcoal grey)
  - Primary Text: `#f1f5f9` (High-contrast off-white)
  - Muted Text: `#64748b` (Muted slate blue)
  - Selected Accent: `#2563eb` (Restrained terminal blue)
  - Bullish Indicators: `#059669` (Muted forest green)
  - Bearish Indicators: `#dc2626` (Muted crimson red)
- **Typography:**
  - Base font: `Inter, sans-serif`
  - Data / Numeric font: `Consolas, Menlo, Monaco, monospace` (For clean tabular layouts and readouts)
  - Scale: Font sizes reduced across the board (Body base: `13px`, Tables: `12px`, Headings: `16px`-`20px`)

## 3. Implementation Workflow
1. Update `scripts/visualization/build_top100_clean_html_dashboard.py` with the updated color palette, CSS styling, and Plotly layout configurations.
2. Execute the python builder to regenerate the index and symbol detail HTML files.
3. Verify the generated output files locally.
4. Stage, commit, and push the updated viewer dashboard files.
