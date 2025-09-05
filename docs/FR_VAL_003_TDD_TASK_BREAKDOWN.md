# FR-VAL-003 TDD Task Breakdown: Wiki-Link Validation

## Overview

This document provides actionable TDD tasks for implementing FR-VAL-003 Wiki-Link Validation following strict TDD methodology: RED → GREEN → REFACTOR.

## Development Principles

- **TDD First**: Write failing test before any implementation
- **SOLID Architecture**: Single responsibility, dependency injection, extensible design
- **KISS Implementation**: Functions ≤20 lines, clear naming, minimal complexity
- **DRY Patterns**: Centralized rules, reusable components, shared utilities
- **FR-First Prioritization**: User value before optimization

## TDD Phase Structure

### Phase 1: RED - Write Failing Tests First
Write comprehensive test suite that defines expected behavior. All tests must fail initially.

### Phase 2: GREEN - Minimal Implementation
Write simplest code to make tests pass. Focus on functionality over elegance.

### Phase 3: REFACTOR - Optimize & Extract
Improve code quality while maintaining passing tests. Extract schemas, optimize performance.

## Task Breakdown

### Task Group 1: Wiki-Link Extractor Component (TDD Cycle 1)

#### RED Phase Tasks
- **Task 1.1**: Write test for basic wiki-link pattern extraction
  - Test `[[Simple Link]]` extraction
  - Expected: `["Simple Link"]`

- **Task 1.2**: Write test for multi-word wiki-link extraction
  - Test `[[Multi Word Link]]` extraction
  - Expected: `["Multi Word Link"]`

- **Task 1.3**: Write test for multiple wiki-links in content
  - Test content with `[[Link One]]` and `[[Link Two]]`
  - Expected: `["Link One", "Link Two"]`

- **Task 1.4**: Write test for wiki-links with aliases
  - Test `[[Target Note|Display Text]]` extraction
  - Expected: `["Target Note"]` (extract target, not alias)

- **Task 1.5**: Write test for invalid wiki-link patterns
  - Test single brackets `[Invalid Link]`
  - Expected: `[]` (empty list)

- **Task 1.6**: Write test for nested brackets handling
  - Test `[[Note with [brackets] inside]]`
  - Expected: `["Note with [brackets] inside"]`

#### GREEN Phase Tasks
- **Task 1.7**: Implement `WikiLinkExtractor` class
  - Create minimal class with `extract_links(content: str) -> List[str]` method
  - Use simple regex pattern to make tests pass

- **Task 1.8**: Implement basic wiki-link regex pattern
  - Pattern: `r'\[\[([^\]]+)\]\]'`
  - Handle alias splitting with `|` character

#### REFACTOR Phase Tasks
- **Task 1.9**: Extract regex patterns to constants
  - Move patterns to `WikiLinkPatterns` class for reuse
  - Pre-compile regex for performance

- **Task 1.10**: Add comprehensive edge case handling
  - Empty content, whitespace handling, malformed links
  - Performance optimization with compiled patterns

### Task Group 2: Vault File Resolver Component (TDD Cycle 2)

#### RED Phase Tasks
- **Task 2.1**: Write test for exact filename resolution
  - Given link `"Test Note"`, expect `vault/permanent/notes/test-note.md`
  - Test case-insensitive matching

- **Task 2.2**: Write test for multiple file format resolution
  - Test resolving links to `.md`, `.txt`, `.org` files
  - Priority order: `.md` > `.txt` > `.org`

- **Task 2.3**: Write test for directory traversal resolution
  - Test resolving links across vault subdirectories
  - Search in: `permanent/notes/`, `02-projects/`, `03-areas/`, `04-resources/`

- **Task 2.4**: Write test for ambiguous link resolution
  - Given multiple files matching pattern, return all matches
  - Test disambiguation requirements

- **Task 2.5**: Write test for non-existent file detection
  - Given link with no matching file, return empty result
  - Distinguish between "not found" and "ambiguous"

#### GREEN Phase Tasks
- **Task 2.6**: Implement `VaultFileResolver` class
  - Create minimal class with `resolve_link(link_text: str, vault_path: Path) -> List[Path]`
  - Basic file system traversal implementation

- **Task 2.7**: Implement filename normalization
  - Convert link text to filesystem-friendly format
  - Handle spaces, special characters, case sensitivity

#### REFACTOR Phase Tasks
- **Task 2.8**: Extract file resolution rules to configuration
  - `FileResolutionRules` class with search paths, extensions, priorities
  - Configurable search behavior

- **Task 2.9**: Add caching for performance optimization
  - Cache file system scans with LRU cache
  - Invalidation strategy for file changes

### Task Group 3: Wiki-Link Validator Integration (TDD Cycle 3)

#### RED Phase Tasks
- **Task 3.1**: Write test for complete validation workflow
  - Test file with valid wiki-links → no errors
  - Integration test with real file content

- **Task 3.2**: Write test for broken link detection
  - Test file with non-existent wiki-link → validation error
  - Error message includes link text and suggestions

- **Task 3.3**: Write test for ambiguous link detection
  - Test file with ambiguous wiki-link → validation warning
  - Warning includes all possible matches

- **Task 3.4**: Write test for empty link validation
  - Test file with `[[]]` empty links → validation error
  - Clear error message for empty links

- **Task 3.5**: Write test for duplicate link optimization
  - Test file with same link multiple times → single resolution
  - Performance optimization validation

#### GREEN Phase Tasks
- **Task 3.6**: Implement `WikiLinkValidator` class inheriting from `BaseValidator`
  - Override `validate(file_path: Path) -> List[ValidationResult]`
  - Integrate extractor and resolver components

- **Task 3.7**: Implement error message generation
  - Use centralized error templates
  - Include actionable suggestions for fixing links

#### REFACTOR Phase Tasks
- **Task 3.8**: Extract validation rules to schema
  - `WikiLinkValidationRules` class with error templates
  - Configurable severity levels and behavior

- **Task 3.9**: Add performance optimizations
  - Content hashing for caching validation results
  - Batch resolution of multiple links

### Task Group 4: Integration & Testing (TDD Cycle 4)

#### RED Phase Tasks
- **Task 4.1**: Write integration test with `PKMValidationRunner`
  - Test wiki-link validator integration with runner
  - Multiple files with mixed validation results

- **Task 4.2**: Write test for real PKM vault structure
  - Test with actual vault directory structure
  - Validate against real wiki-link patterns

- **Task 4.3**: Write performance benchmark tests
  - Test validation speed with large files (>1MB)
  - Test with high link density (>100 links per file)

#### GREEN Phase Tasks
- **Task 4.4**: Register `WikiLinkValidator` with validation runner
  - Add to default validator list
  - Configure for markdown file types only

- **Task 4.5**: Implement CLI integration
  - Add wiki-link validation to command line interface
  - Error reporting and summary statistics

#### REFACTOR Phase Tasks
- **Task 4.6**: Add configuration options
  - Enable/disable wiki-link validation
  - Configurable search paths and file types

- **Task 4.7**: Optimize memory usage for large vaults
  - Stream processing for large files
  - Lazy loading of file resolution cache

## Quality Gates

### Code Quality Requirements
- **Test Coverage**: ≥95% line coverage
- **Function Complexity**: Max cyclomatic complexity 5
- **Function Length**: ≤20 lines per function
- **Class Size**: ≤200 lines per class

### Performance Requirements
- **Single File Validation**: <100ms for files <10KB
- **Link Resolution**: <50ms for files with <50 links  
- **Memory Usage**: <50MB for vaults with <10,000 files

### Error Quality Requirements
- **Actionable Messages**: All errors include specific fix suggestions
- **Clear Context**: Error messages include file location and link text
- **Severity Levels**: Appropriate error/warning/info categorization

## Implementation Order

1. **Start with WikiLinkExtractor**: Foundational component, easiest to test
2. **Then VaultFileResolver**: Core business logic, file system operations
3. **Then WikiLinkValidator**: Integration component, ties together extractor and resolver
4. **Finally Integration**: Runner integration, CLI, performance optimization

## Success Criteria

### Phase Completion
- [ ] All tests passing (RED → GREEN achieved)
- [ ] Code coverage ≥95%
- [ ] Performance benchmarks met
- [ ] SOLID principles validated
- [ ] KISS principles enforced (function length, complexity)
- [ ] DRY principles applied (no duplication)

### Integration Success
- [ ] Wiki-link validator integrated with PKM validation runner
- [ ] CLI integration working
- [ ] Real vault validation successful
- [ ] Performance acceptable for typical PKM usage patterns

### Documentation
- [ ] API documentation complete
- [ ] Error message catalog documented
- [ ] Configuration options documented
- [ ] Usage examples provided

---

*This task breakdown ensures systematic TDD implementation of FR-VAL-003 while maintaining code quality and architectural principles.*