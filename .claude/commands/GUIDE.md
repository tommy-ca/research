# Custom Commands Guide

## Quick Start

### 1. Create Your Command (2 minutes)

```bash
# Copy template
cp .claude/commands/analyze.md .claude/commands/mycommand.md

# Edit with your details
```

### 2. Edit Frontmatter

```yaml
---
name: mycommand
pattern: /mycommand
agent: research  # or synthesis
description: What it does
---
```

### 3. Test

```bash
/mycommand "test input"
```

## How Custom Commands Work

```
User Input → Router → Custom Command → Agent → Results
     ↓         ↓            ↓            ↓         ↓
/mycommand  Matches    Loads config  Processes  Output
           pattern    Routes to agent
```

## Best Practices

### DO ✅
- Keep commands focused (one clear purpose)
- Reuse existing agents
- Provide clear examples
- Use descriptive names
- Keep under 50 lines

### DON'T ❌
- Create new agents
- Add complex logic
- Duplicate existing commands
- Over-configure
- Add parameters to frontmatter

## Command Patterns

### Analysis Pattern
```yaml
name: deep-dive
pattern: /deep-dive
agent: research
description: Deep analysis of specific topic
```
Use when: You need detailed research on a narrow topic

### Comparison Pattern
```yaml
name: versus
pattern: /versus
agent: synthesis
description: Compare two or more items
```
Use when: You need to compare multiple things

### Validation Pattern
```yaml
name: fact-check
pattern: /fact-check
agent: research
description: Verify claims with sources
```
Use when: You need to verify specific claims

## Real Examples

### Industry Analysis Command
```yaml
---
name: industry
pattern: /industry
agent: research
description: Analyze an industry sector
---

# Industry Analysis

Comprehensive industry sector analysis.

## Usage
`/industry "sector name"`

## Example
`/industry "renewable energy"`
```

### Technology Comparison
```yaml
---
name: tech-compare
pattern: /tech-compare
agent: synthesis
description: Compare technologies
---

# Technology Comparison

Compare multiple technologies.

## Usage
`/tech-compare "tech1" "tech2" ...`

## Example
`/tech-compare "kubernetes" "docker swarm"`
```

## Troubleshooting

### Command Not Found
- Check pattern starts with `/`
- Verify file is in `.claude/commands/`
- Ensure frontmatter is valid YAML

### Wrong Agent Behavior
- Research agent: for gathering information
- Synthesis agent: for combining information

### Command Not Loading
- Check YAML syntax
- Verify required fields (name, pattern, agent)
- Look for router.sh logs

## Advanced Tips

### 1. Parameter Hints
While agents handle parameters intelligently, you can guide users:
```markdown
## Usage
`/analyze "topic" "specific-focus"`
                    ↑
            Optional: narrows analysis
```

### 2. Output Formats
Agents adapt output automatically, but you can suggest formats:
```markdown
## Output
- Executive summary
- Detailed findings
- Recommendations
- Confidence scores
```

### 3. Combining Commands
Commands can reference each other:
```bash
/research "quantum computing"
/analyze "research_output.md" "commercial applications"
```

## Philosophy

**"Commands are just routing rules"**

- Commands don't contain logic
- Agents handle all intelligence
- Keep specifications minimal
- Let agents adapt to context

## Need Help?

1. Check existing examples in `.claude/commands/`
2. Test with simple inputs first
3. Use the most appropriate agent
4. Keep it simple

Remember: The agents are intelligent - your command just needs to route to them correctly.