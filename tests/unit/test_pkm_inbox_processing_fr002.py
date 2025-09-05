"""
TDD Tests for FR-002: Inbox Processing Command

RED PHASE - These tests MUST FAIL initially to enforce TDD workflow.

Test Specification:
- Given: Items exist in vault/00-inbox/
- When: User runs `/pkm-process-inbox`
- Then: Items categorized using simple keyword matching
- And: Items moved to appropriate PARA folders

Engineering Principles:
- TDD: Tests define specification before implementation
- KISS: Simple keyword matching only (no complex NLP)
- FR-First: Basic categorization before advanced AI
- DRY: Shared configuration for PARA categories
"""

import pytest
import tempfile
from pathlib import Path
from typing import NamedTuple, List, Dict
import yaml


# SOLID Principles: Interface Segregation
class ProcessingResult(NamedTuple):
    """Result of inbox processing operation"""
    processed_count: int
    categorized_items: List[str]
    moved_files: Dict[str, str]  # filename -> destination folder
    errors: List[str]
    success: bool


class ParaCategory(NamedTuple):
    """PARA categorization result"""
    category: str  # project, area, resource, archive
    confidence: float
    keywords_matched: List[str]
    destination_folder: str


# DRY Principle: Shared configuration
PARA_KEYWORDS = {
    'project': ['deadline', 'project', 'goal', 'complete', 'deliver', 'launch'],
    'area': ['maintain', 'standard', 'responsibility', 'ongoing', 'manage'],
    'resource': ['reference', 'learn', 'research', 'knowledge', 'resource'],
    'archive': ['completed', 'archived', 'old', 'finished', 'done']
}

PARA_FOLDERS = {
    'project': '01-projects',
    'area': '02-areas', 
    'resource': '03-resources',
    'archive': '04-archives'
}


class TestPkmInboxProcessingBasicFunctionality:
    """
    RED PHASE: All tests MUST FAIL initially
    
    Tests define specification for simple keyword-based categorization
    No complex NLP - just basic string matching (KISS principle)
    """
    
    @pytest.fixture
    def temp_vault_with_inbox_items(self):
        """Create vault with sample inbox items for processing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            
            # Create PARA folder structure
            for folder in PARA_FOLDERS.values():
                (vault_path / folder).mkdir(parents=True)
            
            inbox_path = vault_path / "00-inbox"
            inbox_path.mkdir(parents=True)
            
            # Create test inbox items with different content
            test_items = [
                ("project_item.md", "Need to complete project deadline next week"),
                ("area_item.md", "Standard maintenance responsibility for server"),
                ("resource_item.md", "Research paper on machine learning algorithms"),
                ("mixed_item.md", "This item has multiple keywords: project and resource")
            ]
            
            for filename, content in test_items:
                item_path = inbox_path / filename
                item_path.write_text(f"---\ndate: 2024-01-01\ntype: capture\n---\n{content}")
            
            yield vault_path
    
    def test_pkm_process_inbox_function_not_implemented_yet(self):
        """
        RED TEST: Must fail - no process_inbox function exists
        
        This test ensures we're in proper TDD RED phase
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.processor import process_inbox
    
    def test_pkm_process_inbox_basic_categorization(self, temp_vault_with_inbox_items):
        """
        RED TEST: Must fail - basic categorization not implemented
        
        Test Spec: Simple keyword matching categorizes items
        - Project keywords → 01-projects/
        - Area keywords → 02-areas/  
        - Resource keywords → 03-resources/
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.processor import process_inbox
            
        # Future test validation:
        # result = process_inbox(vault_path=temp_vault_with_inbox_items)
        # assert result.success is True
        # assert result.processed_count == 4
        # 
        # # Verify items moved to correct folders
        # project_folder = temp_vault_with_inbox_items / "01-projects"
        # assert (project_folder / "project_item.md").exists()
        # 
        # resource_folder = temp_vault_with_inbox_items / "03-resources"  
        # assert (resource_folder / "resource_item.md").exists()
    
    def test_pkm_process_inbox_keyword_matching_algorithm(self, temp_vault_with_inbox_items):
        """
        RED TEST: Must fail - keyword matching not implemented
        
        Test Spec: Simple keyword matching logic
        - Case-insensitive matching
        - Highest keyword count wins
        - Ties go to first match in priority order
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.processor import categorize_content
            
        # Future validation:
        # category = categorize_content("This is a project deadline")
        # assert category.category == "project"
        # assert "deadline" in category.keywords_matched
        # assert category.confidence > 0
    
    def test_pkm_process_inbox_handles_mixed_keywords(self, temp_vault_with_inbox_items):
        """
        RED TEST: Must fail - mixed keyword handling not implemented
        
        Test Spec: Items with multiple category keywords
        - Count keywords per category
        - Choose category with most matches
        - Report confidence level
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.processor import categorize_content
            
        # Future validation for mixed keywords:
        # content = "This project needs research resources for completion"
        # category = categorize_content(content)
        # # Should choose 'project' (2 matches: project, completion)
        # # over 'resource' (1 match: research)
        # assert category.category == "project"
        # assert category.confidence > 0.5
    
    def test_pkm_process_inbox_preserves_frontmatter(self, temp_vault_with_inbox_items):
        """
        RED TEST: Must fail - frontmatter preservation not implemented
        
        Test Spec: Original frontmatter preserved during move
        - Original metadata maintained
        - Add processing metadata
        - Update file location references
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.processor import process_inbox
            
        # Future validation:
        # result = process_inbox(vault_path=temp_vault_with_inbox_items)
        # 
        # # Check that moved file maintains original frontmatter
        # moved_file = temp_vault_with_inbox_items / "01-projects" / "project_item.md"
        # content = moved_file.read_text()
        # frontmatter = yaml.safe_load_all(content).__next__()
        # assert frontmatter["type"] == "capture"  # Original preserved
        # assert "processed_date" in frontmatter  # Processing metadata added


class TestPkmInboxProcessingErrorHandling:
    """
    RED PHASE: Error handling specification
    Following KISS: Simple error cases first
    """
    
    @pytest.fixture 
    def empty_vault(self):
        """Vault with no inbox items"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            (vault_path / "00-inbox").mkdir(parents=True)
            yield vault_path
    
    def test_pkm_process_empty_inbox(self, empty_vault):
        """
        RED TEST: Must fail - empty inbox handling not implemented
        
        Test Spec: Gracefully handle empty inbox
        - Return success with zero processed count
        - No errors reported
        - Appropriate user message
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.processor import process_inbox
            
        # Future validation:
        # result = process_inbox(vault_path=empty_vault)
        # assert result.success is True
        # assert result.processed_count == 0
        # assert len(result.errors) == 0
    
    def test_pkm_process_inbox_missing_para_folders(self):
        """
        RED TEST: Must fail - folder creation not implemented
        
        Test Spec: Create missing PARA folders
        - Auto-create missing destination folders
        - Maintain folder structure integrity
        - Log folder creation actions
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            inbox_path = vault_path / "00-inbox"
            inbox_path.mkdir(parents=True)
            
            # Create test item but no destination folders
            (inbox_path / "test.md").write_text("Project item needs deadline")
            
            with pytest.raises((ImportError, ModuleNotFoundError)):
                from src.pkm.processor import process_inbox
                
            # Future validation:
            # result = process_inbox(vault_path=vault_path)
            # assert (vault_path / "01-projects").exists()
            # assert result.success is True
    
    def test_pkm_process_uncategorizable_items(self, empty_vault):
        """
        RED TEST: Must fail - uncategorizable item handling not implemented
        
        Test Spec: Handle items with no matching keywords
        - Keep items in inbox with flag
        - Add metadata indicating categorization failure
        - Suggest manual categorization
        """
        inbox_path = empty_vault / "00-inbox"
        (inbox_path / "unclear.md").write_text("Random text with no category keywords")
        
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.processor import process_inbox
            
        # Future validation:
        # result = process_inbox(vault_path=empty_vault)
        # assert (inbox_path / "unclear.md").exists()  # Still in inbox
        # assert "unclear.md" in result.errors  # Flagged as uncategorizable


class TestPkmInboxProcessingCommandLineInterface:
    """
    RED PHASE: CLI integration tests
    Command-line interface for inbox processing
    """
    
    def test_pkm_process_inbox_cli_command(self):
        """
        RED TEST: Must fail - CLI command not implemented
        
        Test Spec: Command line interface
        - /pkm-process-inbox processes current vault
        - Returns summary of processing results
        - Handles vault path discovery
        """
        import subprocess
        
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.cli import process_inbox_command
        
        # Future CLI test:
        # result = subprocess.run([
        #     "python", "-m", "src.pkm.cli",
        #     "process-inbox"
        # ], capture_output=True, text=True)
        # assert "processed" in result.stdout.lower()


# Quality Gates - TDD Compliance
class TestTddComplianceFr002:
    """
    Meta-tests to enforce TDD compliance for FR-002
    """
    
    def test_no_implementation_exists_fr002(self):
        """
        TDD Compliance: Verify RED phase for FR-002
        
        Must confirm no implementation exists before writing code
        """
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.processor import process_inbox
            
        with pytest.raises((ImportError, ModuleNotFoundError)):
            from src.pkm.processor import categorize_content
            
        assert True, "Confirmed: FR-002 in proper RED phase"
    
    def test_para_keywords_configuration_exists(self):
        """
        Verify PARA keyword configuration follows DRY principle
        
        Keywords should be centrally configured, not hardcoded
        """
        # Configuration exists in this test file as specification
        assert 'project' in PARA_KEYWORDS
        assert 'area' in PARA_KEYWORDS
        assert 'resource' in PARA_KEYWORDS
        assert 'archive' in PARA_KEYWORDS
        
        # Verify corresponding folders exist
        assert len(PARA_KEYWORDS) == len(PARA_FOLDERS)


# Implementation Guidance
"""
FR-002 Implementation Plan (Post-RED Phase):

GREEN PHASE - Minimal Implementation:
1. Create src/pkm/processor.py with basic keyword matching
2. Implement simple categorize_content() function  
3. Add process_inbox() function for batch processing
4. Create CLI command for /pkm-process-inbox

Key Principles:
- KISS: Simple string matching, no NLP complexity
- DRY: Centralized PARA keyword configuration
- FR-First: User functionality before optimization

REFACTOR PHASE:
1. Extract keyword matching to separate class
2. Add confidence scoring
3. Improve error handling and logging
4. Add configuration file support

Success Criteria:
- All RED tests become GREEN
- Keyword matching works reliably
- Files moved to correct PARA folders
- Simple CLI interface functional
"""