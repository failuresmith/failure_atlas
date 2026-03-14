from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Participant:
    participant_id: str
    tls_key: str


@dataclass(frozen=True)
class RegistryCheckResult:
    registry: dict[str, str]
    participant_count: int
    unique_participant_ids: int
    unique_tls_keys: int
    duplicate_participant_ids: list[str]
    duplicate_tls_keys: list[str]
    has_bijection: bool


def _check_bijection(participants: Iterable[Participant], *, enforce_bijection: bool) -> RegistryCheckResult:
    registry: dict[str, str] = {}
    seen_ids: set[str] = set()
    seen_tls: set[str] = set()
    duplicate_ids: set[str] = set()
    duplicate_tls: set[str] = set()

    participants_list = list(participants)

    for participant in participants_list:
        if participant.participant_id in seen_ids:
            duplicate_ids.add(participant.participant_id)
        seen_ids.add(participant.participant_id)

        if participant.tls_key in seen_tls:
            duplicate_tls.add(participant.tls_key)
        seen_tls.add(participant.tls_key)

        # Overwrite semantics mimic the buggy path; guardrail rejects before this.
        registry[participant.tls_key] = participant.participant_id

    has_bijection = len(registry) == len(participants_list) == len(seen_ids)

    if enforce_bijection and (duplicate_ids or duplicate_tls):
        raise ValueError(
            f"Duplicate identity data detected: ids={sorted(duplicate_ids)}, tls_keys={sorted(duplicate_tls)}"
        )

    return RegistryCheckResult(
        registry=registry,
        participant_count=len(participants_list),
        unique_participant_ids=len(seen_ids),
        unique_tls_keys=len(seen_tls),
        duplicate_participant_ids=sorted(duplicate_ids),
        duplicate_tls_keys=sorted(duplicate_tls),
        has_bijection=has_bijection,
    )


def run_known_broken_baseline(participants: Iterable[Participant]) -> RegistryCheckResult:
    """Baseline path: overwrite duplicates silently (expected bijection violation)."""
    return _check_bijection(participants, enforce_bijection=False)


def run_guarded_with_bijection_enforcement(participants: Iterable[Participant]) -> RegistryCheckResult:
    """Guarded path: fail fast when duplicate IDs or TLS keys are present."""
    return _check_bijection(participants, enforce_bijection=True)


def run_happy_path_unique_participants(participants: Iterable[Participant]) -> RegistryCheckResult:
    """Happy path helper with enforced bijection and unique inputs."""
    return _check_bijection(participants, enforce_bijection=True)
