---
ID: FM_002
Title: Extension authority persists after uninstall
Hypothesis: Authority records keyed only by host/secret survive extension uninstall, leaving stale privilege scope.
Invariant: INV_005
Status: draft
related_pattern:
  - FP_002
---

# FM_002 — Extension authority persists after uninstall

## Description
Authority entries registered by an extension are stored independently of extension lifecycle. Uninstalling the extension leaves stale credential/tool bindings active until restart.

## Trigger
- Extension registers authority mappings.
- Extension is uninstalled or deactivated.
- Registry does not revoke mappings on lifecycle change.

## Preconditions
- Authority registry keyed by host/tool only, not by extension ID.
- In-memory registry survives uninstall events.

## Failure mechanism (step-by-step)
1. Extension installs and registers authority for host(s).
2. Extension is uninstalled.
3. Registry retains mappings because they are not keyed/derived from active extensions.
4. Subsequent authority checks still succeed using stale mappings.

## Symptoms
- `registry.contains(host)` is true after extension uninstall.
- Sensitive operations still pass authority checks for removed extensions.

## Violated invariants
- INV_005 — stale authority remains undetected and active.

## Detection
- `registry.contains(host) AND extension_active(extension_id) == false`.
- Audit asserting zero authority entries for inactive extensions.

## Recovery / prevention strategy
- Key authority entries by extension ID.
- On uninstall, revoke all mappings for that extension.
- Derive effective authority from active extensions only.

## Acceptance criteria
- `tests/test_repro_fm002.py` shows authority persists after uninstall in baseline registry.
- `tests/test_prevent_fm002.py` shows lifecycle-bound registry revokes authority on uninstall.
- `tests/test_fm002_happy_path.py` shows active extension retains authority while installed.
