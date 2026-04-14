# [FM-007] Identity Map Bijection Break
**Pattern:** Identification & Authentication

**The Failure**
Two different users end up sharing the same internal identity or session because the system allows a "last-writer-wins" collision in its identity registry. One user's traffic is suddenly attributed to another.

**Mechanism**
"Non-Bijective Mapping". The registry maps Public Keys to User IDs. If two users are accidentally configured with the same Public Key, a simple `map.put(key, user_id)` will overwrite the first user with the second. The system assumes uniqueness instead of enforcing it.

**Reproduction**
```python
registry = {}

# User A registers with Key X
registry["key_x"] = "user_A"

# User B accidentally has Key X too (e.g., config error)
registry["key_x"] = "user_B" # Overwrites A!

# Traffic from Key X is now ALWAYS user_B
current_user = registry["key_x"] # returns "user_B" -> FAILURE
```
Full reproduction: `lab/identity_authentication/identity_map_collision/`

**Remediation**
Enforce a 1:1 (bijective) mapping. Use "Insert-Only" semantics or explicit collision checks at startup/registration. If a key is already mapped to a different ID, throw a fatal error instead of overwriting.
