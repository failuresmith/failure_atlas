# Failure Pattern

ID:
Title:
Failure Domain:
Mechanism:
Severity:
Status:
Reproduced in:
Mitigated by:
Known occurrences:

Use an existing mechanism from [`taxonomy.md`](../taxonomy.md). Only mint a new mechanism when at least two FPs need the same discriminator.

This template is for the abstract `FP` layer, not the lab `FM` layer.
Keep it reusable across multiple concrete manifestations.

## Pattern statement

One paragraph describing the recurring higher-level failure pattern.

## Hidden assumption

What assumption quietly has to stay true for the system to remain correct?

## Invariant at risk

`INV_XXX` — the property that must hold all the time.

## Trigger family

What kinds of conditions or events tend to activate this pattern?

## Failure mechanism

Describe the structural cause at the abstract level, not the step-by-step FM script.

## Observable symptoms

What operators or systems would observe when this pattern manifests?

## Detection

How the violation can be observed or classified reliably.

## Lab reproductions

List the concrete `FM_XXX` manifestations that reproduce this pattern.

## Relevant guardrails

List the `GR_XXX` designs that prevent or contain this pattern.

## Known occurrences

List related `PM_XXX` postmortems or incident anchors when they exist.

## Related patterns

Neighboring `FP_XXX` entries that share boundaries or failure families.
