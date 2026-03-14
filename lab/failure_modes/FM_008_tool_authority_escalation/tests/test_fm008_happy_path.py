from __future__ import annotations

from pathlib import Path

from failure_modes.FM_008_tool_authority_escalation.prompts import PROMPT_CASES
from failure_modes.FM_008_tool_authority_escalation.scenario import (
    ensure_fake_protected_resource,
    run_guarded_suite,
)


def _safe_planner(_model_name: str, user_prompt: str, _tools: list[dict[str, str]]) -> dict[str, object]:
    return {
        "tool_name": "search_docs",
        "tool_args": {"query": user_prompt},
        "reason": "Use safe public docs for standard prompts.",
        "raw_response": '{"tool_name":"search_docs"}',
    }


def test_fm008_happy_path_benign_prompts_use_safe_tool(experiment_log):
    base_dir = Path(__file__).resolve().parents[1]
    ensure_fake_protected_resource(base_dir)

    benign_cases = [case for case in PROMPT_CASES if case.category == "benign"]
    records = run_guarded_suite(
        model_name="stub-model",
        base_dir=base_dir,
        prompt_cases=benign_cases,
        planner=_safe_planner,
    )

    experiment_log(
        {
            "records": records,
            "benign_count": len(benign_cases),
        }
    )

    assert len(records) == 2
    assert all(record["chosen_tools"] == ["search_docs"] for record in records)
    assert all(record["sensitive_tool_called"] is False for record in records)
    assert all(record["policy_outcome"] == "allowed" for record in records)
