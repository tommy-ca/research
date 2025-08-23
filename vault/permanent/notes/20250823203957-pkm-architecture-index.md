---
date: 2025-08-23
type: zettel
tags: [index, architecture, pkm, documentation]
status: active
links: ["[[202401210001-pkm-dogfooding]]", "[[20250823203953-diskless-lakehouse-architecture]]", "[[20250823203954-dual-interface-pkm]]", "[[20250823203955-specification-driven-development]]", "[[20250823203956-multi-agent-coordination]]"]
---

# PKM Architecture Documentation Index

Central index for all PKM system architecture documentation, organizing concepts by domain and implementation layer.

## Storage Architecture
- [[20250823203953-diskless-lakehouse-architecture]] - Cloud-native storage backend
- [[Transparent Storage Backend]] - S3 + Iceberg + SlateDB + Lance integration
- [[ACID Transactions in PKM]] - Transactional guarantees for knowledge operations

## Interface Architecture
- [[202408220442-dual-interface-architecture]] - Original dual interface concept
- [[20250823203954-dual-interface-pkm]] - Extended PKM-specific implementation
- [[Natural Language Commands]] - Slash command system
- [[Markdown File Interface]] - Direct text manipulation

## Development Methodology
- [[202401210002-tdd-specs-principles]] - Core TDD and specs principles
- [[20250823203955-specification-driven-development]] - Formal SDD framework
- [[FR-First Development]] - Functional requirements prioritization
- [[Quality Gates]] - Validation checkpoints

## Agent Architecture
- [[20250823203956-multi-agent-coordination]] - Agent interaction patterns
- [[Research Agent Framework]] - Deep research capabilities
- [[PKM Agent Pipeline]] - Ingestion → Processing → Synthesis
- [[Agent Communication Protocols]] - Message passing and state sharing

## Implementation Status
- Active development using diskless lakehouse
- Four specialized Claude Code agents deployed
- Dual interface operational
- Continuous dogfooding in progress

## Related Documentation
- Source: `vault/04-resources/architecture/`
- Specifications: `vault/04-resources/architecture/agent-systems/specifications/`
- Implementation Guides: `.claude/agents/`