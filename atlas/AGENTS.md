# Atlas Directory Guide

This file applies only to content inside `atlas/`.

The root [`AGENTS.md`](../AGENTS.md) remains the canonical source for repository purpose, taxonomy, the entry template, and shared authoring rules. This file exists to clarify how to apply those rules within `atlas/` without repeating them.

## What Belongs Here

- One markdown file per reusable failure pattern.
- Path shape: `atlas/<pillar>/<descriptive-slug>.md`
- One failure domain per entry.

## Directory Contract

- Put each entry in the pillar directory that best matches the violated boundary or invariant.
- Choose a descriptive slug that names the mechanism, not a one-off incident.
- Keep the file focused on a single reviewable failure pattern.

## Writing Focus

When authoring or editing an entry in `atlas/`, optimize for these questions:

- What failed?
- Why did it fail?
- What invariant was missing or violated?
- What fix restores that invariant?

If those answers are not obvious from the page, the entry is not ready.

## Local Quality Checks

- The coding example should make the broken boundary visible, not just hint at the symptom.
- The remediation should show the containment approach, not just say "validate" or "add a check".
- References are optional and should be included only when they make the mechanism clearer.
