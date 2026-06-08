# Matrix Alpha Tracing Constitution

STATUS: ACTIVE DRAFT
VERSION: 2026-06-08-v1

## Purpose
This document defines how Matrix Alpha may use OpenAI Agents SDK tracing as an audit and observability layer across personas, build tasks, research reviews, reports, and journals.

## Core Rule
Tracing is an audit spine. It is not governance, validation, permission, scientific proof, or final authority.

## Approved Trace Uses
Tracing may be used to record:

- task ID
- workflow name
- trace ID
- group ID
- persona name
- persona version
- persona source file
- lane/system name
- approved-by field
- mode
- report path
- completion status
- blocked actions
- tool category used

## Prohibited Trace Uses
Tracing must not intentionally store:

- API keys
- OAuth tokens
- private keys
- account credentials
- billing details
- raw proprietary datasets
- raw scanner payloads
- exchange payloads
- environment files
- sensitive account/security records
- full persona files
- high-risk operational instructions

## Persona Trace Reference Rule
Personas are stored in GitHub, Notion, and Drive. Traces should reference persona identity only.

Example:

```json
{
  "persona": "Maya",
  "persona_version": "2026-06-08-v1",
  "persona_source": "personas/maya.md"
}
```

## Matrix Alpha Task Identity Standard
Every traced task should have:

```text
TASK_ID:
GROUP_ID:
WORKFLOW_NAME:
TRACE_ID:
PERSONA:
PERSONA_VERSION:
APPROVED_BY:
MODE:
REPORT_PATH:
STATUS:
```

## Task ID Format

```text
MA-[SYSTEM]-[LANE]-[SHORT-TASK]-[NUMBER]
```

Examples:

```text
MA-FIRESTARTER-A4-SHADOW-TRIGGER-001
MA-NIF-NARRATIVE-CLUSTERING-001
MA-DNA-TAPE-PROFILER-001
MA-BOB-BUILD-LOOP-TRACE-001
MA-COMMAND-CENTER-STATUS-001
```

## Report Template Addition
Every completion report should include:

```text
TASK_ID:
TRACE_ID:
GROUP_ID:
WORKFLOW_NAME:
APPROVED_BY:
MODE:
FILES_READ:
FILES_CREATED:
FILES_UPDATED:
BLOCKED_ACTIONS:
STATUS:
```

If tracing is not active yet:

```text
TRACE_ID: NOT_ENABLED_YET
```

## Rollout Sequence
1. Create tracing constitution.
2. Add task ID standard.
3. Add trace fields to report templates.
4. Test with harmless dummy workflow.
5. Confirm sensitive data is not captured.
6. Expand only after review.

## Final Authority
Chris remains final authority for security, credentials, accounts, billing, deployments, irreversible actions, and production decisions.

FINAL STATUS:
MA_TRACING_CONSTITUTION_INITIALIZED
