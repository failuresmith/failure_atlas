# FM_008 — Tool Authority Escalation via Prompt Injection

- **Spec**: `spec.md`
- **Scenario harness**: `scenario.py`
- **Tests**: `tests/test_repro_fm008.py`, `tests/test_prevent_fm008.py`, `tests/test_fm008_happy_path.py`
- **Guardrail**: `guardrails/GR_008_explicit_tool_authorization_boundary.md`
- **Atlas pattern**: `atlas/FP_008_tool_authority_escalation_via_prompt_injection.md`
- **Postmortem**: `postmortems/PM_008_tool_authority_escalation.md`
- **Extended writeup**: `writeups/tool-authority-escalation-postmortem.md`

Story: model-only planning executed a sensitive tool when adversarial prompts framed it as required. Guardrail inserts deterministic authorization; same prompts are denied and logged.
