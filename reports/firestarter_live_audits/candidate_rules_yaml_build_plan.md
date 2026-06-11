# candidate_rules.yaml Build Plan

## 1. Why candidate_rules.yaml Is the Safest Next Step

The `FAST_LANE_CONTEXT.md` priority build order lists `candidate_rules.yaml` as step 1, before any label or feature code is written. This ordering is deliberate:

- **Zero runtime risk.** A YAML config file cannot execute, pull data, or mutate state.
- **Decouples rule design from implementation.** Rule logic is agreed in config before a single line of Python is written.
- **Provides a single source of truth** for all downstream consumers (label builders, feature generators, backtest evaluators).
- **Matches existing patterns.** The repo already uses YAML configs in `configs/firestarterlive/` for scenarios and alert settings.
- **Reversible without side effects.** A config file can be removed or edited with no runtime consequence.

All prior work (viewer builds, data pulls, audit reports) is complete and committed. No uncommitted changes exist. The repo is ready for a new planned artifact.

## 2. Proposed File Location

```
configs/candidate_rules.yaml
```

Placed alongside existing config files (`configs/firestarterlive/`, `configs/firestarter_core88_binance_usdt_symbols.txt`). Top-level under `configs/` because it is not specific to the FirestarterLive subsystem.

## 3. Proposed Schema

```yaml
# Top-level structure
version: 1          # Schema version for forward compat
updated: "ISO-8601" # Last-modified timestamp

candidates:
  - id: string                    # Unique key, e.g. candidate_001
    mode: string                  # X1_TACTICAL | X2_POSITION | X2_CONTEXT
    direction: string             # long | short | context_boost
    status: string                # draft | active | deprecated | retired
    tags: [string]                # Free-form labels for grouping

    description: string           # Plain-text intent

    entry_conditions:
      all:                        # All must be true (AND group)
        - feature: string         # Feature column name
          operator: string        # < > <= >= == !=
          value: number | string
        - feature: ...
      any: []                     # Optional: at least one true (OR group)

    exit_conditions:
      all: []

    meta:
      author: string
      review_status: string       # unreviewed | jody_pending | jody_approved
      created: ISO-8601

    constraints:                  # Optional validation gates
      min_samples: number
      min_symbols: number
      min_trading_days: number
      block_if_features: [string] # Features that must NOT exist in dataset
```

### Rationale for Schema Choices

- **`all` / `any` groups** mirror established config patterns (`firestarterlive_scenarios.yaml` uses nested condition lists).
- **Explicit `status` field** allows draft rules to coexist with active ones without deletion.
- **`meta.review_status`** tracks the Jody review gate required by `SPB_RESEARCH_BOUNDARIES.md`.
- **`constraints.block_if_features`** prevents accidental use of leaked future information by naming forbidden label columns.
- **`exit_conditions`** is included as a placeholder for triple-barrier exits (future step 2 of the build order) but can be empty initially.

## 4. Proposed Initial Rule Families

Adapted from `FAST_LANE_CONTEXT.md` current research candidates:

### candidate_001 — Three-Gate Swing Long
- Mode: `X2_POSITION`, direction: `long`
- Entry: cross-sectional return rank (1H) < 0.90 AND volume RVOL (4H) < 1.5
- Purpose: Low-volatility mean-reversion swing entry.

### candidate_002 — Red Flag Short
- Mode: `X1_TACTICAL`, direction: `short`
- Entry: cross-sectional return rank (1H) > 0.98 AND volume RVOL (4H) > 3.0 AND close position in bar < 0.5
- Purpose: High-volatility exhaustion short.

### candidate_003 — Beta Decoupling Context
- Mode: `X2_CONTEXT`, direction: `context_boost`
- No hard entry conditions. Acts as a context boost modifier for other candidates.
- Purpose: Detect when a symbol decouples from broad-market beta.

### Reserved IDs for Future Expansion
- `candidate_004` through `candidate_010`: reserved for rule variants (threshold sensitivity, alternative window lengths, inverse filters).

## 5. Validation Checks Required Before Use

Before any script reads `candidate_rules.yaml` for execution or evaluation:

| Check | Description |
|---|---|
| **Schema validation** | All required keys present; no unknown keys; types match schema. |
| **Feature name audit** | Every `feature` value must match an existing column in the research dataset or be explicitly marked as a planned feature. |
| **Operator whitelist** | Only `<`, `>`, `<=`, `>=`, `==`, `!=` allowed. No custom expressions. |
| **ID uniqueness** | No duplicate `candidate_*` IDs across the file. |
| **Mode whitelist** | Must be one of `X1_TACTICAL`, `X2_POSITION`, `X2_CONTEXT`. |
| **Direction whitelist** | Must be one of `long`, `short`, `context_boost`. |
| **Status check** | Only `draft` or `active` rules are loaded; `deprecated`/`retired` are skipped. |
| **Review gate check** | `active` rules must have `meta.review_status: jody_approved`. |
| **Blocked features test** | If `block_if_features` lists any column present in the dataset, the rule is skipped. |

A standalone `validate_candidate_rules.py` script (no data dependency, pure YAML loading) should be the first consumer written after the YAML itself.

## 6. Explicit Blocked Scope

The following are **out of scope** for the `candidate_rules.yaml` build step and must NOT be implemented:

- Writing the YAML file itself (this is a planning report only).
- Any Python script (label builders, feature generators, validators, evaluators).
- Any data pull or data access.
- Any modification to existing configs, scripts, or reports.
- Any runtime or execution logic.
- Any ML model, signal discovery, or black-box scoring.
- Any trading, order, or exchange logic.
- Any API keys, secrets, or credentials.
- Any Cell 2 exposure or promotion.
- Any modification to the Fast Lane scanner.

## 7. Next Approval Gate

Before `candidate_rules.yaml` can be written:

1. **Chris review** of this build plan.
2. **Jody audit** of the proposed rule families, threshold values, and schema.
3. Both approvals recorded in the YAML `meta.review_status` field or in a follow-up audit report.

After approval, the implementation order shall be:

1. Create `configs/candidate_rules.yaml` with the approved schema and initial candidates.
2. Create `scripts/validate_candidate_rules.py` — pure YAML loader + schema/feature/operator checks.
3. Run validation and commit both files.
4. Proceed to `build_triple_barrier_labels.py` (step 2 of the FAST_LANE_CONTEXT.md build order).
