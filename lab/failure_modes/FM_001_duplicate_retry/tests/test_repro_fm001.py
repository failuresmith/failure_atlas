import pytest

from failure_modes.FM_001_duplicate_retry.scenario import run_known_broken_baseline


@pytest.mark.parametrize(
    "lease_seconds,work_duration_seconds",
    [
        (1, 2),
        (1, 3),
        (2, 3),
    ],
)
def test_repro_fm001_duplicate_effect_occurs_without_commit_boundary(
    lease_seconds: int,
    work_duration_seconds: int,
    experiment_log,
):
    """FM_001 repro: retry after timeout causes duplicate logical effect (violates INV_001)."""
    result = run_known_broken_baseline(
        lease_seconds=lease_seconds,
        work_duration_seconds=work_duration_seconds,
    )

    experiment_log(
        {
            "lease_seconds": lease_seconds,
            "work_duration_seconds": work_duration_seconds,
            "effects_count": result.effects_count,
        }
    )

    assert result.effects_count == 2
    assert result.committed_exec_id is not None
