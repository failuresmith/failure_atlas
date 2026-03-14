from failure_modes.FM_002_unbounded_pagination_state.scenario import run_known_broken_baseline


def test_repro_fm002_unbounded_cookie_state_exceeds_budget():
    """FM_002 repro: repeated discover requests grow cookie state beyond safe budget."""
    result = run_known_broken_baseline(
        discover_requests=10,
        max_cookie_budget=3,
    )

    assert result.cookie_count == 10
    assert result.cookie_count > result.max_cookie_budget
    assert result.evicted_count == 0
