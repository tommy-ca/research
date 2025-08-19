# Claude Code Agent System Configuration

## Overview

This directory contains the Claude Code specific configuration and implementation files for the multi-agent research system. Files in this directory are directly used by Claude Code and follow official Claude Code patterns.

## Directory Structure

```
.claude/
├── README.md                     # This file - Claude Code specific documentation
├── agents/                       # Agent definitions (Simple & Clean)
│   ├── research.md              # Research agent (75 lines)
│   ├── review.md                # Review agent (74 lines)
│   ├── synthesis.md             # Synthesis agent (73 lines)
│   ├── README.md                # Agent overview
│   └── MIGRATION.md             # Migration guide from old agents
├── hooks/                        # Claude Code hooks for automation
│   ├── research_command_handler.sh        # Research command processing
│   ├── quality_check.sh                   # Quality validation automation
│   └── specification_compliance_hook.sh   # Compliance validation
└── logs/                        # System logs (created automatically)
    ├── compliance_validation.log
    ├── quality_check.log
    └── research_commands.log
```

**Note**: Specifications and steering documents have been moved to:
- `docs/research/agent-systems/specifications/` - Formal system specifications
- `docs/research/agent-systems/steering/` - Implementation guidance

## Quick Start

### Essential Files for Claude Code

1. **Agent Definition**: `.claude/agents/deep-research-v2.md`
   - Primary research agent following Claude Code patterns
   - YAML frontmatter with agent configuration
   - Specification-compliant implementation

2. **Hooks**: `.claude/hooks/*.sh`
   - Automated validation and quality checking
   - Integrated with Claude Code workflow
   - Real-time compliance monitoring

3. **Specifications**: `docs/research/agent-systems/specifications/`
   - Formal system specifications
   - Interface, behavior, quality, and workflow definitions
   - Version-controlled specification framework

## Agent Usage

### Deep Research Agent v2.0

The primary research agent is configured for Claude Code and ready to use:

```bash
# Basic usage (conceptual - actual usage depends on Claude Code integration)
/research-deep "your research topic"

# Advanced usage with quality controls
/research-deep "AI impact on healthcare" --quality=academic --sources=academic,government

# Status monitoring
/research-status --format=dashboard
```

### Agent Features

- **Specification-Driven**: Follows formal specifications for consistency
- **Quality Assurance**: Built-in quality validation and monitoring
- **Multi-Stage Workflow**: Systematic research process with quality gates
- **Compliance Validation**: Automatic specification compliance checking
- **Error Recovery**: Comprehensive error handling and recovery mechanisms

## Hook Integration

### Automatic Validation

The system includes Claude Code hooks that automatically:

1. **Validate Compliance**: Check specification adherence on file changes
2. **Monitor Quality**: Assess research quality and provide feedback
3. **Handle Commands**: Process research commands with validation

### Hook Configuration

Hooks are configured to integrate with Claude Code's workflow:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/specification_compliance_hook.sh"
          }
        ]
      }
    ]
  }
}
```

## Configuration

### Claude Code Settings

The system works with standard Claude Code configuration in `.claude/settings.json`:

```json
{
  "agents": {
    "deep-research": {
      "enabled": true,
      "quality_checks": true,
      "compliance_validation": true
    }
  },
  "hooks": {
    "compliance_validation": true,
    "quality_monitoring": true
  }
}
```

## Quality Standards

Built-in quality standards ensure enterprise-grade output:

- **Accuracy Rate**: Target 97%, Minimum 90%
- **Source Diversity**: Target 90%, Minimum 70%
- **Bias Mitigation**: Target 88%, Minimum 80%
- **Reproducibility**: Target 95%, Minimum 90%

## Documentation

For comprehensive system documentation, see:

- **System Documentation**: `docs/research/agent-systems/`
- **Getting Started**: `docs/research/agent-systems/implementation/getting-started.md`
- **Architecture Guide**: `docs/research/agent-systems/architecture/system-architecture.md`

## Official References

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Agents](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)

---

This Claude Code configuration provides enterprise-grade multi-agent research capabilities with built-in quality assurance and compliance validation.