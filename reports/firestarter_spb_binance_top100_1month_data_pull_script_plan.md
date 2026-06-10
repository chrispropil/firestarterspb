# Firestarter SPB Binance Top 100 One-Month Data Pull Script Plan

Input:

- `reports/firestarter_spb_binance_top100_1month_expansion_plan.md`

Purpose:

- Plan a bounded local script for pulling one month of public Binance USD-M futures data for the Top 100 USDT perpetual contracts by 24hr quote volume.
- This is a script plan only.

Boundary:

- No data pull.
- No raw files created.
- No raw data committed.
- No API keys.
- No secrets.
- No Cell 2.
- No labels.
- No model training.
- No trading logic.
- No execution logic.

## Status

`PASS_SPB_BINANCE_TOP100_1MONTH_DATA_PULL_SCRIPT_PLAN_READY`

The plan is ready for review. A separate explicit approval is required before script implementation or any real data pull.

## Proposed Script Path

Recommended script:

- `scripts/pull_binance_top100_1month.py`

Recommended mode:

- default to `--dry-run`
- require explicit `--execute` for a real pull
- refuse to run if both `--dry-run` and `--execute` are supplied
- refuse to run without a bounded `--start` and `--end` UTC window

## Public Binance Endpoints

Base URL:

- `https://fapi.binance.com`

Symbol discovery:

- `/fapi/v1/exchangeInfo`
- `/fapi/v1/ticker/24hr`

Per-symbol data:

- `/fapi/v1/klines` for 1H futures candles
- `/fapi/v1/klines` for 4H futures candles
- `/fapi/v1/fundingRate` for funding-rate history
- `/fapi/v1/openInterest` for current open-interest snapshot
- `/futures/data/openInterestHist` for open-interest statistics where available
- `/futures/data/topLongShortAccountRatio` for top-trader account ratio where available
- `/futures/data/topLongShortPositionRatio` for top-trader position ratio where available

Do not use:

- private account endpoints
- signed endpoints
- order endpoints
- paid data providers
- websocket execution streams
- liquidation, order-book, or trade-print endpoints unless separately approved

## Top 100 Symbol Selection

Selection source:

1. Fetch `/fapi/v1/exchangeInfo`.
2. Fetch `/fapi/v1/ticker/24hr`.
3. Keep symbols that:
   - end with `USDT`
   - are USD-M perpetual contracts
   - have exchangeInfo status `TRADING`
   - have numeric `quoteVolume`
4. Exclude non-perpetual delivery contracts, leveraged-token-like symbols, and inactive symbols.
5. Sort descending by 24hr `quoteVolume`.
6. Select the first 100 symbols.
7. Persist the selected-symbol list in the manifest.

Fail-closed behavior:

- If fewer than 100 valid symbols are found, stop in `HOLD` status unless the operator explicitly approves a smaller set.
- If exchangeInfo and ticker symbol lists disagree, log the mismatch and exclude the mismatched symbols.
- If `quoteVolume` cannot be parsed for a symbol, exclude that symbol and record the reason.

## Output Folder Structure

Dry-run output:

- `reports/firestarter_spb_binance_top100_1month_data_pull_dry_run_audit.md`
- `reports/firestarter_spb_binance_top100_1month_data_pull_dry_run_manifest.csv`

Real-pull output, only after explicit approval:

- `data/research/binance_top100_1month/`
- `data/research/binance_top100_1month/{SYMBOL}/`
- `reports/firestarter_spb_binance_top100_1month_data_pull_audit.md`
- `reports/firestarter_spb_binance_top100_1month_data_pull_manifest.csv`

Per-symbol files:

- `{SYMBOL}_futures_klines_1h.csv`
- `{SYMBOL}_futures_klines_4h.csv`
- `{SYMBOL}_funding_rate_history.csv`
- `{SYMBOL}_open_interest_snapshot.csv`
- `{SYMBOL}_open_interest_statistics_1h.csv`
- `{SYMBOL}_open_interest_statistics_4h.csv`
- `{SYMBOL}_top_trader_account_ratio_1h.csv`
- `{SYMBOL}_top_trader_account_ratio_4h.csv`
- `{SYMBOL}_top_trader_position_ratio_1h.csv`
- `{SYMBOL}_top_trader_position_ratio_4h.csv`

Raw-data commit rule:

- `data/research/binance_top100_1month/` must remain untracked.
- No raw CSV or JSON payloads may be committed.

## Manifest Schema

Manifest file:

- `reports/firestarter_spb_binance_top100_1month_data_pull_manifest.csv`

Recommended columns:

- `run_id`
- `run_timestamp_utc`
- `mode`
- `window_start_utc`
- `window_end_utc`
- `symbol_rank`
- `symbol`
- `dataset`
- `interval`
- `path`
- `rows`
- `first_timestamp_utc`
- `last_timestamp_utc`
- `expected_rows`
- `missing_rows`
- `duplicate_timestamps`
- `unavailable_fields`
- `status`
- `error_code`
- `error_message`
- `source_endpoint`
- `request_count`
- `notes`

Status values:

- `OK`
- `PARTIAL`
- `UNAVAILABLE`
- `FAILED`
- `SKIPPED`
- `DRY_RUN_ONLY`

## Per-Symbol File Schemas

1H/4H candles:

- `open_time`
- `open_time_utc`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `close_time`
- `close_time_utc`
- `quote_asset_volume`
- `number_of_trades`
- `taker_buy_base_asset_volume`
- `taker_buy_quote_asset_volume`
- `ignore`

Funding-rate history:

- `symbol`
- `fundingTime`
- `fundingTime_utc`
- `fundingRate`
- `markPrice`

Open-interest statistics:

- `timestamp`
- `timestamp_utc`
- `symbol`
- `sumOpenInterest`
- `sumOpenInterestValue`
- `CMCCirculatingSupply`

Current open-interest snapshot:

- `symbol`
- `openInterest`
- `time`
- `time_utc`

Top-trader account ratio:

- `timestamp`
- `timestamp_utc`
- `symbol`
- `longAccount`
- `shortAccount`
- `longShortRatio`

Top-trader position ratio:

- `timestamp`
- `timestamp_utc`
- `symbol`
- `longAccount`
- `shortAccount`
- `longShortRatio`

Schema rule:

- Preserve endpoint-native numeric values as strings in raw CSVs.
- Add UTC timestamp columns for auditability.
- Do not add formula fields, labels, or interpretation fields in raw pull outputs.

## Rate-Limit Rules

Request pacing:

- sleep between endpoint calls
- sleep between symbols
- track `X-MBX-USED-WEIGHT-1M` response headers when available
- slow down before approaching Binance 1-minute limits

Suggested defaults:

- `--sleep-endpoint 0.15`
- `--sleep-symbol 0.50`
- `--max-retries 3`
- `--timeout-seconds 30`

429 handling:

- read `Retry-After` if present
- otherwise exponential backoff: 2s, 4s, 8s
- after final failure, mark the dataset `FAILED` or symbol `PARTIAL`

5xx handling:

- retry with exponential backoff
- final failure is recorded in manifest

400/403 handling:

- do not retry blindly
- mark endpoint as `UNAVAILABLE` or `FAILED`
- continue only if the failure is isolated to an optional dataset

## Retry And Fail-Closed Rules

Fail closed at symbol-discovery stage if:

- exchangeInfo cannot be fetched
- 24hr ticker cannot be fetched
- Top 100 selection cannot be produced
- selected symbols cannot be written to dry-run manifest

Fail closed at per-symbol stage if:

- required 1H candles fail after retries
- required 4H candles fail after retries

Allow partial symbol output if:

- funding is unavailable
- OI history is retention-limited
- top-trader ratio endpoints reject the requested startTime
- current OI snapshot is temporarily unavailable

Partial-output rule:

- write only successful endpoint files
- mark missing endpoint rows in manifest
- do not synthesize missing endpoint data
- do not backfill, forward-fill, interpolate, or infer missing rows

## Dry-Run Mode

Dry-run must:

- fetch or mock only symbol-discovery metadata, depending on `--dry-run-network`
- produce the Top 100 selected-symbol list when network dry-run is enabled
- estimate request counts
- estimate output file paths
- validate intended schemas
- validate write permissions for report locations
- produce dry-run audit and manifest files only
- create no raw market-data CSV files

Dry-run must not:

- page through historical candles
- fetch funding history
- fetch OI history
- fetch top-trader history
- create `data/research/binance_top100_1month/`
- write raw JSON payloads

## Audit Outputs

Dry-run audit:

- `reports/firestarter_spb_binance_top100_1month_data_pull_dry_run_audit.md`

Real-pull audit, only after explicit approval:

- `reports/firestarter_spb_binance_top100_1month_data_pull_audit.md`

Audit sections:

- run ID
- UTC window
- selected symbols
- endpoint list
- expected request count
- expected output paths
- row-count expectations
- retention-limit warnings
- unavailable endpoint summary
- rate-limit settings
- fail-closed decisions
- boundary checklist
- pass/hold status

Boundary checklist:

- no API keys
- no private endpoints
- no order endpoints
- no trading logic
- no Cell 2
- no labels
- no model training
- no raw data committed

## Dry-Run Command Examples

Local dry-run without historical pulls:

```powershell
python scripts/pull_binance_top100_1month.py --dry-run --start 2026-05-06T00:00:00Z --end 2026-06-06T00:00:00Z
```

Network dry-run for symbol selection only:

```powershell
python scripts/pull_binance_top100_1month.py --dry-run --dry-run-network --start 2026-05-06T00:00:00Z --end 2026-06-06T00:00:00Z
```

Real pull, blocked until explicit approval:

```powershell
python scripts/pull_binance_top100_1month.py --execute --start 2026-05-06T00:00:00Z --end 2026-06-06T00:00:00Z
```

The real-pull command must not be run from this plan.

## Approval Gate Before Real Pull

Required approval before implementation:

- approve script creation

Required approval before dry-run with network:

- approve public Binance symbol-selection request

Required approval before real pull:

- approve historical data pull
- approve target UTC window
- approve output folder
- approve raw-data local-only policy

Hold condition:

`HOLD_SPB_BINANCE_TOP100_1MONTH_DATA_PULL_NEEDS_APPROVAL`

Pass condition:

`PASS_SPB_BINANCE_TOP100_1MONTH_DATA_PULL_SCRIPT_PLAN_READY`

