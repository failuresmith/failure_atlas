# Policies (Recovery & Containment)

Policies are small, explicit mechanisms that keep invariants intact when failures occur. They operate on the minimal runtime (queue, worker, store, deterministic clock).

## Commit boundary (idempotency)
- **Inputs**
  - Job identity + idempotency key
  - Current execution record/state
  - Prior durable execution records for the same logical job
- **Outputs**
  - Exactly one durable `COMMITTED` boundary for a logical execution
  - Side effects emitted only at/after `COMMITTED`
  - Duplicate attempt outcome = safe no-op when `COMMITTED` already exists
- **Invariant(s) enforced**
  - [INV_001](01_invariants.md#inv_001----job-execution-is-logically-idempotent)
- **Failure modes covered**
  - [FM_001 duplicate retry](../failure_modes/FM_001_duplicate_retry/spec.md)

## Reconcile
- **Inputs**
  - Durable execution log + job state records
  - Lease/timeout metadata from in-flight attempts
  - Deterministic clock for expiry checks
- **Outputs**
  - Expired pre-commit executions marked `ABORTED`
  - Safe re-queue decisions for recoverable work
  - Recomputed job state derived from durable records (monotonic, explicit)
- **Invariant(s) enforced**
  - [INV_002](01_invariants.md#inv_002----partial-execution-must-not-leave-irreversible-damage)
  - [INV_004](01_invariants.md#inv_004----recovery-restores-correctness-not-just-availability)
  - [INV_003](01_invariants.md#inv_003----job-state-transitions-are-monotonic-and-explicit)
- **Failure modes covered**
  - [FM_001 duplicate retry](../failure_modes/FM_001_duplicate_retry/spec.md) (timeout/crash recovery path)

## Retry budget / circuit breaker
- **Inputs**
  - Per-job retry counters/history
  - Budget policy (max attempts per time window)
  - Failure outcomes/events from worker attempts
- **Outputs**
  - Permit/deny decision for next retry attempt
  - Circuit-open signal when budget is exhausted
  - Explicit failure signal instead of unbounded retry looping
- **Invariant(s) enforced**
  - [INV_005](01_invariants.md#inv_005----failure-must-be-detectable)
- **Failure modes covered**
  - Retry-storm class failures (tracked in this lab as FM_XXX as added)

## Bounded pagination state registry
- **Inputs**
  - Incoming discover/list requests that allocate pagination cookies
  - Configured cookie state budget (`MAX_COOKIES_TRACKED`)
  - Existing ordered cookie state table
- **Outputs**
  - Bounded cookie registry size (`cookie_count <= MAX_COOKIES_TRACKED`)
  - Deterministic overflow behavior (FIFO eviction in FM_002)
  - Auditable pressure signal (`evicted_count`)
- **Invariant(s) enforced**
  - [INV_006](01_invariants.md#inv_006----remote-request-driven-state-growth-must-be-bounded)
  - [INV_005](01_invariants.md#inv_005----failure-must-be-detectable)
- **Failure modes covered**
  - [FM_002 unbounded pagination state](../failure_modes/FM_002_unbounded_pagination_state/spec.md)

## Inclusive per-principal quota boundary checks
- **Inputs**
  - Principal identity (`peer_id`/tenant/actor)
  - Active allocation count for that principal
  - Configured per-principal maximum (`max_reservations_per_peer`)
- **Outputs**
  - Deterministic admission decision at boundary (`reject when current >= max`)
  - Active allocation count bounded by configuration
  - Detectable policy pressure via rejected request counters
- **Invariant(s) enforced**
  - [INV_007](01_invariants.md#inv_007----per-principal-active-allocations-must-not-exceed-quota)
  - [INV_005](01_invariants.md#inv_005----failure-must-be-detectable)
- **Failure modes covered**
  - [FM_003 quota boundary off-by-one](../failure_modes/FM_003_quota_boundary_off_by_one/spec.md)

## Audit & observability
- **Inputs**
  - State transition events from queue/worker/store
  - Execution outcomes (`STARTED`, `COMMITTED`, `ABORTED`, etc.)
  - Duplicate detection and retry/circuit signals
- **Outputs**
  - Durable audit trail of each transition
  - Counters/metrics for duplicates, retries, aborts, commits
  - Detectable signals suitable for alerting/postmortem analysis
- **Invariant(s) enforced**
  - [INV_003](01_invariants.md#inv_003----job-state-transitions-are-monotonic-and-explicit)
  - [INV_005](01_invariants.md#inv_005----failure-must-be-detectable)
- **Failure modes covered**
  - [FM_001 duplicate retry](../failure_modes/FM_001_duplicate_retry/spec.md) (detection and evidence)
  - Cross-cutting support for all FM_XXX via durable detection evidence

## How these map to artifacts
- Defined in `policies/` modules.
- Exercised by scenarios under `failure_modes/FM_XXX_*/scenario.py`.
- Proven by `tests/test_prevent_fmxxx.py` which asserts invariants stay satisfied even under injected faults.
- Glossary references: see `GLOSSARY.md` entries for commit boundary, reconcile, retry budget, and idempotency boundary.
