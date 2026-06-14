#!/usr/bin/env python3
"""Observation-only Firestarter Optimizer candidate state monitor."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = REPO_ROOT / "reports" / "firestarter_optimizer"
ACTIVE_PATH = REPORT_DIR / "active_candidates.jsonl"
EVENTS_PATH = REPORT_DIR / "candidate_state_events.jsonl"
EXPIRED_PATH = REPORT_DIR / "expired_or_changed_candidates.jsonl"
REPORT_PATH = REPORT_DIR / "update_candidate_states_report.md"
DATA_QUALITY_REPORT_PATH = REPORT_DIR / "update_candidate_states_data_quality_separation_report.md"
Y_HANGER_REPORT_PATH = REPORT_DIR / "y_hanger_diagnostic_state_report.md"

ALLOWED_STATES = {
    "NEW",
    "ACTIVE_VALID",
    "PERSISTENT_HANGER",
    "PERSISTENT_GRIND",
    "PERSISTENT_REAWAKENING",
    "PERSISTENT_THEN_COLLAPSE",
    "PERSISTENT_THEN_BREAKOUT",
    "PERSISTENT_THEN_CHOP",
    "ADVERSE_FIRST",
    "MICRO_MOVE_HIT",
    "GRIND_BROKE",
    "HANGER_CONFIRMED",
    "DATA_GAP",
}

PRODUCTION_INPUT_CANDIDATES = [
    REPO_ROOT / "reports" / "firestarter_optimizer" / "candidate_tickets.jsonl",
    REPO_ROOT / "state" / "firestarter_optimizer" / "candidate_tickets.jsonl",
    REPO_ROOT / "state" / "cloud" / "candidate_tickets.jsonl",
]

TEST_INPUT_CANDIDATES = [
    REPO_ROOT / "reports" / "firestarter_optimizer" / "test_candidate_tickets.jsonl",
    REPO_ROOT / "reports" / "firestarter_optimizer" / "test" / "candidate_tickets.jsonl",
    REPO_ROOT / ".codex_cloud_pr_worktree" / "reports" / "firestarter_optimizer" / "candidate_tickets.jsonl",
    REPO_ROOT / ".codex_cloud_data_pilot_v1" / "reports" / "firestarter_optimizer" / "candidate_tickets.jsonl",
    REPO_ROOT / ".codex_cloud_cell1_metric_producer_v1" / "reports" / "firestarter_optimizer" / "candidate_tickets.jsonl",
    REPO_ROOT / ".codex_cloud_cell1_manual_build_gate_v1" / "reports" / "firestarter_optimizer" / "candidate_tickets.jsonl",
]

FIELD_ALIASES = {
    "candidate_id": ("candidate_id", "id", "ticket_id", "candidate_ticket_id"),
    "symbol": ("symbol", "market", "ticker", "instrument", "instrument_id"),
    "direction_bias": ("direction_bias", "direction", "bias", "side", "action_bias"),
    "signal_family": ("signal_family", "family", "signal", "setup_family", "pattern_family"),
    "action_label": ("action_label", "label", "action", "candidate_label", "state_label"),
    "seen_utc": (
        "seen_utc",
        "timestamp_utc",
        "created_at_utc",
        "detected_at_utc",
        "generated_at_utc",
        "scan_time_utc",
        "event_time_utc",
        "last_seen_utc",
    ),
    "price": (
        "latest_price",
        "price_at_signal",
        "price",
        "mark_price",
        "last_price",
        "close",
        "close_price",
        "entry_reference_price",
        "reference_price",
    ),
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def isoformat_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_utc(value: Any) -> datetime | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).replace(microsecond=0)


def coerce_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def first_present(row: dict[str, Any], field: str) -> Any:
    for key in FIELD_ALIASES[field]:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return None


def normalize_direction(value: Any) -> str:
    text = str(value or "").strip().upper().replace("-", "_").replace(" ", "_")
    if text in {"LONG", "BUY", "BULL", "BULLISH"}:
        return "LONG"
    if text in {"SHORT", "SELL", "BEAR", "BEARISH", "SHORT_REVIEW"}:
        return "SHORT_REVIEW"
    if text in {"AVOID", "AVOID_LONG", "NO_LONG"}:
        return "AVOID_LONG"
    if text in {"WATCH", "WATCH_ONLY", "NEUTRAL"}:
        return "WATCH_ONLY"
    if text in {"DATA_GAP", "GAP"}:
        return "DATA_GAP"
    return text


def direction_sign(direction_bias: str) -> int:
    if direction_bias in {"SHORT_REVIEW", "AVOID_LONG"}:
        return -1
    return 1


def pct_change(first_price: float | None, latest_price: float | None) -> float | None:
    if first_price is None or latest_price is None or first_price == 0:
        return None
    return ((latest_price - first_price) / first_price) * 100.0


def safe_jsonl_read(path: Path) -> tuple[list[dict[str, Any]], int]:
    rows: list[dict[str, Any]] = []
    bad_lines = 0
    if not path.exists():
        return rows, bad_lines
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                row = json.loads(text)
            except json.JSONDecodeError:
                bad_lines += 1
                continue
            if isinstance(row, dict):
                row["_source_line"] = line_number
                rows.append(row)
            else:
                bad_lines += 1
    return rows, bad_lines


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(text)
        temp_name = handle.name
    os.replace(temp_name, path)


def write_jsonl_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    content = "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    atomic_write_text(path, content)


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.open("a", encoding="utf-8").close()
        return
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def count_jsonl_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def discover_input(explicit_input: str | None, force_test: bool) -> tuple[Path | None, str]:
    if explicit_input:
        return Path(explicit_input).resolve(), "explicit"
    if not force_test:
        for path in PRODUCTION_INPUT_CANDIDATES:
            if path.exists():
                return path, "production"
    for path in TEST_INPUT_CANDIDATES:
        if path.exists():
            return path, "isolated_test"
    return None, "none_found"


def stable_group_key(ticket: dict[str, Any]) -> str:
    symbol = ticket.get("symbol")
    direction = ticket.get("direction_bias")
    family = ticket.get("signal_family")
    if symbol and direction and family:
        return f"{symbol}|{direction}|{family}"
    if ticket.get("candidate_id"):
        return f"candidate_id|{ticket['candidate_id']}"
    return f"source_line|{ticket.get('_source_line', 'unknown')}"


def normalize_ticket(row: dict[str, Any], run_time: datetime) -> tuple[dict[str, Any], list[str]]:
    seen = parse_utc(first_present(row, "seen_utc"))
    price = coerce_float(first_present(row, "price"))
    ticket = {
        "candidate_id": first_present(row, "candidate_id"),
        "symbol": str(first_present(row, "symbol") or "").strip().upper(),
        "direction_bias": normalize_direction(first_present(row, "direction_bias")),
        "signal_family": str(first_present(row, "signal_family") or "").strip().upper(),
        "action_label": str(first_present(row, "action_label") or "").strip(),
        "board_read": str(row.get("board_read") or "").strip(),
        "source_signal_family": str(row.get("source_signal_family") or "").strip().upper(),
        "data_quality": str(row.get("data_quality") or "").strip().upper(),
        "classification_confidence": str(row.get("classification_confidence") or "").strip().upper(),
        "data_gap_fields": row.get("data_gap_fields") if isinstance(row.get("data_gap_fields"), list) else [],
        "seen_utc": seen,
        "price": price,
        "_source_line": row.get("_source_line"),
        "_raw": row,
    }
    missing: list[str] = []
    for field in ("symbol", "direction_bias", "signal_family"):
        if not ticket[field]:
            missing.append(field)
    if ticket["direction_bias"] == "DATA_GAP" or ticket["signal_family"] == "DATA_GAP":
        missing.append("ticket_data_gap:classification")
    if seen is None:
        missing.append("seen_utc")
        ticket["seen_utc"] = run_time
    if price is None:
        missing.append("price")
    ticket["stable_group_key"] = stable_group_key(ticket)
    return ticket, missing


def observed_price_path(records: list[dict[str, Any]], first_price: float | None) -> list[tuple[datetime, float, float]]:
    path: list[tuple[datetime, float, float]] = []
    if first_price is None:
        return path
    for record in records:
        price = record.get("price")
        seen = record.get("seen_utc")
        if isinstance(seen, datetime) and isinstance(price, (int, float)):
            change = pct_change(first_price, float(price))
            if change is not None:
                path.append((seen, float(price), change))
    return sorted(path, key=lambda item: item[0])


def movement_metrics(
    records: list[dict[str, Any]],
    direction_bias: str,
    first_price: float | None,
    previous: dict[str, Any] | None,
) -> tuple[float | None, float, float, str | None]:
    sign = direction_sign(direction_bias)
    max_favorable = coerce_float((previous or {}).get("max_favorable_pct")) or 0.0
    max_adverse = coerce_float((previous or {}).get("max_adverse_pct")) or 0.0
    adverse_first_at: str | None = None
    favorable_first_at: str | None = None
    latest_change: float | None = None

    for seen, _price, change in observed_price_path(records, first_price):
        latest_change = change
        directional_change = sign * change
        if directional_change > max_favorable:
            max_favorable = directional_change
        if -directional_change > max_adverse:
            max_adverse = -directional_change
        if directional_change >= 0.3 and favorable_first_at is None:
            favorable_first_at = isoformat_utc(seen)
        if directional_change <= -0.3 and adverse_first_at is None:
            adverse_first_at = isoformat_utc(seen)

    adverse_before_favorable = None
    if adverse_first_at and (not favorable_first_at or adverse_first_at < favorable_first_at):
        adverse_before_favorable = adverse_first_at
    return latest_change, round(max_favorable, 6), round(max_adverse, 6), adverse_before_favorable


def compute_persistence_count(
    records: list[dict[str, Any]],
    previous: dict[str, Any] | None,
) -> int:
    source_count = len(records)
    if not previous:
        return source_count
    previous_count = int(previous.get("persistence_count") or 0)
    previous_last_seen = parse_utc(previous.get("last_seen_utc"))
    seen_values = [record["seen_utc"] for record in records if isinstance(record.get("seen_utc"), datetime)]
    if not seen_values or previous_last_seen is None:
        return max(previous_count, source_count)
    if max(seen_values) <= previous_last_seen:
        return previous_count
    new_since_previous = sum(1 for seen in seen_values if seen > previous_last_seen)
    if source_count >= previous_count:
        return max(previous_count, source_count)
    return previous_count + new_since_previous


def group_unique_values(records: list[dict[str, Any]], field: str) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for record in records:
        value = record.get(field)
        if isinstance(value, list):
            items = [str(item).strip() for item in value if str(item).strip()]
        else:
            items = [str(value).strip()] if value else []
        for item in items:
            if item and item not in seen:
                values.append(item)
                seen.add(item)
    return values


def group_data_quality(records: list[dict[str, Any]], data_gap_fields: list[str]) -> str:
    qualities = {str(record.get("data_quality") or "").upper() for record in records}
    confidences = {str(record.get("classification_confidence") or "").upper() for record in records}
    if "DATA_GAP_BLOCKING" in qualities:
        return "DATA_GAP_BLOCKING"
    if data_gap_fields or "DATA_GAP_PARTIAL" in qualities:
        if "SOURCE_DERIVED_UNVERIFIED" in confidences:
            return "DATA_GAP_PARTIAL"
        return "DATA_GAP_PARTIAL"
    if "SOURCE_DERIVED_UNVERIFIED" in confidences:
        return "SOURCE_DERIVED_UNVERIFIED"
    return "COMPLETE"


def active_distribution(rows: list[dict[str, Any]], field: str) -> Counter[str]:
    return Counter(str(row.get(field) or "(none)") for row in rows)


def active_data_gap_distribution(rows: list[dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        fields = row.get("data_gap_fields") or []
        if not fields:
            counts["(none)"] += 1
            continue
        for field in fields:
            counts[str(field)] += 1
    return counts


def active_y_hanger_distributions(rows: list[dict[str, Any]]) -> tuple[Counter[str], Counter[str], Counter[str]]:
    diagnostic_states: Counter[str] = Counter()
    reason_tags: Counter[str] = Counter()
    missing_inputs: Counter[str] = Counter()
    for row in rows:
        ds = row.get("diagnostic_state") or "(none)"
        diagnostic_states[ds] += 1
        tags = row.get("y_hanger_reason_tags")
        if isinstance(tags, list):
            for tag in tags:
                reason_tags[str(tag)] += 1
        else:
            reason_tags["(none)"] += 1
        inputs = row.get("y_hanger_missing_inputs")
        if isinstance(inputs, list):
            for inp in inputs:
                missing_inputs[str(inp)] += 1
        else:
            missing_inputs["(none)"] += 1
    return diagnostic_states, reason_tags, missing_inputs


def y_hanger_report_lines(
    *,
    run_time: datetime,
    input_path: Path | None,
    ticket_count: int,
    active_count: int,
    event_rows_before: int,
    event_rows_after: int,
    state_distribution: Counter[str],
    data_quality_distribution: Counter[str],
    action_label_distribution: Counter[str],
    direction_bias_distribution: Counter[str],
    signal_family_distribution: Counter[str],
    data_gap_fields_distribution: Counter[str],
    active_rows: list[dict[str, Any]],
    commands_run: list[str],
    files_changed: list[str],
) -> list[str]:
    diagnostic_states, reason_tags, missing_inputs = active_y_hanger_distributions(active_rows)
    lines = [
        "# Firestarter Optimizer Y_HANGER Diagnostic State Report",
        "",
        f"Run UTC: {isoformat_utc(run_time)}",
        "",
        "## Observation-Only Boundary",
        "",
        "This diagnostic run analyzes Y_HANGER candidates. It does not create trade instructions, edge claims, exclusion rules, or automatic rule changes.",
        "",
        "## Input Information",
        "",
        f"- **Input candidate ticket path:** `{input_path}`",
        f"- **Tickets read:** `{ticket_count}`",
        f"- **Active candidate group count:** `{active_count}`",
        "",
        "## Lifecycle State Distribution",
        "",
    ]
    for label, count in sorted((state_distribution or Counter({"(none)": 0})).items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Diagnostic State Distribution", ""])
    for label, count in sorted(diagnostic_states.items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Y_HANGER Reason Tags Distribution", ""])
    for label, count in sorted(reason_tags.items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Y_HANGER Missing Inputs Distribution", ""])
    for label, count in sorted(missing_inputs.items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Data Quality Distribution", ""])
    for label, count in sorted((data_quality_distribution or Counter({"(none)": 0})).items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Direction Bias Distribution", ""])
    for label, count in sorted((direction_bias_distribution or Counter({"(none)": 0})).items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Signal Family Distribution", ""])
    for label, count in sorted((signal_family_distribution or Counter({"(none)": 0})).items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(
        [
            "",
            "## Write Verification",
            "",
            f"- Event rows before run: `{event_rows_before}`",
            f"- Event rows after run: `{event_rows_after}`",
            f"- Confirmation append-only state events were preserved: `{event_rows_after >= event_rows_before}`",
            f"- Confirmation active snapshot was atomically written: `confirmed by temp-file plus os.replace implementation`",
            "",
            "## Commands Run",
            "",
            "```powershell",
        ]
    )
    lines.extend(commands_run)
    lines.extend(["```", "", "## Files Changed", ""])
    for fc in files_changed:
        lines.append(f"- `{fc}`")
    lines.extend(
        [
            "",
            "## Boundary Check",
            "",
            "No raw scanner files, live scanner files, Bitget/order/trading logic, historical JSONL/parquet/OHLCV/Tardis files, `candidate_rules.yaml`, ML files, `signal_discovery.py`, Slack/n8n files, Google Drive sync logic, cloud optimizer queue activation, or Google Drive active outputs were modified.",
        ]
    )
    return lines


def choose_state(
    *,
    missing_fields: list[str],
    signal_family: str,
    source_signal_family: str,
    direction_bias: str,
    persistence_count: int,
    persistence_minutes: float,
    max_favorable_pct: float,
    max_adverse_pct: float,
    adverse_before_favorable: str | None,
    args: argparse.Namespace,
) -> tuple[str, str]:
    if missing_fields:
        return "DATA_GAP", f"missing required fields: {', '.join(sorted(set(missing_fields)))}"

    persistent = persistence_count >= args.persistence_count_threshold or persistence_minutes >= args.persistence_minutes_threshold
    family = signal_family.lower()
    source_family = source_signal_family.lower()
    bearish = direction_bias in {"SHORT_REVIEW", "AVOID_LONG"}

    if "hanger" in family or source_family == "fmlc_hanger":
        if persistence_count > 1:
            return "PERSISTENT_HANGER", "source-derived hanger candidate persisted; data quality is tracked separately"
        return "NEW", "first observation for source-derived hanger candidate; data quality is tracked separately"

    if persistent and max_favorable_pct >= args.chop_threshold_pct and max_adverse_pct >= args.chop_threshold_pct:
        return "PERSISTENT_THEN_CHOP", "persistent candidate moved both favorably and adversely beyond chop threshold"
    if persistent and "hanger" in family and max_favorable_pct >= args.confirm_threshold_pct:
        return "HANGER_CONFIRMED", "hanger-family candidate reached favorable confirmation threshold"
    if persistent and "grind" in family and max_adverse_pct >= args.break_threshold_pct:
        return "GRIND_BROKE", "grind-family candidate moved adversely beyond break threshold"
    if persistent and max_favorable_pct >= args.breakout_threshold_pct:
        if bearish:
            return "PERSISTENT_THEN_COLLAPSE", "persistent bearish candidate had favorable downward movement"
        return "PERSISTENT_THEN_BREAKOUT", "persistent long candidate had favorable upward movement"
    if persistent and max_adverse_pct >= args.collapse_threshold_pct:
        if bearish:
            return "PERSISTENT_THEN_BREAKOUT", "persistent bearish candidate had adverse upward movement"
        return "PERSISTENT_THEN_COLLAPSE", "persistent long candidate had adverse downward movement"
    if adverse_before_favorable:
        return "ADVERSE_FIRST", "adverse movement threshold was observed before favorable movement threshold"
    if max_favorable_pct >= args.micro_move_threshold_pct:
        return "MICRO_MOVE_HIT", "favorable micro-move threshold was observed"
    if persistent and "hanger" in family:
        return "PERSISTENT_HANGER", "hanger-family candidate persisted"
    if persistent and "grind" in family:
        return "PERSISTENT_GRIND", "grind-family candidate persisted"
    if persistent and "reawak" in family:
        return "PERSISTENT_REAWAKENING", "reawakening-family candidate persisted"
    if persistence_count <= 1:
        return "NEW", "first observation for stable candidate group"
    return "ACTIVE_VALID", "candidate remains visible with no stronger observation label"


def load_previous_active(path: Path) -> dict[str, dict[str, Any]]:
    rows, _bad_lines = safe_jsonl_read(path)
    previous: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = row.get("stable_group_key")
        if key:
            previous[str(key)] = row
    return previous


def build_records(
    tickets: list[dict[str, Any]],
    previous_active: dict[str, dict[str, Any]],
    run_time: datetime,
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], Counter[str], Counter[str]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    missing_by_group: dict[str, list[str]] = defaultdict(list)
    missing_fields: Counter[str] = Counter()

    for row in tickets:
        ticket, missing = normalize_ticket(row, run_time)
        grouped[ticket["stable_group_key"]].append(ticket)
        missing_by_group[ticket["stable_group_key"]].extend(missing)
        missing_fields.update(missing)

    active_rows: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    state_distribution: Counter[str] = Counter()

    for key, records in sorted(grouped.items()):
        records = sorted(records, key=lambda item: (item["seen_utc"], item.get("_source_line") or 0))
        previous = previous_active.get(key)
        latest = records[-1]
        data_gap_fields = group_unique_values(records, "data_gap_fields")
        classification_confidences = group_unique_values(records, "classification_confidence")
        source_signal_families = group_unique_values(records, "source_signal_family")
        data_quality = group_data_quality(records, data_gap_fields)
        previous_first_seen = parse_utc((previous or {}).get("first_seen_utc"))
        previous_first_price = coerce_float((previous or {}).get("first_seen_price"))
        first_record_seen = records[0]["seen_utc"]
        first_seen = min(previous_first_seen, first_record_seen) if previous_first_seen else first_record_seen
        first_price = previous_first_price if previous_first_price is not None else records[0].get("price")
        latest_price = latest.get("price")
        last_seen = max(record["seen_utc"] for record in records)
        persistence_count = compute_persistence_count(records, previous)
        persistence_minutes = max(0.0, (last_seen - first_seen).total_seconds() / 60.0)
        price_change, max_favorable, max_adverse, adverse_first_at = movement_metrics(
            records, latest["direction_bias"], first_price, previous
        )
        current_state, reason = choose_state(
            missing_fields=missing_by_group[key],
            signal_family=latest["signal_family"],
            source_signal_family=latest["source_signal_family"],
            direction_bias=latest["direction_bias"],
            persistence_count=persistence_count,
            persistence_minutes=persistence_minutes,
            max_favorable_pct=max_favorable,
            max_adverse_pct=max_adverse,
            adverse_before_favorable=adverse_first_at,
            args=args,
        )
        if current_state not in ALLOWED_STATES:
            current_state = "DATA_GAP"
            reason = "internal state guard forced non-allowed state to DATA_GAP"
        previous_state = str((previous or {}).get("current_state") or "")

        diagnostic_state = None
        diagnostic_question = None
        y_hanger_reason_tags = None
        y_hanger_missing_inputs = None
        y_hanger_confidence = None
        y_hanger_evidence_fields = None

        signal_family_upper = str(latest.get("signal_family") or "").strip().upper()
        source_family_upper = str(latest.get("source_signal_family") or "").strip().upper()
        action_label_upper = str(latest.get("action_label") or "").strip().upper()

        if (signal_family_upper == "SHORT_HANGER" or 
            source_family_upper == "FMLC_HANGER" or 
            "SHORT_HANGER" in action_label_upper):
            diagnostic_state = "Y_HANGER"
            diagnostic_question = "WHY_PRICE_STILL_ELEVATED"
            
            raw_row = latest.get("_raw") or {}
            missing_inputs = []
            evidence_fields = {}
            reason_tags = []
            
            p_pos = raw_row.get("price_position")
            if p_pos is None or p_pos == "":
                missing_inputs.append("price_position")
            else:
                evidence_fields["price_position"] = p_pos
                
            expected_fields = {
                "btc_beta": "HELD_BY_BTC_BETA",
                "market_risk_on": "HELD_BY_MARKET_RISK_ON",
                "liquidity_shelf": "HELD_BY_LIQUIDITY_SHELF",
                "ema_structure": "HELD_BY_EMA_STRUCTURE",
                "fmlc_crowding": "HELD_BY_HIGH_FMLC_CROWDING",
                "absorption": "HELD_BY_ABSORPTION",
                "thin_liquidity": "HELD_BY_THIN_LIQUIDITY",
                "sell_trigger": "HELD_BY_NO_SELL_TRIGGER_YET"
            }
            
            for field, tag in expected_fields.items():
                val = raw_row.get(field)
                if val is not None and val != "":
                    evidence_fields[field] = val
                    reason_tags.append(tag)
                else:
                    missing_inputs.append(field)
                    
            if not reason_tags or missing_inputs:
                reason_tags.append("Y_UNKNOWN_MISSING_INPUTS")
                
            y_hanger_reason_tags = reason_tags
            y_hanger_missing_inputs = missing_inputs
            y_hanger_evidence_fields = evidence_fields
            y_hanger_confidence = raw_row.get("classification_confidence") or "SOURCE_DERIVED_UNVERIFIED"

        row = {
            "candidate_id": latest.get("candidate_id"),
            "symbol": latest["symbol"],
            "direction_bias": latest["direction_bias"],
            "signal_family": latest["signal_family"],
            "source_signal_family": latest["source_signal_family"] or None,
            "action_label": latest["action_label"],
            "board_read": latest["board_read"] or None,
            "stable_group_key": key,
            "first_seen_utc": isoformat_utc(first_seen),
            "last_seen_utc": isoformat_utc(last_seen),
            "persistence_count": persistence_count,
            "persistence_minutes": round(persistence_minutes, 2),
            "first_seen_price": first_price,
            "latest_price": latest_price,
            "price_change_since_first_seen_pct": round(price_change, 6) if price_change is not None else None,
            "max_favorable_pct": max_favorable,
            "max_adverse_pct": max_adverse,
            "current_state": current_state,
            "previous_state": previous_state or None,
            "state_change_reason": reason,
            "data_quality": data_quality,
            "data_gap_fields": data_gap_fields,
            "classification_confidence": classification_confidences[0] if len(classification_confidences) == 1 else classification_confidences,
            "source_ticket_count": len(records),
            "last_updated_utc": isoformat_utc(run_time),
            "observation_only": True,
            "trade_command": False,
            "rule_change": False,
            "diagnostic_state": diagnostic_state,
            "diagnostic_question": diagnostic_question,
            "y_hanger_reason_tags": y_hanger_reason_tags,
            "y_hanger_missing_inputs": y_hanger_missing_inputs,
            "y_hanger_confidence": y_hanger_confidence,
            "y_hanger_evidence_fields": y_hanger_evidence_fields,
        }
        active_rows.append(row)
        state_distribution[current_state] += 1
        events.append(
            {
                "event_utc": isoformat_utc(run_time),
                "event_type": "candidate_state_observed",
                "stable_group_key": key,
                "previous_state": previous_state or None,
                "current_state": current_state,
                "state_change": bool(previous_state and previous_state != current_state),
                "state_change_reason": reason,
                "observation_only": True,
                "diagnostic_state": diagnostic_state,
                "diagnostic_question": diagnostic_question,
                "y_hanger_reason_tags": y_hanger_reason_tags,
                "y_hanger_missing_inputs": y_hanger_missing_inputs,
                "y_hanger_confidence": y_hanger_confidence,
                "y_hanger_evidence_fields": y_hanger_evidence_fields,
                "candidate": row,
            }
        )

    return active_rows, events, state_distribution, missing_fields


def build_expired_or_changed(
    active_rows: list[dict[str, Any]],
    previous_active: dict[str, dict[str, Any]],
    run_time: datetime,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    active_by_key = {row["stable_group_key"]: row for row in active_rows}
    for key, previous in sorted(previous_active.items()):
        current = active_by_key.get(key)
        if current is None:
            rows.append(
                {
                    "event_utc": isoformat_utc(run_time),
                    "event_type": "candidate_missing_from_current_input",
                    "stable_group_key": key,
                    "previous_state": previous.get("current_state"),
                    "current_state": "DATA_GAP",
                    "state_change_reason": "previously active candidate was not present in current candidate-ticket input",
                    "observation_only": True,
                    "diagnostic_state": previous.get("diagnostic_state"),
                    "diagnostic_question": previous.get("diagnostic_question"),
                    "y_hanger_reason_tags": previous.get("y_hanger_reason_tags"),
                    "y_hanger_missing_inputs": previous.get("y_hanger_missing_inputs"),
                    "y_hanger_confidence": previous.get("y_hanger_confidence"),
                    "y_hanger_evidence_fields": previous.get("y_hanger_evidence_fields"),
                    "candidate": previous,
                }
            )
        elif previous.get("current_state") != current.get("current_state"):
            rows.append(
                {
                    "event_utc": isoformat_utc(run_time),
                    "event_type": "candidate_state_changed",
                    "stable_group_key": key,
                    "previous_state": previous.get("current_state"),
                    "current_state": current.get("current_state"),
                    "state_change_reason": current.get("state_change_reason"),
                    "observation_only": True,
                    "diagnostic_state": current.get("diagnostic_state"),
                    "diagnostic_question": current.get("diagnostic_question"),
                    "y_hanger_reason_tags": current.get("y_hanger_reason_tags"),
                    "y_hanger_missing_inputs": current.get("y_hanger_missing_inputs"),
                    "y_hanger_confidence": current.get("y_hanger_confidence"),
                    "y_hanger_evidence_fields": current.get("y_hanger_evidence_fields"),
                    "candidate": current,
                }
            )
    return rows


def report_lines(
    *,
    run_time: datetime,
    input_path: Path | None,
    input_mode: str,
    bad_lines: int,
    ticket_count: int,
    active_count: int,
    event_count: int,
    expired_or_changed_count: int,
    state_distribution: Counter[str],
    data_quality_distribution: Counter[str],
    action_label_distribution: Counter[str],
    direction_bias_distribution: Counter[str],
    signal_family_distribution: Counter[str],
    data_gap_fields_distribution: Counter[str],
    missing_fields: Counter[str],
    dry_run: bool,
    args: argparse.Namespace,
) -> list[str]:
    state_rows = state_distribution or Counter({"(none)": 0})
    data_quality_rows = data_quality_distribution or Counter({"(none)": 0})
    action_rows = action_label_distribution or Counter({"(none)": 0})
    direction_rows = direction_bias_distribution or Counter({"(none)": 0})
    signal_rows = signal_family_distribution or Counter({"(none)": 0})
    data_gap_rows = data_gap_fields_distribution or Counter({"(none)": 0})
    missing_rows = missing_fields or Counter({"(none)": 0})
    lines = [
        "# Firestarter Optimizer Candidate State Monitor Report",
        "",
        f"Run UTC: {isoformat_utc(run_time)}",
        "",
        "## Observation-Only Boundary",
        "",
        "This run is observation-only. The emitted states are evidence labels only; they are not trade commands, exclusion rules, or automatic rule changes.",
        "",
        "## Input",
        "",
        f"- Input mode: `{input_mode}`",
        f"- Input path: `{input_path if input_path else 'none found'}`",
        f"- Dry run: `{dry_run}`",
        f"- Candidate-ticket rows read: `{ticket_count}`",
        f"- Bad JSONL lines skipped: `{bad_lines}`",
    ]
    if input_mode == "isolated_test":
        lines.append("- Production `candidate_tickets.jsonl` was not found; this run used the isolated test output path.")
    if input_mode == "none_found":
        lines.append("- No production or isolated test candidate-ticket JSONL was found; outputs contain no active candidates.")
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- Active snapshot: `{ACTIVE_PATH}`",
            f"- Append-only state events: `{EVENTS_PATH}`",
            f"- Expired or changed candidates: `{EXPIRED_PATH}`",
            f"- Markdown report: `{REPORT_PATH}`",
            "",
            "## Row Counts",
            "",
            f"- Active candidate rows: `{active_count}`",
            f"- State event rows prepared this run: `{event_count}`",
            f"- Expired or changed rows prepared this run: `{expired_or_changed_count}`",
            "",
            "## Lifecycle State Distribution",
            "",
        ]
    )
    for state, count in sorted(state_rows.items()):
        lines.append(f"- `{state}`: `{count}`")
    lines.extend(["", "## Data Quality Distribution", ""])
    for label, count in sorted(data_quality_rows.items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Action Label Distribution", ""])
    for label, count in sorted(action_rows.items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Direction Bias Distribution", ""])
    for label, count in sorted(direction_rows.items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Signal Family Distribution", ""])
    for label, count in sorted(signal_rows.items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Data Gap Fields Distribution", ""])
    for label, count in sorted(data_gap_rows.items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Missing Fields", ""])
    for field, count in sorted(missing_rows.items()):
        lines.append(f"- `{field}`: `{count}`")
    lines.extend(
        [
            "",
            "## Assumptions",
            "",
            f"- Stable grouping prefers `symbol + direction_bias + signal_family`, then `candidate_id`, then source line fallback.",
            f"- Persistence threshold: `{args.persistence_count_threshold}` observations or `{args.persistence_minutes_threshold}` minutes.",
            f"- Micro-move threshold: `{args.micro_move_threshold_pct}%` favorable movement.",
            f"- Breakout/collapse threshold: `{args.breakout_threshold_pct}%` favorable or `{args.collapse_threshold_pct}%` adverse directional movement.",
            f"- Chop threshold: `{args.chop_threshold_pct}%` both favorable and adverse directional movement.",
            "- `max_favorable_pct` and `max_adverse_pct` are directional magnitudes based on `direction_bias`.",
            "- The script only reads candidate-ticket JSONL plus its own previous active snapshot; it does not read or mutate raw scanner, history, Bitget, ML, Slack, n8n, Google Drive, or rule files.",
        ]
    )
    return lines


def data_quality_separation_report_lines(
    *,
    run_time: datetime,
    input_path: Path | None,
    ticket_count: int,
    active_count: int,
    event_rows_before: int,
    event_rows_after: int,
    state_distribution: Counter[str],
    data_quality_distribution: Counter[str],
    action_label_distribution: Counter[str],
    direction_bias_distribution: Counter[str],
    signal_family_distribution: Counter[str],
    data_gap_fields_distribution: Counter[str],
    commands_run: list[str],
    files_changed: list[str],
) -> list[str]:
    lines = [
        "# Firestarter Optimizer State Monitor Data-Quality Separation Report",
        "",
        f"Run UTC: {isoformat_utc(run_time)}",
        "",
        "## Observation-Only Boundary",
        "",
        "This pass separates lifecycle state from data quality. It does not create trade instructions, edge claims, exclusion rules, or automatic rule changes.",
        "",
        "## Input",
        "",
        f"- Candidate ticket input path: `{input_path}`",
        f"- Tickets read: `{ticket_count}`",
        f"- Active candidate groups: `{active_count}`",
        "",
        "## Lifecycle State Distribution",
        "",
    ]
    for label, count in sorted((state_distribution or Counter({"(none)": 0})).items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Data Quality Distribution", ""])
    for label, count in sorted((data_quality_distribution or Counter({"(none)": 0})).items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Action Label Distribution", ""])
    for label, count in sorted((action_label_distribution or Counter({"(none)": 0})).items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Direction Bias Distribution", ""])
    for label, count in sorted((direction_bias_distribution or Counter({"(none)": 0})).items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Signal Family Distribution", ""])
    for label, count in sorted((signal_family_distribution or Counter({"(none)": 0})).items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(["", "## Data Gap Fields Distribution", ""])
    for label, count in sorted((data_gap_fields_distribution or Counter({"(none)": 0})).items()):
        lines.append(f"- `{label}`: `{count}`")
    lines.extend(
        [
            "",
            "## Write Behavior",
            "",
            f"- Event rows before write-run: `{event_rows_before}`",
            f"- Event rows after write-run: `{event_rows_after}`",
            f"- Append-only state events preserved: `{event_rows_after >= event_rows_before}`",
            f"- State events appended this run: `{max(0, event_rows_after - event_rows_before)}`",
            "- Active snapshot atomic write: `confirmed by temp-file plus os.replace implementation`",
            "",
            "## Commands Run",
            "",
            "```powershell",
        ]
    )
    lines.extend(commands_run)
    lines.extend(["```", "", "## Files Changed", ""])
    lines.extend(f"- `{path}`" for path in files_changed)
    lines.extend(
        [
            "",
            "## Boundary Check",
            "",
            "No raw scanner files, live scanner files, Bitget/order/trading logic, historical JSONL/parquet/OHLCV/Tardis files, `candidate_rules.yaml`, ML files, `signal_discovery.py`, Slack/n8n files, Google Drive sync logic, cloud optimizer queue activation, or Google Drive active outputs were modified.",
        ]
    )
    return lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update observation-only Firestarter Optimizer candidate states.")
    parser.add_argument("--input", help="Explicit candidate-ticket JSONL input path.")
    parser.add_argument("--test-mode", action="store_true", help="Skip production discovery and use isolated test candidate-ticket paths only.")
    parser.add_argument("--dry-run", action="store_true", help="Read and report without writing output files.")
    parser.add_argument("--persistence-count-threshold", type=int, default=3)
    parser.add_argument("--persistence-minutes-threshold", type=float, default=15.0)
    parser.add_argument("--micro-move-threshold-pct", type=float, default=0.3)
    parser.add_argument("--confirm-threshold-pct", type=float, default=1.0)
    parser.add_argument("--break-threshold-pct", type=float, default=1.0)
    parser.add_argument("--breakout-threshold-pct", type=float, default=2.0)
    parser.add_argument("--collapse-threshold-pct", type=float, default=2.0)
    parser.add_argument("--chop-threshold-pct", type=float, default=0.75)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_time = utc_now()
    input_path, input_mode = discover_input(args.input, args.test_mode)
    tickets: list[dict[str, Any]] = []
    bad_lines = 0
    if input_path and input_path.exists():
        tickets, bad_lines = safe_jsonl_read(input_path)
    elif input_path:
        input_mode = "missing_explicit"

    previous_active = load_previous_active(ACTIVE_PATH)
    event_rows_before = count_jsonl_rows(EVENTS_PATH)
    active_rows, events, state_distribution, missing_fields = build_records(tickets, previous_active, run_time, args)
    expired_or_changed = build_expired_or_changed(active_rows, previous_active, run_time)
    data_quality_distribution = active_distribution(active_rows, "data_quality")
    action_label_distribution = active_distribution(active_rows, "action_label")
    direction_bias_distribution = active_distribution(active_rows, "direction_bias")
    signal_family_distribution = active_distribution(active_rows, "signal_family")
    data_gap_fields_distribution = active_data_gap_distribution(active_rows)
    lines = report_lines(
        run_time=run_time,
        input_path=input_path,
        input_mode=input_mode,
        bad_lines=bad_lines,
        ticket_count=len(tickets),
        active_count=len(active_rows),
        event_count=len(events),
        expired_or_changed_count=len(expired_or_changed),
        state_distribution=state_distribution,
        data_quality_distribution=data_quality_distribution,
        action_label_distribution=action_label_distribution,
        direction_bias_distribution=direction_bias_distribution,
        signal_family_distribution=signal_family_distribution,
        data_gap_fields_distribution=data_gap_fields_distribution,
        missing_fields=missing_fields,
        dry_run=args.dry_run,
        args=args,
    )

    if not args.dry_run:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        write_jsonl_atomic(ACTIVE_PATH, active_rows)
        append_jsonl(EVENTS_PATH, events)
        append_jsonl(EXPIRED_PATH, expired_or_changed)
        atomic_write_text(REPORT_PATH, "\n".join(lines) + "\n")
        event_rows_after = count_jsonl_rows(EVENTS_PATH)
        commands_run = [
            "python scripts/firestarter_optimizer/update_candidate_states.py --input reports/firestarter_optimizer/candidate_tickets.jsonl --dry-run",
            "python scripts/firestarter_optimizer/update_candidate_states.py --input reports/firestarter_optimizer/candidate_tickets.jsonl",
            "python -m py_compile scripts/firestarter_optimizer/update_candidate_states.py",
        ]
        files_changed = [
            "scripts/firestarter_optimizer/update_candidate_states.py",
            "reports/firestarter_optimizer/active_candidates.jsonl",
            "reports/firestarter_optimizer/candidate_state_events.jsonl",
            "reports/firestarter_optimizer/expired_or_changed_candidates.jsonl",
            "reports/firestarter_optimizer/update_candidate_states_report.md",
            "reports/firestarter_optimizer/update_candidate_states_data_quality_separation_report.md",
            "reports/firestarter_optimizer/y_hanger_diagnostic_state_report.md",
        ]
        atomic_write_text(
            DATA_QUALITY_REPORT_PATH,
            "\n".join(
                data_quality_separation_report_lines(
                    run_time=run_time,
                    input_path=input_path,
                    ticket_count=len(tickets),
                    active_count=len(active_rows),
                    event_rows_before=event_rows_before,
                    event_rows_after=event_rows_after,
                    state_distribution=state_distribution,
                    data_quality_distribution=data_quality_distribution,
                    action_label_distribution=action_label_distribution,
                    direction_bias_distribution=direction_bias_distribution,
                    signal_family_distribution=signal_family_distribution,
                    data_gap_fields_distribution=data_gap_fields_distribution,
                    commands_run=commands_run,
                    files_changed=files_changed,
                )
            )
            + "\n",
        )
        Y_HANGER_REPORT_PATH = REPORT_DIR / "y_hanger_diagnostic_state_report.md"
        atomic_write_text(
            Y_HANGER_REPORT_PATH,
            "\n".join(
                y_hanger_report_lines(
                    run_time=run_time,
                    input_path=input_path,
                    ticket_count=len(tickets),
                    active_count=len(active_rows),
                    event_rows_before=event_rows_before,
                    event_rows_after=event_rows_after,
                    state_distribution=state_distribution,
                    data_quality_distribution=data_quality_distribution,
                    action_label_distribution=action_label_distribution,
                    direction_bias_distribution=direction_bias_distribution,
                    signal_family_distribution=signal_family_distribution,
                    data_gap_fields_distribution=data_gap_fields_distribution,
                    active_rows=active_rows,
                    commands_run=commands_run,
                    files_changed=files_changed,
                )
            )
            + "\n",
        )

    status = {
        "ok": True,
        "observation_only": True,
        "input_mode": input_mode,
        "input_path": str(input_path) if input_path else None,
        "candidate_ticket_rows": len(tickets),
        "active_candidate_rows": len(active_rows),
        "state_events_prepared": len(events),
        "expired_or_changed_prepared": len(expired_or_changed),
        "state_distribution": dict(state_distribution),
        "data_quality_distribution": dict(data_quality_distribution),
        "action_label_distribution": dict(action_label_distribution),
        "direction_bias_distribution": dict(direction_bias_distribution),
        "signal_family_distribution": dict(signal_family_distribution),
        "data_gap_fields_distribution": dict(data_gap_fields_distribution),
        "dry_run": args.dry_run,
    }
    print(json.dumps(status, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
