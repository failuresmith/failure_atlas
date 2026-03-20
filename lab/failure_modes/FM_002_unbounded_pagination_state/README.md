# FM_002 — Unbounded Pagination Cookie State

- **Spec**: `spec.md`
- **Scenario harness**: `scenario.py`
- **Tests**: `tests/test_repro_fm002.py`, `tests/test_prevent_fm002.py`, `tests/test_fm002_happy_path.py`
- **Guardrail**: `guardrails/GR_005_bounded_pagination_state.md`
- **Atlas pattern**: `atlas/FP_005_unbounded_pagination_cookie_state_amplification.md`
- **Postmortem**: `postmortems/PM_005_unbounded_pagination_state.md`

Story: repeated discover requests grow server-side pagination cookies without a cap. Guardrail enforces a hard cookie budget with FIFO eviction.
