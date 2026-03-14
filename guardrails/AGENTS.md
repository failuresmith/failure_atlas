# Guardrails Agent Guide

`guardrails/` stores **containment and prevention patterns**, not failure analysis.

## Purpose

Document reusable designs that enforce invariants under known failure classes.

Use this workflow framing for every entry:

**Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update**

## Boundary

- Put **containment/prevention strategy** in `guardrails/`
- Do **not** restate full failure analysis here (that belongs in `atlas/`)

## Required structure for each guardrail entry

Each entry should include:

1. Failure class mitigated (FM/atlas reference)
2. Invariant enforced
3. Design principle
4. Implementation sketch (minimal, mechanism-level)
5. Tradeoffs / limits / failure of the guardrail itself
6. Explicit links:
   - atlas entry (`atlas/...`)
   - lab proof (`lab/failure_modes/FM_XXX_*`)

## Authoring rules

- Prefer mechanism language over platform-specific details.
- Describe why the guardrail works, not just what to implement.
- Keep entries reusable across domains.
- One guardrail pattern per document.
