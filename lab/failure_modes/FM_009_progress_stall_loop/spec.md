---
ID: FM_009
Title: Progress-stall loop from repeated invalid tool call
Hypothesis: Absent a progress-aware guard, an agent repeats the same failing tool invocation until hitting the iteration cap.
Invariant: INV_002, INV_005
Status: validated
related_pattern:
  - FP_009
---

# FM_009 — Progress-stall loop from repeated invalid tool call

## Context

LLM agents commonly bound work by max iterations. When the planner cannot infer a fix for a failing tool call, it may repeat the same action indefinitely until the cap is reached.

## Hidden assumption

"If the tool call keeps failing, the planner will change its plan before exhausting the iteration budget."

## Violated invariants

- `INV_002` — Partial execution must be detectable (here, no progress signal exists until the hard cap).
- `INV_005` — Failure must be detectable (the loop emits errors but no mechanism classifies them as a stuck state).

## Description

The planner/tool loop lacks a progress ledger. Each iteration repeats the same tool with identical arguments, producing the same validation error. The agent stops only when `max_iterations` is reached, wasting budget and delaying user-visible failure.

## Trigger

1. Planner selects tool `search_db` with invalid arguments.
2. Tool returns a deterministic `ValidationError`.
3. Planner retries with the same arguments because no progress-delta check exists.
4. Loop continues until `max_iterations`.

## Failure mechanism

- No state change between iterations (action, args, and error are constant).
- Termination guard is count-based, not progress-aware.
- The planner treats repeated failures as "try again" rather than "stuck".

## Symptoms

- Identical tool call + identical error across ≥K steps.
- Iteration counter consumed without new observations.
- Termination reason is generic iteration cap, not explicit no-progress.

## Detection

- Maintain a sliding window of recent steps; if `(tool, args, error)` signatures are identical for `K` consecutive steps, classify as `no_progress_detected`.

## Recovery / prevention strategy

- Add a progress-aware guard that terminates early when no new state is observed for `K` steps.
- Emit explicit termination reason and trace to aid debugging.

## Expected impact

- Reduces wasted tool calls and latency during stuck loops.
- Surfaces failure earlier with a precise reason (`no_progress_detected`).

## Acceptance criteria

- `test_repro_fm011.py` shows identical failing tool calls consume the full iteration budget without a progress guard.
- `test_prevent_fm011.py` shows the guard halts after `K` repeated failures and returns `no_progress_detected`.
- `test_fm011_happy_path.py` shows the guard does not trigger when the planner changes arguments and makes progress.
