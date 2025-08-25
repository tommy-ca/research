---
date: 2025-08-24
type: zettel
tags: [event-driven, coordination, messaging, parallel-systems]
links: ["[[202408241600-parallel-compound-engineering-architecture]]", "[[202408241603-mcp-native-parallel-agents]]", "[[202408241605-plan-build-review-agent-pools]]"]
---

# Event-Driven Coordination for Compound Engineering

## Core Principle

**Event-driven coordination replaces rigid handoffs** with asynchronous message passing, enabling true parallelization while maintaining synchronization.

## Message Bus Architecture

```python
class CEMessageBus:
    async def coordinate_pipeline(self, project):
        planners.emit("plan_ready") → builders.receive()
                                   → reviewers.receive("preview_mode")
        
        builders.emit("build_ready") → reviewers.receive("full_review")
                                    → planners.receive("feedback")
```

## Event Categories

### Planning Events
- `plan_ready`: Core design complete, builders can begin detailed implementation
- `architecture_complete`: Full architecture defined, builders can start implementation
- `requirements_defined`: Prerequisites mapped, pools can plan around constraints

### Building Events  
- `build_ready`: Implementation complete, reviewers can begin validation
- `implementation_complete`: Core functionality done, reviewers have artifacts to examine
- `integration_done`: Components connected, reviewers can test full system

### Review Events
- `review_complete`: Quality validation finished
- `quality_validated`: Standards met, progression to next phase approved
- `approval_granted`: Final approval given for deployment

### Coordination Events
- `sync_point_reached`: Pool ready for synchronization
- `conflict_detected`: Disagreement between pools requires resolution
- `resolution_needed`: Human or senior agent intervention required

## Claude Code Implementation

Uses file system for event coordination:

```python
class ClaudeCodeEventBus:
    def __init__(self, workspace_path):
        self.workspace = Path(workspace_path)
        self.events_dir = self.workspace / ".ce-events"
        
    async def emit_event(self, stream, event_type, payload):
        event_file = self.events_dir / f"{stream}_{event_type}_{timestamp()}.json"
        await claude_write(event_file, {
            'stream': stream,
            'event_type': event_type, 
            'payload': payload,
            'timestamp': timestamp()
        })
```

## Coordination Patterns

### 1. Broadcast Pattern
One agent pool notifies multiple others:
- Planners complete architecture → Builders AND Reviewers both notified
- Enables parallel preparation and early feedback

### 2. Pipeline Pattern  
Sequential dependency chain:
- Planners → Builders → Reviewers → Deploy
- But with event-driven async messaging instead of blocking handoffs

### 3. Publish-Subscribe Pattern
Agent pools subscribe to relevant event types:
- Reviewers pool subscribes to `build_ready` events
- Planners pool subscribes to `implementation_feedback` events

### 4. Request-Response Pattern
Bidirectional communication for clarification:
- Builders request clarification from Planners
- Reviewers request additional tests from Builders

## Timing Coordination

### Progressive Synchronization
Agent pools don't wait for complete outputs, they consume **incremental progress**:

```
t=0.5h: planners.emit("schema_v1") → builders.start_implementation()
t=1.0h: builders.emit("early_feedback") → planners.refine_schema()  
t=1.5h: reviewers.emit("security_clear") → builders.proceed_with_auth()
```

### Quality Gates as Sync Points
Critical synchronization moments where all agent pools must align:
- Architecture approval before major implementation
- Security clearance before deployment
- Performance validation before release

## Benefits of Event-Driven Approach

1. **Loose Coupling**: Agent pools operate independently, reducing blocking
2. **Asynchronous Progress**: Work continues while waiting for coordination
3. **Scalability**: Additional pools easily integrate through events
4. **Resilience**: Pool failures don't cascade through tight coupling
5. **Observability**: Event history provides audit trail and debugging info

## Key Insight

The **coordination overhead is logarithmic, not linear**. Adding agent pools increases coordination complexity slowly because events are targeted and asynchronous, unlike synchronous coordination that scales exponentially with participants.

---

**Meta**: Event-driven coordination is the **critical enabler** for parallel compound engineering. Without it, parallelization creates chaos. With it, parallelization creates synergy.