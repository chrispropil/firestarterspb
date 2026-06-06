# Firestarter SPB Binance 5 Token Cell 1 Computation Plan

Inputs:

- `reports/firestarter_spb_binance_5_token_formula_spec_confirmation.md`
- `reports/firestarter_spb_binance_5_token_formula_reconstruction_plan.md`
- `data/research/binance_5_token_1month/`

Scope:

- Symbols: SOLUSDT, XRPUSDT, DOGEUSDT, LINKUSDT, AVAXUSDT
- Window UTC: 2026-05-06T00:00:00Z to 2026-06-06T00:00:00Z, end exclusive
- Timeframes: 1H and 4H
- Research-only Cell 1 feature computation plan

Boundary:

- Do not compute values in this plan.
- Do not implement Cell 2.
- Do not create offline labels.
- Do not train models.
- Do not create classification reports.
- Do not create trade labels.
- Do not create execution logic.
- Do not commit raw data.
- Do not post raw data to Slack, Notion, Drive, or ChatGPT.

## Decision

Plan status:

`PASS_SPB_CELL1_COMPUTATION_PLAN_READY`

Reason:

- The available Binance dataset can support a research-only Cell 1 computation design.
- ER, FMLC, Flowprint-proxy, and raw_score have confirmed ancestor-summary component families.
- The plan below includes parent-field gating, partial-window handling, raw-data exclusion, and hold conditions for missing executable thresholds.

Computation status:

- No computation is authorized by this document.
- Exact scoring thresholds and point allocations must be approved before implementation.

## Source Hierarchy

Formula ancestor:

- `Original Firestarter ER-FMLC-Flowprint - Cell 1 Legacy Scan - 2026-05-29`

Confirmed summary-level formula families:

- ER: RVOL 1H, RVOL 4H window, 24h change ranges, near_breakout, clean_reclaim, clamped 0-10.
- FMLC: liquidity/volume floor, 4H range position, 20-bar range position, clean_reclaim, above_4h_trend, anti-blowoff governor, clamped 0-10.
- Flowprint-proxy: RVOL 1H, RVOL 4H window, OI availability/presence, funding band quality, close above EMA21, near_breakout, clamped 0-8.
- raw_score: `raw_score = ER * 0.35 + FMLC * 0.35 + Flowprint * 0.30`.

Excluded source contexts:

- Cell 1 bootstrap/provenance snippets are ingestion context only.
- Bitget/Colab starter feature scaffolds are reference-only for possible future ingestion planning.
- Cell 2 and model scaffolds are blocked reference only.

## Local Dataset Inventory

Expected files:

- 50 local CSV files under `data/research/binance_5_token_1month/`.
- 10 files per symbol:
  - 1H futures candles
  - 4H futures candles
  - funding-rate history
  - 1H open-interest statistics
  - 4H open-interest statistics
  - current open-interest snapshot
  - 1H top-trader account ratio
  - 4H top-trader account ratio
  - 1H top-trader position ratio
  - 4H top-trader position ratio

Raw-data policy:

- Read raw CSV files locally only during a later approved computation lane.
- Do not commit `data/research/binance_5_token_1month/`.
- Do not copy raw rows into reports.
- Do not send raw rows externally.

## Canonical Grids

Build two canonical grids per symbol from candle files:

| Grid | Source | Rows per symbol | First UTC | Last UTC | Status |
|---|---|---:|---|---|---|
| 1H | `{SYMBOL}_futures_klines_1h.csv` | 744 | 2026-05-06T00:00:00Z | 2026-06-05T23:00:00Z | full-window |
| 4H | `{SYMBOL}_futures_klines_4h.csv` | 186 | 2026-05-06T00:00:00Z | 2026-06-05T20:00:00Z | full-window |

Grid rules:

1. Candle open timestamps are the only canonical row anchors.
2. Every output row must map to a canonical candle row.
3. No candle interpolation is needed or allowed.
4. Duplicate timestamps must fail the computation lane.
5. Missing candle rows must fail the computation lane.

## Parent Field Build Plan

### Candle Parents

Use:

- `open`
- `high`
- `low`
- `close`
- `volume`
- `quote_asset_volume`
- `number_of_trades`
- `taker_buy_base_asset_volume`
- `taker_buy_quote_asset_volume`

Derived research-only parents to plan:

- RVOL 1H
- RVOL 4H window
- 24h change
- range position over 20 bars
- range position over 50 4H bars
- EMA21 state
- clean_reclaim state
- above_4h_trend state
- near_breakout state
- volume_usd or quote-volume liquidity proxy

Do not compute these in this plan.

### Funding Parents

Use:

- `fundingRate`
- `markPrice`
- `fundingTime_utc`

Alignment:

- Normalize the observed 9-10 ms timestamp offset to the 8H funding boundary.
- Join funding to candle rows using the most recent funding observation at or before the candle timestamp.
- Record `funding_parent_status` for every output row.

### Open-Interest Parents

Use:

- `sumOpenInterest`
- `sumOpenInterestValue`
- `CMCCirculatingSupply`

Partial-window gate:

- 1H OI fields start at 2026-05-06T21:00:00Z.
- 4H OI fields start at 2026-05-07T00:00:00Z.
- Early rows must be marked `partial_parent_unavailable`.
- Do not backfill, forward-fill, interpolate, or infer missing OI rows.
- Current OI snapshot is metadata only and must not enter historical formula rows.

### Top-Trader Parents

Use:

- account ratio: `longAccount`, `shortAccount`, `longShortRatio`
- position ratio: `longAccount`, `shortAccount`, `longShortRatio`

Partial-window gate:

- 1H top-trader fields start at 2026-05-06T21:00:00Z.
- 4H top-trader fields start at 2026-05-07T00:00:00Z.
- Early rows must be marked `partial_parent_unavailable`.
- Do not backfill, forward-fill, interpolate, or infer missing top-trader rows.

## ER Computation Plan

Classification:

- `ORIGINAL_RECONSTRUCTABLE_SUMMARY`

Ancestor summary:

- RVOL 1H thresholds
- RVOL 4H window thresholds
- 24h change ranges
- near_breakout
- clean_reclaim
- clamp 0-10

Planned parent dependencies:

- candle grid
- RVOL 1H
- RVOL 4H window
- 24h change
- near_breakout
- clean_reclaim

Window status:

- Full-window eligible if the executable ER thresholds are approved.

Required before implementation:

- exact RVOL threshold table
- exact 24h change range table
- exact near_breakout rule
- exact clean_reclaim rule
- exact ER point allocation
- clamp/reject/null policy

## FMLC Computation Plan

Classification:

- `ORIGINAL_RECONSTRUCTABLE_SUMMARY`

Ancestor summary:

- liquidity/volume floor
- 4H range position
- 20-bar range position
- clean_reclaim
- above_4h_trend
- anti-blowoff governor
- clamp 0-10

Planned parent dependencies:

- quote-volume liquidity proxy
- range position over 50 4H bars
- range position over 20 bars
- clean_reclaim
- above_4h_trend
- 24h change for anti-blowoff governor

Window status:

- Full-window eligible for candle-derived FMLC components.
- If a later executable spec adds OI/top-trader dependencies, FMLC must inherit the partial-window gate.

Required before implementation:

- exact liquidity floor
- exact range-position formulas
- exact trend/reclaim rules
- exact anti-blowoff thresholds
- exact FMLC point allocation
- clamp/reject/null policy

## Flowprint-Proxy Computation Plan

Classification:

- `ORIGINAL_RECONSTRUCTABLE_PROXY`

Ancestor summary:

- RVOL 1H
- RVOL 4H window
- OI availability/presence
- funding band quality
- close above EMA21
- near_breakout
- clamp 0-8

Important exclusion:

- Do not use order-book depth, taker flow, trade prints, or liquidation data.

Planned parent dependencies:

- RVOL 1H
- RVOL 4H window
- OI availability/presence
- funding band quality
- close above EMA21
- near_breakout

Window status:

- Candle/funding components are full-window eligible.
- OI availability/presence is partial-window only for exact historical OI statistics.
- Early rows requiring OI must be marked `partial_parent_unavailable`.

Required before implementation:

- exact RVOL threshold table
- exact OI presence rule
- exact funding band-quality rule
- exact EMA21 calculation source and timeframe
- exact near_breakout rule
- exact Flowprint point allocation
- clamp/reject/null policy

## Raw Score Computation Plan

Confirmed formula:

`raw_score = ER * 0.35 + FMLC * 0.35 + Flowprint * 0.30`

Parent gate:

- Compute raw_score only when ER, FMLC, and Flowprint-proxy are all computed and have acceptable parent status.
- If any component is unavailable, raw_score must be marked parent-gated unavailable.
- Do not use raw_score for ranking, alerting, recommendation language, or execution logic.

Do not compute raw_score in this plan.

## Proposed Output Design For Later Approved Computation

Local-only generated data path:

- `data/research/binance_5_token_1month_cell1/`

Report artifacts:

- `reports/firestarter_spb_binance_5_token_cell1_computation_audit.md`
- `reports/firestarter_spb_binance_5_token_cell1_computation_manifest.csv`

Suggested research-only columns:

- `symbol`
- `timeframe`
- `timestamp_utc`
- `er_value`
- `er_parent_status`
- `fmlc_value`
- `fmlc_parent_status`
- `flowprint_proxy_value`
- `flowprint_parent_status`
- `raw_score`
- `raw_score_parent_status`
- `funding_parent_status`
- `oi_parent_status`
- `top_trader_parent_status`
- `partial_window_flag`
- `formula_spec_version`

Forbidden output columns:

- Cell 2 labels
- offline labels
- model labels
- trade labels
- execution instructions
- order fields
- recommendation fields

## Validation Plan

Before any later computation is accepted:

1. Verify 50 expected raw CSV files are present locally.
2. Verify no raw CSV/JSON files are staged or committed.
3. Recount candle rows: 744 1H rows and 186 4H rows per symbol.
4. Verify duplicate candle timestamps equal zero.
5. Verify funding rows align to the 8H cadence after millisecond tolerance.
6. Verify OI/top-trader partial-window starts are preserved.
7. Verify current OI snapshot is not joined into historical rows.
8. Verify parent status columns exist before formula values are accepted.
9. Verify all formula components use approved executable thresholds.
10. Verify no Cell 2, labels, models, classification reports, or execution-adjacent outputs are created.

## Hold Conditions

Use hold marker:

`HOLD_SPB_CELL1_COMPUTATION_PLAN_SPEC_GAP`

Hold the later computation lane if any of the following are true:

- exact ER threshold and scoring rules are unavailable
- exact FMLC threshold and scoring rules are unavailable
- exact Flowprint threshold and scoring rules are unavailable
- raw_score parent-gating rules are not approved
- any raw data file is missing locally
- raw data is accidentally staged for commit
- Cell 2 files, labels, model training, or classification reports appear in scope
- output schema includes trade labels or execution logic

## Pass Condition

This plan is ready for review:

`PASS_SPB_CELL1_COMPUTATION_PLAN_READY`

Next gate:

`JODY REVIEW - SPB_BINANCE_5_TOKEN_CELL1_COMPUTATION_PLAN`

