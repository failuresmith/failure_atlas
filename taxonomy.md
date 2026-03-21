# Failure Taxonomy

Canonical catalog spine for Failure Patterns (`FP_XXX`) in `atlas/`. Keep just enough domain/mechanism detail to disambiguate labels; anything deeper belongs in the FP/FM/GR artifacts.

## Domains and mechanisms (single-line definitions)

- **Identity Integrity / Identity Registry Collisions** — bijective identity/key mapping breaks when inserts overwrite or collide.
- **Policy Enforcement / Extension Authority Lifecycle** — delegated capability persists beyond intended scope or ownership.
- **Policy Enforcement / Read/Write Boundary Drift** — read-only surfaces permit writes or mutable side effects.
- **Policy Enforcement / Quota Boundary Math** — inclusive/exclusive boundary errors let policy overshoot or undershoot.
- **State Consistency / Retry Idempotence Window** — retries outside the idempotence envelope replay effects.
- **Resource Exhaustion / Server-side Cursor Growth** — pagination/cursor state grows without a hard cap.
- **Model Behavior / Anthropomorphic Projection** — human intent is imputed to stochastic model output.
- **Tool / Agent Interfaces / Tool Authorization Conflation** — planner-selected tool invocations execute without runtime policy gate.

Reserved headers (define when needed): Concurrency; Recovery & Reconciliation; Distributed Coordination; Economic / Incentive Failures; Input Validation; Boundary Violations.

## Global index

| Domain                  | Mechanism                     | Failure Pattern                                                                                                              | FM     | GR     |
| ----------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------ | ------ |
| State Consistency       | Retry Idempotence Window      | [FP_001 Duplicate Execution After Retry Timeout](./atlas/FP_001_duplicate_execution_after_retry_timeout.md)                 | FM_001 | GR_001 |
| Policy Enforcement      | Extension Authority Lifecycle | [FP_002 Extension Authority Persistence](./atlas/FP_002_extension_authority_persistence.md)                                 | FM_009 | GR_002 |
| Policy Enforcement      | Read/Write Boundary Drift     | [FP_003 Read-only Enforcement Gap](./atlas/FP_003_read_only_enforcement_gap.md)                                             | FM_010 | GR_003 |
| Model Behavior          | Anthropomorphic Projection    | [FP_004 Anthropomorphic Misinterpretation](./atlas/FP_004_anthropomorphic_misinterpretation.md)                             | n/a    | GR_004 |
| Resource Exhaustion     | Server-side Cursor Growth     | [FP_005 Unbounded Pagination Cookie State Amplification](./atlas/FP_005_unbounded_pagination_cookie_state_amplification.md) | FM_002 | GR_005 |
| Policy Enforcement      | Quota Boundary Math           | [FP_006 Quota Boundary Off-by-One Admission](./atlas/FP_006_quota_boundary_off_by_one_admission.md)                         | FM_003 | GR_006 |
| Identity Integrity      | Identity Registry Collisions  | [FP_007 Identity Map Bijection Break](./atlas/FP_007_identity_map_bijection_break.md)                                       | FM_004 | GR_007 |
| Tool / Agent Interfaces | Tool Authorization Conflation | [FP_008 Tool Authority Escalation via Prompt Injection](./atlas/FP_008_tool_authority_escalation_via_prompt_injection.md)   | FM_008 | GR_008 |

Notes:

- `reproduced_in` and `mitigated_by` are list-valued in artifact metadata.
- Multiple FMs and GRs may link to one FP as the atlas grows.
- FM IDs 005–007 are intentionally unused; numbering stays aligned with FP IDs while their lab reproductions are covered by FM_002–FM_004.
