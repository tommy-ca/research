#!/usr/bin/env python3
"""
PKM Ingest Pipeline - Ultra-Clean KISS Implementation

Simplified pipeline following KISS principles:
- Uses clean pkm_capture() function
- No complex class hierarchies
- Simple argument handling
"""
import argparse
import sys
from pathlib import Path

# Ensure src is importable
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.pkm.capture import pkm_capture


def main():
    """Simple ingestion pipeline - KISS compliant"""
    parser = argparse.ArgumentParser(description="PKM Ingestion Pipeline")
    parser.add_argument('--file', required=True, help="Input file to ingest")
    parser.add_argument('--vault', required=True, help="Vault directory")
    parser.add_argument('--gist-url', help="Optional gist URL for metadata")
    
    args = parser.parse_args()
    
    # Read content
    content = Path(args.file).read_text(encoding='utf-8')
    
    # Add gist URL as metadata if provided
    if args.gist_url:
        content = f"Source: {args.gist_url}\n\n{content}"
    
    # Use clean capture function
    result = pkm_capture(content, vault_path=Path(args.vault))
    
    if result.success:
        print(f"✅ Captured to: {result.filepath}")
        return 0
    else:
        print(f"❌ Capture failed: {result.error_message}")
        return 1


if __name__ == "__main__":
    sys.exit(main())