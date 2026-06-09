# Firestarter Core 88 Watchlist Selection Rationale

**Status:** Research-only universe update  
**Project:** Matrix Alpha / FirestarterSPB / Top 100 Evidence Viewer  
**Created:** 2026-06-08  
**Repository:** `chrispropil/firestarterspb`  
**Config file:** `configs/firestarter_core88_binance_usdt_symbols.txt`

---

## 1. Purpose

This document locks the rationale for replacing the blind Binance Top 100 universe with a curated Firestarter Core 88 universe.

The previous Top 100 route was too exposed to small speculative names, unstable volatility, thin history, and noisy one-off movers. The Core 88 universe is intended to preserve volatility while improving research quality, chart readability, historical comparability, and symbol-profile consistency.

---

## 2. Research Boundary

This is a research-only universe definition.

Blocked:
- No trading logic
- No buy/sell recommendations
- No live scanner hooks
- No production daemon
- No Cell 2 implementation
- No automated labels
- No raw dataset commits
- No strategy validation claims

Allowed:
- Symbol universe definition
- Viewer routing updates
- Evidence-viewer data pulls
- Visual inspection
- Profile-first research
- DNA tape planning criteria
- Reports-only forensic review

---

## 3. Selection Thesis

The target universe should contain assets that are:

1. Liquid enough to build useful history.
2. Volatile enough to expose Firestarter behavior.
3. Tradable enough for profile research.
4. Less polluted by tiny speculative one-day movers.
5. Broad enough to cover major narratives: L1/L2, DeFi, AI, RWA, infra, gaming, meme-beta, privacy, old majors, and high-beta midcaps.

BTCUSDT and ETHUSDT remain in the universe as market-regime anchors, not as primary target symbols. The user considers BTC and ETH too expensive for the intended active research style, but they remain useful for market-context alignment.

---

## 4. Intended Viewer Change

The Top 100 Evidence Viewer should be migrated toward a Core 88 Evidence Viewer path.

Primary config:

```text
configs/firestarter_core88_binance_usdt_symbols.txt
```

Viewer goal:

```text
Price panel on top
Metrics panel in middle
ER panel on bottom
One-screen stacked forensic inspection layout
```

The viewer should use the Core 88 list as the controlled universe before expanding back to 100.

---

## 5. Core 88 Governance Rule

Do not automatically expand back to 100.

The next 12 symbols should only be added after:

1. Binance route availability check.
2. Data completeness check.
3. Viewer load validation.
4. Category-gap review.
5. Manual chart review.

---

## 6. DNA Tape Planning Implication

The Core 88 should become the first candidate universe for DNA tape planning.

DNA tape pull criteria should be planned only after:

1. Core 88 synced data pull is complete.
2. Evidence Viewer successfully loads the new universe.
3. ER/FMLC/Flowprint behavior can be visually reviewed.
4. Shadow trigger candidates are manually marked.
5. Storage/runtime risk is reviewed.

---

## 7. Current Locked Status

```text
FIRESTARTER_CORE88_UNIVERSE_CREATED
TOP100_REPLACEMENT_DIRECTION_ACCEPTED
VIEWER_MIGRATION_PENDING
DNA_TAPE_PULL_CRITERIA_PENDING_VIEWER_VALIDATION
RESEARCH_ONLY_BOUNDARIES_LOCKED
```
