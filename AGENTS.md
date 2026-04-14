# Failure Atlas Agent Instructions

This repository is a personal, searchable, and engineering-credible "Software Failure Log". It documents software security failure modes to help engineers learn from past mistakes and prevent similar failures.

## Taxonomy: CWE-1000

All failure modes must be categorized under one of the following 6 pillars from the CWE-1000 (Research View):

1. **Resource Management** (CWE-399): Exhaustion (OOM), memory safety (Buffer Overflow), and leaks.
2. **Access Control & Authorization** (CWE-285): Privilege escalation, policy bypass, and boundary violations.
3. **State & Data Integrity** (CWE-664): Race conditions, idempotency failures, and consistency drift. (Folder: `state_concurrency`)
4. **Input Validation & Representation** (CWE-20): Injection (Prompt/SQL), overflows, and boundary math errors.
5. **Control Flow & Logic** (CWE-691): Algorithmic complexity, agent loop stalls, and deadlock/livelocks. (Folder: `logic_calculation`)
6. **Identification & Authentication** (CWE-287): Identity map collisions and trust boundary failures. (Folder: `identity_authentication`)

## Entry Template (`atlas/<pillar>/<descriptive-slug>.md`)

Every entry must follow this "human-handwritten" tone—concise, technical, and non-verbose.

```markdown
# [ID] Title
**Pattern:** <Pillar Name>

**The Failure**
[1-2 sentences on why this is tricky/dangerous. What is the "gotcha"?]

**Mechanism**
[Technical deep-dive: what happens in memory/state/logic. Why does it fail?]

**Reproduction**
[Short, credible code snippet or pseudo-code showing the failure.]
Full reproduction: `lab/<pillar>/<descriptive-slug>/`

**Remediation**
[Specific code-level fixes, architectural patterns, or invariant-enforcing designs.]
```

## Lab Standards (`lab/<pillar>/<descriptive-slug>/`)

- **Standalone**: Prefer simple, standalone scripts or minimal projects over complex frameworks.
- **Reproducible**: Must include a clear way to run the reproduction and observe the failure.
- **Credible**: Use realistic environments (e.g., specific library versions or memory constraints if relevant).

## Guiding Principles

- **Searchability**: Use descriptive slugs for filenames and clear headings for easy grep/search.
- **Engineering Credibility**: Include technical details like memory layouts or race condition traces where appropriate.
- **Minimalism**: Avoid industrial documentation bloat. No auto-generated sites or complex registries. Pure Markdown is the source of truth.
