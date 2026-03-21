# FM_009 — Progress-stall loop from repeated invalid tool call

Minimal harness showing an agent repeating the same tool invocation + validation error until the iteration cap, and the guardrail that stops it early.

Artifacts:
- spec: `spec.md`
- scenario: `scenario.py`
- tests: `tests/` (`repro`, `prevent`, `happy_path`)
