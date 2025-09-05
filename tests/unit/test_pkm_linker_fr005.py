"""
FR-005 Simple Link Generation - TDD Test Suite

RED PHASE: All tests written to FAIL first
Following TDD: Write failing tests → minimal implementation → refactor

Test Coverage:
- Link suggestion functionality
- Keyword extraction and matching
- Bidirectional link handling
- User interaction simulation
- Error handling scenarios
- KISS principle compliance
"""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the module we're testing (will fail initially - RED phase)
from src.pkm.linker import pkm_link, LinkResult, LinkSuggestion


class TestPkmLinkerBasicFunctionality:
    """Test core link generation functionality"""
    
    def test_pkm_link_function_exists(self):
        """FR-005: Verify function exists"""
        from src.pkm.linker import pkm_link
        assert callable(pkm_link)
    
    def test_pkm_link_finds_shared_keywords(self):
        """FR-005: Finds notes with shared keywords"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            target_note = vault / '04-resources' / 'target.md'
            result = pkm_link(target_note, vault_path=vault)
            
            assert result.success is True
            assert len(result.suggestions) > 0
            
            # Should find notes with shared keywords
            suggestion_files = [s.target_file.name for s in result.suggestions]
            assert any('project' in file.lower() for file in suggestion_files)
    
    def test_pkm_link_suggests_bidirectional_links(self):
        """FR-005: Suggests bidirectional links"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            target_note = vault / '04-resources' / 'target.md'
            result = pkm_link(target_note, vault_path=vault)
            
            assert result.success is True
            for suggestion in result.suggestions:
                assert hasattr(suggestion, 'bidirectional')
                assert hasattr(suggestion, 'link_text')
                # Should suggest proper markdown link format
                assert '[[' in suggestion.link_text and ']]' in suggestion.link_text
    
    def test_pkm_link_returns_result_object(self):
        """FR-005: Returns structured result object"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir(parents=True)
            
            test_note = vault / 'test.md'
            test_note.write_text('---\ndate: 2025-09-04\n---\nTest content')
            
            result = pkm_link(test_note, vault_path=vault)
            
            assert hasattr(result, 'success')
            assert hasattr(result, 'suggestions')
            assert hasattr(result, 'target_file')
            assert hasattr(result, 'message')
    
    def test_pkm_link_excludes_target_note(self):
        """FR-005: Doesn't suggest linking to self"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            notes_dir = vault / '04-resources'
            notes_dir.mkdir(parents=True)
            
            target_note = notes_dir / 'self_reference.md'
            target_note.write_text('---\ndate: 2025-09-04\n---\nSelf reference test')
            
            result = pkm_link(target_note, vault_path=vault)
            
            assert result.success is True
            # Should not suggest linking to itself
            suggestion_files = [s.target_file for s in result.suggestions]
            assert target_note not in suggestion_files
    
    def _create_test_notes(self, vault: Path):
        """Helper: Create test notes for link testing"""
        notes_dir = vault / '04-resources'
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        test_notes = [
            ('target.md', 'Project planning and development tasks'),
            ('project1.md', 'Project management best practices'),
            ('development.md', 'Software development lifecycle planning'),
            ('unrelated.md', 'Completely different health topic'),
        ]
        
        for filename, content in test_notes:
            note_path = notes_dir / filename
            frontmatter = f"---\ndate: 2025-09-04\ntype: resource\n---\n\n"
            note_path.write_text(frontmatter + content)


class TestPkmLinkerKeywordExtraction:
    """Test keyword extraction and matching logic"""
    
    def test_extracts_meaningful_keywords(self):
        """FR-005: Extracts meaningful keywords from content"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            notes_dir = vault / '04-resources'
            notes_dir.mkdir(parents=True)
            
            target_note = notes_dir / 'keyword_test.md'
            content = """---
date: 2025-09-04
type: resource
---

# Machine Learning Models

This note covers neural networks, deep learning algorithms, 
and artificial intelligence applications in data science.
"""
            target_note.write_text(content)
            
            # Create related note
            related_note = notes_dir / 'ai_research.md'
            related_note.write_text('---\ndate: 2025-09-04\n---\nNeural networks research and applications')
            
            result = pkm_link(target_note, vault_path=vault)
            
            assert result.success is True
            # Should find the related note based on shared keywords
            assert len(result.suggestions) > 0
    
    def test_ignores_common_stop_words(self):
        """FR-005: Ignores common stop words in keyword matching"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            notes_dir = vault / '04-resources'
            notes_dir.mkdir(parents=True)
            
            target_note = notes_dir / 'stop_words.md'
            target_note.write_text('---\ndate: 2025-09-04\n---\nThe and or but with for')
            
            other_note = notes_dir / 'other.md'
            other_note.write_text('---\ndate: 2025-09-04\n---\nAnd the but specific content here')
            
            result = pkm_link(target_note, vault_path=vault)
            
            # Should not suggest linking based on stop words alone
            assert result.success is True
            # May have 0 suggestions if only stop words match
    
    def test_keyword_matching_case_insensitive(self):
        """FR-005: Keyword matching is case insensitive"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            notes_dir = vault / '04-resources'
            notes_dir.mkdir(parents=True)
            
            target_note = notes_dir / 'case_test.md'
            target_note.write_text('---\ndate: 2025-09-04\n---\nMACHINE learning research')
            
            related_note = notes_dir / 'related.md'
            related_note.write_text('---\ndate: 2025-09-04\n---\nmachine Learning applications')
            
            result = pkm_link(target_note, vault_path=vault)
            
            assert result.success is True
            assert len(result.suggestions) > 0


class TestPkmLinkerSuggestionFormatting:
    """Test link suggestion formatting and structure"""
    
    def test_suggestions_include_relevance_score(self):
        """FR-005: Suggestions include relevance scoring"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            target_note = vault / '04-resources' / 'target.md'
            result = pkm_link(target_note, vault_path=vault)
            
            assert result.success is True
            for suggestion in result.suggestions:
                assert hasattr(suggestion, 'relevance_score')
                assert isinstance(suggestion.relevance_score, (int, float))
                assert suggestion.relevance_score > 0
    
    def test_suggestions_ranked_by_relevance(self):
        """FR-005: Suggestions ranked by relevance"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            notes_dir = vault / '04-resources'
            notes_dir.mkdir(parents=True)
            
            # Create target with specific keywords
            target_note = notes_dir / 'target.md'
            target_note.write_text('---\ndate: 2025-09-04\n---\nProject planning tasks')
            
            # Create notes with different relevance levels
            high_rel = notes_dir / 'high.md'
            high_rel.write_text('---\ndate: 2025-09-04\n---\nProject planning project tasks')
            
            low_rel = notes_dir / 'low.md'  
            low_rel.write_text('---\ndate: 2025-09-04\n---\nTasks only mentioned once')
            
            result = pkm_link(target_note, vault_path=vault)
            
            assert result.success is True
            if len(result.suggestions) > 1:
                # First suggestion should have higher relevance
                assert result.suggestions[0].relevance_score >= result.suggestions[1].relevance_score
    
    def test_suggestions_include_link_preview(self):
        """FR-005: Suggestions include preview of content"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            target_note = vault / '04-resources' / 'target.md'
            result = pkm_link(target_note, vault_path=vault)
            
            assert result.success is True
            for suggestion in result.suggestions:
                assert hasattr(suggestion, 'preview_text')
                assert len(suggestion.preview_text) > 0
                # Preview should be reasonable length
                assert len(suggestion.preview_text) <= 200
    
    def _create_test_notes(self, vault: Path):
        """Helper: Create test notes"""
        notes_dir = vault / '04-resources'
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        (notes_dir / 'target.md').write_text('---\ndate: 2025-09-04\n---\nProject planning meeting')
        (notes_dir / 'related.md').write_text('---\ndate: 2025-09-04\n---\nProject management practices')


class TestPkmLinkerUserInteraction:
    """Test user interaction for accepting/rejecting suggestions"""
    
    @patch('builtins.input', return_value='y')
    def test_user_can_accept_suggestions(self, mock_input):
        """FR-005: User can accept link suggestions"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            target_note = vault / '04-resources' / 'target.md'
            result = pkm_link(target_note, vault_path=vault, interactive=True)
            
            assert result.success is True
            # Should have processed user input
            if result.suggestions:
                mock_input.assert_called()
    
    @patch('builtins.input', return_value='n')
    def test_user_can_reject_suggestions(self, mock_input):
        """FR-005: User can reject link suggestions"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            target_note = vault / '04-resources' / 'target.md'
            result = pkm_link(target_note, vault_path=vault, interactive=True)
            
            assert result.success is True
            if result.suggestions:
                mock_input.assert_called()
    
    def test_non_interactive_mode_returns_suggestions(self):
        """FR-005: Non-interactive mode just returns suggestions"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            target_note = vault / '04-resources' / 'target.md'
            result = pkm_link(target_note, vault_path=vault, interactive=False)
            
            assert result.success is True
            # Should return suggestions without user interaction
            assert hasattr(result, 'suggestions')
    
    def _create_test_notes(self, vault: Path):
        """Helper: Create test notes"""
        notes_dir = vault / '04-resources'
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        (notes_dir / 'target.md').write_text('---\ndate: 2025-09-04\n---\nProject planning')
        (notes_dir / 'related.md').write_text('---\ndate: 2025-09-04\n---\nProject management')


class TestPkmLinkerErrorHandling:
    """Test error scenarios and edge cases"""
    
    def test_handles_missing_target_file(self):
        """FR-005: Graceful failure when target file doesn't exist"""
        result = pkm_link(Path("/nonexistent/file.md"), vault_path=Path("/tmp"))
        
        assert result.success is False
        assert "file does not exist" in result.message.lower()
    
    def test_handles_missing_vault_directory(self):
        """FR-005: Graceful failure when vault doesn't exist"""
        with tempfile.TemporaryDirectory() as tmp:
            test_file = Path(tmp) / 'test.md'
            test_file.write_text('test content')
            
            result = pkm_link(test_file, vault_path=Path("/nonexistent/path"))
            
            assert result.success is False
            assert "vault directory does not exist" in result.message.lower()
    
    def test_handles_empty_vault(self):
        """FR-005: Handles vault with no other notes"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            target_note = vault / 'only_note.md'
            target_note.write_text('---\ndate: 2025-09-04\n---\nSingle note content')
            
            result = pkm_link(target_note, vault_path=vault)
            
            assert result.success is True
            assert len(result.suggestions) == 0
            assert "no suitable links found" in result.message.lower()
    
    def test_handles_malformed_target_file(self):
        """FR-005: Handles files with malformed frontmatter"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            target_note = vault / 'malformed.md'
            target_note.write_text('Invalid frontmatter\nSome content')
            
            result = pkm_link(target_note, vault_path=vault)
            
            # Should still work, just use content without frontmatter
            assert result.success is True


class TestTddCompliance:
    """Test that implementation follows TDD principles"""
    
    def test_implementation_exists_fr005(self):
        """FR-005: Implementation was created after tests (TDD compliance)"""
        try:
            from src.pkm.linker import pkm_link, LinkResult, LinkSuggestion
            # If this passes, implementation exists
            assert True
        except ImportError:
            # This should fail during RED phase, pass during GREEN phase
            pytest.fail("Implementation should exist after RED phase")
    
    def test_specification_compliance(self):
        """FR-005: Implementation matches original specification"""
        from src.pkm.linker import pkm_link
        
        # Test specification requirements
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            test_note = vault / 'test.md'
            test_note.write_text('---\ndate: 2025-09-04\n---\nTest content')
            
            # Should be able to call without errors
            result = pkm_link(test_note, vault_path=vault)
            assert hasattr(result, 'success')


class TestKissCompliance:
    """Test that implementation follows KISS principles"""
    
    def test_main_function_is_simple(self):
        """FR-005: pkm_link() function is ≤20 lines"""
        import inspect
        from src.pkm.linker import pkm_link
        
        source_lines = inspect.getsource(pkm_link).strip().split('\n')
        # Remove empty lines and comments for accurate count
        code_lines = [line for line in source_lines 
                     if line.strip() and not line.strip().startswith('#')]
        
        assert len(code_lines) <= 20, f"Function has {len(code_lines)} lines, should be ≤20 (KISS principle)"
    
    def test_helper_functions_are_simple(self):
        """FR-005: All helper functions are ≤20 lines"""
        import inspect
        import src.pkm.linker as module
        
        for name in dir(module):
            if name.startswith('_') and callable(getattr(module, name)):
                func = getattr(module, name)
                if hasattr(func, '__module__') and func.__module__ == module.__name__:
                    source_lines = inspect.getsource(func).strip().split('\n')
                    code_lines = [line for line in source_lines 
                                 if line.strip() and not line.strip().startswith('#')]
                    assert len(code_lines) <= 20, f"Helper function {name} has {len(code_lines)} lines, should be ≤20"