"""
TDD Tests for FR-001: Basic PKM Capture Command - FUNCTIONAL TESTS

GREEN PHASE - These tests validate the actual implementation functionality.
These replace the RED phase import-error tests with real functional validation.

Test Specification:
- Given: User has content to capture
- When: User runs `/pkm-capture "content"`
- Then: Content saved to vault/00-inbox/ with timestamp
- And: Basic frontmatter added with capture metadata

Engineering Principles:
- TDD GREEN: Tests validate actual working functionality
- KISS: Simple test cases for simple functionality
- FR-First: User-facing functionality tested before optimization
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime
import yaml
import re

# Import the actual implementation
from src.pkm.capture import pkm_capture, CaptureResult
from src.pkm.cli import capture_command


class TestPkmCaptureBasicFunctionality:
    """
    GREEN PHASE: Test actual implementation functionality
    
    These tests validate that the minimal implementation works correctly
    """
    
    @pytest.fixture
    def temp_vault(self):
        """Create temporary vault structure for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            yield vault_path
    
    def test_pkm_capture_creates_inbox_file_basic(self, temp_vault):
        """
        GREEN TEST: Test basic capture functionality works
        
        Test Spec: Basic capture functionality
        - Simple content gets captured to inbox
        - File created with proper timestamp name
        """
        # Test the actual implementation
        result = pkm_capture("Test content", vault_path=temp_vault)
        
        assert result.success is True
        assert result.filepath.parent.name == "00-inbox"
        assert result.filename.endswith(".md")
        assert (temp_vault / "00-inbox").exists()
        assert result.filepath.exists()
    
    def test_pkm_capture_generates_proper_filename(self, temp_vault):
        """
        GREEN TEST: Test filename generation
        
        Test Spec: Filename follows timestamp pattern
        - Format: YYYYMMDDHHMMSS.md
        - Unique per second resolution
        """
        result = pkm_capture("Test", vault_path=temp_vault)
        
        filename_pattern = r"^\d{14}\.md$"
        assert re.match(filename_pattern, result.filename)
        
        # Verify it's a valid timestamp
        timestamp_part = result.filename[:-3]  # Remove .md
        parsed_time = datetime.strptime(timestamp_part, "%Y%m%d%H%M%S")
        assert isinstance(parsed_time, datetime)
    
    def test_pkm_capture_creates_valid_frontmatter(self, temp_vault):
        """
        GREEN TEST: Test frontmatter creation
        
        Test Spec: Frontmatter contains required metadata
        - date: ISO format timestamp
        - type: "capture"
        - tags: empty list initially
        - status: "draft"
        - source: "capture_command"
        """
        result = pkm_capture("Test content", vault_path=temp_vault)
        
        frontmatter = result.frontmatter
        assert frontmatter["type"] == "capture"
        assert frontmatter["status"] == "draft"
        assert frontmatter["source"] == "capture_command"
        assert isinstance(frontmatter["tags"], list)
        assert "date" in frontmatter
        
        # Verify date is in correct format
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        assert re.match(date_pattern, frontmatter["date"])
    
    def test_pkm_capture_creates_readable_markdown_file(self, temp_vault):
        """
        GREEN TEST: Test file creation and format
        
        Test Spec: Created file is valid markdown with frontmatter
        - YAML frontmatter at top
        - Markdown content after frontmatter
        - File readable as text
        """
        test_content = "# Test Header\nTest content"
        result = pkm_capture(test_content, vault_path=temp_vault)
        
        file_content = result.filepath.read_text()
        
        # Check structure
        assert file_content.startswith("---")
        assert "# Test Header" in file_content
        
        # Verify YAML frontmatter is valid
        parts = file_content.split("---")
        assert len(parts) >= 3  # Should have opening ---, frontmatter, closing ---, content
        
        frontmatter_yaml = parts[1].strip()
        parsed_frontmatter = yaml.safe_load(frontmatter_yaml)
        assert parsed_frontmatter["type"] == "capture"


class TestPkmCaptureErrorHandling:
    """
    GREEN PHASE: Test error handling functionality
    
    Following KISS: Simple error cases handled gracefully
    """
    
    @pytest.fixture
    def temp_vault(self):
        """Create temporary vault for error testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            yield vault_path
    
    def test_pkm_capture_handles_missing_inbox_directory(self, temp_vault):
        """
        GREEN TEST: Test missing inbox handling
        
        Test Spec: Gracefully handle missing inbox
        - Create inbox directory if missing
        - Return success with directory creation note
        """
        # Verify inbox doesn't exist initially
        inbox_path = temp_vault / "00-inbox"
        assert not inbox_path.exists()
        
        result = pkm_capture("Test", vault_path=temp_vault)
        
        # Should succeed and create the directory
        assert result.success is True
        assert inbox_path.exists()
        assert result.filepath.parent == inbox_path
    
    def test_pkm_capture_handles_empty_content(self, temp_vault):
        """
        GREEN TEST: Test empty content handling
        
        Test Spec: Handle empty content gracefully
        - Empty string creates note with placeholder
        - None content returns error
        """
        # Test empty string
        result_empty = pkm_capture("", vault_path=temp_vault)
        assert result_empty.success is True
        content = result_empty.filepath.read_text()
        assert "Empty capture" in content  # Should have placeholder
        
        # Test None content
        result_none = pkm_capture(None, vault_path=temp_vault)
        assert result_none.success is False
        assert "content cannot be none" in result_none.error.lower()


class TestPkmCaptureIntegration:
    """
    GREEN PHASE: Integration tests for command-line interface
    """
    
    @pytest.fixture
    def temp_vault(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            yield vault_path
    
    def test_pkm_capture_command_function(self, temp_vault):
        """
        GREEN TEST: Test CLI command function
        
        Test Spec: Command function integration
        - capture_command works correctly
        - Returns boolean success
        """
        success = capture_command("Test content with spaces", vault_path=temp_vault)
        assert success is True
        
        # Verify file was created
        inbox_path = temp_vault / "00-inbox"
        assert inbox_path.exists()
        
        files = list(inbox_path.glob("*.md"))
        assert len(files) == 1
        
        content = files[0].read_text()
        assert "Test content with spaces" in content


class TestTddCompliance:
    """
    TDD Compliance tests - verify we've successfully transitioned from RED to GREEN
    """
    
    def test_implementation_now_exists_fr001(self):
        """
        TDD Compliance Test: Verify we're now in GREEN phase
        
        This test confirms implementation exists and imports work
        """
        # These should work now (GREEN phase)
        from src.pkm.capture import pkm_capture
        from src.pkm.cli import capture_command
        
        # Test that functions are callable
        assert callable(pkm_capture)
        assert callable(capture_command)
        
        # Verify return types match specification
        temp_result = pkm_capture("")
        assert isinstance(temp_result, CaptureResult)
        assert hasattr(temp_result, 'success')
        assert hasattr(temp_result, 'filepath')
    
    def test_specification_compliance(self):
        """
        Verify implementation meets FR-001 acceptance criteria
        """
        # Test with minimal content to avoid file creation
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            result = pkm_capture("test", vault_path=vault_path)
            
            # FR-001 acceptance criteria validation
            assert result.success is True  # Content saved successfully
            assert result.filepath.parent.name == "00-inbox"  # Saved to inbox
            assert result.filename.endswith(".md")  # Proper filename
            assert result.frontmatter["type"] == "capture"  # Basic frontmatter
    
    def test_kiss_principle_compliance(self):
        """
        Verify implementation follows KISS principle
        """
        # Read the implementation to check line counts
        from pathlib import Path
        import inspect
        
        # Get the source file
        capture_module_path = Path("src/pkm/capture.py")
        if capture_module_path.exists():
            # Count lines in main function
            from src.pkm.capture import pkm_capture
            source_lines = inspect.getsource(pkm_capture).split('\n')
            # Remove empty lines and comments for actual code count
            code_lines = [line for line in source_lines 
                         if line.strip() and not line.strip().startswith('#')]
            
            # KISS compliance: function should be reasonably simple
            assert len(code_lines) < 50, f"Function too complex: {len(code_lines)} lines"


# Performance validation (basic)
class TestPkmCapturePerformance:
    """
    Basic performance validation - not optimization, just basic requirements
    """
    
    def test_capture_performance_reasonable(self):
        """
        GREEN TEST: Verify basic performance is reasonable
        
        This is NOT optimization (which would violate FR-First)
        Just ensuring basic functionality isn't pathologically slow
        """
        import time
        
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            
            start_time = time.time()
            result = pkm_capture("Performance test content", vault_path=vault_path)
            end_time = time.time()
            
            # Basic sanity check - should complete in reasonable time
            assert result.success is True
            assert (end_time - start_time) < 2.0  # Should be fast enough for user interaction


# Integration with existing vault structure
class TestPkmCaptureVaultIntegration:
    """
    Test integration with existing vault structures
    """
    
    def test_captures_to_existing_vault_structure(self):
        """
        GREEN TEST: Integration with existing vault
        
        Test Spec: Works with existing vault structure
        - Doesn't overwrite existing files
        - Respects existing directory structure
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            
            # Create existing structure
            (vault_path / "01-projects").mkdir(parents=True)
            (vault_path / "02-areas").mkdir(parents=True)
            existing_file = vault_path / "01-projects" / "existing.md"
            existing_file.write_text("Existing content")
            
            # Capture should not affect existing structure
            result = pkm_capture("New capture", vault_path=vault_path)
            
            assert result.success is True
            assert existing_file.read_text() == "Existing content"  # Unchanged
            assert result.filepath.parent.name == "00-inbox"  # New file in inbox
            assert result.filepath != existing_file  # Different file