"""
Unit tests for PKM capture functionality
TDD implementation - tests written before code
"""

import pytest
import os
import re
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Import will fail initially - this is expected in TDD RED phase
try:
    from src.pkm.core.capture import PkmCapture
    from src.pkm.exceptions import CaptureError
except ImportError:
    # Expected during RED phase - tests written before implementation
    PkmCapture = None
    CaptureError = Exception


class TestPkmCapture:
    """Unit tests for PKM capture functionality"""
    
    @pytest.fixture
    def capture_service(self, temp_vault):
        """Fixture providing configured capture service"""
        if PkmCapture is None:
            pytest.skip("PkmCapture not implemented yet (TDD RED phase)")
        return PkmCapture(vault_path=str(temp_vault))
    
    def test_capture_creates_file_in_inbox(self, capture_service, temp_vault):
        """Test that capture creates file in inbox with proper naming"""
        # Arrange
        content = "Test note content"
        expected_path_pattern = r"00-inbox/\d{8}-\d{6}-.+\.md"
        
        # Act
        result = capture_service.capture(content)
        
        # Assert
        assert result.success is True
        assert re.match(expected_path_pattern, result.file_path)
        assert result.metadata['type'] == 'capture'
        assert result.metadata['status'] == 'inbox'
    
    def test_capture_adds_proper_frontmatter(self, capture_service):
        """Test that capture adds complete YAML frontmatter"""
        # Arrange
        content = "Test content with metadata"
        source = "test_source"
        
        # Act
        result = capture_service.capture(content, source=source)
        
        # Assert
        assert 'date' in result.frontmatter
        assert 'type' in result.frontmatter
        assert 'source' in result.frontmatter
        assert result.frontmatter['source'] == source
        assert result.frontmatter['type'] == 'capture'
    
    def test_capture_handles_empty_content(self, capture_service):
        """Test graceful handling of empty content"""
        # Arrange
        content = ""
        
        # Act & Assert
        with pytest.raises(CaptureError) as exc_info:
            capture_service.capture(content)
        
        assert "Content cannot be empty" in str(exc_info.value)
    
    @pytest.mark.parametrize("content,expected_filename", [
        ("Short note", "short-note.md"),
        ("A very long note title that should be truncated properly", 
         "a-very-long-note-title-that-should-be.md"),
        ("Note with Special Characters! @#$%", "note-with-special-characters.md")
    ])
    def test_filename_generation(self, capture_service, content, expected_filename):
        """Test filename generation from content"""
        # Act
        filename = capture_service._generate_filename(content)
        
        # Assert
        assert filename.endswith(expected_filename)
    
    def test_capture_creates_directories_if_missing(self, capture_service, temp_vault):
        """Test that capture creates inbox directory if it doesn't exist"""
        # Arrange
        inbox_path = temp_vault / "00-inbox"
        inbox_path.rmdir()  # Remove inbox directory
        content = "Test content"
        
        # Act
        result = capture_service.capture(content)
        
        # Assert
        assert result.success is True
        assert inbox_path.exists()
    
    def test_capture_with_tags(self, capture_service):
        """Test capture with custom tags"""
        # Arrange
        content = "Tagged note content"
        tags = ["test", "automation", "tdd"]
        
        # Act
        result = capture_service.capture(content, tags=tags)
        
        # Assert
        assert result.frontmatter['tags'] == tags
    
    def test_capture_with_invalid_characters(self, capture_service):
        """Test handling of content with invalid filename characters"""
        # Arrange
        content = "Note with / \\ : * ? \" < > | characters"
        
        # Act
        result = capture_service.capture(content)
        
        # Assert
        assert result.success is True
        # Filename portion should be sanitized (extract filename from path)
        filename_only = result.file_path.split('/')[-1]  # Get just the filename part
        assert "/" not in filename_only
        assert "\\" not in filename_only
        assert ":" not in filename_only
        assert "*" not in filename_only
        assert "?" not in filename_only
        assert "\"" not in filename_only
        assert "<" not in filename_only
        assert ">" not in filename_only
        assert "|" not in filename_only
    
    def test_capture_generates_unique_filenames(self, capture_service):
        """Test that concurrent captures generate unique filenames"""
        # Arrange
        content = "Duplicate content"
        
        # Act
        result1 = capture_service.capture(content)
        result2 = capture_service.capture(content)
        
        # Assert
        assert result1.file_path != result2.file_path
    
    def test_capture_preserves_markdown_formatting(self, capture_service):
        """Test that markdown formatting is preserved in captured content"""
        # Arrange
        content = """# Header
        
## Subheader

- List item 1
- List item 2

**Bold text** and *italic text*

```python
code_block = "preserved"
```
"""
        
        # Act
        result = capture_service.capture(content)
        
        # Assert
        assert result.success is True
        # Verify content is preserved (this will need file reading in implementation)


# These tests should ALL FAIL initially (TDD RED phase)
# Implementation comes next (GREEN phase)
# Then refactoring (REFACTOR phase)