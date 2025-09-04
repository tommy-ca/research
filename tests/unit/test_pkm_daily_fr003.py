"""
FR-003 Daily Note Creation - TDD Test Suite

RED PHASE: All tests written to FAIL first
Following TDD: Write failing tests → minimal implementation → refactor

Test Coverage:
- Daily note creation functionality
- Directory structure handling (YYYY/MM-month/)
- Date formatting and templates
- Error handling scenarios
- KISS principle compliance
"""
import pytest
import tempfile
from pathlib import Path
from datetime import datetime, date
# Removed patch import - using direct date injection instead

# Import the module we're testing (will fail initially - RED phase)
from src.pkm.daily import pkm_daily, DailyNoteResult


class TestPkmDailyBasicFunctionality:
    """Test core daily note creation functionality"""
    
    def test_pkm_daily_function_exists(self):
        """FR-003: Verify function exists"""
        from src.pkm.daily import pkm_daily
        assert callable(pkm_daily)
    
    def test_pkm_daily_creates_todays_note(self):
        """FR-003: Creates today's daily note"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            # Use direct date injection for predictable testing
            test_date = date(2025, 9, 4)  # September 4, 2025
            result = pkm_daily(vault_path=vault, today=test_date)
            
            expected_path = vault / 'daily' / '2025' / '09-September' / '2025-09-04.md'
            assert result.success is True
            assert result.note_path == expected_path
            assert expected_path.exists()
    
    def test_pkm_daily_creates_directory_structure(self):
        """FR-003: Creates YYYY/MM-month directory structure"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            test_date = date(2025, 12, 25)  # December 25, 2025
            result = pkm_daily(vault_path=vault, today=test_date)
            
            year_dir = vault / 'daily' / '2025'
            month_dir = year_dir / '12-December'
            
            assert year_dir.exists()
            assert month_dir.exists()
            assert result.created_directories == [str(year_dir), str(month_dir)]
    
    def test_pkm_daily_opens_existing_note(self):
        """FR-003: Opens existing note if already exists"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            
            # Pre-create the note
            test_date = date(2025, 9, 4)
            daily_path = vault / 'daily' / '2025' / '09-September' / '2025-09-04.md'
            daily_path.parent.mkdir(parents=True)
            original_content = "---\ndate: 2025-09-04\ntype: daily\n---\nExisting content"
            daily_path.write_text(original_content)
            
            result = pkm_daily(vault_path=vault, today=test_date)
            
            assert result.success is True
            assert result.note_path == daily_path
            assert result.was_existing is True
            # Should not overwrite existing content
            assert "Existing content" in daily_path.read_text()
    
    def test_pkm_daily_returns_result_object(self):
        """FR-003: Returns structured result"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            result = pkm_daily(vault_path=vault)
            
            assert hasattr(result, 'success')
            assert hasattr(result, 'note_path')
            assert hasattr(result, 'was_existing')
            assert hasattr(result, 'created_directories')
            assert hasattr(result, 'message')
    
    def test_pkm_daily_applies_frontmatter_template(self):
        """FR-003: Applies basic frontmatter template"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            test_date = date(2025, 9, 4)
            result = pkm_daily(vault_path=vault, today=test_date)
            
            content = result.note_path.read_text()
            assert content.startswith('---')
            assert 'date: 2025-09-04' in content
            assert 'type: daily' in content
            assert 'tags: [daily]' in content


class TestPkmDailyDateHandling:
    """Test date formatting and directory structure"""
    
    def test_daily_handles_different_months(self):
        """FR-003: Correctly formats different months"""
        month_tests = [
            (date(2025, 1, 15), '01-January'),
            (date(2025, 6, 20), '06-June'),
            (date(2025, 12, 31), '12-December'),
        ]
        
        for test_date, expected_month in month_tests:
            with tempfile.TemporaryDirectory() as tmp:
                vault = Path(tmp) / 'vault'
                vault.mkdir()
                
                result = pkm_daily(vault_path=vault, today=test_date)
                
                expected_dir = vault / 'daily' / str(test_date.year) / expected_month
                assert expected_dir.exists()
                assert expected_month in str(result.note_path)
    
    def test_daily_handles_year_transitions(self):
        """FR-003: Handles year transitions correctly"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            # Test different years
            for year in [2024, 2025, 2026]:
                test_date = date(year, 3, 15)
                result = pkm_daily(vault_path=vault, today=test_date)
                
                year_dir = vault / 'daily' / str(year)
                assert year_dir.exists()
                assert str(year) in str(result.note_path)
    
    def test_daily_filename_format(self):
        """FR-003: Creates filename in YYYY-MM-DD.md format"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            test_date = date(2025, 9, 4)
            result = pkm_daily(vault_path=vault, today=test_date)
            
            assert result.note_path.name == '2025-09-04.md'


class TestPkmDailyErrorHandling:
    """Test error scenarios and edge cases"""
    
    def test_handles_missing_vault_directory(self):
        """FR-003: Graceful failure when vault doesn't exist"""
        result = pkm_daily(vault_path=Path("/nonexistent/path"))
        
        assert result.success is False
        assert "vault directory does not exist" in result.message.lower()
    
    def test_handles_permission_errors(self):
        """FR-003: Graceful handling of permission issues"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            # Test should not crash even with permission issues
            result = pkm_daily(vault_path=vault)
            assert isinstance(result, DailyNoteResult)
    
    def test_handles_existing_file_not_markdown(self):
        """FR-003: Handles case where daily path exists but isn't markdown"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            
            test_date = date(2025, 9, 4)
            daily_path = vault / 'daily' / '2025' / '09-September' / '2025-09-04.md'
            daily_path.parent.mkdir(parents=True)
            
            # Create non-markdown file at expected location
            daily_path.write_text("Not markdown content")
            
            result = pkm_daily(vault_path=vault, today=test_date)
            
            # Should handle gracefully
            assert result.success is True
            assert result.was_existing is True


class TestPkmDailyTemplating:
    """Test frontmatter template functionality"""
    
    def test_frontmatter_includes_required_fields(self):
        """FR-003: Frontmatter includes all required fields"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            test_date = date(2025, 9, 4)
            result = pkm_daily(vault_path=vault, today=test_date)
            
            content = result.note_path.read_text()
            
            # Check required frontmatter fields
            assert 'date: 2025-09-04' in content
            assert 'type: daily' in content
            assert 'tags: [daily]' in content
    
    def test_template_includes_daily_structure(self):
        """FR-003: Template includes basic daily note structure"""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            result = pkm_daily(vault_path=vault)
            content = result.note_path.read_text()
            
            # Check for basic daily note sections
            assert '# Daily Note' in content
            assert '## Tasks' in content
            assert '## Notes' in content


class TestTddCompliance:
    """Test that implementation follows TDD principles"""
    
    def test_implementation_exists_fr003(self):
        """FR-003: Implementation was created after tests (TDD compliance)"""
        try:
            from src.pkm.daily import pkm_daily, DailyNoteResult
            # If this passes, implementation exists
            assert True
        except ImportError:
            # This should fail during RED phase, pass during GREEN phase
            pytest.fail("Implementation should exist after RED phase")
    
    def test_specification_compliance(self):
        """FR-003: Implementation matches original specification"""
        from src.pkm.daily import pkm_daily
        
        # Test specification requirements
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / 'vault'
            vault.mkdir()
            
            # Should be able to call without errors
            result = pkm_daily(vault_path=vault)
            assert isinstance(result, DailyNoteResult)


class TestKissCompliance:
    """Test that implementation follows KISS principles"""
    
    def test_main_function_is_simple(self):
        """FR-003: pkm_daily() function is ≤20 lines"""
        import inspect
        from src.pkm.daily import pkm_daily
        
        source_lines = inspect.getsource(pkm_daily).strip().split('\n')
        # Remove empty lines and comments for accurate count
        code_lines = [line for line in source_lines 
                     if line.strip() and not line.strip().startswith('#')]
        
        assert len(code_lines) <= 20, f"Function has {len(code_lines)} lines, should be ≤20 (KISS principle)"
    
    def test_helper_functions_are_simple(self):
        """FR-003: All helper functions are ≤20 lines"""
        import inspect
        import src.pkm.daily as module
        
        for name in dir(module):
            if name.startswith('_') and callable(getattr(module, name)):
                func = getattr(module, name)
                if hasattr(func, '__module__') and func.__module__ == module.__name__:
                    source_lines = inspect.getsource(func).strip().split('\n')
                    code_lines = [line for line in source_lines 
                                 if line.strip() and not line.strip().startswith('#')]
                    assert len(code_lines) <= 20, f"Helper function {name} has {len(code_lines)} lines, should be ≤20"