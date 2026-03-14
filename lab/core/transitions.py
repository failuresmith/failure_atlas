from __future__ import annotations

from dataclasses import dataclass

from .clock import Clock
from .faults import Faults
from .state import Store


@dataclass(frozen=True)
class Lease:
    exec_id: str
    job_id: str
    worker_id: str


class Queue:
    """Minimal queue with at-least-once lease semantics."""

    def __init__(self, *, store: Store, clock: Clock, lease_seconds: int) -> None:
        self.store = store
        self.clock = clock
        self.lease_seconds = lease_seconds

    def submit_job(self, *, payload: dict) -> str:
        return self.store.create_job(payload=payload)

    def lease(self, *, worker_id: str) -> Lease | None:
        now = self.clock.now()
        for job_id in self.store.job_order:
            if self.store.can_lease(job_id=job_id, now=now):
                exec_id = self.store.create_lease(
                    job_id=job_id,
                    worker_id=worker_id,
                    lease_seconds=self.lease_seconds,
                )
                return Lease(exec_id=exec_id, job_id=job_id, worker_id=worker_id)
        return None


class Worker:
    """Minimal worker that reproduces/prevents failures via deterministic faults."""

    def __init__(
        self,
        *,
        worker_id: str,
        store: Store,
        queue: Queue,
        clock: Clock,
        faults: Faults,
    ) -> None:
        self.worker_id = worker_id
        self.store = store
        self.queue = queue
        self.clock = clock
        self.faults = faults

    def start(self, lease: Lease) -> None:
        self.store.mark_started(lease.exec_id)

    def finish(self, lease: Lease) -> None:
        if self.faults.crash_before_commit:
            return

        self.store.apply_effect(
            exec_id=lease.exec_id,
            enforce_idempotent_commit=self.faults.enforce_idempotent_commit,
        )

        if self.faults.crash_after_commit_before_done:
            return

        self.store.mark_finished(lease.exec_id)
