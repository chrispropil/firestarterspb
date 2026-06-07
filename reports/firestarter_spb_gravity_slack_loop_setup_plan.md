# Firestarter SPB Gravity Slack Loop Setup Plan

## Objective
Establish a secure, read/write integration between Gravity (local ODIN environment) and the `#matrix-alpha-gravity` Slack channel without compromising tokens or violating source-control safety.

## 1. Required Slack Bot Scopes
The Slack application/bot requires strictly the following OAuth scopes to function:
- `channels:read` (To view public channel information)
- `channels:history` (To read messages in the channel)
- `chat:write` (To post completion reports and status updates)

## 2. Channel Invitation Requirement
The generated Slack bot must be explicitly invited to the target channel.
- **Channel Name:** `#matrix-alpha-gravity`
- **Channel ID:** `C0B7HJLTDCZ`
- **Action Required:** In Slack, type `/invite @<YourBotName>` in the target channel.

## 3. Proposed Script Paths
We will create dedicated Python scripts isolated within a new directory module:
- **Reader Script:** `scripts/gravity_slack/slack_read_latest.py`
  *(Pulls the latest instructions or confirmations from the channel.)*
- **Writer Script:** `scripts/gravity_slack/slack_post_report.py`
  *(Pushes short execution status reports to the channel.)*

## 4. Local Windows Token Setup
- **Strict Boundary:** We will exclusively use local environment variables.
- **Variable Name:** `SLACK_BOT_TOKEN`
- **Setup Method (Windows PowerShell):**
  Create a local `.env` file in the project root containing:
  `SLACK_BOT_TOKEN="xoxb-your-secret-token-here"`
  The python scripts will use `python-dotenv` or standard `os.environ` to load this securely at runtime.

## 5. Dry-Run Test Command
Once the token is set and the scripts are built, the integration will be validated using:
```powershell
python scripts/gravity_slack/slack_post_report.py --message "Gravity Slack connection dry-run successful."
```

## 6. Safety Boundaries
1. **No Tokens Printed:** Gravity will never output the value of `SLACK_BOT_TOKEN` to stdout or chat.
2. **No Secrets Saved in Code:** Scripts will rely 100% on `os.environ.get('SLACK_BOT_TOKEN')`.
3. **No GitHub Commit of `.env`:** A `.gitignore` rule has been implemented to exclude `.env` and token files from git tracking.
4. **No Raw Market Data / Trading Limits:** The Slack integration is strictly for workflow signaling and completion reports, not for live execution signaling or raw data dumping.

## Gate Check
This is a plan only. Do not execute or create the python scripts until approved.
