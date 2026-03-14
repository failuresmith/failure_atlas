from __future__ import annotations

from dataclasses import dataclass

from policies.budget import CookieRegistry


@dataclass(frozen=True)
class ScenarioResult:
    cookie_count: int
    max_cookie_budget: int
    evicted_count: int


def _run_internal(*, discover_requests: int, max_cookie_budget: int, enforce_budget: bool) -> ScenarioResult:
    registry = CookieRegistry(max_entries=max_cookie_budget)

    for i in range(discover_requests):
        cookie = f"cookie-{i + 1}"
        registrations = {f"reg-{i + 1}"}
        registry.insert(cookie=cookie, registrations=registrations, enforce_budget=enforce_budget)

    return ScenarioResult(
        cookie_count=registry.count(),
        max_cookie_budget=max_cookie_budget,
        evicted_count=registry.evicted_count,
    )


def run_known_broken_baseline(*, discover_requests: int, max_cookie_budget: int) -> ScenarioResult:
    """Baseline path with no budget enforcement (expected growth beyond budget)."""
    return _run_internal(
        discover_requests=discover_requests,
        max_cookie_budget=max_cookie_budget,
        enforce_budget=False,
    )


def run_guarded_with_bounded_cookie_registry(*, discover_requests: int, max_cookie_budget: int) -> ScenarioResult:
    """Prevention path with deterministic FIFO budget enforcement enabled."""
    return _run_internal(
        discover_requests=discover_requests,
        max_cookie_budget=max_cookie_budget,
        enforce_budget=True,
    )
