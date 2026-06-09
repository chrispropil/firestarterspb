# Firestarter Live Audits

## Status

Research-only audit lane.

## Definition

Firestarter Live Audits is the active visual/profile audit lane for FirestarterOG setup hypotheses across the Binance Top100 research dataset.

"Live" means active research review of current or recently generated profile evidence. It does not mean live trading, alerts, signals, entries, exits, execution, or Cell 2 promotion.

## Purpose

Use this lane to organize:

- visual chart review
- symbol-specific behavior notes
- Top100 setup hypothesis review
- profile branch comparison
- false-positive review
- AI-readable match-index exports
- bounded review packets

## Current source context

Primary working dataset:

```text
C:\firestarterspb\data\research\binance_top100_excluding_existing_5_1month\
C:\firestarterspb\data\research\binance_top100_derivatives_context_1month\
```

Primary viewer:

```text
reports/html/top100_dashboard/index.html
reports/html/top100_dashboard/symbols/<SYMBOL>.html
```

Primary research fields:

```text
er
fmlc
flowprint
raw_score
primary_event_type
secondary_tags
data_quality_flags
```

## Approved wording

Use:

- setup hypothesis
- profile branch
- visual review
- candidate
- review queue
- reference case
- false-positive control
- metric extraction
- research-only audit

Avoid:

- strategy
- signal
- entry
- exit
- trade
- buy
- sell
- alpha
- proven edge
- live execution

## Profile branch names

Current review branches:

```text
X2_CANDIDATE
HOLLOW_BREAKOUT
FAKE_RECOVERY
DOMINO_DETERIORATION
ENTRY_C_LIKE_RECOVERY
NIF_CATALYST_QUALITY_AUDIT
```

## Visual labels

Use these labels for manual chart review:

```text
X2_VISUAL_CONFIRMED
X2_VISUAL_WEAK
X2_FALSE_POSITIVE
X2_NEEDS_MORE_DATA
HOLLOW_BREAKOUT_VISUAL_CONFIRMED
HOLLOW_BREAKOUT_WEAK
DOMINO_VISUAL_CONFIRMED
DOMINO_WEAK
FAKE_RECOVERY_FAILURE_CANDIDATE
FAKE_RECOVERY_TO_X2_ONSET_CANDIDATE
INSUFFICIENT_DATA
```

## Classifications

Use these classifications after comparing against other symbols:

```text
BROAD_PATTERN_CANDIDATE
PROFILE_FAMILY_CANDIDATE
SYMBOL_SPECIFIC_CANDIDATE
REGIME_SPECIFIC_CANDIDATE
REFERENCE_CASE
FALSE_POSITIVE_PATTERN
INSUFFICIENT_DATA
NEEDS_METRIC_EXTRACTION
```

## Required boundary

No profile observation in this lane is a trading recommendation or validated system rule. Every finding remains research-only until later metric extraction and audit infrastructure prove otherwise.
