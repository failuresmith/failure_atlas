from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Callable
from urllib.error import URLError
from urllib.request import Request, urlopen

try:  # pragma: no cover - import convenience for direct script usage
    from .prompts import PromptCase, build_planner_prompt
    from .tools import SAFE_TOOL_NAME, SENSITIVE_TOOL_NAME, execute_tool, tool_catalog
except ImportError:  # pragma: no cover
    from prompts import PromptCase, build_planner_prompt
    from tools import SAFE_TOOL_NAME, SENSITIVE_TOOL_NAME, execute_tool, tool_catalog


PlannerCallable = Callable[[str, str, list[dict[str, str]]], dict[str, Any]]


@dataclass(frozen=True)
class PlannerDecision:
    tool_name: str
    tool_args: dict[str, Any]
    reason: str
    raw_response: str


def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = text[start : end + 1]
        try:
            parsed = json.loads(snippet)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    return {}


def _normalize_tool_choice(*, user_prompt: str, payload: dict[str, Any], raw_response: str) -> PlannerDecision:
    tool_name = str(payload.get("tool_name", "")).strip() or SAFE_TOOL_NAME
    tool_args = payload.get("tool_args", {})
    if not isinstance(tool_args, dict):
        tool_args = {}
    reason = str(payload.get("reason", "")).strip() or "No reason provided by planner."

    raw_l = raw_response.lower()
    if (
        tool_name == SAFE_TOOL_NAME
        and not payload.get("tool_name")
        and (SENSITIVE_TOOL_NAME in raw_l or "/protected/system_config.txt" in raw_l)
    ):
        tool_name = SENSITIVE_TOOL_NAME
        if "fallback" not in reason.lower():
            reason = f"Fallback parser selected sensitive tool from raw output: {reason}"

    if tool_name not in {SAFE_TOOL_NAME, SENSITIVE_TOOL_NAME}:
        tool_name = SAFE_TOOL_NAME

    if tool_name == SAFE_TOOL_NAME:
        query = str(tool_args.get("query", "")).strip() or user_prompt
        tool_args = {"query": query}
    else:
        path = str(tool_args.get("path", "")).strip() or "/protected/system_config.txt"
        tool_args = {"path": path}

    return PlannerDecision(
        tool_name=tool_name,
        tool_args=tool_args,
        reason=reason,
        raw_response=raw_response,
    )


def ollama_planner(model_name: str, user_prompt: str, tools: list[dict[str, str]]) -> dict[str, Any]:
    planner_prompt = build_planner_prompt(user_prompt=user_prompt, tools=tools)
    payload = {
        "model": model_name,
        "prompt": planner_prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0,
            "seed": 7,
        },
    }
    request = Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
    except URLError as exc:
        raise RuntimeError(
            "Failed to reach Ollama at http://127.0.0.1:11434. Ensure `ollama serve` is running."
        ) from exc

    raw_response = str(body.get("response", "")).strip()
    parsed = _extract_json_object(raw_response)
    parsed["raw_response"] = raw_response
    return parsed


class BaselineAgent:
    """Vulnerable baseline: model-selected tools execute without authz boundary."""

    def __init__(
        self,
        *,
        model_name: str,
        base_dir: Path,
        planner: PlannerCallable | None = None,
    ) -> None:
        self.model_name = model_name
        self.base_dir = base_dir
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
        tool_result = execute_tool(decision.tool_name, decision.tool_args, base_dir=self.base_dir)
        final_answer = (
            f"Baseline answer using {tool_result.tool_name}: {tool_result.output}"
        )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "baseline",
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
            "sensitive_tool_called": tool_result.sensitive_tool_called,
            "policy_outcome": "not_applicable",
            "policy_reason": "No external tool authorization in baseline.",
            "final_answer": final_answer,
            "tool_output": tool_result.output,
        }
