# FirestarterLive Candidate Fingerprint Registry

## fmlc_hanger_local_review_003_tight_cluster24

Status: CANDIDATE_FINGERPRINT  
Validation: NOT_PROVEN_EDGE  
Mode: X2_POSITION_RESEARCH  
Created: 2026-06-10  
Source index: reports/firestarter_live_audits/ai_match_index.csv  
Generated outputs: reports/firestarter_live_audits/pattern_searches/  
Drive sync: NOT USED  

### Purpose

Detects a possible FMLC hanger profile: price holding high in its recent range after a prior move, with high FMLC but low ER, weak Flowprint, and low raw score.

This is a research-only setup fingerprint. It is not a signal, trade setup, alert, strategy, entry, exit, or validated edge.

### Exact Pattern Command

```powershell
C:\Users\User\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\firestarter_live_audits\search_ai_match_patterns.py `
  --pattern-name fmlc_hanger_local_review_003_tight_cluster24 `
  --start 2026-05-17 `
  --end 2026-06-07 `
  --upper-range-hours 72 `
  --min-close-position-in-range 0.80 `
  --prior-return-hours 72 `
  --min-prior-return-pct 10 `
  --min-fmlc 8 `
  --max-er 1.5 `
  --max-flowprint 2 `
  --max-raw-score 3.5 `
  --cluster-hours 24 `
  --top-n 50
```
