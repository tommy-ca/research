"""
PKM Validation System - Base Components Tests
FR-VAL-001: TDD Tests for Base Validation Infrastructure

Following TDD RED → GREEN → REFACTOR cycle
All tests written BEFORE implementation
"""

import pytest
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
from abc import ABC, abstractmethod


# Test ValidationResult data structure
def test_validation_result_creation():
    """Test ValidationResult can be created with required fields"""
    from src.pkm.validators.base import ValidationResult
    
    result = ValidationResult(
        file_path=Path("test.md"),
        rule="test-rule",
        severity="error", 
        message="Test message"
    )
    
    assert result.file_path == Path("test.md")
    assert result.rule == "test-rule"
    assert result.severity == "error"
    assert result.message == "Test message"
    assert result.line_number is None


def test_validation_result_with_line_number():
    """Test ValidationResult with optional line number"""
    from src.pkm.validators.base import ValidationResult
    
    result = ValidationResult(
        file_path=Path("test.md"),
        rule="test-rule", 
        severity="warning",
        message="Test message",
        line_number=42
    )
    
    assert result.line_number == 42


def test_validation_result_severity_types():
    """Test ValidationResult accepts valid severity types"""
    from src.pkm.validators.base import ValidationResult
    
    # Valid severities
    for severity in ["error", "warning", "info"]:
        result = ValidationResult(
            file_path=Path("test.md"),
            rule="test-rule",
            severity=severity,
            message="Test message"
        )
        assert result.severity == severity


# Test BaseValidator abstract class
def test_base_validator_is_abstract():
    """Test BaseValidator cannot be instantiated directly"""
    from src.pkm.validators.base import BaseValidator
    
    with pytest.raises(TypeError):
        BaseValidator()


def test_base_validator_requires_validate_method():
    """Test concrete validators must implement validate method"""
    from src.pkm.validators.base import BaseValidator
    
    class IncompleteValidator(BaseValidator):
        pass
    
    with pytest.raises(TypeError):
        IncompleteValidator()


def test_base_validator_concrete_implementation():
    """Test concrete validator implementation works"""
    from src.pkm.validators.base import BaseValidator, ValidationResult
    
    class TestValidator(BaseValidator):
        def validate(self, file_path: Path) -> List[ValidationResult]:
            return [ValidationResult(
                file_path=file_path,
                rule="test-rule",
                severity="info", 
                message="Test validation"
            )]
    
    validator = TestValidator()
    results = validator.validate(Path("test.md"))
    
    assert len(results) == 1
    assert results[0].rule == "test-rule"
    assert results[0].file_path == Path("test.md")


# Test PKMValidationRunner
def test_validation_runner_creation():
    """Test PKMValidationRunner can be created with vault path"""
    from src.pkm.validators.runner import PKMValidationRunner
    
    vault_path = Path("vault/")
    runner = PKMValidationRunner(vault_path)
    
    assert runner.vault_path == vault_path
    assert runner.validators == []


def test_validation_runner_add_validator():
    """Test adding validators to runner"""
    from src.pkm.validators.runner import PKMValidationRunner
    from src.pkm.validators.base import BaseValidator, ValidationResult
    
    class MockValidator(BaseValidator):
        def validate(self, file_path: Path) -> List[ValidationResult]:
            return []
    
    runner = PKMValidationRunner(Path("vault/"))
    validator = MockValidator()
    
    runner.add_validator(validator)
    
    assert len(runner.validators) == 1
    assert runner.validators[0] == validator


def test_validation_runner_validate_empty_vault(tmp_path):
    """Test validation runner with empty vault returns no results"""
    from src.pkm.validators.runner import PKMValidationRunner
    
    runner = PKMValidationRunner(tmp_path)
    results = runner.validate_vault()
    
    assert results == []


def test_validation_runner_validate_vault_with_files(tmp_path):
    """Test validation runner processes markdown files"""
    from src.pkm.validators.runner import PKMValidationRunner
    from src.pkm.validators.base import BaseValidator, ValidationResult
    
    # Create test files
    (tmp_path / "test1.md").write_text("# Test 1")
    (tmp_path / "test2.md").write_text("# Test 2")
    (tmp_path / "other.txt").write_text("Not markdown")
    
    class MockValidator(BaseValidator):
        def validate(self, file_path: Path) -> List[ValidationResult]:
            return [ValidationResult(
                file_path=file_path,
                rule="mock-rule",
                severity="info",
                message=f"Processed {file_path.name}"
            )]
    
    runner = PKMValidationRunner(tmp_path)
    runner.add_validator(MockValidator())
    
    results = runner.validate_vault()
    
    # Should process only .md files
    assert len(results) == 2
    processed_files = {result.file_path.name for result in results}
    assert processed_files == {"test1.md", "test2.md"}


def test_validation_runner_multiple_validators(tmp_path):
    """Test validation runner with multiple validators"""
    from src.pkm.validators.runner import PKMValidationRunner
    from src.pkm.validators.base import BaseValidator, ValidationResult
    
    (tmp_path / "test.md").write_text("# Test")
    
    class ValidatorA(BaseValidator):
        def validate(self, file_path: Path) -> List[ValidationResult]:
            return [ValidationResult(file_path, "rule-a", "info", "A")]
    
    class ValidatorB(BaseValidator):
        def validate(self, file_path: Path) -> List[ValidationResult]:
            return [ValidationResult(file_path, "rule-b", "warning", "B")]
    
    runner = PKMValidationRunner(tmp_path)
    runner.add_validator(ValidatorA())
    runner.add_validator(ValidatorB())
    
    results = runner.validate_vault()
    
    assert len(results) == 2
    rules = {result.rule for result in results}
    assert rules == {"rule-a", "rule-b"}


def test_validation_runner_recursive_file_search(tmp_path):
    """Test validation runner finds files recursively"""
    from src.pkm.validators.runner import PKMValidationRunner
    from src.pkm.validators.base import BaseValidator, ValidationResult
    
    # Create nested structure
    (tmp_path / "root.md").write_text("# Root")
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "nested.md").write_text("# Nested")
    
    class CountingValidator(BaseValidator):
        def validate(self, file_path: Path) -> List[ValidationResult]:
            return [ValidationResult(file_path, "count", "info", "Found")]
    
    runner = PKMValidationRunner(tmp_path)
    runner.add_validator(CountingValidator())
    
    results = runner.validate_vault()
    
    assert len(results) == 2
    file_names = {result.file_path.name for result in results}
    assert file_names == {"root.md", "nested.md"}


# TDD Compliance Tests
def test_tdd_compliance_base_components_exist():
    """Test all base components are available for implementation"""
    # These imports should NOT fail once implementation exists
    try:
        from src.pkm.validators.base import ValidationResult, BaseValidator
        from src.pkm.validators.runner import PKMValidationRunner
        assert True  # If we get here, all components exist
    except ImportError as e:
        pytest.fail(f"Base components not implemented: {e}")


def test_kiss_principle_compliance():
    """Test implementation follows KISS principles"""
    from src.pkm.validators.base import ValidationResult
    
    # ValidationResult should be a simple dataclass
    assert hasattr(ValidationResult, '__dataclass_fields__')
    
    # Should have exactly the expected fields  
    expected_fields = {'file_path', 'rule', 'severity', 'message', 'line_number'}
    actual_fields = set(ValidationResult.__dataclass_fields__.keys())
    assert actual_fields == expected_fields


class TestSpecificationCompliance:
    """Test implementation matches specification requirements"""
    
    def test_validation_result_matches_spec(self):
        """Test ValidationResult matches specification design"""
        from src.pkm.validators.base import ValidationResult
        
        # Test required fields from spec
        result = ValidationResult(
            file_path=Path("test.md"),
            rule="spec-test",
            severity="error",
            message="Spec compliance test"
        )
        
        assert isinstance(result.file_path, Path)
        assert isinstance(result.rule, str)
        assert result.severity in ["error", "warning", "info"]
        assert isinstance(result.message, str)
    
    def test_base_validator_matches_spec(self):
        """Test BaseValidator matches specification interface"""
        from src.pkm.validators.base import BaseValidator, ValidationResult
        from inspect import signature
        
        # Should have abstract validate method
        assert hasattr(BaseValidator, 'validate')
        
        # Validate method should have correct signature
        # (This test will help ensure implementation matches spec)
        class TestValidator(BaseValidator):
            def validate(self, file_path: Path) -> List[ValidationResult]:
                return []
        
        validator = TestValidator()
        sig = signature(validator.validate)
        params = list(sig.parameters.keys())
        
        assert params == ['file_path']
        assert sig.return_annotation == List[ValidationResult]


# Performance baseline tests (for future optimization)
def test_validation_result_creation_performance():
    """Test ValidationResult creation is fast enough"""
    import time
    from src.pkm.validators.base import ValidationResult
    
    start_time = time.time()
    
    # Create 1000 ValidationResults
    for i in range(1000):
        ValidationResult(
            file_path=Path(f"test{i}.md"),
            rule=f"rule-{i}",
            severity="info",
            message=f"Message {i}"
        )
    
    duration = time.time() - start_time
    
    # Should create 1000 results in under 0.1 seconds
    assert duration < 0.1, f"ValidationResult creation too slow: {duration}s"


# Error handling tests
def test_validation_runner_handles_nonexistent_vault():
    """Test validation runner handles nonexistent vault path gracefully"""
    from src.pkm.validators.runner import PKMValidationRunner
    
    runner = PKMValidationRunner(Path("/nonexistent/path"))
    
    # Should not crash, should return empty results
    results = runner.validate_vault()
    assert results == []


def test_validation_runner_handles_permission_errors(tmp_path):
    """Test validation runner handles file permission errors gracefully"""
    import os
    from src.pkm.validators.runner import PKMValidationRunner
    from src.pkm.validators.base import BaseValidator, ValidationResult
    
    # Create file and remove read permissions (if possible on system)
    test_file = tmp_path / "restricted.md"
    test_file.write_text("# Restricted")
    
    try:
        os.chmod(test_file, 0o000)  # Remove all permissions
        
        class MockValidator(BaseValidator):
            def validate(self, file_path: Path) -> List[ValidationResult]:
                # This might fail due to permissions
                with open(file_path, 'r') as f:
                    f.read()
                return []
        
        runner = PKMValidationRunner(tmp_path)
        runner.add_validator(MockValidator())
        
        # Should not crash the entire validation
        results = runner.validate_vault()
        # Results depend on system behavior, but shouldn't crash
        assert isinstance(results, list)
        
    except (OSError, PermissionError):
        # Skip test if we can't modify permissions
        pytest.skip("Cannot modify file permissions on this system")
    finally:
        # Restore permissions for cleanup
        try:
            os.chmod(test_file, 0o644)
        except:
            pass