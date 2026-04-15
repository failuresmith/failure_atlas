[<- Index](../../README.md)
# [FM-009] Progress Stall Detection Gap
**Pattern:** Control Flow & Logic

**The Failure**
An AI agent gets stuck in a loop calling the same tool with the same failing arguments over and over. It burns through its budget (and your API credits) because the only thing stopping it is a high "max iterations" limit.

**Mechanism**
"Progress Ledger Omission". The agent loop tracks *how many* steps it has taken, but not *what* happened in those steps. If the last 3 steps are identical (same tool, same error), it is "stalled", but the loop continues until the iteration count hits the hard cap.

**Coding Example**
```python
def agent_loop_unsafe():
    max_iterations = 10

    for step in range(max_iterations):
        action = ("read_file", {"id": "invalid-123"})
        result = "Error: invalid ID"

        record_iteration_count(step)
        # BUG:
        # loop tracks how many steps happened,
        # but not whether the same action produced the same result again

        try_again(action)


agent_loop_unsafe()
# FAILURE:
# budget is consumed even though the system is clearly stuck


def agent_loop_safe():
    recent_action_results = []

    for step in range(10):
        action = ("read_file", {"id": "invalid-123"})
        result = "Error: invalid ID"
        action_result = (action, result)

        if repeated_too_many_times(action_result, recent_action_results):
            return stop_with_stall_detected()

        recent_action_results.append(action_result)
```

**Invariant Violated**
Each agent step must either make progress, change strategy, or terminate.

**Remediation**
Implement a "Progress Guard". Maintain a small buffer of the last N actions and observations. If the agent repeats the exact same action and receives the exact same observation/error multiple times, terminate early with a `StallDetected` error.

**Invariant Restored**
The control loop is progress-aware. Repeated non-progressing states are converted into termination or escalation instead of unlimited retries.

**References**

- [Langchain Issue #36139](https://github.com/langchain-ai/langchain/issues/36139)