# REFACTOR PLAN — Failure Atlas

Goal: transform this repository into a **Failure Atlas manufacturing pipeline**.

The repository must produce **engineering knowledge about Failure Patternes**, not software frameworks.

Target workflow:

```

Real failure
↓
FM — minimal reproduction (lab)
↓
FP — generalized failure pattern
↓
GR — guardrail pattern

```

The lab proves failures.
The atlas explains recurring failure patterns.
Guardrails prescribe reusable mitigations.

---

# Decision Log (Canonical Clarifications)

## D1. Canonical workflow order

The canonical manufacturing workflow is:

```
Real failure
↓
FM — minimal reproduction
↓
FP — generalized failure pattern
↓
GR — guardrail pattern
```

Meaning:

- FM proves
- FP explains
- GR mitigates

So the atlas is not “last update”; it is the pattern layer between experiment and mitigation.

## D2. Canonical path map

Legacy paths migrate as follows:

```
lab/docs/01_invariants.md   → docs/invariants.md
lab/runtime/*               → lab/core/*
lab/faults/*                → lab/core/faults.py or lab/core/*
lab/policies/*              → keep temporarily; migrate reused logic only
lab/docs/*                  → docs/*
atlas/class-subfolders/*    → atlas/FP_XXX_name.md
```

## D3. YAML frontmatter coverage

YAML frontmatter is required for:

- FM specs
- FP entries
- GR entries

It is not required for:

- `README.md` files
- taxonomy or index files
- invariant docs
- migration plans
- templates unless useful

## D4. Atlas layout

The atlas is flat and ID-driven:

`atlas/FP_XXX_name.md`

Taxonomy is expressed in metadata and indexed in `docs/taxonomy.md`, not by directory nesting.

## D5. FM test contract

Every FM must include:

- `test_fmxxx_happy_path.py`
- `test_repro_fmxxx.py`
- `test_prevent_fmxxx.py`

`test_recover_fmxxx.py` is optional.

Exception:

- FM_001 must include recovery because it is the reference migration case.

## D6. Guardrail promotion rule

Use this rule:

A mitigation is promoted to `GR` only when it is reusable, generalizable, or expresses a stable invariant-preserving design pattern.

Case-specific fixes remain in FM documentation until generalized.

## D7. Link cardinality

`reproduced_in` and `mitigated_by` are lists, not single values.

Example:

```yaml
reproduced_in:
  - FM_001
mitigated_by:
  - GR_001
  - GR_004
```

This keeps the system extensible.

## D8. Migration sequencing

Before structural refactor:

- restore baseline test hygiene
- fix duplicate module/test naming issues
- ensure lab tests collect and run
- then begin path and architecture migration

---

# Core Principles

1. **Failure-first**
   - Everything must relate to a **failure mode**.
   - The repository studies how **systems break**.

2. **Minimal experiments**
   - The lab is **not a system simulator**.
   - It demonstrates mechanisms with the **smallest possible system**.

3. **Determinism**
   - Experiments must be reproducible.
   - Forbidden:
     - wall clock timing
     - randomness
     - nondeterministic concurrency
   - Allowed:
     - deterministic clock
     - explicit fault injection

4. **Invariants first**
   - Every failure mode violates an explicit invariant.
     - `docs/invariants.md`
   - Invariants anchor the entire pipeline:
     - FM → FP → GR

5. **Single responsibility**
   - Each directory has one exactly one role.

lab/ → experiments
atlas/ → failure knowledge
guardrails/ → mitigation patterns

---

# Operating Vocabulary

Strict terminology must be used.

### FM — Failure Mode

Minimal reproducible experiment in the lab.

Location:

`lab/failure_modes/FM_XXX_name/`

Purpose:

`prove the failure mechanism exists.`

### FP — Failure Pattern

Generalized **failure class** extracted from experiments or real systems.

Location:

`atlas/FP_XXX_name.md`

Purpose:

`explain the mechanism behind recurring failures.`

### GR — Guardrail Pattern

Reusable **engineering mitigation pattern**.

Location:

`guardrails/GR_XXX_name.md`

Purpose:

`prevent, contain, or recover from a failure pattern`

### INV — Invariant

Explicit correctness property.

Location:

`docs/invariants.md`

Purpose:

`define the property that must never be violated`

# Knowledge Pipeline

Artifacts must follow this pipeline:

`FM → FP → GR`

Meaning:

```
experiment
↓
generalized failure pattern
↓
guardrail design
```

Experiments produce evidence.
Patterns produce understanding.
Guardrails produce engineering guidance.

# Boundary Rules

```
lab/        → proves failure
atlas/      → explains failure
guardrails/ → prescribes mitigation

```

Rules:

- `atlas/` must **not contain guardrail implementation details**
- `guardrails/` must **not repeat failure explanations**
- `lab/` must **not simulate real systems**
- `lab/` must **only demonstrate mechanisms**

---

# Evidence Rules

A failure pattern may be added to the atlas only if backed by:

1. a validated lab reproduction (FM)

or

2. a real-world investigated failure with explicit invariant and mechanism analysis.

Speculative patterns are not allowed.

# Guardrail Reuse Rule

A new guardrail should only be created if the mitigation is reusable.

If the mitigation is specific to a single experiment, it belongs inside the FM documentation until generalized.

Guardrails should represent **design patterns**, not patches.

# Artifact Schema (Mandatory)

All FM, FP, and GR artifacts must begin with YAML frontmatter metadata.

Frontmatter is required only for:
- FM specs
- FP entries
- GR entries

Frontmatter is not required for:
- README files
- taxonomy or index files
- invariant docs
- migration plans
- templates unless useful

This enables automatic indexing and taxonomy generation without forcing metadata onto non-catalog documents.

Ensure the atlas behaves like a **catalog of failure knowledge**, not free-form notes.

---

## Failure Mode Schema (FM)

Location:

`lab/failure_modes/FM_XXX_name/`

spec.md must begin with:

```yaml
ID: FM_XXX
Title: short failure description
Hypothesis: mechanism being tested
Invariant: INV_XXX
Status: draft | reproduced | validated
related_pattern:
  - FP_XXX
```

Required files:

```
spec.md
scenario.py
tests/
```

Tests required:

```
test_fmxxx_happy_path.py
test_repro_fmxxx.py
test_prevent_fmxxx.py
```

Optional:
`test_recover_fmxxx.py`

Test meanings:

| Test    | Purpose                                |
| ------- | -------------------------------------- |
| happy   | system works normally                  |
| repro   | failure occurs                         |
| prevent | invariant prevents failure             |
| recover | system restores correctness (optional) |

Experiments should remain <200 lines if possible.

Purpose:

FM documents a **minimal reproducible experiment** proving a failure mechanism.

---

## Failure Pattern Schema (FP)

Location:

`atlas/FP_XXX_name.md`

Frontmatter:

```yaml
ID: FP_XXX
Title: failure pattern name
Class: taxonomy category
Severity: reliability | integrity | safety
Status: draft | validated
reproduced_in:
  - FM_XXX
mitigated_by:
  - GR_XXX
```

Required sections:

```

Failure Pattern
Hidden Assumption
Trigger Condition
Failure Mechanism
Observable Symptoms
Detection
Lab Reproduction
Relevant Guardrails
Related Patterns

```

Atlas entries must **not contain implementation detail**.

Purpose:

FP documents the **generalized Failure Pattern** extracted from experiments or real systems.

---

## Guardrail Pattern Schema (GR)

Location:

`guardrails/GR_XXX_name.md`

Frontmatter:

```yaml
ID: GR_XXX
Title: guardrail design
mitigates:
  - FP_XXX
enforces:
  - INV_XXX
Type: prevention | containment | recovery
Status: proposed | validated
```

Required sections:

```

Failure Pattern Mitigated
Invariant Enforced
Guardrail Design
Implementation Sketch
Tradeoffs
Related Failure Patterns

```

Guardrails may mitigate **multiple failure patterns**.

Purpose:

GR documents the **engineering mechanism preventing or containing a Failure Pattern**.

# Failure Taxonomy

The atlas organizes failure patterns into a stable taxonomy.

Location:  
`docs/taxonomy.md`

Initial taxonomy:

```

Identity & Authority
Policy Enforcement
State Consistency
Concurrency
Recovery & Reconciliation
Resource Exhaustion
Distributed Coordination
Economic / Incentive Failures
Input Validation
Boundary Violations
Model Behavior
Tool / Agent Interfaces

```

The taxonomy index maintains a global table:

| Class                | Failure Pattern                        | FM     | GR     |
| -------------------- | -------------------------------------- | ------ | ------ |
| Policy Enforcement   | FP_004 Capability-Authority Conflation | FM_004 | GR_002 |
| Identity & Authority | FP_001 Implicit Identity Binding       | FM_001 | GR_001 |

This table becomes the global index of the Failure Atlas.

# Target Repository Structure

```

failure-atlas/

atlas/
FP_XXX_name.md

lab/
core/
failure_modes/
FM_XXX_name/
spec.md
scenario.py
tests/

guardrails/
GR_XXX_name.md

docs/
invariants.md
taxonomy.md

```

---

# Lab Architecture

The lab must be a **tiny experimental kernel**.

Allowed abstractions in `lab/core/`:

```

state.py
transitions.py
faults.py
invariants.py
recovery.py

```

Rules:

- New core abstractions require **≥2 failure modes**
- The lab demonstrates **conceptual failures**, not infrastructure.

---

# FM_001 Migration Target

Current FM_001:

duplicate execution after retry.

Target experiment:

```
job processing
↓
retry after timeout
↓
duplicate execution
```

Tests must prove:

```
happy path → correct execution
repro → duplicate effect occurs
prevent → idempotency boundary prevents duplication
recover → reconciliation restores correctness

```

Remove infrastructure complexity not required to demonstrate the mechanism.

Each failure mode must contain:

`lab/failure_modes/FM_XXX_name/`

Required files:

### spec.md

Must contain:

- Context
- Hidden assumption
- Violated invariant (INV_XXX)
- Trigger
- Failure mechanism
- Expected impact

---

### scenario.py

Minimal reproduction of the failure.

No infrastructure simulation.

Only the smallest system required.

---

# Atlas Entry Structure (FP)

Atlas entries document **Failure Patternes**, not incidents.

```

atlas/FP_XXX_name.md

```

Required sections:

- Failure Pattern
- Hidden assumption
- Trigger condition
- Failure mechanism
- Observable symptoms
- Detection
- Lab Reproductions (`FM_XXX`)
- Relevant Guardrails (`GR_XXX`)
- Related patterns

Atlas entries **must not contain implementation details**.

---

# Guardrail Entry Structure (GR)

Guardrails describe **engineering containment patterns**.

```

guardrails/GR_XXX_name.md

```

Required sections:

- Failure Pattern mitigated
- Invariant enforced
- Guardrail design
- Implementation sketch
- Tradeoffs
- Related failure patterns

Guardrails may reference multiple failure patterns.

---

# Migration Steps

1. Restore baseline test hygiene
   - Fix duplicate module/test naming issues
   - Ensure `lab` tests collect and run
2. Stabilize terminology (FM, FP, GR, INV)
3. Introduce YAML metadata schema
4. Refactor lab to minimal kernel
5. Simplify FM_001 experiment
6. Introduce FP template
7. Introduce GR template
8. Remove unnecessary infrastructure
9. Ensure deterministic tests
10. Generate taxonomy index

---

# Success Criteria

Artifacts follow the knowledge pipeline:

`FM → FP → GR`

Every failure pattern links:

```
experiment
↓
pattern
↓
guardrail
```

The repository evolves into a **taxonomy of system failures**.

---

# Non-Goals

This repository is **not**:

- a reliability framework
- a distributed systems simulator
- a production library

It is a **research artifact** documenting how systems fail.

---

# Long-Term Vision

The Failure Atlas becomes **a field guide to system failures**.

Comparable to:

- vulnerability taxonomies in security
- fault models in distributed systems
- safety case libraries in engineering

Primary output:

`Engineering knowledge about failure patterns.`
