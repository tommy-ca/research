#!/usr/bin/env python3
"""
Validate PKM vault structure per vault/README.md.

Checks:
- Required top-level directories exist: 00-inbox, 01-notes, 02-projects, 03-areas,
  04-resources, 05-archives, 06-synthesis, 07-journal, 08-media, 09-data, daily, permanent, templates
- No legacy top-level directories exist: 0-inbox, 1-projects, 3-resources, 4-archives,
  docs, resources, knowledge-base
- Optional: warn on unnumbered immediate subdirectories under numbered top-level dirs (02/03/04/05)

Exit code:
- 0 when required structure is OK (warnings allowed)
- 2 when violations are found
"""

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT = REPO_ROOT / "vault"

REQUIRED_TOP_LEVEL = {
    "00-inbox",
    "01-notes",
    "02-projects",
    "03-areas",
    "04-resources",
    "05-archives",
    "06-synthesis",
    "07-journal",
    "08-media",
    "09-data",
    "daily",
    "permanent",
    "templates",
}

FORBIDDEN_TOP_LEVEL = {
    "0-inbox",
    "1-projects",
    "2-areas",
    "3-resources",
    "4-archives",
    "docs",
    "resources",
    "knowledge-base",
}

NUMBERED_PARENTS = [
    "02-projects",
    "03-areas",
    "04-resources",
    "05-archives",
]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not VAULT.exists():
        print(f"Vault directory not found at: {VAULT}", file=sys.stderr)
        return 2

    top_level = {p.name for p in VAULT.iterdir() if p.is_dir()}

    # Required
    missing = sorted(REQUIRED_TOP_LEVEL - top_level)
    if missing:
        errors.append(f"Missing required top-level directories: {', '.join(missing)}")

    # Forbidden
    present_forbidden = sorted(FORBIDDEN_TOP_LEVEL & top_level)
    if present_forbidden:
        errors.append(f"Forbidden top-level directories present: {', '.join(present_forbidden)}")

    # Optional: numbering for children of numbered parents
    for parent in NUMBERED_PARENTS:
        parent_dir = VAULT / parent
        if not parent_dir.exists():
            continue
        for child in parent_dir.iterdir():
            if not child.is_dir():
                continue
            # Allow dot-dirs and special placeholders
            if child.name.startswith('.'):
                continue
            if not (len(child.name) >= 3 and child.name[:2].isdigit() and child.name[2] == '-'):
                warnings.append(
                    f"Unnumbered subdirectory under {parent}: {child.name} (expected 'NN-name')"
                )

    # Report
    if errors:
        print("❌ Vault structure validation failed:", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        if warnings:
            print("\n⚠️ Warnings:", file=sys.stderr)
            for w in warnings:
                print(f"- {w}", file=sys.stderr)
        return 2

    print("✅ Vault structure OK")
    if warnings:
        print("\n⚠️ Warnings:")
        for w in warnings:
            print(f"- {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
