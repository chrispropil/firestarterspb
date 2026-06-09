# Firestarter Live Audits Drive Sync

This helper copies the latest derived AI Match Index artifacts into Google Drive
so they are easy to access from ChatGPT through Drive.

## Source Files

- `reports\firestarter_live_audits\ai_match_index.csv`
- `reports\firestarter_live_audits\ai_match_index_summary.md`

## Drive Target

`G:\My Drive\Matrix Alpha\FirestarterOG\Live Audits\AI Match Index\`

## Drive Output Files

- `ai_match_index_latest.csv`
- `ai_match_index_summary_latest.md`
- `ai_match_index_manifest.md`

## Run

From the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\firestarter_live_audits\sync_ai_match_index_to_drive.ps1
```

## Behavior

The script creates the Drive target folder if it is missing, fails clearly if the
derived CSV or summary is missing, copies the latest derived files, and writes a
manifest with sync timestamp, source paths, target paths, and file sizes.

It does not modify source files, scanner files, dashboard HTML, raw data, or
market data files. The generated `ai_match_index.csv` remains untracked/ignored.
