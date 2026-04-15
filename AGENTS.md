# Failure Atlas Repository Guide

This file defines the repository-wide contract for humans and agents.

`atlas/AGENTS.md` is a narrower supplement for files under `atlas/`. If the two files overlap, treat this root file as the canonical source for shared rules and treat the `atlas/` file as local clarification only.

## Repository Purpose

Failure Atlas is a field guide for reviewing modern autonomous systems before shipping. It maps broad CWE-1000 classes to concrete failure patterns seen in agentic workflows, tool-using runtimes, and automation systems.

The repository standard is mechanical legibility. Every entry should make the failure understandable across stacks, not just document an anecdote from one codebase.

## Scope

- Use this file for repository-wide expectations, taxonomy, naming, and entry structure.
- Use `atlas/AGENTS.md` only when editing files inside `atlas/`.

## Taxonomy: CWE-1000

All failure modes must be categorized under one of these 6 pillars from the CWE-1000 Research View:

1. **Resource Management** (`atlas/resource_management`, CWE-399): Exhaustion, memory safety, and leaks.
2. **Access Control & Authorization** (`atlas/access_control`, CWE-285): Privilege escalation, policy bypass, and boundary violations.
3. **State & Data Integrity** (`atlas/state_concurrency`, CWE-664): Race conditions, idempotency failures, and consistency drift.
4. **Input Validation & Representation** (`atlas/input_validation`, CWE-20): Injection, overflows, and boundary math errors.
5. **Control Flow & Logic** (`atlas/logic_calculation`, CWE-691): Algorithmic complexity, agent loop stalls, and deadlock or livelock behavior.
6. **Identification & Authentication** (`atlas/identity_authentication`, CWE-287): Identity map collisions and trust boundary failures.

## Core Standard

Each entry must be mechanically legible. A reader should be able to answer:

- What failed?
- Why did it fail?
- What invariant was missing or violated?
- What fix restores that invariant?

If an entry cannot answer those questions clearly, it is not ready.

## Canonical Entry Template

Every atlas entry should follow this structure:

```markdown
# [ID] Title
**Pattern:** <Pillar Name>

**The Failure**
[1-2 sentences on why this is tricky or dangerous. What is the operational gotcha?]

**Mechanism**
[Explain what actually fails in state, logic, authorization, identity, or resource handling.
Make the broken boundary, assumption, or trust model visible.]

**Coding Example**
[Short, credible pseudo-Python showing the failure path and the containment approach.]

**Invariant Violated**
[State the missing or broken invariant precisely.]

**Remediation**
[Specific code-level or architectural fixes.]

**Invariant Restored**
[Explain what invariant the fix restores, and why that closes this class of bug.]

**References** *(optional)*
- [Incident, PR, issue, advisory, or postmortem]
```

## Authoring Rules

- Keep entries reusable across systems. Favor mechanism over incident storytelling.
- Make the violated boundary or hidden assumption explicit.
- Make the remediation reusable. Name the invariant the fix restores, not just the patch.
- Write examples in pseudo-Python, but keep helper names and comments readable enough that a non-specialist can still follow the flow.
- Use descriptive slugs and clear headings so entries are easy to grep and browse.
- Keep the repository minimal. Markdown is the source of truth.

## Evidence Rules

- A short coding example is required for every entry.
- Pseudocode should be pseudo-Pythonic: code-shaped, but not fully real code.
- Pseudocode is enough if it clearly shows the failure path.
- Pseudocode should also make the broken boundary or hidden assumption visible.
- Pseudocode should also make the restored invariant visible in the remediation.
- A real-world reference is valid when it makes the failure class clearer than a toy implementation would.
