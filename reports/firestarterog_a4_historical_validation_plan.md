# FirestarterOG A4 Historical Validation Plan

**Date:** 2026-06-07  
**Status:** DRAFT / READY FOR REVIEW  
**Lineage:** Historical Verification Lane  

---

## 1. Artifact Discovery & Metadata Verification

The target A4 historical validation dataset has been successfully located on the local system:

- **Primary Artifact Path:** [firestarter_lane_a4_25_symbol_cell1_replay_output.csv](file:///C:/Users/User/fastlane/data/firestarter_lane_a4_25_symbol_cell1_replay_output.csv)
- **Secondary Artifact Path:** [firestarter_lane_a4_25_symbol_cell1_replay_output.jsonl](file:///C:/Users/User/fastlane/data/firestarter_lane_a4_25_symbol_cell1_replay_output.jsonl)

### Metadata Profile Confirmations:
- **Total Row Count:** Exactly **10,000** rows.
- **Unique Symbols Count:** Exactly **25** (BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, LINKUSDT, DOTUSDT, MATICUSDT, BNBUSDT, LTCUSDT, BCHUSDT, AVAXUSDT, UNIUSDT, ATOMUSDT, NEARUSDT, FILUSDT, ICPUSDT, VETUSDT, AAVEUSDT, STXUSDT, SHIBUSDT, TRXUSDT, XMRUSDT, ALGOUSDT).
- **Rows per Symbol:** Exactly **400** rows per symbol.
- **Core Score Columns Present:** `ER`, `FMLC`, `Flowprint`, `raw_score` exist in the dataset.

---

## 2. Plan for Formula Verification

To verify the historical continuity of the scoring model, we will perform a mathematical score validation across all 10,000 rows.

### 2.1 Formula to Validate
For every row, the calculated `raw_score` must align with the weighted sum of its component scores:
$$\text{raw\_score} = \text{ER} \times 0.35 + \text{FMLC} \times 0.35 + \text{Flowprint} \times 0.30$$
The results will be rounded to 2 decimal places.

### 2.2 Comparison Methodology
1. Load the historical CSV dataset.
2. For each row, recompute the `raw_score` using the `ER`, `FMLC`, and `Flowprint` values from that row.
3. Compare the recomputed score against the pre-existing `raw_score` stored in the file.
4. Log any discrepancy greater than a tolerance threshold of $0.01$.

---

## 3. Plan for Recovered Formula Comparison

To check if the recovered logic is identical to the logic that generated the A4 output:
1. Extract the raw inputs (RVOLs, price changes, range positions, breakout/reclaim flags, funding, open interest) from each row of the A4 CSV.
2. Run our recovered Python scoring logic (`scripts/recovery_test_20_symbol.py`) on those inputs.
3. Compare the newly calculated `ER`, `FMLC`, and `Flowprint` values against the historical ones in the file.
4. Record any mismatch rate to identify if any formula boundary cases or edge logic differ.

---

## 4. Sandbox Tweaks Boundary (Research-Only)

All sandbox/experimental metrics are flagged as **Research-Only** and must not be promoted to the main recovery scripts. These include:
- `conviction_score`
- `fakeout`
- `hard_fakeout`
- `raw_score_no_4h_trend`

Any scripts created during validation will isolate these metrics and report them under a distinct "Experimental" section, ensuring no pollution of the original FirestarterOG scoring baseline.

---

## 5. Safety Boundaries & DO-NOT Checklist

The execution phase of this plan will adhere to the following safety guardrails:
- **No File Modification:** The historical source files (`firestarter_lane_a4_25_symbol_cell1_replay_output.*`) will be read in a read-only manner. No writes, overwrites, or modifications will occur.
- **No Raw Data Commit:** The raw A4/A5 CSV/JSONL files are in `C:\Users\User\fastlane\data` and will remain outside the `firestarterspb` git staging area.
- **No Cell 2 Labeling:** No live SCOUT/TRIGGER buy labels will be assigned to this data.
- **No Secrets Exposure:** No private environment files or API keys will be read or logged.
- **No Live Alerts or Trading:** All validation is local, offline, and retrospective. No messages will be posted to Slack.

---

`PASS_FIRESTARTEROG_A4_HISTORICAL_VALIDATION_PLAN_READY`
