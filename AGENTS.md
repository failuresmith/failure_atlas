# Failure Atlas — Agent Operating Rules

This repository is a **failure-pattern manufacturing pipeline**.

## Core workflow (non-negotiable)

Every contribution must follow this chain:

1. Identify a failure hypothesis (hidden assumption + invariant risk)
2. Build a **minimal deterministic lab reproduction**
3. Isolate the failure mechanism (structural cause)
4. Document a guardrail / containment pattern
5. Update atlas knowledge entry with links to lab + guardrail

Use this exact framing:

**Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update**

---

## Repository boundaries

- `atlas/` = failure knowledge (what fails and why)
- `lab/` = reproducible mechanism proofs (how it fails under controlled conditions)
- `guardrails/` = containment/prevention knowledge (how to make it fail safely)

Never merge these responsibilities.

---

## Design principles

1. **Minimal abstractions first**
   - Keep the smallest model that exposes the failure domain.

2. **No product simulation**
   - The lab is not a production-like clone.
   - Avoid domain details unless required to expose the mechanism.

3. **Determinism required**
   - Reproductions and tests must be stable and repeatable.

4. **No abstraction without reuse proof**
   - Add shared abstraction only when justified by at least 2 failure modes.

5. **One failure mode per change set**
   - Avoid mixed-scope changes.

6. **Agent loops require explicit progress detection**
   - When modeling agents, include a deterministically checkable progress/stuck signal (e.g., sliding window of step signatures) instead of relying on iteration caps.

7. **Centralize ID renames**
   - When changing FP/FM/GR/PM numbers, edit `scripts/id_map.yml` once and run `make relink` to propagate references. Do not hand-edit scattered links.

---

## Standard deliverables for each new failure domain

1. Atlas entry (failure knowledge)
2. Lab failure mode bundle (repro + prevention test proof)
3. Guardrail entry (containment pattern)

All three must cross-link explicitly.

---

## Success criterion

This repository should become a map of **domains of failure** and reusable containment designs,
not a catalog of isolated bugs.
