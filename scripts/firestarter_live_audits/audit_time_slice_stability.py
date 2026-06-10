import argparse
import csv
import sys
import os
from datetime import datetime, timedelta
from collections import Counter, defaultdict

# Stage 1 baseline constants
BASELINE_TOP_SYMBOL_SHARE_PCT = 30.77
BASELINE_TOP_SYMBOL = "HOMEUSDT"
BASELINE_CLUSTERED_EVENTS = 13
BASELINE_RAW_MATCHES = 26

def parse_args():
    parser = argparse.ArgumentParser(description="Stage 2 Time-Slice Stability Validation")
    parser.add_argument("--slice-days", type=int, default=28)
    parser.add_argument("--fingerprint", type=str, default="fmlc_hanger_local_review_003_tight_cluster24")
    parser.add_argument("--input", type=str, default="reports/firestarter_live_audits/ai_match_index.csv")
    parser.add_argument("--out-md", type=str, default="reports/firestarter_live_audits/validation/fmlc_hanger_local_review_003_time_slice_stability.md")
    parser.add_argument("--out-csv", type=str, default="reports/firestarter_live_audits/validation/fmlc_hanger_local_review_003_slice_metrics.csv")
    return parser.parse_args()

def fail_exit(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

def filter_matches(input_path):
    if not os.path.exists(input_path):
        fail_exit(f"Input file missing: {input_path}")
    
    matches = []
    try:
        with open(input_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            if not headers:
                fail_exit(f"File empty or unreadable: {input_path}")
            
            req_cols = ["timestamp", "symbol", "fmlc", "er", "flowprint", "raw_score"]
            for c in req_cols:
                if c not in headers:
                    fail_exit(f"Missing required column '{c}' in {input_path}")
            
            for r in reader:
                # Using the already accepted Stage 1 fingerprint identity only, not inventing new parameters.
                # Since the index does not contain pre-computed advanced features like prior_return_pct 
                # (which are calculated via history loading in the original search script), 
                # we apply the core fingerprint thresholds natively present in the index as an unavoidable fallback.
                try:
                    fmlc = float(r["fmlc"])
                    er = float(r["er"])
                    flowprint = float(r["flowprint"])
                    raw_score = float(r["raw_score"])
                except ValueError:
                    continue
                
                if fmlc >= 8 and er <= 1.5 and flowprint <= 2 and raw_score <= 3.5:
                    matches.append(r)
    except Exception as e:
        fail_exit(f"Error reading {input_path}: {e}")
    
    return matches

def parse_dt(ts_str):
    ts_str = ts_str.replace("Z", "+0000")
    try:
        return datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        try:
            return datetime.strptime(ts_str[:19], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return None

def cluster_matches_conservative(matches):
    # Conservative fallback clustering: group by symbol, consecutive matches <= 24h are same event
    by_sym = defaultdict(list)
    for m in matches:
        dt = parse_dt(m["timestamp"])
        if dt:
            by_sym[m["symbol"]].append((dt, m))
    
    events = []
    for sym, sym_matches in by_sym.items():
        sym_matches.sort(key=lambda x: x[0])
        current_cluster = []
        for dt, m in sym_matches:
            if not current_cluster:
                current_cluster.append((dt, m))
            else:
                last_dt = current_cluster[-1][0]
                if (dt - last_dt).total_seconds() <= 24 * 3600:
                    current_cluster.append((dt, m))
                else:
                    events.append({
                        "symbol": sym,
                        "event_start": current_cluster[0][0],
                        "event_end": current_cluster[-1][0],
                        "match_count": len(current_cluster)
                    })
                    current_cluster = [(dt, m)]
        if current_cluster:
            events.append({
                "symbol": sym,
                "event_start": current_cluster[0][0],
                "event_end": current_cluster[-1][0],
                "match_count": len(current_cluster)
            })
    return events

def main():
    args = parse_args()
    os.makedirs(os.path.dirname(args.out_md), exist_ok=True)
    
    matches = filter_matches(args.input)
    if not matches:
        fail_exit("No matches found after filtering")
        
    events = cluster_matches_conservative(matches)
    if not events:
        fail_exit("No events formed after clustering")
        
    all_dts = [parse_dt(m["timestamp"]) for m in matches if parse_dt(m["timestamp"])]
    if not all_dts:
        fail_exit("No valid timestamps found")
        
    min_dt = min(all_dts)
    max_dt = max(all_dts)
    
    slices = []
    curr_start = min_dt
    slice_id = 1
    
    while curr_start <= max_dt:
        curr_end = curr_start + timedelta(days=args.slice_days)
        
        slice_matches = [m for m in matches if parse_dt(m["timestamp"]) and curr_start <= parse_dt(m["timestamp"]) < curr_end]
        slice_events = [e for e in events if curr_start <= e["event_start"] < curr_end]
        
        raw_match_count = len(slice_matches)
        clustered_event_count = len(slice_events)
        
        event_symbols = Counter(e["symbol"] for e in slice_events)
        symbol_count = len(event_symbols)
        
        if event_symbols:
            top_symbol, top_symbol_event_count = event_symbols.most_common(1)[0]
            top_symbol_share_pct = (top_symbol_event_count / clustered_event_count) * 100
        else:
            top_symbol = "None"
            top_symbol_event_count = 0
            top_symbol_share_pct = 0.0
            
        delta_vs_baseline_pp = top_symbol_share_pct - BASELINE_TOP_SYMBOL_SHARE_PCT
        
        if clustered_event_count < 5:
            stability_flag = "ANOMALY"
        elif abs(delta_vs_baseline_pp) <= 10:
            stability_flag = "STABLE"
        elif 10 < abs(delta_vs_baseline_pp) <= 20:
            stability_flag = "DRIFT"
        else:
            stability_flag = "ANOMALY"
            
        slices.append({
            "slice_id": slice_id,
            "start_date": curr_start.strftime("%Y-%m-%d"),
            "end_date": curr_end.strftime("%Y-%m-%d"),
            "raw_match_count": raw_match_count,
            "clustered_event_count": clustered_event_count,
            "symbol_count": symbol_count,
            "top_symbol": top_symbol,
            "top_symbol_event_count": top_symbol_event_count,
            "top_symbol_share_pct": top_symbol_share_pct,
            "delta_vs_baseline_pp": delta_vs_baseline_pp,
            "stability_flag": stability_flag
        })
        
        curr_start = curr_end
        slice_id += 1
        
    valid_slices = slices
    n_valid = len(valid_slices)
    n_stable = sum(1 for s in valid_slices if s["stability_flag"] == "STABLE")
    n_drift = sum(1 for s in valid_slices if s["stability_flag"] == "DRIFT")
    n_anomaly = sum(1 for s in valid_slices if s["stability_flag"] == "ANOMALY")
    
    stable_pct = (n_stable / n_valid) * 100 if n_valid > 0 else 0
    
    shares = [s["top_symbol_share_pct"] for s in valid_slices if s["clustered_event_count"] >= 5]
    mean_share = sum(shares) / len(shares) if shares else 0
    mean_delta_pp = mean_share - BASELINE_TOP_SYMBOL_SHARE_PCT

    decision = "PASS"
    if stable_pct < 40 or n_anomaly >= 2 or abs(mean_delta_pp) > 20:
        decision = "FAIL"
    elif 40 <= stable_pct < 70 or n_anomaly == 1 or 15 < abs(mean_delta_pp) <= 20:
        decision = "WARN"
    elif stable_pct >= 70 and n_anomaly == 0 and abs(mean_delta_pp) <= 15:
        decision = "PASS"
    else:
        decision = "FAIL"

    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["slice_id", "start_date", "end_date", "raw_match_count", "clustered_event_count", "symbol_count", "top_symbol", "top_symbol_event_count", "top_symbol_share_pct", "delta_vs_baseline_pp", "stability_flag"])
        total_matches = 0
        total_events = 0
        for s in slices:
            writer.writerow([s["slice_id"], s["start_date"], s["end_date"], s["raw_match_count"], s["clustered_event_count"], s["symbol_count"], s["top_symbol"], s["top_symbol_event_count"], round(s["top_symbol_share_pct"], 2), round(s["delta_vs_baseline_pp"], 2), s["stability_flag"]])
            total_matches += s["raw_match_count"]
            total_events += s["clustered_event_count"]
        writer.writerow(["SUMMARY", "", "", total_matches, total_events, "", "", "", round(mean_share, 2), round(mean_delta_pp, 2), decision])

    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write("# Stage 2 Time-Slice Stability Validation\n\n")
        f.write(f"**Candidate Fingerprint:** `{args.fingerprint}`\n\n")
        f.write("> **Note:** This is research-only validation. No trading claims, no signals, no pattern discovery. Findings are temporal consistency checks only.\n\n")
        f.write("## Stage 1 Baseline Reference\n")
        f.write(f"- Top Symbol Share: {BASELINE_TOP_SYMBOL_SHARE_PCT}%\n")
        f.write(f"- Top Symbol: {BASELINE_TOP_SYMBOL}\n")
        f.write(f"- Clustered Events: {BASELINE_CLUSTERED_EVENTS}\n")
        f.write(f"- Raw Matches: {BASELINE_RAW_MATCHES}\n\n")
        
        f.write("## Configuration\n")
        f.write(f"- Input File: `{args.input}`\n")
        f.write(f"- Slice Days: {args.slice_days}\n\n")
        
        f.write("## Slice-by-Slice Metrics\n")
        f.write("| Slice ID | Start Date | End Date | Matches | Events | Top Symbol | Share % | Delta pp | Flag |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for s in slices:
            f.write(f"| {s['slice_id']} | {s['start_date']} | {s['end_date']} | {s['raw_match_count']} | {s['clustered_event_count']} | {s['top_symbol']} | {s['top_symbol_share_pct']:.2f}% | {s['delta_vs_baseline_pp']:.2f} | {s['stability_flag']} |\n")
        f.write("\n")
        
        f.write("## Stability Summary\n")
        f.write(f"- Total Slices: {n_valid}\n")
        f.write(f"- STABLE: {n_stable}\n")
        f.write(f"- DRIFT: {n_drift}\n")
        f.write(f"- ANOMALY: {n_anomaly}\n")
        f.write(f"- Mean Top-Symbol Share (valid slices): {mean_share:.2f}%\n")
        f.write(f"- Mean Delta vs Baseline: {mean_delta_pp:.2f}pp\n\n")
        
        if any(s["clustered_event_count"] < 5 for s in slices):
            f.write("**Sparse Sample Warning:** One or more slices have fewer than 5 clustered events and were flagged as ANOMALY.\n\n")
            
        f.write("## Symbol Concentration Notes\n")
        f.write(f"The baseline concentration was heavily focused on {BASELINE_TOP_SYMBOL}. Drift in top symbol share indicates whether the fingerprint relies on regime-specific behavior from a single asset or generalizes.\n\n")
        
        f.write("## Overall Decision\n")
        f.write(f"**{decision}**\n\n")
        
        f.write("This is research-only validation. No trading claims, no signals, no pattern discovery. Findings are temporal consistency checks only.\n")

    print(f"Validation complete. Decision: {decision}")
    print(f"Slices: {n_valid} (STABLE: {n_stable}, DRIFT: {n_drift}, ANOMALY: {n_anomaly})")

if __name__ == "__main__":
    main()
