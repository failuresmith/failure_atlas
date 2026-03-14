from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

try:  # pragma: no cover - import convenience for direct script usage
    from .agent_baseline import PlannerDecision, _normalize_tool_choice, ollama_planner
    from .policy import ToolAuthorizationPolicy
    from .prompts import PromptCase
    from .tools import SENSITIVE_TOOL_NAME, execute_tool, tool_catalog
except ImportError:  # pragma: no cover
    from agent_baseline import PlannerDecision, _normalize_tool_choice, ollama_planner
    from policy import ToolAuthorizationPolicy
    from prompts import PromptCase
    from tools import SENSITIVE_TOOL_NAME, execute_tool, tool_catalog


PlannerCallable = Callable[[str, str, list[dict[str, str]]], dict[str, Any]]


class GuardedAgent:
    """Guarded variant: runtime policy authorizes tool calls before execution."""

    def __init__(
        self,
        *,
        model_name: str,
        base_dir: Path,
        policy: ToolAuthorizationPolicy,
        planner: PlannerCallable | None = None,
    ) -> None:
        self.model_name = model_name
        self.base_dir = base_dir
        self.policy = policy
        self.planner = planner or ollama_planner

    def _plan(self, case: PromptCase) -> PlannerDecision:
        tools = tool_catalog()
        planner_payload = self.planner(self.model_name, case.user_prompt, tools)
        raw_response = str(planner_payload.get("raw_response", ""))
        return _normalize_tool_choice(
            user_prompt=case.user_prompt,
            payload=planner_payload,
            raw_response=raw_response,
        )

    def run_prompt(self, case: PromptCase) -> dict[str, Any]:
        decision = self._plan(case)
        policy_decision = self.policy.authorize(
            request_class=case.request_class,
            tool_name=decision.tool_name,
        )

        sensitive_tool_called = False
        tool_output = ""
        final_answer = ""

        if policy_decision.allowed:
            tool_result = execute_tool(decision.tool_name, decision.tool_args, base_dir=self.base_dir)
            sensitive_tool_called = tool_result.sensitive_tool_called
            tool_output = tool_result.output
            final_answer = f"Guarded answer using {tool_result.tool_name}: {tool_result.output}"
        else:
            tool_output = f"POLICY_DENIED: {policy_decision.reason}"
            final_answer = "I cannot use that tool for this request class due to runtime policy."

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "guarded",
            "model_name": self.model_name,
            "prompt_id": case.prompt_id,
            "prompt_category": case.category,
            "request_class": case.request_class,
            "prompt": case.user_prompt,
            "chosen_tools": [decision.tool_name],
            "tool_args": decision.tool_args,
            "planner_reason": decision.reason,
            "planner_raw_response": decision.raw_response,
            "sensitive_tool_requested": decision.tool_name == SENSITIVE_TOOL_NAME,
            "sensitive_tool_called": sensitive_tool_called,
            "policy_outcome": policy_decision.outcome,
            "policy_reason": policy_decision.reason,
            "final_answer": final_answer,
            "tool_output": tool_output,
        }
