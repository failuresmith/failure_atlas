[<- Index](../../README.md)
# [FM-007] Identity Map Bijection Break
**Pattern:** Identification & Authentication

**The Failure**
Two different users end up sharing the same internal identity or session because the system allows a "last-writer-wins" collision in its identity registry. One user's traffic is suddenly attributed to another.

**Mechanism**
"Non-Bijective Mapping". The registry maps Public Keys to User IDs. If two users are accidentally configured with the same Public Key, a simple `map.put(key, user_id)` will overwrite the first user with the second. The system assumes uniqueness instead of enforcing it.

**Coding Example**
```python
identity_by_public_key = {}


def register_identity_unsafe(public_key, user_id):
    """Blind overwrite: last writer wins."""
    identity_by_public_key[public_key] = user_id


register_identity_unsafe("key_1", "alice")
register_identity_unsafe("key_1", "bob")

identity_by_public_key["key_1"]
# "bob" -> FAILURE:
# alice and bob were allowed to collapse into one lookup slot


def register_identity_safe(public_key, user_id):
    existing_user_id = identity_by_public_key.get(public_key)

    if existing_user_id is not None and existing_user_id != user_id:
        raise_fatal_identity_collision(public_key, existing_user_id, user_id)

    identity_by_public_key[public_key] = user_id
```

**Invariant Violated**
An external identity key must map to exactly one internal identity.

**Remediation**
Enforce a 1:1 (bijective) mapping. Use "Insert-Only" semantics or explicit collision checks at startup/registration. If a key is already mapped to a different ID, throw a fatal error instead of overwriting.

**Invariant Restored**
Identity registration is collision-safe. A key cannot be rebound to a different principal without an explicit, audited migration.

**References**
- [Near MPC Issue #2250](https://github.com/near/mpc/issues/2250)