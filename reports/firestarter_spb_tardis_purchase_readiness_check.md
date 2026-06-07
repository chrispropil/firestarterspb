# Tardis.dev Purchase-Readiness & ODIN Feasibility Report

## Objective
Evaluate Tardis.dev as the definitive data backbone for deep microstructure research (DNA/Tape) and validate if local processing (ODIN) can feasibly handle the immense scale of raw tick/L2 data.

## 1. Exchange Coverage
- **Binance USDT Perps:** ✅ **Fully Covered.** (Available since ~November 17, 2019).
- **Bitget USDT Perps:** ✅ **Fully Covered.**

## 2. Available Data Types
Tardis directly records WebSocket streams exactly as broadcasted by the exchange:
- **Trades:** ✅ Yes (Tick-by-tick with buy/sell maker sides).
- **L2 Order Book Incremental:** ✅ Yes (Every single bid/ask update).
- **L2 Order Book Snapshots:** ✅ Yes (Synthetic snapshots generated for easy sync).
- **Open Interest:** ✅ Yes (Often logged in the `derivative_ticker` channel).
- **Funding Rates:** ✅ Yes.
- **Liquidations:** ✅ Yes (Logged if broadcasted via the exchange WS liquidation channel).
- **Mark/Index Price:** ✅ Yes.
- **OHLCV:** ✅ Yes (Though deriving it from raw trades gives exact precision).

## 3. Data Integrity & Precision
- **Earliest History:** Extends back to late 2019 for Binance Futures.
- **Delisted Symbols:** ✅ **Survivor-Bias Free.** All delisted, expired, and renamed pairs are preserved exactly as they traded.
- **Timestamp Precision:** Microsecond (`µs`) precision. Tardis provides both the `exchange_timestamp` (when it happened on the matching engine) and the `local_timestamp` (when Tardis servers received it) for latency analysis.

## 4. Export Formats
- **CSV Format:** Daily chunked gzip-compressed CSV files.
- **Local Download:** Direct HTTP bulk downloads via CLI or UI.
- **API/Replay:** Dedicated Python/Node.js client libraries for seamless historical streaming.
- **Python Libraries:** The `tardis-client` seamlessly normalizes schemas across different exchanges.

---

## 5. Storage Burden Estimates
Tardis data—specifically `incremental_book_L2`—is massive. A volatile pair like `SOLUSDT` can generate 500MB+ of compressed data *per day* (uncompressing to 2GB-5GB).

- **10 Symbols / 5 Event Windows (assuming 3-day windows = 150 symbol-days):** ~50GB Compressed / ~250GB Uncompressed. *(Easily manageable)*
- **15 Symbols / 10 Event Windows (450 symbol-days):** ~150GB Compressed / ~750GB Uncompressed. *(Requires decent SSD space)*
- **50 Symbols / 6 Months (~9000 symbol-days):** **~3.5TB to 5TB Compressed / 20TB+ Uncompressed.** *(Requires dedicated NVMe RAID/NAS and chunked processing)*

## 6. ODIN Feasibility Evaluation
Can the local ODIN environment handle this?
- **Download Size:** Yes, assuming a standard fiber/broadband connection, but TB-scale pulls take days.
- **Decompression & Local Parsing:** **WARNING.** You cannot load an entire month of Tardis L2 data into Pandas memory at once. ODIN must be coded to use chunked processing (e.g., `Polars` lazyframes or `Pandas` chunksize iterator).
- **Replay Windows:** Generating specific event windows (like the A4 crash) is exactly what Tardis is built for.
- **Feasibility Verdict:** High feasibility for event-driven replays. Low feasibility for holding a 50-token, 6-month continuous L2 state in RAM.

---

## 7. Recommended First Paid Sample Pull
Before buying the massive institutional tiers, validate ODIN's processing pipeline with a cheap surgical pull:
- **Symbols:** 3 (e.g., `SOLUSDT`, `DOGEUSDT`, `AVAXUSDT`)
- **Window:** 3 days (spanning the recent A4 Crash Start event: `2026-05-15` to `2026-05-17`)
- **Data Types:** `trades`, `incremental_book_L2`, `derivative_ticker`, `liquidations`
- **Max Expected Size:** ~3-5GB compressed.
- **Goal:** Write an ODIN Python script to parse the `local_timestamp`, sync the L2 book, and match it against the trades without running out of RAM.

---

## 8. Safety Boundaries & Compliance
- **No Live Trading:** This data is strictly for historical DNA/Tape reconstruction.
- **No API Key Exposure:** API keys for Tardis downloads must reside in `.env` files and never be committed.
- **No Raw Data Commits:** Gigabyte CSVs must be aggressively `.gitignore`'d.
- **No Cell 2/Strategy Claims:** This is raw microstructure recording. No forward-looking alpha claims will be attached to it until rigorous out-of-sample validation.

---

## 9. Comparison & Final Recommendation

**Compared to CoinGlass:** CoinGlass is infinitely easier for macro-structural metrics (historical OI, Funding, aggregated L/S ratios) because the data is already heavily aggregated into 1H/4H candles. Tardis requires building those candles from scratch using raw WS data. 

**Conclusion:** 
Use CoinGlass for fast SPB multi-month macro-behavioral testing.
Use Tardis exclusively for precision DNA/Tape event-window reconstruction.

**Status:**
**PASS: TARDIS_PRIMARY_APPROVED_FOR_SAMPLE_CHECK**
