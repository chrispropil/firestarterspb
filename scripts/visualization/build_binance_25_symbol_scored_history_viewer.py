from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INPUT_CSV = ROOT / "data" / "research" / "binance_25_symbol_1month_scored" / "binance_25_symbol_1month_firestarter_scored.csv"
OUT_HTML = ROOT / "reports" / "cloud_pattern_watch" / "v1" / "binance_25_symbol_1month_scored_viewer.html"
REPORT_PATH = ROOT / "reports" / "cloud_pattern_watch" / "v1" / "binance_25_symbol_1month_scored_viewer_report.md"


def as_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def load_rows() -> dict[str, list[dict[str, Any]]]:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Missing scored input CSV: {INPUT_CSV.relative_to(ROOT)}")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    with INPUT_CSV.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            symbol = str(row.get("symbol", "")).strip().upper()
            if not symbol:
                continue
            grouped[symbol].append(row)
    for symbol in grouped:
        grouped[symbol].sort(key=lambda row: str(row.get("timestamp_utc", "")))
    return dict(sorted(grouped.items()))


def build_export(grouped: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    symbols: dict[str, dict[str, Any]] = {}
    for symbol, rows in grouped.items():
        symbols[symbol] = {
            "time": [row.get("timestamp_utc", "") for row in rows],
            "price": [as_float(row.get("price")) for row in rows],
            "er": [as_float(row.get("er")) for row in rows],
            "fmlc": [as_float(row.get("fmlc")) for row in rows],
            "flowprint": [as_float(row.get("flowprint")) for row in rows],
            "raw_score": [as_float(row.get("raw_score")) for row in rows],
            "funding": [as_float(row.get("funding")) for row in rows],
            "rvol_1h": [as_float(row.get("rvol_1h")) for row in rows],
            "rvol_4h_window": [as_float(row.get("rvol_4h_window")) for row in rows],
            "price_position": [as_float(row.get("price_position")) for row in rows],
            "range_pos_20": [as_float(row.get("range_pos_20")) for row in rows],
            "range_pos_50_4h": [as_float(row.get("range_pos_50_4h")) for row in rows],
            "near_breakout": [as_bool(row.get("near_breakout")) for row in rows],
            "clean_reclaim": [as_bool(row.get("clean_reclaim")) for row in rows],
            "above_4h_trend": [as_bool(row.get("above_4h_trend")) for row in rows],
            "data_quality_flags": [row.get("data_quality_flags", "") for row in rows],
            "scoring_mode": [row.get("scoring_mode", "") for row in rows],
        }
    return {
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": str(INPUT_CSV.relative_to(ROOT)),
        "symbols": symbols,
    }


def generate_html(export_data: dict[str, Any]) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Firestarter Binance Scored History Viewer</title>
  <script src=\"https://cdn.plot.ly/plotly-latest.min.js\"></script>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif; margin: 0; background: #eef4f8; color: #0f172a; }}
    .header {{ position: sticky; top: 0; z-index: 10; background: #ffffff; padding: 14px 18px; border-bottom: 1px solid #dbeafe; box-shadow: 0 2px 8px rgba(15,23,42,0.08); }}
    .title {{ font-size: 20px; font-weight: 800; margin-bottom: 8px; }}
    .controls {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
    select, input {{ padding: 7px 10px; font-size: 15px; border: 1px solid #cbd5e1; border-radius: 6px; background: #fff; }}
    .badge {{ padding: 6px 10px; border-radius: 6px; background: #e0f2fe; border: 1px solid #bae6fd; font-size: 13px; }}
    #readout {{ margin-top: 10px; padding: 10px; background: #f8fafc; border: 1px solid #dbeafe; border-radius: 6px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; overflow-x: auto; }}
    #chart {{ margin: 14px; padding: 10px; background: #ffffff; border: 1px solid #dbeafe; border-radius: 8px; min-height: 820px; }}
  </style>
</head>
<body>
  <div class=\"header\">
    <div class=\"title\">Firestarter Binance 25-Symbol 1-Month Scored Viewer</div>
    <div class=\"controls\">
      <label>Symbol <select id=\"symbolSelect\"></select></label>
      <input id=\"symbolSearch\" type=\"text\" placeholder=\"Search symbol...\" />
      <span class=\"badge\" id=\"rowBadge\"></span>
      <span class=\"badge\">Generated: {export_data['generated_utc']}</span>
      <span class=\"badge\">Research only / alerts off</span>
    </div>
    <div id=\"readout\">Hover over the chart to view exact Firestarter metrics.</div>
  </div>
  <div id=\"chart\"></div>
<script>
const exportData = {json.dumps(export_data)};
const symbolsData = exportData.symbols;
const sel = document.getElementById('symbolSelect');
const search = document.getElementById('symbolSearch');
const rowBadge = document.getElementById('rowBadge');
const readout = document.getElementById('readout');

function valuesFor(symbol, key) {{ return symbolsData[symbol][key]; }}
function safeFixed(v, n=4) {{ return (v === null || v === undefined || Number.isNaN(v)) ? '' : Number(v).toFixed(n); }}

function populate(filter='') {{
  const current = sel.value;
  sel.innerHTML = '';
  const symbols = Object.keys(symbolsData).filter(s => s.toLowerCase().includes(filter.toLowerCase())).sort();
  for (const symbol of symbols) {{
    const opt = document.createElement('option');
    opt.value = symbol;
    opt.textContent = symbol;
    sel.appendChild(opt);
  }}
  if (symbols.includes(current)) sel.value = current;
  else if (symbols.length) sel.value = symbols[0];
}}

function draw(symbol) {{
  const sd = symbolsData[symbol];
  if (!sd) return;
  rowBadge.textContent = `${{symbol}} rows: ${{sd.time.length}}`;
  const traces = [
    {{ x: sd.time, y: sd.price, name: 'Price', type: 'scatter', yaxis: 'y', hoverinfo: 'none' }},
    {{ x: sd.time, y: sd.fmlc, name: 'FMLC', type: 'scatter', yaxis: 'y2', hoverinfo: 'none' }},
    {{ x: sd.time, y: sd.flowprint, name: 'Flowprint', type: 'scatter', yaxis: 'y2', hoverinfo: 'none' }},
    {{ x: sd.time, y: sd.raw_score, name: 'Raw Score', type: 'scatter', yaxis: 'y2', hoverinfo: 'none' }},
    {{ x: sd.time, y: sd.er, name: 'ER', type: 'bar', yaxis: 'y3', hoverinfo: 'none' }},
    {{ x: sd.time, y: sd.funding, name: 'Funding', type: 'scatter', yaxis: 'y4', hoverinfo: 'none' }},
  ];
  const layout = {{
    title: symbol + ' Firestarter Scored History',
    height: 860,
    paper_bgcolor: '#ffffff',
    plot_bgcolor: '#f8fafc',
    hovermode: 'x',
    showlegend: true,
    xaxis: {{ title: 'Timestamp UTC', showspikes: true, spikemode: 'across', spikethickness: 1 }},
    yaxis: {{ title: 'Price', domain: [0.68, 1.0], side: 'left', showgrid: true, zeroline: false }},
    yaxis5: {{ title: 'Price', overlaying: 'y', side: 'right', showgrid: false, zeroline: false }},
    yaxis2: {{ title: 'FMLC / Flowprint / Raw', domain: [0.38, 0.64], side: 'left', range: [0, 10], showgrid: true, zeroline: false }},
    yaxis6: {{ title: 'Scores', overlaying: 'y2', side: 'right', range: [0, 10], showgrid: false, zeroline: false }},
    yaxis3: {{ title: 'ER', domain: [0.14, 0.34], side: 'left', range: [0, 10], showgrid: true, zeroline: false }},
    yaxis7: {{ title: 'ER', overlaying: 'y3', side: 'right', range: [0, 10], showgrid: false, zeroline: false }},
    yaxis4: {{ title: 'Funding', domain: [0.0, 0.10], side: 'left', showgrid: true, zeroline: true }},
    margin: {{l: 70, r: 70, t: 60, b: 50}}
  }};
  Plotly.newPlot('chart', traces, layout, {{responsive: true}});
  document.getElementById('chart').on('plotly_hover', function(evt) {{
    const i = evt.points[0].pointIndex;
    readout.innerHTML = `<strong>${{symbol}}</strong> | <strong>Time:</strong> ${{sd.time[i]}} | <strong>Price:</strong> ${{safeFixed(sd.price[i], 4)}} | <strong>ER:</strong> ${{safeFixed(sd.er[i], 2)}} | <strong>FMLC:</strong> ${{safeFixed(sd.fmlc[i], 2)}} | <strong>Flowprint:</strong> ${{safeFixed(sd.flowprint[i], 2)}} | <strong>Raw:</strong> ${{safeFixed(sd.raw_score[i], 4)}} | <strong>Funding:</strong> ${{safeFixed(sd.funding[i], 6)}} | <strong>Mode:</strong> ${{sd.scoring_mode[i]}} | <strong>Flags:</strong> ${{sd.data_quality_flags[i]}}`;
  }});
}}

populate();
sel.addEventListener('change', e => draw(e.target.value));
search.addEventListener('input', e => {{ populate(e.target.value); if (sel.value) draw(sel.value); }});
if (sel.value) draw(sel.value);
</script>
</body>
</html>
"""


def write_report(grouped: dict[str, list[dict[str, Any]]], out_html: Path) -> None:
    total_rows = sum(len(rows) for rows in grouped.values())
    first = min((rows[0].get("timestamp_utc", "") for rows in grouped.values() if rows), default="")
    last = max((rows[-1].get("timestamp_utc", "") for rows in grouped.values() if rows), default="")
    lines = [
        "# Binance 25 Symbol Scored History Viewer Report",
        "",
        f"Generated UTC: `{datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')}`",
        f"Input: `{INPUT_CSV.relative_to(ROOT)}`",
        f"Output HTML: `{out_html.relative_to(ROOT)}`",
        f"Symbols: `{len(grouped)}`",
        f"Rows: `{total_rows}`",
        f"First UTC: `{first}`",
        f"Last UTC: `{last}`",
        "",
        "## Boundary",
        "",
        "Static viewer only. No live state mutation, no Pattern Watch send, no n8n, no trading.",
        "",
        "## Pass Condition",
        "",
        "PASS_BINANCE_25_SYMBOL_SCORED_HISTORY_VIEWER_READY",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    grouped = load_rows()
    export_data = build_export(grouped)
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(generate_html(export_data), encoding="utf-8")
    write_report(grouped, OUT_HTML)
    print("PASS_BINANCE_25_SYMBOL_SCORED_HISTORY_VIEWER_READY")
    print(f"Output: {OUT_HTML.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
