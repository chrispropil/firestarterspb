# Binance Cell 1 Source Gate

STATUS: PRODUCER_READY_FOR_CLOUD_VALIDATION

## Decision

The Bitget limited trial produced enough evidence for the current purpose. The active source should move toward Binance because the local research viewer and historical Binance artifacts are Binance-oriented.

## Scope in this branch

- Add Binance Cell 1 producer config.
- Add Binance Cell 1 metric producer.
- Keep the governed 25-symbol object unchanged.
- Keep output compatibility with the existing metric snapshot adapter.

## Files

- `configs/cloud_cell1_metric_producer_binance_v1.json`
- `scripts/automation/cloud_cell1_metric_producer_binance_v1.py`
- `reports/cloud_pattern_watch/v1/binance_cell1_source_gate.md`

## Validation plan

1. Pause the Bitget limited trial cron.
2. Sync this branch or merged main to cloud.
3. Compile the Binance producer.
4. Run Binance dry-run.
5. Run one Binance manual build.
6. Run existing snapshot adapter write.
7. Confirm at least 20 accepted symbols.
8. Only then wire scheduled pulling to the Binance producer.

## Safety

No Pattern Watch send is activated.
No n8n flow is activated.
No trading execution is added.
No symbol-list mutation is included.
