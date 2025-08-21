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
├── 0-inbox/             # 📥 Capture everything here first
├── 1-projects/          # 🎯 Active projects with deadlines
├── 2-areas/             # 🔄 Ongoing responsibilities  
├── 3-resources/         # 📚 Reference materials
├── 4-archives/          # 🗄️ Completed/inactive items
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
1. **Capture First, Organize Later**: Everything goes to `vault/0-inbox/` first
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
3. **Project Updates**: Update project status in `vault/1-projects/` daily
4. **Archive Completed**: Move finished projects to `vault/4-archives/`
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

### For Every Session
1. Check daily note: `vault/daily/YYYY/MM-month/YYYY-MM-DD.md`
2. Process any inbox items: `vault/0-inbox/`
3. Update relevant projects: `vault/1-projects/`
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