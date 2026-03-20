---
ID: FM_010
Title: Read-only flag does not remove write tools
Hypothesis: A read-only runtime flag is advisory only, so write tools remain registered and callable.
Invariant: INV_003
Status: draft
related_pattern:
  - FP_003
---

# FM_010 — Read-only flag does not remove write tools

## Description
The server exposes write-capable tools even when launched in read-only mode because the flag only annotates intent and does not constrain tool registration.

## Trigger
- Server started with `read_only=True`.
- Tool registry still includes destructive operations.

## Preconditions
- Read-only intent is represented only as metadata, not enforced in registration.
- Tool dispatch does not check read-only mode before exposing operations.

## Failure mechanism (step-by-step)
1. Server starts with `read_only=True`.
2. Tool registration path unconditionally registers read and write tools.
3. Client discovery lists write tools; invocations succeed.

## Symptoms
- `list_tools` contains write operations in read-only mode.
- Write tool invocations succeed instead of returning `METHOD_NOT_FOUND`.

## Violated invariants
- INV_003 — policy intent is not projected into explicit capability-state transitions.

## Detection
- `read_only == true AND write_tools ∈ exposed_toolset`.
- Audit that no destructive tools are present when read-only is enabled.

## Recovery / prevention strategy
- Condition tool registration on the read-only flag.
- Reject write tool invocations with deterministic errors when read-only.

## Acceptance criteria
- `tests/test_repro_fm010.py` shows write tools exposed in read-only baseline.
- `tests/test_prevent_fm010.py` shows write tools absent in guarded registry when read-only.
- `tests/test_fm010_happy_path.py` shows write tools available in standard mode.
