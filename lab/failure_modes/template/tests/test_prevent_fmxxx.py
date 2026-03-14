from failure_modes.template.scenario import run
from faults.injectors import Faults


def test_prevent_fmxxx_fix_preserves_invariants(experiment_log):
    faults = Faults(enforce_idempotent_commit=True)

    result = run(
        lease_seconds=1,
        work_duration_seconds=2,
        faults=faults,
    )

    experiment_log(
        {
            "lease_seconds": 1,
            "work_duration_seconds": 2,
            "effects_count": result.effects_count,
            "committed_exec_id": result.committed_exec_id,
        }
    )

    # After the fix, the invariant-preserving behavior is asserted.
    assert result.effects_count == 1
    assert result.committed_exec_id is not None
