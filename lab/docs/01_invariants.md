# Invariants 

This document defines the **non-negotiable correctness guarantees** of the system.

An invariant is a property that must hold **before, during and after failure**.
If an invariant is violated, the system is considered incorrect -- even if it appears to be functioning.

--- 

## INV_001 -- Job execution is logically idempotent 

A job may be delivered or executed more than once, but its **logical effect** must be applied at most once.

- Duplicate execution must not corrupt state 
- Duplicate execution must not amplify side effects 
- Idempotency must be enforced explicitly, not assumed
- Job-level completion is **derived** from execution records (see [`state_model`](./02_state_model.md)); we do not mutate job state independently of executions.

--- 

## INV_002 -- Partial execution must not leave irreversible damage 

If a worker crashes mid-execution:

- The system must be able to detect partial progress 
- The system must be able to safely resume or compensate 
- No irreversible action may occur without durable confirmation
- Observability comes from the durable execution state machine (see [`state_model`](./02_state_model.md)); job state is an aggregate projection over those records, ensuring crashes are detectable without guessing job status.

Crash consistency is mandatory.

--- 

## INV_003 -- Job state transitions are monotonic and explicit 

Job state must move forward through **well-defined transitions**.

- No implicit state transitions
- No inferred completion
- No hidden side effects 

Every state change must be:
- persisted 
- observable 
- auditable 

--- 

## INV_004 -- Recovery restores correctness, not just availability

After recovery:

- The system must not lie about completed work 
- The system must not silently drop work 
- The system must not duplicate irreversible effects 

A system that resumes processing but violates correctness is considered failed.

--- 

## INV_005 -- Failure must be detectable 

Silent failure is the most dangerous failure mode.

For every known failure:
- there must be a detectable signal 
- detection must not rely on manual inspection
- ambiguity must be treated as failure 

---

## INV_006 -- Remote request-driven state growth must be bounded

For protocol surfaces reachable by untrusted remote peers:

- server-maintained per-request state must have explicit upper bounds
- growth must not be unbounded under protocol-compliant traffic
- overflow behavior (evict/reject/expire) must be deterministic and auditable

---

## INV_007 -- Per-principal active allocations must not exceed quota

For any principal identity (peer/tenant/actor):

- active allocations must satisfy `active <= configured_max`
- admission checks must enforce inclusive boundaries at exact limits
- boundary behavior must be covered by deterministic regression tests (`0`, `1`, `N`)

---

## INV_008 -- Participant identity mapping must be bijective

For participant registries keyed by credentials (e.g., TLS keys):

- each credential maps to exactly one participant ID
- participant IDs must be globally unique
- startup must fail fast on duplicate IDs or duplicate credentials
- registries must not silently overwrite prior mappings

---

## INV_009 -- Tool execution authority must be enforced outside model reasoning

For LLM-driven tool runtimes:

- tool execution must pass deterministic runtime authorization checks
- sensitive tools require explicit policy authorization independent of prompt text
- model planning output must not directly grant privileged execution rights
- denied tool calls must produce auditable policy events

--- 

# Invariant discipline

- Every failure mode must reference the invariant(s) it violates 
- Every test must assert invariant preservation 
- Every recovery mechanism must explicitly restore invariants 

If an invariant cannot be enforced, it must be revised -- not ignored.

--- 

**Cross-links**

- ["State Model"](./02_state_model.md) 
- ["Policies"](./03_policies.md) 