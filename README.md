# Software Failure Atlas

This repo is a field guide to recurring failure patterns in modern autonomous systems.

It groups concrete mechanisms under the CWE-1000 pillars so they are easier to review, compare, and extend.

<details>
<summary>What</summary>

A set of failure modes that show up in agentic runtimes, tool-using systems, and automation workflows.

The point is to make the failure easy to inspect:

- what failed
- why it failed
- what invariant was missing
- what would restore it

</details>

<details>
<summary>Why</summary>

CWE is useful, but broad. Incidents are useful, but narrow. This atlas tries to sit between the two.

The entries are meant to be reusable across systems, not tied to one stack or one postmortem.

</details>

<details>
<summary>How To Use It</summary>

Use it during:

- design review
- threat modeling
- launch readiness review
- implementation review
- postmortem cleanup

Start from the taxonomy if you already know the weakness class. Start from the symptom if you do not.

Each entry shows:

- the failure
- the mechanism
- the violated invariant
- the remediation
- the restored invariant

</details>

## Referenced Entries

- [FM-002 Extension Authority Persistence](./atlas/access_control/extension_authority_persistence.md): Ironclaw
- [FM-007 Identity Map Bijection Break](./atlas/identity_authentication/identity_map_collision.md): Near MPC
- [FM-009 Progress Stall Detection Gap](./atlas/logic_calculation/progress_stall_loop.md): LangChain

<details>
<summary>See All</summary>

- [[FM-001] Duplicate Execution After Retry Timeout](./atlas/state_integrity/duplicate_retry_timeout.md)
- [[FM-003] Read-only Enforcement Gap](./atlas/access_control/read_only_enforcement_gap.md)
- [[FM-005] Unbounded Pagination State Amplification](./atlas/resource_management/unbounded_pagination.md)
- [[FM-006] Quota Boundary Off-by-One](./atlas/input_validation/quota_off_by_one.md)
- [[FM-008] Tool Authority Escalation via Prompt Injection](./atlas/access_control/tool_authority_escalation.md)

</details>

---

<details>
<summary>How To Contribute
</summary>

Add an entry when you can name a reusable mechanism, not just an isolated incident.

Each entry should:

- classify the entry under one CWE-1000 pillar
- describe one failure pattern per file
- choose a descriptive slug that names the mechanism, not the incident
- make the broken boundary or hidden assumption explicit
- include a short pseudo-Python example
- name the invariant that was violated
- describe the remediation in terms of the invariant it restores

The template and authoring rules live here:

- [AGENTS.md](./AGENTS.md) defines the repository-wide contract, template, taxonomy, and authoring rules
- [atlas/AGENTS.md](./atlas/AGENTS.md) adds local guidance for files under `atlas/`

</details>
