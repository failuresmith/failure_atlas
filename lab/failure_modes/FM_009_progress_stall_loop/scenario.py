from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Deque, Dict, List, Optional, Tuple


@dataclass
class Step:
    iteration: int
    tool: str
    args: Dict[str, Any]
    error: Optional[str]
    observation: Optional[Any]


@dataclass
class RunResult:
    iterations: int
    terminated_reason: Optional[str]
    steps: List[Step]


class StubAgent:
    """Planner that repeats the same failing call until it sees a success.

    If `valid_after` is provided, the agent switches to valid args on or after
    that iteration to simulate genuine progress.
    """

    def __init__(self, valid_after: Optional[int] = None) -> None:
        self.valid_after = valid_after

    def next_action(self, iteration: int, last_error: Optional[str]) -> Tuple[str, Dict[str, Any]]:
        if self.valid_after is not None and iteration >= self.valid_after:
            return "search_db", {"query": "valid"}
        return "search_db", {"query": "invalid"}


class ProgressGuard:
    """Detects no-progress loops via repeated step signatures."""

    def __init__(self, window_size: int = 5, threshold: int = 3) -> None:
        self.window: Deque[Tuple[str, Tuple[Tuple[str, Any], ...], Optional[str], Optional[str]]] = deque(
            maxlen=window_size
        )
        self.threshold = threshold

    def record(self, step: Step) -> Optional[str]:
        signature = (
            step.tool,
            tuple(sorted(step.args.items())),
            step.error,
            str(step.observation) if step.observation is not None else None,
        )
        self.window.append(signature)

        if len(self.window) < self.threshold:
            return None

        recent = list(self.window)[-self.threshold :]
        if len(set(recent)) == 1:
            return "no_progress_detected"
        return None


def search_db(args: Dict[str, Any]) -> str:
    if args.get("query") == "valid":
        return "result:ok"
    raise ValueError("ValidationError: invalid query payload")


def run_without_progress_guard(max_iterations: int = 5) -> RunResult:
    agent = StubAgent()
    steps: List[Step] = []
    terminated_reason: Optional[str] = None
    last_error: Optional[str] = None

    for iteration in range(1, max_iterations + 1):
        tool, args = agent.next_action(iteration, last_error)
        error: Optional[str] = None
        observation: Optional[str] = None

        try:
            observation = search_db(args)
        except ValueError as exc:  # deterministic failure for invalid args
            error = str(exc)

        steps.append(
            Step(
                iteration=iteration,
                tool=tool,
                args=args,
                error=error,
                observation=observation,
            )
        )

        last_error = error

        if error is None:
            terminated_reason = "succeeded"
            break

    if terminated_reason is None:
        terminated_reason = "iteration_limit"

    return RunResult(iterations=len(steps), terminated_reason=terminated_reason, steps=steps)


def run_with_progress_guard(
    max_iterations: int = 5,
    window_size: int = 5,
    threshold: int = 3,
    valid_after: Optional[int] = None,
) -> RunResult:
    agent = StubAgent(valid_after=valid_after)
    guard = ProgressGuard(window_size=window_size, threshold=threshold)
    steps: List[Step] = []
    terminated_reason: Optional[str] = None
    last_error: Optional[str] = None

    for iteration in range(1, max_iterations + 1):
        tool, args = agent.next_action(iteration, last_error)
        error: Optional[str] = None
        observation: Optional[str] = None

        try:
            observation = search_db(args)
        except ValueError as exc:
            error = str(exc)

        step = Step(
            iteration=iteration,
            tool=tool,
            args=args,
            error=error,
            observation=observation,
        )
        steps.append(step)
        last_error = error

        guard_reason = guard.record(step)

        if error is None:
            terminated_reason = "succeeded"
            break
        if guard_reason is not None:
            terminated_reason = guard_reason
            break

    if terminated_reason is None:
        terminated_reason = "iteration_limit"

    return RunResult(iterations=len(steps), terminated_reason=terminated_reason, steps=steps)
