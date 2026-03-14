---
ID: FP_003
Title: Read-only Enforcement Gap
Class: Policy Enforcement
Severity: integrity
Status: draft
reproduced_in:
  - FM_001
mitigated_by:
  - GR_003
---

# Failure Pattern

Declared read-only policy is not enforced at capability exposure boundaries.

## Hidden Assumption

Advisory metadata/hints are assumed to provide hard runtime enforcement.

## Trigger Condition

System is launched in "read-only" intent while write-capable operations remain
registered and invocable.

## Failure Mechanism

Policy is represented only in metadata and never projected into executable tool
registration/dispatch constraints.

## Observable Symptoms

- write tools appear in read-only mode tool registry
- write operations succeed when policy says they should be impossible
- policy compliance depends on caller behavior

## Detection

`read_only == true AND write_tools ∈ exposed_toolset`

## Lab Reproduction

- `lab/failure_modes/FM_001_duplicate_retry/`

## Relevant Guardrails

- `guardrails/GR_003_capability_surface_reduction.md`

## Postmortem

- `lab/postmortems/PM_003_read_only_enforcement_gap.md`

## Related Patterns

- FP_001 Duplicate Execution After Retry Timeout
- FP_002 Extension Authority Persistence
