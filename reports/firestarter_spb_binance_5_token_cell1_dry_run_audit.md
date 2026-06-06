# Firestarter SPB Binance 5 Token Cell 1 Dry-Run Audit

## Execution Summary

* **Run Timestamp (UTC):** 2026-06-06T23:54:00Z
* **Script Executed:** `scripts/dry_run_cell1.py`
* **Output Folder:** `data/research/binance_5_token_1month_cell1/` (Untracked)
* **Total Output Files:** 10 CSV files (2 per symbol: 1H and 4H grids for SOLUSDT, XRPUSDT, DOGEUSDT, LINKUSDT, AVAXUSDT)
* **Total Output Rows:** 4,650
* **Status:** PASS (All pipeline checks passed, mock calculations validated, and partial-window gates successfully verified)

---

## Ingestion & Integrity Metrics

| Symbol | Timeframe | Expected Rows | Processed Rows | Duplicate Timestamps | Gated Rows (Partial) | Ingestion Status |
|---|---|---|---|---|---|---|
| SOLUSDT | 1h | 744 | 744 | 0 | 21 | OK |
| SOLUSDT | 4h | 186 | 186 | 0 | 6 | OK |
| XRPUSDT | 1h | 744 | 744 | 0 | 21 | OK |
| XRPUSDT | 4h | 186 | 186 | 0 | 6 | OK |
| DOGEUSDT | 1h | 744 | 744 | 0 | 21 | OK |
| DOGEUSDT | 4h | 186 | 186 | 0 | 6 | OK |
| LINKUSDT | 1h | 744 | 744 | 0 | 21 | OK |
| LINKUSDT | 4h | 186 | 186 | 0 | 6 | OK |
| AVAXUSDT | 1h | 744 | 744 | 0 | 21 | OK |
| AVAXUSDT | 4h | 186 | 186 | 0 | 6 | OK |

---

## Verification Plan Audit

1. **Pre-flight Check:** Verified that all 50 required raw CSV files are present in `data/research/binance_5_token_1month/`.
2. **Canonical Grids Integrity:** Ingested candles successfully. Verified that each symbol contains exactly 744 (1H) and 186 (4H) rows, matching 31 days. Duplicates check returned zero.
3. **Funding Rate Alignment:** Successfully corrected the millisecond API timestamp offset by rounding funding timestamps to the nearest 8H boundary. Checked that funding rate joined correctly using latest-value-at-or-before logic.
4. **Derivatives Gating (Partial-Window check):**
   * Verified that all 1H rows before `2026-05-06T21:00:00Z` (exactly 21 rows per symbol) have `oi_parent_status` and `top_trader_parent_status` set to `partial_parent_unavailable`.
   * Verified that all 4H rows before `2026-05-07T00:00:00Z` (exactly 6 rows per symbol) have `oi_parent_status` and `top_trader_parent_status` set to `partial_parent_unavailable`.
5. **Score Gating check:** Verified that `raw_score_parent_status` was successfully gated to `parent_gated_unavailable` for all rows falling in the partial window, and that no mock `raw_score` values were outputted for these periods.
6. **Git Safety Check:** Confirmed that the raw data folder and the newly generated `data/research/binance_5_token_1month_cell1/` features output folder are kept locally and remain untracked. No CSV files are staged or committed.

---

## Safety & Security Boundaries

* **Cell 2 offline labeling files created?** NO
* **ML/Model training scripts executed?** NO
* **Trade signals or execution logic generated?** NO
* **Slack tokens or secrets exposed/printed?** NO

---

## Status Decision

### Pass Condition
The Cell 1 dry-run execution has succeeded and verified pipeline stability:
`PASS_SPB_CELL1_DRY_RUN_AUDIT_READY`

### Hold Condition
Hold pipeline deployment and enter:
`HOLD_SPB_CELL1_DRY_RUN_DATA_OR_SECURITY_RISK`
if any data discrepancies, formatting errors, or security leakages are found.
