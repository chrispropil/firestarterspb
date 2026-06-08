# Matrix Alpha Persona Governance

STATUS: ACTIVE
VERSION: 2026-06-08-v1

## Purpose
This document defines how Matrix Alpha personas are stored, referenced, updated, and audited.

## Storage Layers

### GitHub
GitHub is the technical source of truth for persona files.

Primary folder:

```text
personas/
```

### Notion
Notion is the readable persona command library and operational reference layer.

### Google Drive
Google Drive is the journal and archive layer.

### OpenAI Traces
OpenAI traces are the audit trail only. Traces should reference persona name, version, source file, task ID, and report path. Traces should not become the persona database.

## Persona Reference Standard
Every persona should have:

```text
STATUS:
VERSION:
ROLE:
CORE FUNCTION:
AUTHORITY BOUNDARY:
SUMMON BEHAVIOR:
TRACE_METADATA_REFERENCE:
```

## Trace Metadata Standard

```json
{
  "system": "Matrix Alpha",
  "persona": "Maya",
  "persona_version": "2026-06-08-v1",
  "persona_source": "personas/maya.md",
  "task_id": "MA-EXAMPLE-001",
  "workflow_name": "Matrix Alpha / Example Workflow",
  "approved_by": "Bob",
  "report_path": "reports/..."
}
```

## Update Rule
Persona changes require:

1. GitHub file update.
2. Notion summary update.
3. Google Drive journal/archive note.
4. Completion report or chat note describing what changed.

## Authority Rule
Personas may assist with research, review, build governance, and executive framing. They do not replace Chris on security, credentials, account, billing, deployment, destructive, irreversible, or final authority decisions.

## Safety Rule
Do not store secrets, API keys, OAuth tokens, private keys, raw proprietary datasets, account details, or sensitive payloads in persona files or trace metadata.

## Current Registry Status
- Maya: saved in GitHub.
- Bob: saved in GitHub.
- Steve: saved in GitHub.
- Red Team: saved in GitHub.
- Jody: pending if connector write is blocked; preserve Jody role from existing Notion/Drive/persona memory until file is added safely.

FINAL STATUS:
MA_PERSONA_GOVERNANCE_INITIALIZED
