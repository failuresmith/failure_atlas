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

## INV_006 — Remote request-driven state growth is bounded

For protocol surfaces reachable by untrusted remote peers:

- server-maintained request-derived state must have explicit upper bounds
- protocol-compliant traffic must not induce unbounded growth
- overflow behavior (evict/reject/expire) must be deterministic and auditable

## INV_007 — Per-principal active allocations respect configured quotas

For any principal identity (peer/tenant/actor):

- active allocations must always satisfy `active <= configured_max`
- admission logic must enforce inclusive boundary semantics at exact limits
- boundary conditions (`0`, `1`, `N`) require explicit regression coverage

## INV_008 — Participant identity mapping is bijective

For any participant registry using credentials (e.g., TLS keys):

- each TLS key maps to exactly one participant identifier
- participant identifiers are unique (`participant_id ↔ credential` is one-to-one)
- startup must fail fast on duplicate participant IDs or duplicate credentials
- registries must not silently overwrite existing mappings

---

## Pipeline mapping

Invariants anchor the manufacturing pipeline:

`FM → FP → GR`

- FM proves how an invariant can fail
- FP explains the recurring mechanism
- GR enforces the invariant-preserving guardrail
