#!/usr/bin/env python3
"""Generate index docs from registry/registry.yml (single source of truth).

Outputs:
- failure_index.md
- taxonomy.md (global index section)

Run: make registry
"""
from __future__ import annotations

import argparse
import yaml
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry" / "registry.yml"
FAILURE_INDEX = ROOT / "failure_index.md"
TAXONOMY = ROOT / "taxonomy.md"
LAB_FAILURE_INDEX = ROOT / "lab" / "docs" / "failure_mode_index.md"
LAB_TAXONOMY = ROOT / "lab" / "docs" / "taxonomy.md"

HEADER = "<!-- Generated from registry/registry.yml. Do not edit by hand. -->\n\n"


def slugify(title: str) -> str:
    import re

    slug = re.sub(r"[^A-Za-z0-9]+", "_", title.lower())
    return slug.strip("_")


def load_registry():
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    entries = data.get("entries", {}) if isinstance(data, dict) else {}
    # sort by numeric id
    def sort_key(item):
        fp_id = item[0]
        return int(fp_id.split("_")[1])

    return [v | {"id": k} for k, v in sorted(entries.items(), key=sort_key)]


def render_failure_index(entries):
    header = HEADER + dedent(
        """# Failure Index

Catalog of Failure Patterns in the FM → FP → GR pipeline (PM numbers align to FP IDs).

| ID | PM | Failure Pattern | Domain | Mechanism | Reproduced In | Mitigated By |
| --- | --- | --- | --- | --- | --- | --- |
"""
    )
    rows = []
    for e in entries:
        pm = e.get("pm") or "— (no PM yet)"
        pm_link = pm if pm.startswith("—") else f"[{pm}](./postmortems/{pm}_".replace("_", "_") + f"{e['title'].lower().replace(' ', '_')}.md)" if pm else "—"
        # safer: build path from id
        if isinstance(e.get("pm"), str):
            pm_link = f"[{e['pm']}](./postmortems/{e['pm']}_{e['title'].lower().replace(' ', '_')}.md)"
        elif e.get("pm"):
            pm_link = e.get("pm")
        else:
            pm_link = "— (no PM yet)"
        fp_slug = slugify(e['title'])
        fp_link = f"[ {e['title']} ](./atlas/{e['id']}_{fp_slug}.md)".replace("  ", " ")
        fm = e.get("fm") or "n/a"
        grs = e.get("gr") or []
        gr_cell = ", ".join(grs) if grs else "n/a"
        row = f"| {e['id']} | {pm_link} | {fp_link} | {e['domain']} | {e['mechanism']} | {fm} | {gr_cell} |"
        rows.append(row)
    return header + "\n".join(rows) + "\n\nCanonical taxonomy lives in [`taxonomy.md`](./taxonomy.md).\n"


def render_taxonomy(entries):
    intro = HEADER + dedent(
        """# Failure Taxonomy

Canonical catalog spine for Failure Patterns (`FP_XXX`) in `atlas/`. Keep just enough domain/mechanism detail to disambiguate labels; anything deeper belongs in the FP/FM/GR artifacts.

## Domains and mechanisms (single-line definitions)

- **Agent Runtime / Progress Ledger Omission** — agent loop counts steps but lacks state-change detection, so it spins on identical failures.

Reserved headers (define when needed): Concurrency; Recovery & Reconciliation; Distributed Coordination; Economic / Incentive Failures; Input Validation; Boundary Violations.

## Global index

| Domain                  | Mechanism                     | Failure Pattern                                                                                                              | FM     | GR     |
| ----------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------ | ------ |
"""
    )
    rows = []
    for e in entries:
        fm = e.get("fm") or "n/a"
        gr = e.get("gr") or []
        gr_cell = gr[0] if gr else "n/a"
        fp_slug = slugify(e['title'])
        fp_link = f"[ {e['title']} ](./atlas/{e['id']}_{fp_slug}.md)".replace("  ", " ")
        rows.append(
            f"| {e['domain']} | {e['mechanism']} | {fp_link} | {fm} | {gr_cell} |"
        )
    notes = dedent(
        """
Notes:

- `reproduced_in` and `mitigated_by` are list-valued in artifact metadata.
- Multiple FMs and GRs may link to one FP as the atlas grows.
- FM IDs align 1:1 with FP/GR numbering; FP_004 currently has no FM.
"""
    )
    return intro + "\n".join(rows) + "\n" + notes + "\n"


def render_lab_failure_mode_index(entries):
    header = HEADER + dedent(
        """# Failure Mode Index (Generated)

Source of truth: `registry/registry.yml`. Detailed FM specs/tests live in `lab/failure_modes/FM_XXX_*`.

| Failure Mode | Failure Pattern | Guardrail(s) | Postmortem | Status |
| --- | --- | --- | --- | --- |
"""
    )
    rows = []
    for e in entries:
        fm = e.get("fm") or "n/a"
        fp_slug = slugify(e['title'])
        fp_link = f"[{e['id']} {e['title']}](../../atlas/{e['id']}_{fp_slug}.md)"
        grs = e.get("gr") or []
        gr_cell = ", ".join(grs) if grs else "n/a"
        pm = e.get("pm") or "—"
        rows.append(
            f"| {fm} | {fp_link} | {gr_cell} | {pm} | {e.get('status','').title()} |"
        )
    note = "\nFM_004 currently unassigned (no lab repro for FP_004).\n"
    return header + "\n".join(rows) + note


def render_lab_taxonomy_pointer():
    return HEADER + dedent(
        """# Taxonomy (Generated)

This lab taxonomy view is generated from `registry/registry.yml`.
For canonical domain/mechanism mapping, see `../../taxonomy.md`.
"""
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit nonzero if files differ")
    args = parser.parse_args()

    entries = load_registry()
    outputs = {
        FAILURE_INDEX: render_failure_index(entries),
        TAXONOMY: render_taxonomy(entries),
        LAB_FAILURE_INDEX: render_lab_failure_mode_index(entries),
        LAB_TAXONOMY: render_lab_taxonomy_pointer(),
    }

    if args.check:
        dirty = []
        for path, content in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                dirty.append(path)
        if dirty:
            for p in dirty:
                print(f"Out of date: {p.relative_to(ROOT)}")
            raise SystemExit(1)
        print("Registry-synced files are up to date.")
        return

    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")

    print("Regenerated indexes from registry/registry.yml")


if __name__ == "__main__":
    main()
