---
title: "PKM Migration Phase 2 Specification"
date: 2024-01-21
type: specification
status: active
tags: [spec, migration, pkm, tdd, fr-first]
---

# Specification: PKM Migration Phase 2

## Feature Overview
Complete migration of remaining repository content (74%) into PKM vault structure, extracting atomic notes and building comprehensive link network.

## Requirements

### Functional Requirements (PRIORITY: HIGH - Days 2-5)

#### FR-001: Migrate Knowledge Base Content
- **Description**: Move all knowledge-base/* content to appropriate PARA folders
- **Acceptance**: All files accessible in new locations
- **Test**: `test_knowledge_base_migration_complete()`
- **Target**: 15 files

#### FR-002: Migrate Experiments Directory
- **Description**: Transfer experiments code, notebooks, and data
- **Acceptance**: Experiments functional in new structure
- **Test**: `test_experiments_accessible()`
- **Target**: 10+ files

#### FR-003: Extract Atomic Notes from Documents
- **Description**: Break down long documents into atomic concepts
- **Acceptance**: 50+ atomic notes created
- **Test**: `test_atomic_note_count()`
- **Target**: Average 10 notes per major document

#### FR-004: Build Bidirectional Link Network
- **Description**: Create connections between related notes
- **Acceptance**: 100+ bidirectional links established
- **Test**: `test_link_density()`
- **Target**: 3+ links per note average

#### FR-005: Process Remaining Docs
- **Description**: Migrate remaining 42 documentation files
- **Acceptance**: Zero files in original locations
- **Test**: `test_no_orphan_files()`
- **Target**: 100% migration

#### FR-006: Create Migration Automation
- **Description**: Build scripts for bulk operations
- **Acceptance**: Scripts reduce manual effort by 50%
- **Test**: `test_automation_scripts()`
- **Deliverables**:
  - `migrate-files.py` - Bulk file mover
  - `add-frontmatter.py` - Metadata adder
  - `extract-atomic.py` - Note splitter
  - `build-links.py` - Link creator

### Non-Functional Requirements (PRIORITY: LOW - Defer)

#### NFR-001: Performance Optimization (DEFER)
- **Description**: Optimize large file processing
- **Rationale**: Current speed acceptable for one-time migration
- **Target Date**: Post-migration

#### NFR-002: Concurrent Processing (DEFER)
- **Description**: Parallel file migration
- **Rationale**: Sequential processing sufficient
- **Target Date**: If needed

#### NFR-003: Rollback Capability (DEFER)
- **Description**: Automated rollback on failure
- **Rationale**: Git provides manual rollback
- **Target Date**: Future automation

## Test Cases (TDD - Write First!)

### Day 2 Tests
```python
def test_knowledge_base_concepts_migrated():
    """FR-001: Knowledge base concepts in vault"""
    assert exists('vault/2-areas/knowledge-mgmt/concepts/')
    assert count_files('vault/2-areas/knowledge-mgmt/concepts/') >= 5

def test_frameworks_migrated():
    """FR-001: Frameworks moved to resources"""
    assert exists('vault/3-resources/frameworks/')
    assert all_markdown_files_have_frontmatter('vault/3-resources/frameworks/')

def test_investment_strategies_migrated():
    """FR-001: Investment content organized"""
    assert exists('vault/3-resources/finance/strategies/')
    assert no_broken_links('vault/3-resources/finance/')
```

### Day 3 Tests
```python
def test_experiments_code_migrated():
    """FR-002: Experiment code accessible"""
    assert exists('vault/1-projects/experiments/code/')
    assert can_execute('vault/1-projects/experiments/code/main.py')

def test_notebooks_migrated():
    """FR-002: Jupyter notebooks moved"""
    assert exists('vault/1-projects/experiments/notebooks/')
    assert all_notebooks_valid('vault/1-projects/experiments/notebooks/')
```

### Day 4 Tests
```python
def test_atomic_notes_extracted():
    """FR-003: Atomic notes created from documents"""
    assert count_atomic_notes() >= 50
    assert average_note_length() < 500  # words
    assert all_notes_have_single_concept()

def test_bidirectional_links():
    """FR-004: Link network established"""
    assert total_links() >= 100
    assert average_links_per_note() >= 3
    assert no_orphan_notes()
```

## Implementation Schedule

### Day 2: Knowledge Base Migration (Tuesday, Jan 23)

#### Morning (3 hours)
- [ ] Migrate knowledge-base/concepts/* → vault/2-areas/knowledge-mgmt/concepts/
- [ ] Migrate knowledge-base/frameworks/* → vault/3-resources/frameworks/
- [ ] Extract 10 atomic notes from concepts
- [ ] Create concept relationship map

#### Afternoon (3 hours)
- [ ] Migrate knowledge-base/tools/* → vault/3-resources/tools/
- [ ] Migrate investment-strategies/* → vault/3-resources/finance/
- [ ] Build cross-domain links
- [ ] Update permanent index

#### Deliverables
- 15+ files migrated
- 10+ atomic notes created
- 20+ new links established

### Day 3: Experiments & Code (Wednesday, Jan 24)

#### Morning (3 hours)
- [ ] Migrate experiments/code/* → vault/1-projects/experiments/code/
- [ ] Migrate experiments/notebooks/* → vault/1-projects/experiments/notebooks/
- [ ] Create project documentation for each experiment
- [ ] Extract learnings as atomic notes

#### Afternoon (3 hours)
- [ ] Migrate experiments/data/* → vault/3-resources/datasets/
- [ ] Process research papers → vault/3-resources/papers/
- [ ] Create literature notes
- [ ] Link experiments to concepts

#### Deliverables
- All experiments migrated
- 5+ project notes created
- 15+ atomic notes from learnings

### Day 4: Automation & Processing (Thursday, Jan 25)

#### Morning (3 hours)
- [ ] Create `migrate-files.py` script
- [ ] Create `add-frontmatter.py` script
- [ ] Test automation on sample files
- [ ] Document automation usage

#### Afternoon (3 hours)
- [ ] Create `extract-atomic.py` script
- [ ] Create `build-links.py` script
- [ ] Run automation on remaining files
- [ ] Verify migration integrity

#### Deliverables
- 4 automation scripts
- 20+ files processed automatically
- 50% time reduction achieved

### Day 5: Completion & Validation (Friday, Jan 26)

#### Morning (3 hours)
- [ ] Complete remaining file migrations
- [ ] Extract final atomic notes
- [ ] Build remaining links
- [ ] Run validation checks

#### Afternoon (3 hours)
- [ ] Archive original structure
- [ ] Update all documentation
- [ ] Create migration report
- [ ] Celebrate completion! 🎉

#### Deliverables
- 100% migration complete
- 50+ atomic notes total
- 100+ links established
- Zero orphan files

## Acceptance Criteria

### Definition of Done
- [x] All 57 docs files migrated
- [ ] All knowledge-base content organized
- [ ] All experiments accessible
- [ ] 50+ atomic notes created
- [ ] 100+ bidirectional links
- [ ] Automation scripts functional
- [ ] Zero orphan files
- [ ] Migration report complete

## Success Metrics

### Quantitative
- Files migrated: 57/57 (100%)
- Atomic notes: 50+ created
- Links: 100+ bidirectional
- Automation: 50% time saved
- Orphans: 0

### Qualitative
- Knowledge more discoverable
- Clear PARA organization
- Rich link network
- Sustainable structure
- Easy to maintain

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Data loss | High | Git backup, incremental migration |
| Broken links | Medium | Link validation script |
| Wrong categorization | Low | Review and adjust in PR |
| Time overrun | Medium | Focus on high-value content |

## Automation Scripts Specification

### migrate-files.py
```python
"""
Bulk file migration with PARA categorization
Input: Source directory, mapping rules
Output: Files moved to vault with structure preserved
"""
```

### add-frontmatter.py
```python
"""
Add YAML frontmatter to all markdown files
Input: Directory of markdown files
Output: Files with appropriate metadata
"""
```

### extract-atomic.py
```python
"""
Split long documents into atomic notes
Input: Long markdown document
Output: Multiple atomic note files
"""
```

### build-links.py
```python
"""
Create bidirectional links between related notes
Input: Directory of notes
Output: Notes with [[wiki-links]] added
"""
```

## Priority Decision (FR-First)

### Implement NOW (Days 2-5)
- ✅ File migration (user value)
- ✅ Atomic extraction (knowledge value)
- ✅ Link building (connection value)
- ✅ Basic automation (time value)

### Defer LATER (Post-migration)
- ⏸️ Performance optimization
- ⏸️ Advanced automation
- ⏸️ Migration rollback
- ⏸️ Metrics dashboard

---

*Specification follows TDD and FR-First principles*
*Focus: Complete migration with high-quality knowledge extraction*
*Method: Systematic, tested, automated where valuable*