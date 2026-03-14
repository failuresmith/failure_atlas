from failure_modes.FM_002_unbounded_pagination_state.scenario import run_guarded_with_bounded_cookie_registry


def test_prevent_fm002_bounded_cookie_registry_preserves_budget_invariant(experiment_log):
    """FM_002 prevention: bounded registry keeps cookie state within configured cap."""
    result = run_guarded_with_bounded_cookie_registry(
        discover_requests=10,
        max_cookie_budget=3,
    )

    experiment_log(
        {
            "discover_requests": 10,
            "max_cookie_budget": 3,
            "cookie_count": result.cookie_count,
            "evicted_count": result.evicted_count,
        }
    )

    assert result.cookie_count == 3
    assert result.cookie_count <= result.max_cookie_budget
    assert result.evicted_count == 7
