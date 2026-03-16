---
ID: PM_002
Title: PM_002 — Extension authority persists after uninstall
Summary: |-
  Credential mappings registered by an extension were not revoked on uninstall/deactivate, so HTTP credential injection authority could outlive the extension until process restart. This incident seeded FP_002.
---

# PM_002 — Extension authority persists after uninstall

## Summary
Credential mappings registered by an extension were not revoked on uninstall/deactivate, so HTTP credential injection authority could outlive the extension until process restart. This incident seeded FP_002.

## Impact
- Violated least-privilege expectations; removed extensions still influenced credential injection decisions.
- Risk of unintended credential exposure/approval semantics while registry remained stale.

## Timeline (deterministic reproduction)
1. Install extension; it registers credential host mappings in `SharedCredentialRegistry`.
2. Uninstall or deactivate the extension.
3. Mappings remain in memory; HTTP tool still treats credentials as available for those hosts.
4. Authority only disappears after process restart.

## Root cause
- Registry keyed by host/secret, not by extension ID.
- No revocation path on uninstall/deactivate to remove mappings.

## Detection
- `registry.contains(mapping) AND extension_active(extension_id) == false`.
- Approval logic observes credentials for hosts where owning extension is absent.

## Corrective actions
1. Key mappings by extension ID and derive effective registry from active extensions.
2. Revoke mappings on unregister/deactivate events.
3. Add regression tests proving authority disappears immediately on uninstall.

## Verification
- Regression tests (in upstream patch) prove mapping removal and absence of credential injection after uninstall.

## Occurrences
- Extension uninstall left credential mappings in memory, keeping injection authority active until restart.

## Links
- Failure pattern: `atlas/FP_002_extension_authority_persistence.md`
- Guardrail: `guardrails/GR_002_lifecycle_bound_authority.md`
