# Chris Approval: Cell 1 Sandbox Defaults

On June 7, 2026, Chris officially approved the following sandbox default parameters and thresholds for partial Cell 1 reconstruction on the Top 100 dashboard.

---

## 1. Approved Sandbox Defaults

1. **RVOL Lookback Window:**
   - **Approved:** 24 periods (24 hours on 1H grid, 96 hours on 4H grid).
2. **Liquidity Floor:**
   - **Approved:** $10,000,000 daily quote volume.
3. **Near Breakout Margin:**
   - **Approved:** Within 1.0% of the 20-bar rolling high.
4. **Clean Reclaim:**
   - **Approved:** Close above EMA21 with volume $> 1.2\times$ average.
5. **Anti-Blowoff Governor:**
   - **Approved:** Rolling 24h change $\ge \pm 15\%$.
6. **Healthy Funding Band:**
   - **Approved:** $-0.01\%$ to $+0.03\%$ funding rate.
7. **OI Accumulation Floor:**
   - **Approved:** $+1.5\%$ change over the 1H/4H window.

---

## 2. Scope & Boundaries
- **Approval Scope:** Sandbox reconstruction only. Cell 1 ancestor metrics only. Partial research metrics allowed. Dashboard visualization allowed.
- **Strict Boundaries:** No Cell 2, no labels, no model training, no trading logic, no recommendations, no live trading, and no strategy performance claims.

---

## 3. Approval Metadata
- **Approver:** Chris
- **Approval Code:** `PASS_PARTIAL_CELL1_RECONSTRUCTION_DATA_READY`
- **Execution Date:** 2026-06-07T17:36:53-04:00 (local time)
