---
ID: FP_001
Title: Duplicate Execution After Retry Timeout
Domain: State Consistency
Mechanism: Retry Idempotence Window
Severity: integrity
Status: validated
reproduced_in:
  - FM_001
mitigated_by:
  - GR_001
---

# Failure Pattern

At-least-once retry after lease timeout can apply one logical effect more than
once unless a durable idempotency boundary exists.

## Hidden Assumption

"Timeout implies no committed side effect was produced."

## Trigger Condition

Worker A lease expires before completion; Worker B retries the same job while A
may still complete.

## Failure Mechanism

Two executions race toward effect application.
Without first-commit gating, both cross the effect boundary.

## Observable Symptoms

- `count_effects(job_id) > 1`
- multiple successful executions for one logical job
- correctness drift requiring reconciliation

## Detection

`count_effects(job_id) > 1`

## Lab Reproduction

- `lab/failure_modes/FM_001_duplicate_retry/`

## Relevant Guardrails

- `guardrails/GR_001_idempotent_commit_boundary.md`

## Postmortem

- `lab/postmortems/PM_001_duplicate_execution.md`

## Related Patterns

- FP_002 Extension Authority Persistence
- FP_003 Read-only Enforcement Gap
