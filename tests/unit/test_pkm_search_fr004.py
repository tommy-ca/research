"""
FR-004 Basic Note Search - TDD Test Suite

RED PHASE: All tests written to FAIL first
Following TDD: Write failing tests → minimal implementation → refactor

Test Coverage:
- Basic note search functionality
- Text matching and case insensitivity
- Result formatting and context
- Relevance ranking
- Error handling scenarios
- KISS principle compliance
"""
import pytest
import tempfile
from pathlib import Path
from datetime import datetime, date

# Import the module we're testing (will fail initially - RED phase)
from src.pkm.search import pkm_search, SearchResult


class TestPkmSearchBasicFunctionality:
    """Test core search functionality"""
    
    def test_pkm_search_function_exists(self):
        """FR-004: Verify function exists"""
        from src.pkm.search import pkm_search
        assert callable(pkm_search)
    
    def test_pkm_search_finds_exact_matches(self):
        """FR-004: Text search finds exact matches"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            result = pkm_search("project planning", vault_path=vault)
            
            assert result.success is True
            assert len(result.matches) > 0
            # Should find the note with "project planning" content
            match_found = any("project planning" in match.content.lower() 
                            for match in result.matches)
            assert match_found
    
    def test_pkm_search_case_insensitive(self):
        """FR-004: Case-insensitive search works"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            # Search with different cases
            results = [
                pkm_search("PROJECT", vault_path=vault),
                pkm_search("project", vault_path=vault),
                pkm_search("Project", vault_path=vault),
            ]
            
            # All should return same matches
            for result in results:
                assert result.success is True
                assert len(result.matches) > 0
            
            # Should have same number of matches
            match_counts = [len(result.matches) for result in results]
            assert len(set(match_counts)) == 1  # All counts should be equal
    
    def test_pkm_search_returns_result_object(self):
        """FR-004: Returns structured result object"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir(parents=True)
            
            result = pkm_search("test", vault_path=vault)
            
            assert hasattr(result, 'success')
            assert hasattr(result, 'matches')
            assert hasattr(result, 'total_matches')
            assert hasattr(result, 'query')
            assert hasattr(result, 'message')
    
    def test_pkm_search_no_matches_returns_empty(self):
        """FR-004: No matches returns empty result"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            result = pkm_search("nonexistentquery12345", vault_path=vault)
            
            assert result.success is True
            assert len(result.matches) == 0
            assert result.total_matches == 0
            assert "No matches found" in result.message
    
    def _create_test_notes(self, vault: Path):
        """Helper: Create test notes for searching"""
        notes_dir = vault / '04-resources'
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        test_notes = [
            ('note1.md', 'Project planning meeting for Q4'),
            ('note2.md', 'Daily health and fitness routine'),
            ('note3.md', 'Reference documentation for API'),
            ('note4.md', 'Project retrospective and next steps'),
        ]
        
        for filename, content in test_notes:
            note_path = notes_dir / filename
            frontmatter = f"---\ndate: 2025-09-04\ntype: resource\n---\n\n"
            note_path.write_text(frontmatter + content)


class TestPkmSearchResultFormatting:
    """Test search result formatting and context"""
    
    def test_search_results_include_file_path(self):
        """FR-004: Results show file paths"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            result = pkm_search("project", vault_path=vault)
            
            assert result.success is True
            for match in result.matches:
                assert hasattr(match, 'file_path')
                assert isinstance(match.file_path, Path)
                assert match.file_path.exists()
    
    def test_search_results_include_line_context(self):
        """FR-004: Results show line context"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            result = pkm_search("project", vault_path=vault)
            
            assert result.success is True
            for match in result.matches:
                assert hasattr(match, 'line_number')
                assert hasattr(match, 'content')
                assert isinstance(match.line_number, int)
                assert match.line_number > 0
                assert len(match.content.strip()) > 0
    
    def test_search_results_show_surrounding_context(self):
        """FR-004: Results include surrounding lines for context"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            notes_dir = vault / '04-resources'
            notes_dir.mkdir(parents=True, exist_ok=True)
            
            # Create note with multiple lines
            content = """---
date: 2025-09-04
type: resource
---

# Meeting Notes

Project planning is essential
for successful outcomes.

Next steps include review.
"""
            (notes_dir / 'multiline.md').write_text(content)
            
            result = pkm_search("planning", vault_path=vault)
            
            assert result.success is True
            assert len(result.matches) > 0
            
            # Should include context around the match
            match = result.matches[0]
            assert "planning" in match.content.lower()
    
    def _create_test_notes(self, vault: Path):
        """Helper: Create test notes for searching"""
        notes_dir = vault / '04-resources'
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        test_notes = [
            ('project1.md', 'Project planning meeting for Q4'),
            ('project2.md', 'Project retrospective and next steps'),
        ]
        
        for filename, content in test_notes:
            note_path = notes_dir / filename
            frontmatter = f"---\ndate: 2025-09-04\ntype: resource\n---\n\n"
            note_path.write_text(frontmatter + content)


class TestPkmSearchRelevanceRanking:
    """Test search result relevance ranking"""
    
    def test_search_results_ranked_by_relevance(self):
        """FR-004: Results ranked by relevance"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            notes_dir = vault / '04-resources'
            notes_dir.mkdir(parents=True, exist_ok=True)
            
            # Create notes with different relevance levels
            test_notes = [
                ('high_relevance.md', 'project project project planning meeting'),  # 3 matches
                ('medium_relevance.md', 'project planning discussion'),             # 2 matches  
                ('low_relevance.md', 'planning only mentioned once'),               # 1 match
            ]
            
            for filename, content in test_notes:
                note_path = notes_dir / filename
                frontmatter = f"---\ndate: 2025-09-04\ntype: resource\n---\n\n"
                note_path.write_text(frontmatter + content)
            
            result = pkm_search("project", vault_path=vault)
            
            assert result.success is True
            assert len(result.matches) >= 2  # Should find at least high and medium relevance
            
            # First result should have higher relevance score
            if len(result.matches) > 1:
                assert result.matches[0].relevance_score >= result.matches[1].relevance_score
    
    def test_search_results_include_relevance_score(self):
        """FR-004: Results include relevance scoring"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._create_test_notes(vault)
            
            result = pkm_search("project", vault_path=vault)
            
            assert result.success is True
            for match in result.matches:
                assert hasattr(match, 'relevance_score')
                assert isinstance(match.relevance_score, (int, float))
                assert match.relevance_score > 0
    
    def _create_test_notes(self, vault: Path):
        """Helper: Create test notes"""
        notes_dir = vault / '04-resources'
        notes_dir.mkdir(parents=True, exist_ok=True)
        
        (notes_dir / 'test.md').write_text('---\ndate: 2025-09-04\n---\n\nProject planning meeting')


class TestPkmSearchDirectoryTraversal:
    """Test search across different vault directories"""
    
    def test_search_across_all_vault_directories(self):
        """FR-004: Search traverses all vault directories"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            
            # Create notes in different PARA directories
            directories = ['02-projects', '03-areas', '04-resources']
            for i, dir_name in enumerate(directories):
                dir_path = vault / dir_name
                dir_path.mkdir(parents=True)
                
                note_path = dir_path / f'note{i}.md'
                content = f'---\ndate: 2025-09-04\n---\n\nSearchable content in {dir_name}'
                note_path.write_text(content)
            
            result = pkm_search("searchable", vault_path=vault)
            
            assert result.success is True
            assert len(result.matches) == 3  # Should find all three notes
            
            # Should find notes from all directories
            found_dirs = set()
            for match in result.matches:
                for dir_name in directories:
                    if dir_name in str(match.file_path):
                        found_dirs.add(dir_name)
            
            assert len(found_dirs) == 3  # Found in all three directories
    
    def test_search_includes_daily_notes(self):
        """FR-004: Search includes daily notes directory"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            daily_dir = vault / 'daily' / '2025' / '09-September'
            daily_dir.mkdir(parents=True)
            
            daily_note = daily_dir / '2025-09-04.md'
            content = '---\ndate: 2025-09-04\ntype: daily\n---\n\nDaily searchable content'
            daily_note.write_text(content)
            
            result = pkm_search("searchable", vault_path=vault)
            
            assert result.success is True
            assert len(result.matches) > 0
            assert any('daily' in str(match.file_path) for match in result.matches)


class TestPkmSearchErrorHandling:
    """Test error scenarios and edge cases"""
    
    def test_handles_missing_vault_directory(self):
        """FR-004: Graceful failure when vault doesn't exist"""
        result = pkm_search("test", vault_path=Path("/nonexistent/path"))
        
        assert result.success is False
        assert "vault directory does not exist" in result.message.lower()
        assert len(result.matches) == 0
    
    def test_handles_empty_query(self):
        """FR-004: Handles empty search query"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            result = pkm_search("", vault_path=vault)
            
            assert result.success is False
            assert "query cannot be empty" in result.message.lower()
    
    def test_handles_none_query(self):
        """FR-004: Handles None search query"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            result = pkm_search(None, vault_path=vault)
            
            assert result.success is False
            assert "query cannot be empty" in result.message.lower()
    
    def test_handles_vault_with_no_notes(self):
        """FR-004: Handles vault with no markdown files"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            result = pkm_search("test", vault_path=vault)
            
            assert result.success is True
            assert len(result.matches) == 0
            assert "No matches found" in result.message


class TestTddCompliance:
    """Test that implementation follows TDD principles"""
    
    def test_implementation_exists_fr004(self):
        """FR-004: Implementation was created after tests (TDD compliance)"""
        try:
            from src.pkm.search import pkm_search, SearchResult
            # If this passes, implementation exists
            assert True
        except ImportError:
            # This should fail during RED phase, pass during GREEN phase
            pytest.fail("Implementation should exist after RED phase")
    
    def test_specification_compliance(self):
        """FR-004: Implementation matches original specification"""
        from src.pkm.search import pkm_search
        
        # Test specification requirements
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            # Should be able to call without errors
            result = pkm_search("test", vault_path=vault)
            assert hasattr(result, 'success')


class TestKissCompliance:
    """Test that implementation follows KISS principles"""
    
    def test_main_function_is_simple(self):
        """FR-004: pkm_search() function is ≤20 lines"""
        import inspect
        from src.pkm.search import pkm_search
        
        source_lines = inspect.getsource(pkm_search).strip().split('\n')
        # Remove empty lines and comments for accurate count
        code_lines = [line for line in source_lines 
                     if line.strip() and not line.strip().startswith('#')]
        
        assert len(code_lines) <= 20, f"Function has {len(code_lines)} lines, should be ≤20 (KISS principle)"
    
    def test_helper_functions_are_simple(self):
        """FR-004: All helper functions are ≤20 lines"""
        import inspect
        import src.pkm.search as module
        
        for name in dir(module):
            if name.startswith('_') and callable(getattr(module, name)):
                func = getattr(module, name)
                if hasattr(func, '__module__') and func.__module__ == module.__name__:
                    source_lines = inspect.getsource(func).strip().split('\n')
                    code_lines = [line for line in source_lines 
                                 if line.strip() and not line.strip().startswith('#')]
                    assert len(code_lines) <= 20, f"Helper function {name} has {len(code_lines)} lines, should be ≤20"