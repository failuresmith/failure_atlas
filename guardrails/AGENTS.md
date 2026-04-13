# Guardrails Agent Guide

`guardrails/` stores **containment and prevention designs**, not failure analysis.

## Purpose

Document reusable designs that enforce invariants under known failure classes.

Use this workflow framing for every entry:

**Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update**

Inside that chain, `guardrails/` owns the `GR` layer. A guardrail is the most detailed artifact for how prevention or containment works.

## Boundary

- Put **containment/prevention strategy** in `guardrails/`
- Include enough detail that another engineer can understand exactly how the guardrail enforces the invariant.
- Do **not** restate full failure analysis here; that belongs in `atlas/`.

## Required structure for each guardrail entry

Each entry should include:

1. Failure pattern and failure modes mitigated (`FP` / `FM` references)
2. Invariant enforced
3. Enforcement point / trust boundary
4. Mechanism of action (state transitions, decision rules, deny/allow behavior)
5. Detection / observability produced by the guardrail
6. Tradeoffs / limits / failure of the guardrail itself
7. Explicit links:
   - atlas entry (`atlas/...`)
   - lab proof (`lab/failure_modes/FM_XXX_*`)

## Authoring rules

- Prefer mechanism language over platform-specific details.
- Describe why the guardrail works and how it works, not just what to implement.
- Keep entries reusable across domains.
- One guardrail pattern per document.
