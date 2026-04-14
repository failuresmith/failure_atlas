# [FM-009] Progress Stall Detection Gap
**Pattern:** Control Flow & Logic

**The Failure**
An AI agent gets stuck in a loop calling the same tool with the same failing arguments over and over. It burns through its budget (and your API credits) because the only thing stopping it is a high "max iterations" limit.

**Mechanism**
"Progress Ledger Omission". The agent loop tracks *how many* steps it has taken, but not *what* happened in those steps. If the last 3 steps are identical (same tool, same error), it is "stalled", but the loop continues until the iteration count hits the hard cap.

**Reproduction**
```python
# Agent loop
for i in range(10):
    # Model keeps trying the same invalid argument
    result = tool.call(id="invalid-123")
    print(f"Step {i}: Error {result.error}")

    # FAILURE: No check if we are doing the same thing repeatedly
```
Full reproduction: `lab/logic_calculation/progress_stall_loop/`

**Remediation**
Implement a "Progress Guard". Maintain a small buffer of the last N actions and observations. If the agent repeats the exact same action and receives the exact same observation/error multiple times, terminate early with a `StallDetected` error.
