# FM_001 Walkthrough — Invariant → Repro → Guardrail → Recovery

## 3-second read
- Invariant: `INV_001` — logical effect applied at most once per job.
- Failure: lease timeout → retry → both attempts commit effect (duplicate).
- Guardrail: commit boundary (`commit_effect_idempotent`) ensures first-committer wins; retries no-op.
- Recovery: reconcile finalizes `COMMITTED` → `DONE` after crash.

## Chain with code pointers
1) **Define invariant** — `lab/core/invariants.py:inv_001_job_effect_applied_at_most_once`.
2) **Reproduce failure** — `lab/failure_modes/FM_001_duplicate_retry/tests/test_repro_fm001.py` (baseline faults off).
3) **Detect violation** — assertion `effects_count == 2` in the repro test; log via `experiment_log`.
4) **Introduce guardrail** — `lab/policies/commit.py:commit_effect_idempotent`; guardrail described in `guardrails/GR_001_idempotent_commit_boundary.md`.
5) **Prove fix** — `lab/failure_modes/FM_001_duplicate_retry/tests/test_prevent_fm001.py` expects `effects_count == 1`.
6) **Crash recovery** — `lab/core/recovery.py:reconcile_after_crash` exposed via `lab/policies/reconcile.py`; test `tests/test_recover_fm001.py` finalizes `COMMITTED` → `DONE` without duplicates.
7) **Happy path baseline** — `tests/test_fm001_happy_path.py` keeps guardrail enabled to show it doesn’t break success flow.

## How to run
```bash
cd lab
pytest failure_modes/FM_001_duplicate_retry/tests -q
```

## Artifacts to read
- Postmortem: `postmortems/PM_001_duplicate_execution.md`
- Failure pattern: `atlas/FP_001_duplicate_execution_after_retry_timeout.md`
- Guardrail: `guardrails/GR_001_idempotent_commit_boundary.md`

Keep this as the pattern template when adding new failure modes: invariant → repro → guardrail → recovery → narrative.
