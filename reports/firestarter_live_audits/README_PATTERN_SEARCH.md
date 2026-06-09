# Firestarter Live Audits Pattern Search

`search_ai_match_patterns.py` searches the derived
`reports\firestarter_live_audits\ai_match_index.csv` across the full Top100
universe. It is for flexible research fingerprints over the compact hourly
profile table.

## Input

`reports\firestarter_live_audits\ai_match_index.csv`

The script does not read raw 5m candles and does not mutate the index.

## Outputs

Each run writes three files under:

`reports\firestarter_live_audits\pattern_searches\`

- `<pattern_name>_matches.csv`
- `<pattern_name>_summary.md`
- `<pattern_name>_top_examples.csv`

With `--sync-drive`, those three files are copied to:

`G:\My Drive\Matrix Alpha\FirestarterOG\Live Audits\Pattern Searches\`

## Examples

```powershell
python scripts\firestarter_live_audits\search_ai_match_patterns.py --pattern-name smoke_x2_like --min-fmlc 7 --min-raw-score 7 --top-n 20

python scripts\firestarter_live_audits\search_ai_match_patterns.py --pattern-name smoke_hollow_weakness --max-flowprint 3 --max-raw-score 4 --top-n 20
```

## Supported Filters

- Date and symbol: `--start`, `--end`, `--symbol`
- Metric ranges: `--min-fmlc`, `--max-fmlc`, `--min-flowprint`,
  `--max-flowprint`, `--min-raw-score`, `--max-raw-score`, `--min-er`,
  `--max-er`
- Movement fingerprints: `--fmlc-rising-hours`, `--fmlc-falling-hours`,
  `--raw-score-rising-hours`, `--raw-score-falling-hours`,
  `--flowprint-rising-hours`, `--flowprint-falling-hours`, `--price-up-hours`,
  `--price-down-hours`, `--price-compression-hours`
- Price extension and recent-high research filters: `--prior-return-hours`,
  `--min-prior-return-pct`, `--near-recent-high-hours`,
  `--max-distance-from-recent-high-pct`, `--forward-return-hours`,
  `--max-forward-return-pct`
- Range-position research filters: `--upper-range-hours`,
  `--min-close-position-in-range`
- Tags and quality: `--primary-event-type`, `--secondary-tag-contains`,
  `--data-quality-exclude`
- Output controls: `--top-n`, `--sync-drive`
- Optional event clustering: `--cluster-hours`

`--price-compression-hours` uses a compact fixed definition: over the requested
hour window, the close range must be no more than 1.0% of the latest close in
that window.

The prior-return filter compares the current close to the close N hours earlier
for the same symbol. The recent-high filter computes the highest close over the
current/prior N-hour symbol window and requires current close to be within the
requested percentage distance from that high. The forward-return filter compares
the close N hours after the current row to the current close. These are
research filters only and do not mutate the source index.

The range-position filter computes the recent low and high over the
current/prior N-hour close window for each symbol, then calculates
`(current_close - recent_low) / (recent_high - recent_low)`. Rows with an
unavailable or zero-width range are excluded from this filter. A value of `0.70`
means the current close is in the upper 30% of its recent close range.

`--cluster-hours` groups repeated matching rows for the same symbol into one
event when consecutive matching rows are within the supplied number of hours.
When clustering is enabled, the run also writes `<pattern_name>_events.csv` with
one row per clustered event:

- `symbol`
- `event_start`
- `event_end`
- `match_count`
- `best_timestamp`
- `best_raw_score`
- `max_fmlc`
- `min_er`
- `min_flowprint`
- `first_close`
- `last_close`

Default behavior is unchanged when `--cluster-hours` is not supplied.

## Boundary

This is a research-only pattern search. Matches are setup hypotheses / profile
behavior candidates only. They are not signals, strategies, entries, exits,
trades, alerts, validated edge, or Cell 2 labels.
