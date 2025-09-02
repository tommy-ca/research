"""
PKM CLI Module - Command Line Interface

TDD GREEN Phase: Minimal CLI implementation to make tests pass
Following KISS principle: Simple command handling
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
from .capture import pkm_capture


def main():
    """
    Main CLI entry point
    
    TDD GREEN Phase: Minimal implementation for basic command handling
    """
    parser = argparse.ArgumentParser(description="PKM Command Line Interface")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("content", nargs="?", help="Content for commands that need it")
    
    args = parser.parse_args()
    
    if args.command == "capture":
        if not args.content:
            print("Error: capture command requires content")
            sys.exit(1)
        
        # Use current working directory as vault path
        vault_path = Path.cwd()
        result = pkm_capture(args.content, vault_path=vault_path)
        
        if result.success:
            print(f"Content captured successfully to {result.filename}")
            sys.exit(0)
        else:
            print(f"Error: {result.error}")
            sys.exit(1)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


def capture_command(content: str, vault_path: Optional[Path] = None) -> bool:
    """
    Capture command handler
    
    Simple wrapper around pkm_capture for CLI usage
    """
    result = pkm_capture(content, vault_path)
    return result.success


if __name__ == "__main__":
    main()