class ToolRegistry:
    def __init__(self, read_only=False):
        self.read_only = read_only
        self.tools = {
            "get_info": {"type": "read", "func": lambda: "data"},
            "delete_all": {"type": "write", "func": lambda: "nuked!"}
        }

    def get_tools_unsafe(self):
        # BUG: Returns all tools regardless of mode
        return self.tools

    def get_tools_safe(self):
        if self.read_only:
            return {k: v for k, v in self.tools.items() if v["type"] == "read"}
        return self.tools

def reproduce_failure():
    print("--- Reproducing FM-003 (Unsafe) ---")
    reg = ToolRegistry(read_only=True)
    available_tools = reg.get_tools_unsafe()

    print(f"Mode: Read-Only. Available tools: {list(available_tools.keys())}")
    if "delete_all" in available_tools:
        print("FAILURE: 'delete_all' tool exposed in read-only mode!")
        assert True

def verify_fix():
    print("\n--- Verifying Fix (Safe) ---")
    reg = ToolRegistry(read_only=True)
    available_tools = reg.get_tools_safe()

    print(f"Mode: Read-Only. Available tools: {list(available_tools.keys())}")
    if "delete_all" not in available_tools:
        print("SUCCESS: Write tools filtered out of registry.")
        assert True
    else:
        assert False, "Write tools still present!"

if __name__ == "__main__":
    reproduce_failure()
    verify_fix()
