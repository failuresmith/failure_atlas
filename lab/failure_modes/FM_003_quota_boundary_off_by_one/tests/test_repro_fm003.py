import pytest

from failure_modes.FM_003_quota_boundary_off_by_one.scenario import run_known_broken_baseline


@pytest.mark.parametrize("max_reservations_per_peer", [0, 1, 3])
def test_repro_fm003_strict_comparator_allows_one_extra_reservation(
    max_reservations_per_peer: int, experiment_log
):
    """FM_003 repro: strict `>` quota check admits one extra allocation at boundary."""
    result = run_known_broken_baseline(
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

    assert result.active_reservations == max_reservations_per_peer + 1
    assert result.active_reservations > result.max_reservations_per_peer
    assert result.rejected_requests == 1
