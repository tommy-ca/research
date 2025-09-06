"""
PKM Vault Manager - Manages vault operations with validation integration  
Task Group 1: TDD REFACTOR Phase - Production-optimized implementation

Following SOLID principles: Single responsibility, dependency inversion
Following KISS principle: Simple operations with clear error handling
Following DRY principle: Reuse validation patterns and avoid duplication
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
import tempfile
import shutil
from dataclasses import dataclass
from .base import CommandResult, CommandStatus


@dataclass
class VaultStructureResult:
    """
    Result of vault structure validation with detailed information
    
    SOLID: Single responsibility - only holds validation results
    KISS: Clear success/failure with descriptive error messages
    """
    success: bool
    errors: List[str]
    warnings: List[str] = None
    validated_paths: List[Path] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []
        if self.validated_paths is None:
            self.validated_paths = []


@dataclass
class CreateNoteResult:
    """
    Result of note creation with comprehensive status information
    
    SOLID: Single responsibility - only holds creation results
    DRY: Consistent with other result structures
    """
    success: bool
    created_file: Optional[Path] = None
    validation_results: List[Any] = None
    rollback_performed: bool = False
    error_message: str = ""
    
    def __post_init__(self):
        if self.validation_results is None:
            self.validation_results = []


class VaultManager:
    """
    Manages vault operations with validation integration and atomic operations
    
    SOLID: Single responsibility - only manages vault file operations
    SOLID: Dependency inversion - depends on validator abstraction
    KISS: Simple file operations with comprehensive error handling
    DRY: Centralized validation and rollback logic
    """
    
    def __init__(self, vault_path: Path, validator_runner=None):
        """
        Initialize vault manager with path and optional validation
        
        Args:
            vault_path: Path to PKM vault root
            validator_runner: Optional validation runner for file validation
        """
        self.vault_path = Path(vault_path)
        self.validator_runner = validator_runner
        self.required_directories = self._get_required_vault_directories()
    
    def _get_required_vault_directories(self) -> List[str]:
        """
        Get list of required vault directories - centralized configuration
        
        DRY: Single source of truth for vault structure
        KISS: Simple list of required directories
        """
        return [
            "00-inbox",
            "01-projects", 
            "02-areas",
            "03-resources",
            "04-archives",
            "daily",
            "permanent/notes",
            "templates"
        ]
    
    def validate_vault_structure(self) -> VaultStructureResult:
        """
        Validate vault structure with comprehensive checking
        
        Returns:
            VaultStructureResult with validation details
        """
        errors = []
        warnings = []
        validated_paths = []
        
        # Check if vault root exists
        if not self.vault_path.exists():
            return VaultStructureResult(
                success=False,
                errors=[f"Vault root directory does not exist: {self.vault_path}"],
                warnings=warnings,
                validated_paths=validated_paths
            )
        
        if not self.vault_path.is_dir():
            return VaultStructureResult(
                success=False,
                errors=[f"Vault path is not a directory: {self.vault_path}"],
                warnings=warnings,
                validated_paths=validated_paths
            )
        
        # Check required directories
        for dir_name in self.required_directories:
            dir_path = self.vault_path / dir_name
            validated_paths.append(dir_path)
            
            if not dir_path.exists():
                warnings.append(f"Optional directory missing: {dir_path}")
            elif not dir_path.is_dir():
                errors.append(f"Path exists but is not a directory: {dir_path}")
        
        return VaultStructureResult(
            success=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            validated_paths=validated_paths
        )
    
    def create_note(self, content: str, location: str, filename: str) -> CreateNoteResult:
        """
        Create note with atomic operations and validation integration
        
        Args:
            content: Note content to write
            location: Relative path within vault for note
            filename: Name of file to create
            
        Returns:
            CreateNoteResult with creation status and details
        """
        target_dir = self.vault_path / location
        target_file = target_dir / filename
        temp_file = None
        
        try:
            # Ensure target directory exists
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Create temporary file first for atomic operation
            temp_file = self._create_temporary_file(content)
            
            # Run validation on temporary file if validator available
            validation_results = []
            if self.validator_runner and hasattr(self.validator_runner, 'validate_file'):
                try:
                    validation_results = self.validator_runner.validate_file(temp_file)
                    if validation_results:
                        # Check if any results are errors (not just warnings)
                        has_errors = any(
                            getattr(result, 'severity', 'error') == 'error' 
                            for result in validation_results
                        )
                        if has_errors:
                            return CreateNoteResult(
                                success=False,
                                validation_results=validation_results,
                                error_message="Validation failed with errors"
                            )
                except Exception as validation_error:
                    return CreateNoteResult(
                        success=False,
                        error_message=f"Validation system error: {str(validation_error)}"
                    )
            
            # Atomic move from temp file to final location
            shutil.move(str(temp_file), str(target_file))
            temp_file = None  # Prevent cleanup since file was moved
            
            return CreateNoteResult(
                success=True,
                created_file=target_file,
                validation_results=validation_results
            )
            
        except Exception as e:
            # Rollback: cleanup temp file if it exists
            rollback_performed = False
            if temp_file and temp_file.exists():
                try:
                    temp_file.unlink()
                    rollback_performed = True
                except Exception:
                    pass  # Best effort cleanup
            
            return CreateNoteResult(
                success=False,
                error_message=f"Note creation failed: {str(e)}",
                rollback_performed=rollback_performed
            )
    
    def _create_temporary_file(self, content: str) -> Path:
        """
        Create temporary file with content - atomic operation helper
        
        Args:
            content: Content to write to temporary file
            
        Returns:
            Path to created temporary file
        """
        # Create temp file in same directory for atomic move
        temp_dir = self.vault_path / "temp"
        temp_dir.mkdir(exist_ok=True)
        
        with tempfile.NamedTemporaryFile(
            mode='w', 
            dir=temp_dir, 
            delete=False, 
            suffix='.md',
            encoding='utf-8'
        ) as f:
            f.write(content)
            return Path(f.name)
    
    def ensure_vault_structure(self) -> VaultStructureResult:
        """
        Ensure vault structure exists, creating missing directories
        
        Returns:
            VaultStructureResult with creation details
        """
        created_paths = []
        errors = []
        
        try:
            # Ensure vault root exists
            self.vault_path.mkdir(parents=True, exist_ok=True)
            
            # Create required directories
            for dir_name in self.required_directories:
                dir_path = self.vault_path / dir_name
                if not dir_path.exists():
                    dir_path.mkdir(parents=True, exist_ok=True)
                    created_paths.append(dir_path)
            
            return VaultStructureResult(
                success=True,
                errors=[],
                warnings=[f"Created directory: {path}" for path in created_paths],
                validated_paths=created_paths
            )
            
        except Exception as e:
            errors.append(f"Failed to create vault structure: {str(e)}")
            return VaultStructureResult(
                success=False,
                errors=errors,
                warnings=[],
                validated_paths=created_paths
            )
    
    def get_vault_statistics(self) -> Dict[str, Any]:
        """
        Get vault statistics for monitoring and insights
        
        Returns:
            Dictionary with vault statistics
        """
        stats = {
            "vault_path": str(self.vault_path),
            "total_files": 0,
            "total_directories": 0,
            "files_by_type": {},
            "directory_contents": {},
            "validation_enabled": self.validator_runner is not None
        }
        
        if not self.vault_path.exists():
            stats["error"] = "Vault path does not exist"
            return stats
        
        try:
            # Count files and directories
            for item in self.vault_path.rglob("*"):
                if item.is_file():
                    stats["total_files"] += 1
                    # Count by file type
                    suffix = item.suffix.lower()
                    stats["files_by_type"][suffix] = stats["files_by_type"].get(suffix, 0) + 1
                elif item.is_dir():
                    stats["total_directories"] += 1
            
            # Count files in each main directory
            for dir_name in self.required_directories:
                dir_path = self.vault_path / dir_name
                if dir_path.exists():
                    file_count = len([f for f in dir_path.rglob("*") if f.is_file()])
                    stats["directory_contents"][dir_name] = file_count
                else:
                    stats["directory_contents"][dir_name] = 0
            
        except Exception as e:
            stats["error"] = f"Failed to collect statistics: {str(e)}"
        
        return stats


class VaultOperationContext:
    """
    Context manager for vault operations with rollback capability
    
    SOLID: Single responsibility - manages operation context and cleanup
    KISS: Simple context manager with clear rollback semantics
    """
    
    def __init__(self, vault_manager: VaultManager, operation_name: str):
        self.vault_manager = vault_manager
        self.operation_name = operation_name
        self.created_files: List[Path] = []
        self.created_directories: List[Path] = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Exception occurred, perform rollback
            self._rollback()
    
    def add_created_file(self, file_path: Path):
        """Track created file for potential rollback"""
        self.created_files.append(file_path)
    
    def add_created_directory(self, dir_path: Path):
        """Track created directory for potential rollback"""
        self.created_directories.append(dir_path)
    
    def _rollback(self):
        """Perform rollback of created files and directories"""
        # Remove created files
        for file_path in reversed(self.created_files):
            try:
                if file_path.exists():
                    file_path.unlink()
            except Exception:
                pass  # Best effort cleanup
        
        # Remove created directories (in reverse order)
        for dir_path in reversed(self.created_directories):
            try:
                if dir_path.exists() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
            except Exception:
                pass  # Best effort cleanup


# Export main classes for external use
__all__ = [
    'VaultManager',
    'VaultStructureResult',
    'CreateNoteResult',
    'VaultOperationContext'
]