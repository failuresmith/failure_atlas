---
ID: GR_006
Title: Inclusive Quota Boundary Admission Checks
mitigates:
  - FP_006
enforces:
  - INV_007
Type: prevention
Status: validated
---

# Failure Pattern Mitigated

- FP_006 Quota Boundary Off-by-One Admission

## Invariant Enforced

- INV_007 — per-principal active allocations must not exceed configured quota.

## Guardrail Design

Quota admission checks must reject at the exact configured boundary by using an
inclusive predicate (`current >= max`) before allocation is admitted.

## Implementation Sketch

- maintain active allocation count per principal
- on admission request:
  - if `current >= max`: reject
  - else: accept and increment
- keep deterministic boundary regression tests for `max=0`, `max=1`, `max=N`

## Tradeoffs / Limits

- strict quota checks may increase rejection rate for bursty legitimate traffic
- fairness is improved, but operator tuning of `max` remains required
- does not solve identity-splitting/Sybil behavior; scope is per-identity boundary correctness

## Explicit Links

- atlas: `atlas/FP_006_quota_boundary_off_by_one_admission.md`
- lab proof: `lab/failure_modes/FM_006_quota_boundary_off_by_one/`
