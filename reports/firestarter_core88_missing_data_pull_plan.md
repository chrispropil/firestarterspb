# Firestarter Core 88 Missing Data Pull Plan

## Trigger

This plan is required because the Core 88 coverage audit found missing local data.

## Missing Symbols

The same six symbols are missing from both OHLCV and local derivatives coverage:

- `PEPEUSDT`
- `BONKUSDT`
- `FLOKIUSDT`
- `MKRUSDT`
- `AIUSDT`
- `OMUSDT`

## Data Needed

### OHLCV

- Endpoint family: Binance USDT perpetual 5m klines
- Scope: 1 month per symbol
- File pattern: `<symbol>_1month_5m.csv`
- Estimated files: 6

### Derivatives Context

Public Binance derivatives context needed per symbol:

- `fundingRate`
- `openInterestHist`
- `takerlongshortRatio`
- `globalLongShortAccountRatio`
- `topLongShortAccountRatio`
- `topLongShortPositionRatio`
- `premiumIndex`

- Estimated files: 42
- Total estimated files: 48

## Estimated Size

Based on the current local file averages:

- Average OHLCV file size: about 0.91 MB
- Average derivatives CSV size: about 24.41 KB

Estimated pull size:

- OHLCV: about 5.46 MB
- Derivatives: about 1.00 MB
- Total: about 6.5 MB

## Existing Bounded Pull Support

The repo already contains bounded pull support for the missing coverage set.

- OHLCV pull helper exists for the missing Core 88 1-month 5m set.
- Derivatives pull coverage already exists for the missing Core 88 derivatives set.

No live pull was run for this audit.

## Manual Approval Gate

Before any live pull, confirm:

1. The six missing symbols should be revalidated against Binance route status.
2. The bounded pull helper is still the desired source of truth for ingestion.
3. The resulting files should remain local-only and uncommitted.

## Approval Required

**Manual approval is required before any live pull.**
