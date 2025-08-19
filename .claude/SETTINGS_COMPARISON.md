# Settings.json Simplification

## Before (v1): 156 lines of complexity
```json
{
  "agents": {
    "research_agents": {
      "deep_research": {
        "capabilities": [10 items],
        "enhanced_quality_standards": {7 nested settings},
        "performance_targets": {8 metrics},
        "command_support": [7 commands]
      },
      "peer_review": {
        "enhanced_review_standards": {8 settings},
        "review_capabilities": [6 items]
      },
      "synthesis": {
        "synthesis_methods": [6 methods],
        "integration_capabilities": [6 items]
      }
    }
  },
  "hooks": {
    "enhanced_research_commands": {...},
    "advanced_quality_gates": {...},
    "research_monitoring": {...}
  }
}
```

## After (v2): 45 lines of clarity
```json
{
  "agents": {
    "research": {
      "enabled": true,
      "description": "Intelligent research with built-in quality validation",
      "tools": ["WebSearch", "WebFetch", "Read", "Write", "Grep"]
    },
    "synthesis": {
      "enabled": true,
      "description": "Information synthesis with automatic insight extraction", 
      "tools": ["Read", "Write", "Edit"]
    }
  },
  "hooks": {
    "router": {
      "UserPromptSubmit": {
        "match": "/research|/synthesize",
        "script": ".claude/hooks/router.sh"
      }
    }
  }
}
```

## Key Improvements

### 71% Reduction
- **Before**: 156 lines
- **After**: 45 lines
- **Savings**: 111 lines removed

### Eliminated Complexity
- ❌ 31 capability definitions
- ❌ 23 quality standards
- ❌ 8 performance metrics
- ❌ 7 command variations
- ❌ 3 complex hooks
- ❌ Model-specific configurations
- ❌ Environment variables

### What Remains
- ✅ 2 agent definitions
- ✅ 1 simple hook
- ✅ Essential permissions
- ✅ Clear project info

## Philosophy

**Before**: Configuration attempting to control intelligence
**After**: Configuration enabling intelligent agents

The agents are smart enough to handle quality, validation, and optimization internally. Configuration should enable, not constrain.