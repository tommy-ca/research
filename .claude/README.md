# Claude Code Research System

Simple, powerful research agents for Claude Code.

## Quick Start

```bash
# Research any topic
/research "artificial intelligence in healthcare"

# Synthesize multiple sources
/synthesize research1.md research2.md research3.md
```

## Architecture

```
.claude/
├── agents/
│   ├── research.md    # Research + validation (24 lines)
│   └── synthesis.md   # Synthesis + insights (24 lines)
└── hooks/
    └── router.sh      # Simple routing (55 lines)
```

**Total: 103 lines** - Simple, focused, effective.

## Commands

### /research [topic]
Comprehensive research with automatic quality validation.

**What it does:**
- Searches multiple sources
- Validates facts automatically
- Detects and mitigates bias
- Provides confidence scores

**Example:**
```
/research "quantum computing applications"
```

### /synthesize [sources]
Combines multiple sources into unified insights.

**What it does:**
- Integrates information
- Identifies patterns
- Generates frameworks
- Provides recommendations

**Example:**
```
/synthesize report1.md report2.md data.json
```

## How It Works

1. **Command**: You issue a simple command
2. **Routing**: Router directs to appropriate agent
3. **Execution**: Agent performs the task
4. **Output**: Structured results with quality metrics

## Quality Built-In

Every research includes:
- Multi-source validation
- Bias detection
- Confidence scoring
- Source citations

No need for separate quality checks - it's automatic.

## Design Principles

1. **Simplicity First**: 2 commands, not 20
2. **Quality by Default**: No separate validation needed
3. **Minimal Infrastructure**: Hooks simpler than agents
4. **Smart Defaults**: Works great out of the box

## Advanced Usage

### Research Options
The research agent intelligently adapts based on your topic:
- Academic topics → Prioritizes scholarly sources
- Current events → Emphasizes recent sources
- Technical topics → Focuses on authoritative sources

### Synthesis Patterns
The synthesis agent automatically detects:
- Contradictions between sources
- Common themes and patterns
- Gaps in information
- Emerging trends

## Technical Details

For implementation details, see:
- `docs/research/agent-systems/technical/`

## Migration from v1

If upgrading from the previous version:
- `/research-deep` → `/research`
- `/review` + `/quality-check` → Built into `/research`
- `/extract-insights` → Built into `/synthesize`

## Performance

- **89% less code** than v1 (103 vs 1,323 lines)
- **Faster execution** due to simplified routing
- **Same functionality** through intelligent design

---

*Claude Code Research System v2.0 - Simplicity through intelligence*