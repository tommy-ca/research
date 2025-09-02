"""
PKM Package - Personal Knowledge Management System

TDD Implementation following engineering principles:
- Test-Driven Development (RED → GREEN → REFACTOR)
- FR-First prioritization (Functional Requirements before optimization)
- KISS principle (Keep It Simple, Stupid)
- SOLID principles for maintainable architecture
"""

from .capture import pkm_capture, CaptureResult
from .cli import main, capture_command

__all__ = ['pkm_capture', 'CaptureResult', 'main', 'capture_command']