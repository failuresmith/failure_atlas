<!-- Generated from registry/registry.yml. Do not edit by hand. -->

# Failure Mode Index (Generated)

Source of truth: `registry/registry.yml`. Detailed FM specs/tests live in `lab/failure_modes/FM_XXX_*`.

| Failure Mode | Failure Pattern | Guardrail(s) | Postmortem | Status |
| --- | --- | --- | --- | --- |
| FM_001 | [FP_001 Duplicate Execution After Retry Timeout](../../atlas/FP_001_duplicate_execution_after_retry_timeout.md) | GR_001 | PM_001 | Validated |
| FM_002 | [FP_002 Extension Authority Persistence](../../atlas/FP_002_extension_authority_persistence.md) | GR_002 | PM_002 | Validated |
| FM_003 | [FP_003 Read-only Enforcement Gap](../../atlas/FP_003_read_only_enforcement_gap.md) | GR_003 | PM_003 | Validated |
| n/a | [FP_004 Anthropomorphic Misinterpretation](../../atlas/FP_004_anthropomorphic_misinterpretation.md) | GR_004 | — | Theoretical |
| FM_005 | [FP_005 Unbounded Pagination Cookie State Amplification](../../atlas/FP_005_unbounded_pagination_cookie_state_amplification.md) | GR_005 | PM_005 | Validated |
| FM_006 | [FP_006 Quota Boundary Off-by-One Admission](../../atlas/FP_006_quota_boundary_off_by_one_admission.md) | GR_006 | PM_006 | Validated |
| FM_007 | [FP_007 Identity Map Bijection Break](../../atlas/FP_007_identity_map_bijection_break.md) | GR_007 | PM_007 | Validated |
| FM_008 | [FP_008 Tool Authority Escalation via Prompt Injection](../../atlas/FP_008_tool_authority_escalation_via_prompt_injection.md) | GR_008 | PM_008 | Draft |
| FM_009 | [FP_009 Progress Stall Detection Gap](../../atlas/FP_009_progress_stall_detection_gap.md) | GR_009 | — | Draft |
FM_004 currently unassigned (no lab repro for FP_004).
