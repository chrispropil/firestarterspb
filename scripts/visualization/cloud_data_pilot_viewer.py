#!/usr/bin/env python3
"""Build a Cloud Data Pilot v1 viewer scaffold."""

from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
CHARTS = [
    "Price + Volume",
    "Price + ER",
    "Price + FMLC",
    "Price + Flowprint",
    "Combined Firestarter State",
    "1H / 4H Trend Context",
    "Outcome Replay",
    "25-Symbol Comparison Board",
    "RVOL / Volume Expansion",
    "Volatility / Range Compression",
]
PENDING_FEATURES = {"ER", "FMLC", "Flowprint", "Combined Firestarter State", "Outcome Replay", "RVOL"}


def repo_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else REPO_ROOT / candidate


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def render(manifest: dict[str, Any]) -> str:
    rows = manifest.get("row_count_by_symbol", {})
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    cards = []
    for chart in CHARTS:
        pending = any(token in chart for token in PENDING_FEATURES)
        note = "PENDING_FEATURE_SOURCE" if pending else "Ready for OHLCV baseline input"
        cards.append(
            f"<section><h2>{html.escape(chart)}</h2><p>{html.escape(note)}</p></section>"
        )
    board_rows = "\n".join(
        f"<tr><td>{html.escape(symbol)}</td><td>{count}</td></tr>" for symbol, count in sorted(rows.items())
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cloud Data Pilot v1 Viewer</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #172033; background: #f7f8fb; }}
    main {{ max-width: 1100px; margin: 0 auto; }}
    section {{ background: #fff; border: 1px solid #d9deea; border-radius: 8px; padding: 14px; margin: 12px 0; }}
    h1, h2 {{ margin: 0 0 8px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d9deea; padding: 8px; text-align: left; }}
    .flags {{ font-family: monospace; }}
  </style>
</head>
<body>
<main>
  <h1>Cloud Data Pilot v1 Viewer</h1>
  <p>Generated: {html.escape(generated)}</p>
  <p class="flags">raw_data_mutation={str(manifest.get("raw_data_mutation", False)).lower()} scoring_changes={str(manifest.get("scoring_changes", False)).lower()} trading_execution={str(manifest.get("trading_execution", False)).lower()}</p>
  {''.join(cards)}
  <section>
    <h2>25-Symbol Comparison Board</h2>
    <table><thead><tr><th>Symbol</th><th>Rows</th></tr></thead><tbody>{board_rows}</tbody></table>
  </section>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Cloud Data Pilot v1 static viewer scaffold.")
    parser.add_argument("--manifest", default="reports/cloud_data_pilot/v1/manifest.json", help="Manifest JSON input path.")
    parser.add_argument("--output", default="reports/cloud_data_pilot/v1/viewer.html", help="Viewer HTML output path.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned viewer output without writing HTML.")
    args = parser.parse_args()

    manifest = load_json(repo_path(args.manifest))
    output = repo_path(args.output)
    if args.dry_run:
        print(json.dumps({"ok": True, "planned_output": str(output.relative_to(REPO_ROOT)), "charts": CHARTS}, indent=2))
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(manifest), encoding="utf-8")
    print(json.dumps({"ok": True, "output": str(output.relative_to(REPO_ROOT)), "charts": CHARTS}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
