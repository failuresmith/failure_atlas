import pytest

from failure_modes.FM_009_progress_stall_loop.scenario import run_without_progress_guard


@pytest.mark.parametrize("max_iterations", [3, 5, 7])
def test_repro_fm011_agent_spins_until_iteration_cap(max_iterations: int, experiment_log):
    """FM_009 repro: identical failing tool call consumes the full iteration budget."""
    result = run_without_progress_guard(max_iterations=max_iterations)

    experiment_log(
        {
            "max_iterations": max_iterations,
            "observed_iterations": result.iterations,
            "terminated_reason": result.terminated_reason,
            "unique_signatures": len(
                {
                    (step.tool, tuple(sorted(step.args.items())), step.error)
                    for step in result.steps
                }
            ),
        }
    )

    assert result.iterations == max_iterations
    assert result.terminated_reason == "iteration_limit"
    assert len(result.steps) == max_iterations
    # All steps are identical: same tool, args, and error.
    assert (
        len(
            {
                (step.tool, tuple(sorted(step.args.items())), step.error)
                for step in result.steps
            }
        )
        == 1
    )
