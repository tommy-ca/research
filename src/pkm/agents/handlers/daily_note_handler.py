"""
PKM Agent System - Daily Note Handler  
Task Group 2: TDD REFACTOR Phase - Production-optimized implementation

Following SOLID principles: Single responsibility, dependency inversion
Following KISS principle: Simple operations with clear error handling
Following DRY principle: Reuse templates and date handling patterns
"""

from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, date, timedelta
from dataclasses import dataclass, field
import calendar
import logging
from enum import Enum

from ..base import BaseCommandHandler, CommandArgs, CommandResult
from ..vault_manager import VaultManager, CreateNoteResult


class DateParseMode(Enum):
    """Date parsing modes for different input types"""
    STRICT = "strict"      # Exact format matching
    FLEXIBLE = "flexible"  # Multiple format attempts
    NATURAL = "natural"    # Natural language parsing


@dataclass
class DailyNoteConfig:
    """
    Configuration for daily note operations - centralized settings
    
    SOLID: Single responsibility - only manages configuration
    DRY: Centralized date formats and template settings
    KISS: Simple key-value configuration structure
    """
    date_formats: List[str] = field(default_factory=lambda: [
        "%Y-%m-%d",      # 2024-01-15  
        "%Y/%m/%d",      # 2024/01/15
        "%d-%m-%Y",      # 15-01-2024
        "%B %d, %Y",     # January 15, 2024
        "%d %B %Y",      # 15 January 2024
        "%b %d, %Y",     # Jan 15, 2024
    ])
    template_filename: str = "daily-note.md"
    directory_structure: str = "{year}/{month:02d}-{month_name}"
    filename_pattern: str = "{date}.md"
    natural_date_mappings: Dict[str, int] = field(default_factory=lambda: {
        "today": 0,
        "yesterday": -1,
        "tomorrow": 1
    })


@dataclass
class DailyNoteResult:
    """
    Result of daily note operations with comprehensive status information
    
    SOLID: Single responsibility - only holds operation results
    DRY: Consistent with other result structures
    """
    success: bool
    created_file: Optional[Path] = None
    message: str = ""
    was_existing: bool = False
    operation_type: str = ""
    validation_results: List[Any] = field(default_factory=list)


class DateParser:
    """
    Specialized date parser for daily notes - extracted for reuse
    
    SOLID: Single responsibility - only handles date parsing
    KISS: Clear parsing logic with error handling
    DRY: Centralized date parsing patterns
    """
    
    def __init__(self, config: DailyNoteConfig):
        self.config = config
    
    def parse_date(self, date_str: str, mode: DateParseMode = DateParseMode.FLEXIBLE) -> date:
        """Parse date string using configured formats and mode"""
        if not date_str or not date_str.strip():
            return date.today()
        
        date_str = date_str.strip().lower()
        
        # Handle natural language dates
        if mode in [DateParseMode.FLEXIBLE, DateParseMode.NATURAL]:
            natural_date = self._parse_natural_date(date_str)
            if natural_date is not None:
                return natural_date
        
        # Try configured date formats
        return self._parse_formatted_date(date_str)
    
    def _parse_natural_date(self, date_str: str) -> Optional[date]:
        """Parse natural language date expressions"""
        if date_str in self.config.natural_date_mappings:
            offset = self.config.natural_date_mappings[date_str]
            return date.today() + timedelta(days=offset)
        return None
    
    def _parse_formatted_date(self, date_str: str) -> date:
        """Parse date using configured formats"""
        for fmt in self.config.date_formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        # Try title case for month names
        try:
            return datetime.strptime(date_str.title(), "%b %d, %Y").date()
        except ValueError:
            pass
        
        raise ValueError(f"Unable to parse invalid date format: '{date_str}'")


class DailyNotePathManager:
    """
    Manages daily note file paths and directory structure
    
    SOLID: Single responsibility - only handles path operations
    KISS: Simple path generation with clear structure
    DRY: Centralized path logic and directory creation
    """
    
    def __init__(self, vault_path: Path, config: DailyNoteConfig):
        self.vault_path = Path(vault_path)
        self.daily_dir = self.vault_path / "daily"
        self.config = config
    
    def generate_note_path(self, target_date: date) -> Path:
        """Generate complete path for daily note file"""
        directory_path = self._generate_directory_path(target_date)
        filename = self._generate_filename(target_date)
        return directory_path / filename
    
    def ensure_directory_structure(self, target_date: date) -> None:
        """Ensure daily note directory structure exists"""
        directory_path = self._generate_directory_path(target_date)
        directory_path.mkdir(parents=True, exist_ok=True)
    
    def _generate_directory_path(self, target_date: date) -> Path:
        """Generate directory path for given date"""
        month_name = calendar.month_name[target_date.month].lower()
        directory_name = self.config.directory_structure.format(
            year=target_date.year,
            month=target_date.month,
            month_name=month_name
        )
        return self.daily_dir / directory_name
    
    def _generate_filename(self, target_date: date) -> str:
        """Generate filename for daily note"""
        return self.config.filename_pattern.format(
            date=target_date.strftime('%Y-%m-%d')
        )


class DailyNoteTemplateEngine:
    """
    Template engine for daily note content generation
    
    SOLID: Single responsibility - only handles template operations
    KISS: Simple template variable substitution
    DRY: Centralized template logic and variable handling
    """
    
    def __init__(self, templates_dir: Path, config: DailyNoteConfig):
        self.templates_dir = Path(templates_dir)
        self.config = config
    
    def apply_template(self, target_date: date, initial_content: str = "") -> str:
        """Apply daily note template with date substitution"""
        template_content = self._load_template()
        variables = self._generate_template_variables(target_date)
        
        try:
            formatted_content = template_content.format(**variables)
        except KeyError as e:
            logging.warning(f"Template variable missing: {e}")
            formatted_content = template_content
        
        return self._add_initial_content(formatted_content, initial_content)
    
    def _load_template(self) -> str:
        """Load daily note template or return default"""
        template_path = self.templates_dir / self.config.template_filename
        
        if template_path.exists():
            try:
                return template_path.read_text(encoding='utf-8')
            except Exception as e:
                logging.warning(f"Failed to load template: {e}")
        
        return self._get_default_template()
    
    def _generate_template_variables(self, target_date: date) -> Dict[str, str]:
        """Generate template variables for date substitution"""
        return {
            'date': target_date.strftime('%Y-%m-%d'),
            'date_formatted': target_date.strftime('%B %d, %Y'),
            'year': str(target_date.year),
            'month': f"{target_date.month:02d}",
            'day': f"{target_date.day:02d}",
            'month_name': calendar.month_name[target_date.month],
            'weekday': target_date.strftime('%A'),
            'iso_week': target_date.isocalendar()[1]
        }
    
    def _add_initial_content(self, template_content: str, initial_content: str) -> str:
        """Add initial content to template if provided"""
        if not initial_content.strip():
            return template_content
        
        # Insert initial content after template but before footer
        if "---\n*Daily note created automatically*" in template_content:
            return template_content.replace(
                "---\n*Daily note created automatically*",
                f"\n{initial_content}\n\n---\n*Daily note created automatically*"
            )
        else:
            return f"{template_content}\n\n{initial_content}\n"
    
    def _get_default_template(self) -> str:
        """Get default daily note template structure"""
        return """---
date: {date}
type: daily
tags: [daily-note]
status: active
---

# Daily Note - {date_formatted}

## Today's Focus
- 

## Notes


## Tasks
- [ ] 

## Reflections


## Tomorrow's Plan
- 

---
*Daily note created automatically*
"""


class DailyNoteHandler(BaseCommandHandler):
    """
    Daily Note Handler - Production-optimized implementation with helper classes
    
    SOLID: Single responsibility - orchestrates daily note operations using specialized helpers
    SOLID: Dependency inversion - depends on VaultManager abstraction
    KISS: Simple orchestration with comprehensive error handling
    DRY: Delegates to specialized helper classes to avoid duplication
    """
    
    def __init__(self, vault_path: Path, vault_manager: Optional[VaultManager] = None):
        """
        Initialize daily note handler with specialized helpers
        
        Args:
            vault_path: Path to PKM vault root
            vault_manager: Optional VaultManager for file operations
        """
        super().__init__(vault_path)
        self.vault_manager = vault_manager or VaultManager(vault_path)
        
        # Initialize configuration and helper classes
        self.config = DailyNoteConfig()
        self.date_parser = DateParser(self.config)
        self.path_manager = DailyNotePathManager(vault_path, self.config)
        self.template_engine = DailyNoteTemplateEngine(
            vault_path / "templates", 
            self.config
        )
        
        # Legacy properties for backward compatibility
        self.daily_dir = self.path_manager.daily_dir
        self.templates_dir = self.template_engine.templates_dir
    
    def handle(self, args: CommandArgs) -> CommandResult:
        """
        Handle daily note command with comprehensive error handling
        
        Args:
            args: Command arguments with date options and content
            
        Returns:
            CommandResult with execution status and details
        """
        try:
            target_date = self._parse_date_from_args(args)
            
            if self._daily_note_exists(target_date):
                result = self._handle_existing_note(target_date, args.content)
            else:
                result = self._handle_new_note(target_date, args.content)
            
            return self._format_command_result(result, target_date)
                
        except Exception as e:
            logging.error(f"Daily note operation failed: {e}")
            return CommandResult.failure(f"Daily note operation failed: {str(e)}")
    
    def validate_args(self, args: CommandArgs) -> CommandResult:
        """
        Validate daily note command arguments with enhanced validation
        
        Args:
            args: Command arguments to validate
            
        Returns:
            CommandResult indicating validation status
        """
        if args.command != "daily":
            return CommandResult.failure(
                f"Invalid command '{args.command}' - expected 'daily' command"
            )
        
        if "date" in args.options:
            try:
                self.date_parser.parse_date(args.options["date"])
            except ValueError as e:
                return CommandResult.failure(f"Invalid date format: {str(e)}")
        
        return CommandResult.success("Daily command arguments are valid")
    
    def _parse_date_from_args(self, args: CommandArgs) -> date:
        """Parse target date from command arguments or default to today"""
        if "date" in args.options:
            return self.date_parser.parse_date(args.options["date"])
        return date.today()
    
    def _handle_existing_note(self, target_date: date, content: str) -> DailyNoteResult:
        """Handle operations on existing daily note"""
        result = self._open_existing_daily_note(target_date)
        
        if result.success and content.strip():
            append_result = self._append_to_daily_note(target_date, content)
            if not append_result.success:
                return append_result
            result.operation_type = "opened_and_appended"
        else:
            result.operation_type = "opened"
        
        return result
    
    def _handle_new_note(self, target_date: date, content: str) -> DailyNoteResult:
        """Handle creation of new daily note"""
        result = self._create_daily_note(target_date, content)
        result.operation_type = "created"
        return result
    
    def _format_command_result(self, note_result: DailyNoteResult, target_date: date) -> CommandResult:
        """Format daily note result as command result"""
        if note_result.success:
            return CommandResult.success(
                message=f"Daily note ready: {note_result.created_file.name}",
                data={
                    "file_path": str(note_result.created_file),
                    "date": str(target_date),
                    "operation": note_result.operation_type,
                    "was_existing": note_result.was_existing
                }
            )
        else:
            return CommandResult.failure(note_result.message)
    
    # Legacy method names for backward compatibility with tests
    def _parse_date(self, date_str: str) -> date:
        """Legacy wrapper for date parsing - delegates to DateParser"""
        return self.date_parser.parse_date(date_str)
    
    def _generate_daily_note_path(self, target_date: date) -> Path:
        """Legacy wrapper for path generation - delegates to PathManager"""
        return self.path_manager.generate_note_path(target_date)
    
    def _get_daily_note_path(self, target_date: date) -> Path:
        """Legacy alias for path generation"""
        return self._generate_daily_note_path(target_date)
    
    def _ensure_daily_directory_structure(self, target_date: date) -> None:
        """Legacy wrapper for directory creation - delegates to PathManager"""
        self.path_manager.ensure_directory_structure(target_date)
    
    def _daily_note_exists(self, target_date: date) -> bool:
        """Check if daily note already exists for target date"""
        note_path = self.path_manager.generate_note_path(target_date)
        return note_path.exists()
    
    def _create_daily_note(self, target_date: date, initial_content: str = "") -> DailyNoteResult:
        """
        Create new daily note using atomic operations
        
        Args:
            target_date: Date for the daily note
            initial_content: Optional initial content to include
            
        Returns:
            DailyNoteResult with creation status
        """
        try:
            # Ensure directory structure exists
            self.path_manager.ensure_directory_structure(target_date)
            
            # Generate content from template - use legacy method for test compatibility
            content = self._apply_daily_template(target_date, initial_content)
            
            # Get target path and use vault manager for atomic creation
            note_path = self.path_manager.generate_note_path(target_date)
            location = str(note_path.parent.relative_to(self.vault_path))
            
            vault_result = self.vault_manager.create_note(content, location, note_path.name)
            
            return DailyNoteResult(
                success=vault_result.success,
                created_file=vault_result.created_file if vault_result.success else None,
                message=vault_result.error_message if not vault_result.success else "Daily note created successfully",
                validation_results=vault_result.validation_results
            )
                
        except Exception as e:
            logging.error(f"Daily note creation failed: {e}")
            return DailyNoteResult(
                success=False,
                message=f"Failed to create daily note: {str(e)}"
            )
    
    def _open_existing_daily_note(self, target_date: date) -> DailyNoteResult:
        """
        Open existing daily note without modification
        
        Args:
            target_date: Date for the daily note to open
            
        Returns:
            DailyNoteResult with operation status
        """
        note_path = self.path_manager.generate_note_path(target_date)
        
        if not note_path.exists():
            return DailyNoteResult(
                success=False,
                message="Daily note does not exist"
            )
        
        return DailyNoteResult(
            success=True,
            created_file=note_path,
            message="Opened existing daily note",
            was_existing=True
        )
    
    def _append_to_daily_note(self, target_date: date, content: str) -> DailyNoteResult:
        """
        Append content to existing daily note
        
        Args:
            target_date: Date for the daily note
            content: Content to append
            
        Returns:
            DailyNoteResult with append operation status
        """
        note_path = self.path_manager.generate_note_path(target_date)
        
        if not note_path.exists():
            return DailyNoteResult(
                success=False,
                message="Cannot append to non-existent daily note"
            )
        
        try:
            existing_content = note_path.read_text(encoding='utf-8')
            new_content = existing_content + content
            note_path.write_text(new_content, encoding='utf-8')
            
            return DailyNoteResult(
                success=True,
                created_file=note_path,
                message="Content appended to daily note"
            )
        except Exception as e:
            logging.error(f"Failed to append to daily note: {e}")
            return DailyNoteResult(
                success=False,
                message=f"Failed to append content: {str(e)}"
            )
    
    def _apply_daily_template(self, target_date: date, initial_content: str = "") -> str:
        """Legacy wrapper for template application - delegates to TemplateEngine"""
        return self.template_engine.apply_template(target_date, initial_content)