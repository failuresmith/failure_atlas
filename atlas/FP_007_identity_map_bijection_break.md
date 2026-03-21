---
ID: FP_007
Title: Identity Map Bijection Break
Domain: Identity Integrity
Mechanism: Identity Registry Collisions
Severity: integrity
Status: draft
reproduced_in:
  - FM_007
mitigated_by:
  - GR_007
---

# Failure Pattern

Participant identity registry allows duplicate credentials or IDs to overwrite existing entries, breaking the required bijection between participant IDs and TLS keys.

## Hidden Assumption

Startup configuration is assumed to contain unique participant IDs and credentials; overwriting in a map is assumed safe.

## Trigger Condition

- Duplicate TLS keys or participant IDs present during startup.
- Registry is built with insert/overwrite semantics and no validation.

## Failure Mechanism

Registry keyed by credential replaces earlier mapping when a duplicate key is inserted. Authenticated traffic for the shared key is attributed to whichever participant was inserted last.

## Observable Symptoms

- Authenticated traffic attributed to the wrong participant.
- Conflicting participants appear to share identity in diagnostics.
- No startup error despite non-bijective mapping.

## Detection

- `len(unique_tls_keys) != len(participant_ids)`
- `len(set(participant_ids)) != len(participant_ids)`

## Lab Reproduction

- `lab/failure_modes/FM_007_identity_map_bijection/`

## Relevant Guardrails

- `guardrails/GR_007_identity_bijection_startup_validation.md`

## Postmortem

- `lab/postmortems/PM_007_identity_map_bijection_break.md`

## Related Patterns

- FP_001 Duplicate Execution After Retry Timeout (shared recovery themes around idempotent boundaries)
