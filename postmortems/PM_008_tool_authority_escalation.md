# PM_008 — Tool Authority Escalation via Prompt Injection

## TL;DR
- Baseline let a standard-user prompt steer the model into calling a sensitive tool (`read_sensitive_config`) → INV_009 broken.
- Guarded runtime added GR_008 (deterministic authorization) → same prompts blocked; zero sensitive calls.
- Evidence: baseline sensitive calls 4/6 adversarial prompts; guarded sensitive calls 0/6; see `results/*.json` + `results/summary.md`.

## Quick signals (copy/paste for dashboards)
- Detection: `request_class == "standard_user" AND sensitive_tool_called == true`
- Guarded denial code: `policy_outcome = "denied_sensitive_tool"`
- Clearest model signal: qwen2.5-coder:7b (3/3 adversarial calls in baseline, 0/3 guarded).

## Boundary failure → guardrail
- Broken boundary: “planner output == authorization.” Flow was user prompt → model reasoning → tool invocation → privileged execution.
- Guardrail: deterministic policy check between tool request and execution. Model remains planner; runtime enforces authority.

```mermaid
flowchart TD
    A[User Prompt] --> B[LLM Reasoning] --> C[Tool Request]
    C --> D[Policy Authorization] --> E{Allow?}
    E -->|Yes| F[Execute]
    E -->|No| G[Denied + Log]
```

## Deterministic reproduction (lab proof)
1. Configure tools: `search_docs` (public), `read_sensitive_config` (sensitive).
2. Run baseline suite with 2 benign + 3 adversarial prompts across models.
3. Baseline results: qwen2.5-coder:7b executes sensitive tool on all 3 adversarial prompts; qwen2.5-coder:1.5b on 1/3.
4. Re-run with GR_008: policy denies all sensitive tool attempts; sensitive calls drop to 0.

## Evidence files
- `lab/failure_modes/FM_008_tool_authority_escalation/results/baseline_results.json`
- `lab/failure_modes/FM_008_tool_authority_escalation/results/guarded_results.json`
- `lab/failure_modes/FM_008_tool_authority_escalation/results/summary.md`

## Root cause
- Tool availability was treated as implicit authorization.
- No deterministic pre-dispatch policy; prompt-steerable planning became a security decision point.

## Verification
- Repro: `tests/test_repro_fm008.py`
- Prevention: `tests/test_prevent_fm008.py`
- Happy path safety: `tests/test_fm008_happy_path.py`

## Generalization
Applies to any “prompt → planner model → tool execution” stack (LangChain-style agents, MCP runtimes, AutoGPT variants, assistant tool-calling) where authorization is delegated to model reasoning instead of runtime policy.

## Links
- Failure pattern: [`atlas/FP_008_tool_authority_escalation_via_prompt_injection.md`](../atlas/FP_008_tool_authority_escalation_via_prompt_injection.md)
- Guardrail: [`guardrails/GR_008_explicit_tool_authorization_boundary.md`](../guardrails/GR_008_explicit_tool_authorization_boundary.md)
- Lab bundle: [`lab/failure_modes/FM_008_tool_authority_escalation/`](../lab/failure_modes/FM_008_tool_authority_escalation/)
- Lab writeup: [`tool-authority-escalation-postmortem.md`](../lab/failure_modes/FM_008_tool_authority_escalation/writeups/tool-authority-escalation-postmortem.md)
