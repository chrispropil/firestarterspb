# Firestarter Cell 1 Formula Spec Lock Sheet

This locked specification report converts the summary-level Firestarter Cell 1 ancestor logic into an executable rule and decision table. This serves as the design baseline for future metric calculation, pending Chris/Jody approval.

---

## 1. ER (Ignition/Momentum Pressure) Executable Spec Draft

### Input Fields
- `open`, `high`, `low`, `close` (prices)
- `volume` (volume in base asset)
- `quote_asset_volume` (volume in quote asset)
- `trades` (trade count)

### Lookback Windows
- **RVOL 1H Average Volume:** 24-hour rolling average (24 bars on 1H grid).
- **RVOL 4H Average Volume:** 24-bar rolling average (96 hours on 4H grid).
- **24h Price Change:** 24 bars on 1H grid, 6 bars on 4H grid.
- **Breakout High:** 20-bar rolling high.

### Threshold Bands & Points Allocation
ER is a composite score of volume pressure, price momentum, and breakout state:
1. **Relative Volume (RVOL) Score (Max 4 points):**
   - $\text{RVOL} > 2.5$: +4 points
   - $1.8 < \text{RVOL} \le 2.5$: +3 points
   - $1.2 < \text{RVOL} \le 1.8$: +2 points
   - $0.8 < \text{RVOL} \le 1.2$: +1 point
   - $\text{RVOL} \le 0.8$: 0 points
2. **Breakout State (`near_breakout`) Score (Max 3 points):**
   - If `close` is within 1% of the 20-bar rolling high: +3 points
   - If `close` is within 2.5% of the 20-bar rolling high: +1 point
   - Otherwise: 0 points
3. **Price Reclaim (`clean_reclaim`) Score (Max 3 points):**
   - If `close` is above the 21-period Exponential Moving Average (EMA21) and the candle range (`high` - `low`) is above the 10-bar average range: +3 points
   - Otherwise: 0 points

### Clamp Range
- Output score is clamped between **0 and 10** inclusive.

### Missing-Data Behavior
- If any required candle price or volume field is missing or contains nulls, the ER score is returned as **null/unavailable** (parent-gated).

---

## 2. FMLC (Governor / Structural Quality) Executable Spec Draft

### Input Fields
- `close`, `high`, `low` (prices)
- `volume` (liquidity)
- `fundingRate` (funding cadence)
- `sumOpenInterest` (open interest)
- `longShortRatio` (positioning)

### Liquidity/Volume Requirements
- **Liquidity Floor:** The rolling 24-hour trading volume (in USD or quote asset) must exceed **$10,000,000 USD** to register FMLC scoring. If below the floor, FMLC is hard-coded to **0 points** (gated for insufficient liquidity).

### Range-Position Formula
- **4H 50-bar Range Position:**
  $$\text{RP}_{50} = \frac{\text{close} - \text{low}_{50}}{\text{high}_{50} - \text{low}_{50}} \times 10$$
- **20-bar Range Position:**
  $$\text{RP}_{20} = \frac{\text{close} - \text{low}_{20}}{\text{high}_{20} - \text{low}_{20}} \times 10$$
- **Composite Range Position Score:** $0.5 \times \text{RP}_{50} + $0.5 \times \text{RP}_{20}$.

### Trend/Reclaim Conditions
- **Above Trend (`above_4h_trend`):**
  - If `close` is above the 50-period simple moving average (SMA50): +3 points.
  - If `close` is below the SMA50 but above the EMA21: +1 point.
  - Otherwise: 0 points.

### Anti-Blowoff Governor
- **Governor Trigger:** If the rolling 24h price change exceeds **+15%** (overextended) or falls below **-15%** (capitulating), FMLC is penalized by subtracting **4 points** from the structural score.

### Point Allocation
FMLC is a composite of structural position and trend compliance:
1. **Range Position Score:** Max 5 points.
2. **Trend Score:** Max 3 points.
3. **Funding Rate Score:** Max 2 points.
   - If `fundingRate` $\le 0.01\%$ (neutral/disbelieving): +2 points.
   - If `fundingRate` $> 0.01\%$ and $\le 0.05\%$: +1 point.
   - If `fundingRate` $> 0.05\%$ (overheated leverage): 0 points.

### Clamp Range
- Output score is clamped between **0 and 10** inclusive.

### Missing-Data Behavior
- If funding rate or open interest fields are missing (e.g., in the early partial window or for custom symbols), the FMLC score is returned as **null/unavailable** (parent-gated).

---

## 3. Flowprint_proxy (Participation Proxy) Executable Spec Draft

### Input Fields
- `volume`, `quote_asset_volume`, `number_of_trades`
- `taker_buy_base_asset_volume`, `taker_buy_quote_asset_volume`
- `sumOpenInterest`
- `fundingRate`

### OI Availability & Change Calculation
- **OI Availability:** `sumOpenInterest` must be present. If missing, Flowprint_proxy returns **null/unavailable** (no fallback or forward-fill allowed).
- **OI Change:**
  $$\text{OI\_Change}_{1h} = \frac{\text{sumOpenInterest}_t - \text{sumOpenInterest}_{t-1}}{\text{sumOpenInterest}_{t-1}}$$

### Funding Band Quality
- **Premium Score (Max 2 points):**
  - If $-0.01\% \le \text{fundingRate} \le +0.03\%$ (Healthy/Normal Premium): +2 points.
  - If $\text{fundingRate} < -0.01\%$ or $\text{fundingRate} > +0.03\%$: 0 points.

### Taker Buy/Sell Pressure
- **Taker Volume Ratio:**
  $$\text{Taker\_Ratio} = \frac{\text{taker\_buy\_base\_asset\_volume}}{\text{volume}}$$
- **Taker Score (Max 2 points):**
  - $\text{Taker\_Ratio} \ge 0.52$ (Dominant Buyer Flow): +2 points.
  - $0.48 \le \text{Taker\_Ratio} < 0.52$ (Neutral Flow): +1 point.
  - $\text{Taker\_Ratio} < 0.48$ (Seller Flow): 0 points.

### Volume & OI Participation Score
1. **RVOL 1H Score (Max 2 points):**
   - If $\text{RVOL} > 1.5$: +2 points.
   - If $1.0 < \text{RVOL} \le 1.5$: +1 point.
   - Otherwise: 0 points.
2. **OI Accumulation Score (Max 2 points):**
   - If $\text{OI\_Change}_{1h} > +1.5\%$: +2 points.
   - If $0\% < \text{OI\_Change}_{1h} \le +1.5\%$: +1 point.
   - Otherwise: 0 points.

### Clamp Range
- Output score is clamped between **0 and 8** inclusive.

### Missing-Data Behavior
- If any volume, taker volume, OI, or funding field is missing, Flowprint_proxy returns **null/unavailable** (parent-gated).

---

## 4. raw_score Executable Spec Draft

### Exact Weighted Blend
raw_score is calculated as:
$$\text{raw\_score} = \text{ER} \times 0.35 + \text{FMLC} \times 0.35 + \text{Flowprint\_proxy} \times 0.30$$

### Required Normalized Ranges
Before blending, the component outputs are:
- $\text{ER} \in [0, 10]$
- $\text{FMLC} \in [0, 10]$
- $\text{Flowprint\_proxy} \in [0, 8]$

*Note on Blending:* The maximum unscaled blended score is $10 \times 0.35 + 10 \times 0.35 + 8 \times 0.30 = 9.4$. To normalize the final `raw_score` to a standard $0$ to $10$ scale, the result is divided by $0.94$:
$$\text{raw\_score\_normalized} = \frac{\text{raw\_score}}{0.94}$$

### Missing Metric Behavior
- **Strict Gating:** If any of the three inputs (`ER`, `FMLC`, or `Flowprint_proxy`) is **null/unavailable**, the final `raw_score` is returned as **null/unavailable** (fail-closed). No partial score is computed.

### Clamp Range
- Output normalized score is clamped between **0 and 10** inclusive.

---

## 5. Open Questions Table

| Field Name | Current Evidence | Proposed Default | Risk | Chris/Jody Approval Needed |
|---|---|---|---|---|
| **RVOL Lookback Window** | Summary logs mention averages but omit the length. | **24 periods** (24 hours on 1H grid, 96 hours on 4H grid). | Short windows increase noise; long windows delay trend pivot recognition. | **Yes** |
| **Liquidity Floor Threshold** | Replay files show token-specific gates. | **$10,000,000 USD** daily rolling volume. | May exclude newly listed low-cap tokens with high momentum. | **Yes** |
| **Near Breakout Threshold** | Mentions close near breakout highs. | **Within 1.0%** of the 20-period rolling high. | Too narrow misses early breakouts; too wide creates false breakout flags. | **Yes** |
| **Clean Reclaim EMA** | Mentions close above trend line. | Close above **EMA21** with volume $> 1.2\times$ average. | False reclaims on low volume can generate noisy scores. | **Yes** |
| **Anti-Blowoff Governor** | Mentions anti-blowoff on large changes. | **$\pm 15\%$** price change in 24 hours. | May penalize valid momentum runaways during heavy trends. | **Yes** |
| **Healthy Funding Band** | Mentions premium state governors. | **$-0.01\%$ to $+0.03\%$** funding rate. | Shifts in market baseline regime might render this band overly restrictive. | **Yes** |
| **OI Accumulation Floor** | Mentions OI presence scoring. | **$+1.5\%$** change over the 1H/4H window. | Noise in contract rollover periods could flag false accumulation. | **Yes** |

---

## 6. Implementation Decision

```text
READY_FOR_CHRIS_REVIEW_ONLY
```

*Reason:* The draft executable rule set captures all ancestor families, normalization parameters, and gating rules. However, implementation is strictly blocked until Chris or Jody reviews the open questions table and locks the proposed default values.
