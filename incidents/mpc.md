### Background

If two participants share the same TLS key (e.g., operator/config drift during rotation or scaling), one silently overwrites the other in the peer identity mapping.

**If ignored**:  authenticated traffic may be attributed to the wrong participant (or connections may fail inconsistently), weakening protocol identity guarantees and complicating incident analysis.

**Fix**:  fail startup when participant identity mapping is not strictly 1:1 (`participant_id` ↔ `tls_key`) before opening listeners.

### User Story

As an MPC operator or maintainer, I need participant identity mappings to be strictly validated at startup so that configuration drift (e.g., duplicate TLS keys during rotation or scaling) cannot silently weaken protocol identity guarantees.

The system should fail fast if identity mapping is ambiguous, preventing runtime misattribution and simplifying incident analysis.

### Acceptance Criteria

- Startup fails if duplicate `participant_id` values are detected.
- Startup fails if duplicate TLS/P2P public keys are detected.
- `participant_id` ↔ `tls_key` mapping must be strictly bijective.
- Error message clearly identifies conflicting participant IDs and key.
- No network listeners or tasks start if validation fails.
- Deterministic tests verify duplicate-ID and duplicate-key configs are rejected.

### Resources & Additional Notes

<details>
<summary>Technical details</summary>

In `new_tls_mesh_network`, `ParticipantIdentities.key_to_participant_id` is built via `HashMap::insert`.
A duplicate key overwrites prior mapping.

`verify_peer_identity` then resolves that key to only one participant ID.

This violates the required invariant: `participant_id ↔ tls_key` must be bijective.

For __outgoing__ connections, the `peer_id == target_participant_id` check causes some aliasing cases to fail closed (connection rejected).
For __incoming__ handling, attribution relies on `verify_peer_identity` lookup, so misattribution remains possible.


The specific data structure used is less important than ensuring:
- the bijection invariant is enforced before runtime
- configuration errors fail fast
- operator-facing diagnostics are clear and actionable

</details>

--- 

> If this direction aligns with your expectations, I’m happy to implement the startup invariant enforcement and tests in a follow-up PR.


Reference: https://github.com/near/mpc/issues/2250

status: pending review