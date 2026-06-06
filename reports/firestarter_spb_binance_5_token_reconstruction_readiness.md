# Firestarter SPB Binance 5 Token Reconstruction Readiness

Run basis: `reports/firestarter_spb_binance_5_token_1month_pull_audit.md` and `reports/firestarter_spb_binance_5_token_1month_manifest.csv`

Dataset folder: `data/research/binance_5_token_1month/`

Window UTC: 2026-05-06T00:00:00Z to 2026-06-06T00:00:00Z, end exclusive

Symbols: SOLUSDT, XRPUSDT, DOGEUSDT, LINKUSDT, AVAXUSDT

Boundary check: this report contains dataset-readiness assessment only. It does not create trade signals, Cell 2 labels, recommendation language, performance claims, or external raw-data publication.

## Decision

Recommendation for formula reconstruction: PASS with partial OI/top-trader warning.

Pass condition:

PASS_SPB_RECONSTRUCTION_READY_WITH_PARTIAL_OI_WARNING

The dataset is ready to reconstruct candle-complete research fields and partial-window flow/participation fields. It should not be treated as a full-window OI/top-trader history because Binance returned those public futures-data endpoints only for a retained latest-30-day window.

## Integrity Summary

| Check | Result |
|---|---|
| Dataset files | 50 files present |
| Total manifest rows | 18,665 |
| 1H candle continuity | Complete for all five symbols |
| 4H candle continuity | Complete for all five symbols |
| Funding alignment | Complete 8H sequence for all five symbols; timestamps are offset by 9-10 ms from exact 8H boundaries and should be normalized with tolerance |
| OI statistics | Partial window: 1H starts 2026-05-06T21:00:00Z; 4H starts 2026-05-07T00:00:00Z |
| Top-trader account ratio | Partial window with same gap as OI statistics |
| Top-trader position ratio | Partial window with same gap as OI statistics |
| Current OI snapshot | Present for all five symbols; snapshot time is after the research window and should be treated as current metadata, not historical window data |
| Duplicate timestamps | 0 across manifest |
| Unavailable fields | 0 after retry capture |

## Row Counts By File

| File | Rows | First UTC | Last UTC | Missing | Duplicates | Status |
|---|---:|---|---|---:|---:|---|
| SOLUSDT_futures_klines_1h.csv | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 0 | 0 | ok |
| SOLUSDT_futures_klines_4h.csv | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 0 | 0 | ok |
| SOLUSDT_funding_rate_history.csv | 93 | 2026-05-06T00:00:00.010000Z | 2026-06-05T16:00:00.009000Z | 0 | 0 | ok |
| SOLUSDT_open_interest_statistics_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| SOLUSDT_open_interest_statistics_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| SOLUSDT_top_trader_account_ratio_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| SOLUSDT_top_trader_account_ratio_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| SOLUSDT_top_trader_position_ratio_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| SOLUSDT_top_trader_position_ratio_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| SOLUSDT_open_interest_snapshot.csv | 1 | 2026-06-06T20:56:20.924000Z | 2026-06-06T20:56:20.924000Z | n/a | 0 | ok |
| XRPUSDT_futures_klines_1h.csv | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 0 | 0 | ok |
| XRPUSDT_futures_klines_4h.csv | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 0 | 0 | ok |
| XRPUSDT_funding_rate_history.csv | 93 | 2026-05-06T00:00:00.010000Z | 2026-06-05T16:00:00.009000Z | 0 | 0 | ok |
| XRPUSDT_open_interest_statistics_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| XRPUSDT_open_interest_statistics_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| XRPUSDT_top_trader_account_ratio_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| XRPUSDT_top_trader_account_ratio_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| XRPUSDT_top_trader_position_ratio_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| XRPUSDT_top_trader_position_ratio_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| XRPUSDT_open_interest_snapshot.csv | 1 | 2026-06-06T20:56:24.846000Z | 2026-06-06T20:56:24.846000Z | n/a | 0 | ok |
| DOGEUSDT_futures_klines_1h.csv | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 0 | 0 | ok |
| DOGEUSDT_futures_klines_4h.csv | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 0 | 0 | ok |
| DOGEUSDT_funding_rate_history.csv | 93 | 2026-05-06T00:00:00.010000Z | 2026-06-05T16:00:00.009000Z | 0 | 0 | ok |
| DOGEUSDT_open_interest_statistics_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| DOGEUSDT_open_interest_statistics_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| DOGEUSDT_top_trader_account_ratio_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| DOGEUSDT_top_trader_account_ratio_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| DOGEUSDT_top_trader_position_ratio_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| DOGEUSDT_top_trader_position_ratio_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| DOGEUSDT_open_interest_snapshot.csv | 1 | 2026-06-06T20:56:24.907000Z | 2026-06-06T20:56:24.907000Z | n/a | 0 | ok |
| LINKUSDT_futures_klines_1h.csv | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 0 | 0 | ok |
| LINKUSDT_futures_klines_4h.csv | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 0 | 0 | ok |
| LINKUSDT_funding_rate_history.csv | 93 | 2026-05-06T00:00:00.010000Z | 2026-06-05T16:00:00.009000Z | 0 | 0 | ok |
| LINKUSDT_open_interest_statistics_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| LINKUSDT_open_interest_statistics_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| LINKUSDT_top_trader_account_ratio_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| LINKUSDT_top_trader_account_ratio_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| LINKUSDT_top_trader_position_ratio_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| LINKUSDT_top_trader_position_ratio_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| LINKUSDT_open_interest_snapshot.csv | 1 | 2026-06-06T20:56:24.906000Z | 2026-06-06T20:56:24.906000Z | n/a | 0 | ok |
| AVAXUSDT_futures_klines_1h.csv | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 0 | 0 | ok |
| AVAXUSDT_futures_klines_4h.csv | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 0 | 0 | ok |
| AVAXUSDT_funding_rate_history.csv | 93 | 2026-05-06T00:00:00.010000Z | 2026-06-05T16:00:00.009000Z | 0 | 0 | ok |
| AVAXUSDT_open_interest_statistics_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| AVAXUSDT_open_interest_statistics_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| AVAXUSDT_top_trader_account_ratio_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| AVAXUSDT_top_trader_account_ratio_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| AVAXUSDT_top_trader_position_ratio_1h.csv | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 | partial |
| AVAXUSDT_top_trader_position_ratio_4h.csv | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 | partial |
| AVAXUSDT_open_interest_snapshot.csv | 1 | 2026-06-06T20:56:28.367000Z | 2026-06-06T20:56:28.367000Z | n/a | 0 | ok |

## Continuity And Alignment

1H candles are continuous for all five symbols from 2026-05-06T00:00:00Z through 2026-06-05T23:00:00Z. Each symbol has 744 rows, matching 31 days times 24 hourly bars.

4H candles are continuous for all five symbols from 2026-05-06T00:00:00Z through 2026-06-05T20:00:00Z. Each symbol has 186 rows, matching 31 days times 6 four-hour bars.

Funding history has 93 rows per symbol, matching 31 days times 3 eight-hour funding observations. Funding timestamps are recorded at the expected 8H cadence but are offset by 9-10 ms from exact boundary times. Reconstruction should align funding by nearest 8H boundary or floor/round with a small millisecond tolerance.

OI statistics, top-trader account ratio, and top-trader position ratio are internally continuous within the retained partial window. They are not complete for the full requested 31-day window:

| Dataset family | 1H retained window | 1H missing | 4H retained window | 4H missing |
|---|---|---:|---|---:|
| Open-interest statistics | 2026-05-06T21:00:00Z to 2026-06-05T23:00:00Z | 21 | 2026-05-07T00:00:00Z to 2026-06-05T20:00:00Z | 6 |
| Top-trader account ratio | 2026-05-06T21:00:00Z to 2026-06-05T23:00:00Z | 21 | 2026-05-07T00:00:00Z to 2026-06-05T20:00:00Z | 6 |
| Top-trader position ratio | 2026-05-06T21:00:00Z to 2026-06-05T23:00:00Z | 21 | 2026-05-07T00:00:00Z to 2026-06-05T20:00:00Z | 6 |

## Field Support

Formula definitions were not included with the inputs, so this readiness pass maps available raw columns to reconstruction support. It does not define final formulas or labels.

### ER Support

ER can be supported over the full requested window if it is candle-derived.

Available full-window candle fields:

- `open_time`, `open_time_utc`, `open`, `high`, `low`, `close`, `volume`
- `quote_asset_volume`, `number_of_trades`
- `taker_buy_base_asset_volume`, `taker_buy_quote_asset_volume`
- 1H and 4H candle grids with no missing rows or duplicate timestamps

Readiness: full-window ready for candle-only ER reconstruction on both 1H and 4H.

Constraint: any ER variant requiring OI/top-trader history must start at the partial-window boundary or handle the initial gap explicitly.

### FMLC Support

FMLC can be supported as a partial-window reconstruction if it depends on leverage/participation/positioning proxies from funding, OI, and top-trader ratios.

Available fields:

- Funding: `fundingTime`, `fundingTime_utc`, `fundingRate`, `markPrice`
- OI statistics: `timestamp`, `timestamp_utc`, `sumOpenInterest`, `sumOpenInterestValue`, `CMCCirculatingSupply`, `symbol`
- Top-trader account ratio: `timestamp`, `timestamp_utc`, `longAccount`, `shortAccount`, `longShortRatio`, `symbol`
- Top-trader position ratio: `timestamp`, `timestamp_utc`, `longAccount`, `shortAccount`, `longShortRatio`, `symbol`
- Current OI snapshot: `symbol`, `openInterest`, `time`, `time_utc`

Readiness: partial-window ready for FMLC reconstruction from 2026-05-06T21:00:00Z on 1H and 2026-05-07T00:00:00Z on 4H.

Constraint: not full-window ready for OI/top-trader-dependent FMLC without an explicit missing-window policy.

### Flowprint Proxy Support

Flowprint-proxy reconstruction can be supported by synchronized candle flow fields plus partial-window OI/top-trader context.

Available full-window candle-flow fields:

- `volume`
- `quote_asset_volume`
- `number_of_trades`
- `taker_buy_base_asset_volume`
- `taker_buy_quote_asset_volume`
- OHLC price fields for candle range and direction-free market-state reconstruction

Available partial-window context fields:

- `sumOpenInterest`
- `sumOpenInterestValue`
- `longAccount`, `shortAccount`, `longShortRatio`

Readiness: full-window ready for candle-only Flowprint proxy components; partial-window ready for OI/top-trader-enhanced Flowprint proxy components.

Constraint: any joined Flowprint proxy using OI/top-trader fields must either begin at 2026-05-06T21:00:00Z for 1H / 2026-05-07T00:00:00Z for 4H, or mark early-window OI/top-trader values missing.

## Missing Or Partial Fields

| Field group | Status | Reconstruction handling |
|---|---|---|
| 1H candles | Complete | Usable across full window |
| 4H candles | Complete | Usable across full window |
| Funding history | Complete cadence with millisecond timestamp offset | Normalize to 8H grid with tolerance |
| OI statistics 1H | Partial | First 21 hourly rows unavailable |
| OI statistics 4H | Partial | First 6 four-hour rows unavailable |
| Top-trader account ratio 1H | Partial | First 21 hourly rows unavailable |
| Top-trader account ratio 4H | Partial | First 6 four-hour rows unavailable |
| Top-trader position ratio 1H | Partial | First 21 hourly rows unavailable |
| Top-trader position ratio 4H | Partial | First 6 four-hour rows unavailable |
| Current OI snapshot | Present but outside requested historical window | Use only as current reference metadata |
| Raw field availability | No unavailable fields reported in manifest | No field-level hold required |

## Reconstruction Recommendation

PASS for formula reconstruction with a mandatory partial OI/top-trader warning.

Use the full 2026-05-06T00:00:00Z to 2026-06-06T00:00:00Z window for candle-derived ER and candle-only Flowprint-proxy components.

Use only the retained partial window for OI/top-trader-dependent FMLC and OI/top-trader-enhanced Flowprint-proxy components unless the reconstruction code explicitly marks the early-window gap as missing.

Do not use the current OI snapshot as historical data inside the one-month study window.

