from __future__ import annotations

from dataclasses import dataclass

from .clock import Clock
from .state import Store


@dataclass(frozen=True)
class ReconcileResult:
    """Deterministic summary of recovery changes."""

    finalized_exec_ids: list[str]
    aborted_exec_ids: list[str]


def reconcile_after_crash(*, store: Store, clock: Clock) -> ReconcileResult:
    """Restore correctness after crash/timeouts.

    Rules (minimum for FM_001):
    - COMMITTED but not DONE executions are finalized to DONE.
    - Expired LEASED/IN_PROGRESS executions are marked ABORTED.
    """
    finalized: list[str] = []
    aborted: list[str] = []

    for exec_id in store.list_exec_ids_by_status("COMMITTED"):
        store.mark_finished(exec_id)
        finalized.append(exec_id)

    now = clock.now()
    for exec_id, record in store.executions.items():
        if record.status in {"LEASED", "IN_PROGRESS"} and record.lease_expires_at <= now:
            record.status = "ABORTED"
            if store.get_committed_exec_id(record.job_id) is None:
                store.jobs[record.job_id]["state"] = "PENDING"
            aborted.append(exec_id)

    return ReconcileResult(finalized_exec_ids=finalized, aborted_exec_ids=aborted)
