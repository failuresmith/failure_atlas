# Failure Atlas — Agent Operating Rules

This repository is a **failure-knowledge manufacturing pipeline**.

## Core workflow (non-negotiable)

Every contribution must follow this chain:

1. Identify a failure hypothesis (hidden assumption + invariant risk)
2. Build a **minimal deterministic lab reproduction**
3. Isolate the failure mechanism (structural cause)
4. Document a guardrail / containment pattern
5. Update atlas knowledge entry with links to lab + guardrail

Use this exact framing:

**Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update**

## Artifact model (keep these distinct)

- `PM` = the real-world occurrence record. A postmortem captures one incident or a tightly related set of validated occurrences.
- `FM` = one concrete deterministic manifestation in the lab. It is a single activation path of a broader failure class.
- `FP` = the abstract recurring failure pattern. It captures the higher-level hidden assumption, invariant risk, and structural mechanism shared across multiple manifestations.
- `GR` = the detailed prevention/containment design. It explains exactly how the guardrail enforces the invariant, where it acts, what it observes, and how it fails safely.

`FM` and `FP` must be complementary, not duplicates.

- If an `FP` can be replaced by a step-by-step lab script, it is too concrete.
- If an `FM` only restates the abstract mechanism in prose without a deterministic scenario, it is too abstract.

---

## Repository boundaries

- `postmortems/` = real incidents / validated occurrences (`PM`)
- `atlas/` = abstract failure-pattern knowledge (`FP`)
- `lab/` = reproducible concrete failure modes (`FM`)
- `guardrails/` = detailed containment/prevention designs (`GR`)

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

1. Postmortem / incident anchor when a real occurrence exists
2. Atlas failure-pattern entry
3. Lab failure-mode bundle (repro + prevention test proof)
4. Guardrail entry with mechanism details

All artifacts must cross-link explicitly.

---

## Success criterion

This repository should become a map of **domains of failure** and reusable containment designs,
not a catalog of isolated bugs.
