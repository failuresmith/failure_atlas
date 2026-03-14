---
ID: FM_002
Title: Unbounded pagination cookie state under repeated discover requests
Hypothesis: Repeated protocol-compliant discover requests can force unbounded server-side cookie state growth when no hard state budget is enforced.
Invariant: INV_006
Status: draft
related_pattern:
  - FP_005
---

# FM_002 — Unbounded pagination cookie state under repeated discover requests

## Description

Server-side pagination that persists cookies/cursors per request can become a
remote memory amplification vector when cookie state has no enforced bound.

## Trigger

1. A remote peer sends repeated DISCOVER-style requests.
2. Each request creates a new server-side pagination cookie entry.
3. No cap/eviction/expiry budget is enforced.

## Preconditions

- pagination state is stored server-side
- cookie creation is reachable via protocol-compliant traffic
- cookie registry has no hard upper bound

## Failure mechanism (step-by-step)

1. Request arrives and pagination state is generated.
2. New cookie is inserted into cookie registry.
3. Registry size increases monotonically with each request.
4. Remote caller controls growth rate by request volume.

## Symptoms

- monotonically increasing cookie registry size
- cookie count exceeds configured safety budget
- memory pressure grows with request volume

## Violated invariants

- INV_006 — remote request-driven state growth must remain bounded.
- INV_005 — failure mode must be machine-detectable.

## Detection

- `cookie_count > max_cookie_budget`
- monotonic `cookie_count` growth under repeated unauthenticated requests

## Recovery / prevention strategy

- enforce hard cookie-state budget (`MAX_COOKIES_TRACKED`)
- deterministic eviction policy when budget is exceeded (FIFO in this lab)

## Acceptance criteria

- `test_repro_fm002.py` demonstrates cookie growth exceeds budget without guardrail
- `test_prevent_fm002.py` proves cookie count stays within budget with guardrail

## Notes

This FM intentionally models mechanism only (state budget boundary), not
protocol implementation details.
