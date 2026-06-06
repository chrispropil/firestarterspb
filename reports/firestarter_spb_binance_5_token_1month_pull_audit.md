# Firestarter SPB Binance 5 Token 1 Month Pull Audit

Run timestamp UTC: 2026-06-06T20:56:39.392108Z
Window UTC: 2026-05-06T00:00:00Z to 2026-06-06T00:00:00Z (end exclusive)
Symbols: SOLUSDT, XRPUSDT, DOGEUSDT, LINKUSDT, AVAXUSDT
Source: Binance public USD-M futures REST API; no API keys used.
Boundaries observed: no trading logic, no signal labels, no Cell 2, no paid data, no external raw-data publishing.

## Summary

- Output directory: `data\research\binance_5_token_1month`
- Manifest: `reports\firestarter_spb_binance_5_token_1month_manifest.csv`
- Dataset files: 50
- Total rows: 18665
- Missing-row audit exceptions: 30
- Duplicate timestamp exceptions: 0
- Unavailable-field exceptions: 0

## Dataset Audit

| Symbol | Dataset | Interval | Rows | First UTC | Last UTC | Missing | Duplicates | Unavailable fields |
|---|---|---:|---:|---|---|---:|---:|---|
| SOLUSDT | futures_klines | 1h | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 0 | 0 |  |
| SOLUSDT | futures_klines | 4h | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 0 | 0 |  |
| SOLUSDT | funding_rate_history | 8h | 93 | 2026-05-06T00:00:00.010000Z | 2026-06-05T16:00:00.009000Z | 0 | 0 |  |
| SOLUSDT | open_interest_statistics | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| SOLUSDT | open_interest_statistics | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| SOLUSDT | top_trader_account_ratio | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| SOLUSDT | top_trader_account_ratio | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| SOLUSDT | top_trader_position_ratio | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| SOLUSDT | top_trader_position_ratio | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| SOLUSDT | open_interest_snapshot | current | 1 | 2026-06-06T20:56:20.924000Z | 2026-06-06T20:56:20.924000Z | n/a | 0 |  |
| XRPUSDT | futures_klines | 1h | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 0 | 0 |  |
| XRPUSDT | futures_klines | 4h | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 0 | 0 |  |
| XRPUSDT | funding_rate_history | 8h | 93 | 2026-05-06T00:00:00.010000Z | 2026-06-05T16:00:00.009000Z | 0 | 0 |  |
| XRPUSDT | open_interest_statistics | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| XRPUSDT | open_interest_statistics | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| XRPUSDT | top_trader_account_ratio | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| XRPUSDT | top_trader_account_ratio | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| XRPUSDT | top_trader_position_ratio | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| XRPUSDT | top_trader_position_ratio | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| XRPUSDT | open_interest_snapshot | current | 1 | 2026-06-06T20:56:24.846000Z | 2026-06-06T20:56:24.846000Z | n/a | 0 |  |
| DOGEUSDT | futures_klines | 1h | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 0 | 0 |  |
| DOGEUSDT | futures_klines | 4h | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 0 | 0 |  |
| DOGEUSDT | funding_rate_history | 8h | 93 | 2026-05-06T00:00:00.010000Z | 2026-06-05T16:00:00.009000Z | 0 | 0 |  |
| DOGEUSDT | open_interest_statistics | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| DOGEUSDT | open_interest_statistics | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| DOGEUSDT | top_trader_account_ratio | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| DOGEUSDT | top_trader_account_ratio | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| DOGEUSDT | top_trader_position_ratio | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| DOGEUSDT | top_trader_position_ratio | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| DOGEUSDT | open_interest_snapshot | current | 1 | 2026-06-06T20:56:24.907000Z | 2026-06-06T20:56:24.907000Z | n/a | 0 |  |
| LINKUSDT | futures_klines | 1h | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 0 | 0 |  |
| LINKUSDT | futures_klines | 4h | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 0 | 0 |  |
| LINKUSDT | funding_rate_history | 8h | 93 | 2026-05-06T00:00:00.010000Z | 2026-06-05T16:00:00.009000Z | 0 | 0 |  |
| LINKUSDT | open_interest_statistics | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| LINKUSDT | open_interest_statistics | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| LINKUSDT | top_trader_account_ratio | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| LINKUSDT | top_trader_account_ratio | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| LINKUSDT | top_trader_position_ratio | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| LINKUSDT | top_trader_position_ratio | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| LINKUSDT | open_interest_snapshot | current | 1 | 2026-06-06T20:56:24.906000Z | 2026-06-06T20:56:24.906000Z | n/a | 0 |  |
| AVAXUSDT | futures_klines | 1h | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 0 | 0 |  |
| AVAXUSDT | futures_klines | 4h | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 0 | 0 |  |
| AVAXUSDT | funding_rate_history | 8h | 93 | 2026-05-06T00:00:00.010000Z | 2026-06-05T16:00:00.009000Z | 0 | 0 |  |
| AVAXUSDT | open_interest_statistics | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| AVAXUSDT | open_interest_statistics | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| AVAXUSDT | top_trader_account_ratio | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| AVAXUSDT | top_trader_account_ratio | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| AVAXUSDT | top_trader_position_ratio | 1h | 723 | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 | 0 |  |
| AVAXUSDT | top_trader_position_ratio | 4h | 180 | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 | 0 |  |
| AVAXUSDT | open_interest_snapshot | current | 1 | 2026-06-06T20:56:28.367000Z | 2026-06-06T20:56:28.367000Z | n/a | 0 |  |

## Pass Condition

PASS_SPB_BINANCE_5_TOKEN_DATA_READY_FOR_JODY_AUDIT
