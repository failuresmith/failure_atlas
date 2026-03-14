# Invariants

This document defines the **non-negotiable correctness guarantees** across the
Failure Atlas pipeline.

An invariant is a property that must hold **before, during, and after failure**.
If an invariant is violated, the system is incorrect even if it appears available.

---

## INV_001 — Job execution is logically idempotent

A job may be delivered/executed more than once, but its **logical effect** must
be applied at most once.

- duplicate execution must not amplify side effects
- idempotency must be enforced explicitly, not assumed

## INV_002 — Partial execution must not leave irreversible damage

If a worker crashes mid-execution:

- partial progress must be detectable
- resume/compensate paths must be safe
- irreversible action requires durable confirmation

## INV_003 — State transitions are monotonic and explicit

State changes must be:

- persisted
- observable
- auditable

No hidden/implicit transitions.

## INV_004 — Recovery restores correctness, not only availability

After recovery, the system must not:

- lie about completed work
- silently drop work
- duplicate irreversible effects

## INV_005 — Failure must be detectable

For every known failure mode there must be a clear, machine-detectable signal.

---

## Pipeline mapping

Invariants anchor the manufacturing pipeline:

`FM → FP → GR`

- FM proves how an invariant can fail
- FP explains the recurring mechanism
- GR enforces the invariant-preserving guardrail
