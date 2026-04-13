# Failure Patterns - observational studies

Notes on recurring ways systems break and how those failures can be contained.

Most investigations start with a simple question:

**What assumption is this system relying on — and what happens if it breaks?**

In practice, failures usually begin with small violations of invariants:

- hidden assumptions
- ambiguous state transitions
- adversarial or malformed inputs
- edge conditions under load

This repository records those investigations as complementary artifacts:

- `PM` for the real occurrence
- `FM` for one concrete minimal reproduction
- `FP` for the reusable higher-level pattern
- `GR` for the detailed containment design

Each note follows roughly the same [structure](./TEMPLATE.md).

The purpose is simple: document reusable failure patterns so they are not repeated, then anchor them to concrete FMs and guardrails.

---

## Systems Covered

Examples come from different kinds of systems:

- distributed infrastructure
- cryptographic protocols
- permission and identity systems
- application lifecycle boundaries
- AI model behavior and evaluation

Despite their differences, many failures follow similar structural patterns.
