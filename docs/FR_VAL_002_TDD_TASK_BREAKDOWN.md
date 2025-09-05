# FR-VAL-002 TDD Task Breakdown
*Actionable TDD tasks for YAML Frontmatter Validation implementation*

## Implementation Overview

Following the ultra-thinking analysis and comprehensive specifications, this document breaks down FR-VAL-002 implementation into specific, actionable TDD tasks following the RED → GREEN → REFACTOR cycle.

## Phase 1: TDD RED Phase (Write Failing Tests First)

### Task Group A: Basic Functionality Tests ⭐ **Priority 1**

#### Task A1: Required Field Validation Tests
**Estimated Time:** 2 hours  
**TDD Phase:** RED (Write failing tests)  
**Acceptance:** All tests fail with appropriate ImportError/ModuleNotFoundError

**Specific Test Cases to Implement:**
```python
# File: tests/unit/test_frontmatter_validator_fr_val_002.py

def test_valid_frontmatter_passes():
    """Test valid frontmatter returns no errors"""
    # Given: File with complete valid frontmatter
    # When: FrontmatterValidator.validate() called
    # Then: Returns empty list (no ValidationResult objects)

def test_missing_date_field_fails():
    """Test missing required date field reports error"""
    # Given: Frontmatter without 'date' field
    # When: FrontmatterValidator.validate() called
    # Then: Returns ValidationResult with rule="missing-required-field"

def test_missing_type_field_fails():
    """Test missing required type field reports error"""
    
def test_missing_tags_field_fails():
    """Test missing required tags field reports error"""
    
def test_missing_status_field_fails():
    """Test missing required status field reports error"""
```

**Success Criteria:**
- [ ] 5 test functions written and documented
- [ ] All tests import from non-existent module (fail appropriately)
- [ ] Test names clearly describe expected behavior
- [ ] Given/When/Then structure documented in docstrings

#### Task A2: Field Format Validation Tests
**Estimated Time:** 2 hours  
**TDD Phase:** RED  
**Dependencies:** Task A1 complete

**Specific Test Cases to Implement:**
```python
def test_valid_date_format_accepted():
    """Test valid ISO date format (YYYY-MM-DD) is accepted"""
    
def test_invalid_date_format_rejected():
    """Test invalid date format reports specific error"""
    
def test_valid_note_type_accepted():
    """Test valid note types (daily, zettel, etc.) are accepted"""
    
def test_invalid_note_type_rejected():
    """Test invalid note type reports specific error"""
    
def test_valid_tags_array_accepted():
    """Test valid tags array format is accepted"""
    
def test_invalid_tags_format_rejected():
    """Test non-array tags format reports error"""
    
def test_valid_status_accepted():
    """Test valid status values are accepted"""
    
def test_invalid_status_rejected():
    """Test invalid status values report error"""
```

**Success Criteria:**
- [ ] 8 test functions for format validation
- [ ] Covers all enum values and valid formats
- [ ] Tests both positive and negative cases
- [ ] Clear error message expectations documented

### Task Group B: YAML Parsing Tests ⭐ **Priority 1**

#### Task B1: YAML Structure Tests
**Estimated Time:** 1.5 hours  
**TDD Phase:** RED  
**Dependencies:** Task A1-A2 complete

**Specific Test Cases to Implement:**
```python
def test_missing_frontmatter_delimiters():
    """Test file without '---' delimiters reports error"""
    
def test_invalid_yaml_syntax_error():
    """Test malformed YAML reports syntax error with line number"""
    
def test_empty_frontmatter_handled():
    """Test empty frontmatter section handled gracefully"""
    
def test_frontmatter_extraction_successful():
    """Test frontmatter correctly extracted from markdown content"""
```

**Success Criteria:**
- [ ] 4 test functions for YAML parsing edge cases
- [ ] Tests cover structural validation before content validation
- [ ] Line number error reporting tested
- [ ] Both success and failure paths covered

### Task Group C: Integration Tests ⭐ **Priority 2**

#### Task C1: PKMValidationRunner Integration Tests  
**Estimated Time:** 1 hour  
**TDD Phase:** RED  
**Dependencies:** All Task A, B complete

**Specific Test Cases to Implement:**
```python
def test_frontmatter_validator_integrates_with_runner():
    """Test FrontmatterValidator works with PKMValidationRunner"""
    
def test_multiple_files_validation():
    """Test validator processes multiple files correctly"""
    
def test_mixed_valid_invalid_files():
    """Test validator handles mix of valid/invalid files"""
    
def test_error_accumulation():
    """Test errors from multiple files are accumulated correctly"""
```

**Success Criteria:**
- [ ] 4 integration test functions
- [ ] Tests validator plugs into existing PKMValidationRunner  
- [ ] Covers batch processing scenarios
- [ ] Error handling across multiple files tested

### Task Group D: Edge Case Tests ⭐ **Priority 2**

#### Task D1: Error Handling Edge Cases
**Estimated Time:** 1.5 hours  
**TDD Phase:** RED  
**Dependencies:** Core tests (A, B) complete

**Specific Test Cases to Implement:**
```python
def test_file_permission_error_handled():
    """Test graceful handling of file permission errors"""
    
def test_file_not_found_handled():
    """Test graceful handling of missing files"""
    
def test_unicode_content_handled():
    """Test proper handling of Unicode characters in YAML"""
    
def test_very_large_frontmatter_handled():
    """Test handling of unusually large frontmatter sections"""
    
def test_nested_yaml_structures_handled():
    """Test handling of complex nested YAML structures"""
    
def test_binary_file_handled():
    """Test graceful handling of binary files"""
```

**Success Criteria:**
- [ ] 6 edge case test functions  
- [ ] Comprehensive error scenario coverage
- [ ] Tests verify graceful degradation
- [ ] Performance edge cases included

### RED Phase Completion Checklist

**Test Suite Completeness:** 22 total tests
- [ ] **8 tests**: Required field validation (Task A1)
- [ ] **8 tests**: Field format validation (Task A2)  
- [ ] **4 tests**: YAML parsing validation (Task B1)
- [ ] **4 tests**: Integration testing (Task C1)
- [ ] **6 tests**: Edge case handling (Task D1)

**Quality Standards:**  
- [ ] All test functions have clear docstrings with Given/When/Then
- [ ] Test names are descriptive and behavior-focused  
- [ ] All imports reference non-existent modules (proper RED phase)
- [ ] Test file follows established naming conventions
- [ ] Tests cover all acceptance criteria from specification

**Validation Commands:**
```bash
# Confirm all tests fail appropriately (RED phase)
python -m pytest tests/unit/test_frontmatter_validator_fr_val_002.py -v
# Expected: 22 failures with ModuleNotFoundError/ImportError
```

## Phase 2: TDD GREEN Phase (Minimal Implementation)

### Task Group E: Core Infrastructure Setup ⭐ **Priority 1**

#### Task E1: Dependencies Installation
**Estimated Time:** 30 minutes  
**TDD Phase:** GREEN (Enable testing)  
**Dependencies:** RED phase complete

**Specific Actions:**
```bash
# Install required dependencies
pip install jsonschema>=4.17.0
pip install pydantic>=2.0.0  
pip install pyyaml>=6.0

# Update requirements file or pyproject.toml
```

**Success Criteria:**
- [ ] All dependencies installed successfully
- [ ] Import statements in tests no longer fail  
- [ ] Dependencies properly documented in project requirements

#### Task E2: Basic Module Structure Creation
**Estimated Time:** 45 minutes  
**TDD Phase:** GREEN  
**Dependencies:** Task E1 complete

**Files to Create:**
```python
# src/pkm/validators/frontmatter_validator.py
from pathlib import Path
from typing import List
from .base import BaseValidator, ValidationResult

class FrontmatterValidator(BaseValidator):
    """Validates YAML frontmatter - minimal implementation"""
    
    def validate(self, file_path: Path) -> List[ValidationResult]:
        """Validate YAML frontmatter in markdown file"""
        # MINIMAL implementation - just enough to make some tests pass
        return []  # Start with empty implementation
```

**Success Criteria:**
- [ ] Module imports successfully  
- [ ] Class inherits from BaseValidator correctly
- [ ] Basic method signature matches specification
- [ ] Some tests begin passing (those expecting empty results)

### Task Group F: Core Validation Implementation ⭐ **Priority 1**

#### Task F1: YAML Frontmatter Extraction
**Estimated Time:** 2 hours  
**TDD Phase:** GREEN  
**Dependencies:** Task E1-E2 complete

**Implementation Focus:**
- Basic frontmatter delimiter detection (`---`)
- YAML parsing using pyyaml
- Error handling for malformed YAML
- **Goal:** Make YAML parsing tests pass

**Minimal Implementation Strategy:**
```python
def _extract_frontmatter(self, content: str) -> tuple[dict, str]:
    """Extract frontmatter from markdown content - minimal version"""
    if not content.strip().startswith('---'):
        return {}, "No frontmatter delimiters found"
    
    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, "Invalid frontmatter structure"
            
        frontmatter_yaml = parts[1].strip()
        import yaml
        frontmatter = yaml.safe_load(frontmatter_yaml)
        return frontmatter or {}, ""
    except yaml.YAMLError as e:
        return {}, f"YAML syntax error: {e}"
    except Exception as e:
        return {}, f"Parsing error: {e}"
```

**Success Criteria:**
- [ ] YAML parsing tests pass
- [ ] Frontmatter extraction working for valid cases
- [ ] Error handling for malformed YAML implemented
- [ ] No regression in previously passing tests

#### Task F2: Required Field Validation
**Estimated Time:** 1.5 hours  
**TDD Phase:** GREEN  
**Dependencies:** Task F1 complete

**Implementation Focus:**
- Check for presence of required fields (date, type, tags, status)
- Generate appropriate ValidationResult for missing fields
- **Goal:** Make required field validation tests pass

**Minimal Implementation Strategy:**
```python
def _validate_required_fields(self, frontmatter: dict, file_path: Path) -> List[ValidationResult]:
    """Validate required fields presence - minimal version"""
    results = []
    required_fields = ['date', 'type', 'tags', 'status']
    
    for field in required_fields:
        if field not in frontmatter:
            results.append(ValidationResult(
                file_path=file_path,
                rule="missing-required-field",
                severity="error",
                message=f"Required field '{field}' is missing"
            ))
    
    return results
```

**Success Criteria:**
- [ ] Required field validation tests pass
- [ ] Missing field errors correctly generated  
- [ ] Error messages are clear and actionable
- [ ] ValidationResult objects properly constructed

#### Task F3: Field Format Validation
**Estimated Time:** 2 hours  
**TDD Phase:** GREEN  
**Dependencies:** Task F2 complete

**Implementation Focus:**
- Date format validation (YYYY-MM-DD pattern)
- Note type enum validation  
- Tags array format validation
- Status enum validation
- **Goal:** Make field format validation tests pass

**Minimal Implementation Strategy:**
```python
def _validate_field_formats(self, frontmatter: dict, file_path: Path) -> List[ValidationResult]:
    """Validate field formats - minimal version"""
    results = []
    
    # Date format validation
    if 'date' in frontmatter:
        import re
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        if not re.match(date_pattern, str(frontmatter['date'])):
            results.append(ValidationResult(
                file_path=file_path, rule="invalid-date-format",
                severity="error", message="Date must be in YYYY-MM-DD format"
            ))
    
    # Type validation
    if 'type' in frontmatter:
        valid_types = ['daily', 'zettel', 'project', 'area', 'resource', 'capture']
        if frontmatter['type'] not in valid_types:
            results.append(ValidationResult(
                file_path=file_path, rule="invalid-note-type",
                severity="error", message=f"Invalid note type: {frontmatter['type']}"
            ))
    
    # Tags validation  
    if 'tags' in frontmatter:
        if not isinstance(frontmatter['tags'], list):
            results.append(ValidationResult(
                file_path=file_path, rule="invalid-tags-format", 
                severity="error", message="Tags must be an array of strings"
            ))
    
    # Status validation
    if 'status' in frontmatter:
        valid_statuses = ['draft', 'active', 'review', 'complete', 'archived']
        if frontmatter['status'] not in valid_statuses:
            results.append(ValidationResult(
                file_path=file_path, rule="invalid-status",
                severity="error", message=f"Invalid status: {frontmatter['status']}"
            ))
    
    return results
```

**Success Criteria:**
- [ ] Field format validation tests pass
- [ ] Date pattern matching working  
- [ ] Enum validation for type and status working
- [ ] Tags array format validation working
- [ ] All validation errors properly formatted

### Task Group G: Integration & Error Handling ⭐ **Priority 1**

#### Task G1: Complete Integration with Runner
**Estimated Time:** 1 hour  
**TDD Phase:** GREEN  
**Dependencies:** Task F1-F3 complete

**Implementation Focus:**
- Combine all validation methods in main validate() method
- Ensure proper error handling and accumulation
- **Goal:** Make integration tests pass

**Minimal Implementation Strategy:**
```python
def validate(self, file_path: Path) -> List[ValidationResult]:
    """Complete validation implementation - minimal version"""
    results = []
    
    try:
        content = file_path.read_text(encoding='utf-8')
        frontmatter, parse_error = self._extract_frontmatter(content)
        
        if parse_error:
            results.append(ValidationResult(
                file_path=file_path, rule="frontmatter-parse-error",
                severity="error", message=parse_error
            ))
            return results  # Can't validate content if parsing failed
        
        # Validate required fields and formats
        results.extend(self._validate_required_fields(frontmatter, file_path))
        results.extend(self._validate_field_formats(frontmatter, file_path))
        
    except FileNotFoundError:
        results.append(ValidationResult(
            file_path=file_path, rule="file-not-found",
            severity="error", message="File not found"
        ))
    except PermissionError:
        results.append(ValidationResult(
            file_path=file_path, rule="permission-error", 
            severity="error", message="Permission denied reading file"
        ))
    except Exception as e:
        results.append(ValidationResult(
            file_path=file_path, rule="validation-error",
            severity="error", message=f"Validation error: {e}"
        ))
    
    return results
```

**Success Criteria:**
- [ ] Integration tests pass
- [ ] All validation methods work together  
- [ ] Error handling comprehensive
- [ ] Works seamlessly with PKMValidationRunner

#### Task G2: Edge Case Handling
**Estimated Time:** 1.5 hours  
**TDD Phase:** GREEN  
**Dependencies:** Task G1 complete  

**Implementation Focus:**
- Handle Unicode content properly
- Graceful handling of permission errors
- Handle binary files appropriately
- **Goal:** Make edge case tests pass

**Success Criteria:**
- [ ] Edge case tests pass
- [ ] Unicode content handled properly
- [ ] Error conditions handled gracefully
- [ ] No crashes on malformed input

### GREEN Phase Completion Checklist

**Implementation Complete:**
- [ ] All 22 tests passing
- [ ] FrontmatterValidator fully functional
- [ ] Integration with PKMValidationRunner working
- [ ] Error handling comprehensive
- [ ] Basic performance acceptable

**Quality Validation:**
```bash
# Confirm all tests pass (GREEN phase complete)
python -m pytest tests/unit/test_frontmatter_validator_fr_val_002.py -v
# Expected: 22 passed

# Integration test with existing system  
python -m pytest tests/unit/ -v
# Expected: All existing tests still pass + new tests pass
```

## Phase 3: TDD REFACTOR Phase (Quality & Performance)

### Task Group H: Code Quality Refactoring ⭐ **Priority 1**

#### Task H1: Extract Schema Definitions
**Estimated Time:** 1 hour  
**TDD Phase:** REFACTOR  
**Dependencies:** GREEN phase complete

**Refactoring Focus:**
- Extract schema definitions to separate module
- Create reusable schema validation components
- Improve maintainability and extensibility

**Actions:**
```python
# Create: src/pkm/validators/schemas/frontmatter_schema.py
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class FrontmatterSchema(BaseModel):
    """Type-safe frontmatter schema using Pydantic"""
    date: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')
    type: Literal["daily", "zettel", "project", "area", "resource", "capture"]
    tags: List[str]
    status: Literal["draft", "active", "review", "complete", "archived"]
    
    # Optional fields
    links: Optional[List[str]] = None
    source: Optional[str] = None
```

**Success Criteria:**
- [ ] Schema definitions extracted to separate module
- [ ] All tests still pass after refactoring
- [ ] Code is more maintainable and extensible
- [ ] Type safety improved with Pydantic models

#### Task H2: Performance Optimization
**Estimated Time:** 2 hours  
**TDD Phase:** REFACTOR  
**Dependencies:** Task H1 complete

**Optimization Focus:**
- Optimize YAML parsing performance
- Add caching for repeated validations
- Minimize memory usage

**Performance Improvements:**
```python
class FrontmatterValidator(BaseValidator):
    def __init__(self):
        # Cache compiled regex patterns
        self._date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        self._schema = self._load_schema()  # Load once, reuse
    
    def _extract_frontmatter(self, content: str) -> tuple[dict, str]:
        # Optimized frontmatter extraction
        # Early return for non-frontmatter files
        # Efficient string splitting
        pass
```

**Success Criteria:**
- [ ] Performance benchmarks met (≥100 files/second)
- [ ] Memory usage within limits (<50MB for 1000 files)
- [ ] All tests still pass after optimization
- [ ] Performance regression testing implemented

#### Task H3: Enhanced Error Messages
**Estimated Time:** 1 hour  
**TDD Phase:** REFACTOR  
**Dependencies:** Task H2 complete

**Enhancement Focus:**
- More detailed, actionable error messages
- Include context and suggestions for fixing
- Better user experience

**Error Message Improvements:**
```python
# BEFORE: Generic error message
message="Invalid date format"

# AFTER: Detailed, actionable error message  
message=f"Invalid date format '{frontmatter['date']}'. Expected YYYY-MM-DD format (e.g., '2025-09-04')"
```

**Success Criteria:**
- [ ] Error messages are detailed and actionable
- [ ] Users understand what went wrong and how to fix it
- [ ] All tests still pass with improved messages
- [ ] Error message consistency across all validators

### Task Group I: Documentation & Finalization ⭐ **Priority 2**

#### Task I1: Comprehensive Documentation
**Estimated Time:** 1.5 hours  
**TDD Phase:** REFACTOR  
**Dependencies:** All refactoring complete

**Documentation Tasks:**
- Complete docstrings for all public methods
- Add usage examples and API documentation  
- Update project documentation with new validator

**Success Criteria:**
- [ ] All public methods have comprehensive docstrings
- [ ] Usage examples provided
- [ ] API documentation updated
- [ ] Integration documentation complete

#### Task I2: Final Quality Validation
**Estimated Time:** 1 hour  
**TDD Phase:** REFACTOR  
**Dependencies:** All tasks complete

**Quality Checks:**
- Run full test suite including performance tests
- Code quality metrics validation
- SOLID principle compliance review
- Integration testing with full PKM system

**Success Criteria:**
- [ ] All tests pass including performance benchmarks
- [ ] Code quality metrics meet standards
- [ ] SOLID principle compliance verified  
- [ ] Integration testing successful

### REFACTOR Phase Completion Checklist

**Quality Improvements Complete:**
- [ ] Schema definitions extracted and optimized
- [ ] Performance optimizations implemented and validated
- [ ] Error messages enhanced for user experience
- [ ] Documentation comprehensive and up-to-date

**Final Validation:**
```bash
# Complete test suite with performance
python -m pytest tests/unit/ -v --benchmark-only
# Expected: All tests pass, performance benchmarks met

# Type checking
mypy src/pkm/validators/
# Expected: No type errors

# Code quality
flake8 src/pkm/validators/
# Expected: No style violations  
```

---

## Implementation Timeline Summary

**Total Estimated Time:** 18-20 hours over 5 days

### Day 1: TDD RED Phase (4 hours)
- **Hours 1-2:** Required field validation tests (Task A1)
- **Hours 3-4:** Field format validation tests (Task A2)  
- **Deliverable:** 16 core test functions written and failing

### Day 2: TDD RED Phase Complete + GREEN Start (4 hours)  
- **Hours 1-1.5:** YAML parsing tests (Task B1)
- **Hour 1.5-2:** Integration tests (Task C1)
- **Hour 2-3.5:** Edge case tests (Task D1)
- **Hour 3.5-4:** Dependencies setup (Task E1-E2)
- **Deliverable:** All 22 tests written, dependencies installed

### Day 3: TDD GREEN Phase (4 hours)
- **Hours 1-3:** Core validation implementation (Tasks F1-F3)
- **Hour 3-4:** Integration and error handling (Tasks G1-G2)
- **Deliverable:** All tests passing, basic functionality complete

### Day 4: TDD REFACTOR Phase (3-4 hours)
- **Hour 1:** Schema extraction (Task H1)  
- **Hours 2-3:** Performance optimization (Task H2)
- **Hour 3-4:** Error message enhancement (Task H3)
- **Deliverable:** Production-quality implementation

### Day 5: Documentation & Finalization (2 hours)
- **Hour 1-1.5:** Documentation (Task I1)
- **Hour 1.5-2:** Final quality validation (Task I2)
- **Deliverable:** Complete, documented, production-ready feature

---

*This task breakdown provides the complete roadmap for implementing FR-VAL-002 following strict TDD methodology and maintaining the architectural excellence established in the PKM validation system foundation.*