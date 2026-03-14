---
ID: GR_003
Title: Capability Surface Reduction at Startup
mitigates:
  - FP_003
enforces:
  - INV_003
Type: prevention
Status: proposed
---

# Failure Pattern Mitigated

- FP_003 Read-only Enforcement Gap

## Invariant Enforced

- INV_003 — policy state must map to explicit executable state transitions.

## Guardrail Design

Project policy mode into the runtime capability surface during registration, not
at invocation hints.

## Implementation Sketch

- if `read_only=true`, do not register write tools
- return "not found" for write operations in read-only mode
- include startup assertion for forbidden capability exposure

## Tradeoffs

- reduced operational flexibility without restart/reconfiguration
- explicit mode switching semantics required

## Related Failure Patterns

- FP_003
- FP_002
