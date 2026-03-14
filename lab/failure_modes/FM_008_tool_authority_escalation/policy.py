from __future__ import annotations

from dataclasses import dataclass, field

try:  # pragma: no cover - import convenience for direct script usage
    from .tools import SAFE_TOOL_NAME, SENSITIVE_TOOL_NAME
except ImportError:  # pragma: no cover
    from tools import SAFE_TOOL_NAME, SENSITIVE_TOOL_NAME


TOOL_SENSITIVITY = {
    SAFE_TOOL_NAME: "public",
    SENSITIVE_TOOL_NAME: "sensitive",
}


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    outcome: str
    reason: str


@dataclass
class ToolAuthorizationPolicy:
    """Deterministic authorization boundary enforced outside the LLM."""

    privileged_mode: bool = False
    allowed_tools_by_request_class: dict[str, set[str]] = field(
        default_factory=lambda: {
            "standard_user": {SAFE_TOOL_NAME},
            "privileged_diagnostic": {SAFE_TOOL_NAME, SENSITIVE_TOOL_NAME},
        }
    )

    def authorize(self, *, request_class: str, tool_name: str) -> PolicyDecision:
        if tool_name not in TOOL_SENSITIVITY:
            return PolicyDecision(
                allowed=False,
                outcome="denied_unknown_tool",
                reason=f"Tool `{tool_name}` is not in the approved tool registry.",
            )

        if TOOL_SENSITIVITY[tool_name] == "sensitive" and not self.privileged_mode:
            return PolicyDecision(
                allowed=False,
                outcome="denied_sensitive_tool",
                reason="Sensitive tool requires privileged_mode=True set by runtime configuration.",
            )

        allowed_tools = self.allowed_tools_by_request_class.get(request_class, {SAFE_TOOL_NAME})
        if tool_name not in allowed_tools:
            return PolicyDecision(
                allowed=False,
                outcome="denied_request_class_policy",
                reason=f"Tool `{tool_name}` is not allowed for request class `{request_class}`.",
            )

        return PolicyDecision(
            allowed=True,
            outcome="allowed",
            reason="Tool call authorized by deterministic policy boundary.",
        )
