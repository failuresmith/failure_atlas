# Failure Taxonomy

This taxonomy is the catalog spine for Failure Patterns (`FP_XXX`) in `atlas/`.

## Classes

- Identity & Authority
- Policy Enforcement
- State Consistency
- Concurrency
- Recovery & Reconciliation
- Resource Exhaustion
- Distributed Coordination
- Economic / Incentive Failures
- Input Validation
- Boundary Violations
- Model Behavior
- Tool / Agent Interfaces

## Global Index

| Class | Failure Pattern | FM | GR |
| --- | --- | --- | --- |
| State Consistency | FP_001 Duplicate Execution After Retry Timeout | FM_001 | GR_001 |
| Policy Enforcement | FP_002 Extension Authority Persistence | FM_001 | GR_002 |
| Policy Enforcement | FP_003 Read-only Enforcement Gap | FM_001 | GR_003 |
| Model Behavior | FP_004 Anthropomorphic Misinterpretation | n/a | GR_004 |
| Resource Exhaustion | FP_005 Unbounded Pagination Cookie State Amplification | FM_002 | GR_005 |
| Policy Enforcement | FP_006 Quota Boundary Off-by-One Admission | pending (external report) | pending |

> Notes:
> - `reproduced_in` and `mitigated_by` are list-valued in artifact metadata.
> - Multiple FMs and GRs may link to one FP as the atlas grows.
