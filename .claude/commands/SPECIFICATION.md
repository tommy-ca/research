# Custom Command Specification v1.0

Note: PKM-specific command contracts and routing are specified in
`vault/02-projects/01-pkm-system-meta/specifications/claude-commands-and-subagents.md`.

## Command Format

Custom commands are Markdown files with YAML frontmatter.

### Required Fields
```yaml
---
name: command_name      # Unique identifier
pattern: /command       # Pattern to match (must start with /)
agent: research|synthesis|compound  # Which agent processes the command
---
```

### Optional Fields
```yaml
description: Brief description  # One-line description
parameters: ["param1", "param2"]  # Expected parameters
output_format: structured|text  # Output format hint
```

## File Structure
```markdown
---
name: example
pattern: /example
agent: research
description: Example custom command
---

# Command Name

Brief description of what the command does.

## Usage
`/command [required] [optional]`

## Example
`/command "actual example"`

## Output
- What the command returns
- Format of results
```

## Rules

1. **File Location**: Must be in `.claude/commands/` directory
2. **File Extension**: Must be `.md`
3. **File Size**: Maximum 50 lines
4. **Pattern Format**: Must start with `/`
5. **Agent Selection**: Use existing agents (research, synthesis, or compound)

## Agent Capabilities

### Research Agent
Best for:
- Information gathering
- Fact validation
- Analysis tasks
- Quality assessment

### Synthesis Agent
Best for:
- Combining information
- Pattern recognition
- Comparison tasks
- Framework generation

### Compound Agent
Best for:
- Planning small, testable steps
- Orchestrating multi-agent execution
- Structured critique and fix-forward loops
- Preparing concise PR summaries

## Examples

See:
- `analyze.md` - Focused analysis command
- `compare.md` - Comparison command
- `validate.md` - Validation command
