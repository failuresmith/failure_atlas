## What’s wrong
Credential mappings are appended to `SharedCredentialRegistry` on extension install, but not removed on uninstall/deactivate. So injection authority can outlive the extension until process restart (registry is in-memory).

<details>
<summary>Scenario (simple)</summary>

Install Gmail plugin → it registers credential host patterns + secret name → uninstall plugin → mappings remain in memory → HTTP tool may still think credentials exist for those hosts (injection attempts / approval semantics) until restart.
</details>


## Why it matters
Removed extensions can still influence HTTP credential injection + approval behavior (`has_credentials_for_host `→ `requires_approval()`), keeps credential injection authority active after uninstall in long-lived processes. 

Secrets still need to exist for injection to succeed, but this lifecycle mismatch breaks least-privilege expectations and can surprise operators.

## How I can help 

<details>
<summary>Proposed direction</summary>

Key mappings by extension ID, derive effective mappings from active extensions only, revoke on unregister/deactivate, add tests proving revocation.
</details>


If this is unintended, I can submit a PR to:

1. Key mappings by extension ID
2. Derive effective mappings from active extensions only
3. Revoke mappings on unregister/deactivate
4. Add tests proving authority disappears immediately



reference: https://github.com/nearai/ironclaw/issues/358

status: merged at https://github.com/nearai/ironclaw/pull/428
