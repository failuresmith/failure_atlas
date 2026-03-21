from failure_modes.FM_005_unbounded_pagination_state.scenario import run_guarded_with_bounded_cookie_registry


def test_happy_path_fm002_cookie_budget_not_exceeded(experiment_log):
    """Happy path: bounded registry within budget under normal request volume."""
    result = run_guarded_with_bounded_cookie_registry(
        discover_requests=2,
        max_cookie_budget=5,
    )

    experiment_log(
        {
            "discover_requests": 2,
            "max_cookie_budget": 5,
            "cookie_count": result.cookie_count,
            "evicted_count": result.evicted_count,
        }
    )

    assert result.cookie_count == 2
    assert result.cookie_count <= result.max_cookie_budget
    assert result.evicted_count == 0
