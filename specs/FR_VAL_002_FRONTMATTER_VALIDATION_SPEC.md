# FR-VAL-002: YAML Frontmatter Validation Specification
*Following TDD → Specs-driven → FR-first → KISS → DRY → SOLID principles*

## Executive Summary

Implementation of comprehensive YAML frontmatter validation for PKM notes, ensuring structural integrity and consistency across the knowledge vault. This specification follows the ultra-thinking analysis recommendations and maintains the established architectural excellence.

## Functional Requirements (FR-VAL-002)

### FR-VAL-002.1: Required Field Validation ⭐ **Priority 1**
**Objective**: Ensure all notes contain mandatory frontmatter fields

**Requirements**:
- VAL-002.1.1: Validate presence of `date` field
- VAL-002.1.2: Validate presence of `type` field  
- VAL-002.1.3: Validate presence of `tags` field
- VAL-002.1.4: Validate presence of `status` field

**Acceptance Criteria**:
- [ ] Given note without `date` field, When validation runs, Then error reported with specific missing field
- [ ] Given note without `type` field, When validation runs, Then error reported with specific missing field
- [ ] Given note without `tags` field, When validation runs, Then error reported with specific missing field
- [ ] Given note without `status` field, When validation runs, Then error reported with specific missing field
- [ ] Given note with all required fields, When validation runs, Then no errors reported

### FR-VAL-002.2: Field Format Validation ⭐ **Priority 1**
**Objective**: Validate field data types and formats

**Requirements**:
- VAL-002.2.1: Validate `date` follows ISO format (YYYY-MM-DD)
- VAL-002.2.2: Validate `type` matches allowed enum values
- VAL-002.2.3: Validate `tags` is array of strings
- VAL-002.2.4: Validate `status` matches allowed enum values

**Acceptance Criteria**:
- [ ] Given date "2025-09-04", When validation runs, Then date format accepted
- [ ] Given date "invalid-date", When validation runs, Then date format error reported
- [ ] Given type "daily", When validation runs, Then type accepted
- [ ] Given type "invalid-type", When validation runs, Then type error reported
- [ ] Given tags ["research", "crypto"], When validation runs, Then tags accepted
- [ ] Given tags "not-array", When validation runs, Then tags format error reported

### FR-VAL-002.3: Optional Field Validation ⭐ **Priority 2**
**Objective**: Validate optional fields when present

**Requirements**:
- VAL-002.3.1: Validate `links` array format when present
- VAL-002.3.2: Validate `source` string when present
- VAL-002.3.3: Allow additional custom fields without error

**Acceptance Criteria**:
- [ ] Given links ["[[note1]]", "[[note2]]"], When validation runs, Then links accepted
- [ ] Given links "not-array", When validation runs, Then links format error reported
- [ ] Given custom field "project: example", When validation runs, Then no error reported

### FR-VAL-002.4: YAML Parsing Validation ⭐ **Priority 1**
**Objective**: Handle malformed YAML gracefully

**Requirements**:
- VAL-002.4.1: Detect missing frontmatter delimiters
- VAL-002.4.2: Handle invalid YAML syntax
- VAL-002.4.3: Report parsing errors with line numbers

**Acceptance Criteria**:
- [ ] Given file without frontmatter delimiters, When validation runs, Then missing delimiters error reported
- [ ] Given file with invalid YAML syntax, When validation runs, Then YAML syntax error reported with line number
- [ ] Given file with valid YAML, When validation runs, Then parsing succeeds

## Technical Specification

### Data Schema Definition

#### Required Frontmatter Schema
```yaml
---
date: "YYYY-MM-DD"              # ISO date format, required
type: "daily|zettel|project|area|resource|capture"  # Enum, required
tags: ["tag1", "tag2"]          # Array of strings, required  
status: "draft|active|review|complete|archived"     # Enum, required
---
```

#### Optional Fields Schema  
```yaml
---
# ... required fields above ...
links: ["[[note1]]", "[[note2]]"]    # Array of wiki-links, optional
source: "capture_command"             # String, optional  
author: "username"                    # String, optional
modified: "YYYY-MM-DD"               # ISO date, optional
---
```

### Implementation Architecture

#### Core Components (SOLID Design)

**1. FrontmatterValidator (Single Responsibility)**
```python
from src.pkm.validators.base import BaseValidator, ValidationResult
from pathlib import Path
from typing import List

class FrontmatterValidator(BaseValidator):
    """Validates YAML frontmatter using jsonschema - single responsibility"""
    
    def __init__(self, schema_path: Optional[Path] = None):
        self.schema = self._load_schema(schema_path)
    
    def validate(self, file_path: Path) -> List[ValidationResult]:
        """Validate YAML frontmatter in markdown file"""
        # Implementation following KISS principles
        pass
```

**2. FrontmatterSchema (Data Abstraction)**
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date

class FrontmatterSchema(BaseModel):
    """Type-safe frontmatter schema using Pydantic"""
    
    date: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')
    type: Literal["daily", "zettel", "project", "area", "resource", "capture"]
    tags: List[str]
    status: Literal["draft", "active", "review", "complete", "archived"]
    
    # Optional fields
    links: Optional[List[str]] = None
    source: Optional[str] = None
    author: Optional[str] = None
    modified: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}-\d{2}$')
```

**3. YAMLParser (Dependency Injection)**
```python
import yaml
from typing import Dict, Any, Optional

class YAMLParser:
    """YAML parsing utility - injectable dependency"""
    
    def parse_frontmatter(self, content: str) -> tuple[Dict[Any, Any], Optional[str]]:
        """Parse frontmatter from markdown content"""
        # Returns: (frontmatter_dict, error_message)
        pass
        
    def extract_frontmatter_section(self, content: str) -> tuple[str, Optional[str]]:
        """Extract frontmatter section from markdown"""
        # Returns: (frontmatter_yaml, error_message)
        pass
```

### Dependencies

#### Required Dependencies
```toml
[tool.poetry.dependencies]
python = "^3.9"
jsonschema = "^4.17.0"      # JSON Schema validation
pydantic = "^2.0.0"         # Type-safe data validation  
pyyaml = "^6.0"             # YAML parsing
```

#### Dependency Integration Strategy
- **jsonschema**: Core validation engine for schema compliance
- **pydantic**: Type-safe models with automatic validation
- **pyyaml**: Safe YAML parsing with error handling
- **Integration**: Layered approach - pyyaml → pydantic → jsonschema

### Error Handling Strategy

#### Error Categories and Responses
```python
# File structure errors
ValidationResult(rule="missing-frontmatter", severity="error", 
                message="No frontmatter found in file")

# YAML parsing errors  
ValidationResult(rule="yaml-syntax-error", severity="error",
                message="Invalid YAML syntax at line 5", line_number=5)

# Schema validation errors
ValidationResult(rule="missing-required-field", severity="error", 
                message="Required field 'date' is missing")

ValidationResult(rule="invalid-field-format", severity="error",
                message="Field 'date' must be in YYYY-MM-DD format")

# Type validation errors
ValidationResult(rule="invalid-field-type", severity="error",
                message="Field 'tags' must be an array of strings")
```

## TDD Implementation Plan

### Phase 1: RED (Write Failing Tests) - Day 1

#### Test Categories
1. **Basic Functionality Tests (8 tests)**
   - Valid frontmatter acceptance
   - Required field validation  
   - Field format validation
   - YAML parsing validation

2. **Edge Case Tests (6 tests)**
   - Missing frontmatter delimiters
   - Malformed YAML syntax
   - Empty files and permission errors
   - Unicode and special characters

3. **Integration Tests (4 tests)**
   - Integration with PKMValidationRunner
   - Multiple file validation
   - Error accumulation and reporting
   - Performance with large files

4. **Error Handling Tests (4 tests)**
   - Graceful failure modes
   - Informative error messages
   - Line number reporting
   - Recovery from parsing errors

**Total: 22 comprehensive tests covering all acceptance criteria**

### Phase 2: GREEN (Minimal Implementation) - Day 2

#### Implementation Order (KISS Approach)
1. **Basic YAML Parsing** - Minimal frontmatter extraction
2. **Schema Validation** - Core required fields only  
3. **Error Reporting** - Basic ValidationResult creation
4. **Integration** - Plugin into PKMValidationRunner

#### Minimal Implementation Strategy
```python
class FrontmatterValidator(BaseValidator):
    def validate(self, file_path: Path) -> List[ValidationResult]:
        """MINIMAL implementation - just enough to pass tests"""
        try:
            content = file_path.read_text()
            frontmatter = self._extract_frontmatter(content)
            return self._validate_frontmatter(frontmatter, file_path)
        except Exception as e:
            return [ValidationResult(
                file_path=file_path, rule="parse-error", 
                severity="error", message=str(e)
            )]
    
    def _extract_frontmatter(self, content: str) -> dict:
        """Extract frontmatter - minimal implementation"""
        # Just enough logic to pass tests
        pass
        
    def _validate_frontmatter(self, frontmatter: dict, file_path: Path) -> List[ValidationResult]:
        """Validate frontmatter - minimal implementation"""
        # Just enough validation to pass tests
        pass
```

### Phase 3: REFACTOR (Quality & Performance) - Day 3

#### Refactoring Priorities
1. **Extract Schema Definitions** - Move to separate module
2. **Optimize YAML Parsing** - Add caching and performance improvements
3. **Enhance Error Messages** - Detailed, actionable error descriptions
4. **Add Type Safety** - Complete type hints and validation
5. **Documentation** - Comprehensive docstrings and examples

#### Quality Improvements
- **DRY**: Extract common validation patterns
- **SOLID**: Ensure single responsibility maintained
- **Performance**: Benchmark and optimize bottlenecks
- **Maintainability**: Clear function names and documentation

## Performance Requirements

### Benchmarks
- **Processing Speed**: ≥100 files/second
- **Memory Usage**: <50MB for 1000 files
- **Error Recovery**: <1ms per validation error
- **YAML Parsing**: <5ms per file average

### Optimization Strategies
- **Lazy Loading**: Load schema once, reuse across validations
- **Early Failure**: Stop validation on first critical error when appropriate
- **Caching**: Cache parsed YAML for repeated validations
- **Streaming**: Process files individually to minimize memory usage

## Quality Gates

### Definition of Done
- [ ] All 22 tests passing (100% test coverage)
- [ ] TDD compliance verified (tests written first)
- [ ] SOLID principles validated through design review
- [ ] KISS compliance confirmed (functions ≤20 lines)
- [ ] Performance benchmarks met
- [ ] Integration tests passing with PKMValidationRunner
- [ ] Error handling comprehensive and informative
- [ ] Documentation complete with examples

### Success Criteria
- [ ] **Functional Complete**: All FR-VAL-002 requirements implemented
- [ ] **Quality Assured**: Code review and static analysis passing  
- [ ] **Performance Validated**: All benchmarks met or exceeded
- [ ] **Integration Tested**: Seamless operation with existing system
- [ ] **User Experience**: Clear, actionable error messages
- [ ] **Maintainable**: Clean code following all established principles

## File Structure

### Implementation Files
```
src/pkm/validators/
├── __init__.py
├── base.py                    # Existing
├── runner.py                  # Existing  
├── frontmatter_validator.py   # NEW - Main validator
├── schemas/
│   ├── __init__.py           # NEW
│   └── frontmatter_schema.py  # NEW - Schema definitions
└── utils/
    ├── __init__.py           # NEW
    └── yaml_parser.py        # NEW - YAML utilities

tests/unit/validators/
├── test_validation_base_fr_val_001.py      # Existing
├── test_frontmatter_validator_fr_val_002.py # NEW - Main tests
├── test_frontmatter_schema.py              # NEW - Schema tests
└── test_yaml_parser.py                     # NEW - Parser tests
```

### Integration Points
- **PKMValidationRunner**: Plugin via `add_validator(FrontmatterValidator())`
- **Schema Definitions**: Centralized in `schemas/` module
- **Error Handling**: Consistent with existing ValidationResult pattern
- **Testing**: Follows established TDD patterns and conventions

---

*This specification provides the complete roadmap for implementing FR-VAL-002 following ultra-thinking analysis recommendations and maintaining architectural excellence established in the PKM validation system foundation.*