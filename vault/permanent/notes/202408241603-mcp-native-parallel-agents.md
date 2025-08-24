---
date: 2025-08-24
type: zettel
tags: [mcp, claude-code, parallel-agents, native-integration]
links: ["[[202408241600-parallel-compound-engineering-architecture]]", "[[202408241601-event-driven-ce-coordination]]"]
---

# MCP-Native Parallel Agents for Compound Engineering

## Core Innovation

**MCP-native parallel agents** use Claude Code's Model Context Protocol patterns to achieve true parallelization with intelligent coordination, leveraging native capabilities rather than fighting against them.

## Agent Architecture

### Stream Agent Pattern
```yaml
# MCP Stream Agent Template
---
name: ce-planning-stream
description: MCP-native planning stream for parallel compound engineering
tools: [Task, Read, Write, Grep, WebSearch]
mcp_pattern: stream_agent
parent_coordination: ce-coordinator
---
```

Each stream agent:
- **Operates independently** using Claude Code tools
- **Coordinates through events** via shared workspace
- **Spawns sub-agents** using Task tool for specialized work
- **Integrates with PKM** for knowledge retrieval and capture

### Coordination Hierarchy
```
ce-coordinator (Master)
├── ce-planning-stream (Independent)
├── ce-execution-stream (Independent) 
├── ce-review-stream (Independent)
└── ce-state-manager (Shared State)
```

## MCP Coordination Patterns

### Parallel Task Spawning
```python
class MCPParallelCEOrchestrator:
    async def spawn_parallel_streams_mcp(self, goal):
        # Create MCP coordination context
        context = await self.setup_mcp_context(goal)
        
        # Spawn streams with MCP coordination
        planning_stream = await self.spawn_mcp_agent(
            agent_type="ce-planning-stream",
            context=context,
            coordination_config={
                "event_targets": ["ce-execution-stream", "ce-review-stream"],
                "state_sharing": True,
                "pkm_integration": True
            }
        )
```

Uses Claude Code's **Task tool** as the primary mechanism for parallel agent spawning, with native MCP patterns for coordination.

### State Synchronization
```yaml
shared_state:
  workspace_root: ".ce-workspace/"
  
  coordination:
    events_dir: ".ce-workspace/.events/"
    state_dir: ".ce-workspace/.state/" 
    progress_dir: ".ce-workspace/.progress/"
    conflicts_dir: ".ce-workspace/.conflicts/"
  
  stream_states:
    planning: {phase: "architecture_design", status: "active"}
    execution: {phase: "implementation", status: "waiting"}
    review: {phase: "quality_validation", status: "waiting"}
```

**MCP State Management**:
- **Atomic Updates**: File locks prevent race conditions
- **Event-Driven**: State changes trigger coordination events  
- **Conflict Detection**: Automatic detection and resolution
- **PKM Integration**: State changes captured as insights

## Agent Specializations

### CE Planning Stream Agent
- **Parent Agents**: `research` + `synthesis`
- **Responsibilities**: Architecture design, requirement analysis, dependency mapping
- **Coordination**: Emits `architecture_ready`, `dependencies_identified` events
- **PKM Integration**: Queries historical architectures, captures design decisions

### CE Execution Stream Agent  
- **Parent Agents**: `knowledge` + `pkm-processor`
- **Responsibilities**: Implementation, testing, integration
- **Coordination**: Emits `code_ready`, `tests_complete` events
- **PKM Integration**: Retrieves implementation patterns, captures solution approaches

### CE Review Stream Agent
- **Parent Agents**: `synthesis` + `pkm-feynman`
- **Responsibilities**: Quality validation, security review, performance testing
- **Coordination**: Emits `quality_validated`, `security_cleared` events
- **PKM Integration**: Applies quality criteria, captures improvement patterns

## MCP Hook Integration

```bash
# .claude/hooks/mcp-parallel-router.sh
case "$COMMAND" in
    /ce-parallel-plan*)
        echo "🛠️ Parallel CE Planning activated"
        echo "Agent: compound-parallel"
        echo "Mode: parallel_orchestration" 
        echo "MCP: event_coordination_enabled"
        ;;
        
    /ce-parallel-exec*)
        echo "⚡ Parallel CE Execution activated"
        echo "Agent: ce-coordinator"
        echo "Mode: stream_coordination"
        echo "MCP: parallel_task_spawning"
        ;;
esac
```

Router recognizes MCP patterns and activates appropriate coordination mechanisms.

## Native Tool Integration

### Task Tool Usage
- **Primary Mechanism**: Spawn parallel agent streams
- **Background Execution**: Long-running coordination processes
- **Sub-Agent Spawning**: Specialized work within streams
- **Exception Handling**: Graceful failure management

### File System Coordination
- **Read/Write/Edit**: Event and state management via files
- **Grep**: Event filtering and pattern matching
- **Directory Structure**: Organized workspace for coordination

### Web Integration
- **WebSearch/WebFetch**: Enhanced research in planning stream
- **Real-time Information**: Current best practices and patterns
- **Validation Data**: External quality standards and benchmarks

## Configuration Management

```json
# .claude/settings.json (enhanced)
{
  "agents": {
    "compound-parallel": {
      "enabled": true,
      "mcp_capabilities": ["parallel_task_spawning", "event_coordination", "state_management"]
    },
    
    "ce-planning-stream": {
      "enabled": true,
      "parent_agents": ["research", "synthesis"],
      "coordination": "event_driven"
    },
    
    "ce-coordinator": {
      "enabled": true,
      "coordination": "orchestrator",
      "state_management": "master_control"
    }
  }
}
```

## Key Benefits of MCP-Native Approach

1. **Native Performance**: Uses Claude Code's optimized execution paths
2. **Tool Integration**: Leverages existing tool ecosystem seamlessly  
3. **Agent Reuse**: Builds on existing research/synthesis/knowledge agents
4. **Backward Compatibility**: Existing workflows continue working
5. **Scalability**: MCP patterns handle coordination complexity efficiently

## Coordination Protocol Example

```python
# MCP Event Patterns
planning_events = {
    "architecture_ready": {
        "targets": ["ce-execution-stream", "ce-review-stream"],
        "payload": {"architecture_doc", "dependencies", "constraints"}
    },
    "requirements_clarified": {
        "targets": ["ce-execution-stream"], 
        "payload": {"requirements_spec", "acceptance_criteria"}
    },
    "planning_blocked": {
        "targets": ["ce-coordinator"],
        "payload": {"blocker_type", "resolution_needed", "priority"}
    }
}
```

Events follow MCP patterns with structured payloads and targeted routing.

## Critical Success Factor

The **MCP-native approach** ensures parallel CE works **with** Claude Code's architecture rather than against it. This provides:
- **Reliability**: Uses tested, stable coordination patterns
- **Performance**: Optimized for Claude Code's execution model
- **Maintainability**: Follows established patterns and conventions
- **Extensibility**: Easy to add new streams and coordination mechanisms

---

**Meta**: MCP-native parallel agents represent the **optimal integration** between parallel compound engineering concepts and Claude Code's native capabilities. The result is a system that achieves true parallelization while remaining stable, performant, and extensible.