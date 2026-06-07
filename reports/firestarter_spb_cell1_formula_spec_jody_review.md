# Cell 1 Formula Spec Jody Review

This document presents a formal governance review of the Cell 1 Formula Spec Lock Sheet (`reports/firestarter_spb_cell1_formula_spec_lock_sheet.md`) to determine if the proposed parameters and rules are safe for dashboard implementation.

---

## 1. Specification & Governance Answers

### 1. Are the proposed formula rules executable?
**YES.** The spec lock sheet converts qualitative legacy descriptions into precise mathematical expressions, lookback ranges, and threshold bands with explicit point allocations, bounding limits, and null handling rules. This can be directly translated into Python/Pandas logic.

### 2. Which rules are evidence-backed by source reports?
The summary-level components and weights are fully backed by the legacy reports:
- The raw score weighted blend: `raw_score = ER * 0.35 + FMLC * 0.35 + Flowprint_proxy * 0.30`.
- The score clamp ranges: ER [0, 10], FMLC [0, 10], Flowprint_proxy [0, 8].
- The constituent parent field categories (relative volume, price changes, range positions, EMA reclaims, funding rates, open interest changes, and taker volume ratios).

### 3. Which rules are proposed defaults rather than confirmed legacy logic?
The exact numeric bounds, lookback values, and point assignments listed in the Open Questions table are proposed defaults:
- **RVOL lookback:** 24 periods.
- **Liquidity Floor:** $10,000,000 USD daily volume.
- **Near Breakout Margin:** Within 1.0% of the 20-bar rolling high.
- **Clean Reclaim EMA:** Close above EMA21 with volume $> 1.2\times$ average.
- **Anti-Blowoff Governor:** $\pm 15\%$ price change.
- **Healthy Funding Band:** $-0.01\%$ to $+0.03\%$ funding rate.
- **OI Accumulation Floor:** $+1.5\%$ change over the window.

### 4. Which defaults are acceptable for sandbox reconstruction?
For a research sandbox, **all of the proposed defaults are acceptable as initial testing baselines**. They are standard quant signals that reflect the momentum-ignition and anti-blowoff properties described in the legacy scanner logs.

### 5. Which values require Chris approval?
All **7 parameters** listed in the Open Questions table require formal Chris review and approval before they can be locked for production or trading system calculations.

### 6. Does the spec allow partial Top 100 dashboard computation without inventing formulas?
**NO.** We cannot begin dashboard computation yet because the 7 threshold values are still unapproved proposed defaults. If we ran them on the dashboard now, we would be inventing parameters.
However, once Chris signs off on these defaults (or provides the legacy values), the spec *does* allow partial computation. The 98 standard symbols will compute using the capped 29-day derivatives history window, while the early windows and the 2 non-standard symbols will remain cleanly parent-gated/disabled.

---

## 2. Governance Verdict

```text
HOLD_NEEDS_CHRIS_FORMULA_DECISIONS
```

*Reason:* While the executable spec draft is logically complete and ready for code translation, the 7 open parameter questions must be reviewed and officially approved by Chris to ensure we do not invent arbitrary signals.
