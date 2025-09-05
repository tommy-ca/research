"""
TDD Tests for FR-004: Basic Note Search Command

RED PHASE - These tests MUST FAIL initially to enforce TDD workflow.

Test Specification:
- Given: Notes exist in vault
- When: User runs `/pkm-search "query"`  
- Then: Matching notes displayed with context
- And: Results ranked by relevance

Engineering Principles:
- TDD: Test specification drives implementation
- KISS: Simple text search using grep, no complex indexing
- FR-First: Basic functionality before advanced search features
- SRP: Search function has single clear responsibility
"""

import pytest
import tempfile
from pathlib import Path
from typing import NamedTuple, List, Optional, Dict
import re


# SOLID Principles: Interface Segregation
class SearchResult(NamedTuple):
    """Single search result with context"""
    filepath: Path
    line_number: int
    line_content: str
    match_context: str  # Surrounding lines for context
    relevance_score: float


class SearchResults(NamedTuple):
    """Complete search results"""
    query: str
    results: List[SearchResult]
    total_matches: int
    files_searched: int
    search_time_ms: float
    success: bool
    error: Optional[str] = None


class TestPkmSearchBasicFunctionality:
    """
    RED PHASE: All tests MUST FAIL initially
    
    Tests define specification for simple grep-based search
    Following KISS: Basic text matching before advanced features
    """
    
    @pytest.fixture
    def vault_with_sample_notes(self):
        """Create vault with various sample notes for search testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            
            # Create sample notes with different content
            sample_notes = {
                "01-projects/machine-learning.md": '''---
date: 2024-01-01
type: project
tags: [ai, machine-learning, python]
---

# Machine Learning Project

This project involves building a neural network for image classification.
We need to implement convolutional layers and train the model on large datasets.

## Requirements
- Python with TensorFlow
- GPU support for training
- Large dataset (>10GB)
''',
                "02-areas/research.md": '''---
date: 2024-01-02
type: area
tags: [research, academic]
---

# Research Area

This area covers ongoing research activities in artificial intelligence.
Topics include machine learning, natural language processing, and computer vision.

Key papers to review:
- Attention Is All You Need
- BERT: Pre-training of Deep Bidirectional Transformers
''',
                "03-resources/python-tutorial.md": '''---
date: 2024-01-03
type: resource
tags: [python, programming, tutorial]
---

# Python Programming Tutorial

Basic Python concepts for beginners:

1. Variables and data types
2. Functions and classes  
3. File I/O operations
4. Error handling with try/except

Python is great for machine learning and data science.
''',
                "daily/2024/01-january/2024-01-15.md": '''---
date: 2024-01-15
type: daily
tags: [daily-notes]
---

# Daily Note - 2024-01-15

## Tasks
- Review machine learning papers
- Update Python project
- Meeting with research team

## Notes
Today I learned about transformer architectures in deep learning.
The attention mechanism is really fascinating.
'''
            }
            
            # Create all sample notes
            for relative_path, content in sample_notes.items():
                note_path = vault_path / relative_path
                note_path.parent.mkdir(parents=True, exist_ok=True)
                note_path.write_text(content)
            
            yield vault_path
    
    def test_pkm_search_function_not_implemented_yet(self):
        """
        RED TEST: Must fail - no search function exists
        
        Ensures proper TDD RED phase compliance
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import search_vault
    
    def test_pkm_search_basic_text_matching(self, vault_with_sample_notes):
        """
        RED TEST: Must fail - basic text search not implemented
        
        Test Spec: Simple text search across all notes
        - Case-insensitive matching by default
        - Returns file paths and line numbers
        - Includes surrounding context for matches
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import search_vault
            
        # Future test validation:
        # results = search_vault("machine learning", vault_path=vault_with_sample_notes)
        # assert results.success is True
        # assert len(results.results) > 0
        # 
        # # Should find matches in multiple files
        # matched_files = [r.filepath.name for r in results.results]
        # assert "machine-learning.md" in matched_files
        # assert "research.md" in matched_files
    
    def test_pkm_search_case_insensitive_matching(self, vault_with_sample_notes):
        """
        RED TEST: Must fail - case insensitive search not implemented
        
        Test Spec: Case insensitive text matching
        - "Python" matches "python" and "PYTHON"
        - "Machine Learning" matches "machine learning"
        - Preserve original case in results
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import search_vault
            
        # Future validation:
        # results = search_vault("PYTHON", vault_path=vault_with_sample_notes)
        # assert len(results.results) > 0
        # 
        # # Should find both "Python" and "python" instances
        # found_content = [r.line_content for r in results.results]
        # assert any("python" in content.lower() for content in found_content)
    
    def test_pkm_search_provides_line_context(self, vault_with_sample_notes):
        """
        RED TEST: Must fail - context extraction not implemented
        
        Test Spec: Provide context around matches
        - Include 1-2 lines before and after match
        - Show line numbers for matches
        - Truncate very long lines appropriately
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import search_vault
            
        # Future validation:
        # results = search_vault("neural network", vault_path=vault_with_sample_notes)
        # 
        # for result in results.results:
        #     assert result.line_number > 0
        #     assert len(result.match_context) > len(result.line_content)
        #     assert result.line_content in result.match_context
    
    def test_pkm_search_ranks_results_by_relevance(self, vault_with_sample_notes):
        """
        RED TEST: Must fail - relevance ranking not implemented
        
        Test Spec: Simple relevance scoring
        - Multiple matches in same file = higher score
        - Matches in titles/headers = higher score
        - Earlier matches in document = slightly higher score
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import calculate_relevance_score
            
        # Future validation:
        # results = search_vault("machine learning", vault_path=vault_with_sample_notes)
        # 
        # # Results should be sorted by relevance score (highest first)
        # scores = [r.relevance_score for r in results.results]
        # assert scores == sorted(scores, reverse=True)
        # 
        # # File with multiple matches should have higher total relevance
        # ml_project_results = [r for r in results.results if "machine-learning" in str(r.filepath)]
        # other_results = [r for r in results.results if "machine-learning" not in str(r.filepath)]
        # if ml_project_results and other_results:
        #     max_ml_score = max(r.relevance_score for r in ml_project_results)
        #     max_other_score = max(r.relevance_score for r in other_results)
        #     assert max_ml_score >= max_other_score
    
    def test_pkm_search_handles_multiple_terms(self, vault_with_sample_notes):
        """
        RED TEST: Must fail - multi-term search not implemented
        
        Test Spec: Multiple search terms
        - "machine learning python" finds notes with all terms
        - Terms can appear in any order
        - Quoted phrases searched as exact strings
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import parse_search_query
            
        # Future validation:
        # results = search_vault("machine learning python", vault_path=vault_with_sample_notes)
        # 
        # # Should find notes containing all three words
        # for result in results.results:
        #     content = result.filepath.read_text().lower()
        #     assert "machine" in content
        #     assert "learning" in content  
        #     assert "python" in content


class TestPkmSearchAdvancedFeatures:
    """
    RED PHASE: Advanced search features specification
    These are LOWER priority - implement after basic search works
    """
    
    @pytest.fixture
    def vault_with_sample_notes(self):
        """Reuse sample vault from basic tests"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            
            note_content = '''---
date: 2024-01-01
type: project
tags: [ai, research]
---

# AI Research Project

This project focuses on natural language processing.
'''
            note_path = vault_path / "test.md"
            note_path.parent.mkdir(parents=True)
            note_path.write_text(note_content)
            
            yield vault_path
    
    def test_pkm_search_filters_by_file_type(self, vault_with_sample_notes):
        """
        RED TEST: Must fail - file type filtering not implemented
        
        Test Spec: Filter search by file patterns
        - --type daily searches only daily notes
        - --type project searches only project files
        - --ext md searches only markdown files
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import search_vault
            
        # Future validation:
        # results = search_vault("project", vault_path=vault_with_sample_notes, file_types=["project"])
        # for result in results.results:
        #     assert "01-projects" in str(result.filepath) or result.filepath.read_text().find('type: project') > -1
    
    def test_pkm_search_frontmatter_aware(self, vault_with_sample_notes):
        """
        RED TEST: Must fail - frontmatter search not implemented
        
        Test Spec: Search within frontmatter fields
        - tag:ai finds notes with "ai" tag
        - type:project finds project notes
        - date:2024-01 finds January 2024 notes
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import search_frontmatter
            
        # Future validation:
        # results = search_vault("tag:ai", vault_path=vault_with_sample_notes)
        # for result in results.results:
        #     frontmatter = extract_frontmatter(result.filepath)
        #     assert "ai" in frontmatter.get("tags", [])
    
    def test_pkm_search_regex_patterns(self, vault_with_sample_notes):
        """
        RED TEST: Must fail - regex search not implemented
        
        Test Spec: Regular expression search support
        - --regex flag enables regex mode
        - Validate regex patterns before search
        - Provide helpful error messages for invalid regex
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import search_vault
            
        # Future validation:
        # results = search_vault(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", vault_path=vault_with_sample_notes, regex=True)
        # # Should find proper nouns like "Natural Language"


class TestPkmSearchErrorHandling:
    """
    RED PHASE: Error handling specification
    Following KISS: Handle basic error cases gracefully
    """
    
    def test_pkm_search_empty_query(self):
        """
        RED TEST: Must fail - empty query handling not implemented
        
        Test Spec: Handle empty search queries
        - Empty string returns appropriate error
        - None query returns error
        - Whitespace-only query returns error
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import search_vault
            
        # Future validation:
        # result = search_vault("", vault_path=Path("/tmp"))
        # assert result.success is False
        # assert "empty" in result.error.lower()
    
    def test_pkm_search_nonexistent_vault(self):
        """
        RED TEST: Must fail - path validation not implemented
        
        Test Spec: Handle invalid vault paths
        - Non-existent directory returns error
        - Non-directory path returns error  
        - Permission denied handled gracefully
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import search_vault
            
        # Future validation:
        # result = search_vault("test", vault_path=Path("/nonexistent"))
        # assert result.success is False
        # assert "not found" in result.error.lower()
    
    def test_pkm_search_no_matching_files(self):
        """
        RED TEST: Must fail - no results handling not implemented
        
        Test Spec: Handle queries with no matches
        - Return success=True with empty results
        - Provide helpful message about search scope
        - Suggest alternative search terms
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            empty_vault = Path(tmpdir) / "vault"
            empty_vault.mkdir()
            
            with pytest.raises((ImportError, ModuleNotFoundError)):
                from src.pkm.search import search_vault
                
            # Future validation:
            # result = search_vault("nonexistent", vault_path=empty_vault)
            # assert result.success is True
            # assert len(result.results) == 0
            # assert result.total_matches == 0


class TestPkmSearchCommandLineInterface:
    """
    RED PHASE: CLI integration specification  
    Simple command interface for search functionality
    """
    
    def test_pkm_search_cli_command_not_implemented(self):
        """
        RED TEST: Must fail - CLI command not implemented
        
        Test Spec: Command-line search interface
        - /pkm-search "query" performs basic search
        - Results displayed in readable format
        - Exit code indicates success/failure
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.cli import search_command
        
        # Future CLI validation:
        # import subprocess
        # result = subprocess.run([
        #     "python", "-m", "src.pkm.cli", "search", "test query"
        # ], capture_output=True, text=True)
        # assert result.returncode == 0
        # assert "found" in result.stdout.lower()
    
    def test_pkm_search_cli_output_format(self):
        """
        RED TEST: Must fail - output formatting not implemented
        
        Test Spec: Readable CLI output format
        - Show filename and line number for each match
        - Highlight search terms in results
        - Display total match count
        - Limit results display (with --all flag to show more)
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import format_search_results
        
        # Future validation will test output formatting
    
    def test_pkm_search_cli_handles_special_characters(self):
        """
        RED TEST: Must fail - special character handling not implemented
        
        Test Spec: Handle special characters in queries
        - Escape shell special characters properly
        - Handle quotes within quoted queries
        - Support unicode characters in search
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import escape_search_query
        
        # Future validation for special character handling


# Quality Gates - TDD Compliance
class TestTddComplianceFr004:
    """
    Meta-tests to enforce TDD compliance for FR-004
    """
    
    def test_no_implementation_exists_fr004(self):
        """
        TDD Compliance: Verify RED phase for FR-004
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import search_vault
            
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import calculate_relevance_score
            
        assert True, "Confirmed: FR-004 in proper RED phase"
    
    def test_search_result_types_specification(self):
        """
        Verify search result data structures follow SOLID principles
        """
        # SearchResult should have clear, simple interface
        result_fields = SearchResult._fields
        required_fields = ['filepath', 'line_number', 'line_content', 'relevance_score']
        
        for field in required_fields:
            assert field in result_fields, f"SearchResult missing required field: {field}"
    
    def test_search_covers_all_acceptance_criteria(self):
        """
        Verify test coverage matches FR-004 acceptance criteria
        """
        test_methods = [method for method in dir(TestPkmSearchBasicFunctionality)
                       if method.startswith('test_')]
        
        # Must cover basic search functionality
        required_scenarios = [
            'text_matching',
            'case_insensitive', 
            'line_context',
            'ranks_results'
        ]
        
        for scenario in required_scenarios:
            assert any(scenario in method for method in test_methods), \
                f"Missing test coverage for scenario: {scenario}"


# Performance Requirements (NFR - To be implemented later)
class TestPkmSearchPerformanceRequirements:
    """
    RED PHASE: Performance requirements specification
    
    These are NON-FUNCTIONAL requirements - DEFER until FR-004 basic functionality works
    Following FR-First principle: implement user functionality before optimization
    """
    
    def test_search_performance_requirements_not_implemented_yet(self):
        """
        Performance requirements exist but are NOT prioritized yet
        
        Future performance targets (DEFER):
        - Search < 1000 notes in < 2 seconds
        - Memory usage < 100MB for typical vaults
        - Incremental search results streaming
        """
        # These tests should NOT be implemented until basic functionality works
        # This is an example of FR-First prioritization
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.search import SearchPerformanceOptimizer
        
        assert True, "Performance optimization correctly deferred (FR-First principle)"


# Implementation Guidance
"""
FR-004 Implementation Plan (Post-RED Phase):

GREEN PHASE - Minimal Implementation:
1. Create src/pkm/search.py with basic grep wrapper
2. Implement search_vault() function using simple text matching  
3. Add basic relevance scoring (match count based)
4. Create CLI command for /pkm-search
5. Handle basic error cases

Key Principles:
- KISS: Use grep/ripgrep for text search, no complex indexing
- SRP: Search function focused on finding text matches
- FR-First: Basic text search before advanced features like regex

REFACTOR PHASE:
1. Extract relevance scoring to separate function
2. Add configuration for search options
3. Improve result formatting and display
4. Add search result caching (simple)

DEFER UNTIL LATER (NFRs):
- Performance optimization for large vaults
- Full-text indexing systems
- Advanced query languages
- Real-time search suggestions

Success Criteria:
- All RED tests become GREEN
- Basic text search works across vault
- Results include useful context
- Simple relevance ranking functional
- CLI interface user-friendly
"""