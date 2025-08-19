# Claude Code Agents

Simple, focused agents for research and analysis tasks.

## Available Agents

### 🔬 Research Agent (`research.md`)
- **Purpose**: Comprehensive research and information gathering
- **Commands**: `/research`, `/validate`, `/research-status`
- **Capabilities**: Multi-source research, fact validation, bias detection

### ✅ Review Agent (`review.md`)
- **Purpose**: Quality assurance and peer review
- **Commands**: `/review`, `/quality-check`, `/bias-check`
- **Capabilities**: Quality scoring, bias detection, methodology evaluation

### 🔄 Synthesis Agent (`synthesis.md`)
- **Purpose**: Information synthesis and insight generation
- **Commands**: `/synthesize`, `/extract-insights`, `/create-framework`
- **Capabilities**: Pattern recognition, framework development, insight extraction

## Usage

Agents are designed to work independently or together:

```bash
# Single agent usage
/research "quantum computing applications"

# Multi-agent workflow
/research "AI in healthcare" --depth=comprehensive
/review [research output]
/synthesize [reviewed content]
```

## Design Principles

1. **Simplicity**: Each agent has a clear, focused purpose
2. **Modularity**: Agents can work independently or together
3. **Clarity**: Commands are intuitive and well-documented
4. **Quality**: Built-in validation and quality checks

## Technical Specifications

For detailed technical specifications and implementation details, see:
- `docs/research/agent-systems/specifications/`
- `docs/research/agent-systems/technical/`

## Migration from Legacy Agents

See `MIGRATION.md` for guidance on transitioning from the old verbose agents to the new simplified versions.