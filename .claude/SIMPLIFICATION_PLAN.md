# Ultra-Simplification Plan

## Current State Analysis

### 🔴 Critical Issue: Inverted Complexity
- **Agents**: 222 lines (simple, clean)
- **Hooks**: 1,101 lines (5x more complex!)
- **Documentation**: Scattered across multiple directories
- **Commands**: Too many variants and options

This violates the fundamental principle: **infrastructure should be simpler than what it supports**.

## Simplification Strategy

### 1. Agent Consolidation (222 → ~100 lines)

#### Before (3 agents):
- `research.md` (75 lines) - Research & validation
- `review.md` (74 lines) - Quality & review
- `synthesis.md` (73 lines) - Synthesis & insights

#### After (2 agents):
- `research.md` (~50 lines) - All research, validation, and quality checks
- `synthesis.md` (~50 lines) - All synthesis and insight generation

**Rationale**: Quality review is inherent to good research, not a separate process.

### 2. Command Simplification

#### Before (9 commands):
```
/research, /validate, /research-status
/review, /quality-check, /bias-check
/synthesize, /extract-insights, /create-framework
```

#### After (2 commands):
```
/research [topic]     # All research tasks
/synthesize [sources] # All synthesis tasks
```

**Rationale**: Simpler is better. Options can be inferred from context.

### 3. Hook Minimization (1,101 → ~50 lines)

#### Before (3 complex hooks):
- `research_command_handler.sh` (418 lines)
- `quality_check.sh` (188 lines)
- `specification_compliance_hook.sh` (495 lines)

#### After (1 simple hook):
- `router.sh` (~50 lines) - Simple command routing only

**Rationale**: Hooks should route, not validate. Let agents handle their own logic.

### 4. Documentation Consolidation

#### Before:
```
.claude/README.md
.claude/agents/README.md
.claude/agents/MIGRATION.md
docs/research/agent-systems/[multiple directories]
```

#### After:
```
.claude/README.md         # Everything you need
.claude/agents/[agents]   # Simple agent files
```

**Rationale**: One source of truth, easy to find and maintain.

## Implementation Steps

1. **Merge review into research agent** ✓
2. **Simplify command structure** ✓
3. **Replace complex hooks with simple router** ✓
4. **Consolidate documentation** ✓
5. **Test simplified system** ✓

## Expected Outcome

### Metrics:
- **Total Code**: ~150 lines (vs current 1,323 lines) - 89% reduction
- **Complexity**: Minimal - just route and execute
- **Usability**: 2 commands to remember instead of 9
- **Maintainability**: 10x easier

### Final Structure:
```
.claude/
├── README.md           # Complete guide (~100 lines)
├── agents/
│   ├── research.md    # Research + quality (~50 lines)
│   └── synthesis.md   # Synthesis + insights (~50 lines)
└── hooks/
    └── router.sh      # Simple routing (~50 lines)
```

## Principles Applied

1. **Less is More**: Fewer commands, clearer purpose
2. **Convention over Configuration**: Smart defaults, minimal options
3. **Infrastructure < Application**: Hooks simpler than agents
4. **Single Responsibility**: Each component does one thing well
5. **YAGNI**: Remove anything not absolutely necessary

---

This plan achieves **89% code reduction** while maintaining 100% functionality through intelligent consolidation and simplification.