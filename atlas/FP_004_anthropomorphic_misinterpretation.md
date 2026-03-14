---
ID: FP_004
Title: Anthropomorphic Misinterpretation
Class: Model Behavior
Severity: reliability
Status: draft
reproduced_in:
  - FM_001
mitigated_by:
  - GR_004
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

## Lab Reproduction

- `lab/failure_modes/FM_001_duplicate_retry/`

## Relevant Guardrails

- `guardrails/GR_004_failure_class_disambiguation.md`

## Related Patterns

- FP_003 Read-only Enforcement Gap
