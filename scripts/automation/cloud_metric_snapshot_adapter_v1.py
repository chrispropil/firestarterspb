#!/usr/bin/env python3
"""Build Pattern Watch current_snapshot from existing metric files.

Manual only. Reads local precomputed files and writes a normalized snapshot.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "configs" / "cloud_metric_snapshot_adapter_v1.json"

ALIASES = {
    "symbol": ["symbol", "Symbol", "SYMBOL"],
    "timestamp_utc": ["timestamp_utc", "timestamp", "time", "open_time_utc", "datetime", "date"],
    "price": ["price", "close", "last", "Close", "last_price"],
    "price_position": ["price_position", "range_position", "price_range_position", "range_pos"],
    "er": ["er", "er_value", "ER", "er_score"],
    "fmlc": ["fmlc", "fmlc_value", "FMLC", "fmlc_score"],
    "flowprint": ["flowprint", "flowprint_value", "flowprint_proxy_value", "flowprint_proxy", "Flowprint"],
    "raw_score": ["raw_score", "score", "raw", "RawScore"],
}

STATUS_ALIASES = {
    "er": ["er_parent_status", "er_status"],
    "fmlc": ["fmlc_parent_status", "fmlc_status"],
    "flowprint": ["flowprint_parent_status", "flowprint_status"],
    "raw_score": ["raw_score_parent_status", "score_status"],
}

ACCEPTED_STATUS = {"", "full_window_available", "available", "ok", "pass", "ready"}
REQUIRED = ["symbol", "price_position", "er", "fmlc", "flowprint", "raw_score"]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def repo_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_symbols(path: Path) -> tuple[list[str], set[str], str]:
    cfg = read_json(path)
    symbols = [str(s).upper().strip() for s in cfg.get("symbols", []) if str(s).strip()]
    excluded = {str(s).upper().strip() for s in cfg.get("excluded_symbols", []) if str(s).strip()}
    return symbols[:25], excluded, str(cfg.get("status", "UNKNOWN"))


def find_source(config: dict[str, Any]) -> tuple[dict[str, Any] | None, Path | None]:
    for source in config.get("sources", []):
        if source.get("path"):
            path = repo_path(source["path"])
            if path.exists():
                return source, path
        if source.get("glob"):
            matches = [p for p in REPO_ROOT.glob(str(source["glob"])) if p.is_file()]
            if matches:
                matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                return source, matches[0]
    return None, None


def read_rows(path: Path, fmt: str) -> list[dict[str, Any]]:
    if fmt == "csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    payload = read_json(path)
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if isinstance(payload, dict):
        rows = payload.get("rows") or payload.get("data") or payload.get("records") or []
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    raise ValueError(f"Unsupported JSON row layout: {path}")


def pick(row: dict[str, Any], key: str) -> Any:
    for alias in ALIASES[key]:
        if alias in row and row[alias] not in (None, ""):
            return row[alias]
    return None


def pick_status(row: dict[str, Any], key: str) -> str:
    for alias in STATUS_ALIASES.get(key, []):
        if alias in row and row[alias] is not None:
            return str(row[alias]).strip().lower()
    return ""


def as_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_row(row: dict[str, Any], approved: set[str], excluded: set[str]) -> tuple[dict[str, Any] | None, str]:
    symbol = str(pick(row, "symbol") or "").upper().strip()
    if not symbol:
        return None, "missing_symbol"
    if symbol in excluded:
        return None, "excluded_symbol"
    if symbol not in approved:
        return None, "unapproved_symbol"

    for metric in ["er", "fmlc", "flowprint", "raw_score"]:
        if pick_status(row, metric) not in ACCEPTED_STATUS:
            return None, f"status_blocked_{metric}"

    normalized = {
        "symbol": symbol,
        "timestamp_utc": str(pick(row, "timestamp_utc") or ""),
        "price": pick(row, "price"),
        "price_position": as_float(pick(row, "price_position")),
        "er": as_float(pick(row, "er")),
        "fmlc": as_float(pick(row, "fmlc")),
        "flowprint": as_float(pick(row, "flowprint")),
        "raw_score": as_float(pick(row, "raw_score")),
    }

    for key in REQUIRED:
        if normalized.get(key) in (None, ""):
            return None, f"missing_{key}"

    return normalized, "accepted"


def latest_by_symbol(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        symbol = row["symbol"]
        old = latest.get(symbol)
        if old is None or str(row.get("timestamp_utc", "")) >= str(old.get("timestamp_utc", "")):
            latest[symbol] = row
    return [latest[s] for s in sorted(latest)]


def write_report(path: Path, status: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Cloud Metric Snapshot Adapter v1 Report",
        "",
        f"Generated UTC: `{status['timestamp_utc']}`",
        f"Status: `{status['status']}`",
        f"Mode: `{status['mode']}`",
        f"Source: `{status.get('source_path')}`",
        f"Rows read: `{status['rows_read']}`",
        f"Rows accepted: `{status['rows_accepted']}`",
        f"Symbols accepted: `{status['symbols_accepted']}`",
        "",
        "## Rejections",
        "",
    ]
    for reason, count in sorted(status.get("reject_reasons", {}).items()):
        lines.append(f"- `{reason}`: {count}")
    if not status.get("reject_reasons"):
        lines.append("- None")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Pattern Watch snapshot from an existing metric file.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--input", default=None, help="Optional explicit input file path.")
    parser.add_argument("--format", choices=["json", "csv"], default=None, help="Input format when --input is used.")
    parser.add_argument("--dry-run", action="store_true", help="Validate without writing current_snapshot.json.")
    parser.add_argument("--write", action="store_true", help="Write current_snapshot.json.")
    args = parser.parse_args()

    config = read_json(repo_path(args.config))
    approved_list, excluded, symbol_status = load_symbols(repo_path(config["symbol_config"]))
    approved = set(approved_list)

    if args.input:
        source = {"label": "explicit", "format": args.format or Path(args.input).suffix.lstrip(".")}
        source_path = repo_path(args.input)
    else:
        source, source_path = find_source(config)

    status: dict[str, Any] = {
        "timestamp_utc": utc_now(),
        "mode": "write" if args.write else "dry_run",
        "status": "HOLD_NO_SOURCE",
        "ok": False,
        "symbol_config_status": symbol_status,
        "approved_symbol_count": len(approved_list),
        "source_label": None,
        "source_path": None,
        "rows_read": 0,
        "rows_accepted": 0,
        "symbols_accepted": 0,
        "reject_reasons": {},
    }

    paths = config["paths"]
    if not source or not source_path or not source_path.exists():
        write_json(repo_path(paths["adapter_status"]), status)
        write_report(repo_path(paths["report"]), status)
        print(json.dumps(status, indent=2, sort_keys=True))
        return 1

    fmt = str(source.get("format") or source_path.suffix.lstrip(".")).lower()
    raw_rows = read_rows(source_path, fmt)
    accepted_rows: list[dict[str, Any]] = []
    rejects: dict[str, int] = {}

    for row in raw_rows:
        normalized, reason = normalize_row(row, approved, excluded)
        if normalized is None:
            rejects[reason] = rejects.get(reason, 0) + 1
        else:
            accepted_rows.append(normalized)

    current_rows = latest_by_symbol(accepted_rows)
    snapshot = {
        "timestamp_utc": utc_now(),
        "source": str(source.get("label", "unknown")),
        "source_path": str(source_path.relative_to(REPO_ROOT)) if source_path.is_relative_to(REPO_ROOT) else str(source_path),
        "symbol_config_status": symbol_status,
        "rows": current_rows,
    }

    status.update(
        {
            "status": "PASS" if current_rows else "HOLD_NO_VALID_ROWS",
            "ok": bool(current_rows),
            "source_label": source.get("label"),
            "source_path": snapshot["source_path"],
            "rows_read": len(raw_rows),
            "rows_accepted": len(accepted_rows),
            "symbols_accepted": len(current_rows),
            "reject_reasons": rejects,
        }
    )

    if args.write and current_rows:
        write_json(repo_path(paths["current_snapshot"]), snapshot)
        status["snapshot_written"] = True
    else:
        status["snapshot_written"] = False

    write_json(repo_path(paths["adapter_status"]), status)
    write_report(repo_path(paths["report"]), status)
    print(json.dumps(status, indent=2, sort_keys=True))
    return 0 if status["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
