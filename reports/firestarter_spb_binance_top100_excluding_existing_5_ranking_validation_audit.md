# Firestarter SPB: Ranking Validation Audit (Top 100 Excluding Core 5)

## Overview
This audit mathematically verifies that the 100 symbols successfully ingested in the prior execution genuinely represent the top 100 Binance USDT-M perpetual contracts ordered by 24h quoteVolume, excluding the explicit baselines (`SOLUSDT`, `XRPUSDT`, `DOGEUSDT`, `LINKUSDT`, `AVAXUSDT`).

## Ranking Validation Results
1. **Endpoint Confirmed**: Active perpetual status was sourced strictly from `fapi/v1/exchangeInfo`. Volume rankings were sourced strictly from `fapi/v1/ticker/24hr`.
2. **Filters Confirmed**: The script strictly gated for `status == 'TRADING'`, `contractType == 'PERPETUAL'`, and `quoteAsset == 'USDT'`.
3. **Numeric Sort Confirmed**: `quoteVolume` was parsed as a numeric float (`float(x.get('quoteVolume', 0))`) to ensure accurate mathematical sorting (preventing string-based lexical errors).
4. **Sort Order Confirmed**: Symbols were correctly sorted by volume descending (`reverse=True`).
5. **Baseline Exclusions Confirmed**: The 5 core baseline symbols were structurally discarded prior to slicing the top 100 array.

## Volume Snapshot (Live Audit)
*Note: Snapshot pulled shortly after original ingestion; exact figures fluctuate slightly intra-day.*

### Top 25 Selected Symbols (By quoteVolume)
1. BTCUSDT: 10,670,261,708.81
2. ETHUSDT: 8,004,891,152.39
3. ZECUSDT: 2,289,493,822.28
4. HYPEUSDT: 989,343,030.75
5. WLDUSDT: 729,301,820.70
6. ALLOUSDT: 706,939,255.63
7. LABUSDT: 463,702,766.25
8. BNBUSDT: 390,536,548.75
9. NEARUSDT: 332,319,576.81
10. SIRENUSDT: 292,329,739.21
11. FIDAUSDT: 276,105,141.11
12. BSBUSDT: 264,306,726.71
13. SKYAIUSDT: 237,963,224.01
14. HOMEUSDT: 229,107,412.08
15. BEATUSDT: 222,318,807.30
16. ADAUSDT: 202,206,310.28
17. SUIUSDT: 200,259,772.33
18. 1000PEPEUSDT: 200,256,793.40
19. BTWUSDT: 196,925,718.66
20. XLMUSDT: 187,070,264.43
21. 币安人生USDT: 170,742,905.65
22. HUSDT: 159,646,309.77
23. ENAUSDT: 136,251,181.01
24. TONUSDT: 128,791,695.37
25. TAOUSDT: 122,038,780.70

### Bottom 10 Selected Symbols (By quoteVolume)
91. MEMEUSDT: 15,578,317.64
92. GENIUSUSDT: 14,743,857.55
93. RAVEUSDT: 14,444,167.29
94. KITEUSDT: 13,967,323.87
95. 1000BONKUSDT: 13,905,446.01
96. PLAYUSDT: 13,567,097.77
97. MAGMAUSDT: 13,515,005.53
98. INUSDT: 13,281,237.28
99. SLXUSDT: 13,179,248.44
100. BASEDUSDT: 12,782,485.65

## Symbol Syntax Validation
- **Non-Standard/Unicode Symbols Detected:** 2 (`币安人生USDT`, `龙虾USDT`)
- **Validity:** YES. These are legitimate, actively traded community/meme targets listed natively under Binance's public USDT-M Futures endpoint. The ingestion script was successfully patched to handle their URL encoding safely.
- **Filter Tightness:** The `TRADING`, `PERPETUAL`, and `USDT` filters are functioning exactly as intended. No corrections are recommended, and these community tokens represent legitimate massive-volume liquidity vectors that SPB must ingest.
