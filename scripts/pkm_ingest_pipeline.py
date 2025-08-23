#!/usr/bin/env python3
"""
PKM Ingest Pipeline: capture -> auto-categorize -> validate -> enrich -> atomic note

Input: a local markdown file (e.g., fetched from a gist)

Steps:
  1) Capture to inbox (adds frontmatter, optional source, tags)
  2) Process inbox (PARA categorization)
  3) Validate quality gates (kc_validate)
  4) If FAIL or categorized as archives, enrich and move to 04-resources
  5) Create an atomic note referencing the resource (updates indexes)

Outputs a concise summary with the final resource location and atomic note path.
"""

import sys
import argparse
from pathlib import Path
import json

# Ensure src is importable
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.pkm.core.capture import PkmCapture
from src.pkm.core.process_inbox import PkmInboxProcessor
from src.pkm.core.atomic_notes import PkmAtomicNote


def read_text(p: Path) -> str:
    return p.read_text(encoding='utf-8')


def extract_title_from_markdown(md: str) -> str:
    for line in md.splitlines():
        if line.strip().startswith('#'):
            return line.strip().lstrip('#').strip()[:80]
    # fallback to first non-empty line
    for line in md.splitlines():
        if line.strip():
            return line.strip()[:80]
    return "Untitled"


def main() -> int:
    ap = argparse.ArgumentParser(description="Run full PKM ingest workflow on a markdown file")
    ap.add_argument("--file", required=True, help="Path to local markdown file to ingest")
    ap.add_argument("--vault", default="vault", help="Path to vault root")
    ap.add_argument("--source", default=None, help="Source URL/identifier")
    ap.add_argument("--gist-url", default=None, help="Convenience alias for --source when ingesting from a GitHub Gist")
    ap.add_argument("--tags", default=None, help="Comma-separated tags; else auto-tags")
    args = ap.parse_args()

    in_path = Path(args.file)
    if not in_path.exists():
        print(f"File not found: {in_path}", file=sys.stderr)
        return 2

    content = read_text(in_path)
    # Capture
    cap = PkmCapture(args.vault)
    src_url = args.source or args.gist_url
    tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
    if src_url and 'gist.github.com' in src_url and '#source/gist' not in tags:
        tags.append('#source/gist')
    cap_res = cap.capture(content=content, source=src_url, tags=tags or None)
    captured = Path(args.vault) / cap_res.file_path

    # Process inbox
    proc = PkmInboxProcessor(args.vault)
    proc_res = proc.process_inbox()

    # Determine new location
    moved_path = None
    for fname, category in proc_res.categorized.items():
        if fname == captured.name:
            moved_path = Path(args.vault) / category / fname
            break

    if not moved_path or not moved_path.exists():
        moved_path = captured  # fallback

    # Validate
    import subprocess, json
    val = subprocess.run([
        sys.executable, str(REPO_ROOT / 'scripts' / 'kc_validate.py'), str(moved_path)
    ], capture_output=True, text=True)
    # Last JSON object should be in stdout
    val_json = {}
    try:
        # stdout contains JSON then PASS/FAIL line
        lines = [l for l in val.stdout.splitlines() if l.strip()]
        json_text = '\n'.join(lines[:-1]) if len(lines) > 1 else lines[0]
        val_json = json.loads(json_text)
    except Exception:
        val_json = {'passed': False}

    # Enrich if needed or miscategorized to archives
    categorized_as = moved_path.parts[-2] if len(moved_path.parts) >= 2 else ''
    needs_enrich = (not val_json.get('passed', False)) or ('archives' in categorized_as)
    final_resource_path = moved_path
    if needs_enrich:
        enr = subprocess.run([
            sys.executable, str(REPO_ROOT / 'scripts' / 'kc_enrich.py'), str(moved_path),
            '--vault', args.vault, '--category', '04-resources',
            *(('--source', args.source) if args.source else tuple())
        ], capture_output=True, text=True)
        # Parse enriched path from stdout
        for line in enr.stdout.splitlines():
            if line.startswith('ENRICHED: '):
                final_resource_path = Path(line.replace('ENRICHED: ', '').strip())
                break

    # Create an atomic note referencing the resource
    resource_md = read_text(final_resource_path)
    resource_title = extract_title_from_markdown(resource_md)
    note_content = (
        f"Reference: {final_resource_path}\n\n"
        f"[[{resource_title}]] — resource captured from {args.source or 'unknown source'}.\n\n"
        f"Key takeaways:\n- (add)\n- (add)\n"
    )
    atomic = PkmAtomicNote(args.vault)
    atomic_res = atomic.create_note(title=resource_title, content=note_content)

    print("=== PKM Ingest Pipeline Summary ===")
    print(f"Captured: {captured}")
    print(f"Moved: {moved_path}")
    print(f"Validated: {'PASS' if val_json.get('passed', False) else 'FAIL'}")
    print(f"Enriched: {'yes' if needs_enrich else 'no'}")
    print(f"Resource path: {final_resource_path}")
    print(f"Atomic note: {atomic_res.file_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
