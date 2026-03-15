# Scope

This repository is a **reliability methodology lab**.

Current runtime systems (modelling a narrow domain to reproduce the failure):

- **Experiment 01: Job Queue**
- **Experiment 02: Pagination Cookie Registry**
- **Experiment 03: Per-Peer Quota Admission**

---

## In scope

This system models (see [`state_model`](./02_state_model.md)):

- Asynchronous job processing
- At-least-once delivery semantics
- Duplicate job execution
- Partial execution / partial writes
- Worker crashes mid-task
- Retry behavior (including retry storms)
- Recovery after downtime
- Post-failure reconciliation

Focus: **correctness under failure** (see [`invariants`](./01_invariants.md)), not performance or scale.

How to read this: experiments are runtimes; failure modes (`FM_XXX`) are bundles that run on a runtime. Multiple FMs can share a runtime (e.g., FM_001 on Experiment 01, FM_002 on Experiment 02, FM_003/FM_004 on Experiment 03, FM_008 exercises an authorization harness rather than adding a new runtime).

Default approach: add new `FM_XXX` scenarios inside Experiment 01 until a failure mode cannot be represented faithfully in the queue model, then introduce a new experiment runtime.

---

## Out of scope

Intentionally excluded:

- Performance optimization / benchmarking
- Horizontal scaling and HA guarantees
- Load balancing strategies
- UI/dashboards
- Authn/authz
- Network-level partitions (initially)
- Consensus algorithms
- **Exactly-once delivery claims** (we model at-least-once + idempotency boundaries instead)

A new runtime/experiment is out of scope by default unless justified by a concrete failure mode + invariant gap.

---

## Design constraints

Each change must satisfy at least one:

- Introduce a new failure mode
- Improve detection of an existing failure mode
- Prevent state corruption
- Enable safe recovery

Adding a new experiment/runtime requires explicit justification:

- The target failure mode cannot be modeled with queue + policies + deterministic fault injection, **or**
- The invariant depends on system/protocol properties absent from Experiment 01.

---

## Guiding assumption

- We prefer deterministic proofs over best-effort recovery
- Failure is not an exception. Failure is the **normal operating condition** under which the system must remain correct.
