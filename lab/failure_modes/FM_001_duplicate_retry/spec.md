---
ID: FM_001
Title: Duplicate execution caused by retry after timeout
Hypothesis: Lease timeout + at-least-once retry causes duplicate logical effects without a durable commit boundary.
Invariant: INV_001
Status: validated
related_pattern:
  - FP_001
---

# FM_001 — Duplicate execution caused by retry after timeout

## Context

Systems with at-least-once delivery can legitimately retry work after a timeout.
If commit semantics are not idempotent at the logical job boundary, retries can
amplify side effects.

## Hidden assumption

"If a worker times out, its attempt did not commit any irreversible effect."

## Violated invariant

- `INV_001` — Job execution is logically idempotent.

## Description

When the first worker exceeds lease timeout, the queue re-leases the same job to
another worker. Without an idempotent commit boundary, both workers can apply
the logical effect.

## Trigger

1. Worker A leases job `J`.
2. Worker A starts work and lease expires.
3. Worker B leases the same job `J` as retry.
4. Both workers finish and apply effects.

## Failure mechanism

1. Worker A leases `job J` and starts processing.
2. Lease expires before A reaches terminal completion.
3. Queue re-leases `job J` to Worker B (at-least-once behavior).
4. Both attempts cross effect application without a durable single-commit boundary.
5. Logical effect is applied twice.

## Symptoms

- duplicate side effects for the same `job_id`
- two successful executions for one logical job

## Violated invariants

- `INV_001` (logical idempotency)
- `INV_002` (partial execution crash consistency risk)
- `INV_004` (recovery must restore correctness after crash)

## Detection

- count of side effects by `job_id` > 1
- more than one execution reaching terminal success semantics for the same job

## Recovery / prevention strategy

- enforce a durable `COMMITTED` boundary per `job_id`
- only first commit is accepted
- duplicate attempts must no-op safely

## Expected impact

- correctness loss due to duplicated irreversible effects
- downstream reconciliation burden
- hidden financial/state integrity risk in retry-heavy paths

## Acceptance criteria

- `test_repro_fm001.py` proves duplicate effects in baseline mode
- `test_prevent_fm001.py` proves exactly one effect after commit boundary
- `test_recover_fm001.py` proves crash-after-commit reconciles to correct terminal state without duplicate effects
- `test_fm001_happy_path.py` proves invariant-preserving baseline flow
