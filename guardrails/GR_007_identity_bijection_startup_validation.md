---
ID: GR_007
Title: Identity Bijection Startup Validation
mitigates:
  - FP_007
enforces:
  - INV_008
Type: prevention
Status: draft
---

# Failure Pattern Mitigated

- FP_007 Identity Map Bijection Break

## Invariant Enforced

- INV_008 — participant identity mapping must be bijective.

## Guardrail Design

Validate participant configuration at startup before any listeners are opened:
- compute uniqueness of participant IDs and credentials (TLS keys)
- if counts differ, fail fast with diagnostics listing conflicts
- prohibit silent overwrite; registry build must be rejection-based

## Implementation Sketch

1. Build `id_seen` and `key_seen` sets.
2. On duplicate detection, abort startup and emit: `duplicate participant_id` or `duplicate tls_key` with the conflicting IDs.
3. Construct registry only after validation passes.

## Tradeoffs / Limits

- Failing fast impacts availability during misconfiguration, but preserves identity correctness.
- Requires operators to fix config before restart; no automatic reconciliation.

## Explicit Links

- atlas: `atlas/FP_007_identity_map_bijection_break.md`
- lab proof: `lab/failure_modes/FM_007_identity_map_bijection/`
- postmortem: `lab/postmortems/PM_007_identity_map_bijection_break.md`
