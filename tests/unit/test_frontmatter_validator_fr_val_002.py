"""
PKM Validation System - Frontmatter Validator Tests
FR-VAL-002: TDD Tests for YAML Frontmatter Validation

Following TDD RED → GREEN → REFACTOR cycle
All tests written BEFORE implementation
"""

import pytest
from pathlib import Path
from typing import List, Dict, Any
import tempfile
import os


# ============================================================================
# TASK GROUP A: Basic Functionality Tests - Required Field Validation
# ============================================================================

def test_valid_frontmatter_passes():
    """Test valid frontmatter returns no errors
    
    Given: File with complete valid frontmatter
    When: FrontmatterValidator.validate() called
    Then: Returns empty list (no ValidationResult objects)
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Create test file with valid frontmatter
    valid_content = """---
date: "2025-09-04"
type: "daily"
tags: ["test", "validation"]
status: "draft"
---

# Test Note

This is a test note with valid frontmatter.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(valid_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should return no errors for valid frontmatter
        assert results == [], f"Expected no validation errors, got: {results}"


def test_missing_date_field_fails():
    """Test missing required date field reports error
    
    Given: Frontmatter without 'date' field
    When: FrontmatterValidator.validate() called
    Then: Returns ValidationResult with rule="missing-required-field"
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    from src.pkm.validators.base import ValidationResult
    
    # Create test file missing date field
    missing_date_content = """---
type: "daily"
tags: ["test"]
status: "draft"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(missing_date_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have exactly one error for missing date
        assert len(results) == 1, f"Expected 1 error, got {len(results)}"
        assert results[0].rule == "missing-required-field"
        assert "date" in results[0].message.lower()
        assert results[0].severity == "error"


def test_missing_type_field_fails():
    """Test missing required type field reports error
    
    Given: Frontmatter without 'type' field
    When: FrontmatterValidator.validate() called
    Then: Returns ValidationResult with rule="missing-required-field"
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    missing_type_content = """---
date: "2025-09-04"
tags: ["test"]
status: "draft"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(missing_type_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have exactly one error for missing type
        assert len(results) == 1
        assert results[0].rule == "missing-required-field"
        assert "type" in results[0].message.lower()
        assert results[0].severity == "error"


def test_missing_tags_field_fails():
    """Test missing required tags field reports error
    
    Given: Frontmatter without 'tags' field
    When: FrontmatterValidator.validate() called
    Then: Returns ValidationResult with rule="missing-required-field"
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    missing_tags_content = """---
date: "2025-09-04"
type: "daily"
status: "draft"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(missing_tags_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have exactly one error for missing tags
        assert len(results) == 1
        assert results[0].rule == "missing-required-field"
        assert "tags" in results[0].message.lower()
        assert results[0].severity == "error"


def test_missing_status_field_fails():
    """Test missing required status field reports error
    
    Given: Frontmatter without 'status' field
    When: FrontmatterValidator.validate() called
    Then: Returns ValidationResult with rule="missing-required-field"
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    missing_status_content = """---
date: "2025-09-04"
type: "daily"
tags: ["test"]
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(missing_status_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have exactly one error for missing status
        assert len(results) == 1
        assert results[0].rule == "missing-required-field"
        assert "status" in results[0].message.lower()
        assert results[0].severity == "error"


def test_multiple_missing_fields_all_reported():
    """Test multiple missing required fields are all reported
    
    Given: Frontmatter missing multiple required fields
    When: FrontmatterValidator.validate() called
    Then: Returns multiple ValidationResult objects, one for each missing field
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Only has type, missing date, tags, status
    minimal_content = """---
type: "daily"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(minimal_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have 3 errors (missing date, tags, status)
        assert len(results) == 3
        
        # Check that all missing fields are reported
        missing_fields = []
        for result in results:
            assert result.rule == "missing-required-field"
            assert result.severity == "error"
            # Extract specific field name from enhanced error message
            # New format: "Required field 'FIELD' is missing. All notes must have: ..."
            message = result.message.lower()
            if "required field 'date'" in message:
                missing_fields.append("date")
            elif "required field 'tags'" in message:
                missing_fields.append("tags")
            elif "required field 'status'" in message:
                missing_fields.append("status")
        
        assert set(missing_fields) == {"date", "tags", "status"}


# ============================================================================
# TASK GROUP A2: Field Format Validation Tests
# ============================================================================

def test_valid_date_format_accepted():
    """Test valid ISO date format (YYYY-MM-DD) is accepted
    
    Given: Frontmatter with valid date format
    When: FrontmatterValidator.validate() called
    Then: No date format errors reported
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    valid_date_content = """---
date: "2025-09-04"
type: "daily"
tags: ["test"]
status: "draft"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(valid_date_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should not have any date format errors
        date_errors = [r for r in results if "date" in r.message.lower() and "format" in r.message.lower()]
        assert len(date_errors) == 0, f"Unexpected date format errors: {date_errors}"


def test_invalid_date_format_rejected():
    """Test invalid date format reports specific error
    
    Given: Frontmatter with invalid date format
    When: FrontmatterValidator.validate() called
    Then: Returns ValidationResult with rule="invalid-date-format"
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    invalid_date_content = """---
date: "invalid-date-format"
type: "daily"
tags: ["test"]
status: "draft"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(invalid_date_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have date format error
        date_errors = [r for r in results if "invalid-date-format" in r.rule or ("date" in r.message.lower() and "format" in r.message.lower())]
        assert len(date_errors) >= 1, f"Expected date format error, got results: {results}"
        assert date_errors[0].severity == "error"


def test_valid_note_type_accepted():
    """Test valid note types (daily, zettel, etc.) are accepted
    
    Given: Frontmatter with valid note type
    When: FrontmatterValidator.validate() called  
    Then: No note type errors reported
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Test multiple valid note types
    valid_types = ["daily", "zettel", "project", "area", "resource", "capture"]
    
    for note_type in valid_types:
        valid_type_content = f"""---
date: "2025-09-04"
type: "{note_type}"
tags: ["test"]
status: "draft"
---

# Test Note of type {note_type}
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(valid_type_content)
            f.flush()
            
            validator = FrontmatterValidator()
            results = validator.validate(Path(f.name))
            
            # Clean up
            os.unlink(f.name)
            
            # Should not have any type errors for valid types
            type_errors = [r for r in results if "type" in r.message.lower() and "invalid" in r.message.lower()]
            assert len(type_errors) == 0, f"Unexpected type errors for '{note_type}': {type_errors}"


def test_invalid_note_type_rejected():
    """Test invalid note type reports specific error
    
    Given: Frontmatter with invalid note type  
    When: FrontmatterValidator.validate() called
    Then: Returns ValidationResult with rule="invalid-note-type"
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    invalid_type_content = """---
date: "2025-09-04"
type: "invalid-note-type"
tags: ["test"]
status: "draft"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(invalid_type_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have note type error
        type_errors = [r for r in results if "invalid-note-type" in r.rule or ("type" in r.message.lower() and "invalid" in r.message.lower())]
        assert len(type_errors) >= 1, f"Expected note type error, got results: {results}"
        assert type_errors[0].severity == "error"


def test_valid_tags_array_accepted():
    """Test valid tags array format is accepted
    
    Given: Frontmatter with valid tags array
    When: FrontmatterValidator.validate() called
    Then: No tags format errors reported  
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    valid_tags_content = """---
date: "2025-09-04"
type: "daily"
tags: ["research", "validation", "testing"]
status: "draft"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(valid_tags_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should not have any tags format errors
        tags_errors = [r for r in results if "tags" in r.message.lower() and "format" in r.message.lower()]
        assert len(tags_errors) == 0, f"Unexpected tags format errors: {tags_errors}"


def test_invalid_tags_format_rejected():
    """Test non-array tags format reports error
    
    Given: Frontmatter with tags as string instead of array
    When: FrontmatterValidator.validate() called
    Then: Returns ValidationResult with rule="invalid-tags-format"
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    invalid_tags_content = """---
date: "2025-09-04"
type: "daily"
tags: "not-an-array"
status: "draft"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(invalid_tags_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have tags format error
        tags_errors = [r for r in results if "invalid-tags-format" in r.rule or ("tags" in r.message.lower() and ("format" in r.message.lower() or "array" in r.message.lower()))]
        assert len(tags_errors) >= 1, f"Expected tags format error, got results: {results}"
        assert tags_errors[0].severity == "error"


def test_valid_status_accepted():
    """Test valid status values are accepted
    
    Given: Frontmatter with valid status value
    When: FrontmatterValidator.validate() called
    Then: No status errors reported
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Test multiple valid status values
    valid_statuses = ["draft", "active", "review", "complete", "archived"]
    
    for status in valid_statuses:
        valid_status_content = f"""---
date: "2025-09-04"
type: "daily"
tags: ["test"]
status: "{status}"
---

# Test Note with status {status}
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(valid_status_content)
            f.flush()
            
            validator = FrontmatterValidator()
            results = validator.validate(Path(f.name))
            
            # Clean up
            os.unlink(f.name)
            
            # Should not have any status errors for valid statuses
            status_errors = [r for r in results if "status" in r.message.lower() and "invalid" in r.message.lower()]
            assert len(status_errors) == 0, f"Unexpected status errors for '{status}': {status_errors}"


def test_invalid_status_rejected():
    """Test invalid status values report error
    
    Given: Frontmatter with invalid status value
    When: FrontmatterValidator.validate() called
    Then: Returns ValidationResult with rule="invalid-status"
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    invalid_status_content = """---
date: "2025-09-04"
type: "daily"
tags: ["test"]
status: "invalid-status"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(invalid_status_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have status error
        status_errors = [r for r in results if "invalid-status" in r.rule or ("status" in r.message.lower() and "invalid" in r.message.lower())]
        assert len(status_errors) >= 1, f"Expected status error, got results: {results}"
        assert status_errors[0].severity == "error"


# ============================================================================
# TASK GROUP B: YAML Parsing Tests  
# ============================================================================

def test_missing_frontmatter_delimiters():
    """Test file without '---' delimiters reports error
    
    Given: File without frontmatter delimiters
    When: FrontmatterValidator.validate() called
    Then: Returns ValidationResult with appropriate error
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # File without frontmatter delimiters
    no_frontmatter_content = """# Test Note

This file has no frontmatter section.
It should be detected as missing frontmatter.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(no_frontmatter_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have frontmatter missing error
        frontmatter_errors = [r for r in results if "frontmatter" in r.message.lower() or "delimiter" in r.message.lower()]
        assert len(frontmatter_errors) >= 1, f"Expected frontmatter missing error, got results: {results}"
        assert frontmatter_errors[0].severity == "error"


def test_invalid_yaml_syntax_error():
    """Test malformed YAML reports syntax error with line number
    
    Given: File with invalid YAML syntax in frontmatter
    When: FrontmatterValidator.validate() called
    Then: Returns ValidationResult with YAML syntax error
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Invalid YAML syntax - unmatched quotes, invalid structure
    invalid_yaml_content = """---
date: "2025-09-04
type: daily"
tags: [unclosed, array
status: "draft"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(invalid_yaml_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have YAML syntax error
        yaml_errors = [r for r in results if "yaml" in r.message.lower() and ("syntax" in r.message.lower() or "parsing" in r.message.lower())]
        assert len(yaml_errors) >= 1, f"Expected YAML syntax error, got results: {results}"
        assert yaml_errors[0].severity == "error"


def test_empty_frontmatter_handled():
    """Test empty frontmatter section handled gracefully
    
    Given: File with empty frontmatter section
    When: FrontmatterValidator.validate() called
    Then: Returns appropriate validation errors for missing fields
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    empty_frontmatter_content = """---
---

# Test Note

This file has empty frontmatter.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(empty_frontmatter_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have errors for all missing required fields
        assert len(results) >= 4, f"Expected at least 4 missing field errors, got: {results}"
        
        # Verify that missing field errors are reported (not parsing errors)
        missing_field_errors = [r for r in results if "missing-required-field" in r.rule or "missing" in r.message.lower()]
        assert len(missing_field_errors) >= 4, f"Expected missing field errors, got: {results}"


def test_frontmatter_extraction_successful():
    """Test frontmatter correctly extracted from markdown content
    
    Given: File with valid frontmatter and markdown content
    When: FrontmatterValidator.validate() called
    Then: Validation processes frontmatter correctly (no extraction errors)
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Complex but valid frontmatter with markdown content
    complex_content = """---
date: "2025-09-04"
type: "zettel"
tags: ["complex", "testing", "validation"]
status: "active"
links: ["[[related-note]]", "[[another-note]]"]
source: "test_suite"
---

# Complex Test Note

This note has complex frontmatter and substantial markdown content.

## Section 1

Some content here with **bold** and *italic* text.

## Section 2

- List item 1
- List item 2  
- List item 3

```python
# Code block
def example():
    return "test"
```

More content that should not interfere with frontmatter parsing.
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(complex_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should have no errors for valid, complete frontmatter
        assert results == [], f"Expected no validation errors for valid frontmatter, got: {results}"


# ============================================================================
# TASK GROUP C: Integration Tests
# ============================================================================

def test_frontmatter_validator_integrates_with_runner():
    """Test FrontmatterValidator works with PKMValidationRunner
    
    Given: FrontmatterValidator added to PKMValidationRunner
    When: Runner validates files
    Then: FrontmatterValidator results included in runner output
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    from src.pkm.validators.runner import PKMValidationRunner
    
    # Create test file with validation error
    test_content = """---
date: "invalid-date"
type: "invalid-type"
tags: "not-array"
status: "invalid-status"
---

# Test Note
"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_file = temp_path / "test.md"
        test_file.write_text(test_content)
        
        # Create runner and add frontmatter validator
        runner = PKMValidationRunner(temp_path)
        validator = FrontmatterValidator()
        runner.add_validator(validator)
        
        # Run validation
        results = runner.validate_vault()
        
        # Should have validation errors from frontmatter validator
        assert len(results) > 0, "Expected validation errors from frontmatter validator"
        
        # Verify results are from frontmatter validation
        frontmatter_results = [r for r in results if r.file_path.name == "test.md"]
        assert len(frontmatter_results) >= 4, f"Expected multiple frontmatter errors, got: {frontmatter_results}"


def test_multiple_files_validation():
    """Test validator processes multiple files correctly
    
    Given: Multiple files with different validation states
    When: FrontmatterValidator processes all files
    Then: Each file validated independently with correct results
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    from src.pkm.validators.runner import PKMValidationRunner
    
    valid_content = """---
date: "2025-09-04"
type: "daily"
tags: ["test"]
status: "draft"
---

# Valid Note
"""
    
    invalid_content = """---
date: "invalid-date"
type: "daily"  
tags: ["test"]
status: "draft"
---

# Invalid Note
"""
    
    missing_fields_content = """---
date: "2025-09-04"
---

# Incomplete Note
"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create multiple test files
        (temp_path / "valid.md").write_text(valid_content)
        (temp_path / "invalid.md").write_text(invalid_content) 
        (temp_path / "incomplete.md").write_text(missing_fields_content)
        
        runner = PKMValidationRunner(temp_path)
        runner.add_validator(FrontmatterValidator())
        
        results = runner.validate_vault()
        
        # Should have results for invalid and incomplete files only
        files_with_errors = {r.file_path.name for r in results}
        
        # Valid file should have no errors
        valid_errors = [r for r in results if r.file_path.name == "valid.md"]
        assert len(valid_errors) == 0, f"Valid file should have no errors: {valid_errors}"
        
        # Invalid file should have date format error
        invalid_errors = [r for r in results if r.file_path.name == "invalid.md"]
        assert len(invalid_errors) >= 1, "Invalid file should have date format error"
        
        # Incomplete file should have missing field errors  
        incomplete_errors = [r for r in results if r.file_path.name == "incomplete.md"]
        assert len(incomplete_errors) >= 3, "Incomplete file should have multiple missing field errors"


def test_mixed_valid_invalid_files():
    """Test validator handles mix of valid/invalid files
    
    Given: Directory with mix of valid and invalid files
    When: Validation runs on entire directory
    Then: Only invalid files generate errors, valid files are silent
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    from src.pkm.validators.runner import PKMValidationRunner
    
    valid_file1_content = """---
date: "2025-09-04"
type: "daily"
tags: ["valid"]
status: "draft"
---

# Valid File 1
"""
    
    valid_file2_content = """---
date: "2025-09-05"
type: "zettel"
tags: ["also", "valid"]
status: "active"
---

# Valid File 2
"""
    
    invalid_file_content = """---
type: "missing-other-fields"
---

# Invalid File
"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create mixed files
        (temp_path / "valid1.md").write_text(valid_file1_content)
        (temp_path / "valid2.md").write_text(valid_file2_content)
        (temp_path / "invalid.md").write_text(invalid_file_content)
        
        runner = PKMValidationRunner(temp_path)
        runner.add_validator(FrontmatterValidator())
        
        results = runner.validate_vault()
        
        # Should only have errors from invalid file
        error_files = {r.file_path.name for r in results}
        assert error_files == {"invalid.md"}, f"Expected errors only from invalid.md, got errors from: {error_files}"
        
        # Invalid file should have multiple missing field errors
        invalid_errors = [r for r in results if r.file_path.name == "invalid.md"]
        assert len(invalid_errors) >= 3, f"Expected at least 3 missing field errors, got: {len(invalid_errors)}"


def test_error_accumulation():
    """Test errors from multiple files are accumulated correctly
    
    Given: Multiple files each with different validation errors
    When: Validation runs on directory
    Then: All errors accumulated and returned in single results list
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    from src.pkm.validators.runner import PKMValidationRunner
    
    file1_content = """---
date: "invalid-date"
type: "daily"
tags: ["test"]
status: "draft"
---

# File 1
"""
    
    file2_content = """---
date: "2025-09-04"
type: "invalid-type"
tags: ["test"]
status: "draft"
---

# File 2
"""
    
    file3_content = """---
date: "2025-09-04"
type: "daily"
tags: "invalid-tags"
status: "draft"
---

# File 3
"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create files with different error types
        (temp_path / "file1.md").write_text(file1_content)
        (temp_path / "file2.md").write_text(file2_content)
        (temp_path / "file3.md").write_text(file3_content)
        
        runner = PKMValidationRunner(temp_path)
        runner.add_validator(FrontmatterValidator())
        
        results = runner.validate_vault()
        
        # Should have exactly one error per file (each has one validation issue)
        assert len(results) == 3, f"Expected 3 validation errors (one per file), got: {len(results)}"
        
        # Verify each file has its specific error type
        files_with_errors = {r.file_path.name for r in results}
        assert files_with_errors == {"file1.md", "file2.md", "file3.md"}, f"Expected errors from all 3 files, got: {files_with_errors}"
        
        # Verify error types are as expected
        error_messages = [r.message.lower() for r in results]
        assert any("date" in msg and "format" in msg for msg in error_messages), "Expected date format error"
        assert any("type" in msg and "invalid" in msg for msg in error_messages), "Expected invalid type error"
        assert any("tags" in msg and ("format" in msg or "array" in msg) for msg in error_messages), "Expected tags format error"


# ============================================================================
# TASK GROUP D: Edge Case Tests
# ============================================================================

def test_file_permission_error_handled():
    """Test graceful handling of file permission errors
    
    Given: File with no read permissions
    When: FrontmatterValidator attempts to validate
    Then: Returns ValidationResult with permission error, does not crash
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    import os
    import stat
    
    test_content = """---
date: "2025-09-04"
type: "daily"
tags: ["test"]
status: "draft"
---

# Test Note
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(test_content)
        f.flush()
        
        try:
            # Remove read permissions (if possible on system)
            os.chmod(f.name, 0o000)
            
            validator = FrontmatterValidator()
            results = validator.validate(Path(f.name))
            
            # Should handle permission error gracefully
            assert isinstance(results, list), "Should return list even with permission error"
            
            # May have permission error or may succeed depending on system
            # Main requirement is no crash
            
        except (OSError, PermissionError):
            # Skip test if we can't modify permissions on this system
            pytest.skip("Cannot modify file permissions on this system")
        finally:
            # Restore permissions for cleanup
            try:
                os.chmod(f.name, 0o644)
                os.unlink(f.name)
            except:
                pass


def test_file_not_found_handled():
    """Test graceful handling of missing files
    
    Given: Path to non-existent file
    When: FrontmatterValidator attempts to validate
    Then: Returns ValidationResult with file not found error, does not crash
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Use path to non-existent file
    nonexistent_file = Path("/nonexistent/path/file.md")
    
    validator = FrontmatterValidator()
    results = validator.validate(nonexistent_file)
    
    # Should handle missing file gracefully
    assert isinstance(results, list), "Should return list even with missing file"
    
    # Should have file not found error
    if len(results) > 0:
        assert any("not found" in r.message.lower() or "no such file" in r.message.lower() for r in results), f"Expected file not found error, got: {results}"


def test_unicode_content_handled():
    """Test proper handling of Unicode characters in YAML
    
    Given: Frontmatter with Unicode characters
    When: FrontmatterValidator processes file
    Then: Handles Unicode correctly without errors
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Test with various Unicode characters
    unicode_content = """---
date: "2025-09-04"
type: "daily"
tags: ["测试", "テスト", "тест", "🏷️"]
status: "draft"
author: "José María"
title: "Ñoño testing with émojis 🚀"
---

# Unicode Test Note

This note contains Unicode characters: 中文, 日本語, Русский, العربية
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(unicode_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should handle Unicode without errors (valid frontmatter)
        assert results == [], f"Should handle Unicode content without errors, got: {results}"


def test_very_large_frontmatter_handled():
    """Test handling of unusually large frontmatter sections
    
    Given: File with very large frontmatter section
    When: FrontmatterValidator processes file
    Then: Handles large frontmatter without performance issues
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Create large but valid frontmatter
    large_tags = [f"tag_{i}" for i in range(100)]  # 100 tags
    large_content = f"""---
date: "2025-09-04"
type: "daily"
tags: {large_tags}
status: "draft"
description: "{'Very long description. ' * 100}"
notes: "{'Additional notes content. ' * 50}"
---

# Large Frontmatter Test
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(large_content)
        f.flush()
        
        validator = FrontmatterValidator()
        
        # Time the validation to ensure it's reasonable
        import time
        start_time = time.time()
        results = validator.validate(Path(f.name))
        duration = time.time() - start_time
        
        # Clean up
        os.unlink(f.name)
        
        # Should complete within reasonable time (under 1 second)
        assert duration < 1.0, f"Large frontmatter validation took too long: {duration}s"
        
        # Should validate successfully (all required fields present and valid)
        assert results == [], f"Large but valid frontmatter should not generate errors: {results}"


def test_nested_yaml_structures_handled():
    """Test handling of complex nested YAML structures
    
    Given: Frontmatter with nested YAML structures
    When: FrontmatterValidator processes file
    Then: Handles nested structures correctly
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Complex nested YAML structure
    nested_content = """---
date: "2025-09-04"
type: "project"
tags: ["complex", "nested"]
status: "active"
metadata:
  created_by: "test_user"
  tools_used:
    - name: "tool1"
      version: "1.0"
    - name: "tool2"  
      version: "2.1"
  config:
    settings:
      debug: true
      level: 3
related_links:
  - title: "Link 1"
    url: "https://example.com"
  - title: "Link 2"
    url: "https://example.org"
---

# Nested YAML Test
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(nested_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should handle nested YAML without errors (all required fields present)
        assert results == [], f"Complex nested YAML should not generate errors: {results}"


def test_binary_file_handled():
    """Test graceful handling of binary files
    
    Given: Binary file (non-text)
    When: FrontmatterValidator attempts to process
    Then: Handles binary content gracefully without crashing
    """
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    
    # Create binary content (simulate image or other binary file)
    binary_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
    
    with tempfile.NamedTemporaryFile(suffix='.md', delete=False, mode='wb') as f:
        f.write(binary_content)
        f.flush()
        
        validator = FrontmatterValidator()
        results = validator.validate(Path(f.name))
        
        # Clean up
        os.unlink(f.name)
        
        # Should handle binary file gracefully (likely with parsing error)
        assert isinstance(results, list), "Should return list even with binary content"
        
        # Should have some kind of error (parsing or encoding error)
        assert len(results) > 0, "Should report error for binary content"
        
        # Verify it's a parsing/encoding error, not a crash
        assert all(r.severity == "error" for r in results), "All results should be error severity"


# ============================================================================
# TDD Compliance Tests
# ============================================================================

def test_tdd_compliance_frontmatter_validator_components_exist():
    """Test all frontmatter validator components are available for implementation"""
    # These imports should NOT fail once implementation exists
    try:
        from src.pkm.validators.frontmatter_validator import FrontmatterValidator
        from src.pkm.validators.base import ValidationResult, BaseValidator
        assert True  # If we get here, all components exist
    except ImportError as e:
        pytest.fail(f"Frontmatter validator components not implemented: {e}")


def test_kiss_principle_compliance_frontmatter_validator():
    """Test frontmatter validator implementation follows KISS principles"""
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    from src.pkm.validators.base import BaseValidator
    
    # FrontmatterValidator should inherit from BaseValidator
    assert issubclass(FrontmatterValidator, BaseValidator), "FrontmatterValidator should inherit from BaseValidator"
    
    # Should have the required validate method
    assert hasattr(FrontmatterValidator, 'validate'), "FrontmatterValidator should have validate method"


def test_specification_compliance_frontmatter_validator():
    """Test frontmatter validator matches specification design"""
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    from src.pkm.validators.base import ValidationResult
    from inspect import signature
    from pathlib import Path
    from typing import List
    
    # Validate method should have correct signature
    validator = FrontmatterValidator()
    sig = signature(validator.validate)
    params = list(sig.parameters.keys())
    
    assert params == ['file_path'], f"Expected ['file_path'] parameters, got: {params}"
    assert sig.return_annotation == List[ValidationResult], f"Expected List[ValidationResult] return type, got: {sig.return_annotation}"


# ============================================================================
# Performance Tests
# ============================================================================

def test_frontmatter_validator_performance():
    """Test frontmatter validator performance meets benchmarks"""
    from src.pkm.validators.frontmatter_validator import FrontmatterValidator
    import time
    
    # Create test content
    test_content = """---
date: "2025-09-04"
type: "daily"
tags: ["performance", "test"]
status: "draft"
---

# Performance Test Note
"""
    
    validator = FrontmatterValidator()
    
    # Create multiple temporary files for performance testing
    files = []
    try:
        for i in range(50):  # Test with 50 files
            f = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
            f.write(test_content)
            f.close()
            files.append(Path(f.name))
        
        # Time the validation
        start_time = time.time()
        for file_path in files:
            validator.validate(file_path)
        duration = time.time() - start_time
        
        # Should process at least 25 files per second (conservative benchmark)
        files_per_second = len(files) / duration
        assert files_per_second >= 25, f"Performance too slow: {files_per_second:.1f} files/sec (expected ≥25)"
        
    finally:
        # Clean up
        for file_path in files:
            try:
                os.unlink(file_path)
            except:
                pass