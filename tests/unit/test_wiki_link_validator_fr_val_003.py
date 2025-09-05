"""
PKM Validation System - Wiki-Link Validator Tests
FR-VAL-003: Wiki-Link Validation Implementation Tests

TDD RED Phase: Comprehensive test suite defining expected behavior
All tests written BEFORE implementation - they should FAIL initially

Following TDD methodology:
1. RED: Write failing test first (THIS FILE)
2. GREEN: Write minimal code to pass
3. REFACTOR: Improve code while tests pass
"""

import pytest
from pathlib import Path
from typing import List, Set
import tempfile
import os
from unittest.mock import Mock, patch

# Import will fail initially - this is expected in RED phase
try:
    from src.pkm.validators.wiki_link_validator import (
        WikiLinkValidator,
        WikiLinkExtractor,
        VaultFileResolver,
        WikiLinkValidationRules
    )
    from src.pkm.validators.base import ValidationResult
except ImportError:
    # Expected during RED phase - classes don't exist yet
    WikiLinkValidator = None
    WikiLinkExtractor = None
    VaultFileResolver = None
    WikiLinkValidationRules = None
    ValidationResult = None


class TestWikiLinkExtractor:
    """
    Task Group 1: Wiki-Link Extractor Component Tests
    Tests for extracting wiki-style links from markdown content
    """
    
    def test_basic_wiki_link_extraction(self):
        """Task 1.1: Basic wiki-link pattern extraction"""
        extractor = WikiLinkExtractor()
        content = "Here is a [[Simple Link]] in the text."
        
        result = extractor.extract_links(content)
        
        assert result == ["Simple Link"]
        
    def test_multi_word_wiki_link_extraction(self):
        """Task 1.2: Multi-word wiki-link extraction"""
        extractor = WikiLinkExtractor()
        content = "Reference to [[Multi Word Link]] here."
        
        result = extractor.extract_links(content)
        
        assert result == ["Multi Word Link"]
        
    def test_multiple_wiki_links_extraction(self):
        """Task 1.3: Multiple wiki-links in content"""
        extractor = WikiLinkExtractor()
        content = "See [[Link One]] and also [[Link Two]] for details."
        
        result = extractor.extract_links(content)
        
        assert set(result) == {"Link One", "Link Two"}
        assert len(result) == 2
        
    def test_wiki_link_with_alias_extraction(self):
        """Task 1.4: Wiki-links with aliases - extract target only"""
        extractor = WikiLinkExtractor()
        content = "Check [[Target Note|Display Text]] for info."
        
        result = extractor.extract_links(content)
        
        # Should extract target, not display text
        assert result == ["Target Note"]
        
    def test_invalid_wiki_link_patterns_ignored(self):
        """Task 1.5: Invalid wiki-link patterns should be ignored"""
        extractor = WikiLinkExtractor()
        content = "This is [Invalid Link] and should be ignored."
        
        result = extractor.extract_links(content)
        
        assert result == []
        
    def test_nested_brackets_handling(self):
        """Task 1.6: Nested brackets inside wiki-links"""
        extractor = WikiLinkExtractor()
        content = "See [[Note with [brackets] inside]] for details."
        
        result = extractor.extract_links(content)
        
        assert result == ["Note with [brackets] inside"]
        
    def test_empty_wiki_links_ignored(self):
        """Additional test: Empty wiki-links should be ignored"""
        extractor = WikiLinkExtractor()
        content = "Empty link [[]] should be ignored."
        
        result = extractor.extract_links(content)
        
        assert result == []
        
    def test_whitespace_only_wiki_links_ignored(self):
        """Additional test: Whitespace-only links ignored"""
        extractor = WikiLinkExtractor()
        content = "Whitespace [[   ]] should be ignored."
        
        result = extractor.extract_links(content)
        
        assert result == []
        
    def test_wiki_link_case_preservation(self):
        """Additional test: Case should be preserved in extraction"""
        extractor = WikiLinkExtractor()
        content = "Link to [[CamelCase Note]] here."
        
        result = extractor.extract_links(content)
        
        assert result == ["CamelCase Note"]
        
    def test_wiki_link_special_characters(self):
        """Additional test: Special characters in wiki-links"""
        extractor = WikiLinkExtractor()
        content = "Link to [[Note-with_special.chars]] here."
        
        result = extractor.extract_links(content)
        
        assert result == ["Note-with_special.chars"]


class TestVaultFileResolver:
    """
    Task Group 2: Vault File Resolver Component Tests
    Tests for resolving wiki-link text to actual vault files
    """
    
    def setup_method(self):
        """Setup test vault structure"""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        
        # Create standard PKM vault structure
        (self.vault_path / "permanent" / "notes").mkdir(parents=True)
        (self.vault_path / "02-projects").mkdir(parents=True)
        (self.vault_path / "03-areas").mkdir(parents=True)
        (self.vault_path / "04-resources").mkdir(parents=True)
        
        # Create test files
        (self.vault_path / "permanent" / "notes" / "test-note.md").touch()
        (self.vault_path / "permanent" / "notes" / "another-note.md").touch()
        (self.vault_path / "02-projects" / "project-note.md").touch()
        
    def teardown_method(self):
        """Cleanup test vault"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_exact_filename_resolution(self):
        """Task 2.1: Exact filename resolution with case-insensitive matching"""
        resolver = VaultFileResolver(self.vault_path)
        
        result = resolver.resolve_link("Test Note")
        
        expected_path = self.vault_path / "permanent" / "notes" / "test-note.md"
        assert len(result) == 1
        assert result[0] == expected_path
        
    def test_multiple_file_format_resolution(self):
        """Task 2.2: Multiple file format resolution with priority"""
        # Create files with different extensions
        (self.vault_path / "permanent" / "notes" / "multi-format.md").touch()
        (self.vault_path / "permanent" / "notes" / "multi-format.txt").touch()
        (self.vault_path / "permanent" / "notes" / "multi-format.org").touch()
        
        resolver = VaultFileResolver(self.vault_path)
        
        result = resolver.resolve_link("Multi Format")
        
        # Should prefer .md over .txt over .org
        expected_path = self.vault_path / "permanent" / "notes" / "multi-format.md"
        assert len(result) == 1
        assert result[0] == expected_path
        
    def test_directory_traversal_resolution(self):
        """Task 2.3: Directory traversal resolution across vault subdirectories"""
        resolver = VaultFileResolver(self.vault_path)
        
        result = resolver.resolve_link("Project Note")
        
        expected_path = self.vault_path / "02-projects" / "project-note.md"
        assert len(result) == 1
        assert result[0] == expected_path
        
    def test_ambiguous_link_resolution(self):
        """Task 2.4: Ambiguous link resolution returns all matches"""
        # Create multiple files with similar names
        (self.vault_path / "permanent" / "notes" / "duplicate.md").touch()
        (self.vault_path / "02-projects" / "duplicate.md").touch()
        
        resolver = VaultFileResolver(self.vault_path)
        
        result = resolver.resolve_link("Duplicate")
        
        assert len(result) == 2
        expected_paths = {
            self.vault_path / "permanent" / "notes" / "duplicate.md",
            self.vault_path / "02-projects" / "duplicate.md"
        }
        assert set(result) == expected_paths
        
    def test_non_existent_file_detection(self):
        """Task 2.5: Non-existent file detection"""
        resolver = VaultFileResolver(self.vault_path)
        
        result = resolver.resolve_link("Non Existent Note")
        
        assert result == []
        
    def test_filename_normalization(self):
        """Test filename normalization (spaces, case, special chars)"""
        resolver = VaultFileResolver(self.vault_path)
        
        # Test that "Another Note" resolves to "another-note.md"
        result = resolver.resolve_link("Another Note")
        
        expected_path = self.vault_path / "permanent" / "notes" / "another-note.md"
        assert len(result) == 1
        assert result[0] == expected_path


class TestWikiLinkValidator:
    """
    Task Group 3: Wiki-Link Validator Integration Tests
    Tests for the complete validation workflow
    """
    
    def setup_method(self):
        """Setup test environment with mock vault"""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        (self.vault_path / "permanent" / "notes").mkdir(parents=True)
        
        # Create target notes
        (self.vault_path / "permanent" / "notes" / "existing-note.md").touch()
        
        # Create test markdown file
        self.test_file = self.vault_path / "test-file.md"
        
    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_complete_validation_workflow_valid_links(self):
        """Task 3.1: Complete validation workflow with valid links"""
        content = """---
date: 2024-01-01
type: zettel
tags: [test]
status: draft
---

# Test Note

This references [[Existing Note]] which should be valid.
"""
        self.test_file.write_text(content)
        
        validator = WikiLinkValidator(self.vault_path)
        
        results = validator.validate(self.test_file)
        
        # Should have no validation errors
        assert len(results) == 0
        
    def test_broken_link_detection(self):
        """Task 3.2: Broken link detection with error message"""
        content = """---
date: 2024-01-01
type: zettel
tags: [test]
status: draft
---

# Test Note

This references [[Non Existent Note]] which should cause error.
"""
        self.test_file.write_text(content)
        
        validator = WikiLinkValidator(self.vault_path)
        
        results = validator.validate(self.test_file)
        
        assert len(results) == 1
        assert results[0].severity == "error"
        assert results[0].rule == "broken-wiki-link"
        assert "Non Existent Note" in results[0].message
        assert "not found" in results[0].message.lower()
        
    def test_ambiguous_link_detection(self):
        """Task 3.3: Ambiguous link detection with warning"""
        # Create ambiguous files
        (self.vault_path / "permanent" / "notes" / "duplicate.md").touch()
        (self.vault_path / "02-projects").mkdir(parents=True)
        (self.vault_path / "02-projects" / "duplicate.md").touch()
        
        content = """---
date: 2024-01-01
type: zettel
tags: [test]
status: draft
---

# Test Note

This references [[Duplicate]] which is ambiguous.
"""
        self.test_file.write_text(content)
        
        validator = WikiLinkValidator(self.vault_path)
        
        results = validator.validate(self.test_file)
        
        assert len(results) == 1
        assert results[0].severity == "warning"
        assert results[0].rule == "ambiguous-wiki-link"
        assert "Duplicate" in results[0].message
        assert "multiple matches" in results[0].message.lower()
        
    def test_empty_link_validation(self):
        """Task 3.4: Empty link validation error"""
        content = """---
date: 2024-01-01
type: zettel
tags: [test]
status: draft
---

# Test Note

This has empty link [[]] which should error.
"""
        self.test_file.write_text(content)
        
        validator = WikiLinkValidator(self.vault_path)
        
        results = validator.validate(self.test_file)
        
        assert len(results) == 1
        assert results[0].severity == "error"
        assert results[0].rule == "empty-wiki-link"
        assert "empty" in results[0].message.lower()
        
    def test_duplicate_link_optimization(self):
        """Task 3.5: Duplicate link optimization - single resolution"""
        content = """---
date: 2024-01-01
type: zettel
tags: [test]
status: draft
---

# Test Note

Multiple references to [[Existing Note]] and [[Existing Note]] again.
The same [[Existing Note]] should only be resolved once for performance.
"""
        self.test_file.write_text(content)
        
        validator = WikiLinkValidator(self.vault_path)
        
        # Mock the resolver to track calls
        with patch.object(validator.resolver, 'resolve_link') as mock_resolve:
            mock_resolve.return_value = [self.vault_path / "permanent" / "notes" / "existing-note.md"]
            
            results = validator.validate(self.test_file)
            
            # Should only resolve unique links once
            assert mock_resolve.call_count == 1
            mock_resolve.assert_called_with("Existing Note")
            
        assert len(results) == 0


class TestWikiLinkValidationRules:
    """
    Tests for centralized validation rules and error messages
    Following DRY principles
    """
    
    def test_error_message_templates(self):
        """Test error message template system"""
        rules = WikiLinkValidationRules()
        
        broken_link_msg = rules.format_error_message('broken_wiki_link', link_text="Test Note")
        assert "Test Note" in broken_link_msg
        assert "not found" in broken_link_msg.lower()
        
        ambiguous_link_msg = rules.format_error_message('ambiguous_wiki_link', 
                                                        link_text="Duplicate", 
                                                        matches=["path1.md", "path2.md"])
        assert "Duplicate" in ambiguous_link_msg
        assert "multiple matches" in ambiguous_link_msg.lower()
        assert "path1.md" in ambiguous_link_msg
        assert "path2.md" in ambiguous_link_msg
        
    def test_validation_rule_constants(self):
        """Test centralized validation constants"""
        rules = WikiLinkValidationRules()
        
        # Test search paths
        assert "permanent/notes" in rules.SEARCH_PATHS
        assert "02-projects" in rules.SEARCH_PATHS
        
        # Test file extensions priority
        assert ".md" in rules.FILE_EXTENSIONS
        assert rules.FILE_EXTENSIONS.index(".md") < rules.FILE_EXTENSIONS.index(".txt")


class TestIntegrationWithValidationRunner:
    """
    Task Group 4: Integration & Testing
    Tests for integration with PKM validation system
    """
    
    def test_integration_with_pkm_validation_runner(self):
        """Task 4.1: Integration with PKMValidationRunner"""
        from src.pkm.validators.runner import PKMValidationRunner
        
        temp_dir = tempfile.mkdtemp()
        vault_path = Path(temp_dir)
        
        try:
            runner = PKMValidationRunner(vault_path)
            wiki_validator = WikiLinkValidator(vault_path)
            runner.add_validator(wiki_validator)
            
            # Create test file
            test_file = vault_path / "test.md"
            test_file.write_text("""---
date: 2024-01-01
type: zettel
tags: [test]
status: draft
---

# Test

Reference to [[Non Existent]] note.
""")
            
            results = runner.validate_file(test_file)
            
            # Should have wiki-link validation error
            wiki_errors = [r for r in results if r.rule.startswith("broken-wiki-link")]
            assert len(wiki_errors) > 0
            
        finally:
            import shutil
            shutil.rmtree(temp_dir)
            
    def test_performance_with_large_file(self):
        """Task 4.3: Performance benchmark test"""
        temp_dir = tempfile.mkdtemp()
        vault_path = Path(temp_dir)
        
        try:
            # Create large file with many links
            large_content = """---
date: 2024-01-01
type: zettel
tags: [test]
status: draft
---

# Large Test File

""" + "\n".join([f"Link {i}: [[Test Link {i}]]" for i in range(100)])
            
            test_file = vault_path / "large-test.md"
            test_file.write_text(large_content)
            
            validator = WikiLinkValidator(vault_path)
            
            import time
            start_time = time.time()
            results = validator.validate(test_file)
            end_time = time.time()
            
            # Should complete within reasonable time
            validation_time = end_time - start_time
            assert validation_time < 1.0  # Less than 1 second for 100 links
            
        finally:
            import shutil
            shutil.rmtree(temp_dir)


# Test execution guard
if __name__ == "__main__":
    pytest.main([__file__, "-v"])