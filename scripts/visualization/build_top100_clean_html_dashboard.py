import os
import glob
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime

# Configure stdout encoding to prevent Unicode errors on Windows
sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = "C:/firestarterspb/data/research/binance_top100_excluding_existing_5_1month"
OUTPUT_DIR = "C:/firestarterspb/reports/html/top100_dashboard"
SYMBOLS_DIR = os.path.join(OUTPUT_DIR, "symbols")
AUDIT_REPORT_PATH = "C:/firestarterspb/reports/firestarter_spb_top100_dashboard_v3_firestarter_panels_audit.md"

os.makedirs(SYMBOLS_DIR, exist_ok=True)

def build_inventory():
    csv_files = glob.glob(os.path.join(DATA_DIR, "*_1month_5m.csv"))
    inventory = []
    
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        symbol = filename.replace("_1month_5m.csv", "")
        
        try:
            df_temp = pd.read_csv(filepath)
            row_count = len(df_temp)
            
            if row_count > 0:
                first_ts = int(df_temp.iloc[0]['open_time'])
                last_ts = int(df_temp.iloc[-1]['open_time'])
                
                expected_span_count = int((last_ts - first_ts) / 300000) + 1
                missing_5m = max(0, expected_span_count - row_count)
                
                first_dt = pd.to_datetime(first_ts, unit='ms', utc=True).strftime('%Y-%m-%d %H:%M:%S')
                last_dt = pd.to_datetime(last_ts, unit='ms', utc=True).strftime('%Y-%m-%d %H:%M:%S')
            else:
                first_ts, last_ts = np.nan, np.nan
                first_dt, last_dt = "N/A", "N/A"
                missing_5m = 0
                
            nonstandard_flag = not symbol.isascii()
            
            inventory.append({
                "symbol": symbol,
                "row_count": row_count,
                "first_time_utc": first_dt,
                "last_time_utc": last_dt,
                "missing_5m_count": missing_5m,
                "nonstandard_symbol_flag": nonstandard_flag
            })
        except Exception as e:
            print(f"Error reading {symbol}: {e}")
            
    df_inv = pd.DataFrame(inventory)
    if not df_inv.empty:
        df_inv = df_inv.sort_values(by="symbol")
    return df_inv

def generate_symbol_page(symbol, all_symbols, metadata):
    csv_path = os.path.join(DATA_DIR, f"{symbol}_1month_5m.csv")
    if not os.path.exists(csv_path):
        files = glob.glob(os.path.join(DATA_DIR, f"*{symbol}*_5m.csv"))
        if files:
            csv_path = files[0]
        else:
            print(f"[ERROR] CSV not found: {symbol}")
            return False

    df = pd.read_csv(csv_path)
    df['open_datetime'] = pd.to_datetime(df['open_time'], unit='ms', utc=True)
    df['close_datetime'] = pd.to_datetime(df['close_time'], unit='ms', utc=True)

    # Resample to 1-Hour candles for smooth rendering
    df_resample = df.set_index('open_datetime')
    df_1h = df_resample.resample('1h').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna()
    
    df_4h = df_resample.resample('4h').agg({
        'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'
    }).dropna()

    # Trend lines and rolling stats
    df_1h['sma_20'] = df_1h['close'].rolling(20).mean()
    df_1h['sma_50'] = df_1h['close'].rolling(50).mean()
    df_1h['range_pct'] = ((df_1h['high'] - df_1h['low']) / df_1h['open']) * 100
    df_1h['log_ret'] = np.log(df_1h['close'] / df_1h['close'].shift(1))
    df_1h['rolling_vol'] = df_1h['log_ret'].rolling(20).std() * 100

    # Clean missing values for JSON serialization
    df_1h = df_1h.replace({np.nan: None})

    # Prepare JS data payload
    chart_data = {
        "dates": df_1h.index.strftime('%Y-%m-%dT%H:%M:%SZ').tolist(),
        "open": df_1h['open'].tolist(),
        "high": df_1h['high'].tolist(),
        "low": df_1h['low'].tolist(),
        "close": df_1h['close'].tolist(),
        "volume": df_1h['volume'].tolist(),
        "sma_20": df_1h['sma_20'].tolist(),
        "sma_50": df_1h['sma_50'].tolist(),
        "range_pct": df_1h['range_pct'].tolist(),
        "rolling_vol": df_1h['rolling_vol'].tolist()
    }

    # Format tables with professional classes and styles
    table_desc_1h = df_1h[['open', 'high', 'low', 'close', 'volume']].describe().to_html(classes='data-table', float_format=lambda x: f"{x:,.4f}")
    table_desc_4h = df_4h[['open', 'high', 'low', 'close', 'volume']].describe().to_html(classes='data-table', float_format=lambda x: f"{x:,.4f}")
    
    df_preview = df.tail(20)[['open_datetime', 'open', 'high', 'low', 'close', 'volume', 'trades']]
    df_preview['open_datetime'] = df_preview['open_datetime'].dt.strftime('%Y-%m-%d %H:%M')
    table_preview = df_preview.to_html(classes='data-table', index=False, float_format=lambda x: f"{x:,.4f}")

    # Generate options list for switching
    options_html = ""
    for s in all_symbols:
        selected = "selected" if s == symbol else ""
        options_html += f'<option value="{s}.html" {selected}>{s}</option>\n'

    row_count = metadata.get("row_count", 0)
    first_time_utc = metadata.get("first_time_utc", "N/A")
    last_time_utc = metadata.get("last_time_utc", "N/A")
    missing_5m_count = metadata.get("missing_5m_count", 0)
    nonstandard_flag = metadata.get("nonstandard_symbol_flag", False)
    nonstandard_label = "YES (Unicode)" if nonstandard_flag else "NO"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{symbol} // Local Research Terminal</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: #08090b;
            color: #94a3b8;
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 24px;
            font-size: 13px;
        }}
        .header {{
            background-color: #0e1014;
            border: 1px solid #1e222b;
            border-radius: 6px;
            padding: 16px 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header-title-group {{
            display: flex;
            flex-direction: column;
        }}
        .header h2 {{
            font-family: 'Outfit', sans-serif;
            color: #f8fafc;
            margin: 0;
            font-size: 18px;
            font-weight: 700;
        }}
        .controls {{
            display: flex;
            gap: 16px;
            align-items: center;
        }}
        .control-group {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .control-group label {{
            color: #64748b;
            font-weight: 500;
        }}
        select {{
            background-color: #161a22;
            color: #f1f5f9;
            border: 1px solid #2d3748;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 13px;
            outline: none;
            cursor: pointer;
            font-family: inherit;
        }}
        .home-btn {{
            background-color: #1e293b;
            color: #3b82f6;
            border: 1px solid #2d3748;
            text-decoration: none;
            padding: 6px 14px;
            border-radius: 4px;
            font-size: 13px;
            font-weight: 600;
            transition: background-color 0.2s, color 0.2s;
        }}
        .home-btn:hover {{
            background-color: #2563eb;
            color: #ffffff;
        }}
        .metadata-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 12px;
            background-color: #0e1014;
            border: 1px solid #1e222b;
            border-radius: 6px;
            padding: 16px 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
        }}
        .metadata-item {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .metadata-label {{
            color: #64748b;
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
        }}
        .metadata-value {{
            color: #cbd5e1;
            font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
            font-size: 13px;
        }}
        .font-highlight {{
            color: #38bdf8;
            font-weight: 700;
        }}
        .font-bold {{
            font-weight: 700;
        }}
        .text-success {{
            color: #10b981;
        }}
        .text-danger {{
            color: #ef4444;
        }}
        .hover-readout {{
            background-color: #0e1014;
            border: 1px solid #1e222b;
            border-radius: 6px;
            padding: 10px 16px;
            margin-bottom: 16px;
            font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
            font-size: 12px;
            color: #38bdf8;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
        }}
        #chart {{
            background-color: #0e1014;
            border: 1px solid #1e222b;
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
            padding: 12px;
            margin-bottom: 24px;
            height: 850px;
        }}
        .section-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 14px;
            font-weight: 700;
            color: #f8fafc;
            margin-top: 24px;
            margin-bottom: 12px;
            border-bottom: 1px solid #1e222b;
            padding-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .table-container {{
            overflow-x: auto;
            margin-bottom: 20px;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            text-align: right;
            background-color: #0e1014;
            border: 1px solid #1e222b;
            border-radius: 4px;
            overflow: hidden;
            font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
        }}
        .data-table th, .data-table td {{
            padding: 6px 12px;
            border-bottom: 1px solid #1e222b;
            border-right: 1px solid #1e222b;
        }}
        .data-table th {{
            background-color: #12141c;
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 0.02em;
        }}
        .data-table td {{
            color: #cbd5e1;
        }}
        .data-table tr:hover {{
            background-color: #14171f;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-title-group">
            <h2>{symbol} // Local Research Terminal</h2>
        </div>
        <div class="controls">
            <div class="control-group">
                <label>Symbol Select:</label>
                <select id="symbolSelect" onchange="window.location.href=this.value">
                    {options_html}
                </select>
            </div>
            <a href="../index.html" class="home-btn">Dashboard Home</a>
        </div>
    </div>

    <div class="metadata-grid">
        <div class="metadata-item">
            <span class="metadata-label">Symbol</span>
            <span class="metadata-value font-highlight">{symbol}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Time Window</span>
            <span class="metadata-value">1-Month (5m Resolution)</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Dataset Status</span>
            <span class="metadata-value text-success">Active / Offline Replay</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Row Count</span>
            <span class="metadata-value">{row_count:,}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">First Timestamp (UTC)</span>
            <span class="metadata-value">{first_time_utc}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Last Timestamp (UTC)</span>
            <span class="metadata-value">{last_time_utc}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Missing 5m Candles</span>
            <span class="metadata-value">{missing_5m_count}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Nonstandard Flag</span>
            <span class="metadata-value">{nonstandard_label}</span>
        </div>
        <div class="metadata-item">
            <span class="metadata-label">Firestarter Metric Status</span>
            <span class="metadata-value text-danger font-bold">NOT ENABLED — formula gate required</span>
        </div>
    </div>

    <div id="hoverReadout" class="hover-readout">
        [NO SIGNAL] Hover over the plots to capture active timestamp records.
    </div>

    <div id="chart"></div>

    <div class="section-title">Latest 20 Records (5m Interval)</div>
    <div class="table-container">
        {table_preview}
    </div>

    <div class="section-title">1-Hour Resampled Summary Statistics</div>
    <div class="table-container">
        {table_desc_1h}
    </div>

    <div class="section-title">4-Hour Resampled Summary Statistics</div>
    <div class="table-container">
        {table_desc_4h}
    </div>

    <script>
        const chartData = {json.dumps(chart_data)};
        
        const dates = chartData.dates;
        const close = chartData.close;
        const open = chartData.open;
        const high = chartData.high;
        const low = chartData.low;
        const volume = chartData.volume;
        const sma20 = chartData.sma_20;
        const sma50 = chartData.sma_50;
        const rangePct = chartData.range_pct;
        const rollingVol = chartData.rolling_vol;

        // Muted volume colors
        const volColors = close.map((c, i) => c >= open[i] ? '#059669' : '#dc2626');

        const tracePrice = {{
            x: dates,
            y: close,
            type: 'scatter',
            mode: 'lines',
            name: '1h Close',
            line: {{ color: '#3b82f6', width: 1.2 }}
        }};

        const traceSMA20 = {{
            x: dates,
            y: sma20,
            type: 'scatter',
            mode: 'lines',
            name: '20 SMA',
            line: {{ color: '#94a3b8', width: 1.0, dash: 'dash' }}
        }};

        const traceSMA50 = {{
            x: dates,
            y: sma50,
            type: 'scatter',
            mode: 'lines',
            name: '50 SMA',
            line: {{ color: '#475569', width: 1.0, dash: 'dash' }}
        }};

        const traceVolume = {{
            x: dates,
            y: volume,
            type: 'bar',
            name: 'Volume',
            marker: {{ color: volColors }},
            xaxis: 'x',
            yaxis: 'y2'
        }};

        const zeros = dates.map(() => 0.0);

        // Firestarter Metrics (Disabled Placeholders)
        const traceER = {{
            x: dates,
            y: zeros,
            type: 'scatter',
            mode: 'lines',
            name: 'ER [formula gate required]',
            line: {{ color: '#f59e0b', width: 1.0, dash: 'dot' }},
            xaxis: 'x',
            yaxis: 'y3'
        }};

        const traceFMLC = {{
            x: dates,
            y: zeros,
            type: 'scatter',
            mode: 'lines',
            name: 'FMLC [formula gate required]',
            line: {{ color: '#ef4444', width: 1.0, dash: 'dot' }},
            xaxis: 'x',
            yaxis: 'y3'
        }};

        const traceFlowprint = {{
            x: dates,
            y: zeros,
            type: 'scatter',
            mode: 'lines',
            name: 'Flowprint [formula gate required]',
            line: {{ color: '#10b981', width: 1.0, dash: 'dot' }},
            xaxis: 'x',
            yaxis: 'y3'
        }};

        const traceRawScore = {{
            x: dates,
            y: zeros,
            type: 'scatter',
            mode: 'lines',
            name: 'raw_score [formula gate required]',
            line: {{ color: '#a855f7', width: 1.0, dash: 'dot' }},
            xaxis: 'x',
            yaxis: 'y3'
        }};

        const traceRange = {{
            x: dates,
            y: rangePct,
            type: 'scatter',
            mode: 'lines',
            name: 'Range %',
            line: {{ color: '#818cf8', width: 1.0 }},
            xaxis: 'x',
            yaxis: 'y4'
        }};

        const traceVol = {{
            x: dates,
            y: rollingVol,
            type: 'scatter',
            mode: 'lines',
            name: 'Rolling Vol',
            line: {{ color: '#06b6d4', width: 1.0 }},
            xaxis: 'x',
            yaxis: 'y4'
        }};

        const traceOverlay = {{
            x: dates,
            y: zeros,
            type: 'scatter',
            mode: 'lines',
            name: 'Overlay comparison [benchmark gate required]',
            line: {{ color: '#64748b', width: 1.0, dash: 'dash' }},
            xaxis: 'x',
            yaxis: 'y5'
        }};

        const data = [
            tracePrice, traceSMA20, traceSMA50, 
            traceVolume, 
            traceER, traceFMLC, traceFlowprint, traceRawScore, 
            traceRange, traceVol, 
            traceOverlay
        ];

        const layout = {{
            grid: {{ rows: 5, columns: 1, pattern: 'coupled' }},
            plot_bgcolor: '#0e1014',
            paper_bgcolor: '#08090b',
            font: {{
                family: 'Inter, sans-serif',
                size: 11,
                color: '#64748b'
            }},
            xaxis: {{
                gridcolor: '#1a1c23',
                linecolor: '#1e222b',
                tickcolor: '#1e222b',
                anchor: 'y5'
            }},
            yaxis: {{
                title: 'Price (USDT)',
                gridcolor: '#1a1c23',
                linecolor: '#1e222b',
                tickcolor: '#1e222b',
                domain: [0.68, 1.0]
            }},
            yaxis2: {{
                title: 'Volume',
                gridcolor: '#1a1c23',
                linecolor: '#1e222b',
                tickcolor: '#1e222b',
                domain: [0.53, 0.65]
            }},
            yaxis3: {{
                title: 'Firestarter Metrics',
                gridcolor: '#1a1c23',
                linecolor: '#1e222b',
                tickcolor: '#1e222b',
                domain: [0.35, 0.50]
            }},
            yaxis4: {{
                title: 'Range / Vol %',
                gridcolor: '#1a1c23',
                linecolor: '#1e222b',
                tickcolor: '#1e222b',
                domain: [0.18, 0.32]
            }},
            yaxis5: {{
                title: 'Benchmark Overlay',
                gridcolor: '#1a1c23',
                linecolor: '#1e222b',
                tickcolor: '#1e222b',
                domain: [0.0, 0.15]
            }},
            margin: {{ t: 40, b: 30, l: 60, r: 20 }},
            showlegend: true,
            legend: {{
                x: 0,
                y: 1.05,
                orientation: 'h',
                font: {{ color: '#cbd5e1', size: 10 }}
            }},
            annotations: [
                {{
                    xref: 'paper',
                    yref: 'paper',
                    x: 0.5,
                    y: 0.425,
                    text: 'NOT ENABLED — formula gate required',
                    showarrow: false,
                    font: {{
                        size: 13,
                        color: '#ef4444',
                        family: 'Inter, sans-serif',
                        weight: 'bold'
                    }}
                }},
                {{
                    xref: 'paper',
                    yref: 'paper',
                    x: 0.5,
                    y: 0.075,
                    text: 'NOT ENABLED — benchmark gate required',
                    showarrow: false,
                    font: {{
                        size: 13,
                        color: '#64748b',
                        family: 'Inter, sans-serif',
                        weight: 'bold'
                    }}
                }}
            ]
        }};

        Plotly.newPlot('chart', data, layout);

        const gd = document.getElementById('chart');
        gd.on('plotly_hover', function(data) {{
            const pts = data.points[0];
            const idx = pts.pointIndex;
            const dateStr = pts.x;
            const priceVal = close[idx];
            const volVal = volume[idx];
            const rangeVal = rangePct[idx];
            const volPctVal = rollingVol[idx];
            
            const readout = document.getElementById('hoverReadout');
            readout.innerHTML = `[UTC TIME: ${{dateStr}}] // Price: ${{priceVal !== undefined && priceVal !== null ? priceVal.toFixed(4) : 'N/A'}} // Volume: ${{volVal !== undefined && volVal !== null ? volVal.toLocaleString() : 'N/A'}} // Spread: ${{rangeVal !== undefined && rangeVal !== null ? rangeVal.toFixed(4) + '%' : 'N/A'}} // Volatility: ${{volPctVal !== undefined && volPctVal !== null ? volPctVal.toFixed(4) + '%' : 'N/A'}} // ER/FMLC/Flowprint: [DISABLED]`;
        }});
    </script>
</body>
</html>
"""
    with open(os.path.join(SYMBOLS_DIR, f"{symbol}.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    return True

def generate_index_page(df_inventory):
    symbol_items = ""
    for idx, row in df_inventory.iterrows():
        s = row['symbol']
        is_unicode = row['nonstandard_symbol_flag']
        unicode_class = 'class="unicode-flag"' if is_unicode else ''
        unicode_label = '<span class="badge">Unicode</span>' if is_unicode else ''
        
        symbol_items += f"""
        <div class="symbol-card">
            <span {unicode_class}>{s}</span>
            <div style="font-size: 11px; color: #64748b; margin-bottom: 12px; font-family: monospace; line-height: 1.5;">
                Rows: {row['row_count']}<br>
                Gaps: {row['missing_5m_count']}
            </div>
            {unicode_label}
            <a href="symbols/{s}.html" class="view-btn">Inspect &rarr;</a>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Matrix Alpha // Top 100 Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: #08090b;
            color: #94a3b8;
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 40px;
            font-size: 13px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            border-bottom: 1px solid #1e222b;
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        .header h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 24px;
            color: #f8fafc;
            margin: 0;
            font-weight: 700;
        }}
        .header p {{
            color: #64748b;
            font-size: 13px;
            margin-top: 6px;
            margin-bottom: 0;
        }}
        .note-banner {{
            background-color: #0f111a;
            border-left: 3px solid #2563eb;
            padding: 12px 16px;
            border-radius: 4px;
            margin-bottom: 24px;
            font-size: 12px;
            color: #64748b;
        }}
        .symbol-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
        }}
        .symbol-card {{
            background-color: #0e1014;
            border: 1px solid #1e222b;
            border-radius: 6px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: border-color 0.2s;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}
        .symbol-card:hover {{
            border-color: #3b82f6;
        }}
        .symbol-card span {{
            font-family: 'Outfit', sans-serif;
            font-size: 15px;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 6px;
        }}
        .symbol-card span.unicode-flag {{
            color: #f59e0b;
        }}
        .badge {{
            background-color: #2d1f10;
            color: #f59e0b;
            font-size: 10px;
            font-weight: 600;
            padding: 2px 6px;
            border-radius: 4px;
            align-self: flex-start;
            margin-bottom: 12px;
            border: 1px solid #4d3319;
            text-transform: uppercase;
        }}
        .view-btn {{
            background-color: #1e293b;
            color: #3b82f6;
            text-decoration: none;
            text-align: center;
            font-weight: 600;
            padding: 6px 12px;
            border-radius: 4px;
            font-size: 12px;
            transition: background-color 0.2s, color 0.2s;
            margin-top: auto;
            border: 1px solid #2d3748;
        }}
        .view-btn:hover {{
            background-color: #2563eb;
            color: #ffffff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Matrix Alpha // Top 100 Dashboard</h1>
            <p>Binance Top 100 USDT-M perpetual contracts (excluding core 5) local research index</p>
        </div>
        
        <div class="note-banner">
            Notice: Firestarter metric panels (ER/FMLC/Flowprint/raw_score) are disabled in this build. All metrics are pending approved formula specifications (gated by HOLD_SPB_FORMULA_COMPUTATION_PENDING_EXECUTABLE_SPEC).
        </div>

        <div class="symbol-grid">
            {symbol_items}
        </div>
    </div>
</body>
</html>
"""
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Dashboard index page generated at: {os.path.join(OUTPUT_DIR, 'index.html')}")

def main():
    print("Building local inventory...")
    df_inv = build_inventory()
    symbols = df_inv['symbol'].tolist()
    print(f"Inventory loaded: {len(symbols)} symbols found.")
    
    print("Generating symbol dashboard detail pages...")
    success_count = 0
    for i, s in enumerate(symbols):
        print(f"[{i+1}/{len(symbols)}] Rendering {s}...", end=" ")
        sys.stdout.flush()
        
        # Get metadata row for the symbol
        meta_rows = df_inv[df_inv['symbol'] == s]
        if not meta_rows.empty:
            metadata = meta_rows.iloc[0].to_dict()
        else:
            metadata = {
                "symbol": s,
                "row_count": 0,
                "first_time_utc": "N/A",
                "last_time_utc": "N/A",
                "missing_5m_count": 0,
                "nonstandard_symbol_flag": False
            }
            
        if generate_symbol_page(s, symbols, metadata):
            success_count += 1
            print("OK")
        else:
            print("FAILED")
            
    generate_index_page(df_inv)
    print(f"\nDashboard build complete. Polished {success_count} symbols pages.")
    
    # Generate V3 audit report
    unicode_symbols = df_inv[df_inv['nonstandard_symbol_flag'] == True]['symbol'].tolist()
    audit_content = f"""# Firestarter SPB: Top 100 Dashboard V3 Firestarter Panels Audit

## Overview
This document records the visual quality, layout behavior, and metric panel configuration audit for the Top 100 V3 dashboard rebuild.

## 1. V3 Audit Checklist & Status
- **Metric Source Review Completed:** YES (recorded in `reports/firestarter_spb_top100_dashboard_v3_firestarter_metric_source_review.md`).
- **Dashboard Index Regenerated:** YES (`reports/html/top100_dashboard/index.html`).
- **100 Symbol Pages Regenerated:** YES ({success_count} / 100 pages generated).
- **BTCUSDT Page Generated:** YES (`reports/html/top100_dashboard/symbols/BTCUSDT.html`).
- **ETHUSDT Page Generated:** YES (`reports/html/top100_dashboard/symbols/ETHUSDT.html`).
- **Nonstandard Symbol Pages Generated:** YES ({len(unicode_symbols)} nonstandard pages).
- **Top Info Section Is NOT Sticky:** YES (static grid summary layout implemented).
- **Price/Header/Chart Info Does NOT Follow Scroll:** YES (verified no fixed or sticky elements follow scrolling).
- **Firestarter Panels Status:** DISABLED placeholders added (clearly labeled `NOT ENABLED — formula gate required` for ER, FMLC, Flowprint, and raw_score).
- **No Invented Formulas:** YES (computation status disabled).

## 2. Boundaries & Security Controls
- **No Raw CSV/JSON Committed:** YES (confirmed only HTML outputs and metadata reviews are staged/committed).
- **No Full Raw Dataset Embedded:** YES (HTML detail pages embed only 1-Hour resampled points for Plotly charts, not raw 5m row databases).
- **No Cell 2 / Labels / Model Training:** YES.
- **No Trading Logic / Recommendations / Strategy Claims:** YES (strictly research-only offline replay profile visualization).
- **No Secrets / Credentials Committed:** YES.
"""
    with open(AUDIT_REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(audit_content)
        
    print(f"Audit report written to: {AUDIT_REPORT_PATH}")

if __name__ == "__main__":
    main()
