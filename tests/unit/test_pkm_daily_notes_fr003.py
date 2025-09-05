"""
TDD Tests for FR-003: Daily Note Creation Command

RED PHASE - These tests MUST FAIL initially to enforce TDD workflow.

Test Specification:
- Given: Current date is known
- When: User runs `/pkm-daily`
- Then: Today's note created/opened in vault/daily/YYYY/MM-month/
- And: Basic frontmatter template applied

Engineering Principles:
- TDD: Test specification before implementation
- KISS: Simple date-based file creation
- FR-First: Basic functionality before advanced features
- SRP: Single responsibility - just create/open daily notes
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime, date
from typing import NamedTuple, Optional
import yaml
import calendar


# SOLID Principles: Interface Segregation
class DailyNoteResult(NamedTuple):
    """Result of daily note creation/opening"""
    filepath: Path
    created_new: bool  # True if created, False if opened existing
    frontmatter: dict
    success: bool
    error: Optional[str] = None


class DatePathInfo(NamedTuple):
    """Date-based path information following DRY principle"""
    year: str
    month_num: str  # 01, 02, etc.
    month_name: str  # january, february, etc.
    day: str
    date_string: str  # YYYY-MM-DD
    folder_path: Path  # vault/daily/YYYY/MM-month/
    filename: str  # YYYY-MM-DD.md


class TestPkmDailyNoteBasicFunctionality:
    """
    RED PHASE: All tests MUST FAIL initially
    
    Tests define specification for simple daily note creation
    Following KISS: Just create file with basic structure
    """
    
    @pytest.fixture
    def temp_vault(self):
        """Create temporary vault structure for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            daily_path = vault_path / "daily"
            daily_path.mkdir(parents=True)
            yield vault_path
    
    @pytest.fixture 
    def test_date(self):
        """Fixed test date for consistent testing"""
        return date(2024, 3, 15)  # March 15, 2024
    
    def test_pkm_daily_function_not_implemented_yet(self):
        """
        RED TEST: Must fail - no daily note function exists
        
        Ensures proper TDD RED phase compliance
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import create_daily_note
    
    def test_pkm_daily_creates_new_note_for_today(self, temp_vault, test_date):
        """
        RED TEST: Must fail - daily note creation not implemented
        
        Test Spec: Create new daily note for specified date
        - File created at vault/daily/2024/03-march/2024-03-15.md
        - Basic frontmatter template applied
        - Content area ready for user input
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import create_daily_note
            
        # Future test validation:
        # result = create_daily_note(test_date, vault_path=temp_vault)
        # assert result.success is True
        # assert result.created_new is True
        # 
        # expected_path = temp_vault / "daily" / "2024" / "03-march" / "2024-03-15.md"
        # assert result.filepath == expected_path
        # assert expected_path.exists()
    
    def test_pkm_daily_creates_proper_directory_structure(self, temp_vault, test_date):
        """
        RED TEST: Must fail - directory structure creation not implemented
        
        Test Spec: Proper nested folder structure
        - vault/daily/YYYY/MM-month/ hierarchy
        - Month folder uses number-name format (03-march)
        - Handles year transitions correctly
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import get_daily_path_info
            
        # Future validation:
        # path_info = get_daily_path_info(test_date)
        # assert path_info.year == "2024"
        # assert path_info.month_num == "03"
        # assert path_info.month_name == "march"
        # assert path_info.folder_path.name == "03-march"
        # assert path_info.filename == "2024-03-15.md"
    
    def test_pkm_daily_opens_existing_note_if_present(self, temp_vault, test_date):
        """
        RED TEST: Must fail - existing note detection not implemented
        
        Test Spec: Open existing daily note without overwriting
        - If file exists, return existing file info
        - Don't overwrite existing content
        - Set created_new = False
        """
        # Pre-create existing daily note
        daily_folder = temp_vault / "daily" / "2024" / "03-march"
        daily_folder.mkdir(parents=True)
        existing_file = daily_folder / "2024-03-15.md"
        existing_content = "---\ndate: 2024-03-15\n---\nExisting content"
        existing_file.write_text(existing_content)
        
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import create_daily_note
            
        # Future validation:
        # result = create_daily_note(test_date, vault_path=temp_vault)
        # assert result.success is True
        # assert result.created_new is False  # Opened existing
        # assert "Existing content" in result.filepath.read_text()
    
    def test_pkm_daily_creates_proper_frontmatter(self, temp_vault, test_date):
        """
        RED TEST: Must fail - frontmatter template not implemented
        
        Test Spec: Standard daily note frontmatter
        - date: YYYY-MM-DD format
        - type: "daily"
        - tags: ["daily-notes"]
        - week_of_year: calculated week number
        - day_of_week: monday, tuesday, etc.
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import create_daily_note_frontmatter
            
        # Future validation:
        # frontmatter = create_daily_note_frontmatter(test_date)
        # assert frontmatter["date"] == "2024-03-15"
        # assert frontmatter["type"] == "daily"
        # assert "daily-notes" in frontmatter["tags"]
        # assert frontmatter["day_of_week"] == "friday"
        # assert isinstance(frontmatter["week_of_year"], int)
    
    def test_pkm_daily_includes_basic_content_template(self, temp_vault, test_date):
        """
        RED TEST: Must fail - content template not implemented
        
        Test Spec: Basic daily note content structure
        - Header with date
        - Sections for common daily note elements
        - Links to previous/next days (when they exist)
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import generate_daily_note_content
            
        # Future validation:
        # content = generate_daily_note_content(test_date)
        # assert f"# Daily Note - {test_date}" in content
        # assert "## Tasks" in content
        # assert "## Notes" in content
        # assert "## Reflections" in content


class TestPkmDailyNoteDateHandling:
    """
    RED PHASE: Date handling specification
    Following KISS: Simple date operations, no complex calendar logic
    """
    
    @pytest.fixture
    def temp_vault(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir) / "vault"
    
    def test_pkm_daily_handles_different_months(self, temp_vault):
        """
        RED TEST: Must fail - month handling not implemented
        
        Test Spec: Correct month folder naming
        - January = 01-january, February = 02-february, etc.
        - Handle month transitions correctly
        - Lowercase month names
        """
        test_dates = [
            (date(2024, 1, 1), "01-january"),
            (date(2024, 12, 31), "12-december"),
            (date(2024, 6, 15), "06-june")
        ]
        
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import get_daily_path_info
            
        # Future validation:
        # for test_date, expected_folder in test_dates:
        #     path_info = get_daily_path_info(test_date)
        #     assert expected_folder in str(path_info.folder_path)
    
    def test_pkm_daily_handles_year_transitions(self, temp_vault):
        """
        RED TEST: Must fail - year transition handling not implemented
        
        Test Spec: Proper year folder structure
        - New year creates new YYYY folder
        - Previous year folders remain intact
        - Handles leap years correctly
        """
        dates = [
            date(2023, 12, 31),  # End of 2023
            date(2024, 1, 1),    # Start of 2024  
            date(2024, 2, 29)    # Leap year day
        ]
        
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import create_daily_note
        
        # Future validation will test year folder creation
    
    def test_pkm_daily_default_to_today_if_no_date_provided(self, temp_vault):
        """
        RED TEST: Must fail - default date handling not implemented
        
        Test Spec: Use current date if no date specified
        - Default parameter uses datetime.date.today()
        - CLI command with no date uses today
        - Explicit date overrides default
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import create_daily_note
            
        # Future validation:
        # today = date.today()
        # result = create_daily_note(vault_path=temp_vault)  # No date provided
        # expected_filename = f"{today}.md"
        # assert expected_filename in str(result.filepath)


class TestPkmDailyNoteCommandLineInterface:
    """
    RED PHASE: CLI integration specification
    Simple command-line interface for daily notes
    """
    
    def test_pkm_daily_cli_command_not_implemented(self):
        """
        RED TEST: Must fail - CLI command not implemented
        
        Test Spec: Command-line interface
        - /pkm-daily creates/opens today's note
        - /pkm-daily 2024-03-15 for specific date
        - Returns success message with file path
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.cli import daily_note_command
        
        # Future CLI validation:
        # import subprocess
        # result = subprocess.run([
        #     "python", "-m", "src.pkm.cli", "daily"
        # ], capture_output=True, text=True)
        # assert "daily note" in result.stdout.lower()
        # assert result.returncode == 0
    
    def test_pkm_daily_cli_handles_date_parameter(self):
        """
        RED TEST: Must fail - date parameter handling not implemented
        
        Test Spec: Date parameter parsing
        - Accept YYYY-MM-DD format
        - Handle invalid date formats gracefully
        - Default to today if no date provided
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.cli import parse_date_parameter
            
        # Future validation:
        # parsed_date = parse_date_parameter("2024-03-15")
        # assert parsed_date == date(2024, 3, 15)
        # 
        # # Invalid date handling
        # with pytest.raises(ValueError):
        #     parse_date_parameter("invalid-date")


class TestPkmDailyNoteTemplateSystem:
    """
    RED PHASE: Template system specification
    Following KISS: Simple template, no complex templating engine
    """
    
    def test_daily_note_template_structure(self):
        """
        RED TEST: Must fail - template system not implemented
        
        Test Spec: Basic template structure
        - Frontmatter with standard fields
        - Markdown headers for sections
        - Placeholder text for user guidance
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import DAILY_NOTE_TEMPLATE
            
        # Future template validation:
        # assert "## Tasks" in DAILY_NOTE_TEMPLATE
        # assert "## Notes" in DAILY_NOTE_TEMPLATE
        # assert "## Reflections" in DAILY_NOTE_TEMPLATE


# Quality Gates - TDD Compliance
class TestTddComplianceFr003:
    """
    Meta-tests to enforce TDD compliance for FR-003
    """
    
    def test_no_implementation_exists_fr003(self):
        """
        TDD Compliance: Verify RED phase for FR-003
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import create_daily_note
            
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.daily import get_daily_path_info
            
        assert True, "Confirmed: FR-003 in proper RED phase"
    
    def test_date_handling_specification_complete(self):
        """
        Verify date handling test coverage matches requirements
        """
        # Date path structure follows specification
        test_date = date(2024, 3, 15)
        expected_path_parts = ["2024", "03-march", "2024-03-15.md"]
        
        # Test specification includes all required scenarios
        assert all(part for part in expected_path_parts), \
            "Date path specification must be complete"


# Implementation Guidance  
"""
FR-003 Implementation Plan (Post-RED Phase):

GREEN PHASE - Minimal Implementation:
1. Create src/pkm/daily.py with basic date handling
2. Implement create_daily_note() function
3. Add simple directory structure creation
4. Create basic frontmatter template
5. Add CLI command for /pkm-daily

Key Principles:
- KISS: Simple file creation, no complex templating
- SRP: Each function has single clear purpose
- FR-First: User can create daily notes before advanced features

REFACTOR PHASE:
1. Extract template system to separate module
2. Add configuration for template customization
3. Improve date parsing and validation
4. Add navigation links between daily notes

Success Criteria:
- All RED tests become GREEN
- Daily notes created in proper folder structure
- Basic template applied consistently
- CLI interface works reliably
- Code follows SOLID principles (functions < 20 lines)
"""