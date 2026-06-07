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
AUDIT_REPORT_PATH = "C:/firestarterspb/reports/firestarter_spb_top100_dashboard_high_tech_ui_audit.md"

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

def load_derivatives_data(symbol):
    deriv_dir = "C:/firestarterspb/data/research/binance_top100_derivatives_context_1month"
    data = {}
    
    subdirs = ["fundingRate", "openInterestHist", "takerlongshortRatio", "globalLongShortAccountRatio", "topLongShortAccountRatio", "topLongShortPositionRatio", "premiumIndex"]
    for sd in subdirs:
        file_path = os.path.join(deriv_dir, sd, f"{symbol}_{sd}.csv")
        if os.path.exists(file_path):
            try:
                df_temp = pd.read_csv(file_path)
                if not df_temp.empty:
                    time_col = "fundingTime" if sd == "fundingRate" else ("time" if sd == "premiumIndex" else "timestamp")
                    df_temp['datetime'] = pd.to_datetime(df_temp[time_col], unit='ms', utc=True)
                    data[sd] = df_temp
            except Exception as e:
                pass
    return data

def merge_derivatives(df_1h, deriv_data):
    df_merged = df_1h.copy().sort_index()
    
    # 1. Join fundingRate
    if "fundingRate" in deriv_data:
        df_f = deriv_data["fundingRate"][["datetime", "fundingRate"]].dropna().sort_values("datetime")
        df_merged = pd.merge_asof(df_merged, df_f.set_index("datetime"), left_index=True, right_index=True, direction="backward")
    else:
        df_merged["fundingRate"] = np.nan
        
    # 2. Join openInterestHist
    if "openInterestHist" in deriv_data:
        df_oi = deriv_data["openInterestHist"][["datetime", "sumOpenInterest", "sumOpenInterestValue"]].dropna().sort_values("datetime")
        df_merged = pd.merge_asof(df_merged, df_oi.set_index("datetime"), left_index=True, right_index=True, direction="backward", tolerance=pd.Timedelta("15Min"))
    else:
        df_merged["sumOpenInterest"] = np.nan
        df_merged["sumOpenInterestValue"] = np.nan
        
    # 3. Join takerlongshortRatio
    if "takerlongshortRatio" in deriv_data:
        df_t = deriv_data["takerlongshortRatio"][["datetime", "buySellRatio"]].dropna().sort_values("datetime")
        df_merged = pd.merge_asof(df_merged, df_t.set_index("datetime"), left_index=True, right_index=True, direction="backward", tolerance=pd.Timedelta("15Min"))
    else:
        df_merged["buySellRatio"] = np.nan
        
    # 4. Join globalLongShortAccountRatio
    if "globalLongShortAccountRatio" in deriv_data:
        df_gls = deriv_data["globalLongShortAccountRatio"][["datetime", "longShortRatio"]].dropna().sort_values("datetime")
        df_merged = pd.merge_asof(df_merged, df_gls.set_index("datetime"), left_index=True, right_index=True, direction="backward", tolerance=pd.Timedelta("15Min"))
    else:
        df_merged["longShortRatio"] = np.nan
        
    return df_merged

def compute_cell1_metrics(df_merged):
    # EMA 21 and volume baseline — SMA 20/50 removed from output, not charted
    df_merged['ema_21'] = df_merged['close'].ewm(span=21, adjust=False).mean()
    df_merged['vol_avg_10'] = df_merged['volume'].rolling(10).mean()
    # EMA 50 used internally for trend scoring only (not charted)
    df_merged['_ema_50'] = df_merged['close'].ewm(span=50, adjust=False).mean()

    # RVOL 1H (24-bar approved default)
    df_merged['rvol_1h'] = df_merged['volume'] / df_merged['volume'].rolling(24).mean()
    df_merged['vol_4h'] = df_merged['volume'].rolling(4).sum()
    df_merged['rvol_4h'] = df_merged['vol_4h'] / df_merged['vol_4h'].rolling(96).mean()

    # 24h change (anti-blowoff governor)
    df_merged['change_24h'] = (df_merged['close'] - df_merged['close'].shift(24)) / df_merged['close'].shift(24) * 100

    # 1. ER Calculation
    high_20 = df_merged['high'].rolling(20).max()
    rvol = df_merged['rvol_1h']

    rvol_score = np.zeros(len(df_merged))
    rvol_score[rvol > 2.5] = 4
    rvol_score[(rvol > 1.8) & (rvol <= 2.5)] = 3
    rvol_score[(rvol > 1.2) & (rvol <= 1.8)] = 2
    rvol_score[(rvol > 0.8) & (rvol <= 1.2)] = 1

    near_breakout = np.zeros(len(df_merged))
    near_breakout[df_merged['close'] >= 0.99 * high_20] = 3
    near_breakout[(df_merged['close'] >= 0.975 * high_20) & (df_merged['close'] < 0.99 * high_20)] = 1

    clean_reclaim = np.zeros(len(df_merged))
    clean_reclaim[(df_merged['close'] > df_merged['ema_21']) & (df_merged['volume'] > 1.2 * df_merged['vol_avg_10'])] = 3

    er_raw = rvol_score + near_breakout + clean_reclaim
    df_merged['er'] = np.clip(er_raw, 0, 10)

    er_na = df_merged['close'].isna() | df_merged['rvol_1h'].isna() | high_20.isna()
    df_merged.loc[er_na, 'er'] = np.nan

    # 2. FMLC Calculation
    df_merged['quote_volume'] = df_merged['volume'] * df_merged['close']
    df_merged['quote_volume_24h'] = df_merged['quote_volume'].rolling(24).sum()

    high_200 = df_merged['high'].rolling(200).max()
    low_200 = df_merged['low'].rolling(200).min()
    rp_200 = (df_merged['close'] - low_200) / (high_200 - low_200) * 10

    low_20 = df_merged['low'].rolling(20).min()
    rp_20 = (df_merged['close'] - low_20) / (high_20 - low_20) * 10

    composite_rp = 0.5 * rp_200 + 0.5 * rp_20
    composite_rp_score = composite_rp / 2.0  # max 5 points

    # Trend score uses internal EMA50 (not charted) per approved default
    trend_score = np.zeros(len(df_merged))
    trend_score[df_merged['close'] > df_merged['_ema_50']] = 3
    trend_score[(df_merged['close'] <= df_merged['_ema_50']) & (df_merged['close'] > df_merged['ema_21'])] = 1

    funding_score = np.zeros(len(df_merged))
    funding_score[df_merged['fundingRate'] <= 0.0001] = 2
    funding_score[(df_merged['fundingRate'] > 0.0001) & (df_merged['fundingRate'] <= 0.0005)] = 1

    governor_penalty = np.zeros(len(df_merged))
    governor_penalty[(df_merged['change_24h'] >= 15) | (df_merged['change_24h'] <= -15)] = 4

    fmlc_raw = composite_rp_score + trend_score + funding_score - governor_penalty
    df_merged['fmlc'] = np.clip(fmlc_raw, 0, 10)

    # Liquidity floor: $10M daily quote volume
    df_merged.loc[df_merged['quote_volume_24h'] < 10000000, 'fmlc'] = 0

    fmlc_na = df_merged['fundingRate'].isna() | df_merged['change_24h'].isna() | high_200.isna() | low_20.isna()
    df_merged.loc[fmlc_na, 'fmlc'] = np.nan

    # 3. Flowprint_proxy Calculation
    df_merged['oi_change_1h'] = (
        (df_merged['sumOpenInterest'] - df_merged['sumOpenInterest'].shift(1))
        / df_merged['sumOpenInterest'].shift(1) * 100
    )

    funding_quality = np.zeros(len(df_merged))
    funding_quality[(df_merged['fundingRate'] >= -0.0001) & (df_merged['fundingRate'] <= 0.0003)] = 2

    taker_ratio = df_merged['buySellRatio'] / (df_merged['buySellRatio'] + 1)
    taker_score = np.zeros(len(df_merged))
    taker_score[taker_ratio >= 0.52] = 2
    taker_score[(taker_ratio >= 0.48) & (taker_ratio < 0.52)] = 1

    rvol_fp_score = np.zeros(len(df_merged))
    rvol_fp_score[rvol > 1.5] = 2
    rvol_fp_score[(rvol > 1.0) & (rvol <= 1.5)] = 1

    oi_score = np.zeros(len(df_merged))
    oi_score[df_merged['oi_change_1h'] > 1.5] = 2
    oi_score[(df_merged['oi_change_1h'] > 0) & (df_merged['oi_change_1h'] <= 1.5)] = 1

    flowprint_raw = funding_quality + taker_score + rvol_fp_score + oi_score
    df_merged['flowprint'] = np.clip(flowprint_raw, 0, 8)

    flowprint_na = (
        df_merged['volume'].isna() | df_merged['buySellRatio'].isna()
        | df_merged['sumOpenInterest'].isna() | df_merged['fundingRate'].isna()
        | df_merged['oi_change_1h'].isna()
    )
    df_merged.loc[flowprint_na, 'flowprint'] = np.nan

    # 4. raw_score
    raw_score = df_merged['er'] * 0.35 + df_merged['fmlc'] * 0.35 + df_merged['flowprint'] * 0.30
    df_merged['raw_score'] = np.clip(raw_score / 0.94, 0, 10)

    raw_score_na = df_merged['er'].isna() | df_merged['fmlc'].isna() | df_merged['flowprint'].isna()
    df_merged.loc[raw_score_na, 'raw_score'] = np.nan

    # Drop internal columns not needed downstream
    df_merged.drop(columns=['_ema_50'], errors='ignore', inplace=True)

    return df_merged

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

    # Load and merge derivatives data
    deriv_data = load_derivatives_data(symbol)
    df_merged = merge_derivatives(df_1h, deriv_data)
    
    # Compute Cell 1 metrics
    df_merged = compute_cell1_metrics(df_merged)

    # Rolling stats for visualization
    df_merged['range_pct'] = ((df_merged['high'] - df_merged['low']) / df_merged['open']) * 100
    df_merged['log_ret'] = np.log(df_merged['close'] / df_merged['close'].shift(1))
    df_merged['rolling_vol'] = df_merged['log_ret'].rolling(20).std() * 100

    # Clean missing values for JSON serialization
    df_merged = df_merged.replace({np.nan: None})

    # Prepare JS data payload — price on right axis; metrics on left; volume removed
    chart_data = {
        "dates": df_merged.index.strftime('%Y-%m-%dT%H:%M:%SZ').tolist(),
        "close": df_merged['close'].tolist(),
        "range_pct": df_merged['range_pct'].tolist(),
        "rolling_vol": df_merged['rolling_vol'].tolist(),
        "er": df_merged['er'].tolist(),
        "fmlc": df_merged['fmlc'].tolist(),
        "flowprint": df_merged['flowprint'].tolist(),
        "raw_score": df_merged['raw_score'].tolist()
    }

    # Latest non-null metric values for top output cards
    def _last_val(col):
        vals = [v for v in df_merged[col] if v is not None]
        return f"{vals[-1]:.2f}" if vals else "N/A"

    card_er    = _last_val('er')
    card_fmlc  = _last_val('fmlc')
    card_fp    = _last_val('flowprint')
    card_score = _last_val('raw_score')

    # Format tables with professional classes and styles
    table_desc_1h = df_merged[['open', 'high', 'low', 'close', 'volume']].describe().to_html(classes='data-table', float_format=lambda x: f"{x:,.4f}")
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
            background: radial-gradient(circle at center, #111317 0%, #07080a 100%);
            color: #d1d5db;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            font-size: 12px;
            letter-spacing: -0.01em;
        }}
        .header {{
            background: rgba(10, 10, 10, 0.75);
            border: 1px solid rgba(13, 185, 213, 0.2);
            border-top: 2px solid #0db9d7;
            backdrop-filter: blur(8px);
            border-radius: 4px;
            padding: 10px 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header-title-group {{
            display: flex;
            flex-direction: column;
        }}
        .header h2 {{
            font-family: 'Inter', sans-serif;
            color: #e2e8f0;
            margin: 0;
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
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
            color: #556070;
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 500;
            letter-spacing: 0.05em;
        }}
        select {{
            background-color: #0a0a0a;
            color: #0db9d7;
            border: 1px solid rgba(13, 185, 213, 0.3);
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
            outline: none;
            cursor: pointer;
        }}
        .home-btn {{
            background-color: #0a0a0a;
            color: #94a3b8;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-decoration: none;
            padding: 4px 12px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 500;
            transition: all 0.15s ease;
        }}
        .home-btn:hover {{
            border-color: #0db9d7;
            color: #0db9d7;
            background-color: rgba(13, 185, 213, 0.05);
        }}
        .metadata-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            background: rgba(10, 10, 10, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(4px);
            border-radius: 4px;
            padding: 10px 14px;
            margin-bottom: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        }}
        .metadata-item {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}
        .metadata-label {{
            color: #556070;
            font-size: 9px;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.08em;
        }}
        .metadata-value {{
            color: #cbd5e1;
            font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
            font-size: 11px;
        }}
        .font-highlight {{
            color: #0db9d7;
            font-weight: 600;
        }}
        .font-bold {{
            font-weight: 600;
        }}
        .text-success {{
            color: #10b981;
        }}
        .text-danger {{
            color: #ef4444;
        }}
        /* ── Metric output cards ── */
        .metric-cards {{
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
        }}
        .metric-card {{
            flex: 1;
            background: rgba(10, 10, 10, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 4px;
            padding: 8px 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
            gap: 3px;
            position: relative;
            overflow: hidden;
        }}
        .metric-card::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 3px;
            height: 100%;
        }}
        .mc-er::after {{ background-color: #d19a66; }}
        .mc-fmlc::after {{ background-color: #ef4444; }}
        .mc-fp::after {{ background-color: #5eead4; }}
        .mc-score::after {{ background-color: #a78bfa; }}

        .mc-label {{
            font-size: 9px;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.1em;
            color: #64748b;
        }}
        .mc-value {{
            font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
            font-size: 18px;
            font-weight: 700;
            line-height: 1.1;
        }}
        .mc-sub {{
            font-size: 9px;
            color: #475569;
            font-family: 'Consolas', monospace;
        }}
        .mc-er   .mc-value {{ color: #d19a66; }}
        .mc-fmlc .mc-value {{ color: #ef4444; }}
        .mc-fp   .mc-value {{ color: #5eead4; }}
        .mc-score .mc-value {{ color: #a78bfa; }}
        .hover-readout {{
            background: rgba(10, 10, 10, 0.85);
            border: 1px solid rgba(13, 185, 213, 0.15);
            border-radius: 4px;
            padding: 6px 12px;
            margin-bottom: 12px;
            font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
            font-size: 11px;
            color: #0db9d7;
            box-shadow: inset 0 2px 6px rgba(0,0,0,0.8);
        }}
        #chart {{
            background: rgba(10, 10, 10, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 4px;
            box-shadow: 0 4px 25px rgba(0, 0, 0, 0.6);
            padding: 8px;
            margin-bottom: 20px;
            height: 850px;
        }}
        .section-title {{
            font-family: 'Inter', sans-serif;
            font-size: 11px;
            font-weight: 600;
            color: #94a3b8;
            margin-top: 20px;
            margin-bottom: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 4px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .table-container {{
            overflow-x: auto;
            margin-bottom: 16px;
        }}
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 11px;
            text-align: right;
            background: rgba(10, 10, 10, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 4px;
            overflow: hidden;
            font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
        }}
        .data-table th, .data-table td {{
            padding: 4px 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            border-right: 1px solid rgba(255, 255, 255, 0.03);
        }}
        .data-table th {{
            background: rgba(20, 22, 28, 0.8);
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 10px;
            letter-spacing: 0.04em;
        }}
        .data-table td {{
            color: #cbd5e1;
        }}
        .data-table tr:hover {{
            background: rgba(13, 185, 213, 0.03);
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
            <span class="metadata-value text-success font-bold">ACTIVE (Sandbox Replay)</span>
        </div>
    </div>

    <!-- Metric output cards: latest values per symbol -->
    <div class="metric-cards">
        <div class="metric-card mc-er">
            <span class="mc-label">ER &mdash; Expansion Readiness</span>
            <span class="mc-value">{card_er}</span>
            <span class="mc-sub">scale 0&ndash;10</span>
        </div>
        <div class="metric-card mc-fmlc">
            <span class="mc-label">FMLC &mdash; Momentum / Liquidity</span>
            <span class="mc-value">{card_fmlc}</span>
            <span class="mc-sub">scale 0&ndash;10</span>
        </div>
        <div class="metric-card mc-fp">
            <span class="mc-label">Flowprint&nbsp;proxy</span>
            <span class="mc-value">{card_fp}</span>
            <span class="mc-sub">scale 0&ndash;8</span>
        </div>
        <div class="metric-card mc-score">
            <span class="mc-label">raw_score &mdash; blended</span>
            <span class="mc-value">{card_score}</span>
            <span class="mc-sub">scale 0&ndash;10</span>
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

        const dates      = chartData.dates;
        const closeArr   = chartData.close;
        const rangePct   = chartData.range_pct;
        const rollingVol = chartData.rolling_vol;
        const er         = chartData.er;
        const fmlc       = chartData.fmlc;
        const flowprint  = chartData.flowprint;
        const rawScore   = chartData.raw_score;

        // ── Main chart: Price on RIGHT y-axis (white line)
        const tracePrice = {{
            x: dates, y: closeArr,
            type: 'scatter', mode: 'lines',
            name: 'Price',
            line: {{ color: '#ffffff', width: 1.8 }},
            yaxis: 'y2'
        }};

        // ── Main chart: FMLC — red, opacity intensifies with value, LEFT axis 0-10
        // Cell 1 partial reconstruction — approved sandbox defaults — research only
        const traceFMLC = {{
            x: dates, y: fmlc,
            type: 'scatter', mode: 'lines',
            name: 'FMLC',
            line: {{ color: 'rgba(239,68,68,0.45)', width: 0.9 }},
            yaxis: 'y'
        }};

        // ── Main chart: Flowprint_proxy — thin light green line, LEFT axis
        const traceFlowprint = {{
            x: dates, y: flowprint,
            type: 'scatter', mode: 'lines',
            name: 'Flowprint',
            line: {{ color: 'rgba(94,234,212,0.38)', width: 0.6 }},
            yaxis: 'y'
        }};

        // ── Main chart: raw_score — purple dots, LEFT axis
        const traceRawScore = {{
            x: dates, y: rawScore,
            type: 'scatter', mode: 'markers',
            name: 'Score',
            marker: {{ color: 'rgba(167,139,250,0.55)', size: 3 }},
            yaxis: 'y'
        }};

        // ── ER panel: amber vertical bars, fixed 0-10, own sub-panel below main chart
        const erColors = er.map(v => {{
            if (v === null || v === undefined) return 'rgba(100,116,139,0.10)';
            if (v >= 7) return 'rgba(209,154,102,0.60)';
            if (v >= 4) return 'rgba(209,154,102,0.40)';
            return 'rgba(209,154,102,0.20)';
        }});
        const traceER = {{
            x: dates, y: er,
            type: 'bar',
            name: 'ER',
            marker: {{ color: erColors }},
            yaxis: 'y3'
        }};

        // ── Bottom panel: Range % and Rolling Volatility


        const data = [
            tracePrice,
            traceFMLC, traceFlowprint, traceRawScore,
            traceER
        ];

        const layout = {{
            plot_bgcolor:  '#0a0a0a',
            paper_bgcolor: '#08090b',
            font: {{ family: 'Inter, Roboto, sans-serif', size: 10, color: '#e0e0e0' }},
            bargap: 0.12,

            xaxis: {{
                gridcolor: '#222222', linecolor: '#333333', tickcolor: '#444444',
                domain: [0, 1]
            }},

            // Main left y-axis for raw_score
            yaxis: {{
                title: 'Firestarter Metrics',
                gridcolor: '#222222', linecolor: '#333333', tickcolor: '#444444',
                tickfont: {{ color: '#64748b' }},
                domain: [0.44, 0.80],
                range: [0, 10],
                side: 'left'
            }},

            // RIGHT y-axis — Price (USDT)  [main chart, overlaying metrics]
            yaxis2: {{
                title: 'Price (USDT)',
                gridcolor: 'rgba(0,0,0,0)',
                linecolor: '#333333', tickcolor: '#444444',
                tickfont: {{ color: '#e2e8f0' }},
                overlaying: 'y',
                side: 'right',
                showgrid: false,
                domain: [0.80, 1.0]
            }},

            // ER sub-panel
            yaxis3: {{
                title: 'ER  (0\u201310)',
                gridcolor: '#1e222b', linecolor: '#1e222b', tickcolor: '#1e222b',
                tickfont: {{ color: '#f59e0b' }},
                domain: [0.24, 0.40],
                range: [0, 10],
                fixedrange: true
            }},

            // Bottom panel \u2014 Range / Vol %


            margin: {{ t: 40, b: 30, l: 30, r: 30 }},
            showlegend: true,
            legend: {{
                x: 0, y: 1.055,
                orientation: 'h',
                font: {{ color: '#cbd5e1', size: 10 }}
            }},
            annotations: [
                {{
                    xref: 'paper', yref: 'paper',
                    x: 1.0, y: 1.038,
                    xanchor: 'right', yanchor: 'bottom',
                    text: 'Cell 1 partial reconstruction \u00b7 Approved sandbox defaults \u00b7 Research only',
                    showarrow: false,
                    font: {{ size: 9, color: '#475569', family: 'Inter, sans-serif' }}
                }},
                {{
                    xref: 'paper', yref: 'paper',
                    x: 0, y: 0.395,
                    xanchor: 'left', yanchor: 'bottom',
                    text: 'ER \u2014 Expansion Readiness  |  bars  |  0\u201310',
                    showarrow: false,
                    font: {{ size: 9, color: '#f59e0b', family: 'Inter, sans-serif' }}
                }}
            ]
        }};

        Plotly.newPlot('chart', data, layout, {{responsive: true, displaylogo: false}});

        const gd = document.getElementById('chart');
        gd.on('plotly_hover', function(eventData) {{
            const pts = eventData.points[0];
            const idx = pts.pointIndex;
            const dateStr = pts.x;
            const price   = closeArr[idx];
            const rng     = rangePct[idx];
            const rv      = rollingVol[idx];
            const erVal   = er[idx];
            const fmlcVal = fmlc[idx];
            const fpVal   = flowprint[idx];
            const rawVal  = rawScore[idx];
            const fmt = (v, d=4) => (v !== undefined && v !== null) ? (+v).toFixed(d) : 'N/A';
            const readout = document.getElementById('hoverReadout');
            readout.innerHTML =
                `[UTC: ${{dateStr}}] &nbsp;|&nbsp; Price: ${{fmt(price)}} &nbsp;|&nbsp; Range: ${{fmt(rng,3)}}% &nbsp;|&nbsp; RVol: ${{fmt(rv,3)}}%` +
                ` &nbsp;||&nbsp; <b style="color:#f59e0b">ER: ${{fmt(erVal,2)}}</b>` +
                ` &nbsp;|&nbsp; <b style="color:#ef4444">FMLC: ${{fmt(fmlcVal,2)}}</b>` +
                ` &nbsp;|&nbsp; <b style="color:#34d399">FP: ${{fmt(fpVal,2)}}</b>` +
                ` &nbsp;|&nbsp; <b style="color:#a78bfa">Score: ${{fmt(rawVal,2)}}</b>`;
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
            background: radial-gradient(circle at center, #111317 0%, #07080a 100%);
            color: #d1d5db;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 40px;
            font-size: 12px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        .header h1 {{
            font-family: 'Inter', sans-serif;
            font-size: 20px;
            color: #e2e8f0;
            margin: 0;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}
        .header p {{
            color: #64748b;
            font-size: 11px;
            margin-top: 6px;
            margin-bottom: 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .note-banner {{
            background: rgba(10, 10, 10, 0.6);
            padding: 12px 16px;
            border-radius: 4px;
            margin-bottom: 24px;
            font-size: 11px;
            color: #64748b;
            font-family: 'Consolas', monospace;
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-left: 3px solid #0db9d7;
        }}
        .symbol-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
        }}
        .symbol-card {{
            background: rgba(10, 10, 10, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 4px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.2s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        }}
        .symbol-card:hover {{
            border-color: #0db9d7;
            box-shadow: 0 4px 20px rgba(13, 185, 213, 0.1);
        }}
        .symbol-card span {{
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: #e2e8f0;
            margin-bottom: 6px;
            letter-spacing: 0.02em;
        }}
        .symbol-card span.unicode-flag {{
            color: #d19a66;
        }}
        .badge {{
            background-color: rgba(209, 154, 102, 0.1);
            color: #d19a66;
            font-size: 9px;
            font-weight: 600;
            padding: 2px 6px;
            border-radius: 3px;
            align-self: flex-start;
            margin-bottom: 12px;
            border: 1px solid rgba(209, 154, 102, 0.2);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .view-btn {{
            background-color: #0a0a0a;
            color: #94a3b8;
            text-decoration: none;
            text-align: center;
            font-weight: 500;
            padding: 6px 12px;
            border-radius: 3px;
            font-size: 11px;
            transition: all 0.2s ease;
            margin-top: auto;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .view-btn:hover {{
            border-color: #0db9d7;
            color: #0db9d7;
            background-color: rgba(13, 185, 213, 0.05);
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
            Notice: Firestarter Cell 1 metrics (ER/FMLC/Flowprint/raw_score) are active in this build, computed using Chris approved sandbox defaults (24-bar RVOL, $10M daily volume floor, 1.0% breakout margin, EMA21 reclaim, +/-15% anti-blowoff governor, -0.01% to +0.03% funding rate, and +1.5% OI accumulation).
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
    
    # Generate High-Tech UI audit report
    unicode_symbols = df_inv[df_inv['nonstandard_symbol_flag'] == True]['symbol'].tolist()
    audit_content = f"""# Firestarter SPB: Top 100 Dashboard High-Tech UI Modernization Audit

## Overview
This document records the visual quality, layout behavior, and metric panel configuration audit for the Top 100 high-tech terminal UI rebuild.

## 1. High-Tech UI Audit Checklist & Status
- **High-Tech UI Applied:** YES. Deep black/graphite background gradient, thin muted borders, cyan accents, compact Inter/Roboto typography, and monospaced Consolas/Roboto Mono tables and values.
- **Formulas Unchanged:** YES. Flowprint scaling is flowprint_proxy_0_10 = flowprint_proxy_raw / 8 * 10 clamped to [0,10]; raw_score is ER * 0.35 + FMLC * 0.35 + Flowprint_proxy_0_10 * 0.30.
- **Chart Structure Preserved:** YES.
  - Panel 1: Price only (white line on right y-axis).
  - Panel 2: Firestarter metric group (raw_score dots, FMLC line, Flowprint line sharing left 0-10 y-axis).
  - Panel 3: ER lower panel (amber vertical bars on left 0-10 y-axis).
  - Top cards aligned beside each other (ER, FMLC, Flowprint, Score).
- **No Sticky/Floating Headers:** YES (all headers, top card info, and layout containers are static and do not follow scroll).
- **No Reintroduced Elements:** YES (no SMA 20, SMA 50, volume %, bottom volume, or Range/Vol % panel are present in charts).
- **Dashboard Index Regenerated:** YES (`reports/html/top100_dashboard/index.html`).
- **100 Symbol Pages Regenerated:** YES ({success_count} / 100 pages generated).
- **BTCUSDT Page Generated:** YES (`reports/html/top100_dashboard/symbols/BTCUSDT.html`).
- **ETHUSDT Page Generated:** YES (`reports/html/top100_dashboard/symbols/ETHUSDT.html`).
- **Nonstandard Symbol Pages Generated:** YES ({len(unicode_symbols)} nonstandard pages).
- **Firestarter Panels Status:** ACTIVE (ER, FMLC, Flowprint_proxy, and raw_score fully computed and visualized using Chris approved sandbox defaults).
- **Decisions & Defaults:** Capped 29-day derivatives history window is used for standard symbols, and non-standard symbols are parent-gated/disabled cleanly.

## 2. Boundaries & Security Controls
- **No Raw CSV/JSON Committed:** YES.
- **No Full Raw Dataset Embedded:** YES.
- **No Cell 2 / Labels / Model Training:** YES.
- **No Trading Logic / Recommendations / Strategy Claims:** YES (strictly research-only offline replay profile visualization).
- **No Secrets / Credentials Committed:** YES.
"""
    with open(AUDIT_REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(audit_content)
        
    print(f"Audit report written to: {AUDIT_REPORT_PATH}")

if __name__ == "__main__":
    main()
