---
ID: FP_006
Title: Quota Boundary Off-by-One Admission
Domain: Policy Enforcement
Mechanism: Quota Boundary Math
Severity: availability
Status: validated
reproduced_in:
  - FM_003
mitigated_by:
  - GR_006
---

# Failure Pattern

Resource admission logic uses an exclusive boundary check where an inclusive
limit is required, allowing one extra allocation beyond configured quota.

## Context

Applies to admission controllers that enforce per-principal resource limits
(per peer, tenant, actor, or identity).

## Hidden Assumption

A strict `current > max` guard is assumed equivalent to enforcing
`current <= max`.

## Invariant at Risk

Per-principal active allocations must never exceed configured quota.

## Trigger Condition

A principal reaches exactly the configured maximum and then submits one more
admission request.

## Failure Mechanism

Quota checks run before insertion but compare with strict-greater (`>`) rather
than greater-or-equal (`>=`). At the boundary (`current == max`) the condition
passes, and one additional allocation is admitted.

## Observable Symptoms

- principal holds `max + 1` active allocations
- boundary tests fail only at exact-limit transitions
- policy appears correct in most traffic but fails at edge values

## Detection

For any principal: `active_allocations(principal_id) > configured_max(principal_id)`.

## Relevance / Where This Domain Appears

- connection reservation limits
- API rate bucket admissions
- per-tenant worker/concurrency caps
- any counter-based quota gate with boundary math

## Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update

- **Real failure:** reservation admission allows one extra allocation at boundary
- **Minimal reproduction:** deterministic FM_003 boundary matrix (`max=0,1,N`) with repeated same-principal admissions
- **Mechanism:** strict boundary comparator (`>` vs `>=`) in pre-admit check
- **Guardrail:** inclusive boundary policy + explicit edge-case regression tests
- **Atlas update:** FP_006 linked to validated FM_003 + GR_006 artifacts
- **Postmortem:** lab/postmortems/PM_006_quota_boundary_off_by_one.md

## Lab Reproduction

- `lab/failure_modes/FM_003_quota_boundary_off_by_one/`

## Relevant Guardrails

- `guardrails/GR_006_inclusive_quota_boundary_checks.md`

## Related Patterns

- FP_005 Unbounded Pagination Cookie State Amplification
