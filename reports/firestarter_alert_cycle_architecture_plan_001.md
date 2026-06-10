# Firestarter Alert Cycle Architecture Plan 001

**Task ID:** FIRESTARTER_ALERT_CYCLE_ARCHITECTURE_PLAN_001  
**System:** Matrix Alpha / Firestarter Alert Cycle  
**Mode:** Research only  
**Status:** PASS_FIRESTARTER_ALERT_CYCLE_ARCHITECTURE_PLAN_READY  
**Hold:** HOLD_FIRESTARTER_ALERT_CYCLE_AI_GOVERNANCE_GAP

---

## 1. Board Decision Lock

- Phase 1 architecture plan only
- No live routing
- No Slack activation
- No phone activation
- No production timer

This plan defines the local alert-cycle architecture only. It does not activate any live alert path.

---

## 2. Simple Pattern Naming System

Use only the following simple Firestarter names for Chris-facing readouts, viewer panels, Slack alerts, phone alerts, and dashboards:

- Slingshot
- FMLC Hanger
- Flow Fade
- Hollow Push
- Domino Drop
- Fake Recovery
- Decay Clock
- Hard Recovery

Primary pattern:

- **Slingshot**

Meaning:

- Weak / bearish market
- FMLC reloads
- Flowprint reloads
- Short 4h-8h recovery window

Internal rule:

- bearish regime
- AND FMLC rise >= 2
- AND Flowprint rise >= 2
- AND fixed 8h research window

User-facing readout example:

- `SLINGSHOT — NEARUSDT`
- `FMLC and Flowprint are both reloading while the market is still weak.`
- `This is the short 4h-8h recovery pattern.`
- `Decay risk rises after 8h.`
- `Research only.`

---

## 3. Event Packet Schema Versioning

Every packet must include:

- schema_version
- event_id
- event_hash
- pattern_name
- internal_rule_id
- classifier_version
- scoring_engine_version
- regime_detector_version
- readout_template_version
- created_at_utc
- source_cycle_id

---

## 4. Sanitized Event Packet Example

Example packet:

```yaml
schema_version: 1
event_id: firestarter_event_000001
event_hash: sha256:placeholder
pattern_name: Slingshot
internal_rule_id: slingshot_v0_1
classifier_version: classifier_v0_1
scoring_engine_version: scoring_v0_1
regime_detector_version: regime_v0_1
readout_template_version: template_v0_1
created_at_utc: 2026-06-09T00:00:00Z
source_cycle_id: cycle_000001
```

---

## 5. Deterministic Classifier Ownership

Classifier assigns:

- pattern_name
- internal_rule_id
- alert_level
- research_window
- routing eligibility

AI does not assign these.

---

## 6. Alert Levels

- Level 1: Dashboard only
- Level 2: Slack research watch, future phase
- Level 3: Slack + phone priority watch, future phase

---

## 7. Fail-Closed Behavior

If market data is stale, incomplete, malformed, or missing required scoring fields:

- no Slack alert
- no phone alert
- no priority escalation
- write diagnostic log
- show local viewer status as `DATA_INCOMPLETE`

---

## 8. Duplicate Suppression

Duplicate key:

- symbol + pattern_name + alert_level + research_window_start_utc

Do not resend the same alert unless:

- alert level increases
- Decay Clock begins
- regime changes
- setup invalidates
- ER, FMLC, or Flowprint changes by >= 1.5

---

## 9. Template-First Readout Generator

Phase 1 and Phase 2:

- No open-ended AI generation
- Use approved deterministic templates only

Later optional AI wording pass:

- AI may compress or rephrase only within approved vocabulary
- AI may not introduce new claims, setup types, alert levels, or action language

---

## 10. Readout Guardrails

Every readout must pass:

`readout_text -> forbidden language scanner -> approved vocabulary scanner -> route decision`

If forbidden words are detected:

- block alert
- write violation log
- show local diagnostic only
- do not route to Slack or phone

---

## 11. Forbidden Language

Block:

- BUY
- SELL
- LONG
- SHORT
- ENTRY
- EXIT
- TRADE
- TAKE PROFIT
- STOP LOSS
- LIVE SIGNAL

---

## 12. Approved Language

Allow:

- WATCH
- PRIORITY WATCH
- RESEARCH WINDOW
- DECAY WARNING
- DISTRIBUTION RISK
- STRUCTURE WARNING
- PARTICIPATION CONFIRMATION
- SLINGSHOT
- FMLC HANGER
- FLOW FADE
- HOLLOW PUSH
- DOMINO DROP
- FAKE RECOVERY
- DECAY CLOCK
- HARD RECOVERY
- RESEARCH ONLY

---

## 13. Audit Log Requirements

Every event must log:

- raw event packet
- classifier result
- template used
- generated readout
- validation result
- route decision
- suppression decision
- timestamp
- cycle id

---

## 14. Governance Boundaries

Codex and Antigravity remain build, review, and audit tools only.

They may not:

- operate as live alert agents
- run on a timer
- decide alerts

---

## 15. Activation Gates

Before Slack or phone activation, the board must review and lock:

- event packet schema
- simple pattern names
- alert levels
- duplicate suppression
- routing rules
- safety language
- audit log requirements
- AI readout boundaries

---

## 16. Core Architecture

Windows Task Scheduler
→ `run_firestarter_alert_cycle.py`
→ market data update
→ FirestarterOG scoring engine
→ regime detector
→ deterministic event classifier
→ template-first readout generator
→ forbidden-language validator
→ alert router
→ local viewer / Slack / phone

Core rule:

- The rule engine decides.
- AI only explains.

AI may not:

- discover setups
- choose symbols
- assign alert levels
- escalate alerts
- add new claims
- use forbidden trading language

---

## 17. Phase Boundary

Phase 1 only.

No live Slack alerts.
No phone alerts.
No timer deployment.
No production integration.
No trade execution.
No exchange orders.
No buy/sell labels.
No Cell 2 promotion.
No AI-decided alerts.
No agent-on-timer behavior.

