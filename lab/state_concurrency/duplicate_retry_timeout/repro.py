import time
import uuid

class Database:
    def __init__(self):
        self.effects = {}
        self.committed_jobs = set()

    def apply_effect_unsafe(self, job_id, value):
        self.effects[job_id] = self.effects.get(job_id, 0) + value

    def apply_effect_safe(self, job_id, value):
        if job_id in self.committed_jobs:
            return
        self.effects[job_id] = self.effects.get(job_id, 0) + value
        self.committed_jobs.add(job_id)

def reproduce_failure():
    db = Database()
    job_id = "job_123"

    print(f"--- Reproducing FM-001 (Unsafe) ---")
    # Worker A starts
    print("Worker A: starting work...")
    # System times out Worker A and starts Worker B
    print("System: timeout! Worker A is taking too long. Starting Worker B...")

    # Worker B finishes first
    db.apply_effect_unsafe(job_id, 100)
    print("Worker B: committed effect 100")

    # Worker A finally finishes
    db.apply_effect_unsafe(job_id, 100)
    print("Worker A: committed effect 100")

    print(f"Final state for {job_id}: {db.effects[job_id]} (Expected 100, Got {db.effects[job_id]})")
    assert db.effects[job_id] == 200

def verify_fix():
    db = Database()
    job_id = "job_123"

    print(f"\n--- Verifying Fix (Safe) ---")
    # Worker B finishes first
    db.apply_effect_safe(job_id, 100)
    print("Worker B: committed effect 100")

    # Worker A tries to commit
    db.apply_effect_safe(job_id, 100)
    print("Worker A: attempted commit, but blocked/no-op")

    print(f"Final state for {job_id}: {db.effects[job_id]} (Expected 100, Got {db.effects[job_id]})")
    assert db.effects[job_id] == 100

if __name__ == "__main__":
    reproduce_failure()
    verify_fix()
    print("\nSUCCESS: FM-001 reproduced and fix verified.")
