class System:
    def __init__(self):
        self.active_plugins = set()
        self.tokens = {} # token -> plugin_id

    def install_plugin(self, plugin_id):
        self.active_plugins.add(plugin_id)
        token = f"tok_{plugin_id}"
        self.tokens[token] = plugin_id
        return token

    def uninstall_plugin(self, plugin_id):
        self.active_plugins.remove(plugin_id)
        # BUG: Forgot to purge tokens!

    def verify_token_unsafe(self, token):
        return token in self.tokens

    def verify_token_safe(self, token):
        plugin_id = self.tokens.get(token)
        return plugin_id is not None and plugin_id in self.active_plugins

def reproduce_failure():
    sys = System()
    print("--- Reproducing FM-002 (Unsafe) ---")

    token = sys.install_plugin("plugin_v1")
    print(f"Installed plugin_v1, got token: {token}")

    sys.uninstall_plugin("plugin_v1")
    print("Uninstalled plugin_v1")

    is_valid = sys.verify_token_unsafe(token)
    print(f"Token valid after uninstall? {is_valid}")
    assert is_valid == True # This is the failure

def verify_fix():
    sys = System()
    print("\n--- Verifying Fix (Safe) ---")

    token = sys.install_plugin("plugin_v1")
    sys.uninstall_plugin("plugin_v1")

    is_valid = sys.verify_token_safe(token)
    print(f"Token valid after uninstall (with check)? {is_valid}")
    assert is_valid == False

if __name__ == "__main__":
    reproduce_failure()
    verify_fix()
    print("\nSUCCESS: FM-002 reproduced and fix verified.")
