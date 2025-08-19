# Agent Migration Guide

## Overview

We've simplified the Claude Code agents to follow best practices - clean, concise, and focused. The previous 600+ line agent files have been replaced with ~75 line focused agents.

## What Changed

### Before (Bloated - Now Removed)
- `deep-research.md` - 607 lines
- `deep-research-v2.md` - 693 lines  
- `peer-review.md` - 308 lines
- Total: 1,608 lines of complexity

### After (Simplified)
- `research.md` - 75 lines
- `review.md` - 74 lines
- `synthesis.md` - 73 lines
- Total: 222 lines of clarity

## Command Migration

### Research Commands

| Old Command | New Command | Notes |
|-------------|-------------|-------|
| `/research-deep "topic" --depth=exhaustive --sources=academic,government --timeline=21` | `/research "topic" --depth=comprehensive --sources=academic` | Simplified parameters |
| `/research-plan "topic"` | Built into `/research` | Planning is automatic |
| `/research-execute plan-123` | Not needed | Research executes directly |
| `/research-validate "claim"` | `/validate "claim"` | Simplified name |
| `/research-gap "domain"` | Part of `/research` output | Gaps identified automatically |
| `/research-refine research-123` | Not needed | Quality built into process |
| `/research-status research-123` | `/research-status` | Simplified |

### Review Commands

| Old Command | New Command | Notes |
|-------------|-------------|-------|
| `/peer-review "content" --comprehensive` | `/review [content]` | Simplified |
| `/quality-assessment "content"` | `/quality-check [content]` | Clearer name |
| `/bias-detection "content" --all` | `/bias-check [content]` | Simplified |

### Synthesis Commands

| Old Command | New Command | Notes |
|-------------|-------------|-------|
| `/synthesis-cross-domain [sources]` | `/synthesize [sources]` | Simplified |
| `/framework-generation "topic"` | `/create-framework "topic"` | Clearer |
| `/insight-extraction [content]` | `/extract-insights [content]` | Same |

## Key Improvements

### 1. Simplicity
- Commands are intuitive and self-explanatory
- Fewer parameters, sensible defaults
- Clear, concise documentation

### 2. Performance
- Faster agent loading (86% less code to parse)
- Reduced memory footprint
- Quicker command execution

### 3. Maintainability
- Technical details moved to separate documentation
- Clean separation of concerns
- Easier to understand and modify

## Where Did the Details Go?

Technical specifications have been properly organized:

- **Implementation Details**: `docs/research/agent-systems/technical/agent-implementation-details.md`
- **Specifications**: `docs/research/agent-systems/specifications/`
- **Quality Framework**: `docs/research/agent-systems/quality-assurance/`
- **Architecture**: `docs/research/agent-systems/architecture/`

## Quick Start with New Agents

```bash
# Simple research
/research "artificial intelligence trends"

# Research with options
/research "quantum computing" --depth=comprehensive --sources=academic

# Validate findings
/validate "quantum computers can break RSA encryption"

# Review quality
/review research_output.md

# Synthesize multiple sources
/synthesize research1.md research2.md research3.md
```

## Benefits of Migration

1. **Faster**: Agents load and execute more quickly
2. **Clearer**: Commands are self-documenting
3. **Simpler**: Fewer parameters to remember
4. **Reliable**: Same quality, less complexity
5. **Maintainable**: Easier to update and extend

## Legacy Files Removed

Previous bloated agent files have been removed. The simplified agents now provide the same functionality with better performance.

## Questions?

See the main agent documentation:
- `.claude/agents/README.md` - Agent overview
- Individual agent files for specific commands
- Technical documentation for implementation details