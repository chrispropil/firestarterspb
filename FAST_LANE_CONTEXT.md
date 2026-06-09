# FAST LANE CONTEXT LOCK

## System Identity
Fast Lane is a dual-mode Bitget USDT perpetual futures research system.

It supports:
1. X1 Tactical / High-Leverage Mode
2. X2 Position / Low-Leverage Swing Mode

It is not only a scalping system and not only a position system.

## X1 Tactical / High-Leverage Mode
Purpose:
Fast trades, tight stops, quick validation, quick invalidation.

Research question:
Can the setup move in the intended direction quickly before a tight stop is hit?

Future labels:
- label_x1_long_0_75s_2t_4h
- label_x1_long_1s_3t_8h
- label_x1_long_1_5s_4t_24h
- label_x1_short_0_75s_2t_4h
- label_x1_short_1s_3t_8h
- label_x1_short_1_5s_4t_24h

## X2 Position / Low-Leverage Swing Mode
Purpose:
Lower leverage, wider structure, slower entries, 24h-72h+ follow-through.

Research question:
Is this a clean structural setup that can trend without being late or toxic?

Future labels:
- label_x2_long_3s_8t_24h
- label_x2_long_5s_12t_48h
- label_x2_long_8s_15t_72h
- label_x2_short_3s_8t_24h
- label_x2_short_5s_12t_48h
- label_x2_short_8s_15t_72h

## Current Research Candidates
1. candidate_001_three_gate_swing_long
   - mode: X2_POSITION
   - direction: long
   - rule idea:
     - feat_cross_sectional_return_rank_1h < 0.90
     - feat_volume_rvol_4h < 1.5

2. candidate_002_red_flag_short
   - mode: X1_TACTICAL
   - direction: short
   - rule idea:
     - feat_cross_sectional_return_rank_1h > 0.98
     - feat_volume_rvol_4h > 3.0
     - feat_close_position_in_bar < 0.5

3. candidate_003_beta_decoupling
   - mode: X2_CONTEXT
   - direction: long context boost
   - not a hard entry rule

## Hard Rules
- feat_ columns must be point-in-time clean.
- label_ columns may use future data.
- Never use label_ columns as features.
- Do not trust the 1,331x / 1,569x ratios until audited.
- Do not build signal_discovery.py yet.
- Do not build ML yet.
- Do not deploy live trading logic.
- Do not modify scanner unless explicitly requested.
- Do not run OHLCV backfill unless explicitly requested.

## Priority Build Order
1. candidate_rules.yaml
2. build_triple_barrier_labels.py with X1 and X2 label families
3. audit_candidate_rules.py
4. build_alpha_adjusted_swing_labels.py
5. build_traverse_time_features.py
6. build_volume_truth_features.py
7. build_research_dataset_v2.py
8. only later: signal_discovery.py

## Validation Requirements
Any candidate must be tested with:
- effective sample size correction
- block bootstrap
- shuffle/random-label test
- inverted-filter test
- symbol concentration
- leave-one-symbol-out
- time-slice stability
- threshold sensitivity
- alpha-adjusted labels
- triple-barrier labels
- purged/embargoed validation where feasible

## Current Tardis Status
Tardis pipeline works technically.
Derivative ticker files now cover 50 symbols and 6 dates.
Liquidations mainly cover BTC/ETH.
Tardis Gate 3 is useful for engineering and later context, but not enough for final statistical validation unless we get contiguous data.
