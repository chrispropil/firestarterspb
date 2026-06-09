"""Build a compact Firestarter Live Audits AI match index.

Research-only utility.

This script is intended to create a compact, derived, AI-readable table from the
local Binance Top100 FirestarterOG research dataset. It does not modify source
market data, scanner files, dashboard HTML, or existing raw artifacts.

IMPORTANT:
- No trading signals.
- No strategy validation.
- No Cell 2 labels.
- No live execution.
- No raw 5-minute export in the output index.

The first implementation pass should reuse metric logic from:
    scripts/visualization/build_top100_clean_html_dashboard.py

Default output:
    reports/firestarter_live_audits/ai_match_index.csv
    reports/firestarter_live_audits/ai_match_index_summary.md
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


DEFAULT_CANDLES_DIR = Path(
    r"C:\firestarterspb\data\research\binance_top100_excluding_existing_5_1month"
)
DEFAULT_DERIVATIVES_DIR = Path(
    r"C:\firestarterspb\data\research\binance_top100_derivatives_context_1month"
)
DEFAULT_OUTPUT = Path("reports/firestarter_live_audits/ai_match_index.csv")

REQUIRED_COLUMNS = [
    "timestamp",
    "symbol",
    "close",
    "er",
    "fmlc",
    "flowprint",
    "raw_score",
    "x2_candidate",
    "hollow_breakout",
    "fake_recovery",
    "domino_deterioration",
    "entry_c_recovery",
    "primary_event_type",
    "secondary_tags",
    "data_quality_flags",
    "nan_pct_score",
    "deriv_available",
]


@dataclass(frozen=True)
class BuildSummary:
    run_timestamp_utc: str
    source_candle_dir: str
    source_derivatives_dir: str
    output_path: str
    symbols_seen: int
    symbols_written: int
    row_count: int
    first_timestamp: str
    last_timestamp: str
    notes: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Firestarter Live Audits compact AI match index."
    )
    parser.add_argument("--candles-dir", type=Path, default=DEFAULT_CANDLES_DIR)
    parser.add_argument("--derivatives-dir", type=Path, default=DEFAULT_DERIVATIVES_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Inspect inputs and report intended output without writing CSV.",
    )
    return parser.parse_args()


def discover_symbols(candles_dir: Path) -> list[str]:
    """Discover symbols from local Top100 candle CSV filenames.

    Expected filename pattern:
        <SYMBOL>_1month_5m.csv
    """
    if not candles_dir.exists():
        return []

    symbols: list[str] = []
    for path in sorted(candles_dir.glob("*_1month_5m.csv")):
        symbol = path.name.replace("_1month_5m.csv", "")
        if symbol:
            symbols.append(symbol)
    return symbols


def iter_placeholder_rows(symbols: Iterable[str]) -> Iterable[dict[str, object]]:
    """Yield no data rows in the skeleton implementation.

    This placeholder keeps the file shape safe while allowing Antigravity/Codex to
    add the metric computation in a narrow follow-up patch. The final version
    should resample local 5m candles to 1h, merge derivatives context, and compute
    the approved profile metrics.
    """
    _ = list(symbols)
    return []


def write_csv(output_path: Path, rows: Iterable[dict[str, object]]) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    row_count = 0
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in REQUIRED_COLUMNS})
            row_count += 1
    return row_count


def write_summary(summary_path: Path, summary: BuildSummary) -> None:
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    notes = "\n".join(f"- {note}" for note in summary.notes) if summary.notes else "- None"
    content = f"""# Firestarter Live Audits — AI Match Index Summary

## Status

Research-only derived index summary.

## Run

| Field | Value |
|---|---|
| run_timestamp_utc | `{summary.run_timestamp_utc}` |
| source_candle_dir | `{summary.source_candle_dir}` |
| source_derivatives_dir | `{summary.source_derivatives_dir}` |
| output_path | `{summary.output_path}` |
| symbols_seen | `{summary.symbols_seen}` |
| symbols_written | `{summary.symbols_written}` |
| row_count | `{summary.row_count}` |
| first_timestamp | `{summary.first_timestamp}` |
| last_timestamp | `{summary.last_timestamp}` |

## Notes

{notes}

## Boundary

This index is research-only. It is not a strategy table, signal table, Cell 2 label table, alert source, or execution artifact.
"""
    summary_path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    run_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    symbols = discover_symbols(args.candles_dir)
    notes: list[str] = []

    if not symbols:
        notes.append("No symbols discovered from candle directory.")

    rows = list(iter_placeholder_rows(symbols))

    if args.dry_run:
        print("DRY RUN — no files written")
        print(f"candles_dir={args.candles_dir}")
        print(f"derivatives_dir={args.derivatives_dir}")
        print(f"symbols_seen={len(symbols)}")
        print(f"output={args.output}")
        print("Skeleton implementation only: metric computation not yet enabled.")
        return 0

    row_count = write_csv(args.output, rows)
    summary = BuildSummary(
        run_timestamp_utc=run_timestamp,
        source_candle_dir=str(args.candles_dir),
        source_derivatives_dir=str(args.derivatives_dir),
        output_path=str(args.output),
        symbols_seen=len(symbols),
        symbols_written=0 if row_count == 0 else len(symbols),
        row_count=row_count,
        first_timestamp="N/A",
        last_timestamp="N/A",
        notes=notes
        + [
            "Skeleton builder created index shape only.",
            "Follow-up implementation must reuse approved dashboard metric logic before analysis use.",
        ],
    )
    write_summary(args.output.with_name("ai_match_index_summary.md"), summary)

    print(f"Wrote {args.output}")
    print(f"Wrote {args.output.with_name('ai_match_index_summary.md')}")
    print(f"row_count={row_count}")
    print(f"symbols_seen={len(symbols)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
