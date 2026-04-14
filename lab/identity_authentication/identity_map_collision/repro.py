class IdentityRegistry:
    def __init__(self):
        self.key_to_id = {}

    def register_unsafe(self, key, user_id):
        # BUG: Blind overwrite
        self.key_to_id[key] = user_id

    def register_safe(self, key, user_id):
        if key in self.key_to_id and self.key_to_id[key] != user_id:
            raise ValueError(f"COLLISION: Key {key} already assigned to {self.key_to_id[key]}")
        self.key_to_id[key] = user_id

def reproduce_failure():
    print("--- Reproducing FM-007 (Unsafe) ---")
    reg = IdentityRegistry()
    reg.register_unsafe("key_1", "alice")
    reg.register_unsafe("key_1", "bob") # Overwrites Alice

    owner = reg.key_to_id["key_1"]
    print(f"Key_1 owner: {owner}")
    assert owner == "bob"

def verify_fix():
    print("\n--- Verifying Fix (Safe) ---")
    reg = IdentityRegistry()
    reg.register_safe("key_1", "alice")
    try:
        reg.register_safe("key_1", "bob")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        return
    assert False, "Should have raised ValueError"

if __name__ == "__main__":
    reproduce_failure()
    verify_fix()
