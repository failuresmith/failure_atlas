[<- Index](../../README.md)
# [FM-003] Read-only Enforcement Gap
**Pattern:** Access Control & Authorization

**The Failure**
A system is set to "Read-Only" mode (e.g., for maintenance or an untrusted session), but write operations are still available because the enforcement is only at the UI layer or is just an "advisory" flag that individual tools ignore.

**Mechanism**
"Policy-Mechanism Gap". The policy intent (Read-Only) is not projected into the actual capability surface. The tools are registered with full permissions, and the system relies on the tool *itself* to check the flag, which many tools fail to do.

**Coding Example**
```python
all_tools = {
    "get_info": {"mode": "read"},
    "delete_all": {"mode": "write"},
}


def build_tool_registry_unsafe(session_mode):
    """Returns every tool, regardless of session policy."""
    return all_tools


def start_session_unsafe():
    session_mode = "read_only"
    session_tools = build_tool_registry_unsafe(session_mode)
    return {"mode": session_mode, "tools": session_tools}


read_only_session = start_session_unsafe()
"delete_all" in read_only_session["tools"]
# True -> FAILURE:
# session says "read only", but write capability is still exposed


def build_tool_registry_safe(session_mode):
    if session_mode == "read_only":
        return {
            name: tool
            for name, tool in all_tools.items()
            if tool["mode"] == "read"
        }

    return all_tools


def start_session_safe():
    session_mode = "read_only"
    session_tools = build_tool_registry_safe(session_mode)
    return {"mode": session_mode, "tools": session_tools}


safe_session = start_session_safe()
"delete_all" in safe_session["tools"]
# False -> write tool never enters the capability surface
```

**Invariant Violated**
A read-only session must not be able to obtain write-capable tools.

**Remediation**
Reduce the capability surface. If the session is read-only, do not even register or expose write-capable tools. Enforcement should be at the "Dispatch" or "Registry" level, not left to individual tool implementations.

**Invariant Restored**
Session policy constrains the capability surface before execution. If the session is read-only, the runtime cannot dispatch a write tool because none is available.

**Reference**

- [modelcontextprotocol / servers PR 3505](https://github.com/modelcontextprotocol/servers/pull/3505)