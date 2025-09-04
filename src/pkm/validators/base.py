"""
PKM Validation System - Base Components
FR-VAL-001: Core validation infrastructure following KISS principles

TDD GREEN Phase: Minimal implementation to make tests pass
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from abc import ABC, abstractmethod


@dataclass
class ValidationResult:
    """Result of validation operation - simple data structure"""
    file_path: Path
    rule: str
    severity: str  # "error" | "warning" | "info"
    message: str
    line_number: Optional[int] = None


class BaseValidator(ABC):
    """Abstract base class for all validators - single responsibility"""
    
    @abstractmethod
    def validate(self, file_path: Path) -> List[ValidationResult]:
        """Validate single file and return results"""
        pass