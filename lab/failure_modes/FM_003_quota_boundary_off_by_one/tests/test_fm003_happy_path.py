from failure_modes.FM_003_quota_boundary_off_by_one.scenario import run_guarded_with_inclusive_boundary_check


def test_happy_path_fm003_reservations_stay_within_quota(experiment_log):
    """Happy path: inclusive guard keeps per-peer reservations within limit."""
    result = run_guarded_with_inclusive_boundary_check(
        max_reservations_per_peer=3,
        reservation_requests=2,
        peer_id="peer-friendly",
    )

    experiment_log(
        {
            "max_reservations_per_peer": 3,
            "reservation_requests": 2,
            "active_reservations": result.active_reservations,
            "rejected_requests": result.rejected_requests,
        }
    )

    assert result.active_reservations == 2
    assert result.rejected_requests == 0
    assert result.active_reservations <= result.max_reservations_per_peer
