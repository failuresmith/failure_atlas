---
ID: FM_006
Title: Per-peer reservation quota off-by-one at boundary
Hypothesis: A strict-greater (`>`) admission check allows one extra reservation when active count equals configured maximum.
Invariant: INV_007
Status: validated
related_pattern:
  - FP_006
---

# FM_006 — Per-peer reservation quota off-by-one at boundary

## Description

Per-peer quota enforcement can fail at the exact limit if the admission guard uses strict-greater (`>`) instead of greater-or-equal (`>=`), allowing one extra allocation beyond policy.

## Trigger

1. A peer reaches `active_reservations == max_reservations_per_peer`.
2. The same peer submits another reservation request.
3. Admission check uses `current > max`.

## Preconditions

- resource admission is performed per peer identity
- quota check executes before incrementing active count
- comparator semantics are configurable/implemented incorrectly

## Failure mechanism (step-by-step)

1. Peer submits requests up to the configured max.
2. At boundary (`current == max`), strict comparator evaluates false.
3. Request is accepted and count increments to `max + 1`.
4. Policy intent (`active <= max`) is violated.

## Symptoms

- active reservations for one peer become `max + 1`
- boundary-only failures (often invisible under non-edge traffic)
- per-peer fairness/resource guarantees weaken

## Violated invariants

- INV_007 — per-principal active allocations must not exceed configured quota.
- INV_005 — admission policy violations must be machine-detectable.

## Detection

- `active_reservations(peer_id) > max_reservations_per_peer`
- boundary regression tests at `max=0`, `max=1`, and `max=N`

## Recovery / prevention strategy

- enforce inclusive comparator (`>=`) in pre-admission guard
- keep boundary regression tests as permanent policy contract tests

## Acceptance criteria

- `test_repro_fm003.py` proves strict comparator admits one extra reservation
- `test_prevent_fm003.py` proves inclusive comparator enforces the configured limit

## Notes

This FM isolates admission-boundary semantics only; it intentionally excludes connection lifecycle complexity to keep mechanism legible and deterministic.
