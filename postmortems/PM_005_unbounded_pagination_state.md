---
ID: PM_005
Title: PM_005 — Unbounded pagination cookie state growth
Summary: |-
  Repeated DISCOVER-style requests caused the server to allocate a new pagination cookie per call without any bound or eviction. A single remote peer could grow the cookie registry until memory pressure/OOM. This was the field incident that motivated FM_005/FP_005.
---

# PM_005 — Unbounded pagination cookie state growth

## Summary
Repeated DISCOVER-style requests caused the server to allocate a new pagination cookie per call without any bound or eviction. A single remote peer could grow the cookie registry until memory pressure/OOM. This was the field incident that motivated FM_005/FP_005.

## Impact
- Violated `INV_006` (remote-driven state must be bounded)
- Memory footprint grew linearly with request volume
- Denial-of-service risk from unauthenticated traffic

## Timeline (deterministic reproduction)
1. Peer issues repeated DISCOVER requests.
2. Each request inserts a new pagination cookie in the registry.
3. No budget/eviction is enforced; `cookie_count` increases monotonically.
4. Memory pressure rises; registry exceeds intended safety budget.

## Root cause
- Pagination state table had no hard cap or eviction path.
- Assumed "typical" client behavior would keep cookie count small.

## Detection
- `cookie_count > MAX_COOKIES_TRACKED`
- Monotonic `cookie_count` growth under repeated unauthenticated requests

## Corrective actions
1. Added bounded registry guardrail (FIFO eviction) in FM_005 harness.
2. Added prevention test enforcing `cookie_count <= MAX_COOKIES_TRACKED`.

## Verification
- `test_repro_fm002.py` proves unbounded growth in the broken baseline.
- `test_prevent_fm002.py` proves bounded behavior with guardrail.

## Occurrences
- Rendezvous DISCOVER cookie handling allowed unbounded server-side cookie accumulation under repeated requests.

## Links
- Failure mode: `lab/failure_modes/FM_005_unbounded_pagination_state/`
- Failure pattern: `atlas/FP_005_unbounded_pagination_cookie_state_amplification.md`
- Guardrail: `guardrails/GR_005_bounded_pagination_state.md`
