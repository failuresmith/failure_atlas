def admit_unsafe(current, maximum):
    if current > maximum: # BUG
        return False
    return True

def admit_safe(current, maximum):
    if current >= maximum:
        return False
    return True

def test_boundary():
    MAX = 5
    print(f"--- Testing Quota Boundary (Max={MAX}) ---")

    # At 5 connections, should we admit the 6th? No.
    can_admit_unsafe = admit_unsafe(5, MAX)
    print(f"Unsafe at limit (5): Admitted={can_admit_unsafe}")

    can_admit_safe = admit_safe(5, MAX)
    print(f"Safe at limit (5):   Admitted={can_admit_safe}")

    assert can_admit_unsafe == True  # Failure: admitted 6th
    assert can_admit_safe == False   # Success: blocked 6th

if __name__ == "__main__":
    test_boundary()
    print("\nSUCCESS: FM-006 reproduced and verified.")
