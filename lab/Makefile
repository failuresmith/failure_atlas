UV ?= uv
PYTEST ?= $(UV) run pytest

.PHONY: sync test test-001 test-fm1 test-fm1-fix

# Setup deterministic env from uv.lock (includes dev deps like pytest)
sync:
	$(UV) sync --dev

# Run happy-path coverage plus all FM tests
test:
	$(PYTEST) tests/test_lab_happy_path.py failure_modes

# Experiment 01 only (happy path + FM_001 bundle)
test-001:
	$(PYTEST) tests/test_lab_happy_path.py failure_modes/FM_001_duplicate_retry/tests

# Reproduce FM_001 (expected failure in baseline scenario)
test-fm1:
	$(PYTEST) failure_modes/FM_001_duplicate_retry/tests/test_repro_fm001.py

# Prove FM_001 prevention (idempotent commit boundary)
test-fm1-fix:
	$(PYTEST) failure_modes/FM_001_duplicate_retry/tests/test_prevent_fm001.py
