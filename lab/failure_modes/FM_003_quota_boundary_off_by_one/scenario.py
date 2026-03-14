from __future__ import annotations

from dataclasses import dataclass

from policies.budget import PeerReservationQuota


@dataclass(frozen=True)
class ScenarioResult:
    peer_id: str
    max_reservations_per_peer: int
    active_reservations: int
    accepted_requests: int
    rejected_requests: int


def _run_internal(
    *,
    max_reservations_per_peer: int,
    reservation_requests: int,
    peer_id: str,
    enforce_inclusive_boundary: bool,
) -> ScenarioResult:
    quota = PeerReservationQuota(
        max_reservations_per_peer=max_reservations_per_peer,
        enforce_inclusive_boundary=enforce_inclusive_boundary,
    )

    accepted_requests = 0
    for _ in range(reservation_requests):
        if quota.try_reserve(peer_id=peer_id):
            accepted_requests += 1

    active_reservations = quota.active_reservations(peer_id=peer_id)
    return ScenarioResult(
        peer_id=peer_id,
        max_reservations_per_peer=max_reservations_per_peer,
        active_reservations=active_reservations,
        accepted_requests=accepted_requests,
        rejected_requests=quota.rejected_requests,
    )


def run_known_broken_baseline(
    *,
    max_reservations_per_peer: int,
    reservation_requests: int,
    peer_id: str,
) -> ScenarioResult:
    """Baseline path with strict `>` boundary check (expected off-by-one admission)."""
    return _run_internal(
        max_reservations_per_peer=max_reservations_per_peer,
        reservation_requests=reservation_requests,
        peer_id=peer_id,
        enforce_inclusive_boundary=False,
    )


def run_guarded_with_inclusive_boundary_check(
    *,
    max_reservations_per_peer: int,
    reservation_requests: int,
    peer_id: str,
) -> ScenarioResult:
    """Prevention path with inclusive `>=` boundary check enforcing configured quota."""
    return _run_internal(
        max_reservations_per_peer=max_reservations_per_peer,
        reservation_requests=reservation_requests,
        peer_id=peer_id,
        enforce_inclusive_boundary=True,
    )
