# Failure Index

Catalog of Failure Patterns in the FM → FP → GR pipeline (PM numbers align to FP IDs).

| ID | PM | Failure Pattern | Domain | Mechanism | Reproduced In | Mitigated By |
| --- | --- | --- | --- | --- | --- | --- |
| FP_001 | [PM_001](./postmortems/PM_001_duplicate_execution.md) | [Duplicate Execution After Retry Timeout](./atlas/FP_001_duplicate_execution_after_retry_timeout.md) | State Consistency | Retry Idempotence Window | FM_001 | GR_001 |
| FP_002 | [PM_002](./postmortems/PM_002_extension_authority_persistence.md) | [Extension Authority Persistence](./atlas/FP_002_extension_authority_persistence.md) | Policy Enforcement | Extension Authority Lifecycle | FM_001 | GR_002 |
| FP_003 | [PM_003](./postmortems/PM_003_read_only_enforcement_gap.md) | [Read-only Enforcement Gap](./atlas/FP_003_read_only_enforcement_gap.md) | Policy Enforcement | Read/Write Boundary Drift | FM_001 | GR_003 |
| FP_004 | — (no PM yet) | [Anthropomorphic Misinterpretation](./atlas/FP_004_anthropomorphic_misinterpretation.md) | Model Behavior | Anthropomorphic Projection | n/a | GR_004 |
| FP_005 | [PM_005](./postmortems/PM_005_unbounded_pagination_state.md) | [Unbounded Pagination Cookie State Amplification](./atlas/FP_005_unbounded_pagination_cookie_state_amplification.md) | Resource Exhaustion | Server-side Cursor Growth | FM_002 | GR_005 |
| FP_006 | [PM_006](./postmortems/PM_006_quota_boundary_off_by_one.md) | [Quota Boundary Off-by-One Admission](./atlas/FP_006_quota_boundary_off_by_one_admission.md) | Policy Enforcement | Quota Boundary Math | FM_003 | GR_006 |
| FP_007 | [PM_007](./postmortems/PM_007_identity_map_bijection_break.md) | [Identity Map Bijection Break](./atlas/FP_007_identity_map_bijection_break.md) | Identity Integrity | Identity Registry Collisions | FM_004 | GR_007 |
| FP_008 | [PM_008](./postmortems/PM_008_tool_authority_escalation.md) | [Tool Authority Escalation via Prompt Injection](./atlas/FP_008_tool_authority_escalation_via_prompt_injection.md) | Tool / Agent Interfaces | Tool Authorization Conflation | FM_008 | GR_008 |

Canonical taxonomy lives in [`taxonomy.md`](./taxonomy.md).
