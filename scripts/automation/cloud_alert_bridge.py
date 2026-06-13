#!/usr/bin/env python3
"""Cloud-safe FirestarterSPB alert bridge.

This bridge only emits research-control notifications and local JSONL events.
It does not score markets, mutate trading state, use exchange credentials, or
activate scheduled workflows.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ntfy_notify import send_ntfy


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "configs" / "cloud_alert_bridge_v1.json"


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


def boundaries() -> dict[str, bool]:
    return {
        "live_trading": False,
        "exchange_execution": False,
        "exchange_credentials": False,
        "optimizer_production": False,
        "scoring_changes": False,
        "cell_2": False,
    }


def build_manual_event(config: dict[str, Any], message: str) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "event_type": "manual_test",
        "ok": True,
        "severity": "info",
        "title": config["notification"]["default_title"],
        "message": message,
        "priority": config["notification"]["default_priority"],
        "tags": config["notification"]["default_tags"],
        "boundaries": boundaries(),
    }


def build_health_event(config: dict[str, Any]) -> dict[str, Any]:
    health_path = repo_path(config["paths"]["health_status"])
    health = read_json(health_path)
    ok = bool(health.get("ok"))
    return {
        "timestamp_utc": utc_now(),
        "event_type": "health",
        "ok": ok,
        "severity": "info" if ok else "hold",
        "title": "FirestarterSPB Health PASS" if ok else "FirestarterSPB Health HOLD",
        "message": f"Cloud health ok={ok}. Mode={health.get('mode')}. Trading/scoring boundaries remain false.",
        "priority": "3" if ok else "5",
        "tags": "fire,white_check_mark" if ok else "fire,warning",
        "source": str(health_path.relative_to(REPO_ROOT)),
        "boundaries": boundaries(),
    }


def build_baseline_audit_event(config: dict[str, Any]) -> dict[str, Any]:
    audit_path = repo_path(config["paths"]["baseline_audit"])
    audit = read_json(audit_path)
    records = audit.get("records", {})
    expected_rows = int(config["baseline_policy"]["expected_rows_per_full_symbol"])
    accepted_zero_rows = set(config["baseline_policy"].get("accepted_zero_row_symbols", []))

    short_symbols: dict[str, int] = {}
    for symbol, record in records.items():
        row_count = int(record.get("row_count", 0))
        if row_count < expected_rows:
            short_symbols[symbol] = row_count

    unexpected_short_symbols = {
        symbol: count
        for symbol, count in short_symbols.items()
        if not (count == 0 and symbol in accepted_zero_rows)
    }

    duplicate_count = int(audit.get("duplicate_count", 0))
    gap_count = int(audit.get("gap_count", 0))
    failed_symbols = list(audit.get("failed_symbols", []))
    total_rows = sum(int(record.get("row_count", 0)) for record in records.values())

    ok = not failed_symbols and duplicate_count == 0 and gap_count == 0 and not unexpected_short_symbols
    status = "PASS" if ok else "HOLD"
    severity = "info" if ok else "hold"
    title = f"FirestarterSPB Baseline Audit {status}"

    message = (
        f"Cloud Data Pilot audit {status}. "
        f"symbols={audit.get('symbol_count')} rows={total_rows} "
        f"duplicates={duplicate_count} gaps={gap_count} failed={failed_symbols or []} "
        f"short={short_symbols or {}} accepted_zero={sorted(accepted_zero_rows)}. "
        "Research only. No scoring/trading."
    )

    return {
        "timestamp_utc": utc_now(),
        "event_type": "baseline_audit",
        "ok": ok,
        "severity": severity,
        "title": title,
        "message": message,
        "priority": "3" if ok else "5",
        "tags": "fire,white_check_mark" if ok else "fire,warning",
        "source": str(audit_path.relative_to(REPO_ROOT)),
        "symbol_count": audit.get("symbol_count"),
        "row_count_total": total_rows,
        "duplicate_count": duplicate_count,
        "gap_count": gap_count,
        "failed_symbols": failed_symbols,
        "short_symbols": short_symbols,
        "unexpected_short_symbols": unexpected_short_symbols,
        "accepted_zero_row_symbols": sorted(accepted_zero_rows),
        "boundaries": boundaries(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a cloud-safe FirestarterSPB alert bridge event.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument(
        "--event-type",
        choices=["manual_test", "health", "baseline_audit"],
        default="baseline_audit",
    )
    parser.add_argument("--message", default="Cloud Alert Bridge manual test.")
    parser.add_argument("--dry-run", action="store_true", help="Build and log event but do not send ntfy.")
    parser.add_argument("--send", action="store_true", help="Send ntfy notification using configured env file.")
    args = parser.parse_args()

    config = read_json(repo_path(args.config))
    if args.event_type == "manual_test":
        event = build_manual_event(config, args.message)
    elif args.event_type == "health":
        event = build_health_event(config)
    else:
        event = build_baseline_audit_event(config)

    event["bridge_status"] = config.get("status", "UNKNOWN")
    event["send_requested"] = bool(args.send)
    event["dry_run"] = bool(args.dry_run or not args.send)

    event_log = repo_path(config["paths"]["event_log"])
    append_jsonl(event_log, event)

    if args.send:
        notification_result = send_ntfy(
            env_path=Path(config["ntfy"]["env_path"]),
            title=event["title"],
            message=event["message"],
            priority=str(event["priority"]),
            tags=str(event["tags"]),
            dry_run=False,
        )
        event["notification_result"] = notification_result
        append_jsonl(event_log, event)
    else:
        notification_result = send_ntfy(
            env_path=Path(config["ntfy"]["env_path"]),
            title=event["title"],
            message=event["message"],
            priority=str(event["priority"]),
            tags=str(event["tags"]),
            dry_run=True,
        )

    output = {"event": event, "notification_result": notification_result}
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if event.get("ok") and notification_result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
