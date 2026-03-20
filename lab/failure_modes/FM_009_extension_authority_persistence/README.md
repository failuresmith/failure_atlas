# FM_009 — Extension Authority Persistence

- **Spec**: `spec.md`
- **Scenario harness**: `scenario.py`
- **Tests**: `tests/test_repro_fm009.py`, `tests/test_prevent_fm009.py`, `tests/test_fm009_happy_path.py`
- **Guardrail**: `guardrails/GR_002_lifecycle_bound_authority.md`
- **Atlas pattern**: `atlas/FP_002_extension_authority_persistence.md`
- **Postmortem / incident**: `incidents/ironclaw.md`

Story: uninstalling an extension leaves its authority mappings active because the registry is not lifecycle-bound. Guardrail derives authority from active extensions only and revokes on uninstall.
