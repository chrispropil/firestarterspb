# Tardis.dev Sample Request Pack

## Objective
Provide a highly specific, narrow sample request for Tardis.dev support to validate ODIN's processing capability before committing to a paid, terabyte-scale institutional tier.

## 1. Exact Sample Symbols
- `SOLUSDT` (High volume/volatility benchmark)
- `DOGEUSDT` (Retail/meme participation benchmark)
- `AVAXUSDT` (Mid-cap structure benchmark)

## 2. Exact Sample Window
**3-Day Crash/Stress Window (A4 Event Context)**
- **Start:** `2026-05-15 00:00:00 UTC`
- **End:** `2026-05-17 23:59:59 UTC`

## 3. Exact Data Types Requested
- `trades` (Tick-by-tick execution with maker side)
- `incremental_book_L2` (Granular order book depth updates)
- `derivative_ticker` (Contains Open Interest and Funding records)
- `liquidations` (Exchange broadcasted liquidations)
- `mark_price` / `index_price` (If available/broadcasted by the exchange)

## 4. Max Acceptable Sample Size
- **Target:** **~3 GB to 5 GB (Compressed).**
- *Reasoning:* ODIN needs enough bulk to test lazy loading (Polars/Pandas chunking) without waiting hours for a multi-terabyte download. If the sample exceeds 10GB compressed for just 3 days on 3 tokens, ODIN's local pipeline will require immediate architectural redesign before a full 6-month pull.

## 5. Questions to Ask Tardis Support
When submitting this request to Tardis support, include the following questions:
1. *"Can you provide a 3-day CSV sample of the above parameters so we can test our local decompression and parsing pipeline before subscribing?"*
2. *"Are there any known gaps or latency spikes in the Binance or Bitget WebSocket streams during this specific May 2026 volatility window?"*
3. *"Does the `derivative_ticker` channel for Binance USDT Futures in this specific window reliably contain the Open Interest updates, or do you provide a separate REST-polled dataset for OI?"*

## 6. ODIN Storage / Processing Boundary
- **Memory Limit:** Do not attempt to load the entire `incremental_book_L2` file into memory using standard `pandas.read_csv()`. ODIN must use streaming iterators (`chunksize`) or memory-mapped tools like Polars.
- **Drive Space:** Ensure at least 30 GB of free NVMe storage to handle the uncompressed CSV expansion during the test.

## 7. What Success Looks Like Before Purchase
A successful sample test means:
- The compressed files download correctly.
- ODIN can iterate through the `local_timestamp` fields sequentially without crashing.
- We successfully align an L2 order book snapshot with the corresponding tick trades during the `2026-05-16T02:00:00` crash window.
- The total uncompressed scale is verified to be manageable, giving us the green light to purchase the full 6-month history.

**PASS: PASS_TARDIS_SAMPLE_REQUEST_PACK_READY**
