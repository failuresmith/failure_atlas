# FM_008 Walkthrough — Invariant → Repro → Guardrail

## 3-second read
- Invariant: `INV_009` — tool execution authority must be enforced by deterministic runtime policy.
- Failure: planner/model output == authorization; adversarial prompt triggers sensitive tool.
- Guardrail: GR_008 inserts runtime authorization boundary; sensitive tool denied for standard users.

## Chain with code pointers
1) **Define invariant** — `atlas/FP_008_tool_authority_escalation_via_prompt_injection.md` + `guardrails/GR_008_explicit_tool_authorization_boundary.md`.
2) **Reproduce failure** — `lab/failure_modes/FM_008_tool_authority_escalation/tests/test_repro_fm008.py`; adversarial prompts cause sensitive tool execution.
3) **Detect violation** — check `sensitive_tool_called == True` for `request_class == "standard_user"`; logged via result JSONs.
4) **Introduce guardrail** — `lab/failure_modes/FM_008_tool_authority_escalation/policy.py:ToolAuthorizationPolicy`.
5) **Prove fix** — `tests/test_prevent_fm008.py` shows sensitive tool is denied under guardrail.
6) **Happy path** — `tests/test_fm008_happy_path.py` ensures benign prompts still succeed via safe tool.

## How to run
```bash
cd lab
pytest failure_modes/FM_008_tool_authority_escalation/tests -q
```

## Artifacts to read
- Postmortem: `postmortems/PM_008_tool_authority_escalation.md`
- Failure pattern: `atlas/FP_008_tool_authority_escalation_via_prompt_injection.md`
- Guardrail: `guardrails/GR_008_explicit_tool_authorization_boundary.md`
- Extended writeup: `lab/failure_modes/FM_008_tool_authority_escalation/writeups/tool-authority-escalation-postmortem.md`
