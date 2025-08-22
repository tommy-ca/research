---
title: "PKM Content Migration Map"
date: 2024-01-21
type: project
status: active
tags: [migration, pkm, para, organization]
---

# PKM Content Migration Map

## Overview
This document maps existing repository content to the PARA vault structure for systematic migration.

## Content Audit Summary
- **Docs**: 57 markdown files (mostly PKM architecture)
- **Resources**: 2 files (references)
- **Experiments**: Code, data, notebooks directories
- **Knowledge-base**: Concepts, frameworks, tools, investment strategies
- **Claude agents**: PKM and research agents

## Migration Categorization (PARA Method)

### 1️⃣ PROJECTS (Active work with deadlines)

#### PKM System Implementation
**Source → Destination**
- `docs/pkm-architecture/*.md` → `vault/1-projects/pkm-system/architecture/`
- `docs/pkm-architecture/IMPLEMENTATION-*.md` → `vault/1-projects/pkm-system/implementation/`
- `docs/pkm-architecture/DOGFOODING-PLAN.md` → `vault/1-projects/pkm-system/`

#### Active Experiments
- `experiments/code/*` → `vault/1-projects/experiments/`
- `experiments/notebooks/*.ipynb` → `vault/1-projects/experiments/notebooks/`

### 2️⃣ AREAS (Ongoing responsibilities)

#### Knowledge Management
- `.claude/agents/pkm-*.md` → `vault/2-areas/knowledge-mgmt/agents/`
- `.claude/commands/*.md` → `vault/2-areas/tools/commands/`
- `knowledge-base/concepts/*` → `vault/2-areas/knowledge-mgmt/concepts/`

#### Learning & Research
- `.claude/agents/research.md` → `vault/2-areas/learning/research-methods/`
- `.claude/agents/synthesis.md` → `vault/2-areas/learning/synthesis/`
- `.claude/agents/knowledge*.md` → `vault/2-areas/knowledge-mgmt/`

### 3️⃣ RESOURCES (Reference materials)

#### Architecture & Design
- `docs/pkm-architecture/LAKEHOUSE-*.md` → `vault/3-resources/architecture/lakehouse/`
- `docs/pkm-architecture/STORAGE-ARCHITECTURE.md` → `vault/3-resources/architecture/storage/`
- `docs/pkm-architecture/VAULT-STRUCTURE-SPECIFICATION.md` → `vault/3-resources/specifications/`

#### Development Resources
- `resources/references/*.md` → `vault/3-resources/references/`
- `knowledge-base/frameworks/*` → `vault/3-resources/frameworks/`
- `knowledge-base/tools/*` → `vault/3-resources/tools/`

#### Investment & Finance
- `knowledge-base/investment-strategies/*` → `vault/3-resources/finance/strategies/`
- `resources/datasets/fx-data/*` → `vault/3-resources/datasets/fx/`
- `resources/papers/currency-valuation/*` → `vault/3-resources/papers/finance/`

#### Templates & Examples
- `resources/templates/*` → `vault/3-resources/templates/`
- `knowledge-base/examples/*` → `vault/3-resources/examples/`

### 4️⃣ ARCHIVES (Completed/Inactive)

#### Legacy Documentation
- `docs/archive-v1/*` → `vault/4-archives/v1-docs/`
- Old experiment results → `vault/4-archives/experiments/`

## Migration Priority Order

### Phase 1: High-Value Content (Day 1-2)
1. **PKM Architecture docs** - Core system documentation
2. **Claude agents** - Active automation tools
3. **Implementation plans** - Current project docs

### Phase 2: Active Projects (Day 3)
1. **Experiments** - Active code and notebooks
2. **Knowledge concepts** - Core knowledge base

### Phase 3: Reference Materials (Day 4)
1. **Frameworks** - Mental models and methodologies
2. **Tools documentation** - Reference guides
3. **Investment strategies** - Domain knowledge

### Phase 4: Archive & Cleanup (Day 5)
1. **Archive old versions**
2. **Remove duplicates**
3. **Update links**

## Atomic Note Extraction Plan

### Documents to Split into Atomic Notes

#### From PKM Architecture Docs
- `PKM-SYSTEM-SPECIFICATION.md` → Extract:
  - Core principles (5-7 notes)
  - Each methodology (PARA, Zettelkasten, etc.)
  - Technical components (10-15 notes)

- `LAKEHOUSE-ARCHITECTURE.md` → Extract:
  - Iceberg concepts
  - SlateDB principles
  - Medallion architecture pattern
  - Each major component

#### From Knowledge Base
- Investment strategies → One note per strategy
- Frameworks → One note per framework principle
- Tools → One note per tool with use cases

## Link Building Strategy

### Bidirectional Links to Create
1. **Vertical Links** (hierarchy)
   - Project ↔ Sub-projects
   - Concepts ↔ Examples
   - Principles ↔ Implementations

2. **Horizontal Links** (related)
   - Similar concepts
   - Alternative approaches
   - Complementary tools

3. **Cross-Domain Links**
   - PKM ↔ Development practices
   - Architecture ↔ Implementation
   - Theory ↔ Practice

## Migration Tracking

### Files to Migrate
- [ ] 57 docs files
- [ ] 10+ Claude agents
- [ ] 5+ knowledge-base categories
- [ ] 3+ experiments
- [ ] 2+ resource collections

### Success Metrics
- [ ] All markdown files in vault
- [ ] 50+ atomic notes created
- [ ] 100+ bidirectional links
- [ ] Zero orphan files
- [ ] Complete PARA organization

## Automation Opportunities

### Scripts to Create
1. **Bulk file mover** - Move files maintaining structure
2. **Frontmatter adder** - Add metadata to all files
3. **Link converter** - Update relative links
4. **Atomic splitter** - Break long docs into notes

## Next Actions

1. ✅ Create migration map (this document)
2. [ ] Start with PKM architecture docs
3. [ ] Move Claude agents to areas
4. [ ] Extract atomic notes from long docs
5. [ ] Build link network
6. [ ] Verify no orphans
7. [ ] Archive old structure

---

*Migration map follows PARA principles and FR-first approach*
*Focus on high-value content that enables daily PKM usage*