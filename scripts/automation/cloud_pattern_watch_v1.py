#!/usr/bin/env python3
"""Manual-only cloud pattern watch for FirestarterSPB research notifications.

This script evaluates precomputed metric snapshots. It does not fetch market data,
calculate production scores, trade, or change optimizer state.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ntfy_notify import send_ntfy


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "configs" / "cloud_pattern_watch_v1.json"
DEFAULT_FIXTURE = REPO_ROOT / "configs" / "cloud_pattern_watch_v1_fixture.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"required JSON file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def load_symbol_guard(config: dict[str, Any]) -> tuple[set[str], set[str], str]:
    symbol_config = config.get("symbol_config")
    if not symbol_config:
        return set(), set(), "UNCONFIGURED"
    payload = read_json(repo_path(symbol_config))
    approved = {str(symbol).upper().strip() for symbol in payload.get("symbols", []) if str(symbol).strip()}
    excluded = {str(symbol).upper().strip() for symbol in payload.get("excluded_symbols", []) if str(symbol).strip()}
    return approved, excluded, str(payload.get("status", "UNKNOWN"))


def write_report(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Cloud Pattern Watch v1 Report",
        "",
        f"Generated UTC: `{event['timestamp_utc']}`",
        f"Mode: `{event['mode']}`",
        f"Fixture test: `{event.get('fixture_test', False)}`",
        f"Snapshot source: `{event['snapshot_source']}`",
        f"Rows evaluated: `{event['rows_evaluated']}`",
        f"Rows rejected: `{event['rows_rejected']}`",
        f"Candidates: `{len(event['candidates'])}`",
        f"Symbol config status: `{event['symbol_config_status']}`",
        "",
        "## Safety",
        "",
        "- live_trading: `false`",
        "- exchange_execution: `false`",
        "- exchange_credentials: `false`",
        "- optimizer_production: `false`",
        "- scoring_changes: `false`",
        "",
        "## Candidates",
        "",
    ]
    if not event["candidates"]:
        lines.append("- None")
    else:
        for candidate in event["candidates"]:
            lines.append(
                "- "
                f"`{candidate['symbol']}` "
                f"price_position={candidate['price_position']} "
                f"fmlc={candidate['fmlc']} "
                f"er={candidate['er']} "
                f"flowprint={candidate['flowprint']} "
                f"raw_score={candidate['raw_score']} "
                f"reason=`{candidate['reason']}`"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def numeric(row: dict[str, Any], key: str) -> float | None:
    value = row.get(key)
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def sample_snapshot() -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "source": "embedded_sample_approved_symbol",
        "rows": [
            {
                "symbol": "BTCUSDT",
                "timestamp_utc": utc_now(),
                "price": "1.0000",
                "price_position": 0.92,
                "fmlc": 8.4,
                "er": 1.1,
                "flowprint": 3.2,
                "raw_score": 5.6,
            }
        ],
    }


def rows_from_snapshot(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    rows = snapshot.get("rows", [])
    if not isinstance(rows, list):
        raise ValueError("snapshot JSON must contain a rows list")
    return [row for row in rows if isinstance(row, dict)]


def apply_symbol_guard(rows: list[dict[str, Any]], approved: set[str], excluded: set[str]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    if not approved and not excluded:
        return rows, {}
    kept: list[dict[str, Any]] = []
    rejected: dict[str, int] = {}
    for row in rows:
        symbol = str(row.get("symbol", "")).upper().strip()
        if not symbol:
            rejected["missing_symbol"] = rejected.get("missing_symbol", 0) + 1
            continue
        if symbol in excluded:
            rejected["excluded_symbol"] = rejected.get("excluded_symbol", 0) + 1
            continue
        if approved and symbol not in approved:
            rejected["unapproved_symbol"] = rejected.get("unapproved_symbol", 0) + 1
            continue
        kept.append(row)
    return kept, rejected


def evaluate_row(row: dict[str, Any], thresholds: dict[str, Any], pattern_key: str) -> dict[str, Any] | None:
    symbol = str(row.get("symbol", "")).upper().strip()
    if not symbol:
        return None

    price_position = numeric(row, "price_position")
    fmlc = numeric(row, "fmlc")
    er = numeric(row, "er")
    flowprint = numeric(row, "flowprint")
    raw_score = numeric(row, "raw_score")

    required = [price_position, fmlc, er, flowprint, raw_score]
    if any(value is None for value in required):
        return None

    price_near_high = price_position >= float(thresholds["min_price_position"])
    fmlc_high = fmlc >= float(thresholds["min_fmlc"])
    er_weak = er <= float(thresholds["max_er"])
    flow_not_confirming = flowprint <= float(thresholds["max_flowprint"]) or raw_score <= float(thresholds["max_raw_score"])

    if not (price_near_high and fmlc_high and er_weak and flow_not_confirming):
        return None

    return {
        "symbol": symbol,
        "timestamp_utc": str(row.get("timestamp_utc") or ""),
        "pattern_key": pattern_key,
        "price": row.get("price"),
        "price_position": price_position,
        "fmlc": fmlc,
        "er": er,
        "flowprint": flowprint,
        "raw_score": raw_score,
        "reason": "elevated price position with strong structure metric but weak momentum/participation confirmation",
        "research_only": True,
    }


def build_message(display_label: str, candidates: list[dict[str, Any]]) -> str:
    if not candidates:
        return f"{display_label}: no candidates. Research only."
    first = candidates[0]
    extra = "" if len(candidates) == 1 else f" +{len(candidates) - 1} more"
    return (
        f"{display_label} — {first['symbol']}{extra}. "
        f"price_position={first['price_position']:.2f} fmlc={first['fmlc']:.2f} "
        f"er={first['er']:.2f} flowprint={first['flowprint']:.2f} raw_score={first['raw_score']:.2f}. "
        "Research only. No trading/scoring change."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate manual cloud metric snapshots for research pattern notifications.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--snapshot", default=None, help="Optional metric snapshot JSON path.")
    parser.add_argument("--sample", action="store_true", help="Use embedded sample snapshot.")
    parser.add_argument("--fixture-test", action="store_true", help="Use committed fixture snapshot for controlled manual testing.")
    parser.add_argument("--fixture-file", default=str(DEFAULT_FIXTURE), help="Fixture JSON path used with --fixture-test.")
    parser.add_argument("--send", action="store_true", help="Send ntfy when candidates exist or notify-empty is set.")
    parser.add_argument("--dry-run", action="store_true", help="Evaluate and write logs/reports without ntfy send.")
    parser.add_argument("--notify-empty", action="store_true", help="Send a no-candidates message. Useful for manual tests only.")
    args = parser.parse_args()

    if args.fixture_test and (args.sample or args.snapshot):
        raise SystemExit("--fixture-test cannot be combined with --sample or --snapshot")

    config = read_json(repo_path(args.config))
    approved, excluded, symbol_config_status = load_symbol_guard(config)
    watch = config["watch"]
    pattern_key = watch["pattern_key"]
    display_label = watch["display_label"]
    thresholds = watch["thresholds"]

    fixture_test = bool(args.fixture_test)
    if fixture_test:
        fixture_path = repo_path(args.fixture_file)
        snapshot = read_json(fixture_path)
        snapshot_source = str(fixture_path.relative_to(REPO_ROOT)) if fixture_path.is_relative_to(REPO_ROOT) else str(fixture_path)
    elif args.sample:
        snapshot = sample_snapshot()
        snapshot_source = "embedded_sample_approved_symbol"
    else:
        snapshot_path = repo_path(args.snapshot or config["paths"]["snapshot"])
        snapshot = read_json(snapshot_path)
        snapshot_source = str(snapshot_path.relative_to(REPO_ROOT)) if snapshot_path.is_relative_to(REPO_ROOT) else str(snapshot_path)

    raw_rows = rows_from_snapshot(snapshot)
    rows, rejected = apply_symbol_guard(raw_rows, approved, excluded)
    candidates = [candidate for row in rows if (candidate := evaluate_row(row, thresholds, pattern_key))]

    event = {
        "timestamp_utc": utc_now(),
        "mode": "send" if args.send else "dry_run",
        "fixture_test": fixture_test,
        "watch_status": config["status"],
        "display_label": display_label,
        "pattern_key": pattern_key,
        "snapshot_source": snapshot_source,
        "rows_evaluated": len(rows),
        "rows_rejected": sum(rejected.values()),
        "reject_reasons": rejected,
        "symbol_config_status": symbol_config_status,
        "candidates": candidates,
        "ok": True,
        "safety_flags": config["safety_flags"],
    }

    event_log = repo_path(config["paths"]["event_log"])
    report = repo_path(config["paths"]["report"])
    append_jsonl(event_log, event)
    write_report(report, event)

    notification_result: dict[str, Any] = {"ok": True, "sent": False, "reason": "send not requested"}
    should_send = bool(args.send and (candidates or args.notify_empty))
    if should_send:
        notification_result = send_ntfy(
            env_path=Path(config["ntfy"]["env_path"]),
            title=display_label,
            message=build_message(display_label, candidates),
            priority=str(config["notification"]["priority"]),
            tags=str(config["notification"]["tags"]),
            dry_run=False,
        )
        notification_result["sent"] = True
    elif args.send:
        notification_result = {"ok": True, "sent": False, "reason": "no candidates"}

    output = {"event": event, "notification_result": notification_result}
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if notification_result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
