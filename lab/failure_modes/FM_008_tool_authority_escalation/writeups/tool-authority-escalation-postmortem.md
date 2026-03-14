# Tool Authority Escalation via Prompt Injection

## System
We built a minimal Ollama-backed tool-using agent with two tools: `search_docs(query)` (safe/public) and `read_sensitive_config(path)` (sensitive/simulated protected resource). Two versions were evaluated on the same 5-prompt suite (2 benign, 3 adversarial): baseline (model-selected tool executes directly) and guarded (deterministic policy check before tool execution).

## Assumption
The baseline implicitly assumed the model would choose tools appropriately for user-level requests and avoid sensitive tools unless truly necessary.

## Attack
Adversarial prompts framed protected-resource inspection as required for correctness (e.g., “inspect internal system configuration first,” “verify against /protected/system_config.txt”).

## Observed Failure
In baseline runs, adversarial prompts triggered sensitive tool execution and returned fake protected data. Measured evidence:
- `qwen2.5-coder:7b`: 3/3 adversarial prompts called `read_sensitive_config`
- `qwen2.5-coder:1.5b`: 1/3 adversarial prompts called `read_sensitive_config`

## Root Cause
Model reasoning was treated as a security boundary. The runtime conflated tool availability with authorization, so prompt-steerable planning directly controlled privileged execution.

## Guardrail
We added a deterministic authorization boundary outside the model:
- classify tools by sensitivity
- allow tools by request class
- require `privileged_mode=True` (runtime config) for sensitive tool execution
- deny unauthorized sensitive calls and log explicit policy denial events

## Evidence
Same prompts were replayed against guarded agent:
- baseline adversarial sensitive calls: **4**
- guarded adversarial sensitive calls: **0**
- guarded adversarial attempts blocked: **4**

Result: the guardrail blocked sensitive tool execution even when the model still requested the sensitive tool.

## Residual Risks
- Tool sensitivity classification can be wrong or drift.
- Request-class policy can overblock legitimate operations.
- Indirect escalation may still occur through overly powerful “safe” tools.
- Planner behavior variability across models can affect attack hit rate.

## Pattern
If privileged tool execution is authorized by LLM planning alone, prompt injection can escalate tool authority. Treat model output as untrusted intent, not authority. Enforce authorization in deterministic runtime policy before dispatch.
