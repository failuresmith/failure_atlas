---
ID: GR_004
Title: Failure-Domain Disambiguation Before Mitigation
mitigates:
  - FP_004
enforces:
  - INV_005
Type: containment
Status: proposed
---

# Failure Pattern Mitigated

- FP_004 Anthropomorphic Misinterpretation

## Invariant Enforced

- INV_005 — failure domain assignment must be evidence-backed and testable.

## Guardrail Design

Require domain-disambiguation checks before assigning intent-bearing labels (e.g.,
"deception") to model failures.

## Implementation Sketch

- run representation probes and causal/context perturbation tests
- classify as representation/reasoning/strategic only after evidence threshold
- block policy decisions that skip disambiguation stage

## Tradeoffs

- slower incident triage path
- higher analysis overhead for ambiguous failures

## Related Failure Patterns

- FP_004
