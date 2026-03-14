# PM_003 — Read-only intent not enforced in MCP server

## Summary
The filesystem MCP server exposed destructive tools even when launched with read-only intent, relying on advisory hints instead of runtime enforcement. This incident seeded FP_003.

## Impact
- Violated read-only invariant; automated agents could modify the filesystem despite read-only deployments.
- Safety depended on client compliance rather than server guarantees.

## Timeline (deterministic reproduction)
1. Start MCP filesystem server with read-only intent (no enforcement flag present).
2. `list_tools` includes write-capable operations (`write_file`, `edit_file`, `create_directory`, `move_file`).
3. Calls to write tools succeed; read-only promise is broken.

## Root cause
- Read-only intent expressed as metadata (`readOnlyHint`) with no enforcement in tool registration.
- Startup path always registered write tools.

## Detection
- In read-only mode: `write_tools ∈ exposed_toolset`.
- Attempts to write do not fail fast (`METHOD_NOT_FOUND`).

## Corrective actions
1. Add `--read-only` (or env) flag to suppress registration of write tools.
2. Ensure write calls return `METHOD_NOT_FOUND` when read-only is set.
3. Add integration tests covering `list_tools` and write calls in read-only mode.

## Verification
- E2E tests in upstream PR verify write tools absent and write calls rejected under read-only flag.

## Occurrences
- Filesystem MCP server ran in "read-only" intent but still registered write tools, enabling unintended writes.

## Links
- Failure pattern: `atlas/FP_003_read_only_enforcement_gap.md`
- Guardrail: `guardrails/GR_003_capability_surface_reduction.md`
