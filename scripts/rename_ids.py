#!/usr/bin/env python3
"""Apply ID renames across the repo from a central map.

Usage:
  python scripts/rename_ids.py --map scripts/id_map.yml

Edit scripts/id_map.yml (aliases: old -> new) once, run this script, then
empty aliases once the rename is complete. This keeps scattered markdown/tests
aligned without manual search/replace.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MAP = ROOT / "scripts" / "id_map.yml"
# Skip generated assets; rebuild docs site instead of rewriting generated pages.
SKIP_DIRS = {
    ".git",
    "docs/entries",
    "docs/assets",
    "docs/search-index.json",
    "docs/manifest.json",
    "site/static",
    "__pycache__",
}
ALLOW_EXTS = {".md", ".py", ".yml", ".yaml", ".toml", ".json", ".txt"}


def load_aliases(path: Path) -> dict[str, str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    aliases = data.get("aliases", {})
    if not isinstance(aliases, dict):
        raise ValueError("aliases must be a mapping old_id -> new_id")
    # normalize keys/values
    norm = {}
    for old, new in aliases.items():
        if not isinstance(old, str) or not isinstance(new, str):
            continue
        old = old.strip()
        new = new.strip()
        if old and new and old != new:
            norm[old] = new
    return norm


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return True
    return False


def rewrite_file(path: Path, aliases: dict[str, str]) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in aliases.items():
        pattern = rf"\b{re.escape(old)}\b"
        text = re.sub(pattern, new, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", dest="map_path", default=DEFAULT_MAP, type=Path)
    args = parser.parse_args()

    aliases = load_aliases(args.map_path)
    if not aliases:
        print("No aliases defined; nothing to do.")
        return

    changed = 0
    scanned = 0
    for path in ROOT.rglob("*"):
        if path.is_dir():
            continue
        if should_skip(path):
            continue
        if path.suffix.lower() not in ALLOW_EXTS:
            continue
        scanned += 1
        if rewrite_file(path, aliases):
            changed += 1
            print(f"rewrote {path.relative_to(ROOT)}")

    print(f"Scanned {scanned} files; updated {changed}.")


if __name__ == "__main__":
    main()
