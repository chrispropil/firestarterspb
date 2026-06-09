"""Search the derived Firestarter Live Audits AI Match Index.

Research-only utility. Operates only on ai_match_index.csv and writes derived
pattern-search outputs. It does not read raw candles or mutate source artifacts.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


DEFAULT_INPUT = Path("reports/firestarter_live_audits/ai_match_index.csv")
DEFAULT_OUTPUT_DIR = Path("reports/firestarter_live_audits/pattern_searches")
DEFAULT_DRIVE_DIR = Path(
    r"G:\My Drive\Matrix Alpha\FirestarterOG\Live Audits\Pattern Searches"
)
BOUNDARY_WARNING = (
    "This is a research-only pattern search. Matches are setup hypotheses / "
    "profile behavior candidates only. They are not signals, strategies, "
    "entries, exits, trades, alerts, validated edge, or Cell 2 labels."
)

BASE_COLUMNS = [
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
DERIVED_COLUMNS = ["movement_score"]
OUTPUT_COLUMNS = BASE_COLUMNS + DERIVED_COLUMNS


@dataclass(frozen=True)
class SearchOutputs:
    matches_path: Path
    summary_path: Path
    top_examples_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search ai_match_index.csv with flexible metric fingerprints."
    )
    parser.add_argument("--pattern-name", required=True)
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--symbol")
    parser.add_argument("--min-fmlc", type=float)
    parser.add_argument("--max-fmlc", type=float)
    parser.add_argument("--min-flowprint", type=float)
    parser.add_argument("--max-flowprint", type=float)
    parser.add_argument("--min-raw-score", type=float)
    parser.add_argument("--max-raw-score", type=float)
    parser.add_argument("--min-er", type=float)
    parser.add_argument("--max-er", type=float)
    parser.add_argument("--fmlc-rising-hours", type=int)
    parser.add_argument("--fmlc-falling-hours", type=int)
    parser.add_argument("--raw-score-rising-hours", type=int)
    parser.add_argument("--raw-score-falling-hours", type=int)
    parser.add_argument("--flowprint-rising-hours", type=int)
    parser.add_argument("--flowprint-falling-hours", type=int)
    parser.add_argument("--price-up-hours", type=int)
    parser.add_argument("--price-down-hours", type=int)
    parser.add_argument("--price-compression-hours", type=int)
    parser.add_argument("--prior-return-hours", type=int)
    parser.add_argument("--min-prior-return-pct", type=float)
    parser.add_argument("--near-recent-high-hours", type=int)
    parser.add_argument("--max-distance-from-recent-high-pct", type=float)
    parser.add_argument("--forward-return-hours", type=int)
    parser.add_argument("--max-forward-return-pct", type=float)
    parser.add_argument("--upper-range-hours", type=int)
    parser.add_argument("--min-close-position-in-range", type=float)
    parser.add_argument("--primary-event-type")
    parser.add_argument("--secondary-tag-contains")
    parser.add_argument("--data-quality-exclude")
    parser.add_argument("--top-n", type=int, default=50)
    parser.add_argument("--sync-drive", action="store_true")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--drive-dir", type=Path, default=DEFAULT_DRIVE_DIR)
    return parser.parse_args()


def clean_pattern_name(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in value)
    cleaned = cleaned.strip("._-")
    if not cleaned:
        raise ValueError("--pattern-name must contain at least one safe character")
    return cleaned


def parse_yyyy_mm_dd(value: str | None, label: str) -> str | None:
    if value is None:
        return None
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{label} must use YYYY-MM-DD format: {value}") from exc
    return value


def to_float(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def read_index(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing input index: {path}")

    rows: list[dict[str, object]] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [col for col in BASE_COLUMNS if col not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Input index missing required columns: {', '.join(missing)}")

        for row in reader:
            typed = dict(row)
            for col in ("close", "er", "fmlc", "flowprint", "raw_score", "nan_pct_score"):
                typed[f"_{col}"] = to_float(row.get(col))
            rows.append(typed)

    return rows


def attach_history(rows: list[dict[str, object]]) -> None:
    by_symbol: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_symbol[str(row["symbol"])].append(row)

    for symbol_rows in by_symbol.values():
        symbol_rows.sort(key=lambda item: str(item["timestamp"]))
        for idx, row in enumerate(symbol_rows):
            row["_symbol_index"] = idx
            row["_symbol_rows"] = symbol_rows


def value_at(row: dict[str, object], metric: str, hours_back: int) -> float | None:
    symbol_rows = row["_symbol_rows"]
    idx = int(row["_symbol_index"]) - hours_back
    if idx < 0:
        return None
    return symbol_rows[idx].get(f"_{metric}")  # type: ignore[index]


def future_value_at(row: dict[str, object], metric: str, hours_forward: int) -> float | None:
    symbol_rows = row["_symbol_rows"]
    idx = int(row["_symbol_index"]) + hours_forward
    if idx >= len(symbol_rows):  # type: ignore[arg-type]
        return None
    return symbol_rows[idx].get(f"_{metric}")  # type: ignore[index]


def has_risen(row: dict[str, object], metric: str, hours: int) -> bool:
    current = row.get(f"_{metric}")
    prior = value_at(row, metric, hours)
    return current is not None and prior is not None and float(current) > float(prior)


def has_fallen(row: dict[str, object], metric: str, hours: int) -> bool:
    current = row.get(f"_{metric}")
    prior = value_at(row, metric, hours)
    return current is not None and prior is not None and float(current) < float(prior)


def prior_return_pct(row: dict[str, object], hours: int) -> float | None:
    current = row.get("_close")
    prior = value_at(row, "close", hours)
    if current is None or prior is None or float(prior) == 0:
        return None
    return ((float(current) - float(prior)) / float(prior)) * 100


def forward_return_pct(row: dict[str, object], hours: int) -> float | None:
    current = row.get("_close")
    future = future_value_at(row, "close", hours)
    if current is None or future is None or float(current) == 0:
        return None
    return ((float(future) - float(current)) / float(current)) * 100


def distance_from_recent_high_pct(row: dict[str, object], hours: int) -> float | None:
    current = row.get("_close")
    if current is None:
        return None

    symbol_rows = row["_symbol_rows"]
    idx = int(row["_symbol_index"])
    start = idx - hours + 1
    if start < 0:
        return None

    closes = [
        item.get("_close")
        for item in symbol_rows[start : idx + 1]  # type: ignore[index]
        if item.get("_close") is not None
    ]
    if len(closes) < hours:
        return None

    recent_high = max(float(value) for value in closes)
    if recent_high <= 0:
        return None
    return ((recent_high - float(current)) / recent_high) * 100


def close_position_in_range(row: dict[str, object], hours: int) -> float | None:
    current = row.get("_close")
    if current is None:
        return None

    symbol_rows = row["_symbol_rows"]
    idx = int(row["_symbol_index"])
    start = idx - hours + 1
    if start < 0:
        return None

    closes = [
        item.get("_close")
        for item in symbol_rows[start : idx + 1]  # type: ignore[index]
        if item.get("_close") is not None
    ]
    if len(closes) < hours:
        return None

    recent_low = min(float(value) for value in closes)
    recent_high = max(float(value) for value in closes)
    rolling_range = recent_high - recent_low
    if rolling_range == 0:
        return None
    return (float(current) - recent_low) / rolling_range


def compressed_price(row: dict[str, object], hours: int) -> bool:
    symbol_rows = row["_symbol_rows"]
    idx = int(row["_symbol_index"])
    start = idx - hours + 1
    if start < 0:
        return False
    closes = [
        item.get("_close")
        for item in symbol_rows[start : idx + 1]  # type: ignore[index]
        if item.get("_close") is not None
    ]
    if len(closes) < hours:
        return False
    high = max(float(value) for value in closes)
    low = min(float(value) for value in closes)
    last = float(closes[-1])
    if last <= 0:
        return False
    return ((high - low) / last) * 100 <= 1.0


def meets_min_prior_return(row: dict[str, object], hours: int, threshold: float) -> bool:
    value = prior_return_pct(row, hours)
    return value is not None and value >= threshold


def meets_max_forward_return(row: dict[str, object], hours: int, threshold: float) -> bool:
    value = forward_return_pct(row, hours)
    return value is not None and value <= threshold


def near_recent_high(row: dict[str, object], hours: int, threshold: float) -> bool:
    value = distance_from_recent_high_pct(row, hours)
    return value is not None and value <= threshold


def meets_min_close_position(row: dict[str, object], hours: int, threshold: float) -> bool:
    value = close_position_in_range(row, hours)
    return value is not None and value >= threshold


def movement_delta(row: dict[str, object], metric: str, hours: int | None) -> float:
    if not hours:
        return 0.0
    current = row.get(f"_{metric}")
    prior = value_at(row, metric, hours)
    if current is None or prior is None:
        return 0.0
    return abs(float(current) - float(prior))


def attach_movement_score(row: dict[str, object], args: argparse.Namespace) -> None:
    score = 0.0
    score += movement_delta(row, "fmlc", args.fmlc_rising_hours)
    score += movement_delta(row, "fmlc", args.fmlc_falling_hours)
    score += movement_delta(row, "raw_score", args.raw_score_rising_hours)
    score += movement_delta(row, "raw_score", args.raw_score_falling_hours)
    score += movement_delta(row, "flowprint", args.flowprint_rising_hours)
    score += movement_delta(row, "flowprint", args.flowprint_falling_hours)
    score += movement_delta(row, "close", args.price_up_hours)
    score += movement_delta(row, "close", args.price_down_hours)
    if args.prior_return_hours:
        score += abs(prior_return_pct(row, args.prior_return_hours) or 0.0)
    if args.forward_return_hours:
        score += abs(forward_return_pct(row, args.forward_return_hours) or 0.0)
    if args.near_recent_high_hours:
        distance = distance_from_recent_high_pct(row, args.near_recent_high_hours)
        if distance is not None:
            score += max(0.0, 10.0 - distance)
    if args.upper_range_hours:
        position = close_position_in_range(row, args.upper_range_hours)
        if position is not None:
            score += position * 10.0

    if score == 0:
        for metric in ("raw_score", "fmlc", "flowprint", "er"):
            value = row.get(f"_{metric}")
            if value is not None:
                score += float(value)

    row["movement_score"] = f"{score:.6f}".rstrip("0").rstrip(".")
    row["_movement_score"] = score


def add_numeric_filter(
    checks: list[tuple[str, Callable[[dict[str, object]], bool]]],
    label: str,
    metric: str,
    threshold: float | None,
    op: str,
) -> None:
    if threshold is None:
        return
    if op == "min":
        checks.append(
            (
                f"{label} >= {threshold:g}",
                lambda row, metric=metric, threshold=threshold: row.get(f"_{metric}")
                is not None
                and float(row[f"_{metric}"]) >= threshold,
            )
        )
    else:
        checks.append(
            (
                f"{label} <= {threshold:g}",
                lambda row, metric=metric, threshold=threshold: row.get(f"_{metric}")
                is not None
                and float(row[f"_{metric}"]) <= threshold,
            )
        )


def build_checks(args: argparse.Namespace) -> list[tuple[str, Callable[[dict[str, object]], bool]]]:
    start = parse_yyyy_mm_dd(args.start, "--start")
    end = parse_yyyy_mm_dd(args.end, "--end")
    checks: list[tuple[str, Callable[[dict[str, object]], bool]]] = []

    if start:
        checks.append((f"timestamp date >= {start}", lambda row, start=start: str(row["timestamp"])[:10] >= start))
    if end:
        checks.append((f"timestamp date <= {end}", lambda row, end=end: str(row["timestamp"])[:10] <= end))
    if args.symbol:
        symbol = args.symbol.upper()
        checks.append((f"symbol == {symbol}", lambda row, symbol=symbol: str(row["symbol"]).upper() == symbol))

    add_numeric_filter(checks, "fmlc", "fmlc", args.min_fmlc, "min")
    add_numeric_filter(checks, "fmlc", "fmlc", args.max_fmlc, "max")
    add_numeric_filter(checks, "flowprint", "flowprint", args.min_flowprint, "min")
    add_numeric_filter(checks, "flowprint", "flowprint", args.max_flowprint, "max")
    add_numeric_filter(checks, "raw_score", "raw_score", args.min_raw_score, "min")
    add_numeric_filter(checks, "raw_score", "raw_score", args.max_raw_score, "max")
    add_numeric_filter(checks, "er", "er", args.min_er, "min")
    add_numeric_filter(checks, "er", "er", args.max_er, "max")

    if args.fmlc_rising_hours is not None:
        checks.append((f"fmlc rising over {args.fmlc_rising_hours}h", lambda row: has_risen(row, "fmlc", args.fmlc_rising_hours)))
    if args.fmlc_falling_hours is not None:
        checks.append((f"fmlc falling over {args.fmlc_falling_hours}h", lambda row: has_fallen(row, "fmlc", args.fmlc_falling_hours)))
    if args.raw_score_rising_hours is not None:
        checks.append((f"raw_score rising over {args.raw_score_rising_hours}h", lambda row: has_risen(row, "raw_score", args.raw_score_rising_hours)))
    if args.raw_score_falling_hours is not None:
        checks.append((f"raw_score falling over {args.raw_score_falling_hours}h", lambda row: has_fallen(row, "raw_score", args.raw_score_falling_hours)))
    if args.flowprint_rising_hours is not None:
        checks.append((f"flowprint rising over {args.flowprint_rising_hours}h", lambda row: has_risen(row, "flowprint", args.flowprint_rising_hours)))
    if args.flowprint_falling_hours is not None:
        checks.append((f"flowprint falling over {args.flowprint_falling_hours}h", lambda row: has_fallen(row, "flowprint", args.flowprint_falling_hours)))
    if args.price_up_hours is not None:
        checks.append((f"price up over {args.price_up_hours}h", lambda row: has_risen(row, "close", args.price_up_hours)))
    if args.price_down_hours is not None:
        checks.append((f"price down over {args.price_down_hours}h", lambda row: has_fallen(row, "close", args.price_down_hours)))
    if args.price_compression_hours is not None:
        checks.append((f"price compression <= 1.0% over {args.price_compression_hours}h", lambda row: compressed_price(row, args.price_compression_hours)))
    if args.prior_return_hours is not None:
        if args.min_prior_return_pct is None:
            raise ValueError("--prior-return-hours requires --min-prior-return-pct")
        checks.append(
            (
                f"prior return over {args.prior_return_hours}h >= {args.min_prior_return_pct:g}%",
                lambda row: meets_min_prior_return(
                    row, args.prior_return_hours, args.min_prior_return_pct
                ),
            )
        )
    elif args.min_prior_return_pct is not None:
        raise ValueError("--min-prior-return-pct requires --prior-return-hours")

    if args.near_recent_high_hours is not None:
        if args.max_distance_from_recent_high_pct is None:
            raise ValueError(
                "--near-recent-high-hours requires --max-distance-from-recent-high-pct"
            )
        checks.append(
            (
                "distance from recent high over "
                f"{args.near_recent_high_hours}h <= "
                f"{args.max_distance_from_recent_high_pct:g}%",
                lambda row: near_recent_high(
                    row,
                    args.near_recent_high_hours,
                    args.max_distance_from_recent_high_pct,
                ),
            )
        )
    elif args.max_distance_from_recent_high_pct is not None:
        raise ValueError(
            "--max-distance-from-recent-high-pct requires --near-recent-high-hours"
        )

    if args.forward_return_hours is not None:
        if args.max_forward_return_pct is None:
            raise ValueError("--forward-return-hours requires --max-forward-return-pct")
        checks.append(
            (
                f"forward return over {args.forward_return_hours}h <= "
                f"{args.max_forward_return_pct:g}%",
                lambda row: meets_max_forward_return(
                    row, args.forward_return_hours, args.max_forward_return_pct
                ),
            )
        )
    elif args.max_forward_return_pct is not None:
        raise ValueError("--max-forward-return-pct requires --forward-return-hours")

    if args.upper_range_hours is not None:
        if args.min_close_position_in_range is None:
            raise ValueError(
                "--upper-range-hours requires --min-close-position-in-range"
            )
        checks.append(
            (
                "close position in range over "
                f"{args.upper_range_hours}h >= "
                f"{args.min_close_position_in_range:g}",
                lambda row: meets_min_close_position(
                    row,
                    args.upper_range_hours,
                    args.min_close_position_in_range,
                ),
            )
        )
    elif args.min_close_position_in_range is not None:
        raise ValueError(
            "--min-close-position-in-range requires --upper-range-hours"
        )

    if args.primary_event_type:
        event = args.primary_event_type
        checks.append((f"primary_event_type == {event}", lambda row, event=event: str(row.get("primary_event_type", "")) == event))
    if args.secondary_tag_contains:
        needle = args.secondary_tag_contains
        checks.append((f"secondary_tags contains {needle}", lambda row, needle=needle: needle in str(row.get("secondary_tags", ""))))
    if args.data_quality_exclude:
        excluded = args.data_quality_exclude
        checks.append((f"data_quality_flags excludes {excluded}", lambda row, excluded=excluded: excluded not in str(row.get("data_quality_flags", ""))))

    return checks


def output_paths(output_dir: Path, pattern_name: str) -> SearchOutputs:
    output_dir.mkdir(parents=True, exist_ok=True)
    return SearchOutputs(
        matches_path=output_dir / f"{pattern_name}_matches.csv",
        summary_path=output_dir / f"{pattern_name}_summary.md",
        top_examples_path=output_dir / f"{pattern_name}_top_examples.csv",
    )


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in OUTPUT_COLUMNS})


def write_summary(
    path: Path,
    args: argparse.Namespace,
    filters: list[str],
    rows_searched: int,
    matches: list[dict[str, object]],
    outputs: SearchOutputs,
) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    symbol_counts = Counter(str(row["symbol"]) for row in matches)
    top_symbols = ", ".join(symbol for symbol, _ in symbol_counts.most_common(10))
    first_ts = min((str(row["timestamp"]) for row in matches), default="N/A")
    last_ts = max((str(row["timestamp"]) for row in matches), default="N/A")
    filters_text = "\n".join(f"- {item}" for item in filters) if filters else "- None"

    content = f"""# Firestarter Live Audits - Pattern Search Summary

## Search

| Field | Value |
|---|---|
| pattern_name | `{args.pattern_name}` |
| command_run | `{' '.join(sys.argv)}` |
| timestamp_utc | `{timestamp}` |
| input_index_path | `{args.input}` |
| row_count_searched | `{rows_searched}` |
| match_count | `{len(matches)}` |
| symbol_count_matched | `{len(symbol_counts)}` |
| top_matched_symbols | `{top_symbols or 'N/A'}` |
| first_matched_timestamp | `{first_ts}` |
| last_matched_timestamp | `{last_ts}` |
| matches_path | `{outputs.matches_path}` |
| top_examples_path | `{outputs.top_examples_path}` |

## Filters Applied

{filters_text}

## Boundary Warning

{BOUNDARY_WARNING}
"""
    path.write_text(content, encoding="utf-8")


def sync_to_drive(outputs: SearchOutputs, drive_dir: Path) -> None:
    drive_dir.mkdir(parents=True, exist_ok=True)
    for path in (outputs.matches_path, outputs.summary_path, outputs.top_examples_path):
        shutil.copy2(path, drive_dir / path.name)


def main() -> int:
    args = parse_args()
    args.pattern_name = clean_pattern_name(args.pattern_name)
    if args.top_n < 0:
        raise ValueError("--top-n must be >= 0")

    rows = read_index(args.input)
    attach_history(rows)
    checks = build_checks(args)

    matches: list[dict[str, object]] = []
    for row in rows:
        if all(check(row) for _, check in checks):
            attach_movement_score(row, args)
            matches.append(row)

    matches_by_time = sorted(matches, key=lambda row: (str(row["timestamp"]), str(row["symbol"])))
    top_examples = sorted(
        matches,
        key=lambda row: (
            -float(row.get("_movement_score", 0.0)),
            -(float(row.get("_raw_score") or 0.0)),
            str(row["timestamp"]),
            str(row["symbol"]),
        ),
    )[: args.top_n]

    outputs = output_paths(args.output_dir, args.pattern_name)
    write_csv(outputs.matches_path, matches_by_time)
    write_csv(outputs.top_examples_path, top_examples)
    write_summary(
        outputs.summary_path,
        args,
        [label for label, _ in checks],
        len(rows),
        matches,
        outputs,
    )

    if args.sync_drive:
        sync_to_drive(outputs, args.drive_dir)

    print(f"pattern_name={args.pattern_name}")
    print(f"row_count_searched={len(rows)}")
    print(f"match_count={len(matches)}")
    print(f"symbol_count_matched={len(set(str(row['symbol']) for row in matches))}")
    print(f"matches_path={outputs.matches_path}")
    print(f"summary_path={outputs.summary_path}")
    print(f"top_examples_path={outputs.top_examples_path}")
    if args.sync_drive:
        print(f"drive_dir={args.drive_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
