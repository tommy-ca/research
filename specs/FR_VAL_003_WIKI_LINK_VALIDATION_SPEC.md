# FR-VAL-003: Wiki-Link Validation Specification
*Following TDD → Specs-driven → FR-first → KISS → DRY → SOLID principles*

## Executive Summary

Implementation of comprehensive wiki-link validation for PKM notes, ensuring knowledge graph integrity and connectivity across the vault. This specification builds on the architectural excellence established in FR-VAL-002 and maintains the same systematic development approach.

## Strategic Context

### Why FR-VAL-003 Now?
**Optimal Next Component** based on ultra-thinking analysis:
- **Foundation Ready**: FR-VAL-002 provides structural integrity, wiki-links provide connectivity
- **High User Value**: Broken links destroy PKM system trust and create cognitive friction
- **Low Implementation Risk**: Well-defined problem with deterministic success criteria
- **Architecture Synergy**: Perfect fit with existing BaseValidator and PKMValidationRunner

### User Value Proposition
- **Knowledge Graph Integrity**: Maintain reliable connections between notes
- **Refactoring Confidence**: Enable safe knowledge restructuring without breaking links
- **System Health Monitoring**: Quantifiable PKM quality with link integrity metrics
- **Time Savings**: Eliminate 15-30 minutes/day of manual link verification

## Functional Requirements (FR-VAL-003)

### FR-VAL-003.1: Wiki-Link Extraction ⭐ **Priority 1**
**Objective**: Accurately extract all wiki-style links from markdown content

**Requirements**:
- VAL-003.1.1: Extract basic wiki-links `[[note-title]]`
- VAL-003.1.2: Extract display-text wiki-links `[[note-title|Display Text]]`
- VAL-003.1.3: Extract path-based wiki-links `[[folder/subfolder/note-title]]`
- VAL-003.1.4: Handle Unicode characters in link targets
- VAL-003.1.5: Normalize whitespace in link targets

**Acceptance Criteria**:
- [ ] Given content with `[[simple-link]]`, When extraction runs, Then WikiLink("simple-link") returned
- [ ] Given content with `[[target|Display]]`, When extraction runs, Then WikiLink("target", "Display") returned
- [ ] Given content with `[[folder/note]]`, When extraction runs, Then WikiLink("folder/note") returned
- [ ] Given content with `[[ spaced link ]]`, When extraction runs, Then WikiLink("spaced link") returned
- [ ] Given content with `[[café-notes]]`, When extraction runs, Then WikiLink("café-notes") returned
- [ ] Given content with incomplete `[[broken`, When extraction runs, Then no WikiLink objects returned

**Test Cases**:
1. Test basic link extraction from simple markdown
2. Test multiple links in single file
3. Test links with display text
4. Test nested folder paths
5. Test Unicode and special characters
6. Test malformed link handling

### FR-VAL-003.2: File Resolution ⭐ **Priority 1**
**Objective**: Locate target files for extracted wiki-links within vault structure

**Requirements**:
- VAL-003.2.1: Resolve links relative to current file location
- VAL-003.2.2: Search PARA method directories (01-projects, 02-areas, 03-resources, 04-archives)
- VAL-003.2.3: Search permanent notes directory structure
- VAL-003.2.4: Support multiple file extensions (.md, .txt, .markdown)
- VAL-003.2.5: Handle case-insensitive matching for cross-platform compatibility
- VAL-003.2.6: Support nested directory navigation

**Acceptance Criteria**:
- [ ] Given link `[[note]]` and file `note.md` in same directory, When resolution runs, Then file found
- [ ] Given link `[[project-note]]` and file `02-projects/project/project-note.md`, When resolution runs, Then file found
- [ ] Given link `[[Note]]` and file `note.md` (case difference), When resolution runs, Then file found
- [ ] Given link `[[folder/note]]` and file structure `folder/note.md`, When resolution runs, Then file found
- [ ] Given link `[[nonexistent]]` with no matching file, When resolution runs, Then None returned

**Test Cases**:
1. Test exact filename matching
2. Test case-insensitive matching
3. Test PARA directory search priority
4. Test nested path resolution
5. Test multiple file extension support
6. Test missing file detection

### FR-VAL-003.3: Link Validation ⭐ **Priority 1**
**Objective**: Validate that all extracted wiki-links resolve to existing files

**Requirements**:
- VAL-003.3.1: Report broken links (target file not found)
- VAL-003.3.2: Report ambiguous links (multiple potential targets)
- VAL-003.3.3: Provide clear, actionable error messages
- VAL-003.3.4: Include line numbers for broken links when possible
- VAL-003.3.5: Suggest similar filenames for broken links

**Acceptance Criteria**:
- [ ] Given file with broken link `[[missing]]`, When validation runs, Then ValidationResult with error returned
- [ ] Given file with valid links only, When validation runs, Then empty ValidationResult returned
- [ ] Given broken link, When validation runs, Then error message includes link text and suggestions
- [ ] Given ambiguous link matching multiple files, When validation runs, Then warning with options returned

**Test Cases**:
1. Test validation of files with all valid links
2. Test detection of broken links
3. Test error message quality and clarity
4. Test suggestion generation for typos
5. Test handling of ambiguous link targets

### FR-VAL-003.4: Performance Optimization ⭐ **Priority 2**
**Objective**: Ensure wiki-link validation scales efficiently with vault size

**Requirements**:
- VAL-003.4.1: Cache file system directory listings
- VAL-003.4.2: Index vault structure for fast lookups
- VAL-003.4.3: Process files concurrently when possible
- VAL-003.4.4: Limit memory usage for large vaults

**Acceptance Criteria**:
- [ ] Given vault with 100 files, When validation runs, Then completes in <500ms
- [ ] Given vault with 1000 files, When validation runs, Then memory usage <100MB
- [ ] Given repeated validations, When cache enabled, Then subsequent runs faster

**Test Cases**:
1. Test performance with small vaults (≤100 files)
2. Test performance with medium vaults (≤1000 files)
3. Test memory usage during validation
4. Test caching effectiveness

## Technical Specification

### Data Models

#### WikiLink Data Structure
```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class WikiLink:
    """Immutable representation of a wiki-style link"""
    target: str                    # Link target (note-title or folder/note-title)
    display_text: Optional[str]    # Optional display text for [[target|display]]
    line_number: Optional[int]     # Line number where link appears
    column_start: Optional[int]    # Starting column position
    column_end: Optional[int]      # Ending column position
    
    @property
    def is_path_based(self) -> bool:
        """True if link contains path separators"""
        return '/' in self.target
    
    @property
    def normalized_target(self) -> str:
        """Target with normalized whitespace"""
        return self.target.strip()
```

#### VaultIndex Data Structure
```python
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

@dataclass
class VaultIndex:
    """Cached index of vault file structure for fast lookups"""
    file_map: Dict[str, List[Path]]      # filename -> list of file paths
    directory_structure: Dict[Path, Set[str]]  # directory -> set of filenames
    last_updated: float                   # timestamp of last index update
    
    def lookup_file(self, filename: str) -> List[Path]:
        """Find all files matching the given filename"""
        return self.file_map.get(filename.lower(), [])
    
    def needs_refresh(self, max_age_seconds: int = 300) -> bool:
        """True if index needs refreshing based on age"""
        import time
        return (time.time() - self.last_updated) > max_age_seconds
```

### Implementation Architecture

#### Core Components (SOLID Design)

**1. WikiLinkExtractor (Single Responsibility)**
```python
from typing import List, Iterator
import re
from pathlib import Path

class WikiLinkExtractor:
    """Extracts wiki-style links from markdown content - single responsibility"""
    
    def __init__(self):
        # Pre-compiled regex patterns for performance
        self._patterns = {
            'display': re.compile(r'\[\[([^|]+)\|([^\]]+)\]\]'),  # [[target|display]]
            'basic': re.compile(r'\[\[([^\]]+)\]\]'),             # [[target]]
        }
    
    def extract_from_content(self, content: str) -> List[WikiLink]:
        """Extract all wiki-links from markdown content"""
        # Implementation following KISS principles
        pass
    
    def extract_from_file(self, file_path: Path) -> List[WikiLink]:
        """Extract all wiki-links from markdown file with line numbers"""
        # Implementation with line number tracking
        pass
```

**2. VaultFileResolver (Single Responsibility)**
```python
from typing import Optional, List
from pathlib import Path

class VaultFileResolver:
    """Resolves wiki-link targets to actual file paths - single responsibility"""
    
    def __init__(self, vault_root: Path, config: ResolverConfig):
        self.vault_root = vault_root
        self.config = config
        self._index: Optional[VaultIndex] = None
    
    def resolve_link(self, link: WikiLink, current_file: Path) -> Optional[Path]:
        """Resolve wiki-link to file path using search strategy"""
        # Implementation with PARA-aware search
        pass
    
    def build_index(self) -> VaultIndex:
        """Build searchable index of vault files"""
        # Implementation with performance optimization
        pass
```

**3. WikiLinkValidator (Orchestration)**
```python
from src.pkm.validators.base import BaseValidator, ValidationResult

class WikiLinkValidator(BaseValidator):
    """
    Validates wiki-link integrity using dependency injection.
    
    Follows SOLID principles:
    - Single Responsibility: Only validates wiki-links
    - Open/Closed: Extensible through injected dependencies
    - Dependency Inversion: Depends on abstractions (extractor, resolver)
    """
    
    def __init__(self, 
                 extractor: WikiLinkExtractor,
                 resolver: VaultFileResolver,
                 config: ValidationConfig):
        """Initialize with injected dependencies"""
        self.extractor = extractor
        self.resolver = resolver
        self.config = config
    
    def validate(self, file_path: Path) -> List[ValidationResult]:
        """Validate wiki-links in markdown file"""
        # Implementation following established patterns
        pass
```

### Search Strategy Implementation

#### Hierarchical File Resolution
```python
def resolve_link_with_strategy(self, link: WikiLink, current_file: Path) -> Optional[Path]:
    """Multi-step resolution strategy for maximum compatibility"""
    
    search_locations = [
        # 1. Relative to current file (highest priority)
        self._search_relative_to_file(link, current_file),
        
        # 2. PARA method directories (organized by priority)
        self._search_para_directories(link),
        
        # 3. Permanent notes structure
        self._search_permanent_notes(link),
        
        # 4. Full vault search (lowest priority, highest cost)
        self._search_entire_vault(link)
    ]
    
    for search_result in search_locations:
        if search_result:
            return search_result
    
    return None  # Link target not found
```

#### PARA Method Integration
```python
def _search_para_directories(self, link: WikiLink) -> Optional[Path]:
    """Search PARA method directories in priority order"""
    para_directories = [
        "02-projects",      # Active projects (highest priority)  
        "03-areas",         # Ongoing responsibilities
        "04-resources",     # Reference materials
        "05-archives"       # Historical content (lowest priority)
    ]
    
    for para_dir in para_directories:
        result = self._search_directory_tree(
            self.vault_root / para_dir, 
            link.normalized_target
        )
        if result:
            return result
    
    return None
```

### Error Message Enhancement

#### Suggestion System Implementation
```python
from difflib import SequenceMatcher
from typing import List, Tuple

class LinkSuggestionEngine:
    """Generates helpful suggestions for broken wiki-links"""
    
    def suggest_alternatives(self, broken_link: str, available_files: List[Path]) -> List[str]:
        """Generate "Did you mean..." suggestions"""
        candidates = []
        
        for file_path in available_files:
            filename = file_path.stem
            similarity = self._calculate_similarity(broken_link, filename)
            
            if similarity > 0.6:  # 60% similarity threshold
                candidates.append((filename, similarity))
        
        # Return top 3 suggestions, sorted by similarity
        return [name for name, _ in sorted(candidates, key=lambda x: x[1], reverse=True)[:3]]
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
```

#### Enhanced Error Messages
```python
def format_broken_link_error(self, link: WikiLink, file_path: Path, suggestions: List[str]) -> str:
    """Create detailed, actionable error message"""
    base_message = f"Broken wiki-link: [[{link.target}]]"
    
    if link.line_number:
        base_message += f" at line {link.line_number}"
    
    if suggestions:
        suggestion_text = ", ".join(f"[[{s}]]" for s in suggestions[:3])
        base_message += f"\n💡 Did you mean: {suggestion_text}?"
    
    return base_message
```

## TDD Implementation Plan

### Phase 1: RED (Write Failing Tests) - Day 1

#### Test Categories (15 comprehensive tests)

**1. Wiki-Link Extraction Tests (5 tests)**
```python
class TestWikiLinkExtraction:
    def test_extract_basic_wiki_links():
        content = "See [[my-note]] for details."
        links = extract_wiki_links(content)
        assert len(links) == 1
        assert links[0].target == "my-note"
        assert links[0].display_text is None
    
    def test_extract_display_text_links():
        content = "Check [[project-plan|Project Plan]] here."
        links = extract_wiki_links(content)
        assert links[0].target == "project-plan"
        assert links[0].display_text == "Project Plan"
    
    def test_extract_path_based_links():
        content = "Reference [[projects/crypto/analysis]]."
        links = extract_wiki_links(content)
        assert links[0].target == "projects/crypto/analysis"
        assert links[0].is_path_based == True
    
    def test_extract_multiple_links():
        content = "See [[note1]] and [[note2]] and [[folder/note3]]."
        links = extract_wiki_links(content)
        assert len(links) == 3
        assert {link.target for link in links} == {"note1", "note2", "folder/note3"}
    
    def test_ignore_malformed_links():
        content = "Ignore [[incomplete and [single] and normal text."
        links = extract_wiki_links(content)
        assert len(links) == 0
```

**2. File Resolution Tests (5 tests)**
```python
class TestFileResolution:
    def test_resolve_same_directory_file():
        # Given: link [[note]] and note.md in same directory
        # When: resolve_link called
        # Then: returns path to note.md
    
    def test_resolve_para_directory_file():
        # Given: link [[project-note]] and 02-projects/project/project-note.md
        # When: resolve_link called  
        # Then: returns path to project-note.md
    
    def test_resolve_case_insensitive():
        # Given: link [[Note]] and note.md (different case)
        # When: resolve_link called
        # Then: returns path to note.md
    
    def test_resolve_nested_path():
        # Given: link [[folder/subfolder/note]] and matching structure
        # When: resolve_link called
        # Then: returns correct nested file path
    
    def test_resolve_missing_file():
        # Given: link [[nonexistent]] with no matching file
        # When: resolve_link called
        # Then: returns None
```

**3. Integration Tests (3 tests)**
```python
class TestWikiLinkValidatorIntegration:
    def test_validate_file_with_valid_links():
        # Given: file with all valid wiki-links
        # When: WikiLinkValidator.validate() called
        # Then: returns empty ValidationResult list
    
    def test_validate_file_with_broken_links():
        # Given: file with broken wiki-links
        # When: WikiLinkValidator.validate() called
        # Then: returns ValidationResult with errors
    
    def test_integration_with_pkm_validation_runner():
        # Given: WikiLinkValidator added to PKMValidationRunner
        # When: runner.validate_vault() called
        # Then: wiki-link validation included in results
```

**4. Edge Case Tests (2 tests)**
```python
class TestEdgeCases:
    def test_unicode_wiki_links():
        # Given: content with [[café-notes]] Unicode link
        # When: extraction and resolution run
        # Then: handles Unicode correctly
    
    def test_wiki_links_with_special_characters():
        # Given: links with spaces, symbols: [[notes & ideas!]]
        # When: extraction and resolution run
        # Then: processes correctly
```

### Phase 2: GREEN (Minimal Implementation) - Day 2

#### Implementation Order (KISS Approach)
1. **Basic Link Extraction** - Simple regex for `[[text]]`
2. **Basic File Resolution** - Check same directory first
3. **Basic Validation** - Report broken links as errors
4. **Integration** - Plugin into PKMValidationRunner

#### Minimal Implementation Strategy
```python
# 1. Minimal WikiLinkExtractor
class WikiLinkExtractor:
    def extract_from_content(self, content: str) -> List[WikiLink]:
        import re
        pattern = r'\[\[([^\]]+)\]\]'
        matches = re.findall(pattern, content)
        return [WikiLink(target=match) for match in matches]

# 2. Minimal VaultFileResolver  
class VaultFileResolver:
    def resolve_link(self, link: WikiLink, current_file: Path) -> Optional[Path]:
        # Check same directory only
        candidate = current_file.parent / f"{link.target}.md"
        return candidate if candidate.exists() else None

# 3. Minimal WikiLinkValidator
class WikiLinkValidator(BaseValidator):
    def validate(self, file_path: Path) -> List[ValidationResult]:
        content = file_path.read_text()
        extractor = WikiLinkExtractor()
        resolver = VaultFileResolver()
        
        links = extractor.extract_from_content(content)
        results = []
        
        for link in links:
            if not resolver.resolve_link(link, file_path):
                results.append(ValidationResult(
                    file_path=file_path,
                    rule="broken-wiki-link",
                    severity="error",
                    message=f"Broken wiki-link: [[{link.target}]]"
                ))
        
        return results
```

### Phase 3: REFACTOR (Quality Implementation) - Day 3

#### Refactoring Priorities
1. **Enhanced Link Extraction** - Support display text and paths
2. **PARA-Aware Resolution** - Search project/area/resource directories
3. **Performance Optimization** - Caching and indexing
4. **Error Message Enhancement** - Suggestions and detailed feedback
5. **Configuration Support** - Configurable behavior

#### Quality Improvements
- **DRY**: Extract common patterns and utilities
- **SOLID**: Ensure dependency injection and single responsibility
- **Performance**: Add caching, pre-compiled regex, efficient search
- **Maintainability**: Clear interfaces and comprehensive documentation

## Performance Requirements

### Benchmarks
- **Link Extraction**: <5ms per file with 100 links
- **File Resolution**: <10ms per link lookup  
- **Batch Validation**: <500ms for 100 files with 1000 total links
- **Memory Usage**: <100MB for 1000-file vault
- **Cache Performance**: 2x speed improvement on repeated validations

### Optimization Strategies
- **Vault Indexing**: Build file index once, reuse for all lookups
- **Regex Compilation**: Pre-compile patterns for repeated use
- **Concurrent Processing**: Parallel file validation when beneficial
- **Memory Management**: Stream processing to avoid loading entire vault

## Quality Gates

### Definition of Done
- [ ] All 15 tests passing (100% test coverage)
- [ ] TDD compliance verified (tests written first)
- [ ] SOLID principles validated through design review  
- [ ] KISS compliance confirmed (functions ≤20 lines)
- [ ] Performance benchmarks met
- [ ] Integration tests passing with PKMValidationRunner
- [ ] Error handling comprehensive and informative
- [ ] Documentation complete with usage examples

### Success Criteria
- [ ] **Functional Complete**: All FR-VAL-003 requirements implemented
- [ ] **Quality Assured**: Code review and static analysis passing
- [ ] **Performance Validated**: All benchmarks met or exceeded
- [ ] **Integration Tested**: Seamless operation with existing system
- [ ] **User Experience**: Clear, actionable error messages with suggestions
- [ ] **Maintainable**: Clean code following all established principles

## File Structure

### Implementation Files
```
src/pkm/validators/
├── __init__.py
├── base.py                         # Existing
├── runner.py                       # Existing
├── frontmatter_validator.py        # Existing
├── wiki_link_validator.py          # NEW - Main validator
├── utils/
│   ├── __init__.py                # NEW
│   ├── wiki_link_extractor.py     # NEW - Link extraction utilities
│   ├── vault_resolver.py          # NEW - File resolution utilities
│   └── suggestion_engine.py       # NEW - Link suggestion utilities
└── schemas/
    ├── __init__.py                # Existing
    ├── frontmatter_schema.py      # Existing  
    └── wiki_link_schema.py        # NEW - WikiLink data models

tests/unit/validators/
├── test_validation_base_fr_val_001.py           # Existing
├── test_frontmatter_validator_fr_val_002.py     # Existing
├── test_wiki_link_validator_fr_val_003.py       # NEW - Main tests
├── test_wiki_link_extractor.py                 # NEW - Extraction tests
├── test_vault_resolver.py                      # NEW - Resolution tests
└── test_suggestion_engine.py                   # NEW - Suggestion tests
```

### Integration Points
- **PKMValidationRunner**: Plugin via `add_validator(WikiLinkValidator())`
- **Configuration**: Extend existing settings.json with wiki-link options
- **Error Handling**: Consistent with existing ValidationResult pattern
- **Testing**: Follows established TDD patterns and conventions

## Future Enhancements (Post-MVP)

### Phase 2 Features
- Link suggestion with fuzzy matching
- Auto-repair functionality for common typos
- Link graph analysis (orphaned notes, hub identification)
- Performance optimization for very large vaults (10k+ files)

### Advanced Features  
- Real-time link validation during editing
- Link format migration between PKM tools
- Circular reference detection and reporting
- Wiki-link usage analytics and insights

---

*This specification provides the complete roadmap for implementing FR-VAL-003 following the ultra-thinking analysis recommendations and maintaining the architectural excellence established in the PKM validation system. The systematic TDD approach ensures quality, maintainability, and user value delivery.*