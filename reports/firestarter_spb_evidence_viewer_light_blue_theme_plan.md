# Evidence Viewer Light Blue Theme Plan

This document outlines the visual layout modifications to transition the research-only HTML Evidence Viewer to a modern, light-blue aesthetic while maintaining 100% functional, formulaic, and structural parity.

## 1. Visual Theme Specifications

### Color Palette
- **Body Background:** Light, desaturated steel blue (`#eef4f8` / HSL: 204, 38%, 95%) to reduce eye strain while providing a cool tech feel.
- **Card/Header Background:** Pure white (`#ffffff`) for elevated readability with high-contrast content.
- **Card Borders/Shadows:** Thin border in soft blue-gray (`#dbeafe`) and soft shadows (`rgba(15, 23, 42, 0.05)`) to create visual hierarchy (glassmorphic lift).
- **Text Color:** Charcoal/slate (`#1e293b`) for body text and headers, ensuring proper WCAG accessibility contrast.

### Chart Styling & Contrast
- **Plotly Theme Configuration:** 
  - Plot paper background: `#ffffff`
  - Plot area background (plot_bgcolor): `#f8fafc` (very light slate/blue hint)
  - Gridlines: Soft slate-blue (`#e2e8f0`)
  - Axis labels/ticks: Charcoal/slate (`#475569`)
- **Trace Colors:** Preserve key trace colors to maintain compatibility:
  - FMLC: `purple`
  - Flowprint: `orange`
  - ER: `darkred`
  - Raw Score: `gray` (dotted)
  - Entry C Markers: `green` (triangle-up)
  - Fake Recovery Markers: `red` (x)

### Readability Enhancements
- Modernized font stack favoring system-sans (Inter, system-ui, -apple-system, sans-serif).
- Enhanced padding and soft borders for the hover readout card to draw attention to local indicators.
- Select elements styled with rounded corners and subtle blue focus rings.

---

## 2. Unchanged Boundaries

- **No Formula Modifications:** The calculation of `fmlc_rise`, `fp_rise`, `is_entry_c`, and `is_fake_rec` remains exactly as written.
- **Data Preservation:** The viewer reads `firestarterog_real_historical_variance_sample.csv` without mutation.
- **Workflow & Layout:** The triple-pane layout (Price, Scores, ER) is kept identical, and the hover readout dynamically populates on hover just as before.
- **No Production trading or model components:** The script remains purely a local simulation tool for forensic visual validation.
