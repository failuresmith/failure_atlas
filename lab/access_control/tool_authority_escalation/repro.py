class AgentRuntime:
    def __init__(self):
        self.sensitive_tools = {"read_config"}

    def execute_tool_unsafe(self, tool_name, args):
        # BUG: Trusts the model's choice
        print(f"Executing {tool_name} with {args}...")
        return "sensitive_data"

    def execute_tool_safe(self, tool_name, args, user_role):
        if tool_name in self.sensitive_tools and user_role != "admin":
            raise PermissionError(f"Access Denied: {user_role} cannot use {tool_name}")
        print(f"Executing {tool_name} with {args}...")
        return "sensitive_data"

def reproduce_failure():
    print("--- Reproducing FM-008 (Unsafe) ---")
    runtime = AgentRuntime()
    # Model was tricked into calling read_config for a guest
    runtime.execute_tool_unsafe("read_config", {"path": "/secret"})
    print("FAILURE: Sensitive tool executed for unauthorized request.")

def verify_fix():
    print("\n--- Verifying Fix (Safe) ---")
    runtime = AgentRuntime()
    try:
        runtime.execute_tool_safe("read_config", {"path": "/secret"}, user_role="guest")
    except PermissionError as e:
        print(f"Caught expected error: {e}")
        return
    assert False, "Should have raised PermissionError"

if __name__ == "__main__":
    reproduce_failure()
    verify_fix()
