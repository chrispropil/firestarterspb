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
- Tags and quality: `--primary-event-type`, `--secondary-tag-contains`,
  `--data-quality-exclude`
- Output controls: `--top-n`, `--sync-drive`

`--price-compression-hours` uses a compact fixed definition: over the requested
hour window, the close range must be no more than 1.0% of the latest close in
that window.

## Boundary

This is a research-only pattern search. Matches are setup hypotheses / profile
behavior candidates only. They are not signals, strategies, entries, exits,
trades, alerts, validated edge, or Cell 2 labels.
