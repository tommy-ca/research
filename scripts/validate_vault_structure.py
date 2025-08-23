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
import argparse

REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT = REPO_ROOT / "vault"

REQUIRED_TOP_LEVEL = {
    "00-inbox",
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
    "01-notes",
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

# Additional required sub-structure
REQUIRED_SUBSTRUCTURE = {
    "permanent": ["notes", "index.md"],
    "templates": ["daily-note.md", "project-note.md", "zettel-note.md"],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PKM vault structure")
    parser.add_argument("--strict", action="store_true", help="Treat unnumbered subdirectories as errors")
    args = parser.parse_args()
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

    # Sub-structure checks
    permanent_dir = VAULT / "permanent"
    if permanent_dir.exists():
        # Ensure notes directory
        if not (permanent_dir / "notes").exists():
            errors.append("Missing 'permanent/notes' directory")
        # Ensure index.md exists
        if not (permanent_dir / "index.md").exists():
            errors.append("Missing 'permanent/index.md'")
    else:
        errors.append("Missing 'permanent' directory")

    templates_dir = VAULT / "templates"
    if templates_dir.exists():
        for fname in REQUIRED_SUBSTRUCTURE["templates"]:
            path = templates_dir / fname
            if not path.exists():
                errors.append(f"Missing template: templates/{fname}")
            else:
                try:
                    head = path.read_text(encoding="utf-8").lstrip()
                    if not head.startswith("---"):
                        warnings.append(f"Template missing YAML frontmatter: templates/{fname}")
                except Exception:
                    warnings.append(f"Could not read template: templates/{fname}")
    else:
        errors.append("Missing 'templates' directory")

    # Report
    # In strict mode, unnumbered subdirectories are errors
    if args.strict and warnings:
        errors.append("Unnumbered subdirectories present under numbered parents (strict mode)")

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
