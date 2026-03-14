from __future__ import annotations

from .state import Store


def inv_001_job_effect_applied_at_most_once(*, store: Store, job_id: str) -> bool:
    """INV_001: a logical job's side effect is applied at most once."""
    return store.count_effects(job_id) <= 1


def inv_003_job_state_is_terminal_after_done(*, store: Store, job_id: str) -> bool:
    """INV_003: if any execution is DONE, projected job state is SUCCEEDED."""
    done_exists = any(
        store.executions[exec_id].status == "DONE" for exec_id in store.execs_by_job.get(job_id, [])
    )
    if not done_exists:
        return True
    return store.jobs[job_id]["state"] == "SUCCEEDED"
