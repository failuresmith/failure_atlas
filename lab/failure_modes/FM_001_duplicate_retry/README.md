# FM_001 — Duplicate Execution after Retry Timeout

- **Spec**: `spec.md`
- **Scenario harness**: `scenario.py`
- **Tests**: `tests/test_repro_fm001.py`, `tests/test_prevent_fm001.py`, `tests/test_recover_fm001.py`, `tests/test_fm001_happy_path.py`
- **Guardrail**: `guardrails/GR_001_idempotent_commit_boundary.md`
- **Atlas pattern**: `atlas/FP_001_duplicate_execution_after_retry_timeout.md`
- **Postmortem**: `postmortems/PM_001_duplicate_execution.md`

Story: lease expiry triggers retry; without a commit boundary both attempts apply effects. Guardrail enforces first-committer-wins, recovery finalizes COMMITTED→DONE safely.
