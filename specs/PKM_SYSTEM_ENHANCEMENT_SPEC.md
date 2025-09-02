# PKM System Enhancement Specification v2.0

## Overview
This specification defines comprehensive enhancements to the Personal Knowledge Management (PKM) system, following Test-Driven Development (TDD), FR-First prioritization, and SOLID principles as mandated in CLAUDE.md.

## Engineering Principles Compliance

### 1. TDD Workflow - MANDATORY
```
RED → GREEN → REFACTOR
├── Write failing test/spec first
├── Write minimal code to pass  
└── Improve code while tests pass
```

### 2. Specs-Driven Development - PRIMARY WORKFLOW
```
SPEC FIRST → REVIEW SPEC → IMPLEMENT → VALIDATE
```

### 3. FR-First Prioritization - ALWAYS
- ✅ User-facing features (HIGH priority)
- ⏸️ Performance optimization (DEFER)
- ⏸️ Scalability (DEFER until proven needed)

### 4. KISS Principle - ALWAYS PRIORITIZE
- Simple over clever implementations
- Clear function names over comments
- Single-purpose functions

### 5. DRY Principle - ELIMINATE DUPLICATION
- Extract common logic after patterns emerge
- Shared configuration and constants

### 6. SOLID Principles - ARCHITECTURAL FOUNDATION
- Single Responsibility per class/agent
- Open/Closed for extensions
- Dependency injection over hard-coding

## Current System Analysis

### Strengths
- ✅ 4 specialized PKM agents (ingestion, processor, synthesizer, feynman)
- ✅ Comprehensive testing framework with pytest
- ✅ Well-documented agent architecture
- ✅ Clear separation of concerns

### Critical Gaps (Violations of Engineering Principles)

#### TDD Violations
- ❌ Agents defined without test specifications
- ❌ Complex features implemented before simple versions
- ❌ No failing tests to drive implementation

#### FR-First Violations  
- ❌ Performance optimizations before basic functionality
- ❌ Complex NLP features before simple text processing
- ❌ Advanced synthesis before basic note operations

#### KISS Violations
- ❌ Over-engineered agents (200+ lines) before simple versions
- ❌ Complex configuration before basic functionality
- ❌ Advanced features without minimal viable implementation

#### Missing Command Integration
- ❌ No CLI commands that use the PKM agents
- ❌ No user-facing functionality despite sophisticated backend

## Functional Requirements (FRs) - PRIORITIZE

### FR-001: Basic PKM Capture Command
**Priority: HIGH - Implement First**
```yaml
requirement: User can capture text to inbox via simple command
acceptance_criteria:
  - Given: User has content to capture
  - When: User runs `/pkm-capture "content"`  
  - Then: Content saved to vault/00-inbox/ with timestamp
  - And: Basic frontmatter added with capture metadata
test_cases:
  - Simple text capture works
  - Special characters handled correctly
  - Frontmatter metadata is valid YAML
complexity: SIMPLE - Start here
dependencies: None
```

### FR-002: Inbox Processing Command
**Priority: HIGH - Implement Second**
```yaml
requirement: User can process inbox items with basic categorization
acceptance_criteria:
  - Given: Items exist in vault/00-inbox/
  - When: User runs `/pkm-process-inbox`
  - Then: Items categorized using simple keyword matching
  - And: Items moved to appropriate PARA folders
test_cases:
  - Project keywords move to 01-projects/
  - Area keywords move to 02-areas/
  - Resource keywords move to 03-resources/
complexity: SIMPLE - Basic keyword matching only
dependencies: FR-001
```

### FR-003: Daily Note Creation
**Priority: HIGH - Implement Third**
```yaml
requirement: User can create/open today's daily note
acceptance_criteria:
  - Given: Current date is known
  - When: User runs `/pkm-daily`
  - Then: Today's note created/opened in vault/daily/YYYY/MM-month/
  - And: Basic frontmatter template applied
test_cases:
  - Creates note if doesn't exist
  - Opens existing note if already exists
  - Handles year/month folder creation
complexity: SIMPLE - Date formatting and file creation
dependencies: None
```

### FR-004: Basic Note Search
**Priority: HIGH - Implement Fourth**
```yaml
requirement: User can search across vault content
acceptance_criteria:
  - Given: Notes exist in vault
  - When: User runs `/pkm-search "query"`
  - Then: Matching notes displayed with context
  - And: Results ranked by relevance
test_cases:
  - Text search finds exact matches
  - Case-insensitive search works
  - Results show file paths and line context
complexity: SIMPLE - Text search using grep
dependencies: None
```

### FR-005: Simple Link Generation
**Priority: MEDIUM - Implement After Core Features**
```yaml
requirement: User can find and suggest links between notes
acceptance_criteria:
  - Given: A note mentions concepts found in other notes
  - When: User runs `/pkm-link "note.md"`
  - Then: Suggested links displayed
  - And: User can choose which links to add
test_cases:
  - Finds notes with shared keywords
  - Suggests bidirectional links
  - User can accept/reject suggestions
complexity: MEDIUM - Text analysis and suggestion UI
dependencies: FR-001, FR-002, FR-004
```

## Non-Functional Requirements (NFRs) - DEFER

### NFR-001: Performance Optimization (DEFER)
- Advanced NLP processing
- Real-time search indexing  
- Concurrent processing
- **Status: DEFERRED until FRs 1-5 complete**

### NFR-002: Advanced AI Features (DEFER)
- GPT-based content analysis
- Semantic similarity matching
- Automated insight generation
- **Status: DEFERRED until basic functionality proven**

### NFR-003: Scalability Features (DEFER)
- Large vault handling (>10k notes)
- Distributed processing
- Cloud synchronization
- **Status: DEFERRED until user adoption proven**

## Implementation Roadmap (TDD + FR-First)

### Phase 1: Basic Functionality (FRs 1-4)
**Engineering Approach: TDD + KISS + FR-First**

#### Step 1.1: FR-001 Implementation (TDD)
```python
# 1. RED: Write failing test FIRST
def test_pkm_capture_creates_inbox_note():
    """Test that capture command creates note in inbox"""
    # This test MUST fail initially
    result = pkm_capture("Test content")
    assert Path("vault/00-inbox").exists()
    assert result.filename.endswith(".md")
    assert result.frontmatter["type"] == "capture"
    # TEST FAILS - no implementation yet

# 2. GREEN: Minimal implementation to pass test
def pkm_capture(content: str) -> CaptureResult:
    """Minimal implementation - just make test pass"""
    # Simplest possible implementation
    pass  # Will be implemented to pass test

# 3. REFACTOR: Improve while keeping tests green
def pkm_capture(content: str, tags: List[str] = None) -> CaptureResult:
    """Enhanced but still simple implementation"""
    # Refactored version with better structure
```

#### Step 1.2: Command Integration (KISS)
```bash
# Simple command implementation - no complexity
/pkm-capture "content"  # Calls pkm_capture() function directly
/pkm-daily             # Simple date-based file creation
/pkm-search "query"    # Basic grep wrapper
```

#### Step 1.3: Quality Gates
```yaml
quality_gates:
  tdd_compliance:
    - All features have tests first
    - No implementation without failing test
    - Refactoring maintains green tests
  
  kiss_compliance:
    - Functions under 20 lines
    - Single responsibility per function
    - No complex logic in first iteration
  
  fr_first_compliance:
    - User-facing functionality working
    - No performance optimization
    - No complex features
```

### Phase 2: Enhanced Functionality (FR-005)
**Only after Phase 1 complete and validated**

### Phase 3: Quality & Polish (NFRs)
**Only after user adoption and feedback**

## Agent Enhancement Strategy

### Current Agents: Refactor for Principles Compliance

#### PKM Ingestion Agent - Refactor Plan
```yaml
current_issues:
  - 200+ lines violates KISS
  - Complex features before simple ones
  - No TDD test specification

refactor_plan:
  phase_1_simple:
    - Basic file reading (20 lines)
    - Simple text capture (10 lines) 
    - Minimal frontmatter (15 lines)
  
  phase_2_enhanced:
    - Format detection (after phase 1 proven)
    - Batch processing (after single file works)
    - Quality validation (after basic capture works)
```

#### PKM Processor Agent - Refactor Plan
```yaml
current_issues:
  - NLP complexity before basic text processing
  - Performance features before functional features
  - Violates FR-First principle

refactor_plan:
  phase_1_simple:
    - Keyword extraction (basic regex)
    - Simple tag generation (word frequency)
    - Basic categorization (keyword matching)
  
  phase_2_enhanced:
    - NLP processing (after basic version works)
    - Graph integration (after simple linking works)
    - Advanced analysis (after user adoption)
```

## Testing Strategy (TDD Compliance)

### Test-First Development Process
```yaml
tdd_process:
  for_each_feature:
    1_red_phase:
      - Write comprehensive test specification
      - Write failing unit tests
      - Write failing integration tests
      - Ensure all tests fail for right reasons
    
    2_green_phase:
      - Write MINIMAL implementation
      - Make tests pass with simplest code
      - No optimization or complexity
      - Focus only on test satisfaction
    
    3_refactor_phase:
      - Improve code structure
      - Extract common patterns
      - Apply DRY principle
      - Maintain test passing status
```

### Test Categories (Per pytest.ini)
```yaml
test_categories:
  unit:
    - Individual function testing
    - Fast execution (< 1s each)
    - No external dependencies
    - Mock all I/O operations
  
  integration:
    - Component interaction testing
    - File system operations
    - Agent command integration
    - Cross-agent workflows
  
  acceptance:
    - End-to-end user workflows
    - Real file operations
    - Complete command sequences
    - User story validation
```

## Quality Validation Pipeline

### Automated Quality Gates
```yaml
quality_pipeline:
  pre_commit:
    - TDD compliance check
    - KISS principle validation
    - FR-first priority verification
    - SOLID principle assessment
  
  continuous_integration:
    - All tests must pass
    - Coverage > 80%
    - No code without tests
    - Performance regression detection
  
  pre_merge:
    - Engineering principles review
    - User story validation
    - Documentation completeness
    - Acceptance criteria satisfied
```

## Success Criteria

### Phase 1 Success (Basic PKM Commands)
```yaml
success_criteria:
  functional:
    - /pkm-capture works reliably
    - /pkm-daily creates proper notes
    - /pkm-search finds content
    - /pkm-process-inbox categorizes items
  
  engineering:
    - 100% TDD compliance
    - All functions follow KISS (< 20 lines)
    - FR-first priority maintained
    - SOLID principles applied
  
  user_validation:
    - Commands integrate into daily workflow
    - Users report improved knowledge management
    - System demonstrates clear value
```

### Quality Metrics
```yaml
metrics:
  tdd_compliance: 100%
  test_coverage: > 80%
  function_complexity: < 20 lines average
  user_adoption: > 50% daily command usage
  system_reliability: > 95% command success rate
```

## Risk Mitigation

### Engineering Principle Violations
```yaml
risks:
  tdd_abandonment:
    mitigation: Automated test-first enforcement
    
  complexity_creep:
    mitigation: KISS principle validation gates
    
  fr_last_development:
    mitigation: User story prioritization framework
    
  solid_violations:
    mitigation: Architecture review checkpoints
```

## Conclusion

This specification mandates a complete refactoring of the PKM system to comply with the engineering principles outlined in CLAUDE.md. The approach prioritizes:

1. **TDD compliance** - All features developed test-first
2. **FR-First development** - User value before optimization  
3. **KISS implementation** - Simple solutions before complex ones
4. **Incremental delivery** - Working features over perfect architecture

The goal is a PKM system that demonstrates engineering excellence while delivering immediate user value through simple, reliable functionality.

---

*PKM System Enhancement Specification v2.0 - Engineering Principles First*