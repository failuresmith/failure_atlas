# Failure Patterns - observational studies

Notes on how real systems break — and how those failures can be contained.

Most investigations start with a simple question:

**What assumption is this system relying on — and what happens if it breaks?**

In practice, failures usually begin with small violations of invariants:

- hidden assumptions
- ambiguous state transitions
- adversarial or malformed inputs
- edge conditions under load

This repository records those investigations.

Each note follows roughly the same [structure](./TEMPLATE.md).

The purpose is simple: document these failures so they are not repeated, and make the underlying failure modes visible before they surface as incidents.

---

## Systems Covered

Examples come from different kinds of systems:

- distributed infrastructure
- cryptographic protocols
- permission and identity systems
- application lifecycle boundaries
- AI model behavior and evaluation

Despite their differences, many failures follow similar structural patterns.
