from failure_modes.FM_001_duplicate_retry.scenario import run_single_worker_happy_path


def test_happy_path_fm001_single_worker_finishes_once(experiment_log):
    """Happy path: one worker completes within lease, guardrail still intact."""
    result = run_single_worker_happy_path(lease_seconds=5, work_duration_seconds=1)

    experiment_log(
        {
            "lease_seconds": 5,
            "work_duration_seconds": 1,
            "effects_count": result.effects_count,
            "committed_exec_id": result.committed_exec_id,
        }
    )

    assert result.effects_count == 1
    assert result.committed_exec_id is not None
