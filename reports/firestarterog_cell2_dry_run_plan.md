# FirestarterOG Cell 2 Dry-Run Plan

## 1. Exact Cell 2 Fields Required

To execute the original FirestarterOG Cell 2 Dust Cleaner logic, the following input fields are required:

| Field | Description | Source / Derivation |
|---|---|---|
| `ticker` | Symbol name | Cell 1 |
| `price` | Last price | Cell 1 |
| `change_24h_%` | 24h price change percentage | Cell 1 |
| `volume_usd` | 24h quote asset volume | Cell 1 |
| `rvol_1h` | Relative volume (1H vs 20-bar avg) | Cell 1 |
| `rvol_4h_window` | 4H relative volume | Cell 1 |
| `er` | Cell 1 Expansion Rating | Cell 1 |
| `fmlc` | Cell 1 Funding/Market-Structure rating | Cell 1 |
| `flowprint` | Cell 1 Flowprint score | Cell 1 |
| `raw_score` | Weighted score combination | Cell 1 |
| `near_breakout` | Flag indicating close is within 0.8% of high_20 | Cell 1 |
| `clean_reclaim` | Flag for close > ema_21 and ema_9 > ema_21 | Cell 1 |
| `above_4h_trend` | Flag for close > 4H ema_50 | Cell 1 |
| `range_pos_20` | Range position over 1H 20-bars | Cell 1 |
| `range_pos_50_4h` | Range position over 4H 50-bars | Cell 1 |
| `open_interest` | Current open interest | Cell 1 |
| `funding` | Current funding rate | Cell 1 |
| `ema_21` | Exponential moving average (21-bar) | Cell 1 |
| `is_stock_token` | Boolean blocking stock tokens | Cell 2 Filter |
| `risk_pct` | Estimated stop risk percentage | Cell 2 Gate |
| `invalidation_distance`| Flag ("GOOD", "STRETCHED", "BAD") for stop distance | Cell 2 Gate |
| `ignition_momentum` | Flag ("PASS", "FAIL") for momentum | Cell 2 Gate |
| `ignition_participation`| Flag ("PASS", "FAIL") for participation | Cell 2 Gate |

---

## 2. CSV Field Availability & Gap Analysis

### 2.1 Current CSV Status
The current untracked recovery CSV [firestarterog_binance_20_symbol_cell1_recovery.csv](file:///C:/firestarterspb/reports/firestarterog_binance_20_symbol_cell1_recovery.csv) contains **18 columns** representing the core Cell 1 outputs.

### 2.2 Missing Fields Identified
The CSV is **missing the following 5 columns** required by the Cell 2 dust cleaner:
1. `is_stock_token`
2. `risk_pct`
3. `invalidation_distance`
4. `ignition_momentum`
5. `ignition_participation`

Additionally, helper fields used to calculate the above values (such as `stop`, `tp1`, `tp2`, and `trigger_above`) are calculated in memory during the scan but are not preserved in the CSV.

---

## 3. Neutral Label Mapping

To prevent research candidate scans from being misinterpreted as active trading alerts, the original Cell 2 labels must be mapped to neutral research-oriented labels in all generated reports:

* **SCOUT BUY** $\rightarrow$ `scout_class_candidate`
* **TRIGGER BUY** $\rightarrow$ `trigger_class_candidate`
* **PULLBACK ONLY** $\rightarrow$ `extended_watch_candidate`
* **NO TOUCH** $\rightarrow$ `rejected_candidate`

---

## 4. Dry-Run Execution Steps

The dry-run will be conducted in a two-stage process:

### Stage 1: Extend Cell 1 Output
1. Modify the recovery scan script `scripts/recovery_test_20_symbol.py` to include the missing fields (`is_stock_token`, `risk_pct`, `invalidation_distance`, `ignition_momentum`, `ignition_participation`, `stop`, `tp1`, `tp2`, `trigger_above`) in its CSV serialization.
2. Re-run the scan script to generate a complete `firestarterog_binance_20_symbol_cell1_recovery.csv` containing all 26 columns.

### Stage 2: Cell 2 Gate Execution
1. Create a script `scripts/dry_run_cell2.py`.
2. **Boolean Normalization:** Convert `near_breakout`, `clean_reclaim`, and `above_4h_trend` to clean booleans.
3. **Asset Filter:** Filter out any symbol where `is_stock_token` is True.
4. **Gate Calculations:**
   * `risk_ok = (risk_pct <= 5.0) & (invalidation_distance != "BAD")`
   * `not_too_late = change_24h_% <= 16.0`
   * `participation_ok = (ignition_participation == "PASS") | (rvol_4h_window >= 1.25) | (volume_usd >= 10_000_000)`
   * `structure_ok = (near_breakout == True) | (range_pos_20 >= 0.60) | (range_pos_50_4h >= 0.60)`
5. **Neutral Candidate Classification:**
   * **scout_class_candidate:** `risk_ok & not_too_late & participation_ok & structure_ok & (ignition_momentum == "PASS") & (raw_score >= 6.75) & (fmlc >= 9.0) & (flowprint >= 5.0) & (risk_pct <= 3.5)`
   * **trigger_class_candidate:** `risk_ok & not_too_late & participation_ok & structure_ok & (((raw_score >= 6.5) & (fmlc >= 8.0)) | ((er >= 6.0) & (fmlc >= 9.0) & (flowprint >= 5.0)) | (change_24h_%.between(3, 12) & (fmlc >= 9.0)))`
   * **extended_watch_candidate (pullback_only):** Mapped when a symbol is a strong mover (`change_24h_% > 16.0`) but fails the extension boundaries.
   * **rejected_candidate:** All other rows that do not meet the criteria (Default action).
6. **Reason Text Generation:** Output clear explanation text mapping the exact check failures (e.g., `"Rejected: invalidation too wide"` or `"Rejected: weak participation"`).
7. Save the outputs locally as `reports/firestarterog_cell2_dry_run_recovery.csv` (Untracked) and generate the audit markdown report.

---

## 5. Safety Boundaries

* **No Production Signals:** Dry-run results must be kept strictly local and labeled as research candidates. Do not post active signals or alerts to Slack.
* **No Key/Secret Commit:** Keep all secrets and tokens out of the codebase.
* **No Raw Data Commit:** The generated CSV file must be added to `.gitignore` or kept untracked, and must not be committed to GitHub.

---

## 6. Status & Recommendation

### Recommendation
**HOLD** on Cell 2 dry-run execution. 

The current Cell 1 CSV has a confirmed field gap. We should proceed to stage 1 (modifying the scan script to save the missing fields) before we execute the Cell 2 script.

### Status Markers
* Pass Condition: `PASS_FIRESTARTEROG_CELL2_DRY_RUN_PLAN_READY`
* Hold Condition: `HOLD_FIRESTARTEROG_CELL2_PLAN_FIELD_GAP`

The dry-run plan is ready for review:
`PASS_FIRESTARTEROG_CELL2_DRY_RUN_PLAN_READY`
