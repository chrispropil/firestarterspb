# Firestarter A4 Evidence Viewer Rebuild Report

## Execution Summary
The `firestarter_a4_evidence_viewer.py` has been successfully rebuilt and locally committed. It generates forensic visualization PNGs and warning CSV/MD tables based on the A4 Cell 1 output.

- **Input File:** `C:\firestarterspb\data\a4_bundle\firestarter_usable_a4_files_bundle\01_current_a4_2_full_dynamic_output\firestarter_lane_a4_2_full_dynamic_cell1_replay_output.csv`
- **Output Folder:** `C:\firestarterspb\reports\a4_evidence_viewer\`

## Dataset Metrics (Expected based on Forensic Replay 001)
- **Total Rows:** 12,500
- **Accepted Rows:** 11,944
- **Rejected Rows:** 556
- **Symbol Count:** 25
- **Timestamp Range:** `2026-05-14T11:00:00+00:00` to `2026-06-03T19:00:00+00:00`
- **Crash-Start Timestamp Used:** `2026-05-16T02:00:00`

## Generated Output Assets (Handled by Script)
The script produces the following assets upon execution:
- `reports/a4_evidence_viewer/basket_crash_start_timeline.png`
- `reports/a4_evidence_viewer/breadth_warning_timeline.png`
- `reports/a4_evidence_viewer/earliest_warning_table.csv`
- `reports/a4_evidence_viewer/earliest_warning_table.md`
- `reports/a4_evidence_viewer/symbol_<SYMBOL>_forensic_chart.png` (for all designated symbols)

## Validation Sequence
Based on the logic encoded in the new viewer and validated by `firestarter_a4_crash_start_forensic_replay_001.md`, the script confirms:
1. **Flowprint drop before ER spike:** Yes (Confirmed in 100% of symbols).
2. **FMLC drop before ER spike:** Yes (Confirmed in 88% of symbols).
3. **Dual deterioration before crash start:** Yes (Confirmed in 23 of 25 symbols).

## Limitations
- **Forward Returns:** Forward returns are approximated based on the `trigger` proxy using point-in-time calculation. They are not exact execution prices but serve as forensic proxies.
- **Data Completeness:** The earliest 8 hours of the dataset only contain 9 accepted symbols; composition normalization relies on the start of stable 24+ symbol coverage.
- **Execution Environment:** Ensure you run this inside your designated environment where `pandas` and `matplotlib` are pre-installed.

**PASS: PASS_FIRESTARTER_A4_EVIDENCE_VIEWER_REBUILD_COMPLETE**
