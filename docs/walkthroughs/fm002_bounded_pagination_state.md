# FM_002 Walkthrough — Invariant → Repro → Guardrail

## 3-second read
- Invariant: `INV_006` — remote-driven state growth stays within a bound.
- Failure: each discover request allocates a new pagination cookie; no budget → unbounded growth.
- Guardrail: hard cookie budget with FIFO eviction; duplicates become bounded.

## Chain with code pointers
1) **Define invariant** — `atlas/FP_005_unbounded_pagination_cookie_state_amplification.md` context; implicit `INV_006`.
2) **Reproduce failure** — `lab/failure_modes/FM_002_unbounded_pagination_state/tests/test_repro_fm002.py` shows cookie count exceeds budget when enforcement is off.
3) **Detect violation** — assertion on `cookie_count > max_cookie_budget`; logged via `experiment_log`.
4) **Introduce guardrail** — `lab/policies/budget.py:CookieRegistry.insert(... enforce_budget=True)`; guardrail doc `guardrails/GR_005_bounded_pagination_state.md`.
5) **Prove fix** — `tests/test_prevent_fm002.py` verifies cookie count stays within budget and tracks evictions.
6) **Happy path** — `tests/test_fm002_happy_path.py` ensures bounded mode doesn’t break normal pagination.

## How to run
```bash
cd lab
pytest failure_modes/FM_002_unbounded_pagination_state/tests -q
```

## Artifacts to read
- Postmortem: `postmortems/PM_005_unbounded_pagination_state.md`
- Failure pattern: `atlas/FP_005_unbounded_pagination_cookie_state_amplification.md`
- Guardrail: `guardrails/GR_005_bounded_pagination_state.md`
