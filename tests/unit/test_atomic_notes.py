"""
Unit tests for PKM atomic note creation functionality
TDD Cycle 3 - RED phase implementation following KISS, DRY, SOLID principles
Comprehensive test suite for Zettelkasten atomic notes with linking system
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
    from src.pkm.core.atomic_notes import PkmAtomicNote, AtomicNoteResult
    from src.pkm.exceptions import ProcessingError
except ImportError:
    # Expected during RED phase - tests written before implementation
    PkmAtomicNote = None
    AtomicNoteResult = None
    ProcessingError = Exception


class TestPkmAtomicNote:
    """Unit tests for PKM atomic note creation functionality"""
    
    @pytest.fixture
    def atomic_note_service(self, temp_vault):
        """Fixture providing configured atomic note service"""
        if PkmAtomicNote is None:
            pytest.skip("PkmAtomicNote not implemented yet (TDD RED phase)")
        return PkmAtomicNote(vault_path=str(temp_vault))
    
    # Category 1: Core Creation Tests (KISS Principle)
    
    def test_creates_atomic_note_with_unique_id(self, atomic_note_service, temp_vault):
        """Should create atomic note with unique timestamp-based ID (YYYYMMDDHHMM)"""
        # Arrange
        title = "My First Atomic Note"
        content = "This is the content of my atomic note."
        
        # Act
        result = atomic_note_service.create_note(title, content)
        
        # Assert
        assert result.success is True
        assert result.note_id is not None
        assert len(result.note_id) == 14  # Nanosecond-based unique ID
        assert result.note_id.isdigit()
        
        # File should exist in permanent/notes/
        expected_path = temp_vault / "permanent" / "notes"
        assert expected_path.exists()
        note_files = list(expected_path.glob("*.md"))
        assert len(note_files) == 1
        assert result.note_id in note_files[0].name
    
    def test_generates_proper_frontmatter(self, atomic_note_service, temp_vault):
        """Should generate atomic note frontmatter with required metadata"""
        # Arrange
        title = "Test Note"
        content = "Test content with [[Link to Other Note]]"
        
        # Act
        result = atomic_note_service.create_note(title, content)
        
        # Assert
        note_file = temp_vault / "permanent" / "notes" / f"{result.note_id}-test-note.md"
        file_content = note_file.read_text(encoding='utf-8')
        
        # Should contain YAML frontmatter
        assert file_content.startswith('---')
        
        # Extract and validate frontmatter
        parts = file_content.split('---', 2)
        frontmatter = yaml.safe_load(parts[1])
        
        assert frontmatter['type'] == 'atomic'
        assert frontmatter['title'] == title
        assert frontmatter['created'] is not None
        assert frontmatter['id'] == result.note_id
        assert 'links' in frontmatter
        assert isinstance(frontmatter['tags'], list)
    
    def test_stores_in_permanent_notes_directory(self, atomic_note_service, temp_vault):
        """Should store atomic notes in vault/permanent/notes/ directory"""
        # Arrange
        title = "Storage Test Note"
        content = "Testing storage location"
        
        # Act
        result = atomic_note_service.create_note(title, content)
        
        # Assert
        expected_dir = temp_vault / "permanent" / "notes"
        assert expected_dir.exists()
        
        expected_filename = f"{result.note_id}-storage-test-note.md"
        expected_path = expected_dir / expected_filename
        assert expected_path.exists()
        
        # Should not be in other directories
        assert not (temp_vault / "00-inbox").exists() or len(list((temp_vault / "00-inbox").glob("*.md"))) == 0
    
    def test_handles_invalid_input_gracefully(self, atomic_note_service):
        """Should handle invalid inputs with appropriate errors"""
        # Test empty title
        with pytest.raises(ProcessingError, match="Title cannot be empty"):
            atomic_note_service.create_note("", "Valid content")
        
        # Test empty content
        with pytest.raises(ProcessingError, match="Content cannot be empty"):
            atomic_note_service.create_note("Valid Title", "")
        
        # Test None values
        with pytest.raises(ProcessingError):
            atomic_note_service.create_note(None, "Valid content")
        
        with pytest.raises(ProcessingError):
            atomic_note_service.create_note("Valid Title", None)
        
        # Test whitespace-only inputs
        with pytest.raises(ProcessingError):
            atomic_note_service.create_note("   ", "Valid content")
        
        with pytest.raises(ProcessingError):
            atomic_note_service.create_note("Valid Title", "   ")
    
    def test_supports_unicode_content(self, atomic_note_service, temp_vault):
        """Should handle Unicode characters in title and content"""
        # Arrange
        title = "Unicode Test 🧠 Café Résumé"
        content = """
        # Unicode Content Test
        
        Chinese: 中文内容测试
        Japanese: 日本語のテスト
        Arabic: اختبار المحتوى العربي
        Emoji: 🚀 ⭐ 💡 📚
        Accents: café, résumé, naïve
        """
        
        # Act
        result = atomic_note_service.create_note(title, content)
        
        # Assert
        assert result.success is True
        
        # File should exist and contain Unicode content
        note_file = temp_vault / "permanent" / "notes" / f"{result.note_id}-unicode-test-cafe-resume.md"
        assert note_file.exists()
        
        file_content = note_file.read_text(encoding='utf-8')
        assert "中文内容测试" in file_content
        assert "🚀 ⭐ 💡 📚" in file_content
        assert "café" in file_content
    
    # Category 2: Linking System Tests (Open/Closed Principle)
    
    def test_extracts_wikilinks_from_content(self, atomic_note_service):
        """Should extract [[WikiLink]] style links from content"""
        # Arrange
        title = "Note with Links"
        content = """
        This note references [[Another Note]] and [[Second Reference]].
        It also mentions [[Third Note]] in passing.
        Regular text without links should be ignored.
        """
        
        # Act
        result = atomic_note_service.create_note(title, content)
        
        # Assert
        assert result.success is True
        assert len(result.links) == 3
        assert "Another Note" in result.links
        assert "Second Reference" in result.links
        assert "Third Note" in result.links
    
    def test_creates_backlink_references(self, atomic_note_service, temp_vault):
        """Should create backlink references in linked notes"""
        # Arrange - Create a target note first
        target_content = "This is the target note"
        target_result = atomic_note_service.create_note("Target Note", target_content)
        
        # Create a note that links to the target
        linking_content = "This note links to [[Target Note]] for reference"
        linking_result = atomic_note_service.create_note("Linking Note", linking_content)
        
        # Act & Assert
        # The target note should be updated with backlink information
        target_file = temp_vault / "permanent" / "notes" / f"{target_result.note_id}-target-note.md"
        target_file_content = target_file.read_text(encoding='utf-8')
        
        # Extract frontmatter to check backlinks
        parts = target_file_content.split('---', 2)
        frontmatter = yaml.safe_load(parts[1])
        
        assert 'backlinks' in frontmatter
        assert linking_result.note_id in frontmatter['backlinks']
    
    def test_maintains_link_index(self, atomic_note_service, temp_vault):
        """Should maintain a central index of note relationships"""
        # Arrange
        notes_data = [
            ("First Note", "Content linking to [[Second Note]]"),
            ("Second Note", "Content linking to [[Third Note]]"),
            ("Third Note", "Content linking back to [[First Note]]")
        ]
        
        results = []
        for title, content in notes_data:
            result = atomic_note_service.create_note(title, content)
            results.append(result)
        
        # Act & Assert
        # Check if link index file exists
        link_index_path = temp_vault / "permanent" / ".link_index.yml"
        assert link_index_path.exists()
        
        # Validate index content
        link_index = yaml.safe_load(link_index_path.read_text())
        assert len(link_index) == 3
        
        # Check bidirectional relationships
        first_id = results[0].note_id
        second_id = results[1].note_id
        third_id = results[2].note_id
        
        assert second_id in link_index[first_id]['links']
        assert first_id in link_index[third_id]['links']
    
    def test_handles_orphan_notes(self, atomic_note_service):
        """Should identify and handle notes with no links"""
        # Arrange
        orphan_content = "This is an orphan note with no links to other notes."
        
        # Act
        result = atomic_note_service.create_note("Orphan Note", orphan_content)
        
        # Assert
        assert result.success is True
        assert len(result.links) == 0
        assert result.is_orphan is True
    
    # Category 3: Indexing Tests (Dependency Inversion)
    
    def test_extracts_note_metadata(self, atomic_note_service):
        """Should extract comprehensive metadata from note content"""
        # Arrange
        title = "Metadata Test Note"
        content = """
        # Main Heading
        
        This note contains **bold text** and *italic text*.
        It has multiple paragraphs and lists:
        
        - Item 1
        - Item 2
        - Item 3
        
        Word count should be calculated automatically.
        """
        
        # Act
        result = atomic_note_service.create_note(title, content)
        
        # Assert
        assert result.metadata is not None
        assert result.metadata['word_count'] > 0
        assert result.metadata['paragraph_count'] > 0
        assert result.metadata['has_headings'] is True
        assert result.metadata['has_lists'] is True
    
    def test_generates_hierarchical_tags(self, atomic_note_service):
        """Should generate hierarchical tags from content analysis"""
        # Arrange
        title = "Machine Learning Concepts"
        content = """
        # Neural Networks and Deep Learning
        
        This note covers artificial intelligence concepts including:
        - Machine learning algorithms
        - Deep neural networks
        - Natural language processing
        - Computer vision applications
        """
        
        # Act
        result = atomic_note_service.create_note(title, content)
        
        # Assert
        assert result.tags is not None
        assert len(result.tags) > 0
        
        # Should contain hierarchical tags
        expected_tags = ["#ai/machine-learning", "#ai/neural-networks", "#ai/deep-learning"]
        for tag in expected_tags:
            assert any(tag in generated_tag for generated_tag in result.tags)
    
    def test_updates_search_index(self, atomic_note_service, temp_vault):
        """Should update full-text search index for note discovery"""
        # Arrange
        searchable_content = "This note contains searchable keywords like python programming"
        
        # Act
        result = atomic_note_service.create_note("Searchable Note", searchable_content)
        
        # Assert
        search_index_path = temp_vault / "permanent" / ".search_index.json"
        assert search_index_path.exists()
        
        # Validate search index content
        import json
        search_index = json.loads(search_index_path.read_text())
        
        assert result.note_id in search_index
        assert "python" in search_index[result.note_id]['keywords']
        assert "programming" in search_index[result.note_id]['keywords']
    
    # Category 4: Integration Tests (Liskov Substitution)
    
    def test_integrates_with_capture_workflow(self, atomic_note_service, temp_vault):
        """Should integrate seamlessly with existing capture workflow"""
        # Arrange - Simulate capture-to-atomic-note promotion
        captured_content = """
        ---
        date: 2024-08-22
        type: capture
        status: inbox
        ---
        
        # Captured Idea
        This was originally captured and now promoted to atomic note.
        """
        
        # Act
        result = atomic_note_service.promote_from_capture(captured_content)
        
        # Assert
        assert result.success is True
        assert result.promoted_from == "capture"
        
        # Original capture metadata should be preserved
        note_file = temp_vault / "permanent" / "notes" / f"{result.note_id}-captured-idea.md"
        file_content = note_file.read_text(encoding='utf-8')
        
        parts = file_content.split('---', 2)
        frontmatter = yaml.safe_load(parts[1])
        
        assert frontmatter['original_capture_date'] == '2024-08-22'
        assert frontmatter['type'] == 'atomic'  # Type should be updated
    
    def test_works_with_inbox_processing(self, atomic_note_service):
        """Should work with inbox processing for automatic note creation"""
        # This test verifies Liskov Substitution - atomic note service
        # should be usable wherever base processor is expected
        
        # Arrange
        def process_content(processor, title, content):
            # This function should work with any processor
            return processor.create_note(title, content)
        
        # Act
        result = process_content(atomic_note_service, "Test Note", "Test content")
        
        # Assert
        assert result.success is True
        assert hasattr(result, 'note_id')
    
    def test_maintains_system_consistency(self, atomic_note_service, temp_vault):
        """Should maintain consistency with existing PKM system patterns"""
        # Arrange
        title = "Consistency Test"
        content = "Testing system consistency"
        
        # Act
        result = atomic_note_service.create_note(title, content)
        
        # Assert - Should follow same patterns as capture and inbox processing
        assert hasattr(result, 'success')
        assert hasattr(result, 'file_path') or hasattr(result, 'note_id')
        
        # File should follow naming conventions
        note_files = list((temp_vault / "permanent" / "notes").glob("*.md"))
        assert len(note_files) == 1
        
        filename = note_files[0].name
        # Should match pattern: YYYYMMDDHHMM-title-slug.md
        assert len(filename.split('-')) >= 3
        assert filename.endswith('.md')


# Additional Edge Cases and Error Handling

class TestAtomicNoteEdgeCases:
    """Edge cases and error handling for atomic note creation"""
    
    @pytest.fixture
    def atomic_note_service(self, temp_vault):
        if PkmAtomicNote is None:
            pytest.skip("PkmAtomicNote not implemented yet (TDD RED phase)")
        return PkmAtomicNote(vault_path=str(temp_vault))
    
    def test_handles_extremely_long_titles(self, atomic_note_service):
        """Should handle very long titles with appropriate truncation"""
        # Arrange
        long_title = "A" * 200  # 200 character title
        content = "Short content"
        
        # Act
        result = atomic_note_service.create_note(long_title, content)
        
        # Assert
        assert result.success is True
        # Filename should be truncated but still readable
        assert len(result.file_path.split('/')[-1]) < 100
    
    def test_handles_concurrent_note_creation(self, atomic_note_service):
        """Should handle multiple notes created simultaneously"""
        # Arrange
        import threading
        results = []
        
        def create_note(index):
            result = atomic_note_service.create_note(f"Concurrent Note {index}", f"Content {index}")
            results.append(result)
        
        # Act
        threads = []
        for i in range(5):
            thread = threading.Thread(target=create_note, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Assert
        assert len(results) == 5
        assert all(result.success for result in results)
        
        # All note IDs should be unique
        note_ids = [result.note_id for result in results]
        assert len(set(note_ids)) == 5


# These tests should ALL FAIL initially (TDD RED phase)
# Implementation comes next (GREEN phase)
# Then refactoring with KISS, DRY, SOLID principles (REFACTOR phase)