[<- Index](../../README.md)
# [FM-002] Extension Authority Persistence
**Pattern:** Access Control & Authorization

**The Failure**
A plugin or extension is uninstalled, but the permissions or API keys it was granted remain active in the system. An attacker who has compromised the (now deleted) plugin's credentials can still access the system.

**Mechanism**
The "Identity Registry" and the "Extension Lifecycle" are decoupled. When the extension is deleted, there is no hook to purge its associated authority records. The system checks if a token is *valid* but doesn't check if the *owner* still exists.

**Coding Example**
```python
installed_extensions = {}
granted_tokens = {}


def plugin_install_unsafe(plugin_id, scopes):
    """Install plugin and grant authority in a separate token registry."""
    installed_extensions[plugin_id] = {"status": "active"}

    token = issue_token_for(plugin_id)
    granted_tokens[token] = {
        "owner_plugin_id": plugin_id,
        "scopes": scopes,
    }
    return token


def plugin_uninstall_unsafe(plugin_id):
    """Uninstall plugin, but forget to clean up authority records."""
    del installed_extensions[plugin_id]

    # BUG:
    # granted_tokens still contains tokens that belong to plugin_id
    # Example stale record:
    # granted_tokens["tok_plugin_v1"] = {"owner_plugin_id": "plugin_v1", ...}


def verify_request_unsafe(token):
    """Authorizes from token registry alone."""
    if token in granted_tokens:
        return allow_request()

    return deny_request()


token = plugin_install_unsafe("plugin_v1", scopes=["read_data"])
plugin_uninstall_unsafe("plugin_v1")
verify_request_unsafe(token)
# FAILURE:
# request is accepted even though plugin_v1 no longer exists


def verify_request_safe(token):
    token_record = granted_tokens.get(token)
    if token_record is None:
        return deny_request()

    owner_plugin_id = token_record["owner_plugin_id"]
    owner_plugin = installed_extensions.get(owner_plugin_id)
    if owner_plugin is None or owner_plugin["status"] != "active":
        return deny_request()

    return allow_request()


def plugin_uninstall_safe(plugin_id):
    del installed_extensions[plugin_id]
    delete_all_tokens_owned_by(plugin_id, granted_tokens)
```

**Invariant Violated**
Authority must not outlive the principal that owns it.

**Remediation**
Bind authority to the component lifecycle. Use "Cascading Deletes" in the authority registry, or perform a "Live Existence Check" during token verification to ensure the principal still exists and is active.

**Invariant Restored**
Every authorization artifact resolves to a live, active principal at decision time. Deleting the extension removes its authority or makes any residual token unverifiable.

**References**

- [NearAI / Ironclaw Issue #358](https://github.com/nearai/ironclaw/issues/358)