from failure_modes.FM_011_progress_stall_loop.scenario import run_with_progress_guard


def test_fm011_happy_path_progress_resets_guard(experiment_log):
    """Guard does not trigger when the agent changes arguments and succeeds."""
    result = run_with_progress_guard(
        max_iterations=5, window_size=4, threshold=3, valid_after=3
    )

    experiment_log(
        {
            "iterations": result.iterations,
            "terminated_reason": result.terminated_reason,
            "step_signature": [
                (step.tool, tuple(sorted(step.args.items())), step.error)
                for step in result.steps
            ],
        }
    )

    assert result.terminated_reason == "succeeded"
    assert result.iterations == 3
    assert any(step.error is None for step in result.steps)
