<!-- Generated from registry/registry.yml. Do not edit by hand. -->

# Failure Taxonomy

Canonical catalog spine for Failure Patterns (`FP_XXX`) in `atlas/`. Keep just enough domain/mechanism detail to disambiguate labels; anything deeper belongs in the FP/FM/GR artifacts.

## Domains and mechanisms (single-line definitions)

- **Agent Runtime / Progress Ledger Omission** — agent loop counts steps but lacks state-change detection, so it spins on identical failures.

Reserved headers (define when needed): Concurrency; Recovery & Reconciliation; Distributed Coordination; Economic / Incentive Failures; Input Validation; Boundary Violations.

## Global index

| Domain                  | Mechanism                     | Failure Pattern                                                                                                              | FM     | GR     |
| ----------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------ | ------ |
| State Consistency | Retry Idempotence Window | [ Duplicate Execution After Retry Timeout ](./atlas/FP_001_duplicate_execution_after_retry_timeout.md) | FM_001 | GR_001 |
| Policy Enforcement | Extension Authority Lifecycle | [ Extension Authority Persistence ](./atlas/FP_002_extension_authority_persistence.md) | FM_002 | GR_002 |
| Policy Enforcement | Read/Write Boundary Drift | [ Read-only Enforcement Gap ](./atlas/FP_003_read_only_enforcement_gap.md) | FM_003 | GR_003 |
| Model Behavior | Anthropomorphic Projection | [ Anthropomorphic Misinterpretation ](./atlas/FP_004_anthropomorphic_misinterpretation.md) | n/a | GR_004 |
| Resource Exhaustion | Server-side Cursor Growth | [ Unbounded Pagination Cookie State Amplification ](./atlas/FP_005_unbounded_pagination_cookie_state_amplification.md) | FM_005 | GR_005 |
| Policy Enforcement | Quota Boundary Math | [ Quota Boundary Off-by-One Admission ](./atlas/FP_006_quota_boundary_off_by_one_admission.md) | FM_006 | GR_006 |
| Identity Integrity | Identity Registry Collisions | [ Identity Map Bijection Break ](./atlas/FP_007_identity_map_bijection_break.md) | FM_007 | GR_007 |
| Tool / Agent Interfaces | Tool Authorization Conflation | [ Tool Authority Escalation via Prompt Injection ](./atlas/FP_008_tool_authority_escalation_via_prompt_injection.md) | FM_008 | GR_008 |
| Agent Runtime | Progress Ledger Omission | [ Progress Stall Detection Gap ](./atlas/FP_009_progress_stall_detection_gap.md) | FM_009 | GR_009 |

Notes:

- `reproduced_in` and `mitigated_by` are list-valued in artifact metadata.
- Multiple FMs and GRs may link to one FP as the atlas grows.
- FM IDs align 1:1 with FP/GR numbering; FP_004 currently has no FM.

