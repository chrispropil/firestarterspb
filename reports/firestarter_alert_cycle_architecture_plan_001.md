# Firestarter Alert Cycle Architecture Plan 001

**Task ID:** FIRESTARTER_ALERT_CYCLE_ARCHITECTURE_PLAN_001  
**System:** Matrix Alpha / Firestarter Alert Cycle  
**Mode:** Research only  
**Status:** PASS_FIRESTARTER_ALERT_CYCLE_ARCHITECTURE_PLAN_READY  
**Latest update:** SIMPLE_PATTERN_GLOSSARY_AND_BUILD_QUEUE_LOCKED  
**Hold:** HOLD_FIRESTARTER_ALERT_CYCLE_AI_GOVERNANCE_GAP

---

## 1. Board Decision Lock

Approved for Phase 1 architecture planning only.

Not approved yet:

- live Slack routing
- phone routing
- production timer
- trade execution
- exchange orders
- buy/sell labels
- Cell 2 promotion
- AI-decided alerts
- agent-on-timer behavior

This plan defines how the alert cycle should work. It does not activate any live alert path.

---

## 2. Core Rule

The machine can stay technical internally.

Firestarter must talk to Chris in simple pattern names.

Core operating rule:

- the rule engine decides
- AI only explains
- alerts are research-only
- simple labels are shown to Chris
- long technical rule names stay hidden inside the system

---

## 3. Simple Firestarter Pattern Glossary

Use these names in the viewer, readouts, Slack messages, phone messages, and daily summaries.

### Slingshot

Plain meaning:

- market is weak
- FMLC reloads
- Flowprint reloads
- price may recoil upward for a short 4h-8h window
- do not assume continuation

Short label:

`Slingshot = FMLC + Flowprint reload in weak market.`

Internal rule candidate:

- bearish regime
- FMLC rise >= 2
- Flowprint rise >= 2
- fixed 8h research window

Chris-facing readout example:

`SLINGSHOT — NEARUSDT`

`FMLC and Flowprint are both reloading while the market is still weak.`

`This is the short 4h-8h recovery pattern. Decay risk rises after 8h.`

`Research only.`

---

### FMLC Hanger

Plain meaning:

`The move is hanging on old structure, not fresh momentum.`

Definition:

- price is up or near the high
- FMLC is still high
- ER is weak, missing, or fading
- Flowprint and raw_score are not strongly confirming

Core read:

- FMLC shows structure
- ER proves momentum
- if FMLC is high but ER is gone, the move may be vulnerable

Short label:

`FMLC Hanger = high FMLC near elevated price, but weak/no ER confirmation.`

Failure version:

`FMLC Hanger Fail = price hangs high on FMLC, ER fails to confirm, then price rolls over.`

Chris-facing readout example:

`FMLC HANGER — SOLUSDT`

`Price is still hanging near the high and FMLC remains elevated, but ER is not confirming fresh momentum.`

`This means the move may be holding on old structure instead of new force.`

`Research only.`

---

### Flow Fade

Plain meaning:

`Flowprint starts dying before price fully reacts.`

Definition:

- Flowprint drops
- price may still look stable
- FMLC may still be elevated
- ER may not yet show the full weakness

Short label:

`Flow Fade = Flowprint starts weakening before the move breaks.`

---

### Hollow Push

Plain meaning:

`Price pushes higher without Flowprint support.`

Definition:

- price rises or grinds upward
- Flowprint is flat, weak, or fading
- FMLC may still look healthy
- the move may lack fresh participation

Short label:

`Hollow Push = price rises without Flowprint support.`

---

### Domino Drop

Plain meaning:

`FMLC and Flowprint both break down before the larger move breaks.`

Definition:

- Flowprint drops
- FMLC drops
- ER spike may come later
- price weakness may follow after deterioration

Short label:

`Domino Drop = FMLC + Flowprint both break down.`

---

### Fake Recovery

Plain meaning:

`FMLC improves but Flowprint does not confirm.`

Definition:

- FMLC rises
- Flowprint stays weak or fades
- price recovery may be unstable

Short label:

`Fake Recovery = FMLC improves but Flowprint does not.`

---

### Decay Clock

Plain meaning:

`The useful research window is running out.`

Definition:

- active research window is near its time limit
- for Slingshot, 8h is the current maximum useful window
- after that, decay risk rises

Short label:

`Decay Clock = 8h window running out.`

---

### Hard Recovery

Plain meaning:

`FMLC and Flowprint recover and stay strong.`

Definition:

- FMLC rises
- Flowprint rises
- Flowprint persists instead of rolling over
- stronger than Fake Recovery

Short label:

`Hard Recovery = FMLC + Flowprint recover and hold.`

---

## 4. Event Packet Schema Versioning

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

Purpose:

- every alert can be audited
- every readout can be traced back to the exact rule and data packet
- AI explanations cannot drift away from the packet facts

---

## 5. Sanitized Event Packet Example

```yaml
schema_version: firestarter_event_packet_v0_1
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
symbol: NEARUSDT
regime: bearish
alert_level: PRIORITY_WATCH
price: 5.12
er: 6.8
fmlc: 7.0
flowprint: 6.0
raw_score: 6.45
fmlc_rise_4h: 2.0
flowprint_rise_4h: 2.0
research_window_hours: 8
```

---

## 6. Deterministic Classifier Ownership

The classifier assigns:

- pattern_name
- internal_rule_id
- alert_level
- research_window
- routing eligibility

AI does not assign these.

AI may not:

- discover patterns
- choose symbols
- assign alert levels
- escalate alerts
- add new claims
- use forbidden trading language

---

## 7. Alert Levels

### Level 1 — Dashboard Only

Use for:

- low-confidence structure changes
- partial pattern formation
- noisy behavior
- diagnostics

Routing:

- local viewer only
- no Slack
- no phone

### Level 2 — Research Watch

Use for:

- Fake Recovery
- Flow Fade
- Hollow Push
- Domino Drop warning
- FMLC Hanger

Routing:

- future Slack phase only
- no phone unless upgraded by a deterministic rule

### Level 3 — Priority Watch

Use for:

- Slingshot
- Decay Clock on active Slingshot
- severe Domino Drop

Routing:

- future Slack + phone phase only
- not active in Phase 1

---

## 8. Fail-Closed Behavior

If market data is stale, incomplete, malformed, or missing required scoring fields:

- no Slack alert
- no phone alert
- no priority escalation
- write diagnostic log
- show local viewer status as `DATA_INCOMPLETE`

Fail-closed means silence externally, diagnose locally.

---

## 9. Duplicate Suppression

Duplicate key:

`symbol + pattern_name + alert_level + research_window_start_utc`

Do not resend the same alert unless:

- alert level increases
- Decay Clock begins
- regime changes
- setup invalidates
- ER changes by >= 1.5
- FMLC changes by >= 1.5
- Flowprint changes by >= 1.5

---

## 10. Template-First Readout Generator

Phase 1 and Phase 2:

- no open-ended AI generation
- use approved deterministic templates only
- simple Firestarter names only

Later optional AI wording pass:

- AI may compress or rephrase within approved vocabulary
- AI may not introduce new claims
- AI may not introduce new pattern names
- AI may not assign alert levels
- AI may not use action language

---

## 11. Readout Guardrails

Every readout must pass:

`readout_text -> forbidden language scanner -> approved vocabulary scanner -> route decision`

If forbidden words are detected:

- block alert
- write violation log
- show local diagnostic only
- do not route to Slack or phone

---

## 12. Forbidden Language

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

## 13. Approved Research Language

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

## 14. Audit Log Requirements

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

## 15. Governance Boundaries

Codex and Antigravity remain build, review, and audit tools only.

They may not:

- operate as live alert agents
- run on a timer
- decide alerts
- route live notifications without approval

---

## 16. Activation Gates

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

## 17. Build Queue

### Phase 2A — Local Dry-Run Alert Cycle Plan

Goal:

- design the one-cycle local script behavior
- no timer
- no Slack
- no phone
- no external routing

Expected output:

`reports/firestarter_local_alert_cycle_dry_run_plan_001.md`

### Phase 2B — Pattern Classifier Spec

Goal:

- define deterministic conditions for Slingshot, FMLC Hanger, Flow Fade, Hollow Push, Domino Drop, Fake Recovery, Decay Clock, and Hard Recovery
- keep all thresholds versioned
- keep names simple

Expected output:

`reports/firestarter_simple_pattern_classifier_spec_001.md`

### Phase 2C — Readout Template Spec

Goal:

- create approved templates for each simple pattern
- no open-ended AI generation
- all templates pass forbidden-language rules

Expected output:

`reports/firestarter_readout_template_spec_001.md`

### Phase 2D — Local Viewer Alert Panel Plan

Goal:

- define dashboard-only alert panel
- show latest pattern, symbol, timestamp, research window, and decay clock
- no Slack or phone

Expected output:

`reports/firestarter_local_viewer_alert_panel_plan_001.md`

### Phase 2E — Routing Plan

Goal:

- design future Slack and phone routing only
- no activation
- no secrets
- no live test messages

Expected output:

`reports/firestarter_alert_routing_plan_001.md`

---

## 18. Phase Boundary

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

---

## 19. Current Board Lock

Approved direction:

`APPROVE_PHASE_1_ONLY_WITH_SIMPLE_PATTERN_NAMES`

Current status:

`PASS_FIRESTARTER_ALERT_CYCLE_ARCHITECTURE_PLAN_READY`

Next safe lane:

`FIRESTARTER_LOCAL_ALERT_CYCLE_DRY_RUN_PLAN_001`
