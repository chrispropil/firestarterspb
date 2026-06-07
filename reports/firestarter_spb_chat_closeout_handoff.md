# Firestarter SPB Chat Closeout Handoff

## Status
- Active repo: `chrispropil/firestarterspb`
- Local sandbox: `C:\firestarterspb`
- Branch: `main`
- Raw local data folder remains untracked: `data/research/binance_5_token_1month/`
- No raw CSV/JSON files are committed.
- Cell 2 remains blocked.

## Completed gates
- Binance 5-token 1-month data pull completed locally.
- Audit artifacts committed.
- Reconstruction readiness passed with partial OI/top-trader warning.
- Formula reconstruction plan committed.
- Formula spec confirmation committed.
- Cell 1 computation plan committed.
- Cell 1 dry-run plan committed.
- Cell 1 dry-run audit committed.
- Paid vendor evaluation committed.
- CoinGlass and Tardis readiness reports committed.
- Tardis sample request pack created locally and should be committed if not already done.
- Binance Top 100 one-month expansion plan created locally and should be committed if not already done.

## Key decisions
- Continue free Binance one-month testing before buying paid data.
- Expand to approximately top 100 Binance USDT perpetuals for broad profiling.
- Paid data is justified later, but not required yet.
- Tardis is the preferred long-term forensic/DNA Tape source if ODIN capacity and cost are acceptable.
- CoinGlass is useful as a lower-cost derivatives context source.
- Legacy Cell 1 source is authoritative for ER/FMLC/Flowprint ancestor logic.
- Later starter Colab snippets are ingestion/reference only, not the scoring source.

## Current next lane
`FIRESTARTER SPB BINANCE TOP 100 ONE-MONTH EXPANSION`

Goal: use free Binance public futures data to profile the top 100 active USDT perpetuals across a clean one-month window before paid-data purchase.

Expected next task:
- Commit the Top 100 expansion plan if not already committed.
- Then create a Top 100 data-pull script plan.
- Then execute only after gate approval.

## Boundaries
- No Cell 2.
- No labels.
- No model training.
- No live trading.
- No trade recommendations.
- No secrets in chat, Slack, Notion, Drive, GitHub, or logs.
- No raw market data committed.
- Slack token incident was cleaned locally, but token rotation remains a manual required security step if not already completed.

## Loop rules
- `cc` means check Slack.
- Once Slack/Codex/Antigravity loop is established, use it by default.
- Chat response style: short explanation, then next Codex/Antigravity lane only.
