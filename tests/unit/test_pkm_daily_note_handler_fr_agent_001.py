"""
PKM Agent System - Daily Note Handler Tests
Task Group 2: TDD RED Phase - Daily Note Management (FR-AGENT-001)

TDD RED Phase: Comprehensive test suite defining expected behavior
All tests written BEFORE implementation - they should FAIL initially

Following TDD methodology:
1. RED: Write failing test first (THIS FILE)
2. GREEN: Write minimal code to pass
3. REFACTOR: Improve code while tests pass

Task 2.1-2.10: Daily Note Handler Requirements
"""

import pytest
from pathlib import Path
from typing import Dict, Any, Optional
import tempfile
import shutil
from datetime import datetime, date
from unittest.mock import Mock, patch

# Import will fail initially - this is expected in RED phase
try:
    from src.pkm.agents.base import BaseCommandHandler, CommandArgs, CommandResult
    from src.pkm.agents.handlers.daily_note_handler import DailyNoteHandler
    from src.pkm.agents.vault_manager import VaultManager
except ImportError:
    # Expected during RED phase - classes don't exist yet
    BaseCommandHandler = None
    CommandArgs = None
    CommandResult = None
    DailyNoteHandler = None
    VaultManager = None


class TestDailyNoteHandlerFoundation:
    """
    Task 2.1: Daily note handler foundation
    Tests for basic handler structure and inheritance
    """
    
    def setup_method(self):
        """Setup test environment with mock vault"""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        self.vault_path.mkdir(parents=True)
        
        # Create daily notes directory structure
        daily_dir = self.vault_path / "daily"
        daily_dir.mkdir()
    
    def teardown_method(self):
        """Cleanup test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_daily_note_handler_exists(self):
        """Task 2.1.1: DailyNoteHandler class should exist"""
        # This will fail initially - DailyNoteHandler doesn't exist
        assert DailyNoteHandler is not None, "DailyNoteHandler class should exist"
    
    def test_daily_note_handler_inherits_base_handler(self):
        """Task 2.1.2: DailyNoteHandler should inherit from BaseCommandHandler"""
        assert issubclass(DailyNoteHandler, BaseCommandHandler), \
            "DailyNoteHandler should inherit from BaseCommandHandler"
    
    def test_daily_note_handler_initialization(self):
        """Task 2.1.3: DailyNoteHandler should initialize properly"""
        handler = DailyNoteHandler(self.vault_path)
        
        assert handler.vault_path == self.vault_path
        assert hasattr(handler, 'daily_dir'), "Handler should have daily_dir attribute"
        assert handler.daily_dir == self.vault_path / "daily"
        assert hasattr(handler, 'templates_dir'), "Handler should have templates_dir attribute"
    
    def test_daily_note_handler_has_required_methods(self):
        """Task 2.1.4: DailyNoteHandler should implement required abstract methods"""
        handler = DailyNoteHandler(self.vault_path)
        
        assert hasattr(handler, 'handle'), "Handler should have handle() method"
        assert hasattr(handler, 'validate_args'), "Handler should have validate_args() method"
        assert callable(handler.handle), "handle() should be callable"
        assert callable(handler.validate_args), "validate_args() should be callable"


class TestDailyNoteDateHandling:
    """
    Task 2.2: Date parsing and validation
    Tests for date handling and format validation
    """
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        self.vault_path.mkdir(parents=True)
        (self.vault_path / "daily").mkdir()
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_parse_date_string_formats(self):
        """Task 2.2.1: Should parse various date string formats"""
        handler = DailyNoteHandler(self.vault_path)
        
        # Should handle multiple date formats
        test_cases = [
            ("2024-01-15", date(2024, 1, 15)),
            ("2024/01/15", date(2024, 1, 15)), 
            ("15-01-2024", date(2024, 1, 15)),
            ("Jan 15, 2024", date(2024, 1, 15)),
            ("15 January 2024", date(2024, 1, 15)),
            ("today", date.today()),
            ("yesterday", date.today().replace(day=date.today().day-1)),
            ("", date.today())  # Default to today
        ]
        
        for date_str, expected_date in test_cases:
            parsed_date = handler._parse_date(date_str)
            assert parsed_date == expected_date, f"Failed to parse '{date_str}'"
    
    def test_invalid_date_handling(self):
        """Task 2.2.2: Should handle invalid date strings gracefully"""
        handler = DailyNoteHandler(self.vault_path)
        
        invalid_dates = ["invalid", "2024-13-01", "32/01/2024", "February 30, 2024"]
        
        for invalid_date in invalid_dates:
            with pytest.raises(ValueError) as exc_info:
                handler._parse_date(invalid_date)
            assert "invalid date" in str(exc_info.value).lower()
    
    def test_generate_daily_note_path(self):
        """Task 2.2.3: Should generate correct daily note file paths"""
        handler = DailyNoteHandler(self.vault_path)
        
        test_date = date(2024, 3, 15)
        expected_path = self.vault_path / "daily" / "2024" / "03-march" / "2024-03-15.md"
        
        generated_path = handler._generate_daily_note_path(test_date)
        assert generated_path == expected_path
    
    def test_generate_directory_structure(self):
        """Task 2.2.4: Should generate hierarchical directory structure"""
        handler = DailyNoteHandler(self.vault_path)
        
        test_date = date(2024, 7, 4)
        # Daily structure: daily/YYYY/MM-month/YYYY-MM-DD.md
        expected_year_dir = self.vault_path / "daily" / "2024"
        expected_month_dir = expected_year_dir / "07-july"
        
        note_path = handler._generate_daily_note_path(test_date)
        
        # Should create parent directories
        handler._ensure_daily_directory_structure(test_date)
        
        assert expected_year_dir.exists(), "Year directory should be created"
        assert expected_month_dir.exists(), "Month directory should be created"


class TestDailyNoteCreation:
    """
    Task 2.3: Daily note creation logic
    Tests for creating new daily notes with templates
    """
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        self.vault_path.mkdir(parents=True)
        
        # Create required directories
        (self.vault_path / "daily").mkdir()
        (self.vault_path / "templates").mkdir()
        
        # Create daily note template
        template_content = """---
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
        template_path = self.vault_path / "templates" / "daily-note.md"
        template_path.write_text(template_content)
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_create_new_daily_note(self):
        """Task 2.3.1: Should create new daily note from template"""
        handler = DailyNoteHandler(self.vault_path)
        
        test_date = date(2024, 6, 10)
        result = handler._create_daily_note(test_date)
        
        assert result.success == True, "Daily note creation should succeed"
        assert result.created_file is not None, "Should return created file path"
        
        expected_path = self.vault_path / "daily" / "2024" / "06-june" / "2024-06-10.md"
        assert result.created_file == expected_path
        assert expected_path.exists(), "Daily note file should be created"
    
    def test_daily_note_template_application(self):
        """Task 2.3.2: Should apply template with date substitution"""
        handler = DailyNoteHandler(self.vault_path)
        
        test_date = date(2024, 6, 10)
        result = handler._create_daily_note(test_date)
        
        created_content = result.created_file.read_text()
        
        # Check template variables were substituted
        assert "date: 2024-06-10" in created_content
        assert "Daily Note - June 10, 2024" in created_content
        assert "---" in created_content  # Frontmatter
        assert "## Today's Focus" in created_content
        assert "## Tasks" in created_content
    
    def test_daily_note_content_structure(self):
        """Task 2.3.3: Should create well-structured daily note content"""
        handler = DailyNoteHandler(self.vault_path)
        
        test_date = date(2024, 12, 25)
        result = handler._create_daily_note(test_date)
        
        content = result.created_file.read_text()
        
        # Verify frontmatter structure
        assert content.startswith("---")
        frontmatter_end = content.find("---", 3)
        assert frontmatter_end > 0
        
        frontmatter_section = content[3:frontmatter_end]
        assert "date: 2024-12-25" in frontmatter_section
        assert "type: daily" in frontmatter_section
        assert "tags: [daily-note]" in frontmatter_section
        
        # Verify content sections
        content_body = content[frontmatter_end+3:]
        required_sections = [
            "# Daily Note - December 25, 2024",
            "## Today's Focus",
            "## Notes", 
            "## Tasks",
            "## Reflections",
            "## Tomorrow's Plan"
        ]
        
        for section in required_sections:
            assert section in content_body, f"Missing section: {section}"
    
    def test_create_daily_note_without_template(self):
        """Task 2.3.4: Should create basic daily note if template missing"""
        # Remove template
        (self.vault_path / "templates" / "daily-note.md").unlink()
        
        handler = DailyNoteHandler(self.vault_path)
        test_date = date(2024, 8, 1)
        result = handler._create_daily_note(test_date)
        
        assert result.success == True, "Should succeed even without template"
        
        content = result.created_file.read_text()
        # Should have basic structure
        assert "date: 2024-08-01" in content
        assert "type: daily" in content
        assert "# Daily Note" in content


class TestExistingDailyNoteHandling:
    """
    Task 2.4: Existing note handling
    Tests for opening/updating existing daily notes
    """
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        self.vault_path.mkdir(parents=True)
        (self.vault_path / "daily").mkdir()
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_detect_existing_daily_note(self):
        """Task 2.4.1: Should detect when daily note already exists"""
        handler = DailyNoteHandler(self.vault_path)
        
        # Create existing daily note
        test_date = date(2024, 5, 20)
        note_path = self.vault_path / "daily" / "2024" / "05-may" / "2024-05-20.md"
        note_path.parent.mkdir(parents=True)
        note_path.write_text("# Existing Daily Note")
        
        exists = handler._daily_note_exists(test_date)
        assert exists == True, "Should detect existing daily note"
        
        path = handler._get_daily_note_path(test_date)
        assert path == note_path, "Should return correct path"
    
    def test_open_existing_daily_note(self):
        """Task 2.4.2: Should open existing daily note without modification"""
        handler = DailyNoteHandler(self.vault_path)
        
        # Create existing daily note with content
        test_date = date(2024, 9, 5)
        note_path = self.vault_path / "daily" / "2024" / "09-september" / "2024-09-05.md"
        note_path.parent.mkdir(parents=True)
        original_content = """---
date: 2024-09-05
type: daily
---

# Daily Note - September 5, 2024

Existing content here.
"""
        note_path.write_text(original_content)
        
        result = handler._open_existing_daily_note(test_date)
        
        assert result.success == True, "Should successfully open existing note"
        assert result.created_file == note_path, "Should return existing file path"
        
        # Content should be unchanged
        current_content = note_path.read_text()
        assert current_content == original_content, "Existing content should be preserved"
    
    def test_handle_missing_daily_note(self):
        """Task 2.4.3: Should handle case when expected daily note is missing"""
        handler = DailyNoteHandler(self.vault_path)
        
        test_date = date(2024, 11, 1)
        exists = handler._daily_note_exists(test_date)
        
        assert exists == False, "Should detect when daily note doesn't exist"
    
    def test_append_content_to_existing_note(self):
        """Task 2.4.4: Should support appending content to existing daily note"""
        handler = DailyNoteHandler(self.vault_path)
        
        # Create existing note
        test_date = date(2024, 4, 15)
        note_path = self.vault_path / "daily" / "2024" / "04-april" / "2024-04-15.md"
        note_path.parent.mkdir(parents=True)
        note_path.write_text("# Daily Note\n\nExisting content.")
        
        additional_content = "\n\n## New Section\nAdditional notes"
        result = handler._append_to_daily_note(test_date, additional_content)
        
        assert result.success == True, "Should successfully append content"
        
        final_content = note_path.read_text()
        assert "Existing content." in final_content
        assert "## New Section" in final_content
        assert "Additional notes" in final_content


class TestDailyNoteCommandHandling:
    """
    Task 2.5: Command argument handling
    Tests for processing daily note commands and arguments
    """
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        self.vault_path.mkdir(parents=True)
        (self.vault_path / "daily").mkdir()
        (self.vault_path / "templates").mkdir()
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_validate_daily_command_args(self):
        """Task 2.5.1: Should validate daily note command arguments"""
        handler = DailyNoteHandler(self.vault_path)
        
        # Valid arguments
        valid_args = CommandArgs(
            command="daily",
            content="",
            options={"date": "2024-06-15"},
            vault_path=self.vault_path
        )
        
        result = handler.validate_args(valid_args)
        assert result.success == True, "Valid arguments should pass validation"
    
    def test_handle_daily_command_with_date_option(self):
        """Task 2.5.2: Should handle daily command with specific date"""
        handler = DailyNoteHandler(self.vault_path)
        
        args = CommandArgs(
            command="daily",
            content="",
            options={"date": "2024-07-04"}, 
            vault_path=self.vault_path
        )
        
        result = handler.handle(args)
        
        assert result.success == True, "Daily command should succeed"
        expected_path = self.vault_path / "daily" / "2024" / "07-july" / "2024-07-04.md"
        assert expected_path.exists(), "Daily note should be created for specified date"
    
    def test_handle_daily_command_default_today(self):
        """Task 2.5.3: Should default to today's date when no date specified"""
        handler = DailyNoteHandler(self.vault_path)
        
        args = CommandArgs(
            command="daily",
            content="",
            options={},
            vault_path=self.vault_path
        )
        
        with patch('src.pkm.agents.handlers.daily_note_handler.date') as mock_date:
            mock_date.today.return_value = date(2024, 8, 10)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            
            result = handler.handle(args)
            
            assert result.success == True, "Daily command should succeed with default date"
            expected_path = self.vault_path / "daily" / "2024" / "08-august" / "2024-08-10.md"
            assert expected_path.exists(), "Daily note should be created for today"
    
    def test_handle_daily_command_with_content(self):
        """Task 2.5.4: Should handle daily command with initial content"""
        handler = DailyNoteHandler(self.vault_path)
        
        initial_content = "Initial thoughts for the day"
        args = CommandArgs(
            command="daily",
            content=initial_content,
            options={"date": "2024-05-01"},
            vault_path=self.vault_path
        )
        
        result = handler.handle(args)
        
        assert result.success == True, "Daily command with content should succeed"
        
        created_file = self.vault_path / "daily" / "2024" / "05-may" / "2024-05-01.md"
        content = created_file.read_text()
        assert initial_content in content, "Initial content should be included in daily note"
    
    def test_invalid_command_args_handling(self):
        """Task 2.5.5: Should handle invalid command arguments gracefully"""
        handler = DailyNoteHandler(self.vault_path)
        
        # Invalid command name
        invalid_args = CommandArgs(
            command="not-daily",
            content="",
            options={},
            vault_path=self.vault_path
        )
        
        result = handler.validate_args(invalid_args)
        assert result.success == False, "Invalid command should fail validation"
        assert "daily" in result.message.lower(), "Error should mention daily command"


class TestDailyNoteIntegration:
    """
    Task 2.6: Integration with vault manager and validation
    Tests for integration with existing PKM system components
    """
    
    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        self.vault_path.mkdir(parents=True)
        (self.vault_path / "daily").mkdir()
        (self.vault_path / "templates").mkdir()
    
    def teardown_method(self):
        shutil.rmtree(self.temp_dir)
    
    def test_integration_with_vault_manager(self):
        """Task 2.6.1: Should integrate with VaultManager for file operations"""
        vault_manager = VaultManager(self.vault_path)
        handler = DailyNoteHandler(self.vault_path, vault_manager=vault_manager)
        
        assert handler.vault_manager == vault_manager, "Should accept VaultManager dependency"
    
    def test_daily_note_validation_integration(self):
        """Task 2.6.2: Should integrate with validation system for created notes"""
        from unittest.mock import Mock
        
        mock_validator = Mock()
        mock_validator.validate_file.return_value = []
        
        vault_manager = VaultManager(self.vault_path, validator_runner=mock_validator)
        handler = DailyNoteHandler(self.vault_path, vault_manager=vault_manager)
        
        test_date = date(2024, 3, 20)
        result = handler._create_daily_note(test_date)
        
        assert result.success == True, "Daily note creation should succeed with validation"
        # Validation should be triggered through VaultManager
        assert mock_validator.validate_file.called, "Validation should be triggered"
    
    def test_daily_note_frontmatter_compliance(self):
        """Task 2.6.3: Should create notes compliant with FR-VAL-002 frontmatter validation"""
        handler = DailyNoteHandler(self.vault_path)
        
        test_date = date(2024, 2, 14)
        result = handler._create_daily_note(test_date)
        
        content = result.created_file.read_text()
        
        # Should comply with frontmatter validation requirements
        assert content.startswith("---"), "Should start with frontmatter delimiter"
        assert "date: 2024-02-14" in content, "Should have date field"
        assert "type: daily" in content, "Should have type field"
        assert "tags:" in content, "Should have tags field"
        assert "status:" in content, "Should have status field"
    
    def test_daily_note_atomic_operations(self):
        """Task 2.6.4: Should use atomic operations for file creation"""
        handler = DailyNoteHandler(self.vault_path)
        
        # Mock failure during creation to test rollback
        with patch.object(handler, '_apply_daily_template') as mock_apply:
            mock_apply.side_effect = Exception("Template error")
            
            test_date = date(2024, 1, 1)
            result = handler._create_daily_note(test_date)
            
            assert result.success == False, "Should fail gracefully"
            
            # File should not exist due to rollback
            expected_path = self.vault_path / "daily" / "2024" / "01-january" / "2024-01-01.md"
            assert not expected_path.exists(), "Failed operation should not leave partial files"


# Test execution guard
if __name__ == "__main__":
    pytest.main([__file__, "-v"])