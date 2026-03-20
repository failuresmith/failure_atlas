---
ID: FP_004
Title: Anthropomorphic Misinterpretation
Domain: Human Interpretation
Mechanism: Anthropomorphic Projection
Severity: reliability
Status: draft
mitigated_by:
  - "GR_004 (proposed; unvalidated until FM exists)"
---

# Failure Pattern

Statistical model errors are misclassified as strategic deception due to
anthropomorphic interpretation.

## Hidden Assumption

Confident incorrect output is assumed to imply intentional lying rather than
distributional prediction error.

## Trigger Condition

Models produce plausible but false outputs under uncertainty while evaluators use
human intent frames.

## Failure Mechanism

Observer interpretation layer projects agentive intent onto non-agentic
prediction behavior, collapsing distinct failure classes.

## Observable Symptoms

- failure reports conflate hallucination and deception
- mitigations target "intent" instead of representation/reasoning limits
- evaluation pipelines overfit to narrative explanations

## Detection

- probe representation stability for truth/falsehood clusters
- apply causal/context perturbation tests before assigning intent labels

## Lab Status

The pattern is currently theoretical; no FM reproduction is available yet. Do
not treat any guardrail as validated until a dedicated FM bundle reproduces the
mechanism and exercises the mitigation.

## Relevant Guardrails

- `guardrails/GR_004_failure_class_disambiguation.md` (proposed; pending FM)

## Related Patterns

- FP_003 Read-only Enforcement Gap
