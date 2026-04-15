[<- Index](../../README.md)
# [FM-001] Duplicate Execution After Retry Timeout
**Pattern:** State & Data Integrity

**The Failure**
A background job takes longer than its lease/timeout. The system assumes the worker died and assigns the job to another worker. Both workers eventually finish and apply the same side effect (e.g., charging a customer twice).

**Mechanism**
"At-least-once" delivery semantics without a durable idempotency boundary. The timeout is used as a proxy for failure, but in distributed systems, a timeout does not guarantee that the work isn't still in progress or already completed.

**Coding Example**
```python
committed_job_ids = set()
ledger = []


def apply_side_effect_unsafe(job_id, amount):
    charge_customer(amount)
    ledger.append((job_id, amount))


# Worker A starts job_123 and runs slowly.
# The scheduler times out A and gives the same logical job to Worker B.

apply_side_effect_unsafe("job_123", 100)  # Worker B commits first
apply_side_effect_unsafe("job_123", 100)  # Worker A wakes up and commits too

ledger
# [("job_123", 100), ("job_123", 100)] -> FAILURE:
# one logical job produced two side effects


def apply_side_effect_safe(job_id, amount):
    if job_id in committed_job_ids:
        return return_previous_result(job_id)

    charge_customer(amount)
    committed_job_ids.add(job_id)
    ledger.append((job_id, amount))
```

**Invariant Violated**
A logical job may apply its side effect at most once, regardless of retries or worker overlap.

**Remediation**
Implement a durable "Commit Boundary". Use a unique constraint (e.g., `request_id` or `job_id`) in the database to ensure that only the first attempt to commit the side effect succeeds. Subsequent attempts for the same `job_id` must no-op or return the original result.

**Invariant Restored**
Retries are safe because commit authorization is bound to job identity, not worker timing. Duplicate attempts cannot create duplicate side effects.
