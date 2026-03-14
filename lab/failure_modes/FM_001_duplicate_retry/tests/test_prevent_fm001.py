import pytest

from failure_modes.FM_001_duplicate_retry.scenario import run_guarded_with_commit_boundary


@pytest.mark.parametrize(
    "lease_seconds,work_duration_seconds",
    [
        (1, 2),
        (1, 3),
        (2, 3),
    ],
)
def test_prevent_fm001_idempotent_commit_preserves_inv001(
    lease_seconds: int,
    work_duration_seconds: int,
    experiment_log,
):
    """FM_001 prevention: COMMITTED boundary no-ops duplicate retry attempts."""
    result = run_guarded_with_commit_boundary(
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

    assert result.effects_count == 1
    assert result.committed_exec_id is not None
