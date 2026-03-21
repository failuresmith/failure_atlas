---
ID: GR_009
Title: Progress Guard Middleware
Failure: FP_009_progress_stall_detection_gap
Invariants: INV_002, INV_005
Status: draft
lab_proof:
  - lab/failure_modes/FM_011_progress_stall_loop/
---

# Guardrail — Progress Guard Middleware

Containment for agents that repeat the same failing tool call without making progress.

Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update.

## Failure class mitigated

- `FP_009_progress_stall_detection_gap`
- Reproduced in `FM_011_progress_stall_loop`

## Design principle

Count steps only when state changes. If the agent is emitting identical step signatures, terminate early with an explicit stuck reason.

## Mechanism

- Maintain a sliding window (`N`) of `(tool, args, error/output)` signatures.
- If the last `K` signatures are identical → emit `no_progress_detected` and stop.
- Log the stuck signature and K for auditability.

## Configuration knobs

- `window_size` (`N`): how many recent steps to compare.
- `threshold` (`K`): required consecutive identical signatures to declare stuck.
- `behavior`: terminate, hand off to fallback planner, or request human review.

## Limits / tradeoffs

- Overly small `K` can stop legitimate retries; set per-tool or per-error class.
- Needs deterministic signature hashing; include error text to avoid hiding flaky outputs.
- Does not repair the root cause; it contains wasted work and surfaces the failure early.

## Proof of effectiveness

- `test_prevent_fm011_guard_terminates_on_no_progress` shows early stop at 3 repeated failures.
- `test_fm011_happy_path_progress_resets_guard` shows the guard stays silent once arguments change and a success is observed.

## Implementation sketch

- Add middleware around the agent loop (planning or executor layer) that records step signatures and raises `NoProgressDetected` when triggered.
- Surface the termination reason alongside the trace to make the stuck pattern debuggable.

## Links

- Atlas: `atlas/FP_009_progress_stall_detection_gap.md`
- Lab: `lab/failure_modes/FM_011_progress_stall_loop/`
