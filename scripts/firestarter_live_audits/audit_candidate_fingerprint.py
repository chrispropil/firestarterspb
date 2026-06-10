import csv
import sys
import os
from datetime import datetime
from collections import Counter

MATCHES_PATH = "reports/firestarter_live_audits/pattern_searches/fmlc_hanger_local_review_003_tight_cluster24_matches.csv"
EVENTS_PATH = "reports/firestarter_live_audits/pattern_searches/fmlc_hanger_local_review_003_tight_cluster24_events.csv"
OUT_MD = "reports/firestarter_live_audits/validation/fmlc_hanger_local_review_003_first_pass_validation.md"
OUT_CSV = "reports/firestarter_live_audits/validation/fmlc_hanger_local_review_003_metrics.csv"

def fail_exit(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

def read_csv(path, required_cols):
    if not os.path.exists(path):
        fail_exit(f"File missing: {path}")
    
    rows = []
    try:
        with open(path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            if not headers:
                fail_exit(f"File empty or unreadable: {path}")
            for col in required_cols:
                if col not in headers:
                    fail_exit(f"Missing required column '{col}' in {path}")
            for r in reader:
                rows.append(r)
    except Exception as e:
        fail_exit(f"Error reading {path}: {e}")
    
    return rows

def main():
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)

    matches = read_csv(MATCHES_PATH, ["symbol", "timestamp"])
    events = read_csv(EVENTS_PATH, ["symbol", "event_start", "event_end"])

    if len(matches) == 0:
        fail_exit("Match count is 0")
    if len(events) == 0:
        fail_exit("Event count is 0")

    match_count = len(matches)
    event_count = len(events)

    match_symbols = Counter(r['symbol'] for r in matches)
    event_symbols = Counter(r['symbol'] for r in events)
    
    unique_symbol_count = len(event_symbols)

    top_event_symbol, top_event_cnt = event_symbols.most_common(1)[0] if event_symbols else ("None", 0)
    top_match_symbol, top_match_cnt = match_symbols.most_common(1)[0] if match_symbols else ("None", 0)

    top_event_share = top_event_cnt / event_count if event_count > 0 else 0
    top_match_share = top_match_cnt / match_count if match_count > 0 else 0

    missing_timestamps = sum(1 for r in matches if not r.get("timestamp"))
    missing_event_starts = sum(1 for r in events if not r.get("event_start"))
    missing_pct = max(missing_timestamps / match_count, missing_event_starts / event_count) if match_count > 0 and event_count > 0 else 0

    seen_events = set()
    duplicate_events = 0
    for r in events:
        key = tuple(r.items())
        if key in seen_events:
            duplicate_events += 1
        seen_events.add(key)

    weekly_events = Counter()
    for r in events:
        start_str = r.get("event_start", "")
        if len(start_str) >= 10:
            try:
                dt = datetime.strptime(start_str[:10], "%Y-%m-%d")
                iso_year, iso_week, _ = dt.isocalendar()
                weekly_events[f"{iso_year}-W{iso_week:02d}"] += 1
            except ValueError:
                pass
    
    top_week, top_week_cnt = weekly_events.most_common(1)[0] if weekly_events else ("None", 0)
    top_week_share = top_week_cnt / event_count if event_count > 0 else 0

    fails = []
    warns = []

    if event_count < 10:
        fails.append("clustered events < 10")
    if top_event_share > 0.5:
        fails.append(f"symbol {top_event_symbol} > 50% of clustered events")
    
    if 0.3 < top_event_share <= 0.5:
        warns.append(f"symbol {top_event_symbol} > 30% of clustered events")
    if 10 <= event_count < 30:
        warns.append("clustered events < 30")
    if unique_symbol_count == 1:
        warns.append("symbol count = 1")
    if missing_pct > 0.05:
        warns.append("missing timestamps > 5%")
    if top_week_share > 0.5:
        warns.append(f"week {top_week} > 50% of clustered events")

    decision = "PASS"
    if fails:
        decision = "FAIL"
    elif warns:
        decision = "WARN"

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# First-Pass Candidate Fingerprint Validation\n\n")
        f.write("## Overview\n")
        f.write("This is research-only validation. No trading claims, no signals, no ML. Findings are descriptive only.\n\n")
        
        f.write("## Decision\n")
        f.write(f"**{decision}**\n\n")
        if fails:
            f.write("### Fails\n")
            for msg in fails:
                f.write(f"- {msg}\n")
            f.write("\n")
        if warns:
            f.write("### Warnings\n")
            for msg in warns:
                f.write(f"- {msg}\n")
            f.write("\n")
        
        f.write("## Input Files\n")
        f.write(f"- Matches: `{MATCHES_PATH}`\n")
        f.write(f"- Events: `{EVENTS_PATH}`\n\n")

        f.write("## Counts\n")
        f.write(f"- Raw matches: {match_count}\n")
        f.write(f"- Clustered events: {event_count}\n")
        f.write(f"- Unique symbols: {unique_symbol_count}\n")
        f.write(f"- Top symbol event share: {top_event_share:.2%}\n")
        f.write(f"- Top symbol match share: {top_match_share:.2%}\n")
        f.write(f"- Missing match timestamps: {missing_timestamps}\n")
        f.write(f"- Missing event starts: {missing_event_starts}\n")
        f.write(f"- Duplicate event rows: {duplicate_events}\n\n")

        f.write("## Symbol Concentration\n")
        f.write("| Symbol | Event Count | Event % | Match Count | Match % |\n")
        f.write("|---|---|---|---|---|\n")
        for sym, ecnt in event_symbols.most_common():
            mcnt = match_symbols.get(sym, 0)
            epct = ecnt / event_count
            mpct = mcnt / match_count
            f.write(f"| {sym} | {ecnt} | {epct:.2%} | {mcnt} | {mpct:.2%} |\n")
        f.write("\n")

        f.write("## Weekly Events\n")
        f.write("| Week | Event Count | Event % |\n")
        f.write("|---|---|---|\n")
        for wk, cnt in sorted(weekly_events.items()):
            f.write(f"| {wk} | {cnt} | {cnt/event_count:.2%} |\n")
        f.write("\n")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol", "event_count", "event_pct", "match_count", "match_pct"])
        for sym, ecnt in event_symbols.most_common():
            mcnt = match_symbols.get(sym, 0)
            writer.writerow([sym, ecnt, round(ecnt/event_count, 4), mcnt, round(mcnt/match_count, 4)])
        writer.writerow(["TOTAL", event_count, 1.0, match_count, 1.0])

    print(f"Validation complete. Decision: {decision}")

if __name__ == "__main__":
    main()
