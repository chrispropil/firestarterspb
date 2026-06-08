# Matrix Alpha Persona Registry

STATUS: ACTIVE
VERSION: 2026-06-08-v1

## Purpose
This folder is the GitHub source-of-truth layer for Matrix Alpha persona definitions.

Personas are stored here so agent behavior can be referenced consistently across GitHub, Notion, Google Drive, Slack reports, and future OpenAI Agents SDK traces.

## Current Persona Files
- `maya.md` — Think Tank Director / Hypothesis Mapper
- `jody.md` — Lead R&D Scientist / Logic Critic
- `bob.md` — Build Coordinator / Approval Gate / Filing Operator
- `steve.md` — CEO / Executive Oversight
- `red_team.md` — Adversarial Risk Reviewer

## Source-of-Truth Rule
GitHub persona files are the technical source of truth.

Notion pages are the readable command library.

Google Drive docs are the journal/archive backup.

OpenAI traces are the audit trail and should reference persona name/version/source only.

## Trace Metadata Standard
Traces should use metadata like:

```json
{
  "system": "Matrix Alpha",
  "persona": "Jody",
  "persona_version": "2026-06-08-v1",
  "persona_source": "personas/jody.md",
  "task_id": "MA-FIRESTARTER-A4-EXAMPLE-001",
  "lane": "Firestarter",
  "approved_by": "Bob",
  "report_path": "reports/..."
}
```

## Safety Rule
Do not store full persona files, secrets, credentials, private keys, raw proprietary datasets, account information, or sensitive internal payloads inside OpenAI trace metadata.

## Pending Notes
If a connector blocks a specific persona write, create the missing file manually or through a local safe repo workflow, then update this registry.
