SHELL := /bin/bash

.PHONY: test test-001 test-% new site serve help

# Run the full lab test suite
test:
	$(MAKE) -C lab test

# Run only Experiment 01 (happy path + FM_001)
test-001:
	$(MAKE) -C lab test-001

# Run a single FM repro by number (e.g., make test-002)
test-%:
	$(MAKE) -C lab test-$*

# Scaffold a new atlas entry from template/TEMPLATE.md
new:
	@bash scripts/new_atlas_entry.sh "$(TITLE)" "$(SLUG)"

# Build the static site into docs/
site:
	uv run --project site python site/build.py

# Serve the generated site locally at http://localhost:8000
serve:
	python -m http.server 8000 --directory docs

help:
	@printf "Targets:\n"
	@printf "  make test                     # run all lab tests (includes happy path)\n"
	@printf "  make test-001                 # experiment 01 tests only\n"
	@printf "  make test-XXX                 # repro for FM_XXX (e.g., 002)\n"
	@printf "  make new TITLE=\"...\" [SLUG=...]  # scaffold atlas entry from template\n"
	@printf "  make site                     # rebuild static docs into docs/\n"
	@printf "  make serve                    # serve docs/ locally on port 8000\n"
