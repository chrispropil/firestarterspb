param(
    [string]$DriveTargetFolder = "G:\My Drive\Matrix Alpha\FirestarterOG\Live Audits\AI Match Index"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..")
$SourceCsv = Join-Path $RepoRoot "reports\firestarter_live_audits\ai_match_index.csv"
$SourceSummary = Join-Path $RepoRoot "reports\firestarter_live_audits\ai_match_index_summary.md"

$TargetCsv = Join-Path $DriveTargetFolder "ai_match_index_latest.csv"
$TargetSummary = Join-Path $DriveTargetFolder "ai_match_index_summary_latest.md"
$TargetManifest = Join-Path $DriveTargetFolder "ai_match_index_manifest.md"

if (-not (Test-Path -LiteralPath $SourceCsv -PathType Leaf)) {
    throw "Missing required source file: $SourceCsv. Build ai_match_index.csv before syncing."
}

if (-not (Test-Path -LiteralPath $SourceSummary -PathType Leaf)) {
    throw "Missing required source file: $SourceSummary. Build ai_match_index_summary.md before syncing."
}

New-Item -ItemType Directory -Path $DriveTargetFolder -Force | Out-Null

Copy-Item -LiteralPath $SourceCsv -Destination $TargetCsv -Force
Copy-Item -LiteralPath $SourceSummary -Destination $TargetSummary -Force

$SourceCsvItem = Get-Item -LiteralPath $SourceCsv
$SourceSummaryItem = Get-Item -LiteralPath $SourceSummary
$TargetCsvItem = Get-Item -LiteralPath $TargetCsv
$TargetSummaryItem = Get-Item -LiteralPath $TargetSummary
$SyncTimestampUtc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

$Manifest = @"
# Firestarter Live Audits - AI Match Index Drive Manifest

## Sync

| Field | Value |
|---|---|
| sync_timestamp_utc | ``$SyncTimestampUtc`` |
| source_csv | ``$($SourceCsvItem.FullName)`` |
| source_csv_bytes | ``$($SourceCsvItem.Length)`` |
| target_csv | ``$($TargetCsvItem.FullName)`` |
| target_csv_bytes | ``$($TargetCsvItem.Length)`` |
| source_summary | ``$($SourceSummaryItem.FullName)`` |
| source_summary_bytes | ``$($SourceSummaryItem.Length)`` |
| target_summary | ``$($TargetSummaryItem.FullName)`` |
| target_summary_bytes | ``$($TargetSummaryItem.Length)`` |
| manifest_path | ``$TargetManifest`` |

## Boundary

This sync copies derived report artifacts only. It does not modify source report files, scanner files, dashboard HTML, raw data, or market data files.
"@

Set-Content -LiteralPath $TargetManifest -Value $Manifest -Encoding UTF8

Write-Host "Synced AI Match Index to Drive."
Write-Host "target_folder=$DriveTargetFolder"
Write-Host "csv=$TargetCsv"
Write-Host "summary=$TargetSummary"
Write-Host "manifest=$TargetManifest"
