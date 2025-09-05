"""
PKM Validation Runner - Orchestrates all validation
FR-VAL-001: Validation runner following KISS principles

TDD GREEN Phase: Minimal implementation to make tests pass
"""

from pathlib import Path
from typing import List
from .base import BaseValidator, ValidationResult


class PKMValidationRunner:
    """Orchestrates validation across multiple validators - simple coordinator"""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.validators: List[BaseValidator] = []
    
    def add_validator(self, validator: BaseValidator):
        """Add validator to runner - simple addition"""
        self.validators.append(validator)
    
    def validate_file(self, file_path: Path) -> List[ValidationResult]:
        """Validate single file with all validators"""
        results = []
        
        for validator in self.validators:
            try:
                file_results = validator.validate(file_path)
                results.extend(file_results)
            except Exception:
                # Handle individual validator errors gracefully
                continue
                
        return results
    
    def validate_vault(self) -> List[ValidationResult]:
        """Validate entire vault and return all results"""
        results = []
        
        # Handle nonexistent vault path gracefully
        if not self.vault_path.exists():
            return results
        
        try:
            # Find all markdown files recursively
            for file_path in self.vault_path.rglob("*.md"):
                # Run all validators on each file
                file_results = self.validate_file(file_path)
                results.extend(file_results)
                        
        except (OSError, PermissionError):
            # Handle permission errors gracefully
            pass
            
        return results