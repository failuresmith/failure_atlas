---
ID: FP_009
Title: Progress Stall Detection Gap in Agent Loops
Domain: Agent Runtime
Mechanism: Progress Ledger Omission
Severity: reliability
Status: draft
reproduced_in:
  - FM_011
mitigated_by:
  - GR_009
---

# Failure Pattern

Agents with iteration caps but no progress awareness can loop on an unchanged failing tool invocation until the cap is exhausted.

Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update.

## Context

LLM tool loops typically bound work by `max_iterations`. In absence of a progress ledger, repeated failures are treated as "try again" rather than "stuck".

## Hidden Assumption

"If a tool call fails repeatedly, the planner will adapt before burning the iteration budget." 

## Invariant at Risk

- INV_002 — partial progress must be detectable.
- INV_005 — failure must be detectable.

## Failure Mechanism

- Planner/tool pair emits identical `(tool, args, error)` across steps.
- Termination guard is count-based only; no delta check on observation or action.
- Loop ends at iteration limit with wasted calls and unclear cause.

## Relevance / where this appears

- LangChain agents repeating invalid tool calls (`ValidationError`, auth errors).
- Agents with deterministic tool failures (schema mismatch, missing creds) but no stuck-state detection.
- Any max-iteration guard without progress criteria.

## Guardrail (overview)

Add a progress-aware termination guard:

- Track last `N` step signatures (tool, args, error/output).
- If the last `K` are identical → emit `no_progress_detected` and stop.
- Configure window/threshold per agent; log the stuck signature.

## Explicit links

- lab reproduction: `lab/failure_modes/FM_011_progress_stall_loop/`
- guardrail entry: `guardrails/GR_009_progress_guard_middleware.md`
