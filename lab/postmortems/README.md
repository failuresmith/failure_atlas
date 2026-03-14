# Postmortems

Purpose: anchor each failure class to a concrete real-world incident (“Real failure” in the chain).

Scope and location
- Lives under `lab/postmortems/` because PMs feed the lab reproductions directly.
- Each PM links to its Failure Pattern (FP), Failure Mode (FM) lab (when available), and Guardrail (GR).

Numbering convention
- PM IDs match the corresponding FP ID when an incident clearly maps to one failure class.
- A single PM can cite multiple occurrences of the same class; we don’t duplicate PMs per sighting.
- New classes without FP/FM yet get a PM placeholder ID to record the incident, then the lab/atlas artifacts catch up.

Index (current)
- PM_001 → FP_001 Duplicate Execution After Retry Timeout
- PM_002 → FP_002 Extension Authority Persistence
- PM_003 → FP_003 Read-only Enforcement Gap
- PM_004 → (not yet defined; FP_004 currently theory-only)
- PM_005 → FP_005 Unbounded Pagination Cookie State Amplification
- PM_006 → FP_006 Quota Boundary Off-by-One Admission
- PM_007 → FP_007 Identity Map Bijection Break
- PM_008 → FP_008 Tool Authority Escalation via Prompt Injection

Why IDs can differ from creation order
- PM numbers track failure classes, not calendar order, to keep FP/PM alignment legible over time.
