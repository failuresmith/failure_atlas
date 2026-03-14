---
ID: GR_001
Title: Idempotent Commit Boundary
mitigates:
  - FP_001
enforces:
  - INV_001
Type: prevention
Status: validated
---

# Failure Pattern Mitigated

- FP_001 Duplicate Execution After Retry Timeout

## Invariant Enforced

- INV_001 — logical effects are applied at most once per job.

## Guardrail Design

Introduce a durable single-commit boundary (`COMMITTED`) per logical job.
Only the first execution may cross this boundary; subsequent retries no-op.

## Implementation Sketch

- maintain durable `committed_exec_id` keyed by `job_id`
- on commit attempt:
  - if none exists: persist `committed_exec_id`, apply effect
  - if exists: reject/no-op duplicate effect
- finalize `COMMITTED -> DONE` separately to support crash-safe recovery

## Tradeoffs

- adds commit-state bookkeeping
- requires recovery reconciliation path for `COMMITTED` but not `DONE`

## Related Failure Patterns

- FP_001
