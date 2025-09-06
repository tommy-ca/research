"""
PKM Agent System - Base Components
Task Group 1: TDD REFACTOR Phase - Production-optimized implementation

Following SOLID principles: Single responsibility, dependency inversion
Following KISS principle: Simple, readable, maintainable code
Following DRY principle: Reuse patterns and avoid duplication
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional
from enum import Enum


class CommandStatus(Enum):
    """Command execution status - centralized status definitions"""
    SUCCESS = "success"
    FAILURE = "failure"
    WARNING = "warning"
    VALIDATION_ERROR = "validation_error"


class ValidationSeverity(Enum):
    """Validation severity levels - consistent with validation system"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class CommandArgs:
    """
    Command arguments data structure with validation and defaults
    
    SOLID: Single responsibility - only holds command arguments
    KISS: Simple data structure with clear field purposes
    DRY: Reusable across all command handlers
    """
    command: str
    content: str = ""
    options: Dict[str, Any] = field(default_factory=dict)
    vault_path: Optional[Path] = None
    
    def __post_init__(self):
        """Validate and normalize command arguments"""
        # Normalize vault path
        if self.vault_path and not isinstance(self.vault_path, Path):
            self.vault_path = Path(self.vault_path)
        
        # Ensure options is always a dict
        if self.options is None:
            self.options = {}
        
        # Basic command validation
        if not self.command or not isinstance(self.command, str):
            raise ValueError("Command must be a non-empty string")


@dataclass  
class CommandResult:
    """
    Command result data structure with enhanced error handling
    
    SOLID: Single responsibility - only holds execution results
    KISS: Clear success/failure indication with detailed information
    DRY: Consistent result format across all handlers
    """
    success: bool
    message: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    validation_results: List[Any] = field(default_factory=list)
    status: CommandStatus = CommandStatus.SUCCESS
    execution_time_ms: Optional[float] = None
    
    def __post_init__(self):
        """Set appropriate status based on success and validation results"""
        if not self.success:
            self.status = CommandStatus.FAILURE
        elif self.validation_results:
            # Check if any validation results are errors
            has_errors = any(
                getattr(result, 'severity', None) == ValidationSeverity.ERROR.value 
                for result in self.validation_results
            )
            if has_errors:
                self.status = CommandStatus.VALIDATION_ERROR
            else:
                self.status = CommandStatus.WARNING
    
    @classmethod
    def success(cls, message: str = "", data: Dict[str, Any] = None) -> 'CommandResult':
        """Create successful result - convenience factory method"""
        return cls(
            success=True, 
            message=message,
            data=data or {},
            status=CommandStatus.SUCCESS
        )
    
    @classmethod
    def failure(cls, message: str, data: Dict[str, Any] = None) -> 'CommandResult':
        """Create failure result - convenience factory method"""
        return cls(
            success=False,
            message=message, 
            data=data or {},
            status=CommandStatus.FAILURE
        )
    
    @classmethod
    def validation_error(cls, message: str, validation_results: List[Any]) -> 'CommandResult':
        """Create validation error result - convenience factory method"""
        return cls(
            success=False,
            message=message,
            validation_results=validation_results,
            status=CommandStatus.VALIDATION_ERROR
        )


class BaseCommandHandler(ABC):
    """
    Abstract base class for all PKM command handlers
    
    SOLID: Interface segregation - only essential methods required
    SOLID: Dependency inversion - depends on abstractions not concretions
    KISS: Minimal interface with clear responsibilities
    """
    
    def __init__(self, vault_path: Path):
        """Initialize handler with vault path - dependency injection ready"""
        self.vault_path = Path(vault_path)
    
    @abstractmethod
    def handle(self, args: CommandArgs) -> CommandResult:
        """
        Handle command execution - abstract method
        
        Args:
            args: Command arguments with all necessary context
            
        Returns:
            CommandResult with execution status and details
        """
        pass
    
    @abstractmethod
    def validate_args(self, args: CommandArgs) -> CommandResult:
        """
        Validate command arguments before execution - abstract method
        
        Args:
            args: Command arguments to validate
            
        Returns:
            CommandResult indicating validation status
        """
        pass
    
    def get_handler_type(self) -> str:
        """Get handler type identifier - default implementation"""
        return self.__class__.__name__.lower().replace('handler', '')
    
    def supports_dry_run(self) -> bool:
        """Indicate if handler supports dry-run mode - default false"""
        return False


class CommandHandlerRegistry:
    """
    Registry for command handlers - centralized handler management
    
    SOLID: Single responsibility - only manages handler registration
    DRY: Centralized handler lookup and management
    KISS: Simple dictionary-based registry with validation
    """
    
    def __init__(self):
        self._handlers: Dict[str, BaseCommandHandler] = {}
    
    def register_handler(self, command: str, handler: BaseCommandHandler) -> None:
        """Register command handler with validation"""
        if not command or not isinstance(command, str):
            raise ValueError("Command must be a non-empty string")
        
        if not isinstance(handler, BaseCommandHandler):
            raise TypeError("Handler must be instance of BaseCommandHandler")
        
        self._handlers[command] = handler
    
    def get_handler(self, command: str) -> BaseCommandHandler:
        """Get handler for command with error handling"""
        if command not in self._handlers:
            available_commands = list(self._handlers.keys())
            raise ValueError(f"Unknown command '{command}'. Available commands: {available_commands}")
        
        return self._handlers[command]
    
    def list_commands(self) -> List[str]:
        """List all registered commands"""
        return list(self._handlers.keys())
    
    def has_command(self, command: str) -> bool:
        """Check if command is registered"""
        return command in self._handlers


# Export commonly used types for convenience
__all__ = [
    'BaseCommandHandler',
    'CommandArgs', 
    'CommandResult',
    'CommandHandlerRegistry',
    'CommandStatus',
    'ValidationSeverity'
]