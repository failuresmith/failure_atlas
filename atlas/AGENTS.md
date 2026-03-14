# Atlas Agent Guide

`atlas/` stores **failure knowledge**, not fixes.

## Purpose

Document real-world failure classes so they are reusable across systems.

Use this workflow framing for every entry:

**Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update**

## Boundary

- Put **what fails and why** in `atlas/`
- Do **not** put prevention implementation details here (those belong in `guardrails/`)

## Required structure for each atlas entry

Each entry should include:

1. Context
2. Hidden assumption
3. Invariant at risk
4. Failure mechanism
5. Relevance / where this class appears
6. Explicit links:
   - lab reproduction (`lab/failure_modes/FM_XXX_*`)
   - guardrail entry (`guardrails/GR_XXX_*` or equivalent)

## Authoring rules

- Focus on class-level mechanism, not incident storytelling detail.
- Keep language abstract and reusable across domains.
- One failure class per entry.
- If mechanism is unclear, refine the lab first before expanding atlas text.
