# [FM-006] Quota Boundary Off-by-One
**Pattern:** Input Validation & Representation

**The Failure**
A system designed to limit a user to 5 active connections actually allows them to open 6. While seemingly minor, in high-scale systems this "plus one" can break capacity planning and lead to cascading failures if every user exceeds their limit.

**Mechanism**
"Exclusive vs Inclusive Boundary". The code uses `if count > max: reject` instead of `if count >= max: reject`. When the user has exactly 5 connections, the check `5 > 5` is false, so it allows the 6th connection.

**Reproduction**
```python
def admit_unsafe(current_count, max_limit):
    # BUG: Should be >=
    if current_count > max_limit:
        return "Reject"
    return "Admit"

# User has 5/5 connections
# 5 > 5 is False -> Admitted! Total now 6.
admit_unsafe(5, 5)
```
Full reproduction: `lab/input_validation/quota_off_by_one/`

**Remediation**
Always use inclusive boundary checks (`>=`) for resource limits. Supplement with unit tests that specifically target the "exactly-at-limit" edge case.
