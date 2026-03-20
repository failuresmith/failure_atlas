from __future__ import annotations

from dataclasses import dataclass
from typing import List

WRITE_TOOLS = [
    "write_file",
    "edit_file",
    "create_directory",
    "move_file",
]
READ_TOOLS = [
    "read_file",
    "list_directory",
]


@dataclass(frozen=True)
class ScenarioResult:
    exposed_tools: List[str]
    read_only: bool


class BaselineToolRegistry:
    def __init__(self, *, read_only: bool) -> None:
        self.read_only = read_only

    def list_tools(self) -> List[str]:
        # Baseline ignores read_only and exposes everything.
        return READ_TOOLS + WRITE_TOOLS


class GuardedToolRegistry:
    def __init__(self, *, read_only: bool) -> None:
        self.read_only = read_only

    def list_tools(self) -> List[str]:
        if self.read_only:
            return list(READ_TOOLS)
        return READ_TOOLS + WRITE_TOOLS


def run_baseline_with_read_only_flag(read_only: bool = True) -> ScenarioResult:
    registry = BaselineToolRegistry(read_only=read_only)
    return ScenarioResult(exposed_tools=registry.list_tools(), read_only=read_only)


def run_guarded_read_only_registry(read_only: bool = True) -> ScenarioResult:
    registry = GuardedToolRegistry(read_only=read_only)
    return ScenarioResult(exposed_tools=registry.list_tools(), read_only=read_only)


def run_happy_path_full_tools() -> ScenarioResult:
    registry = GuardedToolRegistry(read_only=False)
    return ScenarioResult(exposed_tools=registry.list_tools(), read_only=False)
