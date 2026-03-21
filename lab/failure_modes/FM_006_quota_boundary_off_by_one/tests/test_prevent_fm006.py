import pytest

from failure_modes.FM_006_quota_boundary_off_by_one.scenario import run_guarded_with_inclusive_boundary_check


@pytest.mark.parametrize("max_reservations_per_peer", [0, 1, 3])
def test_prevent_fm003_inclusive_comparator_enforces_quota(
    max_reservations_per_peer: int, experiment_log
):
    """FM_006 prevention: inclusive `>=` guard preserves per-peer quota invariant."""
    result = run_guarded_with_inclusive_boundary_check(
        max_reservations_per_peer=max_reservations_per_peer,
        reservation_requests=max_reservations_per_peer + 2,
        peer_id="peer-attacker",
    )

    experiment_log(
        {
            "max_reservations_per_peer": max_reservations_per_peer,
            "reservation_requests": max_reservations_per_peer + 2,
            "active_reservations": result.active_reservations,
            "rejected_requests": result.rejected_requests,
        }
    )

    assert result.active_reservations == max_reservations_per_peer
    assert result.active_reservations <= result.max_reservations_per_peer
    assert result.rejected_requests == 2
