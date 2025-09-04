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
from .inbox_processor import pkm_process_inbox
from .daily import pkm_daily
from .search import pkm_search


def main():
    """Main CLI entry point - KISS refactored"""
    parser = argparse.ArgumentParser(description="PKM CLI")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("content", nargs="?", help="Content for commands")
    
    args = parser.parse_args()
    
    if args.command == "capture":
        _handle_capture_command(args.content)
    elif args.command == "process-inbox":
        _handle_process_inbox_command()
    elif args.command == "daily":
        _handle_daily_command()
    elif args.command == "search":
        _handle_search_command(args.content)
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


def _handle_process_inbox_command():
    """Handle process-inbox command - KISS helper"""
    vault_path = Path.cwd() / 'vault'
    result = pkm_process_inbox(vault_path)
    
    if result.success:
        print(result.message)
        for filename, category in result.categorized_items:
            print(f"  {filename} → {category}")
        sys.exit(0)
    else:
        print(f"Error: {result.message}")
        sys.exit(1)


def _handle_daily_command():
    """Handle daily command - KISS helper"""
    vault_path = Path.cwd() / 'vault'
    result = pkm_daily(vault_path)
    
    if result.success:
        print(f"Daily note: {result.note_path}")
        if result.created_directories:
            print("Created directories:")
            for dir_path in result.created_directories:
                print(f"  {dir_path}")
        sys.exit(0)
    else:
        print(f"Error: {result.message}")
        sys.exit(1)


def _handle_search_command(query: str):
    """Handle search command - KISS helper"""
    if not query:
        print("Error: search command requires a query")
        sys.exit(1)
    
    vault_path = Path.cwd() / 'vault'
    result = pkm_search(query, vault_path)
    
    if result.success:
        print(f"Search results for '{result.query}': {result.total_matches} matches")
        for match in result.matches[:10]:  # Show top 10 results
            print(f"  {match.file_path}:{match.line_number} - {match.content[:80]}...")
        sys.exit(0)
    else:
        print(f"Error: {result.message}")
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