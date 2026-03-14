---
ID: FP_005
Title: Unbounded Pagination Cookie State Amplification
Class: Resource Exhaustion
Severity: availability
Status: validated
reproduced_in:
  - FM_002
mitigated_by:
  - GR_005
---

# Failure Pattern

Unauthenticated pagination requests create server-side cursor state without a
global bound, allowing remote peers to amplify memory usage until exhaustion.

## Context

Applies to protocols that support paginated discovery/listing and persist
pagination cookies or cursors in server memory between requests.

## Hidden Assumption

Pagination state growth is assumed to be naturally bounded by legitimate client
behavior.

## Invariant at Risk

Resource consumption for unauthenticated remote requests must remain bounded.

## Trigger Condition

A remote peer repeatedly issues protocol-compliant discovery requests that force
creation of new pagination cookies/cursors.

## Failure Mechanism

Each request allocates durable server-side pagination state in a cookie map. No
hard capacity limit, expiry budget, or eviction boundary is enforced. The state
table grows monotonically with attacker-controlled request volume.

## Observable Symptoms

- monotonic growth of cookie/cursor table size
- memory growth proportional to discover request rate
- process memory pressure / eventual OOM risk

## Detection

`cookie_state_entries` grows without bound under repeated unauthenticated
DISCOVER-style traffic.

## Relevance / Where This Class Appears

- rendezvous/discovery services
- search/index APIs with server-side cursor registries
- any stateless transport carrying stateful pagination handles

## Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update

- **Real failure:** unbounded DISCOVER cookie tracking allows remote memory amplification
- **Minimal reproduction:** deterministic FM_002 repeated discover-request harness
- **Mechanism:** unbounded server-side pagination state table
- **Guardrail:** bounded cookie registry with deterministic overflow behavior
- **Atlas update:** FP_005 linked to validated FM_002 + GR_005 artifacts

## Lab Reproduction

- `lab/failure_modes/FM_002_unbounded_pagination_state/`

## Relevant Guardrails

- `guardrails/GR_005_bounded_pagination_state.md`

## Related Patterns

- FP_006 Quota Boundary Off-by-One Admission
