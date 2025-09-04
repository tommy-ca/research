# PKM Validation System Specification
*Following TDD → Specs-driven → FR-first → KISS → DRY → SOLID principles*

## Overview

A comprehensive validation system for Personal Knowledge Management (PKM) vaults that ensures content quality, structural integrity, and organizational consistency while maintaining KISS architecture principles.

## Functional Requirements (FR) - Implementation Priority

### FR-VAL-001: Markdown Content Validation ⭐ **Priority 1**
**Objective**: Validate markdown syntax and structure consistency

**Requirements**:
- VAL-001.1: Validate markdown syntax using PyMarkdown
- VAL-001.2: Check heading hierarchy (H1 → H2 → H3, no skipping)
- VAL-001.3: Validate list formatting and consistency
- VAL-001.4: Check for trailing whitespace and line ending consistency

**Acceptance Criteria**:
- [ ] Given a markdown file with syntax errors, When validation runs, Then specific errors are reported
- [ ] Given a file with proper markdown, When validation runs, Then no errors are reported
- [ ] Given files with inconsistent formatting, When validation runs, Then formatting issues are identified

**Test Cases**:
1. Test valid markdown returns no errors
2. Test broken headers report specific issues  
3. Test malformed lists are caught
4. Test trailing whitespace detection

### FR-VAL-002: YAML Frontmatter Validation ⭐ **Priority 1**
**Objective**: Ensure all notes have valid, consistent frontmatter

**Requirements**:
- VAL-002.1: Validate required fields (date, type, tags, status)
- VAL-002.2: Check field types and formats (date format, valid enums)
- VAL-002.3: Validate tag consistency across vault
- VAL-002.4: Ensure frontmatter YAML syntax is correct

**Acceptance Criteria**:
- [ ] Given note with missing required fields, When validation runs, Then missing fields are reported
- [ ] Given note with invalid date format, When validation runs, Then date format error is reported
- [ ] Given note with invalid note type, When validation runs, Then type error is reported

**Test Cases**:
1. Test valid frontmatter passes validation
2. Test missing required fields are caught
3. Test invalid date formats are caught
4. Test invalid note types are caught

### FR-VAL-003: Wiki-Link Validation ⭐ **Priority 2**
**Objective**: Ensure all internal [[wiki-style]] links resolve to existing notes

**Requirements**:
- VAL-003.1: Find all [[wiki-style]] links in content
- VAL-003.2: Check if linked files exist in vault
- VAL-003.3: Report broken internal links
- VAL-003.4: Support multiple note locations (permanent/, daily/, etc.)

**Acceptance Criteria**:
- [ ] Given note with valid wiki links, When validation runs, Then no link errors are reported
- [ ] Given note with broken wiki link, When validation runs, Then broken link is identified
- [ ] Given note with links to different vault sections, When validation runs, Then all locations are checked

**Test Cases**:
1. Test valid wiki links pass validation
2. Test broken wiki links are reported
3. Test links across different vault sections work
4. Test case sensitivity handling

### FR-VAL-004: PKM Structure Validation ⭐ **Priority 2**
**Objective**: Validate vault follows PARA method and organizational standards

**Requirements**:
- VAL-004.1: Check required PARA directories exist (01-projects, 02-areas, 03-resources, 04-archives)
- VAL-004.2: Validate file naming conventions by section
- VAL-004.3: Check for orphaned files outside proper structure
- VAL-004.4: Validate daily note naming (YYYY-MM-DD.md)
- VAL-004.5: Validate zettel naming (YYYYMMDDHHmm-title-slug.md)

**Acceptance Criteria**:
- [ ] Given properly structured vault, When validation runs, Then no structure errors are reported
- [ ] Given missing PARA directories, When validation runs, Then missing directories are reported
- [ ] Given improperly named files, When validation runs, Then naming violations are reported

**Test Cases**:
1. Test complete PARA structure passes validation
2. Test missing directories are caught
3. Test invalid file naming is caught
4. Test orphaned files are identified

### FR-VAL-005: External Link Validation ⭐ **Priority 3** (DEFER initially)
**Objective**: Validate external HTTP/HTTPS links are accessible

**Requirements**:
- VAL-005.1: Find all external links in content
- VAL-005.2: Check HTTP status codes
- VAL-005.3: Report broken external links
- VAL-005.4: Support timeout configuration

**Acceptance Criteria**:
- [ ] Given note with valid external links, When validation runs, Then no link errors are reported
- [ ] Given note with broken external links, When validation runs, Then broken links are reported

## Non-Functional Requirements (NFR) - DEFER Phase 1

### NFR-VAL-001: Performance (DEFER)
- Validate 1000+ files within 30 seconds
- Memory usage < 500MB for large vaults

### NFR-VAL-002: Configurability (DEFER)
- YAML configuration file for rules
- Ability to disable specific validation rules

### NFR-VAL-003: Integration (DEFER)
- CLI command interface
- Git pre-commit hook support

## Architecture Design - KISS Principles

### Core Components

#### 1. ValidationResult (Simple Data Structure)
```python
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class ValidationResult:
    file_path: Path
    rule: str
    severity: str  # "error" | "warning" | "info"
    message: str
    line_number: Optional[int] = None
```

#### 2. BaseValidator (Abstract Interface)
```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, file_path: Path) -> List[ValidationResult]:
        """Validate single file and return results"""
        pass
```

#### 3. Concrete Validators (Single Responsibility)
```python
class MarkdownValidator(BaseValidator):
    """Validates markdown syntax using PyMarkdown"""
    
class FrontmatterValidator(BaseValidator):  
    """Validates YAML frontmatter using jsonschema"""
    
class WikiLinkValidator(BaseValidator):
    """Validates [[wiki-style]] internal links"""
    
class StructureValidator(BaseValidator):
    """Validates PKM vault structure and naming"""
```

#### 4. PKMValidationRunner (Orchestrator)
```python
class PKMValidationRunner:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.validators = []
    
    def add_validator(self, validator: BaseValidator):
        self.validators.append(validator)
    
    def validate_vault(self) -> List[ValidationResult]:
        results = []
        for file_path in self.vault_path.rglob("*.md"):
            for validator in self.validators:
                results.extend(validator.validate(file_path))
        return results
```

### Dependencies
```toml
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.9"
pymarkdown = "^0.9.0"        # Markdown linting
jsonschema = "^4.17.0"       # YAML validation
pydantic = "^2.0.0"          # Type-safe validation
pyyaml = "^6.0"              # YAML parsing

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
pytest-cov = "^4.0.0"
```

### File Structure
```
src/pkm/validators/
├── __init__.py
├── base.py                 # BaseValidator, ValidationResult
├── markdown_validator.py   # MarkdownValidator
├── frontmatter_validator.py # FrontmatterValidator  
├── wiki_link_validator.py  # WikiLinkValidator
├── structure_validator.py  # StructureValidator
└── runner.py              # PKMValidationRunner

tests/unit/validators/
├── test_markdown_validator.py
├── test_frontmatter_validator.py
├── test_wiki_link_validator.py
├── test_structure_validator.py
└── test_runner.py
```

## TDD Implementation Plan

### Phase 1: Core Infrastructure (Week 1)
1. **Write tests FIRST** for ValidationResult and BaseValidator
2. **Implement** basic data structures
3. **Write tests** for PKMValidationRunner  
4. **Implement** runner with empty validator list

### Phase 2: Markdown Validation (Week 1)
1. **Write tests FIRST** for MarkdownValidator
2. **Implement** PyMarkdown integration
3. **Refactor** for simplicity and performance
4. **Add** to runner and validate integration

### Phase 3: Frontmatter Validation (Week 2)  
1. **Write tests FIRST** for FrontmatterValidator
2. **Implement** jsonschema-based validation
3. **Add** Pydantic models for type safety
4. **Integrate** and test end-to-end

### Phase 4: Wiki-Link Validation (Week 2)
1. **Write tests FIRST** for WikiLinkValidator
2. **Implement** regex-based link extraction
3. **Add** file existence checking logic
4. **Handle** edge cases (case sensitivity, multiple locations)

### Phase 5: Structure Validation (Week 3)
1. **Write tests FIRST** for StructureValidator
2. **Implement** PARA directory checking
3. **Add** file naming convention validation
4. **Validate** complete vault structure

## Success Criteria

### Definition of Done
- [ ] All FR-VAL-001 through FR-VAL-004 implemented and tested
- [ ] 100% test coverage for all validators
- [ ] All tests passing in CI/CD pipeline
- [ ] Performance benchmarks met (≥100 files/second)
- [ ] KISS principle validated (functions ≤20 lines)
- [ ] Documentation complete with usage examples

### Quality Gates
- [ ] **TDD Compliance**: No code without tests first
- [ ] **KISS Validation**: All functions simple and readable
- [ ] **FR-First**: All functional requirements before non-functional
- [ ] **Error Handling**: Graceful failure with helpful messages
- [ ] **Type Safety**: Full type hints and validation

## Future Enhancements (Post-MVP)

### Phase 2 Features
- Content quality validation (readability scores)
- Grammar checking integration
- Custom rule configuration
- Performance optimization
- CLI interface
- Git hook integration

### Advanced Features
- Real-time validation during editing
- Batch processing optimization
- Machine learning-based content suggestions
- Integration with popular PKM tools
- Web interface for validation results

---

*This specification follows TDD → Specs-driven → FR-first → KISS → DRY → SOLID principles for maintainable, high-quality PKM validation system.*