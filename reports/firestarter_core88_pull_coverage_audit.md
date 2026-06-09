# Firestarter Core 88 Pull Coverage Audit

## Scope

Audit the path from `configs/firestarter_core88_binance_usdt_symbols.txt` through local OHLCV availability, derivatives context availability, and the current evidence viewer wiring.

## Summary

| Check | Result | Notes |
|---|---|---|
| Config symbol count | **88** | 88 unique symbols in the Core 88 config. |
| Viewer symbol count | **100** | The current `reports/html/top100_evidence_viewer/index.html` embeds 100 symbols. |
| OHLCV coverage count | **82** | 37 Core 88 symbols are present in the current Top100 OHLCV set, and 45 more are present in the Core88 missing OHLCV set. |
| Derivatives coverage count | **82** | 82 Core 88 symbols have at least one local derivatives context file across the two derivatives directories. |
| Missing OHLCV symbols | **6** | `PEPEUSDT`, `BONKUSDT`, `FLOKIUSDT`, `MKRUSDT`, `AIUSDT`, `OMUSDT` |
| Missing derivatives symbols | **6** | `PEPEUSDT`, `BONKUSDT`, `FLOKIUSDT`, `MKRUSDT`, `AIUSDT`, `OMUSDT` |
| Invalid Binance route symbols | **6 flagged** | The existing Core88 pull audit marked these six as `skipped_inactive` / `symbol_not_active_usdt_perpetual`. |
| Viewer uses Core88 | **NO** | `scripts/visualization/build_top100_evidence_viewer.py` still hardcodes the Top100 data paths and the HTML title still says Top 100. |
| Final decision | **HOLD_CORE88_PULL_COVERAGE_INCOMPLETE** | Coverage is incomplete and the current viewer is still stale Top100. |

## Config

- Config file: `configs/firestarter_core88_binance_usdt_symbols.txt`
- Unique symbols: 88

## Local OHLCV Coverage

The Core 88 symbols split across the local OHLCV folders as follows:

- Symbols present in `C:\firestarterspb\data\research\binance_top100_excluding_existing_5_1month`: 37
- Symbols present in `C:\firestarterspb\data\research\binance_core88_missing_1month`: 45
- Symbols missing from both local OHLCV locations: 6

Missing OHLCV symbols:

- `PEPEUSDT`
- `BONKUSDT`
- `FLOKIUSDT`
- `MKRUSDT`
- `AIUSDT`
- `OMUSDT`

## Local Derivatives Coverage

Local derivatives context files exist for 82 of the 88 Core 88 symbols across:

- `C:\firestarterspb\data\research\binance_top100_derivatives_context_1month`
- `C:\firestarterspb\data\research\binance_core88_missing_derivatives_context_1month`

Missing derivatives symbols:

- `PEPEUSDT`
- `BONKUSDT`
- `FLOKIUSDT`
- `MKRUSDT`
- `AIUSDT`
- `OMUSDT`

## Viewer Audit

The current viewer under review is `reports/html/top100_evidence_viewer/index.html`.

- Viewer embedded symbol count: 100
- Core 88 symbols actually loaded into that viewer: 37
- Core 88 symbols excluded from that viewer: 51

Loaded Core 88 symbols:

`BTCUSDT`, `ETHUSDT`, `BNBUSDT`, `SUIUSDT`, `ADAUSDT`, `HYPEUSDT`, `RENDERUSDT`, `VVVUSDT`, `WLDUSDT`, `NEARUSDT`, `APTUSDT`, `ARBUSDT`, `OPUSDT`, `SEIUSDT`, `TIAUSDT`, `INJUSDT`, `ONDOUSDT`, `ENAUSDT`, `AAVEUSDT`, `UNIUSDT`, `CRVUSDT`, `FETUSDT`, `TAOUSDT`, `FILUSDT`, `ICPUSDT`, `ALGOUSDT`, `WIFUSDT`, `ZECUSDT`, `LTCUSDT`, `BCHUSDT`, `ETCUSDT`, `XLMUSDT`, `HBARUSDT`, `TRXUSDT`, `DOTUSDT`, `CHZUSDT`, `DASHUSDT`

Excluded Core 88 symbols:

`SOLUSDT`, `XRPUSDT`, `DOGEUSDT`, `LINKUSDT`, `AVAXUSDT`, `JUPUSDT`, `PYTHUSDT`, `PENDLEUSDT`, `LDOUSDT`, `ATOMUSDT`, `GALAUSDT`, `SANDUSDT`, `MANAUSDT`, `PEPEUSDT`, `BONKUSDT`, `FLOKIUSDT`, `ORDIUSDT`, `1000SATSUSDT`, `RUNEUSDT`, `DYDXUSDT`, `MKRUSDT`, `TRBUSDT`, `VETUSDT`, `ACEUSDT`, `AIUSDT`, `ARKMUSDT`, `ARKUSDT`, `AXSUSDT`, `BLURUSDT`, `COMPUSDT`, `COTIUSDT`, `EGLDUSDT`, `ENSUSDT`, `GMTUSDT`, `GMXUSDT`, `HIGHUSDT`, `IMXUSDT`, `KAVAUSDT`, `KSMUSDT`, `MASKUSDT`, `MINAUSDT`, `NOTUSDT`, `OMUSDT`, `QTUMUSDT`, `ROSEUSDT`, `SNXUSDT`, `STXUSDT`, `SUSHIUSDT`, `WOOUSDT`, `XAIUSDT`, `YFIUSDT`

## Evidence

- `scripts/visualization/build_top100_evidence_viewer.py` still uses:
  - `C:/firestarterspb/data/research/binance_top100_excluding_existing_5_1month`
  - `C:/firestarterspb/data/research/binance_top100_derivatives_context_1month`
  - `reports/html/top100_evidence_viewer/index.html`
- The HTML title is still `Top 100 Evidence Viewer`.
- A separate Core88 viewer builder exists, but it is not the viewer path named in this audit.
- The existing Core88 pull audit already flagged the six missing symbols as inactive on the Binance USDT perpetual route:
  - `PEPEUSDT`
  - `BONKUSDT`
  - `FLOKIUSDT`
  - `MKRUSDT`
  - `AIUSDT`
  - `OMUSDT`

## Decision

**HOLD_CORE88_PULL_COVERAGE_INCOMPLETE**

The Core 88 config is present, but the current Evidence Viewer is still Top100-based and only 37 of the 88 Core 88 symbols are actually loaded there. Six Core 88 symbols are still missing from local OHLCV and derivatives coverage, and those six have already been flagged inactive/unavailable by the existing pull audit.
