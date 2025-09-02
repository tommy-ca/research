"""
TDD Tests for PKM CLI Module

GREEN PHASE - These tests validate CLI functionality
Following TDD principles and KISS simplicity
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch
import sys

# Import the CLI module
from src.pkm.cli import capture_command, _handle_capture_command, _handle_unknown_command


class TestPkmCliBasicFunctionality:
    """Test basic CLI functionality"""
    
    def test_capture_command_function_works(self):
        """Test capture_command function returns boolean"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            result = capture_command("Test content", vault_path=vault_path)
            assert isinstance(result, bool)
            assert result is True
    
    def test_capture_command_creates_file(self):
        """Test capture_command creates actual file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir)
            success = capture_command("Test CLI content", vault_path=vault_path)
            
            assert success is True
            inbox_path = vault_path / "00-inbox"
            assert inbox_path.exists()
            
            files = list(inbox_path.glob("*.md"))
            assert len(files) == 1
            assert "Test CLI content" in files[0].read_text()


class TestPkmCliHelperFunctions:
    """Test CLI helper functions for KISS compliance"""
    
    def test_handle_unknown_command_exits(self):
        """Test unknown command handler exits with error"""
        with patch('builtins.print') as mock_print:
            with patch('sys.exit') as mock_exit:
                _handle_unknown_command("unknown")
                
                mock_print.assert_called_with("Unknown command: unknown")
                mock_exit.assert_called_with(1)
    
    def test_handle_capture_command_validates_content(self):
        """Test capture command validates None content"""
        with patch('builtins.print') as mock_print:
            with patch('sys.exit') as mock_exit:
                _handle_capture_command(None)
                
                # Should print an error message and exit with code 1
                mock_exit.assert_called_with(1)
                # Check that an error was printed (exact message may vary)
                args = mock_print.call_args[0]
                assert "Error:" in args[0]
    
    def test_handle_capture_command_handles_empty_content(self):
        """Test capture command handles empty content (creates placeholder)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('src.pkm.cli.Path.cwd', return_value=Path(tmpdir)):
                with patch('builtins.print') as mock_print:
                    with patch('sys.exit') as mock_exit:
                        _handle_capture_command("")
                        
                        # Should succeed (empty content gets placeholder)
                        mock_exit.assert_called_with(0)
                        # Should print success message
                        args = mock_print.call_args[0] 
                        assert "Content captured successfully" in args[0]


class TestTddCompliance:
    """TDD compliance tests for CLI module"""
    
    def test_cli_functions_exist(self):
        """Test that all CLI functions exist and are callable"""
        from src.pkm.cli import main, capture_command
        
        assert callable(main)
        assert callable(capture_command)
        
    def test_cli_helper_functions_exist(self):
        """Test that helper functions exist for KISS compliance"""
        from src.pkm.cli import _handle_capture_command, _handle_unknown_command
        
        assert callable(_handle_capture_command)
        assert callable(_handle_unknown_command)


class TestKissCompliance:
    """KISS principle compliance tests"""
    
    def test_main_function_is_simple(self):
        """Test that main function follows KISS principle"""
        import inspect
        from src.pkm.cli import main
        
        # Get source code and count lines
        source_lines = inspect.getsource(main).split('\n')
        code_lines = [line for line in source_lines 
                     if line.strip() and not line.strip().startswith('#')]
        
        # Should be under 20 lines (KISS compliance)
        assert len(code_lines) <= 20, f"main() has {len(code_lines)} lines, should be ≤20"
    
    def test_helper_functions_are_simple(self):
        """Test that helper functions follow KISS principle"""
        import inspect
        from src.pkm.cli import _handle_capture_command, _handle_unknown_command
        
        # Check each helper function
        for func in [_handle_capture_command, _handle_unknown_command]:
            source_lines = inspect.getsource(func).split('\n')
            code_lines = [line for line in source_lines 
                         if line.strip() and not line.strip().startswith('#')]
            
            assert len(code_lines) <= 20, f"{func.__name__}() has {len(code_lines)} lines, should be ≤20"