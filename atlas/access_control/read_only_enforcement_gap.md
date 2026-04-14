# [FM-003] Read-only Enforcement Gap
**Pattern:** Access Control & Authorization

**The Failure**
A system is set to "Read-Only" mode (e.g., for maintenance or an untrusted session), but write operations are still available because the enforcement is only at the UI layer or is just an "advisory" flag that individual tools ignore.

**Mechanism**
"Policy-Mechanism Gap". The policy intent (Read-Only) is not projected into the actual capability surface. The tools are registered with full permissions, and the system relies on the tool *itself* to check the flag, which many tools fail to do.

**Reproduction**
```python
# System set to read-only
session = Session(read_only=True)

# A 'Write' tool is still available in the registry
tool = session.get_tool("delete_user")

# The tool executes because it doesn't check session.read_only
tool.execute(user_id=123) # FAILURE: Data deleted in read-only session
```
Full reproduction: `lab/access_control/read_only_enforcement_gap/`

**Remediation**
Reduce the capability surface. If the session is read-only, do not even register or expose write-capable tools. Enforcement should be at the "Dispatch" or "Registry" level, not left to individual tool implementations.
