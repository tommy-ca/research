# CLAUDE.md

This file provides persistent guidance to Claude Code (claude.ai/code) when working with this repository as a Personal Knowledge Management (PKM) system.

## Project Overview

This is a living PKM vault implementing our own specifications through dogfooding. The repository serves as both a research knowledge base AND an active PKM system using the PARA method, Zettelkasten principles, and Claude Code as the intelligence layer.

## Official Claude Code Integration

This repository includes a complete `.claude/` folder structure following [Claude Code's official documentation](https://docs.anthropic.com/en/docs/claude-code):

### Agent System (`.claude/agents/`)
- **deep-research.md**: Comprehensive research capabilities with multi-source validation
- **peer-review.md**: Systematic quality assurance and peer review
- **synthesis.md**: Cross-domain integration and framework development
- **pkm-ingestion.md**: Content ingestion and processing (TDD-implemented)
- **pkm-processor.md**: NLP and knowledge extraction (specs-driven)
- **pkm-synthesizer.md**: Knowledge synthesis and insights (FR-first)
- **pkm-feynman.md**: Simplification and teaching (test-validated)

### Configuration (`.claude/settings.json`)
Project-level settings following [Claude Code Settings](https://docs.anthropic.com/en/docs/claude-code/settings) specification with:
- Agent configurations and quality standards
- Hook automation for research commands
- Permission management and security controls
- Environment variables and model selection

### Hook System (`.claude/hooks/`)
Automation scripts following [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) patterns:
- `research_command_handler.sh`: Routes research commands to appropriate agents
- `quality_check.sh`: Automatic quality validation after content creation

## Research Commands

### Deep Research
- `/research-deep "topic"` - Comprehensive research with multi-source validation
- `/research-validate "finding"` - Multi-source validation with confidence scoring
- `/research-gap "domain"` - Systematic research gap identification

### Quality Assurance  
- `/peer-review "file.md"` - Comprehensive systematic review
- `/review-methodology "file.md"` - Methodology validation
- `/validate-sources "file.md"` - Source quality assessment
- `/detect-bias "file.md"` - Multi-dimensional bias detection

### Synthesis
- `/research-synthesize` - Cross-domain research integration
- `/framework-develop "domain"` - Theoretical/practical framework development
- `/pattern-analyze "collection"` - Pattern identification and analysis

## Repository Structure

### PKM Vault Structure (Primary)
```
vault/                    # PKM Vault Root (PARA Method)
├── 00-inbox/            # 📥 Capture everything here first
├── 02-projects/         # 🎯 Active projects with deadlines
├── 03-areas/            # 🔄 Ongoing responsibilities  
├── 04-resources/        # 📚 Reference materials
├── 05-archives/         # 🗄️ Completed/inactive items
├── daily/               # 📅 Daily notes (YYYY/MM-month/YYYY-MM-DD.md)
├── permanent/           # 🧠 Zettelkasten atomic notes
└── templates/           # 📝 Note templates
```

### Supporting Directories
- `docs/`: System documentation, architecture specs, implementation guides
- `.claude/`: Claude Code agent integration and automation
- `.pkm/`: PKM configuration and workflows
- `resources/`: External references and datasets

## PKM Commands (Primary Workflow)

### Daily Operations
- `/pkm-daily` - Create/open today's daily note
- `/pkm-capture "content"` - Quick capture to inbox
- `/pkm-process` - Process inbox items with NLP
- `/pkm-review [daily|weekly|monthly]` - Review workflows

### Note Management
- `/pkm-zettel "title" "content"` - Create atomic note
- `/pkm-link "note"` - Find/suggest bidirectional links
- `/pkm-search "query"` - Search across vault
- `/pkm-tag "note"` - Auto-generate tags

### Organization
- `/pkm-organize` - Categorize notes by PARA method
- `/pkm-archive` - Move completed items to archives
- `/pkm-index` - Update permanent notes index

## Persistent PKM Rules

### ALWAYS (Non-Negotiable)
1. **Capture First, Organize Later**: Everything goes to `vault/00-inbox/` first
2. **Daily Notes**: Create/update `vault/daily/YYYY/MM-month/YYYY-MM-DD.md` for each day
3. **Atomic Notes**: One idea per note in `vault/permanent/notes/`
4. **Bidirectional Links**: Create `[[links]]` between related notes
5. **Frontmatter Required**: All notes must have YAML frontmatter with date, type, tags
6. **PARA Categorization**: Organize into Projects, Areas, Resources, or Archives
7. **Git Commits**: Auto-commit vault changes with descriptive messages

### NEVER (Prohibited)
1. **Skip Inbox**: Don't create notes directly in organized folders
2. **Long Notes**: Don't create notes with multiple unrelated ideas
3. **Orphan Notes**: Don't leave notes without links or categorization
4. **External Storage**: Don't store knowledge outside the vault
5. **Manual Timestamps**: Don't manually create timestamps (use automation)

### Processing Rules
1. **Inbox Zero**: Process inbox items within 48 hours
2. **Weekly Reviews**: Every Sunday, run `/pkm-review weekly`
3. **Project Updates**: Update project status in `vault/02-projects/` daily
4. **Archive Completed**: Move finished projects to `vault/05-archives/`
5. **Link Maintenance**: Check for broken links weekly

## PKM Workflow Automation

### On File Save
```bash
# Automatically triggered by .claude/hooks/pkm-auto-process.sh
- If in inbox → suggest categorization
- If daily note → extract tasks
- If zettel → update index and links
- Always → git commit
```

### Scheduled Tasks
- **9:00 AM Daily**: Create daily note
- **5:00 PM Daily**: Process inbox
- **Sunday 5:00 PM**: Weekly review
- **Month-end**: Archive completed items

### Auto-Processing Pipeline
1. **Capture** → Inbox with timestamp
2. **Extract** → Concepts, entities, topics
3. **Categorize** → PARA method classification
4. **Link** → Find related notes
5. **Tag** → Generate hierarchical tags
6. **Index** → Update search index

## Note Standards

### Frontmatter Template
```yaml
---
date: YYYY-MM-DD
type: daily|zettel|project|area|resource|capture
tags: [tag1, tag2]
status: draft|active|review|complete|archived
links: ["[[note1]]", "[[note2]]"]
---
```

### File Naming
- **Daily**: `YYYY-MM-DD.md`
- **Zettel**: `YYYYMMDDHHmm-title-slug.md`
- **Projects**: `project-name/README.md`
- **Captures**: `YYYYMMDDHHmmss.md`

## Research Workflow

### Standard Research Process
1. **Initialize**: `/research-deep "topic"` for comprehensive analysis
2. **Validate**: `/research-validate "key findings"` for verification
3. **Review**: `/peer-review "output.md"` for quality assurance
4. **Synthesize**: `/research-synthesize` for cross-domain integration
5. **Document**: Store in appropriate repository structure

### Quality Standards
- **Evidence Level**: Academic standards with peer review
- **Source Diversity**: Minimum 3 independent sources for critical claims
- **Bias Assessment**: Multi-dimensional bias detection and mitigation
- **Reproducibility**: Complete methodology documentation and audit trails

## Development Standards

### Core Development Principles

#### 1. Test-Driven Development (TDD) - MANDATORY
**All agents MUST follow TDD workflow:**
```
1. RED: Write failing test/spec first
2. GREEN: Write minimal code to pass
3. REFACTOR: Improve code while tests pass
```

**TDD Rules:**
- **NEVER write code without a test/spec first**
- **Tests define the specification**
- **Each feature starts with expected behavior**
- **Validation before implementation**

**TDD Example Workflow:**
```python
# 1. Write the test FIRST (RED)
def test_pkm_capture_creates_inbox_note():
    result = pkm_capture("Test content")
    assert exists(f"vault/0-inbox/{result.filename}")
    assert result.frontmatter.type == "capture"
    
# 2. Write minimal implementation (GREEN)
def pkm_capture(content):
    # Minimal code to make test pass
    
# 3. Refactor for quality (REFACTOR)
def pkm_capture(content, source=None, tags=None):
    # Improved implementation
```

#### 2. Specs-Driven Development - PRIMARY WORKFLOW
**Every implementation MUST follow:**
1. **SPEC FIRST**: Write complete specification document
2. **REVIEW SPEC**: Validate requirements and acceptance criteria
3. **IMPLEMENT**: Build according to specification
4. **VALIDATE**: Verify against original spec

**Specification Template:**
```markdown
## Feature: [Name]
### Requirements
- FR-001: [Functional requirement]
- FR-002: [Functional requirement]
- NFR-001: [Non-functional requirement] (deferred)

### Acceptance Criteria
- [ ] Given [context], When [action], Then [outcome]
- [ ] Given [context], When [action], Then [outcome]

### Test Cases
1. Test [scenario]: [expected result]
2. Test [scenario]: [expected result]
```

#### 3. FR-First Prioritization - ALWAYS
**Functional Requirements (FRs) ALWAYS come before Non-Functional Requirements (NFRs):**

**PRIORITIZE (FRs):**
- ✅ User-facing features
- ✅ Core functionality  
- ✅ Business logic
- ✅ Workflows that deliver value
- ✅ Integration points

**DEFER (NFRs):**
- ⏸️ Performance optimization (until it blocks FRs)
- ⏸️ Scalability (until proven needed)
- ⏸️ Security hardening (basic security only initially)
- ⏸️ Monitoring/metrics (until system is stable)
- ⏸️ High availability (until production)

**Decision Framework:**
```
if feature.delivers_user_value:
    priority = "HIGH"  # Implement now
elif feature.enables_other_features:
    priority = "MEDIUM"  # Implement soon
elif feature.improves_quality and not feature.blocks_progress:
    priority = "LOW"  # Defer to later phase
```

### Research Excellence
- All research must be reproducible with complete documentation
- Multi-source validation required for critical findings
- Systematic bias detection and mitigation protocols
- Peer review validation for substantial research outputs

### Technical Standards
- Follow Claude Code's official agent patterns and configurations
- Use structured research workflows with quality gates
- Maintain comprehensive audit trails and version control
- Implement security and privacy best practices
- **MANDATORY: TDD for all new features**
- **MANDATORY: Specs-driven development flow**
- **MANDATORY: FR-first prioritization**

### Core Software Engineering Principles

#### 4. KISS Principle (Keep It Simple, Stupid) - ALWAYS PRIORITIZE
**Simplicity is the ultimate sophistication in PKM systems:**

**KISS Rules:**
- **Simple over clever**: Write code that anyone can understand and maintain
- **Minimal viable features**: Start with the simplest implementation that works
- **Clear function names**: Use descriptive names over comments
- **Single-purpose functions**: Each function should do one thing well
- **Avoid premature optimization**: Make it work first, optimize later only if needed

**KISS Examples:**
```python
# GOOD (KISS): Simple, clear, readable
def create_note_id():
    return datetime.now().strftime("%Y%m%d%H%M")

# BAD (Complex): Over-engineered for current needs
def create_note_id(format_type="timestamp", precision="minute", timezone=None, prefix=""):
    # 50 lines of complex logic...
```

**KISS Decision Framework:**
```
if solution.solves_problem and solution.is_simple:
    implement()
elif solution.solves_problem and solution.is_complex:
    simplify_first()
else:
    reject()
```

#### 5. DRY Principle (Don't Repeat Yourself) - ELIMINATE DUPLICATION
**Every piece of knowledge must have a single, unambiguous representation:**

**DRY Rules:**
- **Extract common logic**: Identify patterns and create reusable functions
- **Configuration over code**: Use data structures for repeated patterns
- **Shared constants**: Define values once, reference everywhere
- **Template patterns**: Create templates for similar structures
- **Inheritance hierarchies**: Use base classes for common behavior

**DRY Implementation Patterns:**
```python
# GOOD (DRY): Shared configuration
PARA_CATEGORIES = {
    'project': '01-projects',
    'area': '02-areas',
    'resource': '03-resources',
    'archive': '04-archives'
}

# GOOD (DRY): Common base class
class BasePkmProcessor:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.create_directories()

class PkmCapture(BasePkmProcessor):
    pass

class PkmInboxProcessor(BasePkmProcessor):
    pass
```

**DRY vs Copy-Paste Decision:**
- **Copy once**: Acceptable, monitor for patterns
- **Copy twice**: Consider extracting common logic
- **Copy thrice**: MUST extract - DRY violation

#### 6. SOLID Principles - ARCHITECTURAL FOUNDATION
**Object-oriented design principles for maintainable, flexible code:**

**S - Single Responsibility Principle (SRP)**
- **Rule**: Each class should have only one reason to change
- **PKM Application**: Separate capture, processing, and indexing concerns
```python
class PkmCapture:           # Only responsible for capturing content
class PkmInboxProcessor:    # Only responsible for inbox processing  
class PkmNoteIndexer:       # Only responsible for indexing notes
```

**O - Open/Closed Principle (OCP)**
- **Rule**: Classes should be open for extension, closed for modification
- **PKM Application**: Use strategy pattern for different categorization methods
```python
class BaseCategorizer:
    def categorize(self, content: str) -> str:
        raise NotImplementedError

class ParaCategorizer(BaseCategorizer):
    def categorize(self, content: str) -> str:
        # PARA method implementation

class TagBasedCategorizer(BaseCategorizer):
    def categorize(self, content: str) -> str:
        # Tag-based implementation
```

**L - Liskov Substitution Principle (LSP)**
- **Rule**: Derived classes must be substitutable for their base classes
- **PKM Application**: All processors must work with same interfaces
```python
def process_content(processor: BasePkmProcessor, content: str):
    # Must work with any processor implementation
    return processor.process(content)
```

**I - Interface Segregation Principle (ISP)**
- **Rule**: Clients shouldn't depend on interfaces they don't use
- **PKM Application**: Separate interfaces for different capabilities
```python
class Searchable:
    def search(self, query: str) -> List[str]: pass

class Linkable:
    def create_links(self, content: str) -> List[str]: pass

class Taggable:
    def generate_tags(self, content: str) -> List[str]: pass
```

**D - Dependency Inversion Principle (DIP)**
- **Rule**: Depend on abstractions, not concretions
- **PKM Application**: Inject dependencies rather than hard-coding
```python
class PkmSystem:
    def __init__(self, 
                 capture_service: CaptureInterface,
                 processor_service: ProcessorInterface,
                 indexer_service: IndexerInterface):
        self.capture = capture_service
        self.processor = processor_service
        self.indexer = indexer_service
```

#### Integration with TDD and Specs-Driven Development

**Principle Hierarchy:**
1. **TDD** - Test specification drives implementation
2. **Specs-driven** - Requirements define architecture
3. **FR-first** - User value before optimization
4. **KISS** - Simple solutions over clever ones
5. **DRY** - Eliminate duplication after patterns emerge
6. **SOLID** - Structure for long-term maintainability

**Decision Framework:**
```python
def design_decision(requirement, options):
    # 1. Does it pass tests? (TDD)
    if not all(test.passes for option in options):
        return "write_better_tests"
    
    # 2. Does it meet specs? (Specs-driven)
    valid_options = [opt for opt in options if opt.meets_specs]
    
    # 3. Does it deliver user value? (FR-first)
    fr_options = [opt for opt in valid_options if opt.delivers_value]
    
    # 4. Is it simple? (KISS)
    simple_options = [opt for opt in fr_options if opt.is_simple]
    
    # 5. Does it avoid duplication? (DRY)  
    dry_options = [opt for opt in simple_options if not opt.duplicates_code]
    
    # 6. Is it well-structured? (SOLID)
    return min(dry_options, key=lambda x: x.solid_violations)
```

### Documentation Requirements
- Research methodologies must be fully documented
- All findings require source attribution and validation
- Quality assessments and peer review reports included
- Clear naming conventions and organizational structure

## Code and Notebook Management

- Experimental code should include comprehensive documentation
- Jupyter notebooks require markdown explanations for each analytical step
- Data files must include metadata, source information, and validation
- Results documentation includes analysis, conclusions, and quality metrics
- All outputs subject to automatic quality validation when substantial

## Integration with Official Claude Code

This repository leverages Claude Code's official capabilities:

- **[Settings Management](https://docs.anthropic.com/en/docs/claude-code/settings)**: Hierarchical configuration
- **[Agent Framework](https://docs.anthropic.com/en/docs/claude-code/mcp)**: Specialized research agents
- **[Hook System](https://docs.anthropic.com/en/docs/claude-code/hooks)**: Automated workflows
- **[CLI Integration](https://docs.anthropic.com/en/docs/claude-code/cli-reference)**: Custom commands

For detailed information about the agent system, see `.claude/README.md`.

## PKM Dogfooding Principles

### Active Implementation
- **This repository IS the PKM system** - We use it daily for all knowledge work
- **Continuous improvement** - Every friction point becomes an enhancement
- **Transparent development** - All PKM work happens in the open
- **Real-world validation** - Features tested through actual use

### Quality Metrics
- **Inbox Processing Time**: < 5 minutes per item
- **Daily Note Completion**: 100% daily
- **Link Density**: > 3 links per permanent note
- **Weekly Review Completion**: Every Sunday
- **Archive Rate**: Monthly cleanup

### Integration Points
1. **Research → PKM**: All research outputs become permanent notes
2. **PKM → Research**: Knowledge graph informs research directions
3. **Daily → Projects**: Daily notes feed project updates
4. **Capture → Synthesis**: Inbox items become synthesized knowledge

## Working with This Repository

### Development Workflow for Agents

#### When Implementing ANY Feature
1. **Write Spec First** (specs-driven development)
   ```markdown
   Feature: PKM Capture Command
   Requirements:
   - FR-001: Capture text to inbox with timestamp
   - FR-002: Add frontmatter metadata
   - NFR-001: <100ms response (DEFER)
   ```

2. **Write Test First** (TDD)
   ```python
   def test_capture_creates_file():
       # Test BEFORE implementation
   ```

3. **Implement FR First** (functional before performance)
   - Build user-facing feature
   - Defer optimization
   - Ship working code fast

4. **Validate Against Spec**
   - Check acceptance criteria
   - Run all tests
   - Document completion

### For Every Session
1. Check daily note: `vault/daily/YYYY/MM-month/YYYY-MM-DD.md`
2. Process any inbox items: `vault/00-inbox/`
3. Update relevant projects: `vault/02-projects/`
4. Create atomic notes for insights: `vault/permanent/notes/`
5. Commit changes with descriptive messages

### When Creating Content
1. **Always start in inbox** unless updating existing notes
2. **Use templates** from `vault/templates/`
3. **Add frontmatter** with appropriate metadata
4. **Create links** to related content
5. **Follow PARA** categorization

### When Processing Information
1. **Extract key concepts** into atomic notes
2. **Identify patterns** across notes
3. **Build connections** through links
4. **Generate summaries** at multiple levels
5. **Archive completed** items promptly

## Success Indicators

### Daily Success
- [ ] Daily note created and updated
- [ ] Inbox processed (or scheduled)
- [ ] Projects reviewed
- [ ] Knowledge captured

### Weekly Success  
- [ ] Weekly review completed
- [ ] Links maintained
- [ ] Archives cleaned
- [ ] Patterns identified

### System Health
- [ ] All notes have frontmatter
- [ ] No orphan notes exist
- [ ] Inbox stays near zero
- [ ] Knowledge graph growing
- [ ] Regular git commits

---

*This CLAUDE.md serves as the persistent guide for Claude Code to maintain and evolve this PKM system through active dogfooding.*