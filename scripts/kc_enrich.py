#!/usr/bin/env python3
"""
KC Enrich: Enrich a knowledge entry to meet quality gates and align PARA category.

Actions:
- Ensure frontmatter exists
- Ensure at least one tag (auto-generate basic tags if none)
- Ensure source present (optional override via --source)
- Set type: resource and category: 03-resources unless overridden
- Optionally append a References section with the source URL if missing
- Move file to target PARA directory
"""

import sys
import argparse
from pathlib import Path
import yaml
import re

VAULT_DEFAULT = Path("vault")


def read_frontmatter_and_body(text: str):
    if not text.startswith('---'):
        return {}, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        fm = {}
    return fm, parts[2]


def write_frontmatter_and_body(fm: dict, body: str) -> str:
    yaml_content = yaml.dump(fm, default_flow_style=False)
    return f"---\n{yaml_content}---\n\n{body.lstrip()}"


def auto_tags(text: str):
    lower = text.lower()
    tags = []
    if any(k in lower for k in ["machine learning", "artificial intelligence", "ai"]):
        tags.append("#ai")
    if any(k in lower for k in ["neural network", "transformer", "deep learning"]):
        tags.append("#ai/deep-learning")
    if any(k in lower for k in ["nlp", "natural language"]):
        tags.append("#ai/nlp")
    if any(k in lower for k in ["python", "pandas", "numpy"]):
        tags.append("#programming/python")
    if any(k in lower for k in ["research", "study", "analysis"]):
        tags.append("#research")
    if any(k in lower for k in ["trading", "alpha", "factor", "crypto"]):
        tags.append("#domain/trading")
    return tags


def ensure_references(body: str, source: str | None) -> str:
    if not source:
        return body
    if "## References" in body or "# References" in body:
        return body
    return body.rstrip() + f"\n\n## References\n- {source}\n"


def enrich(file_path: Path, vault: Path, category: str, source_override: str | None) -> Path:
    text = file_path.read_text(encoding='utf-8')
    fm, body = read_frontmatter_and_body(text)
    if not fm:
        fm = {}
    # Ensure tags
    tags = fm.get('tags') or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',') if t.strip()]
    if not tags:
        tags = auto_tags(text)
    fm['tags'] = tags
    # Ensure source
    if source_override:
        fm['source'] = source_override
# Type and category
    fm['type'] = 'resource'
    fm['category'] = category
    # References section
    body = ensure_references(body, fm.get('source'))
    # Write back
    new_text = write_frontmatter_and_body(fm, body)
    file_path.write_text(new_text, encoding='utf-8')
    # Move to target directory
    target_dir = vault / category
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / file_path.name
    if target_path.resolve() != file_path.resolve():
        # Resolve name conflicts
        counter = 1
        final_target = target_path
        while final_target.exists():
            final_target = target_dir / f"{file_path.stem}-{counter}{file_path.suffix}"
            counter += 1
        file_path.rename(final_target)
        return final_target
    return file_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Enrich a knowledge entry and align PARA category")
    parser.add_argument("file", help="Path to markdown file")
    parser.add_argument("--vault", default=str(VAULT_DEFAULT), help="Path to vault root")
    parser.add_argument("--category", default="04-resources", help="Target PARA category path")
    parser.add_argument("--source", default=None, help="Override/add source URL")
    args = parser.parse_args()

    path = Path(args.file)
    vault = Path(args.vault)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    new_path = enrich(path, vault, args.category, args.source)
    print(f"ENRICHED: {new_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

