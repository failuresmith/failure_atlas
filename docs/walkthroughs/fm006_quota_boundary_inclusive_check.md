# FM_006 Walkthrough — Invariant → Repro → Guardrail

## 3-second read
- Invariant: `INV_007` — per-principal active allocations must not exceed configured quota.
- Failure: admission check uses `current > max`; at boundary (`==`), one extra allocation slips through.
- Guardrail: inclusive comparator (`>=`) keeps active count ≤ max.

## Chain with code pointers
1) **Define invariant** — `guardrails/GR_006_inclusive_quota_boundary_checks.md` ties to `INV_007`; pattern in `atlas/FP_006_quota_boundary_off_by_one_admission.md`.
2) **Reproduce failure** — `lab/failure_modes/FM_006_quota_boundary_off_by_one/tests/test_repro_fm006.py` shows `max + 1` allocations admitted.
3) **Detect violation** — assertion `active > max_reservations_per_peer`; logged via `experiment_log`.
4) **Introduce guardrail** — inclusive check in scenario harness `scenario.py` (uses `>=`).
5) **Prove fix** — `tests/test_prevent_fm006.py` confirms boundary holds for multiple max values.
6) **Happy path** — `tests/test_fm006_happy_path.py` confirms inclusive guardrail does not block valid capacity.

## How to run
```bash
cd lab
pytest failure_modes/FM_006_quota_boundary_off_by_one/tests -q
```

## Artifacts to read
- Postmortem: `postmortems/PM_006_quota_boundary_off_by_one.md`
- Failure pattern: `atlas/FP_006_quota_boundary_off_by_one_admission.md`
- Guardrail: `guardrails/GR_006_inclusive_quota_boundary_checks.md`
