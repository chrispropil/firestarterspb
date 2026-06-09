# Firestarter Core88 Missing 1-Month 5m Pull Audit

## Status

| Check | Result |
|---|---|
| Mode | LIVE_PULL |
| Missing Symbols Requested | 51 |
| Active Binance USDT Perps Checked | 531 |
| Successful Pulls | 45 |
| Skipped Inactive Symbols | 6 |
| Failed Pulls | 0 |
| Total Rows Downloaded | 388800 |
| Raw Data Committed | NO |
| Formula Changes | NO |
| Cell 2 / Signal Labels | NO |
| Automation Daemon | NO |

## Output

- Data directory: `data/research/binance_core88_missing_1month`
- Manifest CSV: `reports/firestarter_core88_missing_1month_pull_manifest.csv`

## Boundary

This puller only collects public Binance USDT perpetual 5m kline history for the missing Core88 coverage set. It does not alter formulas, scoring logic, labels, execution rules, or live systems.

## Verdict

PASS_CORE88_MISSING_1MONTH_5M_PULL_COMPLETE
