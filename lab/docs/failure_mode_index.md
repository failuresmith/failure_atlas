# Failure Mode Index

Map of failure modes to the invariants they threaten, the proving tests, and the recovery lever we exercise.
Runtimes under test today: **Experiment 01 (Job Queue)**, **Experiment 02 (Pagination Cookie Registry)**, and **Experiment 03 (Per-Peer Quota Admission)**.
This index is the primary progress ledger for the lab methodology.
New experiments/runtimes are introduced only when an FM cannot be represented in Experiment 01 without violating modeling fidelity.

| Failure Mode | Description | Violated Invariants | Repro Test | Prevent Test | Recovery / Policy Lever |
| --- | --- | --- | --- | --- | --- |
| `FM_001` Duplicate Retry | Lease timeout causes duplicate execution of the same job. | [`INV_001`](./01_invariants.md#inv_001----job-execution-is-logically-idempotent), [`INV_002`](./01_invariants.md#inv_002----partial-execution-must-not-leave-irreversible-damage), [`INV_004`](./01_invariants.md#inv_004----recovery-restores-correctness-not-just-availability) | [`test_repro_fm001`](../failure_modes/FM_001_duplicate_retry/tests/test_repro_fm001.py) | [`test_prevent_fm001`](../failure_modes/FM_001_duplicate_retry/tests/test_prevent_fm001.py), [`test_recover_fm001`](../failure_modes/FM_001_duplicate_retry/tests/test_recover_fm001.py) | Commit boundary (`policies/commit.py`) + reconcile finalization (`policies/reconcile.py`) |
| `FM_002` Unbounded Pagination State | Repeated discover requests grow server cookie state without bound. | [`INV_006`](./01_invariants.md#inv_006----remote-request-driven-state-growth-must-be-bounded), [`INV_005`](./01_invariants.md#inv_005----failure-must-be-detectable) | [`test_repro_fm002`](../failure_modes/FM_002_unbounded_pagination_state/tests/test_repro_fm002.py) | [`test_prevent_fm002`](../failure_modes/FM_002_unbounded_pagination_state/tests/test_prevent_fm002.py) | Bounded cookie registry (`policies/budget.py::CookieRegistry`) |
| `FM_003` Quota Boundary Off-by-One | Strict comparator admits one extra reservation at exact per-peer boundary. | [`INV_007`](./01_invariants.md#inv_007----per-principal-active-allocations-must-not-exceed-quota), [`INV_005`](./01_invariants.md#inv_005----failure-must-be-detectable) | [`test_repro_fm003`](../failure_modes/FM_003_quota_boundary_off_by_one/tests/test_repro_fm003.py) | [`test_prevent_fm003`](../failure_modes/FM_003_quota_boundary_off_by_one/tests/test_prevent_fm003.py) | Inclusive admission boundary (`policies/budget.py::PeerReservationQuota`) |

FM details live in each FM’s `spec.md`.

Cross-pipeline links:

- FP reference: `../../atlas/FP_001_duplicate_execution_after_retry_timeout.md`
- GR reference: `../../guardrails/GR_001_idempotent_commit_boundary.md`
- FP reference: `../../atlas/FP_005_unbounded_pagination_cookie_state_amplification.md`
- GR reference: `../../guardrails/GR_005_bounded_pagination_state.md`
- FP reference: `../../atlas/FP_006_quota_boundary_off_by_one_admission.md`
- GR reference: `../../guardrails/GR_006_inclusive_quota_boundary_checks.md`
