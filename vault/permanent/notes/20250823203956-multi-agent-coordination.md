---
date: 2025-08-23
type: zettel
tags: [agents, coordination, distributed-systems, architecture]
status: active
links: ["[[Agent Systems Architecture]]", "[[Research Agent Framework]]", "[[PKM Agent Pipeline]]"]
---

# Multi-Agent Coordination Patterns

Coordination patterns that enable multiple specialized agents to work together effectively in complex knowledge management and research tasks.

## Coordination Models

### 1. Pipeline Pattern
Agents process information sequentially:
- **Ingestion** → **Processing** → **Synthesis** → **Review**
- Each agent transforms and enriches data
- Clear handoff points and interfaces

### 2. Orchestration Pattern
Central coordinator manages agent interactions:
- Workflow engine assigns tasks
- Monitors progress and dependencies
- Handles error recovery and retries

### 3. Collaboration Pattern
Agents work together on shared tasks:
- Parallel processing of large datasets
- Peer review and validation
- Consensus building for quality

## PKM System Implementation

The PKM system uses hybrid coordination:
1. **Research Pipeline**: Deep research → Validation → Synthesis
2. **PKM Pipeline**: Ingestion → Processing → Feynman simplification
3. **Quality Loop**: Continuous peer review across all agents

## Communication Protocols

- **Message Passing**: Structured data exchange
- **Shared State**: Common knowledge graph access
- **Event Streaming**: Real-time notifications
- **Quality Signals**: Confidence scores and validation

## Related Concepts
- [[Distributed Systems Patterns]]
- [[Agent Communication Languages]]
- [[Workflow Orchestration]]
- [[Consensus Algorithms]]