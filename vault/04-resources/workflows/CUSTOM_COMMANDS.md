# Custom Commands System Documentation

## Overview

The v2.1 system adds **extensibility without complexity** through a minimal custom commands framework.

## Architecture

### System Components
```
Core System (154 lines):
├── agents/research.md     32 lines
├── agents/synthesis.md    32 lines
└── hooks/router.sh        90 lines (+33 for custom support)

Custom Commands (324 lines):
├── commands/
│   ├── analyze.md         21 lines (example)
│   ├── compare.md         21 lines (example)
│   ├── validate.md        21 lines (example)
│   ├── SPECIFICATION.md   75 lines (how to create)
│   └── GUIDE.md          186 lines (detailed guide)

Configuration:
└── settings.json          44 lines

Total: 522 lines (still 60% smaller than v1!)
```

## How It Works

### 1. Command Definition
Custom commands are simple Markdown files with YAML frontmatter:

```markdown
---
name: analyze
pattern: /analyze
agent: research
description: Focused analysis command
---

# Analyze Command

Deep analysis with specific focus.

## Usage
`/analyze "topic" "focus-area"`

## Example
`/analyze "AI safety" "alignment problem"`
```

### 2. Automatic Loading
The router automatically loads commands on startup:
```bash
# Router scans .claude/commands/*.md
# Extracts pattern and agent from frontmatter
# Registers command for routing
```

### 3. Intelligent Processing
Commands are just routing rules - agents handle all intelligence:
```
/analyze "topic" → Router → Research Agent → Intelligent Analysis
```

## Creating Custom Commands

### Quick Start (2 minutes)
1. Copy an example: `cp .claude/commands/analyze.md .claude/commands/mycommand.md`
2. Edit frontmatter (name, pattern, agent)
3. Test: `/mycommand "test"`

### Command Specification
Required fields:
- `name`: Unique identifier
- `pattern`: Match pattern (must start with `/`)
- `agent`: Which agent processes (research or synthesis)

Optional fields:
- `description`: One-line description
- `parameters`: Expected parameters (documentation only)
- `output_format`: Output hint (agents adapt automatically)

## Examples

### Analysis Command
```yaml
pattern: /analyze
agent: research
purpose: Focused, deep analysis on specific aspects
```

### Comparison Command
```yaml
pattern: /compare
agent: synthesis
purpose: Systematic comparison of multiple items
```

### Validation Command
```yaml
pattern: /validate
agent: research
purpose: Fact-checking and claim validation
```

### Industry Analysis (Custom)
```yaml
pattern: /industry
agent: research
purpose: Comprehensive industry sector analysis
```

### Tech Stack Review (Custom)
```yaml
pattern: /tech-stack
agent: synthesis
purpose: Evaluate and recommend technology stacks
```

## Best Practices

### DO ✅
- Keep commands focused (single purpose)
- Reuse existing agents (don't create new ones)
- Provide clear usage examples
- Keep command files under 50 lines
- Use descriptive patterns

### DON'T ❌
- Add complex logic (agents handle that)
- Create new agents (reuse research/synthesis)
- Over-specify parameters (agents are smart)
- Duplicate existing functionality
- Add configuration complexity

## Philosophy

### "Commands are just routing rules"
- **No logic in commands** - Just routing metadata
- **Agents handle complexity** - They're intelligent
- **Minimal specification** - Just enough to route
- **Maximum reusability** - Two agents, infinite commands

### Extensibility without Complexity
- **No new infrastructure** - Reuses existing agents
- **No configuration hell** - Simple frontmatter
- **No learning curve** - Copy, edit, use
- **No performance impact** - Just routing rules

## Advanced Usage

### Command Chaining
Commands can work together:
```bash
/research "quantum computing"
/analyze output.md "commercial viability"
/compare "quantum" "classical" "for optimization"
```

### Domain-Specific Commands
Create specialized commands for your domain:
```yaml
# Legal analysis
pattern: /legal-review
agent: research

# Medical research
pattern: /clinical-study
agent: research

# Business strategy
pattern: /market-analysis
agent: synthesis
```

### Team Collaboration
Teams can share custom commands:
```bash
# Share command library
git add .claude/commands/team-*.md
git commit -m "Team custom commands"
git push
```

## Troubleshooting

### Command not recognized
- Verify pattern starts with `/`
- Check file is in `.claude/commands/`
- Ensure valid YAML frontmatter

### Wrong agent behavior
- Research agent: Information gathering, analysis, validation
- Synthesis agent: Combining, comparing, framework generation

### Loading issues
- Check router.sh logs
- Validate YAML syntax
- Verify required fields

## Performance Impact

### Metrics
- **Core system**: 154 lines (was 121, +27% for extensibility)
- **With examples**: 522 lines (still 60% smaller than v1)
- **Routing overhead**: Negligible (simple pattern matching)
- **Memory impact**: Minimal (just routing table)

### Scalability
- Supports unlimited custom commands
- No performance degradation with more commands
- Each command is just 20-30 lines
- Agents handle all complexity

## Specification Summary

### Command Format
- **File type**: Markdown with YAML frontmatter
- **Location**: `.claude/commands/`
- **Size limit**: 50 lines recommended
- **Required fields**: name, pattern, agent
- **Pattern format**: Must start with `/`

### Agent Selection
- **research**: Analysis, validation, information gathering
- **synthesis**: Comparison, combination, pattern recognition

### Documentation
- **SPECIFICATION.md**: Technical specification (75 lines)
- **GUIDE.md**: User guide with examples (186 lines)
- **This file**: Complete documentation

## Conclusion

The custom commands system provides:
- ✅ **Extensibility** - Unlimited custom commands
- ✅ **Simplicity** - 20-line command definitions
- ✅ **Reusability** - Leverages existing agents
- ✅ **Maintainability** - Clear separation of concerns
- ✅ **Performance** - Minimal overhead

All while maintaining our core philosophy: **"Simplicity through intelligence"**

The system remains simple (522 total lines), yet infinitely extensible through intelligent agents that handle all complexity.

---

*Custom Commands v1.0 - Extensibility without complexity*