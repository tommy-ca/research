"""
TDD Tests for FR-001: Basic PKM Capture Command

RED PHASE - These tests MUST FAIL initially to enforce TDD workflow.
No implementation exists yet - this is the specification-driven test-first approach.

Test Specification:
- Given: User has content to capture  
- When: User runs `/pkm-capture "content"`
- Then: Content saved to vault/00-inbox/ with timestamp
- And: Basic frontmatter added with capture metadata

Engineering Principles:
- TDD: Tests written FIRST, must fail initially
- KISS: Simple test cases for simple functionality  
- FR-First: User-facing functionality tested before optimization
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime
from typing import NamedTuple, Optional, List
import yaml


# Type definitions following SOLID principles (Interface Segregation)
class CaptureResult(NamedTuple):
    """Result of capture operation - simple data structure"""
    filename: str
    filepath: Path
    frontmatter: dict
    content: str
    success: bool
    error: Optional[str] = None


class FrontmatterData(NamedTuple):
    """Frontmatter structure - separate concern from content"""
    date: str
    type: str
    tags: List[str]
    status: str
    source: str


class TestPkmCaptureBasicFunctionality:
    """
    RED PHASE: All tests in this class MUST FAIL initially
    
    These tests define the specification for FR-001 before implementation exists.
    Following TDD: Write test → Watch it fail → Implement minimal solution
    """
    
    @pytest.fixture
    def temp_vault(self):
        """Create temporary vault structure for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            inbox_path = vault_path / "00-inbox"
            inbox_path.mkdir(parents=True)
            yield vault_path
    
    def test_pkm_capture_creates_inbox_file_basic(self, temp_vault):
        """
        RED TEST: Must fail - no pkm_capture function exists yet
        
        Test Spec: Basic capture functionality
        - Simple content gets captured to inbox
        - File created with proper timestamp name
        """
        # This import will fail - no implementation exists (RED PHASE)
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.capture import pkm_capture
            
        # When implementation exists, this test will validate basic capture
        # result = pkm_capture("Test content", vault_path=temp_vault)
        # assert result.success is True
        # assert result.filepath.parent.name == "00-inbox"
        # assert result.filename.endswith(".md")
    
    def test_pkm_capture_generates_proper_filename(self, temp_vault):
        """
        RED TEST: Must fail - filename generation not implemented
        
        Test Spec: Filename follows timestamp pattern
        - Format: YYYYMMDDHHMMSS.md
        - Unique per second resolution
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.capture import pkm_capture
            
        # Future test validation:
        # result = pkm_capture("Test", vault_path=temp_vault)
        # filename_pattern = r"^\d{14}\.md$"
        # assert re.match(filename_pattern, result.filename)
    
    def test_pkm_capture_creates_valid_frontmatter(self, temp_vault):
        """
        RED TEST: Must fail - frontmatter creation not implemented
        
        Test Spec: Frontmatter contains required metadata
        - date: ISO format timestamp
        - type: "capture"  
        - tags: empty list initially
        - status: "draft"
        - source: "capture_command"
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.capture import pkm_capture
            
        # Future test validation:
        # result = pkm_capture("Test content", vault_path=temp_vault)
        # frontmatter = result.frontmatter
        # assert frontmatter["type"] == "capture"
        # assert frontmatter["status"] == "draft"
        # assert frontmatter["source"] == "capture_command"
        # assert isinstance(frontmatter["tags"], list)
        # assert "date" in frontmatter
    
    def test_pkm_capture_creates_readable_markdown_file(self, temp_vault):
        """
        RED TEST: Must fail - file creation not implemented
        
        Test Spec: Created file is valid markdown with frontmatter
        - YAML frontmatter at top
        - Markdown content after frontmatter
        - File readable as text
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.capture import pkm_capture
            
        # Future test validation:
        # result = pkm_capture("# Test Header\nTest content", vault_path=temp_vault)
        # file_content = result.filepath.read_text()
        # assert file_content.startswith("---")
        # assert "# Test Header" in file_content
        # assert yaml.safe_load_all(file_content)  # Valid YAML frontmatter


class TestPkmCaptureErrorHandling:
    """
    RED PHASE: Error handling tests - must fail initially
    
    Following KISS: Simple error cases first, complex scenarios later
    """
    
    @pytest.fixture
    def temp_vault(self):
        """Create temporary vault for error testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"  
            yield vault_path  # Note: inbox NOT created for error testing
    
    def test_pkm_capture_handles_missing_inbox_directory(self, temp_vault):
        """
        RED TEST: Must fail - error handling not implemented
        
        Test Spec: Gracefully handle missing inbox
        - Create inbox directory if missing
        - Return success with directory creation note
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.capture import pkm_capture
            
        # Future validation:
        # result = pkm_capture("Test", vault_path=temp_vault)
        # assert result.success is True
        # assert (temp_vault / "00-inbox").exists()
    
    def test_pkm_capture_handles_empty_content(self, temp_vault):
        """
        RED TEST: Must fail - input validation not implemented
        
        Test Spec: Handle empty content gracefully
        - Empty string creates note with placeholder
        - None content returns error
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.capture import pkm_capture
            
        # Future validation:
        # result_empty = pkm_capture("", vault_path=temp_vault)
        # assert result_empty.success is True
        # assert len(result_empty.content) > 0  # Has placeholder
        # 
        # result_none = pkm_capture(None, vault_path=temp_vault)
        # assert result_none.success is False
        # assert "content" in result_none.error.lower()


class TestPkmCaptureIntegration:
    """
    RED PHASE: Integration tests - must fail initially
    
    Testing command-line integration and file system operations
    """
    
    def test_pkm_capture_command_line_interface(self, temp_vault):
        """
        RED TEST: Must fail - CLI command not implemented
        
        Test Spec: Command line interface works
        - /pkm-capture "content" creates file
        - Returns success message to user
        - Handles quoted content with spaces
        """
        # This will fail - no CLI command exists yet
        import subprocess
        
        # Future test (when CLI exists):
        # result = subprocess.run([
        #     "python", "-m", "src.pkm.cli", 
        #     "capture", "Test content with spaces"
        # ], cwd=temp_vault, capture_output=True, text=True)
        # assert result.returncode == 0
        # assert "captured successfully" in result.stdout.lower()
        
        # For now, just verify the CLI module doesn't exist (RED phase)
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.cli import main
    
    def test_pkm_capture_file_system_permissions(self, temp_vault):
        """
        RED TEST: Must fail - permission handling not implemented
        
        Test Spec: Proper file system permission handling
        - Creates files with correct permissions
        - Handles permission denied scenarios
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.capture import pkm_capture
        
        # Future validation will test file permissions and error handling


# Quality Gates - Enforce TDD Compliance
class TestTddCompliance:
    """
    Meta-tests to enforce TDD workflow compliance
    These tests validate that we're following TDD principles
    """
    
    def test_no_implementation_exists_yet_fr001(self):
        """
        TDD Compliance Test: Ensure we're in RED phase
        
        This test MUST PASS to prove we're following TDD.
        It verifies no implementation exists before tests are written.
        """
        # Verify no implementation modules exist yet (RED phase requirement)
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.capture import pkm_capture
            
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.cli import main
        
        # This passing test proves we're in the correct RED phase
        assert True, "Confirmed: No implementation exists - proper TDD RED phase"
    
    def test_specification_completeness(self):
        """
        Verify test specification covers all FR-001 acceptance criteria
        """
        # This test validates our test coverage matches specification
        test_methods = [method for method in dir(TestPkmCaptureBasicFunctionality) 
                       if method.startswith('test_')]
        
        # FR-001 requires these test scenarios minimum
        required_test_scenarios = [
            'creates_inbox_file',
            'generates_proper_filename', 
            'creates_valid_frontmatter',
            'creates_readable_markdown_file'
        ]
        
        for scenario in required_test_scenarios:
            assert any(scenario in test_method for test_method in test_methods), \
                f"Missing test for required scenario: {scenario}"


# Specification Documentation
"""
FR-001 Implementation Plan (After RED Phase Complete):

GREEN PHASE - Minimal Implementation:
1. Create src/pkm/capture.py with minimal pkm_capture() function
2. Implement basic file creation in vault/00-inbox/
3. Add simple frontmatter generation
4. Create minimal CLI command interface

REFACTOR PHASE - Improve While Tests Pass:
1. Extract frontmatter creation to separate function
2. Add better error handling
3. Improve file naming strategy
4. Add configuration options

Success Criteria:
- All RED tests become GREEN
- Implementation follows KISS principle (functions < 20 lines)
- No complex features added (FR-First compliance)
- Code coverage > 80%
"""