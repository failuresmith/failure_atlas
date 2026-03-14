# Add Strict Read-Only Enforcement to Filesystem MCP Server

## What
Adds a `--read-only` flag to the Reference Filesystem MCP Server.

When enabled, all destructive tools (`write_file`, `edit_file`, `create_directory`, `move_file`) are **not registered**.  
The server exposes only read operations, and attempts to call write tools return `METHOD_NOT_FOUND`.

## Why
`readOnlyHint` annotations currently signal safety to clients but do **not enforce it at runtime**.

This change enables hard read-only operation for:

- **Security:** prevent filesystem modifications by automated agents
- **Reliability:** avoid accidental writes in analysis/search use cases
- **Compliance:** enforce least-privilege deployments

## Implementation
- Adds `--read-only` CLI flag (and `READ_ONLY` env var)
- Conditionally registers write tools at startup
- Refactors startup usage messaging

## Behavior
- Default: full read/write toolset (unchanged)
- `--read-only`: write tools are absent from `list_tools`
- Calls to write tools return `METHOD_NOT_FOUND`

## Testing
E2E verification:

- Standard mode: write tools registered and functional
- Read-only mode:
  - write tools absent from `list_tools`
  - write calls return `METHOD_NOT_FOUND`
  - read tools remain functional


  Reference: https://github.com/modelcontextprotocol/servers/pull/3505

status: reported
