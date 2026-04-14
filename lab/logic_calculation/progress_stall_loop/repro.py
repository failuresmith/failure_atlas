class AgentLoop:
    def __init__(self, max_iters=5):
        self.max_iters = max_iters
        self.history = []

    def run_unsafe(self, action):
        print("--- Running Unsafe Loop ---")
        for i in range(self.max_iters):
            print(f"Step {i}: Executing {action}")
            # Simulate a constant error
            res = "Error: Invalid ID"
            print(f"Result: {res}")
        print("Loop finished (hit max iterations)")

    def run_safe(self, action):
        print("\n--- Running Safe Loop ---")
        for i in range(self.max_iters):
            print(f"Step {i}: Executing {action}")
            res = "Error: Invalid ID"

            state = (action, res)
            if state in self.history:
                print("STALL DETECTED: Repeating same action/result. Terminating.")
                return

            self.history.append(state)
            print(f"Result: {res}")

if __name__ == "__main__":
    loop = AgentLoop()
    loop.run_unsafe("read_file(id=123)")

    loop_safe = AgentLoop()
    loop_safe.run_safe("read_file(id=123)")
