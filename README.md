# Failure Atlas

A field guide to how complex systems fail (safely).

The repository keeps four artifact types deliberately separate:

- `PM` records the real incident or validated occurrence.
- `FM` proves one concrete deterministic manifestation in the lab.
- `FP` explains the abstract recurring pattern above any one manifestation.
- `GR` specifies the prevention/containment design in operational detail.

They are complementary, not duplicates.

<details>
<summary>How?</summary>

> This is an engineering experiment

#### Studying domains of failure, not individual bugs

- Because bugs disappear
- Failure patterns repeat forever

</details>

---

Pipeline:
“Real failure → Minimal reproduction → Mechanism → Guardrail → Atlas update”

Artifact mapping:

- real failure = `PM` when an incident record exists
- minimal reproduction = `FM`
- mechanism = `FP`
- guardrail = `GR`

```mermaid
flowchart TD
  A[real failure]
  A --> P[PM - occurrence record]
  A --> B[FM - concrete minimal reproduction]
  B --> C[FP - abstract recurring pattern]
  C --> D[GR - detailed containment design]
  D --> E[Atlas]
```

PM anchors the real occurrence.
FM proves one manifestation.
FP generalizes the mechanism.
GR explains how prevention or containment actually works.

# example

- Real occurrence: [`PM_008_tool_authority_escalation`](./postmortems/PM_008_tool_authority_escalation.md)
- Failure Mode: [`FM_008_tool_authority_escalation`](./lab/failure_modes/FM_008_tool_authority_escalation/README.md)
- Failure Pattern: [`FP_008_tool_authority_escalation_via_prompt_injection`](./atlas/FP_008_tool_authority_escalation_via_prompt_injection.md)
- Guardrail: [`GR_008_explicit_tool_authorization_boundary`](./guardrails/GR_008_explicit_tool_authorization_boundary.md)

# Components

## Where to find postmortems
- Canonical PMs live in `postmortems/PM_XXX_*.md`.
- `lab/postmortems/PM_XXX_*.md` are thin pointers to the root to prevent drift; edit the root files only.

## [Atlas](./atlas/)

Explain the recurring failure pattern.

Artifacts:

- `FP_XXX_name.md` entries with YAML metadata
- abstract hidden assumption / trigger family / mechanism / detection
- links to representative PMs, concrete FM reproductions, and GR guardrails
- no step-by-step lab script and no guardrail implementation detail

## [Lab](./lab/)

Prove one concrete failure manifestation exists.

Artifacts:

- `FM_XXX_*` bundles (`spec.md`, `scenario.py`, tests)
- deterministic reproduction of a single activation path (happy/repro/prevent, recover when needed)
- explicit invariant references (`INV_XXX`)
- explicit parent `FP` and tested `GR` links

## [Guardrails](./guardrails/)

Document exactly how the failure can be prevented or contained.

Artifacts:

- `GR_XXX_name.md` entries with YAML metadata
- invariant-enforcing design pattern
- enforcement point, state/decision logic, observability, tradeoffs, and failure boundaries
- links back to FP/FM/PM as needed

## Contribute

- `make test` runs the full lab test suite in `lab/` (includes happy-path coverage)
- `make test-001` runs only Experiment 01 tests (happy path + FM_001 bundle)

### Adding or editing atlas items (FP/FM/GR/PM)

- **Do not create/edit `docs/*.html` manually.**
- Markdown is the source of truth:
  - `atlas/FP_XXX_*.md`
  - `guardrails/GR_XXX_*.md`
  - `postmortems/PM_XXX_*.md`
  - `lab/failure_modes/FM_XXX_*/spec.md` (or `README.md` fallback)
- Regenerate the static docs with:
  - `make site` (or `python site/build.py`)

### Site update policy

- The GitHub Pages deployment workflow builds the site from Markdown on every push to `main`.
- That means contributors should focus on source artifacts (FP/FM/GR/PM markdown + tests), not hand-maintained HTML.
- Local rebuild (`make site`) is still useful for preview/review before pushing.
