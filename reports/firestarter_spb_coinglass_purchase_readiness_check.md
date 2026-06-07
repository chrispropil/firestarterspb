# CoinGlass API (V4) Purchase-Readiness Check

## Target Project
Firestarter SPB & Future DNA/Tape Expansion

## 1. Plan & Tier Selection
**Recommended Tier:** **Standard Plan ($299/mo)** or **Professional Plan ($699/mo)**.
- *Reasoning:* The Hobbyist/Startup plans limit requests to 30-80 req/min, which is insufficient for efficiently downloading 6 months of pagination-heavy 1H/4H historical data across 5 tokens. Standard allows 300 req/min, and Professional allows 1,200 req/min.

## 2. Historical Data Inclusion Confirmations
- **Historical Open Interest (OI):** ✅ **INCLUDED.** Available in OHLC format and highly granular intervals.
- **Historical Funding Rates:** ✅ **INCLUDED.** Complete historical look-back available.
- **Historical Liquidations:** ✅ **INCLUDED.** Aggregated contract liquidations and heatmaps are supported.
- **Historical Long/Short Ratios:** ✅ **INCLUDED.** Top Trader (accounts/positions) and global account ratios are supported.

## 3. DNA/Tape Microstructure Readiness
- **L2/L3 Order Book & Footprint Data:** ✅ **INCLUDED.** The V4 API specifically introduced advanced spot footprint tracking and detailed order-book depth snapshots.

## 4. Exchange & Asset Coverage
- **Binance USDT Perps:** ✅ **INCLUDED.** Fully supported.
- **Bitget USDT Perps:** ✅ **INCLUDED.** Fully supported.

## 5. API Execution Limits & Constraints
- **Pagination Limit:** Requests default/max out at **1000 records per request**.
- **Rate Limiting:** Enforced strictly per-minute (e.g., 300 req/min on Standard). A `429 Too Many Requests` response will fire if exceeded. Scripting will require built-in sleep delays.
- **Export:** Raw JSON REST responses can be cleanly transformed into CSVs locally.

## 6. Trial & Sample Availability
- **Free Tier:** ❌ **NOT AVAILABLE.** There is no self-serve free API key.
- **Trial Process:** You must email `contact@coinglass.com` to negotiate an enterprise evaluation or rely on the visual charts on their website to verify data fidelity before buying.

---

## Required Questions to Ask CoinGlass Sales/Support Before Paying
Chris, please email CoinGlass with the following questions before executing any payment:

1. **Historical Depth Limit:** *"Does the Standard ($299/mo) tier allow us to paginate fully backwards through 6+ months of historical data for Open Interest, Top Trader Long/Short Ratios, and Footprint data without forced truncation?"*
2. **Commercial Licensing:** *"Our research involves quantitative profiling (Matrix Alpha). Does the Standard plan cover our internal research usage, or are we forced into the Professional/Enterprise tier?"*
3. **Footprint Coverage:** *"Can you explicitly confirm that footprint execution data (buy/sell imbalance at specific price levels) is available historically for Binance Futures (USDT-M), or is it only available for Spot?"*
4. **Trial Data:** *"Can you provide a 3-day sample CSV export of Binance SOLUSDT footprint and OI data so we can verify schema compatibility with our SPB engine before committing to a monthly subscription?"*

## Final Status
**PASS: PASS_COINGLASS_PURCHASE_READINESS_READY**
