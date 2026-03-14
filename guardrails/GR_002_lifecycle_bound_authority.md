---
ID: GR_002
Title: Lifecycle-Bound Authority Registry
mitigates:
  - FP_002
enforces:
  - INV_005
Type: containment
Status: proposed
---

# Failure Pattern Mitigated

- FP_002 Extension Authority Persistence

## Invariant Enforced

- INV_005 — stale authority must be detectable and revocable.

## Guardrail Design

Authority entries are derived views of active components, not independent mutable
state.

## Implementation Sketch

- key authority records by component/extension ID
- derive active authority set from currently active extensions
- revoke on deactivate/uninstall synchronously
- assert zero stale authority records in lifecycle tests

## Tradeoffs

- stronger coupling between lifecycle and authority registry paths
- uninstall/deactivate path must be failure-aware

## Related Failure Patterns

- FP_002
- FP_003
