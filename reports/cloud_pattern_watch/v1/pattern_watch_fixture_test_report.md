# Pattern Watch Fixture Test Report

STATUS: PLANNED_FIXTURE_GATE_READY

## Scope

This fixture gate validates Pattern Watch candidate detection and alert formatting without waiting for live market rows to produce an FMLC Hanger.

## Files

- `scripts/automation/cloud_pattern_watch_v1.py`
- `configs/cloud_pattern_watch_v1_fixture.json`

## Fixture Expectation

Expected candidate count: `1`

Expected label: `FMLC Hanger`

Expected pattern key: `fmlc_hanger`

Expected candidate symbol: `BTCUSDT`

## Safety

- Scheduler remains inactive.
- N8N remains inactive.
- Trading execution remains false.
- Scoring changes remain false.
- Raw data mutation remains false.
- Fixture data is not live market data.

## Manual Verification

The fixture gate should be run manually from the cloud shell after this branch is merged and pulled.

Dry-run should produce one candidate and no notification send.

Fixture send should produce one research notification only when manually requested by the operator.
