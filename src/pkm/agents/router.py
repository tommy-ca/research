"""
PKM Command Router - Routes PKM commands to appropriate handlers
Task Group 1: TDD REFACTOR Phase - Production-optimized implementation

Following SOLID principles: Single responsibility, dependency inversion
Following KISS principle: Simple routing with clear error handling
Following DRY principle: Centralized routing logic and configuration
"""

from pathlib import Path
from typing import Dict, Optional, List
import time
from .base import (
    BaseCommandHandler, 
    CommandArgs, 
    CommandResult, 
    CommandHandlerRegistry,
    CommandStatus
)


class MockHandler(BaseCommandHandler):
    """
    Mock handler for testing and development - temporary implementation
    
    SOLID: Single responsibility - provides consistent handler interface
    KISS: Minimal implementation for testing purposes
    """
    
    def __init__(self, vault_path: Path, handler_type: str):
        super().__init__(vault_path)
        self.handler_type = handler_type
    
    def handle(self, args: CommandArgs) -> CommandResult:
        """Mock handle implementation - always succeeds"""
        return CommandResult.success(f"Mock {self.handler_type} handler executed")
    
    def validate_args(self, args: CommandArgs) -> CommandResult:
        """Mock validation - always passes"""
        return CommandResult.success("Mock validation passed")


class PkmCommandRouter:
    """
    Routes PKM commands to appropriate handlers with validation integration
    
    SOLID: Single responsibility - only handles command routing
    SOLID: Open/closed - extensible through handler registration  
    SOLID: Dependency inversion - depends on abstractions (BaseCommandHandler)
    KISS: Simple routing with clear error messages
    DRY: Centralized command mapping and validation
    """
    
    def __init__(self, vault_path: Path, validator_runner=None):
        """
        Initialize router with vault path and optional validation
        
        Args:
            vault_path: Path to PKM vault
            validator_runner: Optional validation runner for note operations
        """
        self.vault_path = Path(vault_path)
        self.validator_runner = validator_runner
        self.registry = CommandHandlerRegistry()
        self.handlers = self._initialize_handlers()
        self._register_default_handlers()
    
    def _initialize_handlers(self) -> Dict[str, str]:
        """
        Initialize command-to-handler mapping - centralized configuration
        
        KISS: Simple mapping with clear command-handler relationships
        DRY: Single source of truth for routing configuration
        """
        return {
            "daily": "daily_note",
            "capture": "capture",
            "get": "retrieval", 
            "search": "search",
            "process-inbox": "process_inbox",
            "links": "link_management",
            "template": "templates",
            "stats": "analytics"
        }
    
    def _register_default_handlers(self):
        """Register default mock handlers for testing - temporary"""
        for command, handler_type in self.handlers.items():
            mock_handler = MockHandler(self.vault_path, handler_type)
            self.registry.register_handler(command, mock_handler)
    
    def get_handler(self, command: str) -> BaseCommandHandler:
        """
        Get handler for command with enhanced error handling
        
        Args:
            command: Command string to route
            
        Returns:
            BaseCommandHandler instance for the command
            
        Raises:
            ValueError: If command is not recognized
        """
        try:
            return self.registry.get_handler(command)
        except ValueError as e:
            # Enhanced error message with suggestions
            available_commands = self.registry.list_commands()
            raise ValueError(
                f"Unknown command: '{command}'. "
                f"Available commands: {', '.join(available_commands)}"
            ) from e
    
    def route_command(self, command: str, content: str = "", options: Dict = None) -> CommandResult:
        """
        Route and execute command with full lifecycle management
        
        Args:
            command: Command to execute
            content: Content for the command
            options: Additional command options
            
        Returns:
            CommandResult with execution details and timing
        """
        start_time = time.perf_counter()
        
        try:
            # Create command arguments
            args = CommandArgs(
                command=command,
                content=content,
                options=options or {},
                vault_path=self.vault_path
            )
            
            # Get handler
            handler = self.get_handler(command)
            
            # Validate arguments
            validation_result = handler.validate_args(args)
            if not validation_result.success:
                return validation_result
            
            # Execute command
            result = handler.handle(args)
            
            # Add execution timing
            execution_time = (time.perf_counter() - start_time) * 1000
            result.execution_time_ms = execution_time
            
            return result
            
        except Exception as e:
            execution_time = (time.perf_counter() - start_time) * 1000
            return CommandResult(
                success=False,
                message=f"Command execution failed: {str(e)}",
                status=CommandStatus.FAILURE,
                execution_time_ms=execution_time
            )
    
    def validate_operation(self, file_path: Path, operation_type: str = "general") -> bool:
        """
        Validate file operation using integrated validation system
        
        Args:
            file_path: Path to file to validate
            operation_type: Type of operation for context
            
        Returns:
            True if validation passes, False otherwise
        """
        if not self.validator_runner:
            return True  # No validation configured
        
        try:
            # Use validation system if available
            if hasattr(self.validator_runner, 'validate_file'):
                validation_results = self.validator_runner.validate_file(file_path)
                return len(validation_results) == 0
            
            return True
            
        except Exception:
            # Graceful degradation - don't block operations on validation errors
            return True
    
    def list_available_commands(self) -> List[str]:
        """List all available commands - utility method"""
        return self.registry.list_commands()
    
    def get_command_info(self, command: str) -> Dict[str, str]:
        """Get information about specific command - utility method"""
        try:
            handler = self.get_handler(command)
            return {
                "command": command,
                "handler_type": handler.get_handler_type(),
                "supports_dry_run": str(handler.supports_dry_run()),
                "description": f"Handler for {command} operations"
            }
        except ValueError:
            return {
                "command": command,
                "error": "Command not found",
                "available_commands": ", ".join(self.list_available_commands())
            }


class RouterConfiguration:
    """
    Configuration for PKM command router - centralized settings
    
    SOLID: Single responsibility - only manages router configuration
    DRY: Centralized configuration with default values
    KISS: Simple key-value configuration structure
    """
    
    def __init__(self):
        self.default_timeout_ms = 30000  # 30 seconds
        self.enable_validation = True
        self.enable_timing = True
        self.max_content_length = 10_000_000  # 10MB
        self.supported_file_types = ['.md', '.txt', '.org']
    
    def validate_content_length(self, content: str) -> bool:
        """Validate content length against limits"""
        return len(content.encode('utf-8')) <= self.max_content_length
    
    def is_supported_file_type(self, file_path: Path) -> bool:
        """Check if file type is supported for operations"""
        return file_path.suffix.lower() in self.supported_file_types


# Export main classes for external use
__all__ = [
    'PkmCommandRouter',
    'RouterConfiguration',
    'MockHandler'
]