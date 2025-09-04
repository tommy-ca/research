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
    """Main CLI entry point - KISS refactored"""
    parser = argparse.ArgumentParser(description="PKM CLI")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("content", nargs="?", help="Content for commands")
    
    args = parser.parse_args()
    
    if args.command == "capture":
        _handle_capture_command(args.content)
    else:
        _handle_unknown_command(args.command)


def _handle_capture_command(content: str):
    """Handle capture command - KISS helper"""
    if not content:
        print("Error: capture command requires content")
        sys.exit(1)
    
    result = pkm_capture(content, vault_path=Path.cwd())
    _handle_capture_result(result)


def _handle_capture_result(result):
    """Handle capture result - KISS helper"""
    if result.success:
        print(f"Content captured successfully to {result.filename}")
        sys.exit(0)
    else:
        print(f"Error: {result.error}")
        sys.exit(1)


def _handle_unknown_command(command: str):
    """Handle unknown command - KISS helper"""
    print(f"Unknown command: {command}")
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