# Firestarter Optimizer Candidate State Monitor Report

Run UTC: 2026-06-14T03:57:49Z

## Observation-Only Boundary

This run is observation-only. The emitted states are evidence labels only; they are not trade commands, exclusion rules, or automatic rule changes.

## Input

- Input mode: `explicit`
- Input path: `C:\Users\User\Documents\Firestarter SPB\reports\firestarter_optimizer\candidate_tickets.jsonl`
- Dry run: `False`
- Candidate-ticket rows read: `644`
- Bad JSONL lines skipped: `0`

## Outputs

- Active snapshot: `C:\Users\User\Documents\Firestarter SPB\reports\firestarter_optimizer\active_candidates.jsonl`
- Append-only state events: `C:\Users\User\Documents\Firestarter SPB\reports\firestarter_optimizer\candidate_state_events.jsonl`
- Expired or changed candidates: `C:\Users\User\Documents\Firestarter SPB\reports\firestarter_optimizer\expired_or_changed_candidates.jsonl`
- Markdown report: `C:\Users\User\Documents\Firestarter SPB\reports\firestarter_optimizer\update_candidate_states_report.md`

## Row Counts

- Active candidate rows: `101`
- State event rows prepared this run: `101`
- Expired or changed rows prepared this run: `0`

## Lifecycle State Distribution

- `NEW`: `20`
- `PERSISTENT_HANGER`: `81`

## Data Quality Distribution

- `DATA_GAP_PARTIAL`: `101`

## Action Label Distribution

- `SHORT_HANGER_REVIEW_DATA_GAP`: `101`

## Direction Bias Distribution

- `AVOID_LONG`: `63`
- `SHORT_REVIEW`: `38`

## Signal Family Distribution

- `SHORT_HANGER`: `101`

## Data Gap Fields Distribution

- `price_position`: `101`

## Missing Fields

- `(none)`: `0`

## Assumptions

- Stable grouping prefers `symbol + direction_bias + signal_family`, then `candidate_id`, then source line fallback.
- Persistence threshold: `3` observations or `15.0` minutes.
- Micro-move threshold: `0.3%` favorable movement.
- Breakout/collapse threshold: `2.0%` favorable or `2.0%` adverse directional movement.
- Chop threshold: `0.75%` both favorable and adverse directional movement.
- `max_favorable_pct` and `max_adverse_pct` are directional magnitudes based on `direction_bias`.
- The script only reads candidate-ticket JSONL plus its own previous active snapshot; it does not read or mutate raw scanner, history, Bitget, ML, Slack, n8n, Google Drive, or rule files.
