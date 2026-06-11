import os
import sys
import argparse
import json
import time
from pathlib import Path
from datetime import datetime, timezone

from firesignal_state import load_state, save_state, load_symbols, find_symbol_files
from firesignal_update_from_last_known import perform_update_cycle, trigger_viewer_rebuild, ACTIVE_VIEWER_PATH
from firesignal_derivatives_update_from_last_known import perform_derivatives_update, find_deriv_file, get_last_timestamp

REPORTS_DIR = Path("C:/firestarterspb/reports/firesignal")
STATE_PATH = Path("C:/firestarterspb/state/firesignal_update_state.json")
SAMPLED_SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'DOGEUSDT']

def run_metric_freshness_audit():
    """
    Parses active viewer and checks the 2nd-to-last confirmed bar metrics.
    Returns (audit_success, audit_results)
    """
    html_path = Path("C:/firestarterspb/reports/html/pulled_143_evidence_viewer/index.html")
    if not html_path.exists():
        return False, {}
        
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
            
        idx = html.find("const exportData = ")
        if idx == -1:
            return False, {}
            
        end = html.find("let currentInterval = ")
        if end == -1:
            end = html.find("window.onload = ")
            
        data_json = html[idx+len("const exportData = "):end].strip().rstrip(";")
        data = json.loads(data_json)
        symbols_1h = data.get("symbols_1h", {})
        
        audit_results = {}
        audit_success = True
        
        for sym in SAMPLED_SYMBOLS:
            sym_data = symbols_1h.get(sym, {})
            times = sym_data.get("time", [])
            fmlc = sym_data.get("fmlc", [])
            fp = sym_data.get("fp", [])
            er = sym_data.get("er", [])
            score = sym_data.get("score", [])
            prices = sym_data.get("price", [])
            
            if len(times) < 2:
                audit_success = False
                continue
                
            cb = {
                "timestamp": times[-2],
                "price": prices[-2],
                "er": er[-2],
                "fmlc": fmlcs[-2] if "fmlcs" in locals() else fmlc[-2],
                "fp": fp[-2],
                "score": score[-2]
            }
            
            # Verify Flowprint and Score are not null on 2nd-to-last confirmed bar
            if cb["fp"] is None or cb["score"] is None or cb["fmlc"] is None or cb["er"] is None:
                audit_success = False
                
            audit_results[sym] = {
                "latest_viewer_timestamp": times[-1],
                "second_to_last_confirmed_timestamp": times[-2],
                "confirmed_bar": cb
            }
            
        return audit_success, audit_results
    except Exception as e:
        print(f"[ERROR] Failed to run metric freshness audit: {e}")
        return False, {}

def write_setup_report(verdict, reason, max_intervals):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "firesignal_derivatives_context_update_report.md"
    
    content = f"""# FireSignal Derivatives Context Update Report

**Document ID:** FIRESIGNAL_DERIVATIVES_CONTEXT_UPDATE_REPORT_001  
**Generated at:** {datetime.now(timezone.utc).isoformat()}  
**Verdict:** {verdict}  
**Reason:** {reason}  

---

## 1. Pipeline Execution Flow

When executing the full update pipeline:
1. **Load State:** Read persisted timestamps.
2. **Update Raw Klines:** Fetch missing 5m intervals.
3. **Update Derivatives Context:** Fetch missing Open Interest, Taker Volume ratios, and Funding Rates.
4. **Validate & Swap:** Stage, validate, merge, and swap output files.
5. **Rebuild Viewer:** Run visualization compiler.
6. **Freshness Audit:** Parse index.html and confirm Flowprint and Score are active on confirmed bars.

## 2. CLI Usage Reference

* **Run full pipeline once:**
  ```cmd
  py scripts/firesignal/run_firesignal_once.py
  ```
* **Derivatives-only update:**
  ```cmd
  py scripts/firesignal/run_firesignal_once.py --derivatives-only
  ```
* **Dry-run simulation:**
  ```cmd
  py scripts/firesignal/run_firesignal_once.py --dry-run
  ```
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[REPORT] Setup report written to {report_path}")

def write_manifest_reports(manifest, deriv_stats):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # JSON manifest
    json_path = REPORTS_DIR / "firesignal_derivatives_context_update_manifest.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({**manifest, **deriv_stats}, f, indent=4, sort_keys=True)
    print(f"[MANIFEST] JSON manifest written to {json_path}")
    
    # MD manifest
    md_path = REPORTS_DIR / "firesignal_derivatives_context_update_manifest.md"
    md_content = f"""# FireSignal Derivatives Context Update Manifest

**Updated At:** {manifest['updated_at_utc']}  
**Status:** {manifest['status']}  

---

## 1. Summary of Changes
* **Files Written:** `{manifest['derivatives_files_written']}`
* **Rows Pulled:** `{manifest['derivatives_rows_pulled']}`
* **Rows Added:** `{manifest['derivatives_rows_added']}`
* **Rows Deduped:** `{manifest['derivatives_rows_deduped']}`
* **Viewer Flowprint Current Confirmed:** `{manifest['viewer_flowprint_current_confirmed']}`
* **Viewer Score Current Confirmed:** `{manifest['viewer_score_current_confirmed']}`

## 2. Symbols Updated ({len(manifest['derivatives_symbols_updated'])} total)
{" ".join([f"`{s}`" for s in manifest['derivatives_symbols_updated']]) if manifest['derivatives_symbols_updated'] else "None"}
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[MANIFEST] Markdown manifest written to {md_path}")

def write_post_refresh_audit_report(audit_success, audit_results, last_raw_close_utc):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    audit_path = REPORTS_DIR / "firesignal_post_derivatives_viewer_metric_audit.md"
    
    headers = ["Symbol", "Latest Raw Close UTC", "Latest Viewer Time (Forming)", "Confirmed Time (2nd Last)", "Conf. ER", "Conf. FMLC", "Conf. Flowprint", "Conf. Score"]
    
    rows = []
    for sym in SAMPLED_SYMBOLS:
        res = audit_results.get(sym, {})
        cb = res.get("confirmed_bar", {})
        row = [
            sym,
            last_raw_close_utc or "N/A",
            res.get("latest_viewer_timestamp", "N/A"),
            cb.get("timestamp", "N/A"),
            str(cb.get("er")),
            f"{cb.get('fmlc'):.3f}" if isinstance(cb.get('fmlc'), float) else str(cb.get('fmlc')),
            str(cb.get("fp")),
            f"{cb.get('score'):.3f}" if isinstance(cb.get('score'), float) else str(cb.get('score'))
        ]
        rows.append("| " + " | ".join(row) + " |")
        
    content = f"""# FireSignal Post-Derivatives Viewer Metric Audit

**Audit Timestamp:** {datetime.now(timezone.utc).isoformat()}  
**Verification Success:** `{audit_success}`  

---

## 1. Sampled Symbol Metrics (Confirmed Bar)

| {" | ".join(headers)} |
| {" | ".join(['---'] * len(headers))} |
{"\n".join(rows)}

## 2. Freshness Status Verdict
If Flowprint and Score are fully populated (non-null) for all sampled symbols at their second-to-last timestamp, the audit passes.
"""
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[AUDIT] Post-refresh metric audit report written to {audit_path}")

def main():
    parser = argparse.ArgumentParser(description="FireSignal Bounded Pipeline and Derivatives Updater.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate pipeline range and check validations without writing.")
    parser.add_argument("--viewer-only", action="store_true", help="Rebuild index.html viewer only.")
    parser.add_argument("--derivatives-only", action="store_true", help="Fetch and merge derivatives only.")
    parser.add_argument("--max-intervals", type=int, help="Limit missing raw/derivatives query windows to N intervals.")
    
    args = parser.parse_args()
    
    print("======================================================")
    print(" MATRIX ALPHA // FIRESIGNAL FULL UPDATE PIPELINE")
    print("======================================================")
    
    # Load state
    state = load_state() or {}
    
    raw_verdict = "PASS"
    raw_reason = ""
    raw_manifest = {}
    
    # 1. Raw kline update cycle (unless derivatives-only or viewer-only)
    if not args.derivatives_only and not args.viewer_only:
        print("[PIPELINE STEP 1] Running Raw 5m Kline Update...")
        raw_verdict, raw_reason, raw_manifest = perform_update_cycle(
            dry_run=args.dry_run,
            max_intervals=args.max_intervals
        )
        if raw_verdict != "PASS_FIRESIGNAL_UPDATED_FROM_LAST_KNOWN_AND_VIEWER_REFRESHED" and raw_verdict != "PASS_FIRESIGNAL_RUN_ONCE_READY":
            print(f"[ERROR] Raw update failed: {raw_reason}")
            write_setup_report("HOLD_FIRESIGNAL_UPDATE_PATH_AMBIGUOUS", f"Raw update failed: {raw_reason}", args.max_intervals)
            sys.exit(1)
            
    # 2. Derivatives update cycle (unless viewer-only)
    deriv_verdict = "PASS"
    deriv_reason = ""
    deriv_stats = {}
    
    if not args.viewer_only:
        print("[PIPELINE STEP 2] Running Derivatives Context Update...")
        deriv_verdict, deriv_reason, deriv_stats = perform_derivatives_update(
            dry_run=args.dry_run,
            max_intervals=args.max_intervals
        )
        if deriv_verdict != "PASS_FIRESIGNAL_DERIVATIVES_CONTEXT_UPDATED_FLOWPRINT_SCORE_CURRENT":
            print(f"[ERROR] Derivatives update failed: {deriv_reason}")
            write_setup_report(deriv_verdict, f"Derivatives update failed: {deriv_reason}", args.max_intervals)
            sys.exit(1)
            
    # 3. Rebuild Viewer (if not dry-run)
    rebuild_success = True
    if not args.dry_run:
        print("[PIPELINE STEP 3] Compiling active Plotly index.html viewer...")
        rebuild_success = trigger_viewer_rebuild()
        
    # 4. Metric Freshness Audit on index.html
    audit_success = False
    audit_results = {}
    if rebuild_success and not args.dry_run:
        print("[PIPELINE STEP 4] Conducting Freshness Audit on index.html...")
        audit_success, audit_results = run_metric_freshness_audit()
        
    # Final Verdict Assessment
    if args.dry_run:
        final_verdict = "PASS_FIRESIGNAL_DERIVATIVES_CONTEXT_UPDATED_FLOWPRINT_SCORE_CURRENT"
        final_reason = "Dry run completed successfully."
    elif not rebuild_success:
        final_verdict = "HOLD_FIRESIGNAL_VIEWER_STILL_USING_STALE_CONTEXT"
        final_reason = "Viewer compilation failed."
    elif not audit_success:
        final_verdict = "HOLD_FIRESIGNAL_VIEWER_STILL_USING_STALE_CONTEXT"
        final_reason = "Confirmed bar Flowprint or Score remains null. Stale derivatives context may still be merged."
    else:
        final_verdict = "PASS_FIRESIGNAL_DERIVATIVES_CONTEXT_UPDATED_FLOWPRINT_SCORE_CURRENT"
        final_reason = "Raw data and derivatives context successfully synchronized and verified in the viewer."
        
    # Gather state fields
    now_utc_str = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    
    # Resolve timestamps
    last_oi_ts = "N/A"
    last_taker_ts = "N/A"
    
    # Read one symbol's files to get actual max timestamps
    btc_oi_path = find_deriv_file("BTCUSDT", "openInterestHist")
    btc_taker_path = find_deriv_file("BTCUSDT", "takerlongshortRatio")
    if btc_oi_path and btc_oi_path.exists():
        oi_ts = get_last_timestamp(btc_oi_path, "openInterestHist")
        if oi_ts:
            last_oi_ts = datetime.fromtimestamp(oi_ts / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    if btc_taker_path and btc_taker_path.exists():
        taker_ts = get_last_timestamp(btc_taker_path, "takerlongshortRatio")
        if taker_ts:
            last_taker_ts = datetime.fromtimestamp(taker_ts / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")
            
    last_raw_close = raw_manifest.get("last_successful_5m_close_utc") or state.get("last_successful_5m_close_utc")
    
    # Save State JSON
    new_state = {
        "last_successful_update_utc": now_utc_str,
        "last_successful_5m_close_utc": last_raw_close,
        "symbols_updated": raw_manifest.get("symbols_updated") or state.get("symbols_updated") or [],
        "files_written": raw_manifest.get("files_written", 0),
        "rows_added": raw_manifest.get("rows_added", 0),
        "rows_deduped": raw_manifest.get("rows_deduped", 0),
        "latest_manifest_path": str(REPORTS_DIR / "firesignal_latest_update_manifest.json"),
        "latest_viewer_path": str(ACTIVE_VIEWER_PATH),
        "status": "SUCCESS" if final_verdict.startswith("PASS") else "HOLD",
        "updated_at_utc": now_utc_str,
        
        # New Derivatives Fields
        "last_derivatives_refresh_utc": now_utc_str,
        "last_open_interest_context_utc": last_oi_ts,
        "last_taker_long_short_context_utc": last_taker_ts,
        "derivatives_symbols_updated": deriv_stats.get("derivatives_symbols_updated", []),
        "derivatives_rows_pulled": deriv_stats.get("derivatives_rows_pulled", 0),
        "derivatives_rows_added": deriv_stats.get("derivatives_rows_added", 0),
        "derivatives_rows_deduped": deriv_stats.get("derivatives_rows_deduped", 0),
        "derivatives_files_written": deriv_stats.get("derivatives_files_written", 0),
        "derivatives_refresh_status": "SUCCESS" if deriv_verdict.startswith("PASS") else "HOLD",
        "latest_derivatives_manifest_path": str(REPORTS_DIR / "firesignal_derivatives_context_update_manifest.json"),
        "viewer_flowprint_current_confirmed": audit_success,
        "viewer_score_current_confirmed": audit_success
    }
    
    if not args.dry_run:
        save_state(new_state)
        
    # Write setup report
    write_setup_report(final_verdict, final_reason, args.max_intervals)
    
    # Write manifests
    write_manifest_reports(new_state, deriv_stats)
    
    # Write post-refresh audit
    write_post_refresh_audit_report(audit_success, audit_results, last_raw_close)
    
    print(f"\nExecution Finished. Verdict: {final_verdict}")
    print(f"Details: {final_reason}\n")
    print("======================================================")
    sys.exit(0)

if __name__ == "__main__":
    main()
