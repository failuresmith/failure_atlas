from failure_modes.FM_011_progress_stall_loop.scenario import run_with_progress_guard


def test_prevent_fm011_guard_terminates_on_no_progress(experiment_log):
    """Guard halts after threshold repeated failures with explicit reason."""
    result = run_with_progress_guard(max_iterations=6, window_size=4, threshold=3)

    experiment_log(
        {
            "iterations": result.iterations,
            "terminated_reason": result.terminated_reason,
            "step_errors": [step.error for step in result.steps],
        }
    )

    assert result.terminated_reason == "no_progress_detected"
    assert result.iterations == 3
    assert all(step.error is not None for step in result.steps)
