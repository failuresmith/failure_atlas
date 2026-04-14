# [FM-001] Duplicate Execution After Retry Timeout
**Pattern:** State & Data Integrity

**The Failure**
A background job takes longer than its lease/timeout. The system assumes the worker died and assigns the job to another worker. Both workers eventually finish and apply the same side effect (e.g., charging a customer twice).

**Mechanism**
"At-least-once" delivery semantics without a durable idempotency boundary. The timeout is used as a proxy for failure, but in distributed systems, a timeout does not guarantee that the work isn't still in progress or already completed.

**Reproduction**
```python
# Worker A takes lease, but hangs/slows down
job = queue.acquire(lease_time=30)

# System thinks A is dead, gives job to B
# B finishes and commits
queue.retry(job_id)
db.execute("UPDATE account SET balance = balance - 100")

# Worker A wakes up and also commits
db.execute("UPDATE account SET balance = balance - 100")
# Result: -200 instead of -100
```
Full reproduction: `lab/state_concurrency/duplicate_retry_timeout/`

**Remediation**
Implement a durable "Commit Boundary". Use a unique constraint (e.g., `request_id` or `job_id`) in the database to ensure that only the first attempt to commit the side effect succeeds. Subsequent attempts for the same `job_id` must no-op or return the original result.
