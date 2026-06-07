# High‑Tech UI Design Plan for Top 100 Dashboard

**Objective** – Transform the existing Top 100 dashboard into a premium, dark, research‑terminal style while **preserving all current chart logic, formulas, data loading, and layout**.

---
## 1. Color Palette
- **Background:** Deep black → subtle graphite gradient (`#0a0a0a` to `#111111`).
- **Primary Accent:** Muted cyan/blue (`#0db9d7`) for borders, hover highlights, and subtle panel edges.
- **Secondary Accent:** Soft amber (`#d19a66`) for ER bars.
- **Metric Lines:** 
  - Price: White (`#ffffff`).
  - FMLC: Red‑orange (`#ef4444`) with 0.6 opacity.
  - Flowprint: Light cyan (`#5eead4`) with 0.5 opacity.
  - Raw‑Score Dots: Purple (`#a78bfa`).
- **Text:** Light gray (`#e0e0e0`) for normal text, cyan (`#0db9d7`) for highlighted numbers.
- **Gridlines:** Very dark gray (`#222222`) – thin, unobtrusive.

---
## 2. Panel Hierarchy & Layout
| Panel | Content | Height (domain) | Y‑axis | Notes |
|-------|---------|----------------|--------|-------|
| **Panel 1** (top) | Price line only | `0.80 – 1.00` | Right y‑axis, auto scale | White line, dominant. |
| **Panel 2** (middle) | Firestarter metric group – raw_score dots, FMLC line, Flowprint line | `0.40 – 0.80` | Left y‑axis, fixed **0‑10** | Semi‑transparent glass background, cyan border. |
| **Panel 3** (bottom) | ER vertical bars | `0.00 – 0.40` | Left y‑axis, fixed **0‑10** | Muted amber, low opacity. |

Top‑right metric **cards** (ER, FMLC, Flowprint, Score) sit in a horizontal strip above the panels, each rendered as a compact terminal‑style readout.

---
## 3. Chart Styling (Plotly)
- **Backgrounds:** `paper_bgcolor` and `plot_bgcolor` set to `rgba(0,0,0,0.8)` with a subtle radial gradient via CSS.
- **Gridlines:** `gridcolor: '#222222'`, `gridwidth: 0.5`.
- **Axes:** Tick color `#e0e0e0`, label font `{'family': 'Inter, Roboto, sans-serif', 'size': 10, 'color': '#e0e0e0'}`; axis lines hidden (`showline: false`).
- **Font Family:** General text → `Inter`. Numeric values → `Roboto Mono` for monospaced appearance.
- **Lines:** Widths reduced (price 1.8, FMLC 0.9, Flowprint 0.6). Opacity tuned per palette.
- **Bars (ER):** `marker: {color: 'rgba(217,129,63,0.35)'}` with thin border `line: {width: 0}`.
- **Hover Templates:** Custom HTML using `<div style="background:#111111;color:#0db9d7;padding:4px;border-radius:4px;font-family:'Roboto Mono',monospace;">` to mimic a terminal readout.
- **Margins:** `l:30, r:30, t:40, b:30` to achieve a tight, compact look.
- **Drop‑shadow:** Apply CSS filter `drop-shadow(0 2px 4px rgba(0,0,0,0.6))` to each subplot container.

---
## 4. Card Styling (Top Metric Readouts)
- **Container:** `background: rgba(0,0,0,0.45)`; thin border `1px solid #0db9d7`; border‑radius `4px`.
- **Label:** Small font `size: 10`, color `#a0a0a0`.
- **Value:** Bold font `size: 12`, color `#0db9d7` (cyan) for numeric emphasis.
- **Spacing:** `padding: 4px 8px`; `margin-right: 8px`.
- **Alignment:** Flex row, centered vertically.

---
## 5. Typography
- **Global Font:** `Inter, Roboto, sans-serif` (clean, professional).
- **Numeric Font:** `Roboto Mono` – monospaced, sharp.
- **Headers:** `h1/h2` size reduced to `14‑16px`, color `#e0e0e0`.
- **No Playful Text:** All labels are concise, e.g., `ER`, `FMLC`, `Flow`, `Score`.

---
## 6. Hover / Readout Styling
- Dark background with slight opacity (`rgba(0,0,0,0.85)`).
- Cyan accent for values, gray for labels.
- Rounded corners `4px`.
- No extra tooltips or animated pop‑ups beyond the static hover box.

---
## 7. Navigation Styling
- **Symbol Index:** Compact list on the left side, background `rgba(0,0,0,0.6)`, hover highlight `rgba(13,185,215,0.2)`.
- **Search/Filter Box:** Small input with border `1px solid #0db9d7`, placeholder text in light gray.
- **Active Symbol:** Bold cyan text, background `rgba(13,185,215,0.15)`.
- **Buttons:** Minimalist icons only, no large text labels.

---
## 8. Table Styling (if any tables appear)
- **Background:** Same dark glass `rgba(0,0,0,0.45)`.
- **Borders:** Thin `1px solid #222222`.
- **Font:** `Roboto Mono`, size `10px`.
- **Row Hover:** Background `rgba(13,185,215,0.1)`.
- **No Color Blocks:** Keep rows monochrome.

---
## 9. What Will **NOT** Be Changed
- All formula calculations (`raw_score`, `Flowprint` scaling, ER values).
- Data loading pipeline and CSV/JSON sources.
- Symbol navigation logic and the set of 100 symbols.
- Panel ordering and chart structure (price‑only top panel, metric group, ER lower panel).
- Any SMA 20/50, volume %, Range/Vol % traces, bottom volume panel, or sticky header behavior.

---
## 10. Deliverables
- `reports/firestarter_spb_top100_dashboard_high_tech_ui_plan.md` – this design document.
- Updated `scripts/visualization/build_top100_clean_html_dashboard.py` with the CSS/Plotly style modifications.
- Generated dashboard pages (index + 100 symbol pages).
- `reports/firestarter_spb_top100_dashboard_high_tech_ui_audit.md` – audit checklist (to be produced after regeneration).

---
**Next Steps** – Once you approve this plan, I will patch the Python script with the visual updates, regenerate the dashboard, run the audit, and commit the changes.
