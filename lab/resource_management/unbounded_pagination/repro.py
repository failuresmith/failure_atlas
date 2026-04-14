class Server:
    def __init__(self, limit=None):
        self.cursor_registry = {}
        self.limit = limit

    def handle_request_unsafe(self, request_id):
        # BUG: Creates a new cursor for every request without bounds
        self.cursor_registry[request_id] = "some_large_state_object"

    def handle_request_safe(self, request_id):
        if self.limit and len(self.cursor_registry) >= self.limit:
            # Evict oldest or reject
            oldest = next(iter(self.cursor_registry))
            del self.cursor_registry[oldest]
        self.cursor_registry[request_id] = "some_large_state_object"

def reproduce_failure():
    print("--- Reproducing FM-005 (Unsafe) ---")
    srv = Server()
    for i in range(10000):
        srv.handle_request_unsafe(f"req_{i}")

    print(f"Registry size: {len(srv.cursor_registry)}")
    assert len(srv.cursor_registry) == 10000

def verify_fix():
    print("\n--- Verifying Fix (Safe) ---")
    srv = Server(limit=100)
    for i in range(10000):
        srv.handle_request_safe(f"req_{i}")

    print(f"Registry size with limit: {len(srv.cursor_registry)}")
    assert len(srv.cursor_registry) <= 100

if __name__ == "__main__":
    reproduce_failure()
    verify_fix()
