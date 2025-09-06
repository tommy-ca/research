"""
PKM Agent System - Foundation Infrastructure Tests
Task Group 1: TDD RED Phase - Repository Structure and Base Components

TDD RED Phase: Comprehensive test suite defining expected behavior
All tests written BEFORE implementation - they should FAIL initially

Following TDD methodology:
1. RED: Write failing test first (THIS FILE)
2. GREEN: Write minimal code to pass
3. REFACTOR: Improve code while tests pass

Task 1.1-1.6: Foundation Infrastructure Requirements
"""

import pytest
from pathlib import Path
from typing import List, Dict, Any, Optional
import tempfile
import os
from unittest.mock import Mock, patch
from abc import ABC, abstractmethod

# Import will fail initially - this is expected in RED phase
try:
    from src.pkm.agents.base import BaseCommandHandler, CommandArgs, CommandResult
    from src.pkm.agents.router import PkmCommandRouter
    from src.pkm.agents.vault_manager import VaultManager
    from src.pkm.validators.runner import PKMValidationRunner
except ImportError:
    # Expected during RED phase - classes don't exist yet
    BaseCommandHandler = None
    CommandArgs = None
    CommandResult = None
    PkmCommandRouter = None
    VaultManager = None
    PKMValidationRunner = None


class TestPkmAgentRepositoryStructure:
    """
    Task 1.1: Repository structure setup
    Tests for proper directory creation and organization
    """
    
    def test_claude_agents_directory_exists(self):
        """Task 1.1.1: Test .claude/agents/ directory structure"""
        expected_agents_dir = Path(".claude/agents")
        
        # This will fail initially - directory doesn't exist
        assert expected_agents_dir.exists(), f"PKM agents directory should exist at {expected_agents_dir}"
        assert expected_agents_dir.is_dir(), f"PKM agents path should be a directory"
    
    def test_pkm_agent_handler_directories_exist(self):
        """Task 1.1.2: Test PKM agent handler organization"""
        base_agents_dir = Path(".claude/agents")
        
        expected_handlers = [
            "daily_note",      # FR-AGENT-001: Daily note management
            "capture",         # FR-AGENT-002: Content capture
            "retrieval",       # FR-AGENT-003: Note retrieval  
            "search",          # FR-AGENT-004: Content search
            "process_inbox",   # FR-AGENT-005: Inbox processing
            "link_management", # FR-AGENT-006: Link management
            "templates",       # FR-AGENT-007: Template system
            "analytics"        # FR-AGENT-008: Analytics dashboard
        ]
        
        for handler_name in expected_handlers:
            handler_dir = base_agents_dir / handler_name
            assert handler_dir.exists(), f"Handler directory should exist: {handler_dir}"
            assert handler_dir.is_dir(), f"Handler path should be a directory: {handler_dir}"
    
    def test_pkm_source_directory_structure(self):
        """Task 1.1.3: Test src/pkm/agents/ source code organization"""
        base_src_dir = Path("src/pkm/agents")
        
        expected_structure = [
            "__init__.py",
            "base.py",          # BaseCommandHandler and interfaces
            "router.py",        # PkmCommandRouter
            "vault_manager.py", # VaultManager integration
        ]
        
        assert base_src_dir.exists(), f"Source directory should exist: {base_src_dir}"
        
        for expected_file in expected_structure:
            expected_path = base_src_dir / expected_file
            assert expected_path.exists(), f"Expected source file should exist: {expected_path}"


class TestBaseCommandHandler:
    """
    Task 1.2: Base command handler interface
    Tests for abstract base class definition and behavior
    """
    
    def test_base_command_handler_is_abstract(self):
        """Task 1.2.1: BaseCommandHandler should be abstract class"""
        # This will fail initially - BaseCommandHandler doesn't exist
        assert BaseCommandHandler is not None, "BaseCommandHandler class should exist"
        
        # Should not be able to instantiate abstract class directly
        with pytest.raises(TypeError):
            BaseCommandHandler()
    
    def test_base_command_handler_has_required_abstract_methods(self):
        """Task 1.2.2: BaseCommandHandler should have required abstract methods"""
        assert hasattr(BaseCommandHandler, 'handle'), "BaseCommandHandler should have handle() method"
        assert hasattr(BaseCommandHandler, 'validate_args'), "BaseCommandHandler should have validate_args() method"
        
        # Methods should be abstract
        from inspect import isabstract
        assert isabstract(BaseCommandHandler), "BaseCommandHandler should be abstract"
    
    def test_command_args_data_structure(self):
        """Task 1.2.3: CommandArgs should be proper data structure"""
        assert CommandArgs is not None, "CommandArgs class should exist"
        
        # Should be able to create CommandArgs with required fields
        test_args = CommandArgs(
            command="test",
            content="test content",
            options={"tag": "test"},
            vault_path=Path("/test/vault")
        )
        
        assert test_args.command == "test"
        assert test_args.content == "test content"
        assert test_args.options == {"tag": "test"}
        assert test_args.vault_path == Path("/test/vault")
    
    def test_command_result_data_structure(self):
        """Task 1.2.4: CommandResult should be proper data structure"""
        assert CommandResult is not None, "CommandResult class should exist"
        
        # Should be able to create CommandResult with required fields
        test_result = CommandResult(
            success=True,
            message="Test successful",
            data={"created_file": "test.md"},
            validation_results=[]
        )
        
        assert test_result.success == True
        assert test_result.message == "Test successful"
        assert test_result.data == {"created_file": "test.md"}
        assert test_result.validation_results == []


class TestPkmCommandRouter:
    """
    Task 1.3: Command routing architecture
    Tests for command routing and handler management
    """
    
    def setup_method(self):
        """Setup test environment with mock vault"""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        self.vault_path.mkdir(parents=True)
        
    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_pkm_command_router_initialization(self):
        """Task 1.3.1: PkmCommandRouter should initialize properly"""
        assert PkmCommandRouter is not None, "PkmCommandRouter class should exist"
        
        router = PkmCommandRouter(self.vault_path)
        
        assert router.vault_path == self.vault_path
        assert hasattr(router, 'handlers'), "Router should have handlers registry"
        assert isinstance(router.handlers, dict), "Handlers should be dictionary"
    
    def test_command_routing_to_handlers(self):
        """Task 1.3.2: Router should route commands to appropriate handlers"""
        router = PkmCommandRouter(self.vault_path)
        
        # Test command routing mapping
        expected_routes = {
            "daily": "daily_note",
            "capture": "capture", 
            "get": "retrieval",
            "search": "search",
            "process-inbox": "process_inbox",
            "links": "link_management",
            "template": "templates",
            "stats": "analytics"
        }
        
        for command, expected_handler in expected_routes.items():
            handler = router.get_handler(command)
            assert handler is not None, f"Handler should exist for command: {command}"
            assert handler.handler_type == expected_handler, f"Handler type should match for {command}"
    
    def test_router_handles_unknown_commands(self):
        """Task 1.3.3: Router should handle unknown commands gracefully"""
        router = PkmCommandRouter(self.vault_path)
        
        with pytest.raises(ValueError) as exc_info:
            router.get_handler("unknown-command")
        
        assert "unknown command" in str(exc_info.value).lower()
        assert "unknown-command" in str(exc_info.value)
    
    def test_router_validation_integration(self):
        """Task 1.3.4: Router should integrate with validation system"""
        # Mock validation runner
        mock_validator_runner = Mock(spec=PKMValidationRunner)
        
        router = PkmCommandRouter(self.vault_path, validator_runner=mock_validator_runner)
        
        assert router.validator_runner == mock_validator_runner
        assert hasattr(router, 'validate_operation'), "Router should have validation method"


class TestVaultManagerIntegration:
    """
    Task 1.4-1.6: Vault manager and validation system integration
    Tests for vault operations with validation integration
    """
    
    def setup_method(self):
        """Setup test environment with vault structure"""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        
        # Create standard PKM vault structure
        vault_dirs = [
            "00-inbox",
            "01-projects", 
            "02-areas",
            "03-resources",
            "04-archives",
            "daily",
            "permanent/notes",
            "templates"
        ]
        
        for dir_path in vault_dirs:
            (self.vault_path / dir_path).mkdir(parents=True)
    
    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_vault_manager_initialization(self):
        """Task 1.4.1: VaultManager should initialize with validation integration"""
        assert VaultManager is not None, "VaultManager class should exist"
        
        # Mock validation runner
        mock_validator_runner = Mock(spec=PKMValidationRunner)
        
        vault_manager = VaultManager(self.vault_path, mock_validator_runner)
        
        assert vault_manager.vault_path == self.vault_path
        assert vault_manager.validator_runner == mock_validator_runner
    
    def test_vault_structure_validation(self):
        """Task 1.4.2: VaultManager should validate vault structure"""
        mock_validator_runner = Mock(spec=PKMValidationRunner)
        vault_manager = VaultManager(self.vault_path, mock_validator_runner)
        
        # Should validate that all required directories exist
        validation_result = vault_manager.validate_vault_structure()
        
        assert validation_result.success == True, "Vault structure validation should pass"
        assert len(validation_result.errors) == 0, "No structural errors should be found"
    
    def test_note_creation_with_validation(self):
        """Task 1.4.3: VaultManager should validate notes during creation"""
        mock_validator_runner = Mock(spec=PKMValidationRunner)
        vault_manager = VaultManager(self.vault_path, mock_validator_runner)
        
        # Mock successful validation
        mock_validator_runner.validate_file.return_value = []
        
        result = vault_manager.create_note(
            content="# Test Note\n\nTest content",
            location="00-inbox",
            filename="test-note.md"
        )
        
        assert result.success == True, "Note creation should succeed with validation"
        assert mock_validator_runner.validate_file.called, "Validation should be triggered"
        
        # File should actually be created
        created_file = self.vault_path / "00-inbox" / "test-note.md"
        assert created_file.exists(), "Note file should be created"
    
    def test_note_creation_fails_with_validation_errors(self):
        """Task 1.4.4: VaultManager should handle validation failures"""
        from src.pkm.validators.base import ValidationResult
        
        mock_validator_runner = Mock(spec=PKMValidationRunner)
        vault_manager = VaultManager(self.vault_path, mock_validator_runner)
        
        # Mock validation failure
        mock_validation_error = ValidationResult(
            file_path=Path("test.md"),
            rule="missing-frontmatter", 
            severity="error",
            message="Missing required frontmatter"
        )
        mock_validator_runner.validate_file.return_value = [mock_validation_error]
        
        result = vault_manager.create_note(
            content="Invalid note without frontmatter",
            location="00-inbox",
            filename="invalid-note.md"
        )
        
        assert result.success == False, "Note creation should fail with validation errors"
        assert len(result.validation_results) == 1, "Validation errors should be included"
        assert "missing-frontmatter" in result.validation_results[0].rule
    
    def test_vault_operations_are_atomic(self):
        """Task 1.4.5: VaultManager operations should be atomic with rollback"""
        mock_validator_runner = Mock(spec=PKMValidationRunner)  
        vault_manager = VaultManager(self.vault_path, mock_validator_runner)
        
        # Test that failed operations don't leave partial state
        mock_validator_runner.validate_file.side_effect = Exception("Validation system error")
        
        result = vault_manager.create_note(
            content="# Test Note",
            location="00-inbox", 
            filename="atomic-test.md"
        )
        
        assert result.success == False, "Operation should fail gracefully"
        
        # File should not exist due to rollback
        test_file = self.vault_path / "00-inbox" / "atomic-test.md"
        assert not test_file.exists(), "Failed operation should not leave partial files"


class TestIntegrationWithValidationSystem:
    """
    Task 1.5-1.6: Integration with FR-VAL-002/003 validation system
    Tests for seamless validation system integration
    """
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.vault_path = Path(self.temp_dir) / "vault"
        self.vault_path.mkdir(parents=True)
        
    def teardown_method(self):
        """Cleanup test environment"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_integration_with_frontmatter_validation(self):
        """Task 1.5.1: Integration with FR-VAL-002 frontmatter validation"""
        # This test ensures PKM agents integrate with existing validation
        from src.pkm.validators.frontmatter_validator import FrontmatterValidator
        from src.pkm.validators.runner import PKMValidationRunner
        
        # Setup validation runner with frontmatter validator
        validator_runner = PKMValidationRunner(self.vault_path)
        frontmatter_validator = FrontmatterValidator()
        validator_runner.add_validator(frontmatter_validator)
        
        # PKM agents should work with this validation setup
        vault_manager = VaultManager(self.vault_path, validator_runner)
        
        assert vault_manager.validator_runner == validator_runner
        assert len(validator_runner.validators) >= 1, "Frontmatter validator should be registered"
    
    def test_integration_with_wiki_link_validation(self):
        """Task 1.5.2: Integration with FR-VAL-003 wiki-link validation"""
        # This test ensures PKM agents integrate with wiki-link validation
        from src.pkm.validators.wiki_link_validator import WikiLinkValidator
        from src.pkm.validators.runner import PKMValidationRunner
        
        # Setup validation runner with wiki-link validator  
        validator_runner = PKMValidationRunner(self.vault_path)
        wiki_link_validator = WikiLinkValidator(self.vault_path)
        validator_runner.add_validator(wiki_link_validator)
        
        # PKM agents should work with this validation setup
        vault_manager = VaultManager(self.vault_path, validator_runner)
        
        assert vault_manager.validator_runner == validator_runner
        assert len(validator_runner.validators) >= 1, "Wiki-link validator should be registered"
    
    def test_comprehensive_validation_integration(self):
        """Task 1.5.3: Comprehensive validation with both FR-VAL-002 and FR-VAL-003"""
        from src.pkm.validators.frontmatter_validator import FrontmatterValidator
        from src.pkm.validators.wiki_link_validator import WikiLinkValidator
        from src.pkm.validators.runner import PKMValidationRunner
        
        # Setup comprehensive validation
        validator_runner = PKMValidationRunner(self.vault_path)
        validator_runner.add_validator(FrontmatterValidator())
        validator_runner.add_validator(WikiLinkValidator(self.vault_path))
        
        # Create PKM command router with comprehensive validation
        router = PkmCommandRouter(self.vault_path, validator_runner)
        
        assert router.validator_runner == validator_runner
        assert len(validator_runner.validators) == 2, "Both validators should be registered"
        
        # Test that validation is triggered during operations
        vault_manager = VaultManager(self.vault_path, validator_runner)
        
        # Should integrate both frontmatter and wiki-link validation
        assert hasattr(vault_manager, 'validator_runner'), "Validation runner should be integrated"


# Test execution guard
if __name__ == "__main__":
    pytest.main([__file__, "-v"])