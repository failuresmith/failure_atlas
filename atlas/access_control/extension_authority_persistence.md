# [FM-002] Extension Authority Persistence
**Pattern:** Access Control & Authorization

**The Failure**
A plugin or extension is uninstalled, but the permissions or API keys it was granted remain active in the system. An attacker who has compromised the (now deleted) plugin's credentials can still access the system.

**Mechanism**
The "Identity Registry" and the "Extension Lifecycle" are decoupled. When the extension is deleted, there is no hook to purge its associated authority records. The system checks if a token is *valid* but doesn't check if the *owner* still exists.

**Reproduction**
```python
# Install plugin and grant it authority
plugin_id = registry.install("malicious_plugin")
token = auth.grant_token(plugin_id, scopes=["read_data"])

# Uninstall the plugin
registry.uninstall(plugin_id)

# The token SHOULD be invalid, but it still works
auth.verify(token) # returns True -> FAILURE
```
Full reproduction: `lab/access_control/extension_authority_persistence/`

**Remediation**
Bind authority to the component lifecycle. Use "Cascading Deletes" in the authority registry, or perform a "Live Existence Check" during token verification to ensure the principal still exists and is active.
