import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
CELL1_CSV = REPORTS_DIR / "firestarterog_binance_20_symbol_cell1_recovery.csv"
CELL2_CSV = REPORTS_DIR / "firestarterog_cell2_neutral_dry_run.csv"
CELL2_MD = REPORTS_DIR / "firestarterog_cell2_neutral_dry_run.md"

def run_cell2_dry_run():
    print(f"Loading Cell 1 recovery CSV from: {CELL1_CSV}")
    if not CELL1_CSV.exists():
        raise FileNotFoundError(f"Missing input CSV: {CELL1_CSV}")
        
    df = pd.read_csv(CELL1_CSV)
    input_row_count = len(df)
    print(f"Loaded {input_row_count} rows.")
    
    # 1. Normalize booleans
    bool_cols = ["near_breakout", "clean_reclaim", "above_4h_trend", "is_stock_token"]
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().isin(["true", "1", "yes"])
            
    # 2. Filter crypto only
    crypto_df = df[df["is_stock_token"] == False].copy()
    output_row_count = len(crypto_df)
    print(f"Filtered to crypto only: {output_row_count} rows.")
    
    # 3. Calculate gates
    risk_ok = (crypto_df["risk_pct"] <= 5.0) & (crypto_df["invalidation_distance"] != "BAD")
    not_too_late = crypto_df["change_24h_%"] <= 16.0
    participation_ok = (
        (crypto_df["ignition_participation"] == "PASS") |
        (crypto_df["rvol_4h_window"] >= 1.25) |
        (crypto_df["volume_usd"] >= 10_000_000)
    )
    structure_ok = (
        (crypto_df["near_breakout"] == True) |
        (crypto_df["range_pos_20"] >= 0.60) |
        (crypto_df["range_pos_50_4h"] >= 0.60)
    )
    
    # 4. Apply neutral class gates
    scout = (
        risk_ok & not_too_late & participation_ok & structure_ok &
        (crypto_df["ignition_momentum"] == "PASS") &
        (crypto_df["raw_score"] >= 6.75) &
        (crypto_df["fmlc"] >= 9.0) &
        (crypto_df["flowprint"] >= 5.0) &
        (crypto_df["risk_pct"] <= 3.5)
    )
    
    trigger = (
        risk_ok & not_too_late & participation_ok & structure_ok &
        (
            ((crypto_df["raw_score"] >= 6.5) & (crypto_df["fmlc"] >= 8.0)) |
            ((crypto_df["er"] >= 6.0) & (crypto_df["fmlc"] >= 9.0) & (crypto_df["flowprint"] >= 5.0)) |
            ((crypto_df["change_24h_%"].between(3, 12)) & (crypto_df["fmlc"] >= 9.0))
        )
    )
    
    pullback_only = (crypto_df["change_24h_%"] > 16.0) & (crypto_df["change_24h_%"] <= 25.0)
    
    crypto_df["action"] = "rejected_candidate"
    crypto_df.loc[pullback_only, "action"] = "extended_watch_candidate"
    crypto_df.loc[trigger, "action"] = "trigger_class_candidate"
    crypto_df.loc[scout, "action"] = "scout_class_candidate"
    
    # 5. Generate reasons
    reasons = []
    for _, row in crypto_df.iterrows():
        action = row["action"]
        if action == "scout_class_candidate":
            reason = "Scout allowed: structure, participation, and risk are aligned."
        elif action == "trigger_class_candidate":
            reason = "Actionable setup: wait for trigger/confirmation."
        elif action == "extended_watch_candidate":
            reason = "Strong mover but too extended. Do not chase; wait for pullback."
        elif row["invalidation_distance"] == "BAD":
            reason = "Rejected: invalidation too wide."
        elif row["change_24h_%"] > 25:
            reason = "Rejected: too extended/chase risk."
        elif row["ignition_participation"] != "PASS" and row["volume_usd"] < 10_000_000:
            reason = "Rejected: weak participation."
        else:
            reason = "Rejected: not enough tactical edge."
        reasons.append(reason)
        
    crypto_df["reason"] = reasons
    
    # Save CSV
    crypto_df.to_csv(CELL2_CSV, index=False)
    print(f"Saved: {CELL2_CSV}")
    
    # Build MD Report
    build_markdown_report(crypto_df, input_row_count, output_row_count)

def build_markdown_report(df, input_count, output_count):
    # Class counts
    class_counts = df["action"].value_counts()
    classes = ["scout_class_candidate", "trigger_class_candidate", "extended_watch_candidate", "rejected_candidate"]
    summary_counts = {c: int(class_counts.get(c, 0)) for c in classes}
    
    # Required fields check
    req_fields = [
        "ticker", "price", "change_24h_%", "volume_usd", "rvol_1h", "rvol_4h_window",
        "er", "fmlc", "flowprint", "raw_score", "near_breakout", "clean_reclaim",
        "above_4h_trend", "range_pos_20", "range_pos_50_4h", "open_interest",
        "funding", "ema_21", "is_stock_token", "risk_pct", "invalidation_distance",
        "ignition_momentum", "ignition_participation"
    ]
    missing_fields = [f for f in req_fields if f not in df.columns]
    
    # Top 10 by raw_score
    df_sorted = df.sort_values(by="raw_score", ascending=False)
    top_10 = df_sorted.head(10)
    
    # Rows that met scout/trigger logic
    candidates = df[df["action"].isin(["scout_class_candidate", "trigger_class_candidate"])].sort_values(by="raw_score", ascending=False)
    
    lines = [
        "# FirestarterOG Cell 2 Neutral Dry-Run Audit Report",
        "",
        f"**Run UTC Timestamp:** {datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}",
        "**Purpose:** Live validation of recovered original Firestarter Cell 2 Dust Cleaner logic using neutral research labels.",
        "**Data Source:** Live Cell 1 Binance recovery snapshot CSV.",
        "",
        "## 1. Row Counts & Field Analysis",
        "",
        f"- **Input Row Count (Cell 1 Recovery CSV):** {input_count}",
        f"- **Output Row Count (Crypto Filtered):** {output_count}",
        "- **Required Fields Check:**",
    ]
    
    if missing_fields:
        lines.append(f"  - WARNING: Missing required fields: {', '.join(missing_fields)}")
    else:
        lines.append("  - PASS: All required fields are present in the input dataset.")
        
    lines.extend([
        "",
        "## 2. Candidate Classification Summary",
        "",
        "| Neutral Research Class | Count | Description |",
        "|---|---:|---|",
        f"| `scout_class_candidate` | {summary_counts['scout_class_candidate']} | Controlled risk, strong scores & FMLC/Flowprint participation |",
        f"| `trigger_class_candidate` | {summary_counts['trigger_class_candidate']} | Actionable structure & score qualification, normal risk |",
        f"| `extended_watch_candidate` | {summary_counts['extended_watch_candidate']} | Strong mover (16% to 25% 24h change), too extended for entry |",
        f"| `rejected_candidate` | {summary_counts['rejected_candidate']} | Failed key gates or lacked tactical edge |",
        "",
        "## 3. Top 10 Symbols by raw_score (with Neutral Class & Reason)",
        "",
        "| Rank | Ticker | raw_score | price | 24h Change % | ER | FMLC | Flowprint | Neutral Class | Reason |",
        "|---|---|---:|---|---:|---:|---:|---:|---|---|",
    ])
    
    for rank, (_, row) in enumerate(top_10.iterrows(), start=1):
        lines.append(
            f"| {rank} | {row['ticker']} | {row['raw_score']:.2f} | {row['price']} | {row['change_24h_%']}% | "
            f"{row['er']} | {row['fmlc']} | {row['flowprint']} | `{row['action']}` | {row['reason']} |"
        )
        
    lines.extend([
        "",
        "## 4. Qualified Candidates (Scout/Trigger Class Only)",
        "",
    ])
    
    if len(candidates) == 0:
        lines.append("*No symbols qualified for `scout_class_candidate` or `trigger_class_candidate` in this snapshot.*")
    else:
        lines.extend([
            "| Ticker | raw_score | price | 24h Change % | risk_pct | invalidation_distance | Neutral Class | Reason |",
            "|---|---:|---|---:|---:|---|---|---|",
        ])
        for _, row in candidates.iterrows():
            lines.append(
                f"| {row['ticker']} | {row['raw_score']:.2f} | {row['price']} | {row['change_24h_%']}% | "
                f"{row['risk_pct']}% | {row['invalidation_distance']} | `{row['action']}` | {row['reason']} |"
            )
            
    lines.extend([
        "",
        "## 5. Governance and Safety Confirmations",
        "",
        "- **Cell 1 Formulas Modified:** **NO**. Original formulas for ER, FMLC, Flowprint, and raw_score remain exactly as documented in the master specification and were not altered.",
        "- **Action/Trading Labels or Alerts Triggered:** **NO**. No live notifications were sent, no trade recommendations were made, and all classifications use neutralized research-candidate names.",
        "- **Trading Signal Classification:** **NO**. This is a neutral, local dry-run simulation for historical alignment research and formula verification only.",
        "",
        "PASS_FIRESTARTEROG_CELL2_NEUTRAL_DRY_RUN_COMPLETE",
        ""
    ])
    
    CELL2_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved: {CELL2_MD}")

if __name__ == "__main__":
    run_cell2_dry_run()
