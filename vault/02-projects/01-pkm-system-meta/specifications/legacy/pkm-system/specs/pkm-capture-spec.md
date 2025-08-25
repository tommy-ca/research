---
title: "PKM Capture Command Specification"
date: 2024-08-22
type: specification
status: approved
priority: P0
tier: core
tags: [spec, pkm, capture, tdd, fr-first]
created: 2024-08-22T12:00:00Z
---

# Feature: PKM Capture Command

## Overview
Quick note capture command that takes any text input and saves it to the PKM inbox with proper metadata and formatting for later processing. This is the foundational entry point for all knowledge into the PKM system.

## Functional Requirements (IMPLEMENT NOW - Week 1)

### FR-001: Basic Text Capture
- **Description**: Accept text input and save to inbox with timestamp
- **Acceptance**: Text saved as markdown file in `vault/00-inbox/`
- **Priority**: P0 - Foundation requirement
- **Test**: `test_capture_creates_file_in_inbox()`

### FR-002: Automatic Frontmatter Generation
- **Description**: Generate YAML frontmatter with metadata
- **Acceptance**: Every captured note has complete frontmatter
- **Required Fields**: date, type, status, created, id
- **Test**: `test_capture_adds_proper_frontmatter()`

### FR-003: Intelligent Filename Generation
- **Description**: Generate readable filenames from content
- **Acceptance**: Filename based on first line/sentence, sanitized
- **Format**: `YYYYMMDDHHmmss-title-slug.md`
- **Test**: `test_filename_generation()`

### FR-004: Content Preservation
- **Description**: Preserve markdown formatting and structure
- **Acceptance**: Headers, lists, links, code blocks maintained
- **Edge Cases**: Handle special characters, unicode, long content
- **Test**: `test_capture_preserves_markdown_formatting()`

### FR-005: Directory Management
- **Description**: Create inbox directory if missing
- **Acceptance**: Command works even if vault structure incomplete
- **Behavior**: Auto-create missing directories
- **Test**: `test_capture_creates_directories_if_missing()`

### FR-006: Duplicate Handling
- **Description**: Handle multiple captures with same content
- **Acceptance**: Each capture gets unique filename
- **Method**: Timestamp-based uniqueness
- **Test**: `test_capture_generates_unique_filenames()`

## Non-Functional Requirements (DEFER - Week 4+)

### NFR-001: Performance (DEFER)
- **Description**: Capture should complete in <100ms
- **Rationale**: Not critical for MVP, optimize later
- **Target Date**: Week 4 (if bottleneck identified)

### NFR-002: Concurrent Access (DEFER)  
- **Description**: Handle multiple simultaneous captures
- **Rationale**: Single-user system initially
- **Target Date**: Multi-user phase

### NFR-003: Large Content (DEFER)
- **Description**: Handle captures >10MB
- **Rationale**: Typical captures are <1KB
- **Target Date**: When large content use case appears

### NFR-004: Network Sync (DEFER)
- **Description**: Real-time sync across devices
- **Rationale**: Local-first approach initially
- **Target Date**: Collaboration phase

## Acceptance Criteria

### User Story
**As a** knowledge worker  
**I want to** quickly capture ideas and information  
**So that** nothing is lost and everything enters my PKM system

### Acceptance Tests
- [ ] Given any text input, When I run capture command, Then file created in inbox
- [ ] Given content with markdown, When captured, Then formatting preserved
- [ ] Given empty inbox directory, When capturing, Then directory created
- [ ] Given duplicate content, When captured twice, Then two unique files created
- [ ] Given special characters in content, When captured, Then filename sanitized
- [ ] Given very long content, When captured, Then filename appropriately truncated

## Test Cases (TDD - Written First!)

### Unit Tests (tests/unit/test_capture.py)
1. `test_capture_creates_file_in_inbox()` - Basic file creation
2. `test_capture_adds_proper_frontmatter()` - Metadata generation
3. `test_capture_handles_empty_content()` - Error handling
4. `test_filename_generation()` - Filename logic
5. `test_capture_creates_directories_if_missing()` - Directory management
6. `test_capture_with_tags()` - Custom tag support
7. `test_capture_with_invalid_characters()` - Character sanitization
8. `test_capture_generates_unique_filenames()` - Duplicate handling
9. `test_capture_preserves_markdown_formatting()` - Content preservation

### Integration Tests (tests/integration/test_capture_workflow.py)
1. `test_capture_to_inbox_workflow()` - End-to-end capture process
2. `test_capture_with_file_system_issues()` - Error scenarios
3. `test_capture_metadata_consistency()` - Metadata validation

### Acceptance Tests (tests/acceptance/test_user_capture_workflow.py)
1. `test_user_daily_capture_routine()` - Real user workflow
2. `test_capture_various_content_types()` - Different content scenarios

## Implementation Design

### API Interface
```python
class PkmCapture:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.inbox_path = self.vault_path / "00-inbox"
    
    def capture(self, content: str, source: str = None, tags: List[str] = None) -> CaptureResult:
        """Capture content to PKM inbox with metadata"""
        pass
    
    def _generate_filename(self, content: str) -> str:
        """Generate sanitized filename from content"""
        pass
    
    def _create_frontmatter(self, source: str, tags: List[str]) -> Dict[str, Any]:
        """Generate YAML frontmatter for captured content"""
        pass

class CaptureResult:
    success: bool
    file_path: str
    frontmatter: Dict[str, Any]
    metadata: Dict[str, Any]
    error: Optional[str] = None
```

### File Structure
```
vault/00-inbox/20240822120000-quantum-computing-notes.md
---
date: 2024-08-22
type: capture
status: inbox
created: 2024-08-22T12:00:00Z
id: 20240822120000
source: manual
tags: []
---

# Quantum Computing Notes

Key principles of quantum mechanics...
```

## Implementation Plan (TDD Cycle)

### Phase 1: RED (Tests Written ✅)
- [x] Created comprehensive test suite in `tests/unit/test_capture.py`
- [x] All tests fail initially (expected)
- [x] Tests define exact behavior specification

### Phase 2: GREEN (Minimal Implementation)
```python
# Minimal code to pass tests
def capture(content: str) -> CaptureResult:
    if not content.strip():
        raise CaptureError("Content cannot be empty")
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}-{slugify(content[:50])}.md"
    file_path = inbox_path / filename
    
    frontmatter = {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'type': 'capture',
        'status': 'inbox',
        'created': datetime.now().isoformat(),
        'id': timestamp
    }
    
    full_content = f"---\n{yaml.dump(frontmatter)}---\n\n{content}"
    file_path.write_text(full_content)
    
    return CaptureResult(success=True, file_path=str(file_path), frontmatter=frontmatter)
```

### Phase 3: REFACTOR (Quality Improvements)
- Extract helper methods
- Add error handling
- Improve naming
- Add logging
- Optimize performance
- **Keep all tests passing!**

## Definition of Done

### Code Complete
- [ ] All FR tests passing (100%)
- [ ] Implementation follows specification exactly
- [ ] Error cases handled gracefully
- [ ] Code reviewed and refactored
- [ ] Documentation updated

### Quality Gates
- [ ] Unit test coverage >90%
- [ ] Integration tests passing
- [ ] Acceptance criteria validated
- [ ] Performance within baseline (when measured)
- [ ] Security validation (basic)

### User Value
- [ ] Command available as `/pkm-capture`
- [ ] Users can capture notes successfully
- [ ] Notes appear in inbox for processing
- [ ] No data loss or corruption
- [ ] Intuitive and fast workflow

## Priority Decision (FR-First)

### Implement IMMEDIATELY (Week 1, Day 1)
- ✅ Basic text capture to inbox
- ✅ Frontmatter generation
- ✅ Filename sanitization
- ✅ Directory creation
- ✅ Error handling

### Defer to LATER Phases
- ⏸️ Advanced performance optimization (Week 4)
- ⏸️ Multi-user concurrent access (Collaboration phase)
- ⏸️ Network synchronization (Infrastructure phase)
- ⏸️ Advanced content processing (Intelligence phase)

## Success Metrics

### Week 1 Success (Core FRs)
- [ ] Command captures text to inbox files
- [ ] Generated files have proper structure
- [ ] Users can capture multiple notes daily
- [ ] Zero data loss incidents
- [ ] <5 second learning curve for new users

### Quality Metrics
- [ ] 100% test pass rate
- [ ] >90% code coverage for capture module
- [ ] Zero critical bugs in capture workflow
- [ ] User satisfaction >85% for capture experience

## Dependencies
- **Required**: Vault directory structure (`vault/00-inbox/`)
- **Required**: Python YAML library for frontmatter
- **Required**: Path utilities for file management
- **Optional**: Slugify library for filename generation

## Risk Mitigation
- **File conflicts**: Timestamp-based uniqueness
- **Missing directories**: Auto-creation with error handling
- **Large content**: Graceful handling with size limits
- **Character encoding**: UTF-8 enforcement
- **Concurrent access**: File locking (deferred)

---

## Implementation Notes

This specification follows our TDD and FR-First principles:
- **Tests written first** - All behavior defined by tests
- **Functional requirements prioritized** - User value delivered quickly  
- **Non-functional requirements deferred** - Optimization only when needed
- **Quality gates enforced** - No compromise on reliability

**Next Action**: Implement minimal code to pass existing tests (GREEN phase)

---

*Specification approved for immediate implementation*  
*Part of PKM Phase 3 Week 1 core operations development*