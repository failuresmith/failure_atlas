# Atlas Agent Guide

`atlas/` stores **failure knowledge**, not fixes.

## Purpose

Document recurring failure patterns so they are reusable across systems.

Use this workflow framing for every entry:

**Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update**

Inside that chain, `atlas/` owns the `FP` layer:

- `PM` = the real occurrence record
- `FM` = one concrete deterministic manifestation
- `FP` = the reusable higher-level pattern in `atlas/`
- `GR` = the detailed containment design

`FP` must complement `FM`, not duplicate it.

## Boundary

- Put the **recurring mechanism class** here: what fails and why across cases.
- Do **not** copy the step-by-step deterministic lab sequence here; that belongs in `lab/`.
- Do **not** put prevention implementation details here; those belong in `guardrails/`.

## Required structure for each atlas entry

Each entry should include:

1. Pattern statement
2. Hidden assumption
3. Invariant at risk
4. Recurring mechanism
5. Representative triggers / manifestations
6. Detection / observable symptoms
7. Known occurrences when available (`PM`)
8. Explicit links:
   - concrete lab reproductions (`lab/failure_modes/FM_XXX_*`)
   - guardrail entries (`guardrails/GR_XXX_*`)

## Authoring rules

- Focus on reusable mechanism, not one incident's timeline and not one FM's step log.
- Keep language abstract and reusable across domains.
- One failure domain per entry.
- One FP may and should eventually point to multiple PMs, FMs, or GRs when the mechanism is shared.
- If mechanism is unclear, refine the lab first before expanding atlas text.
