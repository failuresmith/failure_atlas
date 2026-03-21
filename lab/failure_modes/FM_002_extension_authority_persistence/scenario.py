from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set


@dataclass(frozen=True)
class ScenarioResult:
    authority_after_uninstall: bool
    active_extensions: Set[str]
    registry_snapshot: Dict[str, Set[str]]


class BaselineAuthorityRegistry:
    """Registry that never revokes entries on uninstall."""

    def __init__(self) -> None:
        self._entries: Dict[str, Set[str]] = {}

    def register(self, extension_id: str, hosts: Set[str]) -> None:
        for host in hosts:
            self._entries.setdefault(host, set()).add(extension_id)

    def uninstall(self, extension_id: str) -> None:  # intentionally a no-op
        return None

    def has_authority(self, host: str) -> bool:
        return host in self._entries and len(self._entries[host]) > 0

    def snapshot(self) -> Dict[str, Set[str]]:
        return {host: set(exts) for host, exts in self._entries.items()}


class LifecycleBoundAuthorityRegistry:
    """Registry keyed by extension_id; uninstall revokes derived authority."""

    def __init__(self) -> None:
        self._ext_hosts: Dict[str, Set[str]] = {}

    def register(self, extension_id: str, hosts: Set[str]) -> None:
        self._ext_hosts.setdefault(extension_id, set()).update(hosts)

    def uninstall(self, extension_id: str) -> None:
        self._ext_hosts.pop(extension_id, None)

    def has_authority(self, host: str) -> bool:
        return any(host in hosts for hosts in self._ext_hosts.values())

    def snapshot(self) -> Dict[str, Set[str]]:
        return {ext: set(hosts) for ext, hosts in self._ext_hosts.items()}


def run_baseline_with_stale_authority(host: str) -> ScenarioResult:
    registry = BaselineAuthorityRegistry()
    registry.register(extension_id="ext-1", hosts={host})
    registry.uninstall(extension_id="ext-1")

    return ScenarioResult(
        authority_after_uninstall=registry.has_authority(host),
        active_extensions=set(),
        registry_snapshot={"by_host": set(registry.snapshot().keys())},
    )


def run_guarded_lifecycle_bound_registry(host: str) -> ScenarioResult:
    registry = LifecycleBoundAuthorityRegistry()
    registry.register(extension_id="ext-1", hosts={host})
    registry.uninstall(extension_id="ext-1")

    return ScenarioResult(
        authority_after_uninstall=registry.has_authority(host),
        active_extensions=set(registry.snapshot().keys()),
        registry_snapshot=registry.snapshot(),
    )


def run_happy_path_active_extension(host: str) -> ScenarioResult:
    registry = LifecycleBoundAuthorityRegistry()
    registry.register(extension_id="ext-1", hosts={host})

    return ScenarioResult(
        authority_after_uninstall=registry.has_authority(host),
        active_extensions=set(registry.snapshot().keys()),
        registry_snapshot=registry.snapshot(),
    )
