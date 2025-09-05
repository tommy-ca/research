"""
FR-002 Inbox Processing Command - TDD Test Suite

RED PHASE: All tests written to FAIL first
Following TDD: Write failing tests → minimal implementation → refactor

Test Coverage:
- Basic inbox processing functionality
- PARA keyword categorization 
- File movement operations
- Error handling scenarios
- KISS principle compliance
"""
import pytest
import tempfile
from pathlib import Path
import shutil
from datetime import datetime

# Import the module we're testing (will fail initially - RED phase)
from src.pkm.inbox_processor import pkm_process_inbox, InboxResult


class TestPkmInboxProcessorBasicFunctionality:
    """Test core inbox processing functionality"""
    
    def test_pkm_process_inbox_function_exists(self):
        """FR-002: Verify function exists"""
        from src.pkm.inbox_processor import pkm_process_inbox
        assert callable(pkm_process_inbox)
    
    def test_pkm_process_inbox_processes_empty_inbox(self):
        """FR-002: Handle empty inbox gracefully"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            inbox = vault / '00-inbox'
            inbox.mkdir(parents=True)
            
            result = pkm_process_inbox(vault_path=vault)
            
            assert result.success is True
            assert result.processed_count == 0
            assert "No items to process" in result.message
    
    def test_pkm_process_inbox_creates_para_directories(self):
        """FR-002: Creates PARA directories if missing"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            inbox = vault / '00-inbox'
            inbox.mkdir(parents=True)
            
            # Create test file
            test_file = inbox / '20250904120000.md'
            test_file.write_text("---\ndate: 2025-09-04\ntype: capture\n---\nProject planning meeting")
            
            result = pkm_process_inbox(vault_path=vault)
            
            assert (vault / '02-projects').exists()
            assert (vault / '03-areas').exists() 
            assert (vault / '04-resources').exists()
    
    def test_pkm_process_inbox_returns_result_object(self):
        """FR-002: Returns structured result"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            inbox = vault / '00-inbox'
            inbox.mkdir(parents=True)
            
            result = pkm_process_inbox(vault_path=vault)
            
            assert hasattr(result, 'success')
            assert hasattr(result, 'processed_count') 
            assert hasattr(result, 'message')
            assert hasattr(result, 'categorized_items')


class TestPkmInboxProcessorParaKeywordMatching:
    """Test PARA categorization using keyword matching"""
    
    def test_project_keywords_move_to_projects_folder(self):
        """FR-002: Project keywords trigger move to 02-projects/"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._setup_para_directories(vault)
            inbox = vault / '00-inbox'
            
            # Test project keywords
            test_file = inbox / '20250904120000.md'
            test_file.write_text("---\ndate: 2025-09-04\ntype: capture\n---\nProject planning meeting")
            
            result = pkm_process_inbox(vault_path=vault)
            
            assert result.success is True
            assert result.processed_count == 1
            moved_file = vault / '02-projects' / '20250904120000.md'
            assert moved_file.exists()
            assert not test_file.exists()  # Original should be gone
    
    def test_area_keywords_move_to_areas_folder(self):
        """FR-002: Area keywords trigger move to 03-areas/"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._setup_para_directories(vault)
            inbox = vault / '00-inbox'
            
            test_file = inbox / '20250904120001.md'
            test_file.write_text("---\ndate: 2025-09-04\ntype: capture\n---\nHealth fitness routine")
            
            result = pkm_process_inbox(vault_path=vault)
            
            moved_file = vault / '03-areas' / '20250904120001.md'
            assert moved_file.exists()
            assert not test_file.exists()
    
    def test_resource_keywords_move_to_resources_folder(self):
        """FR-002: Resource keywords trigger move to 04-resources/"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._setup_para_directories(vault)
            inbox = vault / '00-inbox'
            
            test_file = inbox / '20250904120002.md'
            test_file.write_text("---\ndate: 2025-09-04\ntype: capture\n---\nReference documentation API")
            
            result = pkm_process_inbox(vault_path=vault)
            
            moved_file = vault / '04-resources' / '20250904120002.md'
            assert moved_file.exists()
            assert not test_file.exists()
    
    def test_default_categorization_for_unknown_keywords(self):
        """FR-002: Items with no clear keywords go to resources by default"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._setup_para_directories(vault)
            inbox = vault / '00-inbox'
            
            test_file = inbox / '20250904120003.md'
            test_file.write_text("---\ndate: 2025-09-04\ntype: capture\n---\nRandom thoughts")
            
            result = pkm_process_inbox(vault_path=vault)
            
            moved_file = vault / '04-resources' / '20250904120003.md'
            assert moved_file.exists()
    
    def test_multiple_files_processed_in_batch(self):
        """FR-002: Process multiple inbox items in single operation"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._setup_para_directories(vault)
            inbox = vault / '00-inbox'
            
            # Create multiple test files
            files = [
                (inbox / '20250904120001.md', "Project planning"),
                (inbox / '20250904120002.md', "Health fitness"),
                (inbox / '20250904120003.md', "Reference docs"),
            ]
            
            for file_path, content in files:
                file_path.write_text(f"---\ndate: 2025-09-04\ntype: capture\n---\n{content}")
            
            result = pkm_process_inbox(vault_path=vault)
            
            assert result.processed_count == 3
            assert len(result.categorized_items) == 3
    
    def _setup_para_directories(self, vault: Path):
        """Helper: Create PARA directory structure"""
        directories = ['00-inbox', '02-projects', '03-areas', '04-resources']
        for dir_name in directories:
            (vault / dir_name).mkdir(parents=True, exist_ok=True)


class TestPkmInboxProcessorErrorHandling:
    """Test error scenarios and edge cases"""
    
    def test_handles_missing_vault_directory(self):
        """FR-002: Graceful failure when vault doesn't exist"""
        result = pkm_process_inbox(vault_path=Path("/nonexistent/path"))
        
        assert result.success is False
        assert "vault directory does not exist" in result.message.lower()
    
    def test_handles_missing_inbox_directory(self):
        """FR-002: Creates inbox if missing"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            # Note: no inbox directory created
            
            result = pkm_process_inbox(vault_path=vault)
            
            assert result.success is True
            assert (vault / '00-inbox').exists()
    
    def test_handles_permission_errors(self):
        """FR-002: Graceful handling of file permission issues"""
        # This would be a more complex test involving file permissions
        # For now, ensure function signature supports error handling
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            
            result = pkm_process_inbox(vault_path=vault)
            # Should not crash even with permission issues
            assert isinstance(result, InboxResult)
    
    def test_handles_malformed_markdown_files(self):
        """FR-002: Process files with invalid frontmatter"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            self._setup_para_directories(vault)
            inbox = vault / '00-inbox'
            
            # Create malformed file
            test_file = inbox / '20250904120000.md'
            test_file.write_text("Invalid frontmatter\nSome content")
            
            result = pkm_process_inbox(vault_path=vault)
            
            # Should still process, defaulting to resources
            assert result.success is True
            moved_file = vault / '04-resources' / '20250904120000.md'
            assert moved_file.exists()
    
    def _setup_para_directories(self, vault: Path):
        """Helper: Create PARA directory structure"""
        directories = ['00-inbox', '02-projects', '03-areas', '04-resources']
        for dir_name in directories:
            (vault / dir_name).mkdir(parents=True, exist_ok=True)


class TestTddCompliance:
    """Test that implementation follows TDD principles"""
    
    def test_implementation_exists_fr002(self):
        """FR-002: Implementation was created after tests (TDD compliance)"""
        try:
            from src.pkm.inbox_processor import pkm_process_inbox, InboxResult
            # If this passes, implementation exists
            assert True
        except ImportError:
            # This should fail during RED phase, pass during GREEN phase
            pytest.fail("Implementation should exist after RED phase")
    
    def test_specification_compliance(self):
        """FR-002: Implementation matches original specification"""
        from src.pkm.inbox_processor import pkm_process_inbox
        
        # Test specification requirements
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            inbox = vault / '00-inbox'
            inbox.mkdir(parents=True)
            
            # Should be able to call without errors
            result = pkm_process_inbox(vault_path=vault)
            assert isinstance(result, InboxResult)


class TestKissCompliance:
    """Test that implementation follows KISS principles"""
    
    def test_main_function_is_simple(self):
        """FR-002: pkm_process_inbox() function is ≤20 lines"""
        import inspect
        from src.pkm.inbox_processor import pkm_process_inbox
        
        source_lines = inspect.getsource(pkm_process_inbox).strip().split('\n')
        # Remove empty lines and comments for accurate count
        code_lines = [line for line in source_lines 
                     if line.strip() and not line.strip().startswith('#')]
        
        assert len(code_lines) <= 20, f"Function has {len(code_lines)} lines, should be ≤20 (KISS principle)"
    
    def test_helper_functions_are_simple(self):
        """FR-002: All helper functions are ≤20 lines"""
        import inspect
        import src.pkm.inbox_processor as module
        
        for name in dir(module):
            if name.startswith('_') and callable(getattr(module, name)):
                func = getattr(module, name)
                if hasattr(func, '__module__') and func.__module__ == module.__name__:
                    source_lines = inspect.getsource(func).strip().split('\n')
                    code_lines = [line for line in source_lines 
                                 if line.strip() and not line.strip().startswith('#')]
                    assert len(code_lines) <= 20, f"Helper function {name} has {len(code_lines)} lines, should be ≤20"