#!/usr/bin/env python3
"""
KC Validate: Validate a knowledge entry against simple quality gates.

Checks:
- Has YAML frontmatter
- Has at least 1 tag
- Has a source field
- Word count >= 300

Outputs a JSON summary to stdout and PASS/FAIL line. Exits 0 regardless
so that a pipeline can handle enrichment on failure.
"""

import sys
import json
from pathlib import Path
import yaml
import re


def extract_frontmatter_and_body(text: str):
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


def validate_file(path: Path) -> dict:
    content = path.read_text(encoding='utf-8')
    fm, body = extract_frontmatter_and_body(content)

    words = re.findall(r"\b\w+\b", body)
    word_count = len(words)

    has_frontmatter = bool(fm)
    tags = fm.get('tags') or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',') if t.strip()]
    has_tags = len(tags) >= 1
    has_source = 'source' in fm and bool(fm['source'])

    passed = has_frontmatter and has_tags and has_source and word_count >= 300

    return {
        'file': str(path),
        'passed': passed,
        'checks': {
            'has_frontmatter': has_frontmatter,
            'has_tags': has_tags,
            'has_source': has_source,
            'word_count': word_count,
            'word_count_ok': word_count >= 300,
        },
        'frontmatter': fm,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: kc_validate.py <markdown_file>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    result = validate_file(path)
    print(json.dumps(result, indent=2))
    print("PASS" if result['passed'] else "FAIL")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

