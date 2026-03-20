# PM_006 — Quota boundary off-by-one admission

## Summary
Per-peer reservation admission used a strict-greater (`>`) comparator. When a peer reached the configured max and sent one more request, the check passed and admitted a `max + 1` reservation. This field bug motivated FM_003/FP_006.

## Impact
- Violated `INV_007` (per-principal allocations must not exceed quota)
- Policy compliance silently breached at the boundary
- Fairness guarantees weakened; capacity planning skewed

## Timeline (deterministic reproduction)
1. Configure `max_reservations_per_peer = 1`.
2. Peer submits first reservation → accepted.
3. Peer submits second reservation at boundary.
4. Strict `current > max` check evaluates false; second admission succeeds → `active = 2`.

## Root cause
- Boundary guard used `>` instead of `>=`.
- No explicit boundary regression tests; edge condition unprotected.

## Detection
- `active_reservations(peer_id) > max_reservations_per_peer`
- Boundary-focused regression matrix (`max=0,1,N`) fails

## Corrective actions
1. Switched admission guard to inclusive comparator (`>=`).
2. Added boundary regression tests to lock policy semantics.

## Verification
- `test_repro_fm003.py` demonstrates over-admission at the boundary.
- `test_prevent_fm003.py` proves inclusive guard holds the limit.

## Occurrences
- Relay v2 reservation admission used strict `>` comparator, allowing `max + 1` reservation for a peer.

## Links
- Failure mode: `lab/failure_modes/FM_003_quota_boundary_off_by_one/`
- Failure pattern: `atlas/FP_006_quota_boundary_off_by_one_admission.md`
- Guardrail: `guardrails/GR_006_inclusive_quota_boundary_checks.md`
