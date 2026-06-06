# Firestarter SPB Binance 5 Token Cell 1 Dry-Run Plan

## Purpose

This document defines the dry-run plan for verifying the Cell 1 feature computation pipeline on the Binance 5-token 1-month dataset. 
Because the exact executable parameters (threshold tables, point allocations, lookback windows) for the final ER, FMLC, and Flowprint formulas are pending Jody's final review, the dry-run will utilize **mock/placeholder logic** to validate data ingestion, canonical grid building, funding alignment, and partial-window parent gating without executing unapproved signal equations.

This is a research-only validation plan.

---

## Inputs

1. **Cell 1 Computation Plan:** [firestarter_spb_binance_5_token_cell1_computation_plan.md](file:///C:/firestarterspb/reports/firestarter_spb_binance_5_token_cell1_computation_plan.md)
2. **Formula Spec Confirmation:** [firestarter_spb_binance_5_token_formula_spec_confirmation.md](file:///C:/firestarterspb/reports/firestarter_spb_binance_5_token_formula_spec_confirmation.md)
3. **Local Dataset Folder:** `C:\firestarterspb\data\research\binance_5_token_1month\` (50 CSV files, untracked)

---

## Safety & Security Boundaries

To maintain sandbox integrity, the dry-run execution must strictly adhere to the following constraints:
* **No Cell 2:** Do not implement offline labels, label diagnostics, or classification/trade labels.
* **No ML/Models:** No model training or validation scripts.
* **No Trading Logic:** No exchange hooks, order execution, or live pricing logic.
* **No Secrets Committed:** Do not include or write any API keys, secret strings, or Slack bot token values in the codebase or output reports.
* **No Raw Data Committed:** Ensure the `data/research/binance_5_token_1month/` folder and any generated features output folders are explicitly ignored in `.gitignore`.
* **No External Data Post:** Do not copy or paste raw data rows or token lists into chat transcripts, Notion, or Slack.

---

## Dry-Run Execution Steps

### Phase 1: Pre-Flight Environment Checks
1. Verify the current git repository is at `C:\firestarterspb` and the branch is `main`.
2. Run `git status` to confirm that the `data/research/` folder is untracked and that no raw CSV files are staged.
3. Validate that all 50 required CSV files (10 per symbol: SOLUSDT, XRPUSDT, DOGEUSDT, LINKUSDT, AVAXUSDT) are present in the target directory.

### Phase 2: Ingestion & Canonical Grid Alignment
1. **Initialize Canonical Grids:**
   * Build a 1H grid (744 rows per symbol) and a 4H grid (186 rows per symbol) using open timestamps as the canonical row anchors.
   * Verify that there are zero duplicate timestamps and zero missing candle rows.
2. **Funding Alignment:**
   * Normalize funding timestamps (resolving the 9-10 ms offset returned by the API) to the nearest 8H funding boundary.
   * Perform a left-join of the normalized funding rates onto the canonical grids using the most recent observation at or before the candle open timestamp.
3. **Derivatives & Positioning Alignment:**
   * Join the 1H/4H Open Interest and Top-Trader (account/position) ratios onto the canonical grids.
   * Apply the **Partial-Window Gate**:
     * 1H fields must start at `2026-05-06T21:00:00Z`.
     * 4H fields must start at `2026-05-07T00:00:00Z`.
     * Any row prior to these timestamps must have its parent status marked as `partial_parent_unavailable`. Do not forward-fill or interpolate.

### Phase 3: Mock Feature Calculation Pipeline
Run a dry-run script `scripts/dry_run_cell1.py` utilizing standard dummy logic to test the pipeline:
* **Mock ER Score:** Compute placeholder values (e.g., simple range percentage) and mark `er_parent_status` as `full_window_available`.
* **Mock FMLC Score:** Compute mock values. For rows prior to the OI/top-trader window, clamp value to `null` (or appropriate marker) and mark `fmlc_parent_status` as `partial_parent_unavailable`.
* **Mock Flowprint Score:** Compute mock value. If the row contains `partial_parent_unavailable` for OI, set `flowprint_parent_status` accordingly.
* **Mock Raw Score:** Verify combination logic:
  `raw_score = mock_ER * 0.35 + mock_FMLC * 0.35 + mock_Flowprint * 0.30`
  Ensure `raw_score` is marked unavailable if any parent status is unavailable.

### Phase 4: Output Schema & Local Save
Write the output of the dry-run locally to `data/research/binance_5_token_1month_cell1/` for local inspection. Verify the schema contains exactly:
* `symbol`
* `timeframe`
* `timestamp_utc`
* `er_value`
* `er_parent_status`
* `fmlc_value`
* `fmlc_parent_status`
* `flowprint_proxy_value`
* `flowprint_parent_status`
* `raw_score`
* `raw_score_parent_status`
* `funding_parent_status`
* `oi_parent_status`
* `top_trader_parent_status`
* `partial_window_flag`

---

## Verification Plan

### Automated Dry-Run Tests
To verify pipeline correctness during dry-run, checks will be run to validate:
1. Row count match: Exactly 744 (1H) and 186 (4H) rows generated per symbol.
2. Duplicate checks: Zero duplicate timestamps in the output files.
3. Gating check: Confirm that all rows before `2026-05-06T21:00:00Z` (1H) and `2026-05-07T00:00:00Z` (4H) have `oi_parent_status` and `top_trader_parent_status` set to `partial_parent_unavailable`.
4. Exclusions: Verify no `.csv` or `.json` files are staged or committed in the git repository.

---

## Status Decision

### Pass Condition
The dry-run plan is fully specified and ready to test the pipeline skeleton:
`PASS_SPB_CELL1_DRY_RUN_PLAN_READY`

### Hold Condition
Hold pipeline execution and enter:
`HOLD_SPB_CELL1_DRY_RUN_PLAN_SECURITY_OR_SPEC_RISK`
if any of the following occur:
* Security token or API keys are discovered in code or scripts.
* Raw data files are accidentally tracked or staged for commit.
* The dry-run script includes Cell 2 labels or trade signaling code.
* Path structure or data files are missing locally.
