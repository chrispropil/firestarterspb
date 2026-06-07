# Top 100 Derivatives Data Gap Plan Audit

## 1. Plan Completeness Checklist
- **Binance Endpoints Identified:** YES (GET `/fapi/v1/fundingRate`, `/futures/data/openInterestHist`, `/futures/data/takerlongshortRatio`, `/futures/data/globalLongShortAccountRatio`, `/futures/data/topLongShortAccountRatio`, `/futures/data/topLongShortPositionRatio`, `/fapi/v1/premiumIndex`).
- **Retention Limits Verified:** YES (30-day API limit noted).
- **Expected Cadence Documented:** YES (8-hour funding, 5-minute or 1-hour intervals for derivatives stats).
- **Formula Mapping Outlined:** YES (mapped to ER, FMLC, Flowprint).
- **Missing Public Fields Noted:** YES (L3, non-aggregated institutional stats).
- **Output Folder Designated:** YES (`data/research/binance_top100_derivatives_context_1month/`).
- **Manifest Schema Defined:** YES.
- **Dry-Run Selection Logic Defined:** YES (test pull on BTCUSDT, ETHUSDT, SOLUSDT).
- **Rate-limiting & Retry Rules Specified:** YES (1000/min weight limit, backoff with jitter).
- **Fail-Closed Strategy Configured:** YES (fail-closed on 3 retries, abort write).
- **Approval Gate Placed:** YES (`PASS_TOP100_DERIVATIVES_PULL_START` required).

## 2. Safety & Security Bounds
- **Any data pulled during this step?** NO.
- **Any formulas implemented?** NO.
- **Any Cell 2 labels or ML model training code created?** NO.
- **Any trading logic or recommendations written?** NO.
- **Any secrets or credentials exposed?** NO.
- **Any raw CSV/JSON staged or committed?** NO.
