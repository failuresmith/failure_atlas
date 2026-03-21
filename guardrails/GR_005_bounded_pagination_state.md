---
ID: GR_005
Title: Bounded Pagination State Registry
mitigates:
  - FP_005
enforces:
  - INV_006
Type: prevention
Status: validated
---

# Failure Pattern Mitigated

- FP_005 Unbounded Pagination Cookie State Amplification

## Invariant Enforced

- INV_006 — remote request-driven state growth must remain bounded.

## Guardrail Design

Project pagination into a deterministic bounded state budget. Every new cookie
allocation must pass through capacity enforcement with explicit overflow
behavior (evict/reject/expire).

## Implementation Sketch

- maintain a cookie registry with explicit `MAX_COOKIES_TRACKED`
- on cookie insert:
  - if under cap: insert
- if at cap: evict oldest entry first (FIFO in FM_005) and then insert
- expose `evicted_count` and `cookie_count` as detection signals

## Tradeoffs / Limits

- attacker can churn cookies and evict legitimate pagination state
- bounded memory is preserved, but pagination continuity may degrade under abuse
- FIFO is simple but not always optimal; TTL/LRU or stateless authenticated
  cookies may better fit production constraints

## Explicit Links

- atlas: `atlas/FP_005_unbounded_pagination_cookie_state_amplification.md`
- lab proof: `lab/failure_modes/FM_005_unbounded_pagination_state/`
