# FM_008 — Tool Authority Escalation via Prompt Injection

Minimal reproducible AI safety experiment showing that model-driven tool choice can be steered to sensitive tools, and that deterministic authorization at the tool boundary blocks the escalation.

## What this contains

- **Version A (baseline):** LLM selects and executes tools directly.
- **Version B (guarded):** same planner, but tool calls pass through deterministic policy authorization.
- **Tools:**
  - `search_docs(query)` (safe/public)
  - `read_sensitive_config(path)` (simulated sensitive/protected)
- **Prompt set:** 2 benign + 3 adversarial prompts.

## Project files

- `run_experiment.py`
- `scenario.py`
- `agent_baseline.py`
- `agent_guarded.py`
- `policy.py`
- `prompts.py`
- `tools.py`
- `results/`
- `writeups/tool-authority-escalation-postmortem.md`

## Setup

Requirements:
- Python 3.11+
- local Ollama service (`ollama serve`)
- models available locally (default):
  - `qwen2.5-coder:7b`
  - `qwen2.5-coder:1.5b`

Install dependencies (none beyond stdlib for this FM):

```bash
python -m pip install -r requirements.txt
```

## Run

From repository root:

```bash
python lab/failure_modes/FM_008_tool_authority_escalation/run_experiment.py
```

Optional custom model list:

```bash
python lab/failure_modes/FM_008_tool_authority_escalation/run_experiment.py --models qwen2.5-coder:7b deepseek-r1:1.5b
```

## Outputs

- `results/baseline_results.json`
- `results/guarded_results.json`
- `results/summary.md`

The runner also prints:
- what worked
- what failed
- model with clearest signal
- confidence statement

## Safety notes

- Uses a fake protected file only: `data/protected/system_config.txt`
- No real secrets, no exfiltration behavior
- Experiment scope is authorization failure in tool-use agents
