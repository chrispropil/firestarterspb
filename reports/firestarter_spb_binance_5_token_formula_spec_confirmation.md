# Firestarter SPB Binance 5 Token Formula Spec Confirmation

Input:

- `reports/firestarter_spb_binance_5_token_formula_reconstruction_plan.md`
- Notion ancestor: `Original Firestarter ER-FMLC-Flowprint - Cell 1 Legacy Scan - 2026-05-29`
- Cell 1 bootstrap/provenance snippet from Chris: ingestion context only, not formula equations
- Colab Cell 2 scaffold: offline labeling scaffold only, not Cell 1 ER/FMLC/Flowprint formula spec

Scope:

- Symbols: SOLUSDT, XRPUSDT, DOGEUSDT, LINKUSDT, AVAXUSDT
- Window UTC: 2026-05-06T00:00:00Z to 2026-06-06T00:00:00Z, end exclusive
- Timeframes: 1H and 4H

Boundary:

- Research-only formula spec confirmation.
- No trade signals.
- No Cell 2 labels.
- No recommendation language.
- No performance claims.
- No raw market-data publication outside the local sandbox.
- No computation of formula values in this report.

## Confirmation Decision

The Notion ancestor page confirms summary-level original Firestarter formula lineage for ER, FMLC, Flowprint, and raw_score. The available Binance dataset and reconstruction plan confirm parent-field availability and reconstruction boundaries for the SPB five-token sandbox.

Overall classification:

`ORIGINAL_RECONSTRUCTABLE_SUMMARY`

Reason:

- Parent fields are available for research-only reconstruction design.
- Full-window and partial-window components are clearly separated.
- The Notion ancestor confirms the original component families and score weights at summary level.
- Full executable formulas, thresholds, and implementation details are still not reconstructed in this report.
- Computing final values remains blocked until an approved computation spec is created from the ancestor summary.

Ancestor source:

- Title: `Original Firestarter ER-FMLC-Flowprint - Cell 1 Legacy Scan - 2026-05-29`
- Notion page ID: `3702c020-d847-81ee-af64-cef352b90632`
- Source status in page: preserved historical research ancestor / replay candidate; documentation only, not active scanner logic.

## Source Hierarchy

Formula ancestor:

- Use `Original Firestarter ER-FMLC-Flowprint - Cell 1 Legacy Scan - 2026-05-29` as the formula source for ER, FMLC, Flowprint, and raw_score summary lineage.

Bootstrap/provenance context:

- The Cell 1 bootstrap/provenance snippet supplied by Chris is ingestion context only.
- It supports read-only dataset inventory, fail-closed file allowlisting, sha256 manifest/provenance logging, and boundary checks.
- It must not be treated as ER, FMLC, Flowprint, or raw_score formula equations.
- It must not change the current formula-source gate.

Cell 2 scaffold context:

- The pasted Colab Cell 2 scaffold is an offline labeling scaffold, not the missing Cell 1 ER/FMLC/Flowprint formula spec.
- Do not implement Cell 2 in this lane.
- Do not use Cell 2 scaffold fields, labels, or downstream cleanup logic as a source for ER, FMLC, Flowprint, or raw_score reconstruction.
- The current formula-spec update remains anchored to the known Cell 1 formula ancestor summary only.

## Formula Classification Summary

| Field | Classification | Reason |
|---|---|---|
| ER | ORIGINAL_RECONSTRUCTABLE_SUMMARY | Ancestor confirms ER as ignition / momentum pressure using rvol, change_24h, near_breakout, and clean_reclaim components, clamped 0 to 10. |
| FMLC | ORIGINAL_RECONSTRUCTABLE_SUMMARY | Ancestor confirms FMLC as structural quality / anti-blowoff governor using liquidity, range position, reclaim/trend, and change_24h governor components, clamped 0 to 10. |
| Flowprint-proxy | ORIGINAL_RECONSTRUCTABLE_PROXY | Ancestor confirms Flowprint as a derivatives / volume participation proxy using relative volume, funding, OI availability, EMA reclaim, and near-breakout state, clamped 0 to 8. |

No field is classified as `ORIGINAL_RECONSTRUCTED` because this report confirms summary-level formula ancestry only and does not reconstruct executable formulas or compute outputs.

## Raw Score Formula

Confirmed ancestor raw_score formula:

`raw_score = ER * 0.35 + FMLC * 0.35 + Flowprint * 0.30`

Use rule:

- This formula is confirmed for future reconstruction design.
- Do not compute raw_score in this report.
- Do not use raw_score for ranking, alerting, recommendation language, or execution logic.

## ER Parent Fields

Confirmed available full-window parent fields:

- `open`
- `high`
- `low`
- `close`
- `volume`
- `quote_asset_volume`
- `number_of_trades`
- 1H canonical candle grid
- 4H canonical candle grid

Ancestor-confirmed ER component family:

- `rvol_1h` thresholds
- `rvol_4h_window` thresholds
- `change_24h` ranges
- `near_breakout`
- `clean_reclaim`
- clamped 0 to 10

Full-window status:

- 1H: ready across 744 rows per symbol.
- 4H: ready across 186 rows per symbol.

Partial-window dependencies:

- None required by the current reconstruction plan.
- If an approved ER formula later requires OI or top-trader fields, ER must inherit the same partial-window guard as FMLC.

Missing executable formula details:

- exact ER point allocation by threshold
- exact rvol thresholds
- exact change_24h ranges
- exact near_breakout definition
- exact clean_reclaim definition
- exact lookback windows for each parent
- required handling for zero-volume or flat-range candles

Classification:

`ORIGINAL_RECONSTRUCTABLE_SUMMARY`

## FMLC Parent Fields

Confirmed available parent fields:

- Funding: `fundingRate`, `markPrice`
- OI statistics: `sumOpenInterest`, `sumOpenInterestValue`, `CMCCirculatingSupply`
- Top-trader account ratio: `longAccount`, `shortAccount`, `longShortRatio`
- Top-trader position ratio: `longAccount`, `shortAccount`, `longShortRatio`
- Candle timestamp and symbol fields for alignment

Ancestor-confirmed FMLC component family:

- `volume_usd` liquidity floor
- `range_pos_50_4h`
- `range_pos_20`
- `clean_reclaim`
- `above_4h_trend`
- anti-blowoff governor based on `change_24h`
- clamped 0 to 10

Full-window components:

- Funding is available on the 8H cadence for the full requested window after millisecond timestamp normalization.
- Candle timestamps and symbol alignment are available for the full 1H and 4H windows.

Partial-window components:

- OI statistics are partial-window only.
- Top-trader account ratio is partial-window only.
- Top-trader position ratio is partial-window only.

Partial-window guard:

- 1H OI/top-trader fields start at 2026-05-06T21:00:00Z.
- 4H OI/top-trader fields start at 2026-05-07T00:00:00Z.
- Early rows must be marked parent unavailable when those fields are required.
- No backfill, forward-fill, interpolation, or inference is approved.

Missing executable formula details:

- exact FMLC point allocation
- exact liquidity floor
- exact range position formulas
- exact above_4h_trend definition
- exact anti-blowoff governor thresholds
- treatment of partial parent availability
- output bounds and clamp/reject policy

Classification:

`ORIGINAL_RECONSTRUCTABLE_SUMMARY`

## Flowprint-Proxy Parent Fields

Confirmed available full-window candle-flow fields:

- `volume`
- `quote_asset_volume`
- `number_of_trades`
- `taker_buy_base_asset_volume`
- `taker_buy_quote_asset_volume`
- `open`
- `high`
- `low`
- `close`

Confirmed available partial-window context fields:

- `sumOpenInterest`
- `sumOpenInterestValue`
- top-trader account ratio fields
- top-trader position ratio fields

Ancestor-confirmed Flowprint component family:

- `rvol_1h`
- `rvol_4h_window`
- open-interest presence
- funding band quality
- close above EMA21
- `near_breakout`
- clamped 0 to 8

Important ancestor correction:

- Flowprint does not use order-book depth, taker flow, trade prints, or liquidation data.

Full-window components:

- Candle-flow components are available across the full 1H and 4H windows.

Partial-window components:

- OI-enhanced and top-trader-enhanced components are available only within the retained partial window.

Missing executable formula details:

- exact Flowprint point allocation
- exact rvol thresholds
- exact funding band-quality thresholds
- exact open-interest presence rule
- exact close-above-EMA21 calculation
- exact near_breakout definition
- output bounds and clamp/reject policy

Classification:

`ORIGINAL_RECONSTRUCTABLE_PROXY`

Reason:

- The ancestor confirms Flowprint as a derivatives / volume participation proxy.
- The available Binance fields can support a research proxy reconstruction path.
- Final computation still requires an approved executable proxy formula spec before values are produced.

## Full-Window vs Partial-Window Components

| Component | Full-window ready | Partial-window only | Notes |
|---|---|---|---|
| 1H candles | yes | no | 744 rows per symbol |
| 4H candles | yes | no | 186 rows per symbol |
| Funding | yes | no | Align to 8H cadence with millisecond tolerance |
| OI statistics 1H | no | yes | First 21 hourly rows unavailable |
| OI statistics 4H | no | yes | First 6 four-hour rows unavailable |
| Top-trader account ratio 1H | no | yes | First 21 hourly rows unavailable |
| Top-trader account ratio 4H | no | yes | First 6 four-hour rows unavailable |
| Top-trader position ratio 1H | no | yes | First 21 hourly rows unavailable |
| Top-trader position ratio 4H | no | yes | First 6 four-hour rows unavailable |
| Current OI snapshot | no | no | Metadata only; exclude from historical formula rows |

## Missing Original Firestarter Executable Details

The following items must be supplied or reconstructed from the full original Cell 1 before formula computation:

- exact ER threshold table and point allocation
- exact FMLC threshold table and point allocation
- exact Flowprint threshold table and point allocation
- exact lookback windows
- normalization and scaling method for each formula
- clamp/reject/null behavior
- clamp, reject, or null policy for out-of-bounds values
- parent-gating rules when required fields are unavailable
- explicit policy for partial OI/top-trader windows
- output schema approval for formula values and parent status fields

## Hold Gate

Hold formula computation until the missing executable details are supplied or reconstructed from the full original Cell 1 and approved.

Formula computation should not begin from this report alone.

Hold marker:

`HOLD_SPB_FORMULA_COMPUTATION_PENDING_EXECUTABLE_SPEC`

## Recommended Next Gate

Provide or approve the executable Firestarter formula specification for:

- ER
- FMLC
- Flowprint-proxy
- raw_score

Next gate:

`JODY REVIEW - SPB_BINANCE_5_TOKEN_FORMULA_SPEC_CONFIRMATION`
