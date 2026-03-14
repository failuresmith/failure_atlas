---
ID: FP_002
Title: Extension Authority Persistence
Class: Policy Enforcement
Severity: integrity
Status: draft
reproduced_in:
  - FM_001
mitigated_by:
  - GR_002
---

# Failure Pattern

Authority granted to an extension persists beyond the extension lifecycle,
creating stale privilege scope.

## Hidden Assumption

Revoking/deactivating a component is assumed to revoke all delegated authority
derived from it.

## Trigger Condition

Extension/plugin uninstall or deactivation occurs while delegated credential/tool
bindings remain registered.

## Failure Mechanism

Lifecycle management and authority registry evolve independently.
Revocation path is missing or asynchronous enough to leave active stale grants.

## Observable Symptoms

- registry contains bindings for inactive extension IDs
- operations still pass authority checks after uninstall
- policy intent differs from runtime capability surface

## Detection

`registry.contains(extension_id) AND NOT extension_active(extension_id)`

## Lab Reproduction

- `lab/failure_modes/FM_001_duplicate_retry/`

## Relevant Guardrails

- `guardrails/GR_002_lifecycle_bound_authority.md`

## Postmortem

- `lab/postmortems/PM_002_extension_authority_persistence.md`

## Related Patterns

- FP_001 Duplicate Execution After Retry Timeout
- FP_003 Read-only Enforcement Gap
