#!/usr/bin/env python3
"""
Ingest a Markdown note into the PKM vault following the capture -> inbox process workflow.

Usage examples:
  - From file:
      scripts/ingest_markdown.py --file /path/to/note.md --source "https://gist.github.com/..." --tags research,pkm
  - From stdin:
      cat note.md | scripts/ingest_markdown.py --source "https://gist.github.com/..."

This script:
  1) Captures content to `vault/00-inbox` with metadata
  2) Processes the inbox to auto-categorize (PARA) and move the note
  3) Prints resulting location and summary
"""

import sys
import argparse
from pathlib import Path

# Ensure repo root is on sys.path so `src` is importable
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.pkm.core.capture import PkmCapture
from src.pkm.core.process_inbox import PkmInboxProcessor


def read_input_content(file_path: str | None) -> str:
    if file_path:
        p = Path(file_path)
        if not p.exists():
            raise SystemExit(f"File not found: {file_path}")
        return p.read_text(encoding="utf-8")
    # Read from stdin
    if sys.stdin.isatty():
        raise SystemExit("No --file provided and no stdin content. Provide input.")
    return sys.stdin.read()


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Markdown into PKM vault")
    parser.add_argument("--file", help="Path to markdown file to ingest", default=None)
    parser.add_argument("--vault", help="Path to PKM vault root", default="vault")
    parser.add_argument("--source", help="Source identifier/URL", default=None)
    parser.add_argument("--gist-url", help="Convenience alias for --source when ingesting from a GitHub Gist", default=None)
    parser.add_argument("--tags", help="Comma-separated tags", default=None)
    parser.add_argument("--auto-tags", help="Auto-generate basic tags from content when --tags not provided", action="store_true")

    args = parser.parse_args()

    content = read_input_content(args.file)
    # Tags: provided or optionally auto-generated
    source_url = args.source or (getattr(args, 'gist_url', None))

    if args.tags:
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    elif args.auto_tags:
        lower = content.lower()
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
    else:
        tags = []

    # Add gist tag if applicable
    if source_url and 'gist.github.com' in source_url:
        if '#source/gist' not in tags:
            tags.append('#source/gist')

    # 1) Capture to inbox
    capture = PkmCapture(args.vault)
    capture_result = capture.capture(content=content, source=source_url, tags=tags)

    inbox_rel_path = capture_result.file_path
    inbox_abs_path = Path(args.vault) / inbox_rel_path

    # 2) Process inbox (PARA categorization and move)
    processor = PkmInboxProcessor(args.vault)
    process_result = processor.process_inbox()

    # Determine where the captured file landed
    categorized = process_result.categorized
    new_location = None
    moved_filename = Path(inbox_abs_path.name)
    for filename, category in categorized.items():
        if filename == moved_filename.name:
            new_location = str(Path(args.vault) / category / filename)
            break

    # Output summary
    print("=== Ingestion Summary ===")
    print(f"Vault: {args.vault}")
    print(f"Source: {source_url or 'n/a'}")
    print(f"Captured: {inbox_abs_path}")
    print(f"Files found in inbox: {process_result.files_found}")
    print(f"Files processed: {process_result.files_processed}")
    if new_location:
        print(f"Moved to: {new_location}")
    else:
        print("Moved to: (could not determine; see report below)")
    if process_result.errors:
        print("Errors during processing:")
        for fname, err in process_result.errors.items():
            print(f"  - {fname}: {err}")
    print("\nReport:\n" + process_result.report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
