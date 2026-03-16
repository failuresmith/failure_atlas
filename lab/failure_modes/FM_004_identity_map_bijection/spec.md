---
ID: FM_004
Title: Participant identity map bijection not enforced
Hypothesis: Duplicate participant IDs or TLS keys can silently overwrite prior mappings at startup, breaking identity attribution.
Invariant: INV_008
Status: draft
related_pattern:
  - FP_007
---

# FM_004 — Participant identity map bijection not enforced

## Description

Startup builds a `tls_key → participant_id` registry using overwrite semantics. If two participants share the same TLS key (or duplicate IDs), the later insert replaces the earlier mapping. Runtime attribution becomes ambiguous.

## Trigger
1. Configuration contains duplicate participant IDs or duplicate TLS keys.
2. Registry construction uses insert/overwrite without validation.
3. Startup completes without error.

## Preconditions
- Participant identities and TLS keys are provided via configuration.
- Registry is constructed in-memory without uniqueness checks.

## Failure mechanism (step-by-step)
1. Load participant configs.
2. Insert each into the registry keyed by TLS key.
3. Later duplicate overwrites earlier mapping.
4. Authenticated traffic for the shared key resolves to the last-written participant.

## Symptoms
- Authenticated traffic attributed to the wrong participant ID.
- Conflicting participants cannot be distinguished at runtime.
- Operator diagnostics show mismatched IDs vs credentials.

## Violated invariants
- INV_008 — participant identity mapping must be bijective.
- INV_005 — failure should be detectable but goes unnoticed at startup.

## Detection
- `len(unique_tls_keys) != len(participants)`
- `len(set(participant_ids)) != len(participants)`

## Recovery / prevention strategy
- Fail fast during startup if bijection is not satisfied.
- Emit clear diagnostics listing conflicting IDs/keys.

## Acceptance criteria
- `test_repro_fm004.py` demonstrates overwrite when duplicates exist.
- `test_prevent_fm004.py` proves startup validation rejects duplicates and preserves bijection.
