# FR-002 through FR-005 Implementation Plan
## TDD + KISS + SOLID Methodology

### Overview
Following strict TDD methodology (RED → GREEN → REFACTOR) for each FR implementation.
Each feature will be implemented as a single, KISS-compliant module with comprehensive test coverage.

## Implementation Order (Dependency-Based)

### 1. FR-002: Inbox Processing Command
**Priority: HIGH (Foundation for organizing system)**

#### TDD Process:
```python
# RED Phase: Write failing tests first
def test_inbox_processing_moves_items_to_para_folders():
    # Test that items get categorized and moved
    pass

def test_inbox_processing_uses_keyword_matching():
    # Test keyword-based categorization
    pass
```

#### Implementation Approach:
- **KISS**: Single function `pkm_process_inbox()` ≤20 lines
- **PARA Keywords**: Simple dict mapping keywords to folders
- **File Operations**: Move files, don't copy (atomic operations)
- **Error Handling**: Graceful failures, rollback on error

#### Dependencies: FR-001 (completed)

### 2. FR-003: Daily Note Creation  
**Priority: HIGH (Independent, core functionality)**

#### TDD Process:
```python
# RED Phase: Write failing tests first  
def test_daily_note_creates_todays_note():
    # Test creation of YYYY-MM-DD.md
    pass

def test_daily_note_creates_directory_structure():
    # Test YYYY/MM-month folder creation
    pass
```

#### Implementation Approach:
- **KISS**: Single function `pkm_daily()` ≤20 lines
- **Date Handling**: Use datetime.now() for current date
- **Template**: Simple frontmatter template
- **Idempotent**: Creates if missing, opens if exists

#### Dependencies: None

### 3. FR-004: Basic Note Search
**Priority: HIGH (Independent search capability)**

#### TDD Process:
```python
# RED Phase: Write failing tests first
def test_note_search_finds_exact_matches():
    # Test exact text matching
    pass

def test_note_search_ranks_by_relevance():
    # Test relevance scoring
    pass
```

#### Implementation Approach:
- **KISS**: Single function `pkm_search()` ≤20 lines
- **Search Engine**: Use ripgrep (rg) subprocess call
- **Result Format**: File path + line number + context
- **Ranking**: Simple frequency-based scoring

#### Dependencies: None

### 4. FR-005: Simple Link Generation
**Priority: MEDIUM (Complex, depends on others)**

#### TDD Process:
```python
# RED Phase: Write failing tests first
def test_link_generation_finds_shared_keywords():
    # Test keyword extraction and matching
    pass

def test_link_generation_suggests_bidirectional_links():
    # Test link suggestion logic
    pass
```

#### Implementation Approach:
- **KISS**: Single function `pkm_link()` ≤20 lines + helpers
- **Keyword Extraction**: Simple word frequency analysis
- **Link Format**: Standard markdown `[[note-name]]`
- **User Interface**: Simple CLI prompts

#### Dependencies: FR-001, FR-002, FR-004

## Engineering Principles Application

### TDD Compliance
```
For each FR:
1. RED: Write 5-10 failing tests covering all acceptance criteria
2. GREEN: Write minimal implementation to pass all tests
3. REFACTOR: Optimize while maintaining test passage
4. VALIDATE: Run quality pipeline for KISS compliance
```

### KISS Compliance  
- **Function Length**: ≤20 lines per function
- **Complexity**: ≤5 cyclomatic complexity
- **Helper Functions**: Extract complex logic to helpers
- **Single Responsibility**: Each function does one thing

### SOLID Principles
- **SRP**: Each module handles one FR
- **OCP**: Extensible through configuration
- **LSP**: All functions return consistent result types
- **ISP**: Minimal interfaces, no unused parameters
- **DIP**: Depend on Path/str abstractions, not file implementations

## File Structure (Clean Architecture)

```
src/pkm/
├── capture.py          # FR-001 (completed)
├── cli.py              # FR-001 (completed)  
├── inbox_processor.py  # FR-002 (new)
├── daily.py            # FR-003 (new)
├── search.py           # FR-004 (new)
├── linker.py           # FR-005 (new)
└── utils.py            # Shared utilities (new)

tests/unit/
├── test_pkm_capture_fr001_functional.py     # FR-001 (completed)
├── test_pkm_cli.py                          # FR-001 (completed)
├── test_pkm_inbox_processor_fr002.py        # FR-002 (new)
├── test_pkm_daily_fr003.py                  # FR-003 (new)
├── test_pkm_search_fr004.py                 # FR-004 (new)
└── test_pkm_linker_fr005.py                 # FR-005 (new)
```

## Quality Gates per FR

### Automated Validation
```bash
# Run after each FR implementation
python3 scripts/quality_validation_pipeline.py
python3 -m pytest tests/unit/test_pkm_*_fr00X.py -v
```

### Success Criteria per FR
- ✅ All tests pass (minimum 10 tests per FR)
- ✅ KISS compliance (≤20 lines, ≤5 complexity)
- ✅ TDD documentation (RED→GREEN→REFACTOR notes)
- ✅ CLI integration working
- ✅ No regression in previous FRs

## CLI Command Integration

### Updated CLI Module
```python
# src/pkm/cli.py expansion
def main():
    """Enhanced CLI with all FR commands"""
    commands = {
        'capture': _handle_capture_command,      # FR-001
        'process-inbox': _handle_inbox_command,  # FR-002  
        'daily': _handle_daily_command,          # FR-003
        'search': _handle_search_command,        # FR-004
        'link': _handle_link_command,            # FR-005
    }
    # KISS: 8 lines implementation
```

## Implementation Timeline

### Phase 1: FR-002 (Inbox Processing)
1. **RED**: Write 8 failing tests (30 minutes)
2. **GREEN**: Implement `pkm_process_inbox()` (45 minutes)  
3. **REFACTOR**: KISS compliance optimization (15 minutes)
4. **INTEGRATE**: Add to CLI (10 minutes)

### Phase 2: FR-003 (Daily Notes)
1. **RED**: Write 6 failing tests (20 minutes)
2. **GREEN**: Implement `pkm_daily()` (30 minutes)
3. **REFACTOR**: Date handling optimization (10 minutes)  
4. **INTEGRATE**: Add to CLI (10 minutes)

### Phase 3: FR-004 (Search)
1. **RED**: Write 7 failing tests (25 minutes)
2. **GREEN**: Implement `pkm_search()` (40 minutes)
3. **REFACTOR**: Result formatting optimization (15 minutes)
4. **INTEGRATE**: Add to CLI (10 minutes)

### Phase 4: FR-005 (Link Generation)  
1. **RED**: Write 10 failing tests (40 minutes)
2. **GREEN**: Implement `pkm_link()` (60 minutes)
3. **REFACTOR**: Keyword extraction helpers (20 minutes)
4. **INTEGRATE**: Add to CLI (15 minutes)

### Phase 5: Integration Testing
1. **Full Test Suite**: Run all 40+ tests (5 minutes)
2. **Quality Validation**: KISS + TDD pipeline (5 minutes)
3. **Integration Tests**: Cross-FR workflows (15 minutes)

**Total Estimated Time: ~6.5 hours**

## Risk Mitigation

### KISS Violations
- **Monitor**: Function length after each implementation
- **Refactor**: Extract helpers immediately when >20 lines
- **Validate**: Automated pipeline prevents violations

### Test Coverage Gaps
- **Minimum**: 10 tests per FR covering all acceptance criteria
- **Edge Cases**: Error handling, empty inputs, malformed data
- **Integration**: Cross-FR interaction tests

### Dependency Conflicts
- **FR-005**: Depends on FR-001,002,004 - implement last
- **Shared Utils**: Extract common patterns to utils.py
- **CLI Integration**: Incremental addition per FR

## Success Metrics

### Technical Quality
- **Test Coverage**: >95% for each FR module
- **KISS Compliance**: 100% (no violations allowed)
- **Performance**: All commands <1 second response time
- **Error Handling**: Graceful failures with helpful messages

### User Experience  
- **Command Consistency**: All commands follow same pattern
- **Help Text**: Clear usage examples for each command
- **Progress Feedback**: User sees what's happening
- **Error Recovery**: Clear guidance when things fail

---

## Next: Begin FR-002 Implementation

Ready to start with RED phase of FR-002 Inbox Processing Command.