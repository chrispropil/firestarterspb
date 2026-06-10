# FirestarterOG Profile Event Tagging Refinement 001

**Task ID:** FIRESTARTEROG_PROFILE_EVENT_TAGGING_REFINEMENT_001  
**System:** Matrix Alpha / FirestarterOG  
**Date:** 2026-06-08  

Research-only profiling. No Cell 2 logic, alerts, raw data mutation, formula changes, or trading/action directives.

---

## Files Changed

| File | Change |
|------|--------|
| `scripts/run_top100_profile_event_scanner.py` | Refined the event output classification layer: `primary_event_type`, `secondary_tags`, and `data_quality_flags`. |
| `reports/firestarterog_profile_event_tagging_refinement_001.md` | Added this bounded validation report. |

No commit was made.

---

## Hierarchy Used

Primary event resolution order:

1. `DATA_INSUFFICIENT`
2. `DOMINO_DETERIORATION`
3. `HOLLOW_BREAKOUT`
4. `FAKE_RECOVERY`
5. `ENTRY_C_LIKE_RECOVERY`
6. `NIF_CATALYST_QUALITY_AUDIT`
7. `NO_PRIMARY_EVENT`

Detected internal event keys are mapped only at the classification output layer:

| Internal event key | Output label |
|--------------------|--------------|
| `ENTRY_C_RECOVERY` | `ENTRY_C_LIKE_RECOVERY` |
| `NIF_CATALYST_QUALITY` | `NIF_CATALYST_QUALITY_AUDIT` |

`secondary_tags` preserves every detected event except the resolved primary event.

Data quality flags:

| Flag | Trigger |
|------|---------|
| `HIGH_NAN_WARNING` | `nan_pct_score >= 25` |
| `INSUFFICIENT_DERIVATIVE_CONTEXT` | Required derivative fields are missing. |
| `LOW_ROW_COUNT` | `hourly_rows < 120` |
| `CLEAN_DATA` | No warning flags triggered. |

---

## CTSIUSDT Before / After Classification

Before:

```text
status: OK
hourly_rows: 721
nan_pct_score: 27.9%
RESEARCH_PRIORITY_SCORE: 45
FAKE_RECOVERY: detected=True
DOMINO_DETERIORATION: detected=True
primary_event_type: not present
secondary_tags: not present
data_quality_flags: not present
```

After:

```text
status: OK
hourly_rows: 721
nan_pct_score: 27.9%
RESEARCH_PRIORITY_SCORE: 45
primary_event_type: DOMINO_DETERIORATION
secondary_tags: FAKE_RECOVERY
data_quality_flags: HIGH_NAN_WARNING
FAKE_RECOVERY: detected=True
DOMINO_DETERIORATION: detected=True
```

Expected CTSIUSDT classification matched.

---

## Short Set Results

Only these symbols were tested:

| Symbol | Status | Hourly Rows | NaN% | Priority | primary_event_type | secondary_tags | data_quality_flags | Detected Events | Result |
|--------|--------|-------------|------|----------|--------------------|----------------|--------------------|-----------------|--------|
| CTSIUSDT | OK | 721 | 27.9 | 45 | `DOMINO_DETERIORATION` | `FAKE_RECOVERY` | `HIGH_NAN_WARNING` | `FAKE_RECOVERY`, `DOMINO_DETERIORATION` | PASS |
| BTWUSDT | NOISY_INSUFFICIENT | 0 | n/a | 0 | `DATA_INSUFFICIENT` | none | `LOW_ROW_COUNT` | none | PASS |
| SLXUSDT | NOISY_INSUFFICIENT | 0 | n/a | 0 | `DATA_INSUFFICIENT` | none | `LOW_ROW_COUNT` | none | PASS |
| ZESTUSDT | NOISY_INSUFFICIENT | 0 | n/a | 0 | `DATA_INSUFFICIENT` | none | `LOW_ROW_COUNT` | none | PASS |
| BEATUSDT | OK | 721 | 27.9 | 25 | `FAKE_RECOVERY` | none | `HIGH_NAN_WARNING` | `FAKE_RECOVERY` | PASS |
| BTCUSDT | OK | 721 | 27.9 | 65 | `FAKE_RECOVERY` | `NIF_CATALYST_QUALITY_AUDIT` | `HIGH_NAN_WARNING` | `FAKE_RECOVERY`, `NIF_CATALYST_QUALITY` | PASS |

Short set result: 6/6 PASS.

---

## Event Definitions Changed?

No.

Unchanged:

- `detect_hollow_breakout`
- `detect_fake_recovery`
- `detect_entry_c_recovery`
- `detect_domino_deterioration`
- `detect_nif_catalyst_quality`
- `compute_research_priority_score`
- Cell 1 formulas

The refinement reads existing detection output and adds profile classification fields only.

---

## Verdict

PASS_FIRESTARTEROG_PROFILE_EVENT_TAGGING_REFINEMENT_COMPLETE
