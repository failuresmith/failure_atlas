# FM_006 — Quota Boundary Off-by-One

- **Spec**: `spec.md`
- **Scenario harness**: `scenario.py`
- **Tests**: `tests/test_repro_fm003.py`, `tests/test_prevent_fm003.py`, `tests/test_fm003_happy_path.py`
- **Guardrail**: `guardrails/GR_006_inclusive_quota_boundary_checks.md`
- **Atlas pattern**: `atlas/FP_006_quota_boundary_off_by_one_admission.md`
- **Postmortem**: `postmortems/PM_006_quota_boundary_off_by_one.md`

Story: strict `>` admission lets one extra reservation at the limit. Guardrail uses inclusive `>=` check and keeps boundary regression tests.
