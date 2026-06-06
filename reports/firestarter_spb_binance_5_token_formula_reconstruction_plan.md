# Firestarter SPB Binance 5 Token Formula Reconstruction Plan

Run basis:

- `reports/firestarter_spb_binance_5_token_1month_pull_audit.md`
- `reports/firestarter_spb_binance_5_token_1month_manifest.csv`
- `reports/firestarter_spb_binance_5_token_reconstruction_readiness.md`

Dataset folder:

- `data/research/binance_5_token_1month/`

Scope:

- Symbols: SOLUSDT, XRPUSDT, DOGEUSDT, LINKUSDT, AVAXUSDT
- Window UTC: 2026-05-06T00:00:00Z to 2026-06-06T00:00:00Z, end exclusive
- Timeframes: 1H and 4H

Boundary:

- Research reconstruction plan only.
- No trade signals.
- No Cell 2 labels.
- No recommendation language.
- No performance claims.
- No raw data publication outside the local sandbox.
- No use of API keys, secrets, paid data, or live execution.

## Current Gate

Formula reconstruction can proceed with a mandatory partial-window warning for open-interest and top-trader fields.

Readiness marker inherited from the reconstruction readiness audit:

`PASS_SPB_RECONSTRUCTION_READY_WITH_PARTIAL_OI_WARNING`

This plan should be treated as a formula reconstruction design gate, not as computed formula output.

## Source Integrity Baseline

| Source family | Files per symbol | Full-window status | Reconstruction status |
|---|---:|---|---|
| 1H futures candles | 1 | Complete: 744 rows per symbol | Ready |
| 4H futures candles | 1 | Complete: 186 rows per symbol | Ready |
| Funding history | 1 | Complete 8H cadence: 93 rows per symbol | Ready after millisecond timestamp normalization |
| Open-interest statistics 1H | 1 | Partial: 723 rows, first 21 hours unavailable | Ready only after partial-window guard |
| Open-interest statistics 4H | 1 | Partial: 180 rows, first 6 bars unavailable | Ready only after partial-window guard |
| Top-trader account ratio 1H | 1 | Partial: 723 rows, first 21 hours unavailable | Ready only after partial-window guard |
| Top-trader account ratio 4H | 1 | Partial: 180 rows, first 6 bars unavailable | Ready only after partial-window guard |
| Top-trader position ratio 1H | 1 | Partial: 723 rows, first 21 hours unavailable | Ready only after partial-window guard |
| Top-trader position ratio 4H | 1 | Partial: 180 rows, first 6 bars unavailable | Ready only after partial-window guard |
| Current OI snapshot | 1 | Present after research window | Metadata only; exclude from historical formula rows |

## Canonical Reconstruction Grids

Create two canonical per-symbol timestamp grids:

| Grid | Start UTC | End UTC | Expected rows per symbol | Source anchor |
|---|---|---|---:|---|
| 1H | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | 744 | 1H candle `open_time_utc` |
| 4H | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | 186 | 4H candle `open_time_utc` |

Rules:

1. Candle rows define the canonical grid.
2. Formula rows must preserve one output row per candle row unless a formula is explicitly marked unavailable by parent-field gating.
3. No missing candle rows may be interpolated because the candle grids are already complete.
4. Funding rows should be aligned to the nearest prior 8H funding boundary with a tolerance for the observed 9-10 ms timestamp offset.
5. OI/top-trader fields must be joined only where their timestamps exist in the retained partial window.

## Partial-Window Guard

The following fields are partial-window only:

- OI statistics: `sumOpenInterest`, `sumOpenInterestValue`, `CMCCirculatingSupply`
- Top-trader account ratio: `longAccount`, `shortAccount`, `longShortRatio`
- Top-trader position ratio: `longAccount`, `shortAccount`, `longShortRatio`

Retained windows:

| Timeframe | Retained start | Retained end | Missing at start |
|---|---|---|---:|
| 1H | 2026-05-06T21:00:00Z | 2026-06-05T23:00:00Z | 21 rows per symbol |
| 4H | 2026-05-07T00:00:00Z | 2026-06-05T20:00:00Z | 6 rows per symbol |

Policy:

- Formula components that require OI/top-trader fields must be marked `partial_parent_unavailable` before the retained start.
- OI/top-trader-dependent formulas must not backfill, forward-fill, interpolate, or infer the missing initial rows.
- Current OI snapshot must not be used to fill historical OI fields.
- Candle-only formula components may still compute across the full window.

## ER Reconstruction Plan

ER should be reconstructed as a candle-derived research field unless a later approved formula spec explicitly adds parent dependencies.

Allowed parent fields:

- `open`, `high`, `low`, `close`
- `volume`
- `quote_asset_volume`
- `number_of_trades`
- 1H and 4H canonical timestamp grids

Plan:

1. Build ER on the full 1H and 4H candle grids.
2. Require non-null OHLC values on every row.
3. Require numeric conversion checks for all parent fields.
4. Emit parent coverage counts before computing any final ER column.
5. Clamp or reject values only if the approved formula spec defines bounds.

Readiness:

- Full-window ready for candle-only reconstruction.
- Hold only if the approved ER formula requires OI/top-trader fields without accepting the partial-window guard.

## FMLC Reconstruction Plan

FMLC should be reconstructed as a parent-gated research field using funding and participation context where available.

Allowed parent fields:

- Funding: `fundingRate`, `markPrice`
- OI statistics: `sumOpenInterest`, `sumOpenInterestValue`, `CMCCirculatingSupply`
- Top-trader account ratio: `longAccount`, `shortAccount`, `longShortRatio`
- Top-trader position ratio: `longAccount`, `shortAccount`, `longShortRatio`
- Candle context as needed for timestamp and symbol alignment

Plan:

1. Normalize funding timestamps to the 8H cadence before joining to candle grids.
2. Join funding to 1H/4H rows by the most recent available funding observation at or before each candle timestamp.
3. Join OI/top-trader fields only on exact retained-window timestamps.
4. Mark early-window rows as parent unavailable where OI/top-trader fields are required.
5. Produce per-parent availability flags before computing FMLC.
6. Keep current OI snapshot outside the FMLC historical row set.

Readiness:

- Ready for partial-window reconstruction.
- Not full-window ready for any FMLC variant requiring OI/top-trader parents.

## Flowprint-Proxy Reconstruction Plan

Flowprint proxy should be split into candle-flow components and optional participation-context components.

Allowed full-window candle-flow fields:

- `volume`
- `quote_asset_volume`
- `number_of_trades`
- `taker_buy_base_asset_volume`
- `taker_buy_quote_asset_volume`
- OHLC fields for candle range context

Allowed partial-window context fields:

- `sumOpenInterest`
- `sumOpenInterestValue`
- top-trader account ratio fields
- top-trader position ratio fields

Plan:

1. Compute candle-flow parent coverage across the full 1H and 4H grids.
2. Keep candle-only proxy components eligible for the full window.
3. Gate OI/top-trader-enhanced proxy components to the retained partial window.
4. Record whether each row is candle-only, OI-enhanced, top-trader-enhanced, or parent unavailable.
5. Do not introduce new proxy formulas beyond the approved reconstruction spec.

Readiness:

- Candle-flow proxy components are full-window ready.
- OI/top-trader-enhanced proxy components are partial-window ready only.

## Output Schema Plan

Recommended reconstruction output should be local-only and should separate parent coverage from formula values.

Suggested files:

- `data/research/binance_5_token_1month_reconstructed/spb_reconstruction_1h.csv`
- `data/research/binance_5_token_1month_reconstructed/spb_reconstruction_4h.csv`
- `reports/firestarter_spb_binance_5_token_formula_reconstruction_audit.md`
- `reports/firestarter_spb_binance_5_token_formula_reconstruction_manifest.csv`

Suggested non-signal columns:

- `symbol`
- `timeframe`
- `timestamp_utc`
- `er_value`
- `er_parent_status`
- `fmlc_value`
- `fmlc_parent_status`
- `flowprint_proxy_value`
- `flowprint_parent_status`
- `funding_parent_status`
- `oi_parent_status`
- `top_trader_account_parent_status`
- `top_trader_position_parent_status`
- `partial_window_flag`

The output schema must not include Cell 2 labels, signal labels, execution fields, or recommendation fields.

## Validation Plan

Before formula values are accepted:

1. Recount all input rows by file.
2. Rebuild 1H and 4H timestamp grids from candle files.
3. Confirm candle continuity remains unchanged: 744 rows per symbol for 1H, 186 rows per symbol for 4H.
4. Confirm funding cadence remains 93 rows per symbol and aligns after millisecond normalization.
5. Confirm OI/top-trader partial windows remain unchanged: 723 rows at 1H and 180 rows at 4H per symbol.
6. Confirm duplicate timestamps remain zero for every joined parent dataset.
7. Confirm no raw rows are written into Slack, Notion, Drive, or ChatGPT.
8. Confirm current OI snapshot is excluded from historical formula computations.
9. Confirm every formula row has parent status fields.
10. Confirm partial-window gaps are visible in the audit output.

## Hold Conditions

Hold formula reconstruction if any of the following occur:

- Any candle file has missing or duplicate timestamps.
- Funding cannot be aligned with the 8H cadence after millisecond tolerance.
- OI/top-trader fields are backfilled, forward-filled, interpolated, or inferred across the missing initial window.
- Current OI snapshot is used as historical OI.
- Formula code creates Cell 2 labels, signal labels, execution fields, or recommendation language.
- Formula code publishes raw market data outside the local sandbox.
- Parent coverage is not reported separately from formula values.
- Approved formula definitions are not available for ER, FMLC, or Flowprint proxy.

## Recommended Next Gate

Proceed to formula-spec confirmation before computing values.

Next gate:

`JODY REVIEW - SPB_BINANCE_5_TOKEN_FORMULA_RECONSTRUCTION_PLAN`

