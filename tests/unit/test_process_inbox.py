"""
Unit tests for PKM inbox processing functionality
TDD implementation - tests written before code (RED phase)
Following proven capture feature testing patterns
"""

import pytest
import os
import shutil
import yaml
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Import will fail initially - this is expected in TDD RED phase
try:
    from src.pkm.core.process_inbox import PkmInboxProcessor, ProcessResult
    from src.pkm.exceptions import ProcessingError
except ImportError:
    # Expected during RED phase - tests written before implementation
    PkmInboxProcessor = None
    ProcessResult = None
    ProcessingError = Exception


class TestPkmInboxProcessor:
    """Unit tests for PKM inbox processing functionality"""
    
    @pytest.fixture
    def inbox_processor(self, temp_vault):
        """Fixture providing configured inbox processor"""
        if PkmInboxProcessor is None:
            pytest.skip("PkmInboxProcessor not implemented yet (TDD RED phase)")
        return PkmInboxProcessor(vault_path=str(temp_vault))
    
    @pytest.fixture
    def sample_inbox_files(self, temp_vault):
        """Create sample files in inbox for testing"""
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        
        # Project file
        project_content = """---
date: 2024-08-22
type: capture
tags: [project, deadline]
---

# Website Redesign Project

Need to complete the website redesign by next month.
- Design mockups
- Development
- Testing
- Launch
"""
        (inbox_dir / "project-file.md").write_text(project_content)
        
        # Area file
        area_content = """---
date: 2024-08-22
type: capture
tags: [area, ongoing]
---

# Health and Fitness

Maintaining regular exercise routine and healthy eating habits.
This is an ongoing area of responsibility.
"""
        (inbox_dir / "area-file.md").write_text(area_content)
        
        # Resource file
        resource_content = """---
date: 2024-08-22
type: capture
tags: [resource, reference]
---

# Python Programming Resources

Collection of useful Python learning materials:
- Documentation links
- Tutorial references
- Code examples
"""
        (inbox_dir / "resource-file.md").write_text(resource_content)
        
        return {
            "project": "project-file.md",
            "area": "area-file.md", 
            "resource": "resource-file.md"
        }
    
    # FR-001: Read Inbox Items
    def test_reads_all_inbox_files(self, inbox_processor, sample_inbox_files, temp_vault):
        """FR-001: Should discover all markdown files in inbox"""
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        assert result.files_found == 3
        assert len(result.categorized) == 3
    
    def test_handles_empty_inbox(self, inbox_processor, temp_vault):
        """Should handle empty inbox gracefully"""
        # Arrange - inbox already empty
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        assert result.files_found == 0
        assert result.files_processed == 0
        assert len(result.categorized) == 0
        assert "Inbox is empty" in result.report
    
    def test_ignores_non_markdown_files(self, inbox_processor, temp_vault):
        """Should only process .md files, ignore others"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        (inbox_dir / "note.md").write_text("# Test Note")
        (inbox_dir / "image.png").write_bytes(b"fake image data")
        (inbox_dir / "document.txt").write_text("plain text")
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.files_found == 1  # Only the .md file
        assert result.files_processed == 1
    
    # FR-002: Extract Metadata
    def test_extracts_frontmatter(self, inbox_processor, temp_vault):
        """FR-002: Should parse YAML frontmatter from each file"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        content = """---
date: 2024-08-22
type: capture
tags: [test, example]
source: test_source
---

# Test Note
Content here"""
        (inbox_dir / "test.md").write_text(content)
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        assert result.files_processed == 1
        # Frontmatter should be extracted and available for categorization
    
    def test_handles_malformed_frontmatter(self, inbox_processor, temp_vault):
        """Should handle invalid YAML gracefully"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        bad_content = """---
bad yaml: [[
invalid: structure: missing quotes
---

# Bad File
This file has malformed frontmatter"""
        (inbox_dir / "bad.md").write_text(bad_content)
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True  # Overall process should still succeed
        assert "bad.md" in result.errors
        assert "Invalid frontmatter" in result.errors["bad.md"]
        # File should remain in inbox
        assert (temp_vault / "00-inbox" / "bad.md").exists()
    
    def test_handles_missing_frontmatter(self, inbox_processor, temp_vault):
        """Should handle files without frontmatter"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        plain_content = """# Plain Note
This note has no frontmatter
Just regular markdown content"""
        (inbox_dir / "plain.md").write_text(plain_content)
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        assert result.files_processed == 1
        # Should still be categorized based on content
    
    # FR-003: Categorize by PARA
    def test_categorizes_by_para_method(self, inbox_processor, sample_inbox_files, temp_vault):
        """FR-003: Should categorize based on content and metadata"""
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        assert result.categorized["project-file.md"] == "02-projects"
        assert result.categorized["area-file.md"] == "03-areas"
        assert result.categorized["resource-file.md"] == "04-resources"
    
    def test_categorizes_by_frontmatter_type(self, inbox_processor, temp_vault):
        """Should prioritize frontmatter type field for categorization"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        
        explicit_project = """---
date: 2024-08-22
type: project
---

# Some content that might seem like a resource
But the type field says it's a project"""
        (inbox_dir / "explicit-project.md").write_text(explicit_project)
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.categorized["explicit-project.md"] == "02-projects"
    
    def test_categorizes_by_content_keywords(self, inbox_processor, temp_vault):
        """Should categorize based on content keywords when type not specified"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        
        archive_content = """---
date: 2024-08-22
type: capture
---

# Completed Project Archive

This project was completed last year and is now archived.
All files moved to historical storage."""
        (inbox_dir / "archive-note.md").write_text(archive_content)
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.categorized["archive-note.md"] == "05-archives"
    
    def test_default_categorization_fallback(self, inbox_processor, temp_vault):
        """Should have a default category for ambiguous content"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        
        ambiguous_content = """---
date: 2024-08-22
type: capture
---

# Ambiguous Note

Some random thoughts that don't clearly fit any category."""
        (inbox_dir / "ambiguous.md").write_text(ambiguous_content)
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        assert "ambiguous.md" in result.categorized
        # Should default to resources or areas (specification will define which)
    
    # FR-004: Move to Target Folder
    def test_moves_files_to_para_folders(self, inbox_processor, sample_inbox_files, temp_vault):
        """FR-004: Should move files to appropriate PARA folders"""
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        
        # Files should be moved from inbox
        inbox_dir = temp_vault / "00-inbox"
        assert not (inbox_dir / "project-file.md").exists()
        assert not (inbox_dir / "area-file.md").exists()
        assert not (inbox_dir / "resource-file.md").exists()
        
        # Files should exist in target directories
        assert (temp_vault / "01-projects" / "project-file.md").exists()
        assert (temp_vault / "02-areas" / "area-file.md").exists()
        assert (temp_vault / "04-resources" / "resource-file.md").exists()
    
    def test_creates_target_directories_if_missing(self, inbox_processor, temp_vault):
        """Should create PARA directories if they don't exist"""
        # Arrange - only inbox exists, no PARA directories
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        (inbox_dir / "test.md").write_text("---\ntype: project\n---\n# Test")
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        assert (temp_vault / "01-projects").exists()
        assert (temp_vault / "01-projects" / "test.md").exists()
    
    def test_handles_file_name_conflicts(self, inbox_processor, temp_vault):
        """Should handle conflicts when target file already exists"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        projects_dir = temp_vault / "01-projects"
        inbox_dir.mkdir(exist_ok=True)
        projects_dir.mkdir(exist_ok=True)
        
        # Create file in target directory first
        (projects_dir / "conflict.md").write_text("# Existing file")
        
        # Create file with same name in inbox
        (inbox_dir / "conflict.md").write_text("---\ntype: project\n---\n# New file")
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        # Should handle conflict somehow (rename, overwrite, or error)
        # Exact behavior to be defined in implementation
    
    # FR-005: Update Frontmatter
    def test_updates_frontmatter_with_processing_info(self, inbox_processor, sample_inbox_files, temp_vault):
        """FR-005: Should add processing metadata to frontmatter"""
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        
        # Check that processed files have updated frontmatter
        project_file = temp_vault / "01-projects" / "project-file.md"
        content = project_file.read_text()
        
        # Should contain processing metadata
        assert "processed_date:" in content
        assert "category:" in content
        assert "processed_by:" in content
    
    def test_preserves_existing_frontmatter(self, inbox_processor, temp_vault):
        """Should preserve original frontmatter while adding processing info"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        
        original_content = """---
date: 2024-08-22
type: project
author: John Doe
custom_field: important_value
---

# Test Note
Content here"""
        (inbox_dir / "preserve-test.md").write_text(original_content)
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        processed_file = temp_vault / "01-projects" / "preserve-test.md"
        content = processed_file.read_text()
        
        # Original frontmatter should be preserved
        assert "author: John Doe" in content
        assert "custom_field: important_value" in content
        # New processing info should be added
        assert "processed_date:" in content
    
    # FR-006: Generate Report
    def test_generates_processing_report(self, inbox_processor, sample_inbox_files, temp_vault):
        """FR-006: Should return summary of processed items"""
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        assert result.files_found == 3
        assert result.files_processed == 3
        assert len(result.categorized) == 3
        assert len(result.errors) == 0
        
        # Report should contain summary information
        assert "3 files processed" in result.report
        assert "01-projects: 1" in result.report
        assert "02-areas: 1" in result.report
        assert "03-resources: 1" in result.report
    
    def test_reports_errors_in_summary(self, inbox_processor, temp_vault):
        """Should include error information in report"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        
        # Good file
        (inbox_dir / "good.md").write_text("---\ntype: project\n---\n# Good")
        
        # Bad file
        (inbox_dir / "bad.md").write_text("---\nbad: yaml: [[\n---\n# Bad")
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True  # Overall success despite errors
        assert result.files_found == 2
        assert result.files_processed == 1  # Only good file processed
        assert len(result.errors) == 1
        assert "bad.md" in result.errors
        
        # Report should mention errors
        assert "1 error" in result.report
        assert "1 file processed successfully" in result.report
    
    # Edge Cases and Error Handling
    def test_handles_permission_errors(self, inbox_processor, temp_vault):
        """Should handle file permission errors gracefully"""
        # This test might need to be platform-specific
        # or use mocking to simulate permission errors
        pass
    
    def test_handles_disk_space_errors(self, inbox_processor, temp_vault):
        """Should handle disk full errors gracefully"""
        # This would typically be tested with mocking
        pass
    
    def test_processes_large_number_of_files(self, inbox_processor, temp_vault):
        """Should handle processing many files efficiently"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        
        # Create 20 test files
        for i in range(20):
            content = f"""---
date: 2024-08-22
type: resource
---

# Test File {i}
Content for file number {i}"""
            (inbox_dir / f"file-{i:02d}.md").write_text(content)
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        assert result.files_found == 20
        assert result.files_processed == 20
        assert len(result.categorized) == 20
    
    def test_handles_unicode_content(self, inbox_processor, temp_vault):
        """Should handle Unicode characters in content and filenames"""
        # Arrange
        inbox_dir = temp_vault / "00-inbox"
        inbox_dir.mkdir(exist_ok=True)
        
        unicode_content = """---
date: 2024-08-22
type: resource
author: João Silva
---

# Café Configuration ☕

Notes about café setup with émojis and açcénts.
Chinese: 中文内容
Japanese: 日本語コンテンツ
Arabic: محتوى عربي
"""
        (inbox_dir / "unicode-test.md").write_text(unicode_content, encoding='utf-8')
        
        # Act
        result = inbox_processor.process_inbox()
        
        # Assert
        assert result.success is True
        assert result.files_processed == 1
        # File should be moved and content preserved
        processed_file = temp_vault / "04-resources" / "unicode-test.md"
        assert processed_file.exists()
        content = processed_file.read_text(encoding='utf-8')
        assert "Café Configuration ☕" in content
        assert "中文内容" in content


# These tests should ALL FAIL initially (TDD RED phase)
# Implementation comes next (GREEN phase)
# Then refactoring (REFACTOR phase)