[<- Index](../../README.md)
# [FM-006] Quota Boundary Off-by-One
**Pattern:** Input Validation & Representation

**The Failure**
A system designed to limit a user to 5 active connections actually allows them to open 6. While seemingly minor, in high-scale systems this "plus one" can break capacity planning and lead to cascading failures if every user exceeds their limit.

**Mechanism**
"Exclusive vs Inclusive Boundary". The code uses `if count > max: reject` instead of `if count >= max: reject`. When the user has exactly 5 connections, the check `5 > 5` is false, so it allows the 6th connection.

**Coding Example**
```python
def admit_connection_unsafe(current_count, connection_limit):
    """Incorrect boundary: rejects only after limit is already exceeded."""
    if current_count > connection_limit:
        return reject_connection()

    return admit_connection()


current_count = 5
connection_limit = 5

admit_connection_unsafe(current_count, connection_limit)
# admitted -> FAILURE:
# user was already at 5 of 5, but the 6th connection was still allowed


def admit_connection_safe(current_count, connection_limit):
    if current_count >= connection_limit:
        return reject_connection()

    return admit_connection()
```

**Invariant Violated**
If usage is already at the configured limit, the next request must be rejected.

**Remediation**
Always use inclusive boundary checks (`>=`) for resource limits. Supplement with unit tests that specifically target the "exactly-at-limit" edge case.

**Invariant Restored**
Admission control preserves the declared capacity boundary exactly. No caller can exceed the configured quota through edge-condition math.
