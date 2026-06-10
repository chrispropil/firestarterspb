# Top 100 FirestarterOG Profile Event Scanner — Run 001

**Run timestamp (UTC):** 2026-06-08T14:58:56Z
**Task ID:** FIRESTARTEROG_TOP100_PROFILE_EVENT_SCANNER_001
**Dataset:** `data/research/binance_top100_excluding_existing_5_1month/`
**Derivatives:** `data/research/binance_top100_derivatives_context_1month/`

> **RESEARCH ONLY.** No action labels, no buy/sell signals, no Cell 2 logic.

---

## 1. Scan Summary

| Metric | Value |
|--------|-------|
| Total symbols scanned | 100 |
| Status: OK (event-eligible) | 95 |
| Status: NOISY_INSUFFICIENT | 5 |
| Status: INSUFFICIENT_DERIVATIVE_CONTEXT | 0 |
| Status: ERROR | 0 |

### Event Detection Counts (OK symbols only)

| Event Type | Detected Count |
|------------|----------------|
| HOLLOW_BREAKOUT | 0 |
| FAKE_RECOVERY | 89 |
| ENTRY_C_RECOVERY | 36 |
| DOMINO_DETERIORATION | 34 |
| NIF_CATALYST_QUALITY | 37 |

---

## 2. Top Priority Symbols (sorted by RESEARCH_PRIORITY_SCORE)

| # | Symbol | RESEARCH_PRIORITY_SCORE | Events Detected | Hourly Rows | NaN% |
|---|--------|------------------------|-----------------|-------------|------|
| 1 | BANKUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 2 | BASEDUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, DOMINO_DETERIORATION, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 3 | BLESSUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 4 | ALLOUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, DOMINO_DETERIORATION, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 5 | ENAUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 6 | EDENUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, DOMINO_DETERIORATION, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 7 | ETHUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 8 | CCUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 9 | VELVETUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 10 | PARTIUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 11 | ONDOUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 12 | PAXGUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 13 | JTOUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, DOMINO_DETERIORATION, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 14 | MEMEUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, DOMINO_DETERIORATION, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 15 | OPGUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, DOMINO_DETERIORATION, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 16 | PHAROSUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 591 | 33.8% |
| 17 | HYPEUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 18 | GWEIUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 19 | GIGGLEUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, NIF_CATALYST_QUALITY | 721 | 27.9% |
| 20 | FIDAUSDT | 100 | FAKE_RECOVERY, ENTRY_C_RECOVERY, DOMINO_DETERIORATION, NIF_CATALYST_QUALITY | 721 | 27.9% |

---

## 3. Per-Symbol Event Detail (OK symbols, score > 0)

### BANKUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.64 then dropped below 2.5 within 24H window. Latest FMLC=5.24, Flowprint=6.00
  - **ENTRY_C_RECOVERY:** Trough score=0.96, recovered to 7.64 over ~18H. OI positive confirms: 11/18H. Funding neutral/negative: 18/18H. Latest raw_score=6.59
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.59 (>= 6.5), OI=133538020 above 24H avg, funding=0.000050 (healthy). Qualifying bars in last 48H: 2

### BASEDUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.85 then dropped below 2.5 within 24H window. Latest FMLC=7.64, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=2.48, recovered to 7.47 over ~18H. OI positive confirms: 6/18H. Funding neutral/negative: 18/18H. Latest raw_score=6.96
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=7.64, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=3.80
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=8.18 (>= 6.5), OI=65412358 above 24H avg, funding=0.000050 (healthy). Qualifying bars in last 48H: 2

### BLESSUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.89 then dropped below 2.5 within 24H window. Latest FMLC=4.73, Flowprint=5.00
  - **ENTRY_C_RECOVERY:** Trough score=1.70, recovered to 7.42 over ~18H. OI positive confirms: 7/18H. Funding neutral/negative: 18/18H. Latest raw_score=5.72
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.62 (>= 6.5), OI=846729072 above 24H avg, funding=0.000057 (healthy). Qualifying bars in last 48H: 4

### ALLOUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.70 then dropped below 2.5 within 24H window. Latest FMLC=0.00, Flowprint=1.00
  - **ENTRY_C_RECOVERY:** Trough score=2.36, recovered to 6.87 over ~18H. OI positive confirms: 5/18H. Funding neutral/negative: 18/18H. Latest raw_score=6.26
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=0.00, Flowprint=1.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=0.32
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.60 (>= 6.5), OI=86864608 above 24H avg, funding=0.000020 (healthy). Qualifying bars in last 48H: 5

### ENAUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.78 then dropped below 2.5 within 24H window. Latest FMLC=2.66, Flowprint=4.00
  - **ENTRY_C_RECOVERY:** Trough score=1.86, recovered to 6.63 over ~18H. OI positive confirms: 6/18H. Funding neutral/negative: 18/18H. Latest raw_score=4.29
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.52 (>= 6.5), OI=484971310 above 24H avg, funding=0.000050 (healthy). Qualifying bars in last 48H: 2

### EDENUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.99 then dropped below 2.5 within 24H window. Latest FMLC=3.99, Flowprint=0.00
  - **ENTRY_C_RECOVERY:** Trough score=2.47, recovered to 7.38 over ~18H. OI positive confirms: 6/18H. Funding neutral/negative: 18/18H. Latest raw_score=5.25
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=3.99, Flowprint=0.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=1.48
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.61 (>= 6.5), OI=119670126 above 24H avg, funding=-0.009731 (healthy). Qualifying bars in last 48H: 4

### ETHUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.51 then dropped below 2.5 within 24H window. Latest FMLC=7.58, Flowprint=4.00
  - **ENTRY_C_RECOVERY:** Trough score=2.22, recovered to 7.67 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 18/18H. Latest raw_score=7.67
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.96 (>= 6.5), OI=2392779 above 24H avg, funding=-0.000102 (healthy). Qualifying bars in last 48H: 3

### CCUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 8.45 then dropped below 2.5 within 24H window. Latest FMLC=6.88, Flowprint=5.00
  - **ENTRY_C_RECOVERY:** Trough score=2.07, recovered to 9.30 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 18/18H. Latest raw_score=6.39
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.16 (>= 6.5), OI=55874532 above 24H avg, funding=0.000050 (healthy). Qualifying bars in last 48H: 4

### VELVETUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.47 then dropped below 2.5 within 24H window. Latest FMLC=3.51, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=2.08, recovered to 8.89 over ~18H. OI positive confirms: 14/18H. Funding neutral/negative: 15/18H. Latest raw_score=6.34
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.97 (>= 6.5), OI=44210078 above 24H avg, funding=0.000271 (healthy). Qualifying bars in last 48H: 3

### PARTIUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.84 then dropped below 2.5 within 24H window. Latest FMLC=7.09, Flowprint=4.00
  - **ENTRY_C_RECOVERY:** Trough score=0.96, recovered to 7.05 over ~18H. OI positive confirms: 5/18H. Funding neutral/negative: 18/18H. Latest raw_score=7.05
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.03 (>= 6.5), OI=166338530 above 24H avg, funding=0.000050 (healthy). Qualifying bars in last 48H: 4

### ONDOUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.03 then dropped below 2.5 within 24H window. Latest FMLC=7.02, Flowprint=2.00
  - **ENTRY_C_RECOVERY:** Trough score=2.04, recovered to 8.30 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 18/18H. Latest raw_score=3.64
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.98 (>= 6.5), OI=89294346 above 24H avg, funding=-0.000149 (healthy). Qualifying bars in last 48H: 2

### PAXGUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.69 then dropped below 2.5 within 24H window. Latest FMLC=3.35, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=2.46, recovered to 5.69 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 18/18H. Latest raw_score=2.19
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.74 (>= 6.5), OI=22773 above 24H avg, funding=0.000047 (healthy). Qualifying bars in last 48H: 3

### JTOUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.26 then dropped below 2.5 within 24H window. Latest FMLC=4.03, Flowprint=2.00
  - **ENTRY_C_RECOVERY:** Trough score=2.23, recovered to 8.59 over ~18H. OI positive confirms: 6/18H. Funding neutral/negative: 18/18H. Latest raw_score=6.98
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=1.00, FMLC=4.03, Flowprint=2.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=2.51
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.98 (>= 6.5), OI=16128023 above 24H avg, funding=-0.000712 (healthy). Qualifying bars in last 48H: 4

### MEMEUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.95 then dropped below 2.5 within 24H window. Latest FMLC=7.66, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=2.36, recovered to 8.25 over ~18H. OI positive confirms: 5/18H. Funding neutral/negative: 18/18H. Latest raw_score=4.55
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=7.66, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=3.81
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.49 (>= 6.5), OI=5344143041 above 24H avg, funding=-0.000043 (healthy). Qualifying bars in last 48H: 2

### OPGUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.72 then dropped below 2.5 within 24H window. Latest FMLC=7.44, Flowprint=2.00
  - **ENTRY_C_RECOVERY:** Trough score=2.38, recovered to 7.52 over ~18H. OI positive confirms: 6/18H. Funding neutral/negative: 18/18H. Latest raw_score=7.11
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=7.44, Flowprint=2.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=3.41
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.89 (>= 6.5), OI=35226223 above 24H avg, funding=0.000050 (healthy). Qualifying bars in last 48H: 5

### PHAROSUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 591
- **NaN score%:** 33.8%
- **Partial-parent rows:** 3 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 8.93 then dropped below 2.5 within 24H window. Latest FMLC=4.37, Flowprint=1.00
  - **ENTRY_C_RECOVERY:** Trough score=2.26, recovered to 8.93 over ~18H. OI positive confirms: 11/18H. Funding neutral/negative: 18/18H. Latest raw_score=3.79
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.90 (>= 6.5), OI=3778704 above 24H avg, funding=-0.000120 (healthy). Qualifying bars in last 48H: 5

### HYPEUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.04 then dropped below 2.5 within 24H window. Latest FMLC=4.90, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=1.88, recovered to 7.04 over ~18H. OI positive confirms: 5/18H. Funding neutral/negative: 18/18H. Latest raw_score=4.33
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.04 (>= 6.5), OI=5342857 above 24H avg, funding=-0.000039 (healthy). Qualifying bars in last 48H: 2

### GWEIUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.21 then dropped below 2.5 within 24H window. Latest FMLC=6.24, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=1.38, recovered to 7.39 over ~18H. OI positive confirms: 5/18H. Funding neutral/negative: 10/18H. Latest raw_score=3.24
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.10 (>= 6.5), OI=109151776 above 24H avg, funding=0.000134 (healthy). Qualifying bars in last 48H: 2

### GIGGLEUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.26 then dropped below 2.5 within 24H window. Latest FMLC=7.90, Flowprint=2.00
  - **ENTRY_C_RECOVERY:** Trough score=1.81, recovered to 7.00 over ~18H. OI positive confirms: 6/18H. Funding neutral/negative: 18/18H. Latest raw_score=6.46
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.44 (>= 6.5), OI=222044 above 24H avg, funding=0.000050 (healthy). Qualifying bars in last 48H: 3

### FIDAUSDT  `RESEARCH_PRIORITY_SCORE=100`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.75 then dropped below 2.5 within 24H window. Latest FMLC=3.98, Flowprint=1.00
  - **ENTRY_C_RECOVERY:** Trough score=1.65, recovered to 7.75 over ~18H. OI positive confirms: 7/18H. Funding neutral/negative: 18/18H. Latest raw_score=4.06
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=1.00, FMLC=3.98, Flowprint=1.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=2.17
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.59 (>= 6.5), OI=160894653 above 24H avg, funding=0.000050 (healthy). Qualifying bars in last 48H: 2

### NEARUSDT  `RESEARCH_PRIORITY_SCORE=85`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.44 then dropped below 2.5 within 24H window. Latest FMLC=7.26, Flowprint=3.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=7.26, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=3.66
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.70 (>= 6.5), OI=49167419 above 24H avg, funding=0.000019 (healthy). Qualifying bars in last 48H: 2

### RAVEUSDT  `RESEARCH_PRIORITY_SCORE=85`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.51 then dropped below 2.5 within 24H window. Latest FMLC=3.56, Flowprint=3.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=3.56, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=2.28
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.80 (>= 6.5), OI=21456581 above 24H avg, funding=0.000216 (healthy). Qualifying bars in last 48H: 2

### UBUSDT  `RESEARCH_PRIORITY_SCORE=85`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.05 then dropped below 2.5 within 24H window. Latest FMLC=6.43, Flowprint=2.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=6.43, Flowprint=2.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=3.03
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.74 (>= 6.5), OI=67956998 above 24H avg, funding=0.000050 (healthy). Qualifying bars in last 48H: 3

### TAOUSDT  `RESEARCH_PRIORITY_SCORE=85`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.41 then dropped below 2.5 within 24H window. Latest FMLC=7.60, Flowprint=3.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=7.60, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=3.79
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=8.41 (>= 6.5), OI=244801 above 24H avg, funding=-0.000099 (healthy). Qualifying bars in last 48H: 2

### BILLUSDT  `RESEARCH_PRIORITY_SCORE=85`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.67 then dropped below 2.5 within 24H window. Latest FMLC=2.32, Flowprint=4.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=2.00, FMLC=2.32, Flowprint=4.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=2.88
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.53 (>= 6.5), OI=104333232 above 24H avg, funding=0.000147 (healthy). Qualifying bars in last 48H: 3

### ASTERUSDT  `RESEARCH_PRIORITY_SCORE=85`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.41 then dropped below 2.5 within 24H window. Latest FMLC=4.66, Flowprint=3.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=4.66, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=2.69
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=8.04 (>= 6.5), OI=118008937 above 24H avg, funding=-0.000037 (healthy). Qualifying bars in last 48H: 2

### DASHUSDT  `RESEARCH_PRIORITY_SCORE=85`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.96 then dropped below 2.5 within 24H window. Latest FMLC=4.64, Flowprint=4.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=4.64, Flowprint=4.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=3.00
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.89 (>= 6.5), OI=435825 above 24H avg, funding=-0.000393 (healthy). Qualifying bars in last 48H: 3

### WLDUSDT  `RESEARCH_PRIORITY_SCORE=85`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.34 then dropped below 2.5 within 24H window. Latest FMLC=3.95, Flowprint=1.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=3.95, Flowprint=1.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=1.79
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.08 (>= 6.5), OI=209423823 above 24H avg, funding=-0.000503 (healthy). Qualifying bars in last 48H: 2

### AAVEUSDT  `RESEARCH_PRIORITY_SCORE=80`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.23 then dropped below 2.5 within 24H window. Latest FMLC=3.67, Flowprint=2.00
  - **ENTRY_C_RECOVERY:** Trough score=2.31, recovered to 5.23 over ~18H. OI positive confirms: 9/18H. Funding neutral/negative: 18/18H. Latest raw_score=4.04
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=1.00, FMLC=3.67, Flowprint=2.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=2.38

### BLUAIUSDT  `RESEARCH_PRIORITY_SCORE=80`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.84 then dropped below 2.5 within 24H window. Latest FMLC=0.00, Flowprint=2.00
  - **ENTRY_C_RECOVERY:** Trough score=1.97, recovered to 6.60 over ~18H. OI positive confirms: 5/18H. Funding neutral/negative: 13/18H. Latest raw_score=5.44
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=0.00, Flowprint=2.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=0.64

### HOMEUSDT  `RESEARCH_PRIORITY_SCORE=80`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.10 then dropped below 2.5 within 24H window. Latest FMLC=0.00, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=0.32, recovered to 5.91 over ~18H. OI positive confirms: 6/18H. Funding neutral/negative: 18/18H. Latest raw_score=5.70
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=1.00, FMLC=0.00, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=1.33

### CLOUSDT  `RESEARCH_PRIORITY_SCORE=80`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.14 then dropped below 2.5 within 24H window. Latest FMLC=3.49, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=0.96, recovered to 7.14 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 11/18H. Latest raw_score=4.13
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=3.49, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=2.26

### OPNUSDT  `RESEARCH_PRIORITY_SCORE=80`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.12 then dropped below 2.5 within 24H window. Latest FMLC=2.60, Flowprint=1.00
  - **ENTRY_C_RECOVERY:** Trough score=1.87, recovered to 7.12 over ~18H. OI positive confirms: 8/18H. Funding neutral/negative: 14/18H. Latest raw_score=4.83
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=2.60, Flowprint=1.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=1.29

### SIRENUSDT  `RESEARCH_PRIORITY_SCORE=80`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY|ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.93 then dropped below 2.5 within 24H window. Latest FMLC=4.86, Flowprint=4.00
  - **ENTRY_C_RECOVERY:** Trough score=2.16, recovered to 6.93 over ~18H. OI positive confirms: 5/18H. Funding neutral/negative: 14/18H. Latest raw_score=6.93
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=7.00, FMLC=4.86, Flowprint=4.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=5.69

### BSBUSDT  `RESEARCH_PRIORITY_SCORE=75`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `ENTRY_C_LIKE_RECOVERY`
- **secondary_tags:** `NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **ENTRY_C_RECOVERY:** Trough score=2.42, recovered to 6.53 over ~18H. OI positive confirms: 6/18H. Funding neutral/negative: 18/18H. Latest raw_score=4.59
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.40 (>= 6.5), OI=53958919 above 24H avg, funding=0.000071 (healthy). Qualifying bars in last 48H: 4

### BNBUSDT  `RESEARCH_PRIORITY_SCORE=65`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.44 then dropped below 2.5 within 24H window. Latest FMLC=7.61, Flowprint=3.00
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.59 (>= 6.5), OI=567361 above 24H avg, funding=0.000000 (healthy). Qualifying bars in last 48H: 3

### PLAYUSDT  `RESEARCH_PRIORITY_SCORE=65`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.55 then dropped below 2.5 within 24H window. Latest FMLC=7.58, Flowprint=6.00
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.97 (>= 6.5), OI=50675092 above 24H avg, funding=0.000050 (healthy). Qualifying bars in last 48H: 5

### BTCUSDT  `RESEARCH_PRIORITY_SCORE=65`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.30 then dropped below 2.5 within 24H window. Latest FMLC=7.01, Flowprint=2.00
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.93 (>= 6.5), OI=102873 above 24H avg, funding=0.000004 (healthy). Qualifying bars in last 48H: 5

### CRVUSDT  `RESEARCH_PRIORITY_SCORE=65`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.17 then dropped below 2.5 within 24H window. Latest FMLC=8.03, Flowprint=5.00
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.87 (>= 6.5), OI=76154854 above 24H avg, funding=0.000012 (healthy). Qualifying bars in last 48H: 4

### ETCUSDT  `RESEARCH_PRIORITY_SCORE=65`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.46 then dropped below 2.5 within 24H window. Latest FMLC=7.30, Flowprint=2.00
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=6.58 (>= 6.5), OI=2154915 above 24H avg, funding=0.000040 (healthy). Qualifying bars in last 48H: 3

### PENGUUSDT  `RESEARCH_PRIORITY_SCORE=65`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.09 then dropped below 2.5 within 24H window. Latest FMLC=7.61, Flowprint=2.00
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.38 (>= 6.5), OI=2175618758 above 24H avg, funding=-0.000075 (healthy). Qualifying bars in last 48H: 3

### SAHARAUSDT  `RESEARCH_PRIORITY_SCORE=65`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.97 then dropped below 2.5 within 24H window. Latest FMLC=8.85, Flowprint=6.00
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=8.56 (>= 6.5), OI=1066215389 above 24H avg, funding=0.000187 (healthy). Qualifying bars in last 48H: 7

### SKYAIUSDT  `RESEARCH_PRIORITY_SCORE=65`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `NIF_CATALYST_QUALITY_AUDIT`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.48 then dropped below 2.5 within 24H window. Latest FMLC=0.00, Flowprint=3.00
  - **NIF_CATALYST_QUALITY:** NIF catalyst window: raw_score=7.48 (>= 6.5), OI=114042417 above 24H avg, funding=0.000283 (healthy). Qualifying bars in last 48H: 4

### 1000PEPEUSDT  `RESEARCH_PRIORITY_SCORE=60`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.10 then dropped below 2.5 within 24H window. Latest FMLC=7.21, Flowprint=2.00
  - **ENTRY_C_RECOVERY:** Trough score=2.41, recovered to 7.34 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 18/18H. Latest raw_score=4.17

### HEIUSDT  `RESEARCH_PRIORITY_SCORE=60`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.62 then dropped below 2.5 within 24H window. Latest FMLC=0.00, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=2.11, recovered to 7.46 over ~18H. OI positive confirms: 9/18H. Funding neutral/negative: 18/18H. Latest raw_score=0.32

### TONUSDT  `RESEARCH_PRIORITY_SCORE=60`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.71 then dropped below 2.5 within 24H window. Latest FMLC=6.78, Flowprint=4.00
  - **ENTRY_C_RECOVERY:** Trough score=1.85, recovered to 7.55 over ~18H. OI positive confirms: 5/18H. Funding neutral/negative: 18/18H. Latest raw_score=4.13

### VVVUSDT  `RESEARCH_PRIORITY_SCORE=60`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.91 then dropped below 2.5 within 24H window. Latest FMLC=3.78, Flowprint=2.00
  - **ENTRY_C_RECOVERY:** Trough score=0.64, recovered to 6.91 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 18/18H. Latest raw_score=4.03

### INJUSDT  `RESEARCH_PRIORITY_SCORE=60`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.84 then dropped below 2.5 within 24H window. Latest FMLC=7.06, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=1.13, recovered to 6.58 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 18/18H. Latest raw_score=2.84

### RENDERUSDT  `RESEARCH_PRIORITY_SCORE=60`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.78 then dropped below 2.5 within 24H window. Latest FMLC=3.51, Flowprint=2.00
  - **ENTRY_C_RECOVERY:** Trough score=2.00, recovered to 7.78 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 18/18H. Latest raw_score=2.53

### ADAUSDT  `RESEARCH_PRIORITY_SCORE=60`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.71 then dropped below 2.5 within 24H window. Latest FMLC=4.74, Flowprint=3.00
  - **ENTRY_C_RECOVERY:** Trough score=2.07, recovered to 7.16 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 18/18H. Latest raw_score=3.79

### EPICUSDT  `RESEARCH_PRIORITY_SCORE=60`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `ENTRY_C_LIKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.43 then dropped below 2.5 within 24H window. Latest FMLC=9.71, Flowprint=5.00
  - **ENTRY_C_RECOVERY:** Trough score=2.24, recovered to 7.33 over ~18H. OI positive confirms: 5/18H. Funding neutral/negative: 18/18H. Latest raw_score=3.94

### CTSIUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.23 then dropped below 2.5 within 24H window. Latest FMLC=3.03, Flowprint=1.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=3.03, Flowprint=1.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=1.45

### XPLUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.49 then dropped below 2.5 within 24H window. Latest FMLC=3.56, Flowprint=4.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=3.56, Flowprint=4.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=2.60

### TRXUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.14 then dropped below 2.5 within 24H window. Latest FMLC=7.30, Flowprint=2.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=3.00, FMLC=7.30, Flowprint=2.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=4.47

### WLFIUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.63 then dropped below 2.5 within 24H window. Latest FMLC=2.46, Flowprint=3.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=2.46, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=1.87

### UNIUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.23 then dropped below 2.5 within 24H window. Latest FMLC=3.72, Flowprint=4.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=3.72, Flowprint=4.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=2.66

### TIAUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.18 then dropped below 2.5 within 24H window. Latest FMLC=6.64, Flowprint=3.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=6.64, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=3.43

### PORTALUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.06 then dropped below 2.5 within 24H window. Latest FMLC=0.00, Flowprint=0.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=0.00, Flowprint=0.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=0.00

### SEIUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.63 then dropped below 2.5 within 24H window. Latest FMLC=3.74, Flowprint=1.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=3.74, Flowprint=1.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=1.71

### HBARUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.18 then dropped below 2.5 within 24H window. Latest FMLC=6.83, Flowprint=5.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=1.00, FMLC=6.83, Flowprint=5.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=4.51

### ALGOUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.10 then dropped below 2.5 within 24H window. Latest FMLC=2.65, Flowprint=1.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=2.65, Flowprint=1.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=1.31

### INUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.93 then dropped below 2.5 within 24H window. Latest FMLC=3.44, Flowprint=2.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=3.44, Flowprint=2.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=1.92

### LABUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.09 then dropped below 2.5 within 24H window. Latest FMLC=2.80, Flowprint=5.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=2.80, Flowprint=5.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=2.64

### CHZUSDT  `RESEARCH_PRIORITY_SCORE=45`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `DOMINO_DETERIORATION`
- **secondary_tags:** `FAKE_RECOVERY`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.06 then dropped below 2.5 within 24H window. Latest FMLC=2.58, Flowprint=3.00
  - **DOMINO_DETERIORATION:** Cascade decline over last 6H: ER=0.00, FMLC=2.58, Flowprint=3.00. Window: 2026-06-07 07:00:00+00:00 → 2026-06-07 18:00:00+00:00. raw_score=1.92

### ZECUSDT  `RESEARCH_PRIORITY_SCORE=35`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `ENTRY_C_LIKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **ENTRY_C_RECOVERY:** Trough score=1.58, recovered to 7.25 over ~18H. OI positive confirms: 4/18H. Funding neutral/negative: 18/18H. Latest raw_score=4.73

### 1000SHIBUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.23 then dropped below 2.5 within 24H window. Latest FMLC=7.11, Flowprint=0.00

### BCHUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.88 then dropped below 2.5 within 24H window. Latest FMLC=7.02, Flowprint=4.00

### 1000BONKUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.26 then dropped below 2.5 within 24H window. Latest FMLC=4.94, Flowprint=2.00

### XMRUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.62 then dropped below 2.5 within 24H window. Latest FMLC=3.64, Flowprint=3.00

### OPUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.74 then dropped below 2.5 within 24H window. Latest FMLC=3.08, Flowprint=1.00

### MAGMAUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.74 then dropped below 2.5 within 24H window. Latest FMLC=6.49, Flowprint=4.00

### ESPORTSUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 8.30 then dropped below 2.5 within 24H window. Latest FMLC=2.46, Flowprint=2.00

### BABYUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.23 then dropped below 2.5 within 24H window. Latest FMLC=6.81, Flowprint=4.00

### ARBUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.82 then dropped below 2.5 within 24H window. Latest FMLC=3.61, Flowprint=2.00

### BEATUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.45 then dropped below 2.5 within 24H window. Latest FMLC=3.81, Flowprint=3.00
  - **BEAT Special Audit:** BEAT 2026-06-06 audit: min_score=1.53, max_score=7.08, mean_score=3.99, rows=24

### APTUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.11 then dropped below 2.5 within 24H window. Latest FMLC=3.24, Flowprint=5.00

### HUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.31 then dropped below 2.5 within 24H window. Latest FMLC=5.01, Flowprint=1.00

### FARTCOINUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.15 then dropped below 2.5 within 24H window. Latest FMLC=5.21, Flowprint=3.00

### FILUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.13 then dropped below 2.5 within 24H window. Latest FMLC=4.04, Flowprint=2.00

### GENIUSUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 5.99 then dropped below 2.5 within 24H window. Latest FMLC=7.58, Flowprint=1.00

### LITUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 8.25 then dropped below 2.5 within 24H window. Latest FMLC=2.75, Flowprint=2.00

### GUAUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.27 then dropped below 2.5 within 24H window. Latest FMLC=2.17, Flowprint=1.00

### ICPUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 7.20 then dropped below 2.5 within 24H window. Latest FMLC=3.14, Flowprint=2.00

### LTCUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.02 then dropped below 2.5 within 24H window. Latest FMLC=3.59, Flowprint=3.00

### WIFUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.21 then dropped below 2.5 within 24H window. Latest FMLC=7.22, Flowprint=2.00

### XLMUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.37 then dropped below 2.5 within 24H window. Latest FMLC=3.33, Flowprint=3.00

### SUIUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.57 then dropped below 2.5 within 24H window. Latest FMLC=7.16, Flowprint=3.00

### KITEUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.57 then dropped below 2.5 within 24H window. Latest FMLC=6.57, Flowprint=4.00

### PUMPUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.40 then dropped below 2.5 within 24H window. Latest FMLC=7.54, Flowprint=5.00

### VIRTUALUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 4.22 then dropped below 2.5 within 24H window. Latest FMLC=5.03, Flowprint=1.00

### PIPPINUSDT  `RESEARCH_PRIORITY_SCORE=25`

- **Hourly rows:** 721
- **NaN score%:** 27.9%
- **Partial-parent rows:** 30 (hourly rows before derivative data begins)
- **Derivative data available:** True
- **primary_event_type:** `FAKE_RECOVERY`
- **secondary_tags:** `none`
- **data_quality_flags:** `HIGH_NAN_WARNING`

  - **FAKE_RECOVERY:** Score rose to 6.78 then dropped below 2.5 within 24H window. Latest FMLC=7.76, Flowprint=6.00

---

## 4. BEATUSDT Special Audit (2026-06-06)

- **Status:** OK
- **RESEARCH_PRIORITY_SCORE:** 25
- **Audit note:** BEAT 2026-06-06 audit: min_score=1.53, max_score=7.08, mean_score=3.99, rows=24
- **FAKE_RECOVERY:** Score rose to 6.45 then dropped below 2.5 within 24H window. Latest FMLC=3.81, Flowprint=3.00

---

## 5. Excluded / Insufficient Symbols

| Symbol | Status | Detail |
|--------|--------|--------|
| BTWUSDT | NOISY_INSUFFICIENT | BTWUSDT is a short-window symbol (< 2 weeks of data). |
| SLXUSDT | NOISY_INSUFFICIENT | SLXUSDT is a short-window symbol (< 2 weeks of data). |
| ZESTUSDT | NOISY_INSUFFICIENT | ZESTUSDT is a short-window symbol (< 2 weeks of data). |
| 币安人生USDT | NOISY_INSUFFICIENT | No derivative context files found. |
| 龙虾USDT | NOISY_INSUFFICIENT | No derivative context files found. |

---

## 6. Data Integrity Notes

- **Derivative lag window:** All derivative signals are hourly-granularity.
  No 5–10 minute lead claimed. Signals reflect ≥1H lag from derivative source.
- **Partial-parent rows:** Rows before the first valid derivative value are
  counted per symbol. These rows will have NaN Flowprint/FMLC funding components.
- **USDCUSDT / FDUSDUSDT:** No Binance perp derivatives market — marked
  `INSUFFICIENT_DERIVATIVE_CONTEXT`. Not scored.
- **BTWUSDT / SLXUSDT / ZESTUSDT:** Very short candle windows (<2 weeks).
  Marked `NOISY_INSUFFICIENT`. Not scored.
- **Formula:** Identical to `build_top100_evidence_viewer.py`. No changes made.
