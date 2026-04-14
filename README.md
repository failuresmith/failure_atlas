# Software Failure Atlas

A personal log of software security failure modes, categorized by the CWE-1000 (Research View) pillars. This atlas is designed for engineering learning and quick reference.

## 1. Resource Management (CWE-399)
*Exhaustion, memory safety, and leaks.*
- [[FM-005] Unbounded Pagination State Amplification](./atlas/resource_management/unbounded_pagination.md)

## 2. Access Control & Authorization (CWE-285)
*Privilege escalation, policy bypass, and boundary violations.*
- [[FM-002] Extension Authority Persistence](./atlas/access_control/extension_authority_persistence.md)
- [[FM-003] Read-only Enforcement Gap](./atlas/access_control/read_only_enforcement_gap.md)
- [[FM-008] Tool Authority Escalation via Prompt Injection](./atlas/access_control/tool_authority_escalation.md)

## 3. State & Data Integrity (CWE-664)
*Race conditions, idempotency, and consistency.*
- [[FM-001] Duplicate Execution After Retry Timeout](./atlas/state_concurrency/duplicate_retry_timeout.md)

## 4. Input Validation & Representation (CWE-20)
*Injection, overflows, and boundary math.*
- [[FM-006] Quota Boundary Off-by-One](./atlas/input_validation/quota_off_by_one.md)

## 5. Control Flow & Logic (CWE-691)
*Algorithmic complexity, loops, and deadlocks.*
- [[FM-004] Anthropomorphic Misinterpretation](./atlas/logic_calculation/anthropomorphic_misinterpretation.md)
- [[FM-009] Progress Stall Detection Gap](./atlas/logic_calculation/progress_stall_loop.md)

## 6. Identification & Authentication (CWE-287)
*Identity collisions and trust boundaries.*
- [[FM-007] Identity Map Bijection Break](./atlas/identity_authentication/identity_map_collision.md)

---

## Lab
Every failure mode has a minimal, standalone reproduction in the `./lab/` directory.

## Contributing
See [AGENTS.md](./AGENTS.md) for the entry template and taxonomy standards.
