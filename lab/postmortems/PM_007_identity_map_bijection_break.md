# PM_007 — Participant identity ↔ TLS key bijection not enforced

## Summary
During TLS key rotation/scale-out, two participants shared the same TLS key. The identity map used `HashMap::insert`, so the later insert overwrote the earlier one. Runtime attribution could map authenticated traffic to the wrong participant, weakening protocol identity guarantees. This incident is pending FM/FP/GR codification.

## Impact
- Violated identity bijection invariant (`participant_id ↔ tls_key` must be 1:1).
- Risk of misattributed authenticated traffic and confusing incident traces.
- Potential connection failures or ambiguous operator diagnostics.

## Timeline (deterministic reproduction)
1. Configure participants with duplicate TLS keys (e.g., rotation drift).
2. Startup builds `key_to_participant_id` map using insert/overwrite semantics.
3. Map ends up 1:N; earlier participant mapping lost.
4. Incoming traffic for shared key resolves to whichever participant was inserted last.

## Root cause
- No startup validation for bijection; duplicate keys/IDs silently accepted.
- Identity registry constructed with overwrite semantics.

## Detection
- `len(unique_tls_keys) != len(participant_ids)` at startup.
- Duplicate `participant_id` or TLS key present in config.

## Corrective actions
1. Fail fast at startup if the participant ↔ TLS key mapping is not bijective.
2. Emit clear diagnostics listing conflicting participants and key.
3. Block listener startup until mapping is fixed.

## Verification
- Pending FM/FP/GR: need deterministic lab harness and prevention test proving startup failure on duplicates.

## Occurrences
- TLS key rotation drift led to two participants sharing a key; registry overwrite broke attribution.

## Links
- Failure pattern: `atlas/FP_007_identity_map_bijection_break.md`
- Failure mode: `lab/failure_modes/FM_004_identity_map_bijection/`
- Guardrail: `guardrails/GR_007_identity_bijection_startup_validation.md`
