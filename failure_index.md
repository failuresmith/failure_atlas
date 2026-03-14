# Failure Index

Catalog of Failure Patterns in the FM → FP → GR pipeline.

| ID | Failure Pattern | Class | Reproduced In | Mitigated By |
| --- | --- | --- | --- | --- |
| FP_001 | [Duplicate Execution After Retry Timeout](./atlas/FP_001_duplicate_execution_after_retry_timeout.md) | State Consistency | FM_001 | GR_001 |
| FP_002 | [Extension Authority Persistence](./atlas/FP_002_extension_authority_persistence.md) | Policy Enforcement | FM_001 | GR_002 |
| FP_003 | [Read-only Enforcement Gap](./atlas/FP_003_read_only_enforcement_gap.md) | Policy Enforcement | FM_001 | GR_003 |
| FP_004 | [Anthropomorphic Misinterpretation](./atlas/FP_004_anthropomorphic_misinterpretation.md) | Model Behavior | n/a | GR_004 |
| FP_005 | [Unbounded Pagination Cookie State Amplification](./atlas/FP_005_unbounded_pagination_cookie_state_amplification.md) | Resource Exhaustion | FM_002 | GR_005 |
| FP_006 | [Quota Boundary Off-by-One Admission](./atlas/FP_006_quota_boundary_off_by_one_admission.md) | Policy Enforcement | FM_003 | GR_006 |

Canonical taxonomy lives in [`docs/taxonomy.md`](./docs/taxonomy.md).
