# FM_003 — Read-only Enforcement Gap

- **Spec**: `spec.md`
- **Scenario harness**: `scenario.py`
- **Tests**: `tests/test_repro_fm010.py`, `tests/test_prevent_fm010.py`, `tests/test_fm010_happy_path.py`
- **Guardrail**: `guardrails/GR_003_capability_surface_reduction.md`
- **Atlas pattern**: `atlas/FP_003_read_only_enforcement_gap.md`
- **Incident**: `incidents/mcp.md`

Story: a read-only flag is advisory; write tools stay registered and callable. Guardrail suppresses write tool registration when read-only is enabled.
