---
date: 2025-08-24
type: zettel
tags: [agent-pools, plan-build-review, specialization, compound-engineering]
links: ["[[202408241600-parallel-compound-engineering-architecture]]", "[[202408241601-event-driven-ce-coordination]]"]
---

# Plan → Build → Review Agent Pool Architecture

## Core Innovation

**Specialized agent pools** replace generic "streams" with **role-specific intelligence**: Planners, Builders, and Reviewers, each optimized for their phase of the compound engineering pipeline.

## Agent Pool Specialization

### Planners Pool
- **Core Function**: Architecture, requirements analysis, system design
- **Agents**: `research` + `synthesis` for comprehensive planning intelligence
- **Events Emitted**: `plan_ready`, `architecture_complete`, `requirements_defined`
- **Intelligence**: Historical pattern recognition, constraint analysis, design optimization

### Builders Pool  
- **Core Function**: Implementation, coding, integration, testing
- **Agents**: `knowledge` + `pkm-processor` for implementation intelligence
- **Events Emitted**: `build_ready`, `implementation_complete`, `integration_done`
- **Intelligence**: Code generation, pattern application, quality assurance during building

### Reviewers Pool
- **Core Function**: Quality validation, testing, approval, security review
- **Agents**: `synthesis` + `pkm-feynman` for comprehensive evaluation
- **Events Emitted**: `review_complete`, `quality_validated`, `approval_granted`
- **Intelligence**: Multi-dimensional quality assessment, risk evaluation, performance validation

## Key Advantages Over Stream Architecture

### 1. **Clear Specialization**
Each pool has **distinct expertise** rather than overlapping responsibilities:
- Planners focus purely on design and architecture
- Builders focus purely on implementation and integration
- Reviewers focus purely on validation and quality

### 2. **Dynamic Resource Allocation**
Pools can **scale independently** based on workload:
- Complex planning phase → More planners activated
- Heavy implementation → Additional builders deployed
- Comprehensive review → Extra reviewers assigned

### 3. **Event-Driven Handoffs**
Clean transitions between phases:
```
Planners.emit("plan_ready") → Builders.activate()
Builders.emit("build_ready") → Reviewers.activate()
Reviewers.emit("approval_granted") → Deploy.proceed()
```

### 4. **Parallel Execution Within Pools**
Multiple agents within each pool work simultaneously:
- Multiple planners can work on different architecture components
- Multiple builders can implement different modules
- Multiple reviewers can validate different quality dimensions

## Implementation Pattern

```python
class AgentPool:
    def __init__(self, pool_type, agent_specs, coordination_bus):
        self.pool_type = pool_type  # planners, builders, reviewers
        self.agents = [spawn_agent(spec) for spec in agent_specs]
        self.coordination_bus = coordination_bus
        
    async def execute_phase(self, task, context):
        # Distribute work across available agents in pool
        subtasks = self.decompose_task(task)
        results = await asyncio.gather(
            *[agent.process(subtask) for agent, subtask in zip(self.agents, subtasks)]
        )
        return self.synthesize_results(results)
```

## Progressive Coordination

**Incremental handoffs** rather than big-bang transfers:
- Planners provide **partial architecture** → Builders start early implementation
- Builders provide **working modules** → Reviewers begin incremental validation
- Reviewers provide **early feedback** → Planners adjust remaining design

## Quality Gates Between Pools

**Synchronized checkpoints** ensure quality progression:
1. **Planning Quality Gate**: Architecture completeness, requirement coverage
2. **Building Quality Gate**: Implementation correctness, integration success  
3. **Review Quality Gate**: Quality validation, performance requirements, security clearance

## Load Balancing and Efficiency

### Intelligent Work Distribution
```python
def assign_task_to_pool(task, pool):
    available_agents = pool.get_available_agents()
    best_agent = pool.select_best_agent_for_task(task, available_agents)
    return best_agent.process(task)
```

### Cross-Pool Learning
- **Planners learn** from builder implementation patterns and reviewer feedback
- **Builders learn** from planner architectural patterns and reviewer quality criteria
- **Reviewers learn** from successful patterns across planning and building phases

## Integration with Claude Code

Maps directly to Claude Code architecture:
- **Agent Pools** → `.claude/agents/ce-planners-pool.md`, etc.
- **Event Coordination** → Hook system with event routing
- **State Management** → Shared workspace coordination
- **Task Distribution** → Task tool for spawning pool agents

## Key Success Pattern

The **Plan → Build → Review** pipeline with specialized pools provides:
1. **Clear Separation of Concerns**: Each pool has distinct responsibilities
2. **Parallel Execution**: Multiple agents per pool enable true parallelization
3. **Progressive Handoffs**: Incremental coordination prevents blocking
4. **Quality Assurance**: Built-in validation at each phase transition

---

**Meta**: This architecture transforms compound engineering from theoretical concept to **implementable system** with clear agent roles, responsibilities, and coordination mechanisms ready for Claude Code deployment.