---
title: "PKM Process Inbox Command Specification"
date: 2024-08-22
type: specification
status: approved
priority: P0
tier: core
tags: [spec, pkm, inbox, tdd, fr-first, para-method]
created: 2024-08-22T22:00:00Z
updated: 2024-08-22T22:00:00Z
---

# Feature: PKM Process Inbox Command

## Overview
Automated inbox processing command that takes captured notes and categorizes them according to the PARA method (Projects, Areas, Resources, Archives), moving files to appropriate vault directories with enhanced metadata.

## Functional Requirements (IMPLEMENT NOW - Week 1)

#### FR-001: Read Inbox Items
- **Description**: Scan and read all files in `vault/00-inbox/`
- **Acceptance**: All .md files discovered and loaded
- **Priority**: P0 - Foundation requirement
- **Test**: `test_reads_all_inbox_files()`

#### FR-002: Extract Metadata
- **Description**: Parse frontmatter from each inbox item
- **Acceptance**: YAML frontmatter extracted as dictionary
- **Priority**: P0 - Foundation requirement
- **Test**: `test_extracts_frontmatter()`

#### FR-003: Categorize by PARA
- **Description**: Determine if item is Project, Area, Resource, or Archive
- **Acceptance**: Each item assigned a PARA category (01-projects, 02-areas, 03-resources, 04-archives)
- **Priority**: P0 - Core functionality
- **Test**: `test_categorizes_by_para()`

#### FR-004: Move to Target Folder
- **Description**: Move file to appropriate PARA folder
- **Acceptance**: File exists in new location, removed from inbox
- **Priority**: P0 - Core functionality
- **Test**: `test_moves_to_para_folder()`

#### FR-005: Update Frontmatter
- **Description**: Add processing metadata (processed_date, category, etc.)
- **Acceptance**: Frontmatter includes processing info
- **Priority**: P0 - Foundation requirement
- **Test**: `test_updates_frontmatter()`

#### FR-006: Generate Report
- **Description**: Return summary of processed items
- **Acceptance**: Report shows items processed and destinations
- **Priority**: P0 - Foundation requirement
- **Test**: `test_generates_report()`

### Non-Functional Requirements (PRIORITY: LOW - Defer to Week 4+)

#### NFR-001: Performance (DEFER)
- **Description**: Process 100 items in < 10 seconds
- **Rationale**: Current volume is < 10 items/day
- **Target Date**: Week 4 (if needed)

#### NFR-002: Concurrent Processing (DEFER)
- **Description**: Process multiple items in parallel
- **Rationale**: Sequential processing sufficient for MVP
- **Target Date**: Production phase

#### NFR-003: Error Recovery (DEFER)
- **Description**: Rollback on failure, maintain consistency
- **Rationale**: Manual recovery acceptable initially
- **Target Date**: Week 5

#### NFR-004: Metrics Tracking (DEFER)
- **Description**: Track processing time, success rate
- **Rationale**: Not critical for initial functionality
- **Target Date**: Monitoring phase

## Test Cases (TDD - Write These First!)

### Test Suite: ProcessInboxTests

```python
# Write these tests BEFORE implementation

def test_reads_all_inbox_files():
    """FR-001: Should discover all markdown files in inbox"""
    # Given: 3 files in inbox
    create_test_files(['file1.md', 'file2.md', 'file3.md'])
    
    # When: Process inbox
    result = process_inbox()
    
    # Then: All files processed
    assert result.files_found == 3
    assert all(f in result.files for f in ['file1.md', 'file2.md', 'file3.md'])

def test_categorizes_by_para():
    """FR-003: Should categorize based on content"""
    # Given: Files with different content types
    create_file('project.md', content='Project with deadline...')
    create_file('area.md', content='Ongoing responsibility...')
    create_file('resource.md', content='Reference material...')
    
    # When: Process inbox
    result = process_inbox()
    
    # Then: Correct categorization
    assert result.categorized['project.md'] == '01-projects'
    assert result.categorized['area.md'] == '02-areas'
    assert result.categorized['resource.md'] == '03-resources'

def test_moves_to_para_folder():
    """FR-004: Should move files to correct folders"""
    # Given: File categorized as project
    create_file('vault/00-inbox/task.md', type='project')
    
    # When: Process inbox
    result = process_inbox()
    
    # Then: File moved to projects
    assert not exists('vault/00-inbox/task.md')
    assert exists('vault/01-projects/task.md')

def test_empty_inbox():
    """Should handle empty inbox gracefully"""
    # Given: Empty inbox
    clear_inbox()
    
    # When: Process inbox
    result = process_inbox()
    
    # Then: Success with zero items
    assert result.success == True
    assert result.files_found == 0
    assert result.message == "Inbox is empty"

def test_malformed_frontmatter():
    """Should handle invalid YAML gracefully"""
    # Given: File with broken frontmatter
    create_file('bad.md', content='---\nbad yaml: [[\n---\n')
    
    # When: Process inbox
    result = process_inbox()
    
    # Then: File skipped with error logged
    assert result.errors['bad.md'] == 'Invalid frontmatter'
    assert exists('vault/00-inbox/bad.md')  # Not moved
```

## Implementation Plan (Following TDD)

### Phase 1: RED (Write Failing Tests)
1. Create test file: `tests/test_process_inbox.py`
2. Write all test cases from spec
3. Run tests - all should fail
4. Commit tests with message: "test: Add process inbox tests (TDD red phase)"

### Phase 2: GREEN (Minimal Implementation)
```python
# Minimal code to make tests pass
def process_inbox():
    inbox_path = Path('vault/00-inbox')
    result = ProcessResult()
    
    # FR-001: Read files
    files = list(inbox_path.glob('*.md'))
    result.files_found = len(files)
    
    for file in files:
        # FR-002: Extract metadata
        content = file.read_text()
        frontmatter = extract_frontmatter(content)
        
        # FR-003: Categorize
        category = categorize_content(content, frontmatter)
        
        # FR-004: Move file
        target = Path(f'vault/{category}/{file.name}')
        file.rename(target)
        
        # FR-005: Update frontmatter
        update_frontmatter(target, {'processed': datetime.now()})
        
        result.processed.append(file.name)
    
    # FR-006: Generate report
    return result
```

### Phase 3: REFACTOR (Improve Quality)
- Extract methods for clarity
- Add error handling
- Improve naming
- Add documentation
- Keep tests passing!

## Acceptance Criteria

### User Story
**As a** PKM user  
**I want to** process my inbox with a single command  
**So that** my captures are organized automatically

### Definition of Done
- [ ] All FR tests passing
- [ ] Command available as `/pkm-process`
- [ ] Documentation updated
- [ ] Error cases handled
- [ ] Report generated after processing
- [ ] Git commit with TDD message format

## Priority Decision (FR-First)

### Implement IMMEDIATELY (Week 1, Day 2)
- ✅ Basic file reading
- ✅ Simple categorization rules
- ✅ File moving
- ✅ Basic report

### Defer LATER (Week 4+)
- ⏸️ Parallel processing
- ⏸️ Performance optimization
- ⏸️ Advanced error recovery
- ⏸️ Metrics dashboard
- ⏸️ ML-based categorization

## Implementation Design

### API Interface
```python
class PkmInboxProcessor:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.inbox_path = self.vault_path / "00-inbox"
    
    def process_inbox(self) -> ProcessResult:
        """Process all items in inbox with PARA categorization"""
        pass
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract YAML frontmatter from markdown content"""
        pass
    
    def _categorize_content(self, content: str, frontmatter: Dict[str, Any]) -> str:
        """Categorize content according to PARA method"""
        pass
    
    def _move_file(self, source_path: Path, target_dir: str) -> Path:
        """Move file to target directory"""
        pass

class ProcessResult:
    success: bool
    files_found: int
    files_processed: int
    categorized: Dict[str, str]  # filename -> category
    errors: Dict[str, str]  # filename -> error message
    report: str
```

### PARA Categorization Rules
```yaml
categorization_logic:
  projects: # 01-projects/
    - keywords: [deadline, project, goal, complete]
    - frontmatter: type == 'project'
    - content_patterns: action items, deliverables
  
  areas: # 02-areas/
    - keywords: [area, ongoing, maintain, responsibility]
    - frontmatter: type == 'area'
    - content_patterns: standards, processes
  
  resources: # 03-resources/
    - keywords: [reference, resource, learn, information]
    - frontmatter: type == 'resource'
    - content_patterns: documentation, links
  
  archives: # 04-archives/
    - keywords: [completed, archive, old, inactive]
    - frontmatter: type == 'archive'
    - content_patterns: historical, deprecated
```

## Success Metrics

### Week 1 Success (FRs)
- [ ] Command processes inbox files
- [ ] Files moved to correct folders
- [ ] Basic categorization working
- [ ] Users can process inbox daily

### Quality Metrics
- [ ] 100% test pass rate
- [ ] >90% code coverage for inbox processing module
- [ ] Zero critical bugs in inbox workflow
- [ ] User satisfaction >85% for organization experience

### Future Success (NFRs - Only if Needed)
- [ ] Process 100+ files quickly (if volume increases)
- [ ] 99.9% reliability (if critical)
- [ ] Real-time processing (if users request)

## Dependencies
- **Required**: Vault directory structure (`vault/00-inbox/`, `vault/01-projects/`, etc.)
- **Required**: Python YAML library for frontmatter parsing
- **Required**: Path utilities for file operations
- **Optional**: NLP libraries for content analysis (deferred)

## Risk Mitigation
- **File conflicts**: Unique naming and conflict resolution
- **Missing directories**: Auto-creation with error handling
- **Malformed content**: Graceful error handling and reporting
- **Large files**: Memory-efficient processing
- **Concurrent access**: File locking (deferred)

---

## Implementation Notes

This specification follows our proven TDD and FR-First principles:
- **Tests written first** - All behavior defined by tests (following capture pattern)
- **Functional requirements prioritized** - User value delivered quickly  
- **Non-functional requirements deferred** - Optimization only when needed
- **Quality gates enforced** - No compromise on reliability

**Next Action**: Create comprehensive test suite following proven capture feature pattern (RED phase)

---

*Specification approved for immediate implementation*  
*Part of PKM Phase 3 Week 1 core operations development*
*Following proven TDD methodology from successful capture feature*