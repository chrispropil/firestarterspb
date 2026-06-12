import argparse
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timezone

input_file = r'reports\firestarter_live_audits\ai_match_index.csv'
output_latest_csv = r'reports\firestarter_live_audits\profile_research_sandbox_latest.csv'
output_events_csv = r'reports\firestarter_live_audits\profile_research_sandbox_events.csv'
output_json = r'reports\firestarter_live_audits\profile_interpreter_read.json'
output_md = r'reports\firestarter_live_audits\profile_interpreter_read.md'
manifest_md = r'reports\firestarter_live_audits\profile_interpreter_manifest.md'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strictness', choices=['loose', 'normal', 'tight'], default='normal')
    return parser.parse_args()

def calculate_price_phase(group):
    closes = group['close'].values
    phases = []
    
    for i in range(len(closes)):
        if i < 5:
            phases.append("NEUTRAL")
            continue
            
        window = closes[max(0, i-6):i+1]
        rmax = np.max(window)
        rmin = np.min(window)
        curr = closes[i]
        prev = closes[i-1]
        ret = (curr - prev) / prev if prev > 0 else 0
        
        range_pct = (rmax - rmin) / rmin if rmin > 0 else 0
        pos_in_range = (curr - rmin) / (rmax - rmin) if rmax > rmin else 0.5
        
        if range_pct > 0.05 and pos_in_range >= 0.8:
            phases.append("EXTENDED")
        elif range_pct < 0.02:
            phases.append("BASE")
        elif ret < -0.01 and pos_in_range < 0.3:
            phases.append("VULNERABLE")
        elif range_pct > 0.04 and pos_in_range < 0.2:
            phases.append("FAILED_RECOVERY")
        elif ret > 0.01 and pos_in_range > 0.5:
            phases.append("GRIND")
        elif ret > 0.02 and pos_in_range > 0.3:
            phases.append("RECLAIM")
        else:
            phases.append("NEUTRAL")
    return phases

def get_thresholds(strictness):
    if strictness == 'tight':
        return {
            'fmlc_hanger': 6.5,
            'fmlc_reawaken': 6.0,
            'fmlc_grind': 6.0,
            'fmlc_late': 7.0,
            'er_reawaken': 4.0,
            'er_grind_pulses': 2,
            'flow_req': True,
            'flow_min': 3.5,
            'rs_req': True,
            'rs_reawaken': 4.5,
            'rs_grind': 4.0,
            'grind_mc': 3,
            'grind_chg': 0.8,
            'grind_max_flow': 4.0,
            'short_chg': -0.5,
            'reawaken_mc': 3
        }
    elif strictness == 'loose':
        return {
            'fmlc_hanger': 4.0,
            'fmlc_reawaken': 4.0,
            'fmlc_grind': 4.0,
            'fmlc_late': 5.0,
            'er_reawaken': 2.0,
            'er_grind_pulses': 1,
            'flow_req': False,
            'flow_min': 2.0,
            'rs_req': False,
            'rs_reawaken': 3.0,
            'rs_grind': 2.5,
            'grind_mc': 1,
            'grind_chg': 0.0,
            'grind_max_flow': 0.0,
            'short_chg': 0.0,
            'reawaken_mc': 1
        }
    else: # normal
        return {
            'fmlc_hanger': 5.0,
            'fmlc_reawaken': 5.0,
            'fmlc_grind': 5.0,
            'fmlc_late': 6.0,
            'er_reawaken': 3.0,
            'er_grind_pulses': 2,
            'flow_req': False,
            'flow_min': 3.0,
            'rs_req': False,
            'rs_reawaken': 4.0,
            'rs_grind': 3.5,
            'grind_mc': 3,
            'grind_chg': 0.5,
            'grind_max_flow': 3.5,
            'short_chg': -0.3,
            'reawaken_mc': 2
        }

def classify_row(row, er_history, rs_history, t):
    fmlc = row.get('fmlc', 0)
    if pd.isna(fmlc): fmlc = 0
    er = row.get('er', 0)
    if pd.isna(er): er = 0
    flowprint = row.get('flowprint', np.nan)
    raw_score = row.get('raw_score', np.nan)
    price_phase = row['price_phase']

    recent_er = er_history[-6:] if len(er_history) >= 6 else er_history
    recent_er_12 = er_history[-12:] if len(er_history) >= 12 else er_history
    recent_rs = rs_history[-6:] if len(rs_history) >= 6 else rs_history

    parent_profile = "UNKNOWN"
    subtype = "UNKNOWN"
    board_read = "UNKNOWN"

    flow_ok = (not pd.isna(flowprint) and flowprint >= t['flow_min']) or (not t['flow_req'] and pd.isna(flowprint))

    # Rule 1: X1_SHORT_REVIEW
    if fmlc >= t['fmlc_hanger'] and er <= 1.0 and price_phase in ['VULNERABLE', 'EXTENDED', 'FAILED_RECOVERY', 'NEUTRAL']:
        if pd.isna(raw_score) or raw_score <= 4.2:
            parent_profile = "FMLC_HANGER"
            subtype = "ER_DEAD / BUSY_REJECTION"
            board_read = "X1_SHORT_REVIEW"

    # Rule 2: X1_REAWAKENING
    prior_er_low = any(e <= 1.0 for e in recent_er[:-1]) if len(recent_er) > 1 else False
    er_rising = (er - recent_er[-2]) > 1.0 if len(recent_er) > 1 else False
    rs_ok_re = (not pd.isna(raw_score) and raw_score >= t['rs_reawaken']) or (not t['rs_req'] and pd.isna(raw_score))

    if fmlc >= t['fmlc_reawaken'] and er >= t['er_reawaken'] and (prior_er_low or er_rising):
        if price_phase in ['BASE', 'GRIND', 'RECLAIM', 'NEUTRAL']:
            if flow_ok and rs_ok_re:
                parent_profile = "FMLC_HANGER"
                subtype = "ER_REAWAKENING / ACTIVE_CHART"
                board_read = "X1_REAWAKENING"
        elif price_phase == 'EXTENDED':
            # EXTENDED becomes LATE_HANGER unless clear reclaim (handled by condition above)
            pass

    # Rule 3: X1_GRIND_ACTIVE
    er_pulses = sum(1 for e in recent_er_12 if e >= 3.0)
    rs_ok_gr = (not pd.isna(raw_score) and raw_score >= t['rs_grind']) or (not t['rs_req'] and pd.isna(raw_score))
    
    if fmlc >= t['fmlc_grind'] and er_pulses >= t['er_grind_pulses'] and price_phase in ['BASE', 'GRIND', 'RECLAIM', 'NEUTRAL']:
        if flow_ok and rs_ok_gr:
            # Overrides short review if both match
            parent_profile = "FMLC_HANGER"
            subtype = "ER_PARTICIPATION_GRIND"
            board_read = "X1_GRIND_ACTIVE"

    # Rule 4: LATE_HIGH_CHURN
    er_mixed = er < 2.0 or (len(recent_er) > 1 and er <= recent_er[-2])
    rs_accel = (len(recent_rs) > 1 and raw_score > recent_rs[-2]) if not pd.isna(raw_score) else False
    
    if price_phase == 'EXTENDED' and fmlc >= t['fmlc_late'] and er_mixed and not rs_accel:
        parent_profile = "FMLC_HANGER"
        subtype = "LATE_HIGH_CHURN"
        board_read = "LATE_HANGER"

    # Rule 5: RESET_IGNITION (Now mapped to something else or excluded if subtype UNKNOWN)
    # Excluded per requirement "Remove UNKNOWN subtype events"
    # Wait, user said: "If X2_STRUCTURE_WATCH has UNKNOWN subtype, exclude it from profile_research_sandbox_events.csv.
    # Keep non-actionable X2 context only in latest summary unless it has a real parent_profile/subtype."
    rs_rising = (len(recent_rs) > 1 and raw_score > recent_rs[-2]) if not pd.isna(raw_score) else False
    if price_phase in ['BASE', 'RECLAIM'] and rs_rising and er >= 2.0 and prior_er_low and fmlc >= 3.0:
        if board_read == "UNKNOWN":
            parent_profile = "RESET_IGNITION"
            subtype = "UNKNOWN"
            board_read = "X2_STRUCTURE_WATCH"

    return parent_profile, subtype, board_read, prior_er_low

def run():
    args = parse_args()
    t = get_thresholds(args.strictness)
    print(f"Running profile interpreter with strictness: {args.strictness}")
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    df = pd.read_csv(input_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by=['symbol', 'timestamp']).reset_index(drop=True)

    input_row_count = len(df)
    events_clustered = []
    latest_rows = []
    raw_candidate_count = 0

    for symbol, group in df.groupby('symbol'):
        group = group.copy()
        group['price_phase'] = calculate_price_phase(group)
        group['is_partial'] = group['flowprint'].isna() | group['raw_score'].isna()
        
        er_history = []
        raw_score_history = []
        symbol_raw_events = []
        latest_complete_row = None
        
        for idx, row in group.iterrows():
            if not row['is_partial']:
                er_history.append(row.get('er', 0) if not pd.isna(row.get('er', 0)) else 0)
                raw_score_history.append(row.get('raw_score', np.nan))
                latest_complete_row = row

            parent_profile, subtype, board_read, prior_er_low = classify_row(row, er_history, raw_score_history, t)

            if parent_profile != "UNKNOWN":
                raw_candidate_count += 1
                symbol_raw_events.append({
                    'timestamp': row['timestamp'],
                    'close': row['close'],
                    'er': row.get('er', 0),
                    'fmlc': row.get('fmlc', 0),
                    'flowprint': row.get('flowprint', np.nan),
                    'raw_score': row.get('raw_score', np.nan),
                    'price_phase': row['price_phase'],
                    'parent_profile': parent_profile,
                    'subtype': subtype,
                    'board_read': board_read,
                    'prior_er_low': prior_er_low
                })
                
        # Clustering
        if symbol_raw_events:
            current_cluster = [symbol_raw_events[0]]
            for i in range(1, len(symbol_raw_events)):
                prev = current_cluster[-1]
                curr = symbol_raw_events[i]
                time_diff = (curr['timestamp'] - prev['timestamp']).total_seconds() / 3600.0
                
                if (curr['board_read'] == prev['board_read'] and 
                    curr['subtype'] == prev['subtype'] and 
                    time_diff <= 2.0):
                    current_cluster.append(curr)
                else:
                    evt = filter_and_build_event(symbol, current_cluster, t, args.strictness)
                    if evt: events_clustered.append(evt)
                    current_cluster = [curr]
                    
            evt = filter_and_build_event(symbol, current_cluster, t, args.strictness)
            if evt: events_clustered.append(evt)

        # Latest summary logic
        actual_latest = group.iloc[-1]
        target_row = latest_complete_row if latest_complete_row is not None else actual_latest
        lag_hours = (actual_latest['timestamp'] - target_row['timestamp']).total_seconds() / 3600.0
        
        # We classify the target row using the same logic!
        lp_profile, lp_subtype, lp_board, _ = classify_row(target_row, er_history, raw_score_history, t)

        latest_rows.append({
            'symbol': symbol,
            'latest_raw_timestamp': actual_latest['timestamp'],
            'latest_complete_metric_timestamp': target_row['timestamp'],
            'metric_lag_hours': round(lag_hours, 2),
            'latest_row_is_partial': bool(actual_latest['is_partial']),
            'latest_close': target_row['close'],
            'latest_er': target_row.get('er', 0),
            'latest_fmlc': target_row.get('fmlc', 0),
            'latest_flowprint': target_row.get('flowprint', np.nan),
            'latest_raw_score': target_row.get('raw_score', np.nan),
            'price_phase': target_row['price_phase'],
            'parent_profile': lp_profile,
            'subtype': lp_subtype,
            'board_read': lp_board,
            'mode': "X1_TACTICAL_MANUAL_REVIEW",
            'confidence': "LOW",
            'reason': "Latest complete row classification",
            'invalidation_note': "Manual review required"
        })

    df_latest = pd.DataFrame(latest_rows)
    
    # Apply global event exclusions (no UNKNOWN board_read, no UNKNOWN subtype)
    valid_events = [e for e in events_clustered if e['board_read'] != 'UNKNOWN' and e['subtype'] != 'UNKNOWN']
    df_events = pd.DataFrame(valid_events)

    df_latest.to_csv(output_latest_csv, index=False)
    if not df_events.empty:
        df_events.to_csv(output_events_csv, index=False)
    else:
        pd.DataFrame(columns=['symbol', 'event_start', 'event_end', 'event_hours', 'match_count', 'best_timestamp', 'best_raw_score', 'max_er', 'min_er', 'max_fmlc', 'max_flowprint', 'first_close', 'last_close', 'close_change_pct', 'parent_profile', 'subtype', 'board_read', 'mode', 'confidence', 'reason', 'invalidation_note']).to_csv(output_events_csv, index=False)

    # Generate Manifest
    with open(manifest_md, 'w') as f:
        f.write("# Profile Interpreter Manifest\n\n")
        f.write(f"Generated at: {datetime.now(timezone.utc).isoformat()}Z\n")
        f.write(f"Strictness: {args.strictness}\n")
        f.write(f"Input row count: {input_row_count}\n")
        f.write(f"Symbol count: {len(df_latest)}\n")
        f.write(f"Latest summaries count: {len(df_latest)}\n")
        
        # Latest distribution
        latest_boards = df_latest['board_read'].value_counts()
        unknown_latest = latest_boards.get('UNKNOWN', 0)
        f.write(f"Latest UNKNOWN count: {unknown_latest}\n")
        partial_count = df_latest['latest_row_is_partial'].sum()
        f.write(f"Latest partial-row count: {partial_count}\n")
        
        f.write(f"Raw row-level candidate count before clustering: {raw_candidate_count}\n")
        f.write(f"Clustered event count: {len(df_events)}\n")
        reduction = 18728 - len(df_events)
        f.write(f"Event reduction vs V1 18,728: {reduction}\n")
        
        unknown_board_events = df_events[df_events['board_read'] == 'UNKNOWN'].shape[0] if not df_events.empty else 0
        unknown_subtype_events = df_events[df_events['subtype'] == 'UNKNOWN'].shape[0] if not df_events.empty else 0
        f.write(f"UNKNOWN board_read event count: {unknown_board_events}\n")
        f.write(f"UNKNOWN subtype event count: {unknown_subtype_events}\n\n")
        
        f.write("## Latest Board Read Distribution\n")
        for k, v in latest_boards.items():
            f.write(f"- {k}: {v}\n")
            
        f.write("\n## Event Board Read Distribution\n")
        if not df_events.empty:
            for k, v in df_events['board_read'].value_counts().items():
                f.write(f"- {k}: {v}\n")
                
        f.write("\n## Event Subtype Distribution\n")
        if not df_events.empty:
            for k, v in df_events['subtype'].value_counts().items():
                f.write(f"- {k}: {v}\n")
                
        f.write("\n## Anchor Diagnostics\n")
        anchors = ['FETUSDT', 'HYPEUSDT', 'VVVUSDT', 'WLDUSDT', 'ALLOUSDT', 'NEARUSDT', 'APTUSDT', 'SOLUSDT', 'ONDOUSDT']
        for anchor in anchors:
            f.write(f"### {anchor}\n")
            latest_diag = df_latest[df_latest['symbol'] == anchor].iloc[0] if not df_latest[df_latest['symbol'] == anchor].empty else None
            if latest_diag is not None:
                f.write(f"- Latest: {latest_diag['board_read']} ({latest_diag['parent_profile']} | {latest_diag['subtype']})\n")
                
            if not df_events.empty:
                matches = df_events[df_events['symbol'] == anchor]
                f.write(f"- Events found: {len(matches)}\n")
                if len(matches) > 0:
                    for idx, m in matches.iterrows():
                        f.write(f"  - {m['event_start']} to {m['event_end']} | {m['parent_profile']} | {m['subtype']} | {m['board_read']}\n")
            else:
                f.write("- Events found: 0\n")
        
    json_out = {
        "latest_profiles": df_latest.to_dict(orient='records'),
        "top_events": df_events.tail(100).to_dict(orient='records') if not df_events.empty else []
    }
    with open(output_json, 'w') as f:
        json.dump(json_out, f, default=str, indent=2)

    with open(output_md, 'w') as f:
        f.write("# Profile Interpreter Read\n\n")
        f.write(f"Generated at: {datetime.now(timezone.utc).isoformat()}Z\n\n")
        f.write(f"Total symbols: {len(df_latest)}\n")
        f.write(f"Total events detected: {len(df_events)}\n")

    print(f"Processed {input_row_count} rows. Generated {len(df_events)} valid clustered events.")

def filter_and_build_event(symbol, cluster, t, strictness):
    start = cluster[0]['timestamp']
    end = cluster[-1]['timestamp']
    hours = (end - start).total_seconds() / 3600.0
    
    first_close = cluster[0]['close']
    last_close = cluster[-1]['close']
    pct_change = (last_close - first_close) / first_close * 100.0 if first_close > 0 else 0
    
    max_er = max(c['er'] for c in cluster)
    min_er = min(c['er'] for c in cluster)
    max_fmlc = max(c['fmlc'] for c in cluster)
    
    flowprints = [c['flowprint'] for c in cluster if not pd.isna(c['flowprint'])]
    max_flow = max(flowprints) if flowprints else np.nan
    
    raw_scores = [c['raw_score'] for c in cluster if not pd.isna(c['raw_score'])]
    best_rs = max(raw_scores) if raw_scores else np.nan
    
    best_ts = cluster[0]['timestamp']
    if raw_scores:
        for c in cluster:
            if c['raw_score'] == best_rs:
                best_ts = c['timestamp']
                break

    board_read = cluster[0]['board_read']
    
    # Cluster Filtering Rules
    if board_read == "X1_GRIND_ACTIVE":
        if len(cluster) < t['grind_mc']:
            return None
        if abs(pct_change) < t['grind_chg']:
            return None
        if not pd.isna(max_flow) and max_flow < t['grind_max_flow']:
            return None
    elif board_read == "X1_REAWAKENING":
        if len(cluster) < t['reawaken_mc']:
            if len(cluster) == 1 and cluster[0]['prior_er_low'] and cluster[0]['price_phase'] != 'EXTENDED' and pct_change >= -0.5:
                if strictness == 'tight':
                    if max_er >= 6.0 and max_fmlc >= 7.0 and (not pd.isna(max_flow) and max_flow >= 4.5) and (not pd.isna(best_rs) and best_rs >= 5.0):
                        pass
                    else:
                        return None
                else:
                    if max_er >= 5.0 and max_fmlc >= 6.5 and (not pd.isna(max_flow) and max_flow >= 4.0) and (not pd.isna(best_rs) and best_rs >= 4.5):
                        pass
                    else:
                        return None
            else:
                return None
    elif board_read == "X1_SHORT_REVIEW":
        phase = cluster[0]['price_phase']
        if phase not in ['EXTENDED', 'VULNERABLE', 'FAILED_RECOVERY']:
            if pct_change > t['short_chg']:
                return None
                
    # Basic fmlc hanger one-row check (if any other one-row cluster made it this far)
    if len(cluster) < 2 and board_read == "LATE_HANGER":
        if max_fmlc < 7.0 or max_er > 1.0:
            return None

    return {
        'symbol': symbol,
        'event_start': start,
        'event_end': end,
        'event_hours': round(hours, 2),
        'match_count': len(cluster),
        'best_timestamp': best_ts,
        'best_raw_score': best_rs,
        'max_er': max_er,
        'min_er': min_er,
        'max_fmlc': max_fmlc,
        'max_flowprint': max_flow,
        'first_close': first_close,
        'last_close': last_close,
        'close_change_pct': round(pct_change, 2),
        'parent_profile': cluster[0]['parent_profile'],
        'subtype': cluster[0]['subtype'],
        'board_read': board_read,
        'mode': 'X1_TACTICAL_MANUAL_REVIEW',
        'confidence': 'LOW',
        'reason': 'Clustered heuristic match',
        'invalidation_note': 'Manual review required'
    }

if __name__ == '__main__':
    run()
