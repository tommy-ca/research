# PKM Dogfooding Plan - Transform Research Repository

## Executive Summary

This document outlines the transformation of our research repository into a fully functional PKM vault, following our own specifications and architecture. We will "eat our own dog food" by implementing the PKM system we designed within this repository.

**Timeline**: 4 weeks (Phase 1) + ongoing iterations
**Approach**: FR-first, specs-driven development
**Platform**: Claude Code as implementation layer

## Current State Analysis

### Existing Structure
```
research/
├── .claude/           # ✅ Agent framework ready
├── docs/              # Mixed documentation
│   ├── pkm-architecture/  # ✅ PKM specs
│   └── archive-v1/    # Legacy content
├── resources/         # Reference materials
└── README.md         # Project overview
```

### Gap Analysis
| Required | Current | Action Needed |
|----------|---------|--------------|
| PARA structure | Partial folders | Create P/A/R/A folders |
| Daily notes | None | Set up journal structure |
| Inbox | None | Create capture workflow |
| Zettelkasten | None | Implement atomic notes |
| Templates | Basic | Expand template library |
| Processing | Manual | Automate with Claude |

## Implementation Schedule

### Week 1: Vault Structure & Basic Operations (Jan 22-26, 2024)

#### Day 1-2: PKM Vault Structure
```yaml
tasks:
  - task: Create PARA structure
    deliverable: |
      vault/
      ├── 0-inbox/           # Capture & triage
      ├── 1-projects/        # Active projects
      ├── 2-areas/           # Ongoing responsibilities
      ├── 3-resources/       # Reference materials
      ├── 4-archives/        # Inactive items
      ├── daily/             # Daily notes
      ├── permanent/         # Zettelkasten
      └── templates/         # Note templates
    
  - task: Set up daily notes
    deliverable: Daily note automation
    
  - task: Create inbox workflow
    deliverable: Capture templates
```

#### Day 3-4: Git Integration & Automation
```yaml
tasks:
  - task: Configure Git hooks
    deliverable: Auto-commit for daily notes
    
  - task: Set up branch strategy
    deliverable: |
      - main: Published knowledge
      - develop: Work in progress
      - capture/*: Inbox items
    
  - task: Create .gitignore rules
    deliverable: Privacy protection
```

#### Day 5: Basic Claude Commands
```yaml
tasks:
  - task: Implement capture command
    deliverable: /pkm-capture functionality
    
  - task: Create process command
    deliverable: /pkm-process inbox
    
  - task: Set up search command
    deliverable: /pkm-search implementation
```

### Week 2: Processing Pipeline (Jan 29 - Feb 2, 2024)

#### Day 6-7: Content Migration
```yaml
tasks:
  - task: Migrate existing docs
    deliverable: |
      - Archive old structure
      - Convert to atomic notes
      - Apply PARA organization
    
  - task: Process research materials
    deliverable: Structured knowledge base
```

#### Day 8-9: Metadata & Tagging
```yaml
tasks:
  - task: Implement frontmatter
    deliverable: YAML metadata standard
    
  - task: Create tag taxonomy
    deliverable: Hierarchical tag system
    
  - task: Add backlinks
    deliverable: Bidirectional linking
```

#### Day 10: Quality Validation
```yaml
tasks:
  - task: Validate structure
    deliverable: Compliance report
    
  - task: Test workflows
    deliverable: Working PKM system
```

### Week 3-4: Intelligence Layer (Feb 5-16, 2024)

#### Enhanced Processing
```yaml
tasks:
  - task: NLP extraction
    deliverable: Auto-tagging system
    
  - task: Concept mapping
    deliverable: Knowledge graph
    
  - task: Summary generation
    deliverable: Multi-level summaries
```

## Vault Structure Specification

### Directory Layout
```
research/
├── .claude/                    # Claude Code configuration
│   ├── agents/                 # PKM agents
│   ├── hooks/                  # Automation
│   └── settings.json          # Configuration
│
├── vault/                      # PKM Vault Root
│   ├── 0-inbox/               # 📥 Capture
│   │   ├── README.md          # Inbox processing guide
│   │   ├── quick-capture/     # Fleeting notes
│   │   ├── web-clips/         # Web content
│   │   └── voice-notes/       # Audio transcriptions
│   │
│   ├── 1-projects/            # 🎯 Active Projects
│   │   ├── pkm-system/        # This PKM implementation
│   │   ├── research-topics/   # Active research
│   │   └── experiments/       # Ongoing experiments
│   │
│   ├── 2-areas/               # 🔄 Areas of Responsibility
│   │   ├── knowledge-mgmt/    # PKM maintenance
│   │   ├── learning/          # Continuous learning
│   │   ├── tools/             # Tool management
│   │   └── processes/         # Workflow optimization
│   │
│   ├── 3-resources/           # 📚 Reference Library
│   │   ├── concepts/          # Core concepts
│   │   ├── frameworks/        # Mental models
│   │   ├── references/        # External resources
│   │   └── snippets/          # Code/text snippets
│   │
│   ├── 4-archives/            # 🗄️ Inactive Items
│   │   ├── completed/         # Finished projects
│   │   ├── deprecated/        # Outdated content
│   │   └── cold-storage/      # Long-term archive
│   │
│   ├── daily/                 # 📅 Daily Notes
│   │   ├── 2024/             
│   │   │   ├── 01-january/   
│   │   │   │   ├── 2024-01-21.md
│   │   │   │   └── ...
│   │   └── README.md         # Daily note guide
│   │
│   ├── permanent/             # 🧠 Zettelkasten
│   │   ├── README.md          # Zettel principles
│   │   ├── index.md           # Master index
│   │   └── notes/             # Atomic notes (ID-based)
│   │       ├── 202401210001-pkm-principles.md
│   │       └── ...
│   │
│   └── templates/             # 📝 Note Templates
│       ├── daily-note.md      
│       ├── project-note.md
│       ├── meeting-note.md
│       ├── book-note.md
│       ├── zettel-note.md
│       └── review-note.md
│
├── docs/                       # 📖 Documentation
│   └── pkm-architecture/       # System specs
│
└── .pkm/                       # PKM Configuration
    ├── config.yaml            # System settings
    ├── shortcuts.yaml         # Quick commands
    └── workflows/             # Automation scripts
```

### Metadata Standards

#### Frontmatter Template
```yaml
---
id: "{{timestamp}}-{{slug}}"
title: "Note Title"
date: 2024-01-21
type: note|project|area|resource|daily|zettel
tags: [tag1, tag2]
status: draft|active|review|complete|archived
links: 
  - "[[related-note-1]]"
  - "[[related-note-2]]"
source: "URL or reference"
created: 2024-01-21T10:00:00Z
modified: 2024-01-21T10:00:00Z
---
```

### Naming Conventions

#### Files
- **Daily Notes**: `YYYY-MM-DD.md` (e.g., `2024-01-21.md`)
- **Zettelkasten**: `YYYYMMDDHHmm-title-slug.md` (e.g., `202401211030-pkm-principles.md`)
- **Projects**: `project-name/README.md` + supporting files
- **Resources**: `category/descriptive-name.md`

#### Folders
- Use lowercase with hyphens
- Prefix with numbers for ordering (0-inbox, 1-projects)
- Descriptive names for clarity

## Claude Code Integration

### PKM Commands Implementation

```python
# .claude/commands/pkm_commands.py

class PKMCommands:
    """
    PKM command implementations for Claude Code
    """
    
    def capture(self, content: str, source: str = None):
        """
        /pkm-capture "content" --source="optional source"
        Captures content to inbox for processing
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"vault/0-inbox/quick-capture/{timestamp}.md"
        
        frontmatter = {
            "date": datetime.now().isoformat(),
            "type": "capture",
            "status": "inbox",
            "source": source
        }
        
        # Create note with frontmatter
        create_note(filename, content, frontmatter)
        
    def process_inbox(self):
        """
        /pkm-process
        Processes inbox items with NLP and categorization
        """
        inbox_items = glob.glob("vault/0-inbox/**/*.md")
        
        for item in inbox_items:
            content = read_file(item)
            
            # Extract concepts
            concepts = extract_concepts(content)
            
            # Determine category (PARA)
            category = classify_note(content)
            
            # Generate tags
            tags = generate_tags(content, concepts)
            
            # Move to appropriate folder
            move_to_category(item, category, tags)
    
    def daily_note(self):
        """
        /pkm-daily
        Creates or opens today's daily note
        """
        today = datetime.now().strftime("%Y-%m-%d")
        month = datetime.now().strftime("%m-%B").lower()
        year = datetime.now().year
        
        filepath = f"vault/daily/{year}/{month}/{today}.md"
        
        if not exists(filepath):
            create_from_template("daily-note", filepath)
        
        return open_in_editor(filepath)
    
    def create_zettel(self, title: str, content: str):
        """
        /pkm-zettel "title" "content"
        Creates atomic note in Zettelkasten
        """
        zettel_id = datetime.now().strftime("%Y%m%d%H%M")
        slug = slugify(title)
        filename = f"vault/permanent/notes/{zettel_id}-{slug}.md"
        
        frontmatter = {
            "id": zettel_id,
            "title": title,
            "type": "zettel",
            "created": datetime.now().isoformat()
        }
        
        create_note(filename, content, frontmatter)
        update_zettel_index(zettel_id, title)
```

### Hook Automation

```bash
#!/bin/bash
# .claude/hooks/pkm_auto_process.sh

# Auto-process on file save
if [[ "$1" == *"vault/0-inbox"* ]]; then
    claude-code /pkm-process "$1"
fi

# Daily note automation
if [[ "$(date +%H:%M)" == "09:00" ]]; then
    claude-code /pkm-daily
fi

# Weekly review reminder
if [[ "$(date +%u)" == "7" ]]; then
    claude-code /pkm-review weekly
fi
```

## Migration Strategy

### Phase 1: Structure (Week 1)
1. Create vault directory structure
2. Set up templates
3. Configure Git integration
4. Implement basic commands

### Phase 2: Content (Week 2)
1. Migrate existing documentation
2. Convert to atomic notes
3. Apply metadata standards
4. Establish linking

### Phase 3: Intelligence (Week 3-4)
1. Enable auto-processing
2. Implement NLP extraction
3. Set up knowledge graph
4. Create dashboards

## Success Metrics

### Week 1 Success
- [ ] Vault structure created
- [ ] Templates operational
- [ ] Basic commands working
- [ ] Git integration complete

### Week 2 Success
- [ ] All content migrated
- [ ] Metadata applied
- [ ] Links established
- [ ] Inbox workflow active

### Week 3-4 Success
- [ ] Auto-processing enabled
- [ ] NLP extraction working
- [ ] Knowledge graph building
- [ ] Daily workflow smooth

## Dogfooding Principles

### We Will
1. **Use our own system daily** - All research uses PKM vault
2. **Follow our specs** - Strict adherence to architecture
3. **Document everything** - Transparent process
4. **Iterate based on usage** - Continuous improvement
5. **Share learnings** - Open development

### We Won't
1. Skip steps for convenience
2. Use external tools that bypass our system
3. Ignore our own best practices
4. Delay feedback incorporation

## Daily Workflow

### Morning Routine
```bash
# Start day
claude-code /pkm-daily           # Open daily note
claude-code /pkm-review inbox    # Process inbox
claude-code /pkm-agenda          # Review projects
```

### Capture Workflow
```bash
# Quick capture
claude-code /pkm-capture "idea or thought"

# Web capture
claude-code /pkm-web "https://article.url"

# Meeting notes
claude-code /pkm-meeting "Meeting Title"
```

### Evening Review
```bash
# End of day
claude-code /pkm-process         # Process inbox
claude-code /pkm-link            # Update links
claude-code /pkm-commit          # Git commit
```

## Next Actions

### Immediate (Today)
1. Create vault directory structure
2. Set up daily notes folder
3. Create initial templates
4. Configure Git hooks

### This Week
1. Implement basic PKM commands
2. Migrate existing content
3. Set up automation
4. Begin daily usage

### Next Week
1. Add NLP processing
2. Implement knowledge graph
3. Create dashboards
4. Gather feedback

## Quality Checklist

### Structure Validation
- [ ] PARA folders created
- [ ] Templates ready
- [ ] Git configured
- [ ] Commands working

### Content Standards
- [ ] Frontmatter consistent
- [ ] Naming conventions followed
- [ ] Links bidirectional
- [ ] Tags hierarchical

### Automation
- [ ] Hooks installed
- [ ] Commands documented
- [ ] Workflows tested
- [ ] Backups configured

---

*PKM Dogfooding Plan v1.0 - Transform research repository into working PKM vault*
*Following our own specifications for maximum learning and validation*