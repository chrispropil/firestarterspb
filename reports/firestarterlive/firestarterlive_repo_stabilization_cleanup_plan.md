# FirestarterLive Repo Stabilization Cleanup Plan

## Status
**Pending Cleanup Before Phase B**

## Context
The FirestarterLive Phase A scaffold is complete (PASS_PHASE_A_SCAFFOLD_CREATED). The Stage 2 Live Audit script has been committed (`a56cc8fc4f3498411dcda945b70cf2c448065f52`). Before beginning Phase B (dry-run scenario evaluator), the repository contains several untracked reporting artifacts and one modified visualization script that must be classified and managed.

## Current Git Status
```text
 M scripts/visualization/build_top100_evidence_viewer.py
?? reports/firestarter_a4_evidence_viewer_rebuild_report.md
?? reports/firestarter_a4_evidence_viewer_recovery_plan.md
?? reports/firestarter_a4_evidence_viewer_recovery_report.md
?? reports/firestarter_a4_viewer_contact_sheet_report.md
?? reports/firestarter_core88_pulled_symbols_inventory.md
?? reports/firestarter_spb_binance_5_token_6month_expansion_plan.md
?? reports/firestarter_spb_binance_top100_1month_data_pull_script_plan.md
?? reports/firestarter_spb_pulled_143_evidence_viewer_build_audit.md
?? reports/firestarterlive/firestarterlive_repo_stabilization_cleanup_plan.md
```

## File Classification

| File | Status | Category | Action |
|---|---|---|---|
| `scripts/visualization/build_top100_evidence_viewer.py` | Modified | viewer / visualization | Commit |
| `reports/firestarter_spb_pulled_143_evidence_viewer_build_audit.md` | Untracked | viewer / visualization | Commit |
| `reports/firestarter_a4_evidence_viewer_rebuild_report.md` | Untracked | viewer / visualization | Commit |
| `reports/firestarter_a4_evidence_viewer_recovery_plan.md` | Untracked | viewer / visualization | Commit |
| `reports/firestarter_a4_evidence_viewer_recovery_report.md` | Untracked | viewer / visualization | Commit |
| `reports/firestarter_a4_viewer_contact_sheet_report.md` | Untracked | viewer / visualization | Commit |
| `reports/firestarter_core88_pulled_symbols_inventory.md` | Untracked | data pull / expansion planning | Commit |
| `reports/firestarter_spb_binance_5_token_6month_expansion_plan.md` | Untracked | data pull / expansion planning | Commit |
| `reports/firestarter_spb_binance_top100_1month_data_pull_script_plan.md` | Untracked | data pull / expansion planning | Commit |
| `reports/firestarterlive/firestarterlive_repo_stabilization_cleanup_plan.md` | Untracked | FirestarterLive framework | Commit |

## Recommended Commit Groups

**Group 1: Evidence Viewer Rewire & A4 Recovery**
- `scripts/visualization/build_top100_evidence_viewer.py`
- `reports/firestarter_spb_pulled_143_evidence_viewer_build_audit.md`
- `reports/firestarter_a4_evidence_viewer_rebuild_report.md`
- `reports/firestarter_a4_evidence_viewer_recovery_plan.md`
- `reports/firestarter_a4_evidence_viewer_recovery_report.md`
- `reports/firestarter_a4_viewer_contact_sheet_report.md`
*Message: "Update Evidence Viewer for 143 pulled symbols and A4 recovery"*

**Group 2: Data Pull & Expansion Planning**
- `reports/firestarter_core88_pulled_symbols_inventory.md`
- `reports/firestarter_spb_binance_5_token_6month_expansion_plan.md`
- `reports/firestarter_spb_binance_top100_1month_data_pull_script_plan.md`
*Message: "Add Core88 inventory and data expansion planning documents"*

**Group 3: FirestarterLive Stabilization**
- `reports/firestarterlive/firestarterlive_repo_stabilization_cleanup_plan.md`
*Message: "Add FirestarterLive Phase A/B stabilization plan"*

## Files to Hold / Park
Currently, all tracked/untracked files relate to completed research blocks. None specifically need to be parked as `untracked` indefinitely unless we prefer to leave the `.md` reports uncommitted. To strictly clean the repo before Phase B, all the above should be committed.

## Phase B Readiness
**Phase B CAN start after the cleanup above.** Once the repo is committed and clean, we can safely scaffold and build the Phase B dry-run scenario evaluator without mixing visualization or data-planning commits with the core framework.
